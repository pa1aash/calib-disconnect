---
title: 'Semantic vs. Structural Signals: Log-Probability and LLM-as-a-Judge for Reference-Free
  Code Evaluation - ACL Anthology'
id: semantic-vs-structural-signals-log-probability-and-llm-as-a-judge-for-reference
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:09:03.164711Z'
updated: '2026-11-09T23:27:44.595609Z'
source: https://doi.org/10.18653/v1/2026.gem-main.55
source_domain: aclanthology.org
fetched_at: '2026-11-09T23:09:03.164365Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL-TEXT (ACL Anthology GEM 2026, pp. 574-581; PDF extracted locally).
  Fedrushkov et al. compare explicit LLM-as-a-judge scores and log P(code|task) against
  execution ground truth on HumanEval-X (164 problems, five languages; five 8-16B
  decoder models: Qwen3, Llama-3.1, DeepSeek-V2, Gemma3, Phi4). Explicit judges reach
  ROC-AUC 0.971 (gpt-oss-120B) and 0.905 (Qwen3-Coder-80B); log-prob pass/fail AUC
  only 0.499 (Llama3) to 0.619 (Gemma3), yet log-prob separates canonical from mutated
  solutions with >97% pairwise accuracy. Near-occupant for L1 (execution-graded readout
  comparison) at small scale; no calibration metrics, no probes, no contamination
  control.'
---

