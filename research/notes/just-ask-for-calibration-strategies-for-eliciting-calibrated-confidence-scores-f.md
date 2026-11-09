---
title: 'Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores
  from Language Models Fine-Tuned with Human Feedback - ACL Anthology'
id: just-ask-for-calibration-strategies-for-eliciting-calibrated-confidence-scores-f
tags:
- code-llm-probe-verbalize-gap-3d8995
- verbalized-confidence
- rlhf-calibration
- foundational
created: '2026-07-20T06:38:35.843786Z'
updated: '2026-07-20T06:42:27.535363Z'
source: https://aclanthology.org/2023.emnlp-main.330/
source_domain: aclanthology.org
fetched_at: '2026-07-20T06:38:35.843418Z'
fetch_provider: builtin
status: draft
type: note
tier: unknown
content_type: unknown
deprecated: false
summary: 'Tian, Mitchell, Zhou, Sharma, Rafailov, Yao, Finn, Manning (Stanford, EMNLP
  2023, arXiv:2305.14975). Evaluates confidence-extraction methods for RLHF-tuned
  LLMs (ChatGPT, GPT-4, Claude), motivated by evidence that RLHF degrades token-probability
  (logit) calibration relative to base pretrained models. Central finding: VERBALIZED
  confidence (asking the model in natural language how confident it is) is typically
  BETTER-calibrated than the same RLHF model''s own conditional token probabilities
  on TriviaQA, SciQ, and TruthfulQA, often cutting expected calibration error by a
  relative ~50%. This is the inverse framing from most of this literature review''s
  other papers: here verbalized/expressed confidence beats an INTERNAL signal (logit
  probability), not the reverse -- but the internal signal being beaten is raw next-token
  probability post-RLHF, not a purpose-trained linear probe on hidden states. Domain:
  general factual QA (TriviaQA/SciQ/TruthfulQA), not code, not per-requirement, whole-answer
  granularity only. Important complication for the disconnect-paper''s framing: this
  paper shows verbalization CAN beat a (specific, RLHF-corrupted) internal signal
  in general QA, meaning ''internal beats verbalized'' is not a universal law -- it
  depends critically on WHICH internal signal (raw logit vs. trained hidden-state
  probe) is used as the comparator, a distinction the AAAI-27 pivot must state precisely
  to avoid an easy reviewer-2 rebuttal citing this exact paper.'
