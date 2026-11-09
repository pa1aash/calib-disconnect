"""Tests for tools/prose_lint.py. Every category has a hit and a permitted non-hit."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "prose_lint.py"


def cats(findings, severity=None):
    return [f.category for f in findings if severity is None or f.severity == severity]


def has(findings, cat):
    return cat in cats(findings)


# ---- 1. negation_not_but ---------------------------------------------------
@pytest.mark.parametrize("text", [
    "The gap is not a bias but a variance effect.",
    "The gap is not a bias, but a variance effect.",
    "The method is not merely faster.",
    "The method is not simply faster.",
    "The method is not only faster but also safer.",
    "The method is not just faster but safer.",
    "It is not A, not B, but C.",
])
def test_not_but_hits(lint, text):
    assert has(lint(text), "negation_not_but")


@pytest.mark.parametrize("text", [
    "The method is not fast.",
    "We use only the small split but many seeds.",
    "The method is only faster.",
])
def test_not_but_nonhits(lint, text):
    assert not has(lint(text), "negation_not_but")


# ---- 2. negation_cascade ---------------------------------------------------
def test_cascade_hit(lint):
    text = ("The score is not a rank. It never uses labels. Nor does it need a model. "
            "The score measures error.")
    f = lint(text)
    assert has(f, "negation_cascade")
    assert [x for x in f if x.category == "negation_cascade"][0].severity == "WARN"


def test_cascade_nonhit(lint):
    text = "The score is not a rank. It uses labels. It never needs a model. The score measures error."
    assert not has(lint(text), "negation_cascade")


# ---- 3. rather_than --------------------------------------------------------
def test_rather_than_required_example(lint):
    f = lint("We estimate the size conservatively rather than exactly.")
    assert cats(f).count("rather_than") == 1
    assert [x for x in f if x.category == "rather_than"][0].severity == "WARN"
    assert cats(f, "HARD") == []
    assert not has(f, "softening_adverb")


def test_rather_alone_is_softener_not_rather_than(lint):
    f = lint("The result is rather large.")
    assert has(f, "softening_adverb") and not has(f, "rather_than")


# ---- 4. significance announcers -------------------------------------------
@pytest.mark.parametrize("text", [
    "It is worth noting that the gap shrinks.",
    "It is worth pausing on the gap.",
    "It is important to check the gap.",
    "Crucially, the gap shrinks.",
    "Notably, the gap shrinks.",
    "The key point is the gap.",
    "What matters here is the gap.",
    "Importantly, the gap shrinks.",
])
def test_significance_hits(lint, text):
    f = lint(text)
    assert has(f, "significance_announcer")
    assert [x for x in f if x.category == "significance_announcer"][0].severity == "HARD"


def test_significance_nonhit(lint):
    assert not has(lint("The gap shrinks from 3 to 2 points."), "significance_announcer")


def test_significantly_is_warn(lint):
    f = lint("The gap is significantly lower.")
    assert [x.severity for x in f if x.category == "significantly"] == ["WARN"]
    assert not has(lint("The gap is large."), "significantly")


# ---- 5. roadmap ------------------------------------------------------------
@pytest.mark.parametrize("text", [
    "In this section we build the estimator.",
    "The rest of this paper is short.",
    "The remainder of this paper covers the proof.",
    "This paper is organized as follows.",
    "Section~\\ref{sec:x} shows the effect.",
    "Sec.~\\ref{sec:x} describes the data.",
    "Table~\\ref{tab:x} collects the findings.",
    "Table 2 summarizes the findings.",
    "We first fit the model and then score it.",
    "Below we define the score.",
    "\\S~\\ref{sec:x} presents the proof.",
    "\\Cref{sec:setup} discusses the setup.",
])
def test_roadmap_hits(lint, text):
    f = lint(text)
    assert has(f, "roadmap"), text


def test_roadmap_nonhit(lint):
    f = lint("Figure~\\ref{fig:a} plots the curve. We fit the model, then score it.")
    assert not has(f, "roadmap")


# ---- 6. softening adverbs and contradictory pairs -------------------------
@pytest.mark.parametrize("word", [
    "arguably", "somewhat", "fairly", "quite", "perhaps", "seemingly", "essentially",
    "virtually", "largely", "generally", "typically", "usually", "roughly",
    "comfortably", "clearly", "actually", "exactly", "almost", "nearly", "really",
    "relatively", "effectively", "particularly", "Rather",
])
def test_softening_hits(lint, word):
    f = lint(f"The gap is {word} small.")
    assert has(f, "softening_adverb")
    assert [x.severity for x in f if x.category == "softening_adverb"] == ["WARN"]


def test_softening_nonhits(lint):
    assert not has(lint("The real data show a gap."), "softening_adverb")
    assert not has(lint("The gap is small."), "softening_adverb")


@pytest.mark.parametrize("pair", [
    "almost exactly", "essentially always", "nearly always", "virtually all",
    "almost always",
])
def test_contradictory_pairs(lint, pair):
    f = lint(f"The results match {pair} here.")
    assert has(f, "contradictory_pair")
    assert [x.severity for x in f if x.category == "contradictory_pair"] == ["HARD"]
    assert not has(f, "softening_adverb")  # no double counting


def test_contradictory_nonhit(lint):
    assert not has(lint("The results match exactly."), "contradictory_pair")


# ---- 7. clefts -------------------------------------------------------------
def test_cleft_what(lint):
    f = lint("Data are scarce. What this shows is the gap.")
    assert has(f, "cleft_what")
    assert not has(lint("We ask a question. What is calibration?"), "cleft_what")
    assert not has(lint("This shows what the gap is."), "cleft_what")


def test_cleft_it_that(lint):
    f = lint("It is this gap that matters.")
    assert [x.severity for x in f if x.category == "cleft_it_that"] == ["WARN"]
    assert not has(lint("It is known that the gap exists."), "cleft_it_that")
    assert not has(lint("The gap is where it matters."), "cleft_it_that")


def test_cleft_there(lint):
    f = lint("There is a gap which matters.")
    assert [x.severity for x in f if x.category == "cleft_there_which"] == ["WARN"]
    assert not has(lint("There is a gap."), "cleft_there_which")


# ---- 8. headings -----------------------------------------------------------
@pytest.mark.parametrize("cmd", [
    "\\section{Calibration: a review}",
    "\\section{Is it calibrated?}",
    "\\section{Models, Data, and Metrics}",
    "\\section{Models, Data and Metrics}",
    "\\subsection{Calibration revisited}",
    "\\subsection{Calibration, revisited}",
    "\\subsection{Results in full}",
    "\\subsection{Method, in detail}",
    "\\subsection*{Setup in detail}",
    "\\paragraph{Models, Data, and Metrics}",
])
def test_heading_hits(lint, cmd):
    f = lint(cmd + "\nBody text goes here.")
    assert has(f, "heading"), cmd
    assert [x.severity for x in f if x.category == "heading"][0] == "HARD"


@pytest.mark.parametrize("cmd", [
    "\\section{Results and Discussion}",
    "\\section{Calibration metrics}",
    "\\subsection[Short]{Expected calibration error}",
    "\\section{Setup, results}",
])
def test_heading_nonhits(lint, cmd):
    assert not has(lint(cmd + "\nBody text goes here."), "heading")


# ---- 9. captions -----------------------------------------------------------
def test_caption_four_sentences(lint):
    body = ("\\begin{figure}\\caption{One is here. Two is here. Three is here. Four is here.}"
            "\\end{figure}")
    assert has(lint(body), "caption_length")


def test_caption_three_short_sentences(lint):
    body = ("\\begin{figure}\\caption{One is here. Two is here. Three is here.}"
            "\\end{figure}")
    assert not has(lint(body), "caption_length")


def test_caption_sixty_one_words_two_sentences(lint):
    s1 = " ".join(["word"] * 30) + "."
    s2 = " ".join(["term"] * 31) + "."
    body = "\\begin{figure}\n\\caption{" + s1 + " " + s2 + "}\n\\end{figure}"
    f = lint(body)
    assert has(f, "caption_length")
    s2b = " ".join(["term"] * 30) + "."
    body = "\\begin{figure}\n\\caption{" + s1 + " " + s2b + "}\n\\end{figure}"
    assert not has(lint(body), "caption_length")


def test_caption_multiline_nested_braces(lint):
    body = ("\\begin{table}\n\\caption{Scores of \\textbf{three {nested}} models.\n"
            "Second sentence here. Third one. Fourth one.}\n\\end{table}")
    assert has(lint(body), "caption_length")


def test_caption_text_mode(lint):
    f = lint("Figure 1: One is here. Two is here. Three is here. Four is here.\n", mode="text")
    assert has(f, "caption_length")
    f = lint("Figure 1: One is here. Two is here.\n", mode="text")
    assert not has(f, "caption_length")


# ---- 10. short paragraph end ----------------------------------------------
def test_short_paragraph_end(lint):
    body = ("The estimator is fitted on a held-out split of the data with ten folds "
            "and a fixed seed for every run. The fit is stable.")
    f = lint(body)
    assert [x.severity for x in f if x.category == "short_paragraph_end"] == ["WARN"]


def test_short_paragraph_end_nonhits(lint):
    long_end = ("The estimator is fitted on a held-out split. "
                "The resulting scores are then compared across all ten folds and seeds.")
    assert not has(lint(long_end), "short_paragraph_end")
    assert not has(lint("The fit is stable."), "short_paragraph_end")  # one sentence skipped


# ---- 11. internal labels, process words, paths, identifiers ---------------
def test_internal_label(lint):
    assert has(lint("Claim C1 holds for all models."), "internal_label")
    assert has(lint("See L2 and B1 and W3."), "internal_label")
    assert not has(lint("We train on A100 and H100 GPUs."), "internal_label")
    assert not has(lint("Claim $C_1$ holds."), "internal_label")
    assert not has(lint("Claim $C1$ holds."), "internal_label")
    assert not has(lint("See Section~\\ref{sec:C1} for details."), "internal_label")
    assert not has(lint("We use GPT4 and T4 and F1."), "internal_label")


def test_process_word(lint):
    for w in ["session", "Sessions", "wave", "waves", "gate", "Gates"]:
        assert has(lint(f"The {w} was long."), "process_word"), w
    assert not has(lint("The assessment was long."), "process_word")
    assert not has(lint("The gateway opened."), "process_word")


def test_file_path(lint):
    for t in ["See results/main.json for numbers.", "Run run_all.py now.", "Open data.csv now.",
              "Edit paper/main.tex now.", "See notes.md now.", "Edit cfg.toml now."]:
        assert has(lint(t), "file_path"), t
    for t in ["Use input/output pairs.", "The ratio is 3/4.", "True/False labels, e.g. yes.",
              "See \\url{https://example.org/a/b.html} for details."]:
        assert not has(lint(t), "file_path"), t


def test_underscore_identifier(lint):
    assert has(lint("The run exp\\_v3\\_all finished."), "underscore_identifier")
    assert has(lint("The variable exp_v3_all finished.", mode="text"), "underscore_identifier")
    assert not has(lint("The run \\texttt{exp\\_v3\\_all} finished."), "underscore_identifier")
    assert not has(lint("The run $x_i$ finished."), "underscore_identifier")
    assert not has(lint("The run finished."), "underscore_identifier")


# ---- 12. decimals ----------------------------------------------------------
def test_decimal(lint):
    assert has(lint("The accuracy is 0.82 overall."), "decimal_in_prose")
    assert has(lint("The rate is .5 overall."), "decimal_in_prose")
    assert has(lint("The rate is 12.5% overall."), "decimal_in_prose")
    assert not has(lint("The accuracy is $0.5$ overall."), "decimal_in_prose")
    assert not has(lint("The accuracy is \\num{0.82} overall."), "decimal_in_prose")
    assert not has(lint("The accuracy is \\result{0.82} overall."), "decimal_in_prose")
    assert not has(lint("The accuracy is 82 percent overall."), "decimal_in_prose")
    assert not has(lint("See Section 4.2 for the proof."), "decimal_in_prose")


def test_decimal_tables_skipped_by_default(lint, cfg):
    body = ("\\begin{table}\n\\begin{tabular}{lc}\nA & 0.82 \\\\\n\\end{tabular}\n"
            "\\caption{Accuracy of 0.82.}\n\\end{table}")
    f = lint(body)
    lines = [x for x in f if x.category == "decimal_in_prose"]
    assert len(lines) == 1  # only the caption
    cfg2 = dict(cfg)
    cfg2["options"] = dict(cfg["options"], decimal_skip_tables=False)
    import prose_lint
    f2 = prose_lint.lint_text("\\begin{document}\n" + body + "\n\\end{document}\n", "latex", cfg2, "x")
    assert len([x for x in f2 if x.category == "decimal_in_prose"]) == 2


# ---- 13. p-value and Monte Carlo precision --------------------------------
def test_pvalue(lint):
    assert not has(lint("We find p = 0.012 here."), "pvalue_precision")
    assert has(lint("We find p = 0.0123 here."), "pvalue_precision")
    assert has(lint("We find $p = 0.0123$ here."), "pvalue_precision")
    assert has(lint("We find $p<0.0123$ here."), "pvalue_precision")
    assert has(lint("A p-value of 0.0123 results."), "pvalue_precision")
    assert not has(lint("We find $p < 0.001$ here."), "pvalue_precision")
    assert has(lint("We find $p = 1.23\\times10^{-4}$ here."), "pvalue_precision")
    assert has(lint("We find p = 1.23e-4 here."), "pvalue_precision")
    assert not has(lint("We find $p = 5\\times10^{-4}$ here."), "pvalue_precision")
    assert not has(lint("% p = 0.0123 in a comment\nText only."), "pvalue_precision")


def test_mc_precision(lint):
    f = lint("The Monte Carlo estimate is 0.04321 across draws.")
    assert [x.severity for x in f if x.category == "mc_precision"] == ["WARN"]
    assert not has(lint("The Monte Carlo estimate is 0.04 across draws."), "mc_precision")
    assert not has(lint("The estimate is 0.04321 across draws."), "mc_precision")
    assert not has(lint("The Monte Carlo test uses 9999 draws."), "mc_precision")


# ---- 14. British spelling --------------------------------------------------
@pytest.mark.parametrize("word", ["colour", "modelling", "optimise", "behaviour", "centre",
                                  "whilst", "grey", "Normalisation", "tokeniser", "judgement"])
def test_british_hits(lint, word):
    assert has(lint(f"The {word} is clear."), "british_spelling"), word


@pytest.mark.parametrize("word", ["precise", "advise", "compromise", "exercise", "surprise",
                                  "enterprise", "promise", "noise", "rise", "concise",
                                  "expertise", "premise", "otherwise", "wise", "dialogue",
                                  "towards", "analyses", "color", "modeling"])
def test_british_nonhits(lint, word):
    assert not has(lint(f"The {word} is stated."), "british_spelling"), word


def test_british_list_size(cfg):
    assert len(cfg["british_spellings"]) >= 60


# ---- 15. em-dash -----------------------------------------------------------
def test_em_dash(lint):
    assert has(lint("The gap \u2014 small as it is \u2014 matters."), "em_dash")
    assert has(lint("The gap --- small as it is --- matters."), "em_dash")
    assert not has(lint("Pages 3--5 show the gap."), "em_dash")
    assert not has(lint("The gap $a --- b$ matters."), "em_dash")
    assert not has(lint("The gap matters. % a --- comment\nMore text."), "em_dash")
    assert not has(lint("\\begin{equation}\na --- b\n\\end{equation}\nText."), "em_dash")
    assert has(lint("A \u2014 B", mode="text"), "em_dash")


# ---- 16. title -------------------------------------------------------------
def test_title(lint):
    doc = "\\documentclass{article}\n\\title{Calibration: a study}\n\\begin{document}\nText.\n\\end{document}\n"
    f = lint(doc, wrap=False)
    t = [x for x in f if x.category == "title"]
    assert len(t) == 1 and t[0].severity == "HARD" and t[0].line == 2
    doc = "\\documentclass{article}\n\\title{Is calibration real?}\n\\begin{document}\nText.\n\\end{document}\n"
    assert has(lint(doc, wrap=False), "title")
    doc = "\\documentclass{article}\n\\title{Calibration of code models}\n\\begin{document}\nText.\n\\end{document}\n"
    assert not has(lint(doc, wrap=False), "title")
    assert has(lint("# Calibration: a study\n\nText here.\n", mode="text"), "title")
    assert not has(lint("# Calibration study\n\nText here.\n", mode="text"), "title")


# ---- stripper behavior -----------------------------------------------------
def test_line_numbers_with_multiline_math(lint):
    doc = (
        "\\documentclass{article}\n"          # 1
        "\\begin{document}\n"                 # 2
        "\\begin{equation}\n"                 # 3
        "x = 1 \\\\\n"                        # 4
        "y = 2\n"                             # 5
        "\\end{equation}\n"                   # 6
        "It is worth noting that this holds.\n"  # 7
        "\\end{document}\n"
    )
    f = lint(doc, wrap=False)
    hit = [x for x in f if x.category == "significance_announcer"]
    assert len(hit) == 1
    assert hit[0].line == 7
    assert hit[0].col == 1
    assert hit[0].source_line == "It is worth noting that this holds."


def test_preamble_skipped_but_title_read(lint):
    doc = ("\\documentclass{article}\n\\usepackage{colour_pkg}\n\\newcommand{\\foo}{session}\n"
           "\\title{Plain title}\n\\begin{document}\nClean text here.\n\\end{document}\n")
    assert lint(doc, wrap=False) == []


def test_stripping_cases(lint):
    f = lint("Claim \\cite{wave_2020} and \\ref{wave:gate} and \\label{session} hold "
             "\\emph{well}.")
    assert not has(f, "process_word") and not has(f, "underscore_identifier")
    f = lint("\\begin{lstlisting}\nsession wave gate\n\\end{lstlisting}\nText here.")
    assert not has(f, "process_word")
    f = lint("Use \\verb|a_b session| here.")
    assert not has(f, "process_word") and not has(f, "underscore_identifier")
    f = lint("A \\textbf{session} here.")
    assert has(f, "process_word")  # braced text arguments stay prose
    f = lint("Cost is 5\\% of 3\\_4 and \\$.")
    assert not has(f, "decimal_in_prose")


def test_escaped_percent_not_comment(lint):
    f = lint("The accuracy is 12.5\\% overall.")
    assert has(f, "decimal_in_prose")


def test_nested_braces_in_args(lint):
    f = lint("\\textbf{A {nested {deep}} session} remains.")
    assert has(f, "process_word")


def test_sentence_splitter_abbreviations():
    import prose_lint
    t = "We use e.g. Fig. 3 and Eq. 2, i.e. the model, vs. others, cf. Smith et al. (2020). Next 3.5 holds."
    spans = prose_lint.split_sentences(t)
    assert len(spans) == 2


def test_item_breaks_sentences(lint):
    f = lint("\\begin{itemize}\n\\item It is worth noting this\n\\item What this shows is x\n\\end{itemize}")
    assert has(f, "significance_announcer") and has(f, "cleft_what")


# ---- CLI -------------------------------------------------------------------
def run_cli(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                          capture_output=True, text=True)


def test_exit_code_warn_only(tmp_path):
    p = tmp_path / "w.tex"
    p.write_text("\\begin{document}\nThe gap is quite small.\n\\end{document}\n")
    r = run_cli(p)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "softening_adverb" in r.stdout


def test_exit_code_hard(tmp_path):
    p = tmp_path / "h.tex"
    p.write_text("\\begin{document}\nIt is worth noting that the gap shrinks.\n\\end{document}\n")
    r = run_cli(p)
    assert r.returncode == 1


def test_exit_code_usage(tmp_path):
    assert run_cli(tmp_path / "missing.tex").returncode == 2
    assert run_cli().returncode == 2
    p = tmp_path / "a.tex"
    p.write_text("Text.\n")
    assert run_cli(p, "--mode", "bogus").returncode == 2
    assert run_cli(p, "--config", tmp_path / "nope.toml").returncode == 2


def test_reports_written(tmp_path):
    p = tmp_path / "r.tex"
    p.write_text("\\begin{document}\nIt is worth noting this is quite odd.\nThe score is 0.82.\n\\end{document}\n")
    j, m = tmp_path / "o.json", tmp_path / "o.md"
    r = run_cli(p, "--json", j, "--md", m, "--quiet")
    assert r.returncode == 1
    assert r.stdout == ""
    data = json.loads(j.read_text())
    assert data["counts"]["significance_announcer"]["HARD"] == 1
    assert data["counts"]["softening_adverb"]["WARN"] == 1
    assert data["counts"]["decimal_in_prose"]["total"] == 1
    assert data["totals"]["HARD"] >= 2
    f = [x for x in data["findings"] if x["category"] == "decimal_in_prose"][0]
    assert f["line"] == 3 and f["col"] == 14 and f["match"] == "0.82"
    assert f["source_line"] == "The score is 0.82."
    assert set(f) >= {"file", "line", "col", "category", "severity", "match", "source_line"}
    md = m.read_text()
    assert "| significance_announcer | 1 | 0 | 1 |" in md
    assert "decimal_in_prose" in md and "The score is 0.82." in md


def test_auto_mode(tmp_path):
    t = tmp_path / "n.txt"
    t.write_text("It is worth noting this.\n")
    assert run_cli(t).returncode == 1
    tex = tmp_path / "n.tex"
    tex.write_text("% It is worth noting this.\nClean text here.\n")
    assert run_cli(tex).returncode == 0


def test_severity_off(tmp_path):
    cfg = tmp_path / "c.toml"
    src = (ROOT / "tools" / "prose_lint.toml").read_text()
    cfg.write_text(src.replace('significance_announcer = "HARD"', 'significance_announcer = "OFF"'))
    p = tmp_path / "x.tex"
    p.write_text("\\begin{document}\nIt is worth noting this.\n\\end{document}\n")
    assert run_cli(p, "--config", cfg).returncode == 0


# ---- extra edge cases ------------------------------------------------------
def test_tex_dimension_not_decimal(lint):
    assert not has(lint("Start.\n\\vskip 0.3in\nMore text here."), "decimal_in_prose")
    assert not has(lint("\\includegraphics[width=0.9\\textwidth]{a.pdf} Text."), "decimal_in_prose")


def test_list_items_not_short_paragraph(lint):
    body = "\\begin{itemize}\n\\item A longer first item sentence with many words in it today\n\\item Short one\n\\end{itemize}"
    assert not has(lint(body), "short_paragraph_end")


def test_internal_label_model_names(lint):
    assert not has(lint("We test DeepSeek-V3 and V3.1 variants."), "internal_label")
    assert has(lint("We test C1 and C2 variants."), "internal_label")


# ---- title macros ----------------------------------------------------------
def test_icmltitle_hit_and_plain_title(lint):
    f = lint("\\icmltitle{Mind the Gap: X}\nBody text here.")
    t = [x for x in f if x.category == "title"]
    assert len(t) == 1 and t[0].severity == "HARD"
    assert not has(lint("\\title{A Plain Title}\nBody text here."), "title")
    assert not has(lint("\\icmltitle{A Plain Title}\nBody text here."), "title")


def test_icmltitlerunning_and_preamble_and_linebreak(lint):
    doc = ("\\documentclass{article}\n\\icmltitlerunning{Short: running}\n"
           "\\begin{document}\n\\icmltitle{Gap\\\\Is it real?}\nBody text here.\n\\end{document}\n")
    f = lint(doc, wrap=False)
    t = [x for x in f if x.category == "title"]
    assert sorted(x.line for x in t) == [2, 4]
    assert not has(lint("\\icmltitle{First\\\\Second}\nBody text here."), "title")
    assert not has(lint("\\icmltitle{Mind the Gap}\nBody text here."), "heading")


# ---- calibration round: roadmap, announcers, comma-not ---------------------
@pytest.mark.parametrize("text", [
    "Table~\\ref{tab:a} and Figure~\\ref{fig:b} present the results.",
    "Table~\\ref{tab:sft} presents the results.",
    "Figure~\\ref{fig:x} presents the curve.",
    "Figure~\\ref{fig:x} also shows the curve.",
    "Fig.~\\ref{fig:x} illustrates the curve.",
    "Table~\\ref{tab:x} lists the settings.",
    "\\Cref{fig:x} displays the curve.",
    "Appendix~\\ref{app:a} gives the details.",
    "Tables 1 and 2 report the results.",
])
def test_roadmap_calibrated_hits(lint, text):
    f = lint(text)
    assert [x.severity for x in f if x.category == "roadmap"] == ["HARD"], text


@pytest.mark.parametrize("text", [
    "Figure~\\ref{fig:x} plots the curve.",
    "As in Table~\\ref{tab:x}, the gap shrinks.",
    "The model shows a gap in Figure~\\ref{fig:x}.",
    "Table~\\ref{tab:x} is long and very dense in cells.",
])
def test_roadmap_calibrated_nonhits(lint, text):
    assert not has(lint(text), "roadmap"), text


@pytest.mark.parametrize("text", [
    "This result, which is noteworthy, holds.",
    "The drop is particularly striking.",
    "The drop is strikingly large.",
    "The drop is remarkably large.",
    "Note that the gap shrinks.",
    "It should be noted that the gap shrinks.",
])
def test_announcer_additions(lint, text):
    f = lint(text)
    assert [x.severity for x in f if x.category == "significance_announcer"] == ["HARD"], text
    assert not has(f, "softening_adverb")


def test_announcer_addition_nonhits(lint):
    assert not has(lint("We note that the gap shrinks."), "significance_announcer")
    assert not has(lint("The gap shrinks, as we note that it must."), "significance_announcer")


def test_negation_comma_not(lint):
    f = lint("The failure is fundamental, not a calibration artifact.")
    assert [x.severity for x in f if x.category == "negation_comma_not"] == ["WARN"]
    assert has(lint("It is the data, not the model."), "negation_comma_not")
    assert has(lint("It is the size, not scale."), "negation_comma_not")
    for t in ["We ask whether or not the gap shrinks.", "The gap shrinks if not vanishes.",
              "Some cells are empty, not shown here.", "It helps, not only speed.",
              "We test it, not.", "The gap is large, but not huge."]:
        assert not has(lint(t), "negation_comma_not"), t
    # not double-reported with not_but
    f = lint("It is fundamental, not a bias, but a variance effect.")
    assert not has(f, "negation_comma_not") and has(f, "negation_not_but")
