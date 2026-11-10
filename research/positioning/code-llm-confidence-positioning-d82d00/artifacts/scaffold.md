# Scaffold — code-llm-confidence-positioning-d82d00

## User Prompt (VERBATIM — gospel)
See research/query-code-llm-confidence-positioning-d82d00.md (full verbatim canonical query). The binding scope document is docs/s3/POSITIONING_BRIEF_R1.md.

## Run config
- vault_tag: code-llm-confidence-positioning-d82d00
- query_file: research/query-code-llm-confidence-positioning-d82d00.md
- modality: compare (per-candidate occupancy verdicts + a committed recommendation)
- response_format: argumentative

## Modality rationale
Five candidates are judged against the literature with proportionate depth each, then ranked; the output commits to OCCUPIED/NARROW/CLEAN per component and a recommended spine.

## Tier rationale
Expected FULL: dense prior-work cluster, adversarial novelty assessment, high stakes (gates paper design). Confirm after step 1.

## Wrapper requirements (wave 4 contract, binding)
- save path: research/notes/final_report_code-llm-confidence-positioning-d82d00.md
- citation style: inline, with arXiv id or DOI per claim; full-text location (section, table, equation) for every verdict-bearing claim; ABSTRACT-ONLY marker where only an abstract was read.
- terminal sections: per-candidate verdict table; close-occupant list; ranked recommendation; instrument gaps.
- Network: headless only, academic APIs only (no WebSearch tool, no Google Scholar, no browser). Allowed hosts: jmlr.org, github.com, openreview.net, api.openreview.net, arxiv.org, export.arxiv.org, api.semanticscholar.org, figures.semanticscholar.org, api.openalex.org, api.crossref.org, doi.org, dblp.org, api.unpaywall.org, aclanthology.org, proceedings.mlr.press, papers.nips.cc, proceedings.neurips.cc, openaccess.thecvf.com, dl.acm.org, ieeexplore.ieee.org, link.springer.com, nature.com, huggingface.co, hal.science, zenodo.org, web.archive.org, plus author or institutional pages linked from a fetched record.
- Conventions: American spelling, no em-dashes, serial comma; never fabricate a citation, number, or quotation.

## Tier rationale (step 1)
FULL + argumentative. Five candidates, each with many sub-facets, judged against a dense, fast-moving 2025-2026 prior-work cluster, with verdicts that gate the paper's design. Adversarial depth (critics, patcher) is needed because incorrect novelty claims are a stated TMLR rejection ground.