---

Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback - ACL Anthology
Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
Katherine Tian
,
Eric Mitchell
,
Allan Zhou
,
Archit Sharma
,
Rafael Rafailov
,
Huaxiu Yao
,
Chelsea Finn
,
Christopher Manning
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
A trustworthy real-world prediction system should produce well-calibrated confidence scores; that is, its confidence in an answer should be indicative of the likelihood that the answer is correct, enabling deferral to an expert in cases of low-confidence predictions. Recent studies have shown that unsupervised pre-training produces large language models (LMs) whose conditional probabilities are remarkably well-calibrated. However, the most widely-used LMs are fine-tuned with reinforcement learning from human feedback (RLHF-LMs), and some studies have suggested that RLHF-LMs produce conditional probabilities that are very poorly calibrated. In light of this perceived weakness, we conduct a broad evaluation of methods for extracting confidence scores from RLHF-LMs. For RLHF-LMs such as ChatGPT, GPT-4, and Claude, we find that verbalized confidences emitted as output tokens are typically better-calibrated than the model’s conditional probabilities on the TriviaQA, SciQ, and TruthfulQA benchmarks, often reducing the expected calibration error by a relative 50%.
Anthology ID:
2023.emnlp-main.330
Volume:
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
Month:
December
Year:
2023
Address:
Singapore
Editors:
Houda Bouamor
,
Juan Pino
,
Kalika Bali
Venue:
EMNLP
SIG:
Publisher:
Association for Computational Linguistics
Note:
Pages:
5433–5442
Language:
URL:
https://aclanthology.org/2023.emnlp-main.330/
DOI:
10.18653/v1/2023.emnlp-main.330
Bibkey:
tian-etal-2023-just
Cite (ACL):
Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn, and Christopher Manning. 2023.
Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
. In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
, pages 5433–5442, Singapore. Association for Computational Linguistics.
Cite (Informal):
Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
(Tian et al., EMNLP 2023)
Copy Citation:
BibTeX
Markdown
MODS XML
Endnote
More
options…
PDF:
https://aclanthology.org/2023.emnlp-main.330.pdf
Video:
https://aclanthology.org/2023.emnlp-main.330.mp4
PDF
Cite
Search
Video
Fix data
Export citation
BibTeX
MODS XML
Endnote
Preformatted
@inproceedings{tian-etal-2023-just,
    title = "Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback",
    author = "Tian, Katherine  and
      Mitchell, Eric  and
      Zhou, Allan  and
      Sharma, Archit  and
      Rafailov, Rafael  and
      Yao, Huaxiu  and
      Finn, Chelsea  and
      Manning, Christopher",
    editor = "Bouamor, Houda  and
      Pino, Juan  and
      Bali, Kalika",
    booktitle = "Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing",
    month = dec,
    year = "2023",
    address = "Singapore",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.emnlp-main.330/",
    doi = "10.18653/v1/2023.emnlp-main.330",
    pages = "5433--5442",
    abstract = "A trustworthy real-world prediction system should produce well-calibrated confidence scores; that is, its confidence in an answer should be indicative of the likelihood that the answer is correct, enabling deferral to an expert in cases of low-confidence predictions. Recent studies have shown that unsupervised pre-training produces large language models (LMs) whose conditional probabilities are remarkably well-calibrated. However, the most widely-used LMs are fine-tuned with reinforcement learning from human feedback (RLHF-LMs), and some studies have suggested that RLHF-LMs produce conditional probabilities that are very poorly calibrated. In light of this perceived weakness, we conduct a broad evaluation of methods for extracting confidence scores from RLHF-LMs. For RLHF-LMs such as ChatGPT, GPT-4, and Claude, we find that verbalized confidences emitted as output tokens are typically better-calibrated than the model{'}s conditional probabilities on the TriviaQA, SciQ, and TruthfulQA benchmarks, often reducing the expected calibration error by a relative 50{\%}."
}
Download as
File
Copy to Clipboard
<?xml version="1.0" encoding="UTF-8"?>
<modsCollection xmlns="http://www.loc.gov/mods/v3">
<mods ID="tian-etal-2023-just">
    <titleInfo>
        <title>Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback</title>
    </titleInfo>
    <name type="personal">
        <namePart type="given">Katherine</namePart>
        <namePart type="family">Tian</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Eric</namePart>
        <namePart type="family">Mitchell</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Allan</namePart>
        <namePart type="family">Zhou</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Archit</namePart>
        <namePart type="family">Sharma</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Rafael</namePart>
        <namePart type="family">Rafailov</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Huaxiu</namePart>
        <namePart type="family">Yao</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Chelsea</namePart>
        <namePart type="family">Finn</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Christopher</namePart>
        <namePart type="family">Manning</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <originInfo>
        <dateIssued>2023-12</dateIssued>
    </originInfo>
    <typeOfResource>text</typeOfResource>
    <relatedItem type="host">
        <titleInfo>
            <title>Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing</title>
        </titleInfo>
        <name type="personal">
            <namePart type="given">Houda</namePart>
            <namePart type="family">Bouamor</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Juan</namePart>
            <namePart type="family">Pino</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Kalika</namePart>
            <namePart type="family">Bali</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <originInfo>
            <publisher>Association for Computational Linguistics</publisher>
            <place>
                <placeTerm type="text">Singapore</placeTerm>
            </place>
        </originInfo>
        <genre authority="marcgt">conference publication</genre>
    </relatedItem>
    <abstract>A trustworthy real-world prediction system should produce well-calibrated confidence scores; that is, its confidence in an answer should be indicative of the likelihood that the answer is correct, enabling deferral to an expert in cases of low-confidence predictions. Recent studies have shown that unsupervised pre-training produces large language models (LMs) whose conditional probabilities are remarkably well-calibrated. However, the most widely-used LMs are fine-tuned with reinforcement learning from human feedback (RLHF-LMs), and some studies have suggested that RLHF-LMs produce conditional probabilities that are very poorly calibrated. In light of this perceived weakness, we conduct a broad evaluation of methods for extracting confidence scores from RLHF-LMs. For RLHF-LMs such as ChatGPT, GPT-4, and Claude, we find that verbalized confidences emitted as output tokens are typically better-calibrated than the model’s conditional probabilities on the TriviaQA, SciQ, and TruthfulQA benchmarks, often reducing the expected calibration error by a relative 50%.</abstract>
    <identifier type="citekey">tian-etal-2023-just</identifier>
    <identifier type="doi">10.18653/v1/2023.emnlp-main.330</identifier>
    <location>
        <url>https://aclanthology.org/2023.emnlp-main.330/</url>
    </location>
    <part>
        <date>2023-12</date>
        <extent unit="page">
            <start>5433</start>
            <end>5442</end>
        </extent>
    </part>
</mods>
</modsCollection>
Download as
File
Copy to Clipboard
%0 Conference Proceedings
%T Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
%A Tian, Katherine
%A Mitchell, Eric
%A Zhou, Allan
%A Sharma, Archit
%A Rafailov, Rafael
%A Yao, Huaxiu
%A Finn, Chelsea
%A Manning, Christopher
%Y Bouamor, Houda
%Y Pino, Juan
%Y Bali, Kalika
%S Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
%D 2023
%8 December
%I Association for Computational Linguistics
%C Singapore
%F tian-etal-2023-just
%X A trustworthy real-world prediction system should produce well-calibrated confidence scores; that is, its confidence in an answer should be indicative of the likelihood that the answer is correct, enabling deferral to an expert in cases of low-confidence predictions. Recent studies have shown that unsupervised pre-training produces large language models (LMs) whose conditional probabilities are remarkably well-calibrated. However, the most widely-used LMs are fine-tuned with reinforcement learning from human feedback (RLHF-LMs), and some studies have suggested that RLHF-LMs produce conditional probabilities that are very poorly calibrated. In light of this perceived weakness, we conduct a broad evaluation of methods for extracting confidence scores from RLHF-LMs. For RLHF-LMs such as ChatGPT, GPT-4, and Claude, we find that verbalized confidences emitted as output tokens are typically better-calibrated than the model’s conditional probabilities on the TriviaQA, SciQ, and TruthfulQA benchmarks, often reducing the expected calibration error by a relative 50%.
%R 10.18653/v1/2023.emnlp-main.330
%U https://aclanthology.org/2023.emnlp-main.330/
%U https://doi.org/10.18653/v1/2023.emnlp-main.330
%P 5433-5442
Download as
File
Copy to Clipboard
Markdown (Informal)
[Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback](https://aclanthology.org/2023.emnlp-main.330/) (Tian et al., EMNLP 2023)
Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
(Tian et al., EMNLP 2023)
ACL
Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn, and Christopher Manning. 2023.
Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
. In
Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
, pages 5433–5442, Singapore. Association for Computational Linguistics.
Copy Markdown to
Clipboard
Copy ACL to
Clipboard