---
title: 'NeuroSym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via
  Hierarchical Calibration - ACL Anthology'
id: neurosym-cal-bridging-the-reasoning-execution-gap-in-code-generation-via-hierarc
tags:
- code-llm-confidence-positioning-d82d00
- abstract-only
created: '2026-11-09T23:07:27.321661Z'
updated: '2026-11-09T23:27:44.360009Z'
source: https://doi.org/10.18653/v1/2026.findings-acl.305
source_domain: aclanthology.org
fetched_at: '2026-11-09T23:07:27.320057Z'
fetch_provider: builtin
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'ABSTRACT-ONLY (ACL Anthology record, Findings of ACL 2026, pp. 6132-6143,
  Liu, Wang, Li, Li, Cai, Ye; the PDF fetch returned junk). Proposes NeuroSym-Cal
  for CoT code generation with reasoning models (e.g., DeepSeek-R1): ''Confidence
  Saturation'' where self-consistency consensus fails under systematic errors; adds
  Reasoning Sensitivity Analysis (latent perturbation curvature) fused with output-consensus
  features by a Contextual Calibration Network; claims state-of-the-art ECE and selective
  generation on OOD benchmarks. Close occupant candidate for L1/L2 on reasoning-model
  calibration for code (latent plus sampled readouts), but benchmarks, labels, baselines,
  models, and contamination handling are not verifiable from the abstract. Full-text
  check required before NARROW/OCCUPIED verdicts.'
---

