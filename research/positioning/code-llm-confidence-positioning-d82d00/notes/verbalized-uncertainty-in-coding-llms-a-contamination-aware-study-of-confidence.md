---
title: 'Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of Confidence
  Calibration - ACL Anthology'
id: verbalized-uncertainty-in-coding-llms-a-contamination-aware-study-of-confidence
tags:
- code-llm-confidence-positioning-d82d00
created: '2026-11-09T23:07:26.431719Z'
updated: '2026-11-09T23:27:44.357305Z'
source: https://doi.org/10.18653/2026.uncertainlp-main.21
source_domain: aclanthology.org
fetched_at: '2026-11-09T23:07:26.430989Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of Confidence
  Calibration - ACL Anthology'
---

Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of Confidence Calibration - ACL Anthology
Verbalized Uncertainty in Coding
LLM
s: A Contamination-Aware Study of Confidence Calibration
Hunter Tuerlings
,
Matias Valdenegro-Toro
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
Coding large language models (LLMs) can produce plausible solutions that fail hidden test cases, making it difficult to judge when to trust their output. This paper presents a contamination-aware comparison of established methods for eliciting verbalized confidence in generated code. Six instruction-tuned, coding-specialized LLMs from three model families are evaluated on 365 problems from a shared contamination-aware
LiveCodeBench
window. For each frozen code generation, confidence is elicited separately under three strategies, Direct numeric scoring, Chain-of-Thought reasoning followed by a score, and Linguistic confidence labels. Under strict scoring, all 18 model-strategy combinations have negative Net Calibration Error, showing a consistent tendency toward overconfidence. Linguistic elicitation achieves the lowest Expected Calibration Error for four of six models, but several favourable values result from collapsed confidence distributions. Eight of the 18 combinations are collapsed and five are unstable across repeated runs, including three Chain-of-Thought combinations. When outputs are ranked by confidence and the least confident are reviewed first, Direct elicitation gives the largest improvement over random selection in four of six models. Verbalized confidence cannot be reduced to a single trustworthy pass probability; calibration, ranking ability, distributional collapse, and stability must each be checked separately.
Anthology ID:
2026.uncertainlp-main.21
Volume:
The Proceedings of the Third Workshop on Uncertainty-Aware NLP
Month:
October
Year:
2026
Address:
Budapest, Hungary
Editors:
Wilker Aziz
,
Jonathan Berant
,
Bryan Eikema
,
Evgenia Ilia
,
Marie-Catherine de Marneffe
,
Barbara Plank
,
Artem Shelmanov
,
Swabha Swayamdipta
,
Jörg Tiedemann
,
Artem Vazhentsev
,
Raúl Vázquez
,
Chrysoula Zerva
Venues:
UncertaiNLP
|
WS
SIG:
Publisher:
Association for Computational Linguistics
Note:
Pages:
328–355
Language:
URL:
https://aclanthology.org/2026.uncertainlp-main.21/
DOI:
10.18653/2026.uncertainlp-main.21
Bibkey:
tuerlings-valdenegro-toro-2026-verbalized
Cite (ACL):
Hunter Tuerlings and Matias Valdenegro-Toro. 2026.
Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of Confidence Calibration
. In
The Proceedings of the Third Workshop on Uncertainty-Aware NLP
, pages 328–355, Budapest, Hungary. Association for Computational Linguistics.
Cite (Informal):
Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of Confidence Calibration
(Tuerlings & Valdenegro-Toro, UncertaiNLP 2026)
Copy Citation:
BibTeX
Markdown
MODS XML
Endnote
More
options…
PDF:
https://aclanthology.org/2026.uncertainlp-main.21.pdf
PDF
Cite
Search
Fix data
Export citation
BibTeX
MODS XML
Endnote
Preformatted
@inproceedings{tuerlings-valdenegro-toro-2026-verbalized,
    title = "Verbalized Uncertainty in Coding {LLM}s: A Contamination-Aware Study of Confidence Calibration",
    author = "Tuerlings, Hunter  and
      Valdenegro-Toro, Matias",
    editor = {Aziz, Wilker  and
      Berant, Jonathan  and
      Eikema, Bryan  and
      Ilia, Evgenia  and
      de Marneffe, Marie-Catherine  and
      Plank, Barbara  and
      Shelmanov, Artem  and
      Swayamdipta, Swabha  and
      Tiedemann, J{\"o}rg  and
      Vazhentsev, Artem  and
      V{\'a}zquez, Ra{\'u}l  and
      Zerva, Chrysoula},
    booktitle = "The Proceedings of the Third Workshop on Uncertainty-Aware {NLP}",
    month = oct,
    year = "2026",
    address = "Budapest, Hungary",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.uncertainlp-main.21/",
    doi = "10.18653/2026.uncertainlp-main.21",
    pages = "328--355",
    ISBN = "979-8-89176-486-6",
    abstract = "Coding large language models (LLMs) can produce plausible solutions that fail hidden test cases, making it difficult to judge when to trust their output. This paper presents a contamination-aware comparison of established methods for eliciting verbalized confidence in generated code. Six instruction-tuned, coding-specialized LLMs from three model families are evaluated on 365 problems from a shared contamination-aware \textsc{LiveCodeBench} window. For each frozen code generation, confidence is elicited separately under three strategies, Direct numeric scoring, Chain-of-Thought reasoning followed by a score, and Linguistic confidence labels. Under strict scoring, all 18 model-strategy combinations have negative Net Calibration Error, showing a consistent tendency toward overconfidence. Linguistic elicitation achieves the lowest Expected Calibration Error for four of six models, but several favourable values result from collapsed confidence distributions. Eight of the 18 combinations are collapsed and five are unstable across repeated runs, including three Chain-of-Thought combinations. When outputs are ranked by confidence and the least confident are reviewed first, Direct elicitation gives the largest improvement over random selection in four of six models. Verbalized confidence cannot be reduced to a single trustworthy pass probability; calibration, ranking ability, distributional collapse, and stability must each be checked separately."
}
Download as
File
Copy to Clipboard
<?xml version="1.0" encoding="UTF-8"?>
<modsCollection xmlns="http://www.loc.gov/mods/v3">
<mods ID="tuerlings-valdenegro-toro-2026-verbalized">
    <titleInfo>
        <title>Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of Confidence Calibration</title>
    </titleInfo>
    <name type="personal">
        <namePart type="given">Hunter</namePart>
        <namePart type="family">Tuerlings</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Matias</namePart>
        <namePart type="family">Valdenegro-Toro</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <originInfo>
        <dateIssued>2026-10</dateIssued>
    </originInfo>
    <typeOfResource>text</typeOfResource>
    <relatedItem type="host">
        <titleInfo>
            <title>The Proceedings of the Third Workshop on Uncertainty-Aware NLP</title>
        </titleInfo>
        <name type="personal">
            <namePart type="given">Wilker</namePart>
            <namePart type="family">Aziz</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Jonathan</namePart>
            <namePart type="family">Berant</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Bryan</namePart>
            <namePart type="family">Eikema</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Evgenia</namePart>
            <namePart type="family">Ilia</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Marie-Catherine</namePart>
            <namePart type="family">de Marneffe</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Barbara</namePart>
            <namePart type="family">Plank</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Artem</namePart>
            <namePart type="family">Shelmanov</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Swabha</namePart>
            <namePart type="family">Swayamdipta</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Jörg</namePart>
            <namePart type="family">Tiedemann</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Artem</namePart>
            <namePart type="family">Vazhentsev</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Raúl</namePart>
            <namePart type="family">Vázquez</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Chrysoula</namePart>
            <namePart type="family">Zerva</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <originInfo>
            <publisher>Association for Computational Linguistics</publisher>
            <place>
                <placeTerm type="text">Budapest, Hungary</placeTerm>
            </place>
        </originInfo>
        <genre authority="marcgt">conference publication</genre>
        <identifier type="isbn">979-8-89176-486-6</identifier>
    </relatedItem>
    <abstract>Coding large language models (LLMs) can produce plausible solutions that fail hidden test cases, making it difficult to judge when to trust their output. This paper presents a contamination-aware comparison of established methods for eliciting verbalized confidence in generated code. Six instruction-tuned, coding-specialized LLMs from three model families are evaluated on 365 problems from a shared contamination-aware LiveCodeBench window. For each frozen code generation, confidence is elicited separately under three strategies, Direct numeric scoring, Chain-of-Thought reasoning followed by a score, and Linguistic confidence labels. Under strict scoring, all 18 model-strategy combinations have negative Net Calibration Error, showing a consistent tendency toward overconfidence. Linguistic elicitation achieves the lowest Expected Calibration Error for four of six models, but several favourable values result from collapsed confidence distributions. Eight of the 18 combinations are collapsed and five are unstable across repeated runs, including three Chain-of-Thought combinations. When outputs are ranked by confidence and the least confident are reviewed first, Direct elicitation gives the largest improvement over random selection in four of six models. Verbalized confidence cannot be reduced to a single trustworthy pass probability; calibration, ranking ability, distributional collapse, and stability must each be checked separately.</abstract>
    <identifier type="citekey">tuerlings-valdenegro-toro-2026-verbalized</identifier>
    <identifier type="doi">10.18653/2026.uncertainlp-main.21</identifier>
    <location>
        <url>https://aclanthology.org/2026.uncertainlp-main.21/</url>
    </location>
    <part>
        <date>2026-10</date>
        <extent unit="page">
            <start>328</start>
            <end>355</end>
        </extent>
    </part>
</mods>
</modsCollection>
Download as
File
Copy to Clipboard
%0 Conference Proceedings
%T Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of Confidence Calibration
%A Tuerlings, Hunter
%A Valdenegro-Toro, Matias
%Y Aziz, Wilker
%Y Berant, Jonathan
%Y Eikema, Bryan
%Y Ilia, Evgenia
%Y de Marneffe, Marie-Catherine
%Y Plank, Barbara
%Y Shelmanov, Artem
%Y Swayamdipta, Swabha
%Y Tiedemann, Jörg
%Y Vazhentsev, Artem
%Y Vázquez, Raúl
%Y Zerva, Chrysoula
%S The Proceedings of the Third Workshop on Uncertainty-Aware NLP
%D 2026
%8 October
%I Association for Computational Linguistics
%C Budapest, Hungary
%@ 979-8-89176-486-6
%F tuerlings-valdenegro-toro-2026-verbalized
%X Coding large language models (LLMs) can produce plausible solutions that fail hidden test cases, making it difficult to judge when to trust their output. This paper presents a contamination-aware comparison of established methods for eliciting verbalized confidence in generated code. Six instruction-tuned, coding-specialized LLMs from three model families are evaluated on 365 problems from a shared contamination-aware LiveCodeBench window. For each frozen code generation, confidence is elicited separately under three strategies, Direct numeric scoring, Chain-of-Thought reasoning followed by a score, and Linguistic confidence labels. Under strict scoring, all 18 model-strategy combinations have negative Net Calibration Error, showing a consistent tendency toward overconfidence. Linguistic elicitation achieves the lowest Expected Calibration Error for four of six models, but several favourable values result from collapsed confidence distributions. Eight of the 18 combinations are collapsed and five are unstable across repeated runs, including three Chain-of-Thought combinations. When outputs are ranked by confidence and the least confident are reviewed first, Direct elicitation gives the largest improvement over random selection in four of six models. Verbalized confidence cannot be reduced to a single trustworthy pass probability; calibration, ranking ability, distributional collapse, and stability must each be checked separately.
%R 10.18653/2026.uncertainlp-main.21
%U https://aclanthology.org/2026.uncertainlp-main.21/
%U https://doi.org/10.18653/2026.uncertainlp-main.21
%P 328-355
Download as
File
Copy to Clipboard
Markdown (Informal)
[Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of Confidence Calibration](https://aclanthology.org/2026.uncertainlp-main.21/) (Tuerlings & Valdenegro-Toro, UncertaiNLP 2026)
Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of Confidence Calibration
(Tuerlings & Valdenegro-Toro, UncertaiNLP 2026)
ACL
Hunter Tuerlings and Matias Valdenegro-Toro. 2026.
Verbalized Uncertainty in Coding LLMs: A Contamination-Aware Study of Confidence Calibration
. In
The Proceedings of the Third Workshop on Uncertainty-Aware NLP
, pages 328–355, Budapest, Hungary. Association for Computational Linguistics.
Copy Markdown to
Clipboard
Copy ACL to
Clipboard