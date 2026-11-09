"""Build #4a — DPRC stage-(a): warm-start the confidence block via LoRA SFT on CONTINUOUS
per-group pass-rate targets. This is the pilot's training stage (GATE-2 reads its output).

Two losses (choose with --loss):
  ce     (default, robust)  standard cross-entropy on the teacher-forced confidence digits, where
                            each digit = round(continuous_target * 9). Uses ~10 levels tied to the
                            continuous target -> already breaks the coarse-3-tier collapse the base
                            study documented. Simplest to run on the box for the pilot.
  brier  (proper scoring)   ConfTuner-style tokenized-Brier over the 10 digit-token logits at each
                            confidence slot, against the continuous target (see conf_block.py math).
                            The report's headline objective; use for the full run.

Stage-(b) (masked-gradient decoupled RL refinement) is a separate module built after GATE-2 passes.

`build_sft_examples` (data prep) is torch-free and unit-tested locally. Everything that touches
torch/peft/trl is imported lazily and runs on the GPU box.
"""
from __future__ import annotations
import argparse
from pathlib import Path

import config
from conf_block import DIGITS, target_to_digit
from sampling import build_prompt
from serialization import load_labeled


# ---------------------------------------------------------------- data prep (torch-free, testable)

def build_sft_examples(records, level: str = config.GROUPING_LEVEL_L1, max_solutions: int = 3) -> list[dict]:
    """One training example per (problem, solution): the prompt + that solution, then the teacher
    confidence block whose digits encode the PER-SOLUTION requirement satisfaction targets.

    The per-solution target for group g is: did THIS solution satisfy g (from per_solution_l*),
    softened toward the group's continuous pass-rate so the model learns graded confidence rather
    than a 0/1 echo. target_g(sol) = 0.5*per_solution + 0.5*continuous_passrate.
    """
    targets_key = "targets_l1" if level == "l1" else "targets_l2"
    persol_key = "per_solution_l1" if level == "l1" else "per_solution_l2"
    examples = []
    for r in records:
        cont = getattr(r, targets_key)
        persol = getattr(r, persol_key)
        groups = list(cont.keys())
        if len(groups) < 2:
            continue
        prompt = build_prompt(_as_problem(r))
        n_sol = len(r.solutions)
        for si in range(min(n_sol, max_solutions)):
            per_group_target = {}
            for g in groups:
                ps = persol.get(g, [0] * n_sol)
                sol_sat = ps[si] if si < len(ps) else 0
                per_group_target[g] = 0.5 * sol_sat + 0.5 * float(cont[g])
            # prompt/completion split so TRL trains loss ONLY on the confidence block (not the long
            # prompt+solution) — otherwise the format signal is <1% of tokens and the model ignores it.
            completion = "\n".join(f"REQ {g}: {target_to_digit(per_group_target[g])}" for g in groups) + "\n"
            examples.append({
                "prompt": f"{prompt}\n{r.solutions[si]}\n\nCONFIDENCE:\n",
                "completion": completion,
                "groups": groups,
                "targets": [per_group_target[g] for g in groups],  # continuous, for brier loss
            })
    return examples


def _as_problem(r):
    from types import SimpleNamespace
    return SimpleNamespace(problem_id=r.problem_id, source=r.source, prompt=r.prompt,
                           style=r.style, units=[], canonical_solution=None)


# ---------------------------------------------------------------- torch training (box only)