NeuroSym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via Hierarchical Calibration - ACL Anthology
N
euro
S
ym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via Hierarchical Calibration
Peiyang Liu
,
Yining Wang
,
Youru Li
,
Long Li
,
Zhi Cai
,
Wei Ye
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
While Chain-of-Thought (CoT) reasoning enhances code generation in Large Language Models (LLMs), it introduces a critical challenge in uncertainty estimation: Confidence Saturation. Existing calibration methods, such as Self-Consistency, rely on the assumption that consensus implies correctness. This assumption fails under systematic errors, where models confidently repeat flawed logic, leading to miscalibrated high-confidence predictions. To address this, we introduce NeuroSym-Cal, a hierarchical calibration framework. We posit that reliable confidence requires interrogating the model at two complementary levels: the extrinsic consensus of its symbolic outputs and the intrinsic sensitivity of its latent reasoning. Specifically, we propose Reasoning Sensitivity Analysis to measure the local curvature of the deductive process via latent perturbation, providing a fine-grained signal that persists even when output consensus saturates. These orthogonal features are fused by a Contextual Calibration Network to predict correctness. Experiments across state-of-the-art reasoning models (e.g., DeepSeek-R1) demonstrate that NeuroSym-Cal effectively de-saturates overconfident errors, achieving state-of-the-art Expected Calibration Error (ECE) and superior selective generation performance on Out-Of-Domain (OOD) benchmarks.
Anthology ID:
2026.findings-acl.305
Volume:
Findings of the Association for Computational Linguistics: ACL 2026
Month:
July
Year:
2026
Address:
San Diego, California, United States
Editors:
Maria Liakata
,
Viviane P. Moreira
,
Jiajun Zhang
,
David Jurgens
Venue:
Findings
SIG:
Publisher:
Association for Computational Linguistics
Note:
Pages:
6132–6143
Language:
URL:
https://aclanthology.org/2026.findings-acl.305/
DOI:
10.18653/v1/2026.findings-acl.305
Bibkey:
liu-etal-2026-neurosym
Cite (ACL):
Peiyang Liu, Yining Wang, Youru Li, Long Li, Zhi Cai, and Wei Ye. 2026.
NeuroSym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via Hierarchical Calibration
. In
Findings of the Association for Computational Linguistics: ACL 2026
, pages 6132–6143, San Diego, California, United States. Association for Computational Linguistics.
Cite (Informal):
NeuroSym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via Hierarchical Calibration
(Liu et al., Findings 2026)
Copy Citation:
BibTeX
Markdown
MODS XML
Endnote
More
options…
PDF:
https://aclanthology.org/2026.findings-acl.305.pdf
Checklist:
2026.findings-acl.305.checklist.pdf
PDF
Cite
Search
Checklist
Fix data
Export citation
BibTeX
MODS XML
Endnote
Preformatted
@inproceedings{liu-etal-2026-neurosym,
    title = "{N}euro{S}ym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via Hierarchical Calibration",
    author = "Liu, Peiyang  and
      Wang, Yining  and
      Li, Youru  and
      Li, Long  and
      Cai, Zhi  and
      Ye, Wei",
    editor = "Liakata, Maria  and
      Moreira, Viviane P.  and
      Zhang, Jiajun  and
      Jurgens, David",
    booktitle = "Findings of the {A}ssociation for {C}omputational {L}inguistics: {ACL} 2026",
    month = jul,
    year = "2026",
    address = "San Diego, California, United States",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.findings-acl.305/",
    doi = "10.18653/v1/2026.findings-acl.305",
    pages = "6132--6143",
    ISBN = "979-8-89176-395-1",
    abstract = "While Chain-of-Thought (CoT) reasoning enhances code generation in Large Language Models (LLMs), it introduces a critical challenge in uncertainty estimation: Confidence Saturation. Existing calibration methods, such as Self-Consistency, rely on the assumption that consensus implies correctness. This assumption fails under systematic errors, where models confidently repeat flawed logic, leading to miscalibrated high-confidence predictions. To address this, we introduce NeuroSym-Cal, a hierarchical calibration framework. We posit that reliable confidence requires interrogating the model at two complementary levels: the extrinsic consensus of its symbolic outputs and the intrinsic sensitivity of its latent reasoning. Specifically, we propose Reasoning Sensitivity Analysis to measure the local curvature of the deductive process via latent perturbation, providing a fine-grained signal that persists even when output consensus saturates. These orthogonal features are fused by a Contextual Calibration Network to predict correctness. Experiments across state-of-the-art reasoning models (e.g., DeepSeek-R1) demonstrate that NeuroSym-Cal effectively de-saturates overconfident errors, achieving state-of-the-art Expected Calibration Error (ECE) and superior selective generation performance on Out-Of-Domain (OOD) benchmarks."
}
Download as
File
Copy to Clipboard
<?xml version="1.0" encoding="UTF-8"?>
<modsCollection xmlns="http://www.loc.gov/mods/v3">
<mods ID="liu-etal-2026-neurosym">
    <titleInfo>
        <title>NeuroSym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via Hierarchical Calibration</title>
    </titleInfo>
    <name type="personal">
        <namePart type="given">Peiyang</namePart>
        <namePart type="family">Liu</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Yining</namePart>
        <namePart type="family">Wang</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Youru</namePart>
        <namePart type="family">Li</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Long</namePart>
        <namePart type="family">Li</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Zhi</namePart>
        <namePart type="family">Cai</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Wei</namePart>
        <namePart type="family">Ye</namePart>
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
            <title>Findings of the Association for Computational Linguistics: ACL 2026</title>
        </titleInfo>
        <name type="personal">
            <namePart type="given">Maria</namePart>
            <namePart type="family">Liakata</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Viviane</namePart>
            <namePart type="given">P</namePart>
            <namePart type="family">Moreira</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Jiajun</namePart>
            <namePart type="family">Zhang</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">David</namePart>
            <namePart type="family">Jurgens</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <originInfo>
            <publisher>Association for Computational Linguistics</publisher>
            <place>
                <placeTerm type="text">San Diego, California, United States</placeTerm>
            </place>
        </originInfo>
        <genre authority="marcgt">conference publication</genre>
        <identifier type="isbn">979-8-89176-395-1</identifier>
    </relatedItem>
    <abstract>While Chain-of-Thought (CoT) reasoning enhances code generation in Large Language Models (LLMs), it introduces a critical challenge in uncertainty estimation: Confidence Saturation. Existing calibration methods, such as Self-Consistency, rely on the assumption that consensus implies correctness. This assumption fails under systematic errors, where models confidently repeat flawed logic, leading to miscalibrated high-confidence predictions. To address this, we introduce NeuroSym-Cal, a hierarchical calibration framework. We posit that reliable confidence requires interrogating the model at two complementary levels: the extrinsic consensus of its symbolic outputs and the intrinsic sensitivity of its latent reasoning. Specifically, we propose Reasoning Sensitivity Analysis to measure the local curvature of the deductive process via latent perturbation, providing a fine-grained signal that persists even when output consensus saturates. These orthogonal features are fused by a Contextual Calibration Network to predict correctness. Experiments across state-of-the-art reasoning models (e.g., DeepSeek-R1) demonstrate that NeuroSym-Cal effectively de-saturates overconfident errors, achieving state-of-the-art Expected Calibration Error (ECE) and superior selective generation performance on Out-Of-Domain (OOD) benchmarks.</abstract>
    <identifier type="citekey">liu-etal-2026-neurosym</identifier>
    <identifier type="doi">10.18653/v1/2026.findings-acl.305</identifier>
    <location>
        <url>https://aclanthology.org/2026.findings-acl.305/</url>
    </location>
    <part>
        <date>2026-07</date>
        <extent unit="page">
            <start>6132</start>
            <end>6143</end>
        </extent>
    </part>