Semantic vs. Structural Signals: Log-Probability and LLM-as-a-Judge for Reference-Free Code Evaluation - ACL Anthology
Semantic vs. Structural Signals: Log-Probability and
LLM
-as-a-Judge for Reference-Free Code Evaluation
Dmitriy Fedrushkov
,
Yulong He
,
Ivan Smirnov
,
Artem Aliev
,
Sergey Kovalchuk
Correct Metadata for
Use this form to create a GitHub issue with structured data describing the correction. You will need a GitHub account.
Once you create that issue, the correction will be reviewed by a staff member.
⚠️ Mobile Users: Submitting this form to create a new issue will only work with github.com, not the GitHub Mobile app.
Important
: The Anthology treat PDFs as authoritative. Please use this form only to correct data
that is out of line with the PDF. See
our corrections
guidelines
if you need to change the PDF.
Title
Adjust the title. Retain tags such as
<fixed-case>.
Authors
Adjust author names and order to match the
PDF.
Add Author
Abstract
Correct abstract if needed. Retain XML formatting tags such as <tex-math>. You may use <b>...</b> for
bold
, <i>...</i> for
italic
, <u>...</u> for
underline
, <sc>...</sc> for
small-caps
, <tt>...<tt> for
typewriter text
, <url>...</url> for URLs, <a href=...> for hyperlinks, and <par/> for paragraph breaks.
Verification against PDF
Ensure that the new title/authors match the snapshot below. (If there
is no snapshot or it is too small, consult
the PDF
.)
Authors concatenated from the text boxes above:
ALL author names match the snapshot above—including
middle initials, hyphens, and accents.
Create GitHub issue for staff review
Abstract
Reference-free evaluation of LLM-generated code is essential when execution-based testing is unavailable or costly. We compare two paradigms:
explicit LLM-as-a-Judge
scoring, which assigns a quality score to a solution, and
log-probability scoring
, which uses
log
P𝜃(
code
∣
task
)
as an instruction-free signal.Across HumanEval-X, we find that the two approaches capture
qualitatively different aspects
of code correctness. Explicit judges — particularly larger models — perform strongly on generated code, reflecting their ability to reason about task-solution alignment, but fail to distinguish correct solutions from minimally mutated ones. Log-probability exhibits the opposite pattern: weaker performance on generated code, but consistent pairwise separation of canonical from mutated solutions.These results reveal a
discrimination-ranking dissociation
and show that the two paradigms provide complementary, non-interchangeable signals: explicit judges capture semantic correctness, while log-probability captures local structural consistency.
Anthology ID:
2026.gem-main.55
Volume:
Proceedings of the Fifth Workshop on Generation, Evaluation and Metrics (GEM)
Month:
July
Year:
2026
Address:
San Diego, California, USA
Editors:
Simon Mille
,
Sebastian Gehrmann
,
Patrícia Schmidtová
,
Ondřej Dušek
,
Marzieh Fadaee
,
Kyle Lo
,
Enrico Santus
,
Gabriel Stanovsky
Venues:
GEM
|
WS
SIG:
Publisher:
Association for Computational Linguistics
Note:
Pages:
574–581
Language:
URL:
https://aclanthology.org/2026.gem-main.55/
DOI:
10.18653/v1/2026.gem-main.55
Bibkey:
fedrushkov-etal-2026-semantic
Cite (ACL):
Dmitriy Fedrushkov, Yulong He, Ivan Smirnov, Artem Aliev, and Sergey Kovalchuk. 2026.
Semantic vs. Structural Signals: Log-Probability and LLM-as-a-Judge for Reference-Free Code Evaluation
. In
Proceedings of the Fifth Workshop on Generation, Evaluation and Metrics (GEM)
, pages 574–581, San Diego, California, USA. Association for Computational Linguistics.
Cite (Informal):
Semantic vs. Structural Signals: Log-Probability and LLM-as-a-Judge for Reference-Free Code Evaluation
(Fedrushkov et al., GEM 2026)
Copy Citation:
BibTeX
Markdown
MODS XML
Endnote
More
options…
PDF:
https://aclanthology.org/2026.gem-main.55.pdf
PDF
Cite
Search
Fix data
Export citation
BibTeX
MODS XML
Endnote
Preformatted
@inproceedings{fedrushkov-etal-2026-semantic,
    title = "Semantic vs. Structural Signals: Log-Probability and {LLM}-as-a-Judge for Reference-Free Code Evaluation",
    author = "Fedrushkov, Dmitriy  and
      He, Yulong  and
      Smirnov, Ivan  and
      Aliev, Artem  and
      Kovalchuk, Sergey",
    editor = "Mille, Simon  and
      Gehrmann, Sebastian  and
      Schmidtov{\'a}, Patr{\'i}cia  and
      Du{\v{s}}ek, Ond{\v{r}}ej  and
      Fadaee, Marzieh  and
      Lo, Kyle  and
      Santus, Enrico  and
      Stanovsky, Gabriel",
    booktitle = "Proceedings of the Fifth Workshop on Generation, Evaluation and Metrics ({GEM})",
    month = jul,
    year = "2026",
    address = "San Diego, California, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.gem-main.55/",
    doi = "10.18653/v1/2026.gem-main.55",
    pages = "574--581",
    ISBN = "979-8-89176-423-1",
    abstract = "Reference-free evaluation of LLM-generated code is essential when execution-based testing is unavailable or costly. We compare two paradigms: $\textbf{explicit LLM-as-a-Judge}$ scoring, which assigns a quality score to a solution, and $\textbf{log-probability scoring}$, which uses $\log P_\theta(\text{code} \mid \text{task})$ as an instruction-free signal.Across HumanEval-X, we find that the two approaches capture $\textit{qualitatively different aspects}$ of code correctness. Explicit judges {---} particularly larger models {---} perform strongly on generated code, reflecting their ability to reason about task-solution alignment, but fail to distinguish correct solutions from minimally mutated ones. Log-probability exhibits the opposite pattern: weaker performance on generated code, but consistent pairwise separation of canonical from mutated solutions.These results reveal a $\textbf{discrimination-ranking dissociation}$ and show that the two paradigms provide complementary, non-interchangeable signals: explicit judges capture semantic correctness, while log-probability captures local structural consistency."
}
Download as
File
Copy to Clipboard
<?xml version="1.0" encoding="UTF-8"?>
<modsCollection xmlns="http://www.loc.gov/mods/v3">
<mods ID="fedrushkov-etal-2026-semantic">
    <titleInfo>
        <title>Semantic vs. Structural Signals: Log-Probability and LLM-as-a-Judge for Reference-Free Code Evaluation</title>
    </titleInfo>
    <name type="personal">
        <namePart type="given">Dmitriy</namePart>
        <namePart type="family">Fedrushkov</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Yulong</namePart>
        <namePart type="family">He</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Ivan</namePart>
        <namePart type="family">Smirnov</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Artem</namePart>
        <namePart type="family">Aliev</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Sergey</namePart>
        <namePart type="family">Kovalchuk</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <originInfo>
        <dateIssued>2026-07</dateIssued>
    </originInfo>
    <typeOfResource>text</typeOfResource>
    <relatedItem type="host">
        <titleInfo>
            <title>Proceedings of the Fifth Workshop on Generation, Evaluation and Metrics (GEM)</title>
        </titleInfo>
        <name type="personal">
            <namePart type="given">Simon</namePart>
            <namePart type="family">Mille</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Sebastian</namePart>
            <namePart type="family">Gehrmann</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Patrícia</namePart>
            <namePart type="family">Schmidtová</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Ondřej</namePart>
            <namePart type="family">Dušek</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Marzieh</namePart>
            <namePart type="family">Fadaee</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Kyle</namePart>
            <namePart type="family">Lo</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Enrico</namePart>
            <namePart type="family">Santus</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Gabriel</namePart>
            <namePart type="family">Stanovsky</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <originInfo>
            <publisher>Association for Computational Linguistics</publisher>
            <place>
                <placeTerm type="text">San Diego, California, USA</placeTerm>
            </place>
        </originInfo>
        <genre authority="marcgt">conference publication</genre>
        <identifier type="isbn">979-8-89176-423-1</identifier>
    </relatedItem>
    <abstract>Reference-free evaluation of LLM-generated code is essential when execution-based testing is unavailable or costly. We compare two paradigms: explicit LLM-as-a-Judge scoring, which assigns a quality score to a solution, and log-probability scoring, which uses łog P_θ(\textcode \mid \texttask) as an instruction-free signal.Across HumanEval-X, we find that the two approaches capture qualitatively different aspects of code correctness. Explicit judges — particularly larger models — perform strongly on generated code, reflecting their ability to reason about task-solution alignment, but fail to distinguish correct solutions from minimally mutated ones. Log-probability exhibits the opposite pattern: weaker performance on generated code, but consistent pairwise separation of canonical from mutated solutions.These results reveal a discrimination-ranking dissociation and show that the two paradigms provide complementary, non-interchangeable signals: explicit judges capture semantic correctness, while log-probability captures local structural consistency.</abstract>
    <identifier type="citekey">fedrushkov-etal-2026-semantic</identifier>
    <identifier type="doi">10.18653/v1/2026.gem-main.55</identifier>
    <location>
        <url>https://aclanthology.org/2026.gem-main.55/</url>
    </location>
    <part>
        <date>2026-07</date>
        <extent unit="page">
            <start>574</start>
            <end>581</end>
        </extent>
    </part>
</mods>
</modsCollection>
Download as
File
Copy to Clipboard
%0 Conference Proceedings
%T Semantic vs. Structural Signals: Log-Probability and LLM-as-a-Judge for Reference-Free Code Evaluation
%A Fedrushkov, Dmitriy
%A He, Yulong
%A Smirnov, Ivan
%A Aliev, Artem
%A Kovalchuk, Sergey
%Y Mille, Simon
%Y Gehrmann, Sebastian
%Y Schmidtová, Patrícia
%Y Dušek, Ondřej
%Y Fadaee, Marzieh
%Y Lo, Kyle
%Y Santus, Enrico
%Y Stanovsky, Gabriel
%S Proceedings of the Fifth Workshop on Generation, Evaluation and Metrics (GEM)
%D 2026
%8 July
%I Association for Computational Linguistics
%C San Diego, California, USA
%@ 979-8-89176-423-1
%F fedrushkov-etal-2026-semantic
%X Reference-free evaluation of LLM-generated code is essential when execution-based testing is unavailable or costly. We compare two paradigms: explicit LLM-as-a-Judge scoring, which assigns a quality score to a solution, and log-probability scoring, which uses łog P_θ(\textcode \mid \texttask) as an instruction-free signal.Across HumanEval-X, we find that the two approaches capture qualitatively different aspects of code correctness. Explicit judges — particularly larger models — perform strongly on generated code, reflecting their ability to reason about task-solution alignment, but fail to distinguish correct solutions from minimally mutated ones. Log-probability exhibits the opposite pattern: weaker performance on generated code, but consistent pairwise separation of canonical from mutated solutions.These results reveal a discrimination-ranking dissociation and show that the two paradigms provide complementary, non-interchangeable signals: explicit judges capture semantic correctness, while log-probability captures local structural consistency.
%R 10.18653/v1/2026.gem-main.55
%U https://aclanthology.org/2026.gem-main.55/
%U https://doi.org/10.18653/v1/2026.gem-main.55
%P 574-581
Download as
File
Copy to Clipboard
Markdown (Informal)
[Semantic vs. Structural Signals: Log-Probability and LLM-as-a-Judge for Reference-Free Code Evaluation](https://aclanthology.org/2026.gem-main.55/) (Fedrushkov et al., GEM 2026)
Semantic vs. Structural Signals: Log-Probability and LLM-as-a-Judge for Reference-Free Code Evaluation
(Fedrushkov et al., GEM 2026)
ACL
Dmitriy Fedrushkov, Yulong He, Ivan Smirnov, Artem Aliev, and Sergey Kovalchuk. 2026.
Semantic vs. Structural Signals: Log-Probability and LLM-as-a-Judge for Reference-Free Code Evaluation
. In
Proceedings of the Fifth Workshop on Generation, Evaluation and Metrics (GEM)
, pages 574–581, San Diego, California, USA. Association for Computational Linguistics.
Copy Markdown to
Clipboard
Copy ACL to
Clipboard