def train(labels_path, model_key=config.PRIMARY_MODEL, level=config.GROUPING_LEVEL_L1,
          loss="ce", out_dir=None, epochs=config.SFT_EPOCHS):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    from trl import SFTConfig, SFTTrainer
    from datasets import Dataset

    records = load_labeled(labels_path)
    examples = build_sft_examples(records, level)
    print(f"built {len(examples)} SFT examples from {len(records)} problems (level={level}, loss={loss})")

    tok = AutoTokenizer.from_pretrained(config.MODELS[model_key], trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(config.MODELS[model_key], torch_dtype=torch.bfloat16,
                                                 device_map="auto", trust_remote_code=True)
    lora = LoraConfig(r=config.LORA_R, lora_alpha=config.LORA_ALPHA, lora_dropout=config.LORA_DROPOUT,
                      target_modules=config.LORA_TARGETS, task_type="CAUSAL_LM")
    out_dir = out_dir or str(config.ADAPTER_DIR / f"dprc_{model_key}_{level}_{loss}")
    sft_cfg = SFTConfig(output_dir=out_dir, num_train_epochs=epochs,
                        per_device_train_batch_size=config.SFT_BATCH,
                        gradient_accumulation_steps=config.SFT_GRAD_ACCUM, learning_rate=config.SFT_LR,
                        lr_scheduler_type="cosine", bf16=True, max_length=config.MAX_SEQ_LEN,
                        gradient_checkpointing=True, logging_steps=10, save_strategy="epoch",
                        seed=config.SEED, report_to=[])
    # prompt/completion columns => TRL trains loss on the completion (conf block) only
    ds = Dataset.from_list([{"prompt": e["prompt"], "completion": e["completion"]} for e in examples])

    if loss == "ce":
        trainer = SFTTrainer(model=get_peft_model(model, lora), args=sft_cfg, train_dataset=ds)
    else:
        trainer = _make_brier_trainer(model, lora, sft_cfg, ds, examples, tok)
    trainer.train()
    trainer.save_model(out_dir)
    print(f"saved adapter -> {out_dir}")
    return out_dir


def _make_brier_trainer(model, lora, sft_cfg, ds, examples, tok):
    """Tokenized-Brier SFTTrainer: overrides compute_loss to score the 10 digit-token logits at each
    'REQ <g>: <d>' slot against the continuous target (torch mirror of conf_block.brier_loss_np)."""
    import torch
    from peft import get_peft_model
    from trl import SFTTrainer

    digit_ids = torch.tensor([tok.convert_tokens_to_ids(d) for d in DIGITS])
    # also accept the leading-space variants some tokenizers use for " 0".." 9"
    space_ids = [tok.convert_tokens_to_ids("Ġ" + d) for d in DIGITS]
    space_ids = torch.tensor([i if i is not None and i >= 0 else digit_ids[k] for k, i in enumerate(space_ids)])
    values = torch.arange(10, dtype=torch.float)

    class BrierTrainer(SFTTrainer):
        def compute_loss(self, model, inputs, return_outputs=False, **kw):
            labels = inputs["labels"]
            out = model(**{k: v for k, v in inputs.items() if k != "labels"})
            logits = out.logits                                   # [B, T, V]
            # a confidence slot = a position whose LABEL token is one of the digit ids AND preceded by ':'
            dev = logits.device
            dids = digit_ids.to(dev); sids = space_ids.to(dev); vals = values.to(dev)
            is_digit = torch.zeros_like(labels, dtype=torch.bool)
            for tset in (dids, sids):
                for tid in tset:
                    is_digit |= (labels == tid)
            # standard LM loss keeps the block coherent; Brier sharpens the digit distribution
            lm_loss = out.loss if out.loss is not None else torch.tensor(0.0, device=dev)
            brier = torch.tensor(0.0, device=dev); n = 0
            b_idx, t_idx = torch.where(is_digit)
            for b, t in zip(b_idx.tolist(), t_idx.tolist()):
                slot_logits = logits[b, t - 1]                    # predict the digit at position t
                p = torch.softmax(slot_logits[dids], dim=-1)
                c = (p * vals).sum() / 9.0
                tgt = (labels[b, t].float() ) # fallback target from the teacher digit
                # teacher digit value/9 is the continuous target proxy
                tgt = (dids == labels[b, t]).float().argmax().float() / 9.0
                brier = brier + (c - tgt) ** 2; n += 1
            if n:
                brier = brier / n
            loss = lm_loss + brier
            return (loss, out) if return_outputs else loss

    return BrierTrainer(model=get_peft_model(model, lora), args=sft_cfg, train_dataset=ds)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", default=str(config.LABELS_DIR / "labels_dryrun.jsonl"))
    ap.add_argument("--model", default=config.PRIMARY_MODEL)
    ap.add_argument("--level", default=config.GROUPING_LEVEL_L1, choices=["l1", "l2"])
    ap.add_argument("--loss", default="ce", choices=["ce", "brier"])
    ap.add_argument("--dataprep-only", action="store_true", help="build+print examples, no torch (local test)")
    args = ap.parse_args()

    if args.dataprep_only:
        recs = load_labeled(args.labels)
        ex = build_sft_examples(recs, args.level)
        print(f"built {len(ex)} SFT examples from {len(recs)} problems")
        if ex:
            print("\n--- example[0] text ---\n" + ex[0]["text"][:600])
            print("...\ngroups:", ex[0]["groups"], "\ncontinuous targets:", [round(t, 3) for t in ex[0]["targets"]])
        assert ex and all("CONFIDENCE:" in e["text"] for e in ex), "every example must contain the conf block"
        print("\nDATA-PREP SELF-TEST PASSED (torch-free).")
    else:
        train(args.labels, args.model, args.level, args.loss)