</mods>
</modsCollection>
Download as
File
Copy to Clipboard
%0 Conference Proceedings
%T NeuroSym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via Hierarchical Calibration
%A Liu, Peiyang
%A Wang, Yining
%A Li, Youru
%A Li, Long
%A Cai, Zhi
%A Ye, Wei
%Y Liakata, Maria
%Y Moreira, Viviane P.
%Y Zhang, Jiajun
%Y Jurgens, David
%S Findings of the Association for Computational Linguistics: ACL 2026
%D 2026
%8 July
%I Association for Computational Linguistics
%C San Diego, California, United States
%@ 979-8-89176-395-1
%F liu-etal-2026-neurosym
%X While Chain-of-Thought (CoT) reasoning enhances code generation in Large Language Models (LLMs), it introduces a critical challenge in uncertainty estimation: Confidence Saturation. Existing calibration methods, such as Self-Consistency, rely on the assumption that consensus implies correctness. This assumption fails under systematic errors, where models confidently repeat flawed logic, leading to miscalibrated high-confidence predictions. To address this, we introduce NeuroSym-Cal, a hierarchical calibration framework. We posit that reliable confidence requires interrogating the model at two complementary levels: the extrinsic consensus of its symbolic outputs and the intrinsic sensitivity of its latent reasoning. Specifically, we propose Reasoning Sensitivity Analysis to measure the local curvature of the deductive process via latent perturbation, providing a fine-grained signal that persists even when output consensus saturates. These orthogonal features are fused by a Contextual Calibration Network to predict correctness. Experiments across state-of-the-art reasoning models (e.g., DeepSeek-R1) demonstrate that NeuroSym-Cal effectively de-saturates overconfident errors, achieving state-of-the-art Expected Calibration Error (ECE) and superior selective generation performance on Out-Of-Domain (OOD) benchmarks.
%R 10.18653/v1/2026.findings-acl.305
%U https://aclanthology.org/2026.findings-acl.305/
%U https://doi.org/10.18653/v1/2026.findings-acl.305
%P 6132-6143
Download as
File
Copy to Clipboard
Markdown (Informal)
[NeuroSym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via Hierarchical Calibration](https://aclanthology.org/2026.findings-acl.305/) (Liu et al., Findings 2026)
NeuroSym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via Hierarchical Calibration
(Liu et al., Findings 2026)
ACL
Peiyang Liu, Yining Wang, Youru Li, Long Li, Zhi Cai, and Wei Ye. 2026.
NeuroSym-Cal: Bridging the Reasoning-Execution Gap in Code Generation via Hierarchical Calibration
. In
Findings of the Association for Computational Linguistics: ACL 2026
, pages 6132–6143, San Diego, California, United States. Association for Computational Linguistics.
Copy Markdown to
Clipboard
Copy ACL to
Clipboard