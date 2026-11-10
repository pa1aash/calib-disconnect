---
title: Probing Functional Correctness in Diffusion Language Models - ACL Anthology
id: probing-functional-correctness-in-diffusion-language-models-acl-anthology
tags:
- code-llm-confidence-positioning-d82d00
- duplicate-abstract-only
created: '2026-11-09T23:07:03.030647Z'
updated: '2026-11-09T23:28:31.610212Z'
source: https://doi.org/10.18653/v1/2026.acl-srw.15
source_domain: aclanthology.org
fetched_at: '2026-11-09T23:07:03.030220Z'
fetch_provider: builtin
status: deprecated
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'ABSTRACT-ONLY in this note (CLI rejected the PDF as junk); full text was
  read from the ACL Anthology PDF via curl and pdftotext in scratchpad. Chiu and Liu,
  ACL 2026 SRW: logistic-regression probes on LLaDA-8B and Dream-7B hidden states
  predict functional correctness on JSON, GSM8K, MBPP (257), ARC; step-0 signal equals
  AR Qwen-2.5-7B probe (prompt difficulty); offline selective generation saves 36-98%
  compute (MBPP 95.5%/97.8%); probe beats entropy baselines by 5-20 pp. Diffusion
  LMs only; no verbal readout, no base/instruct, no calibration metrics. CLOSE for
  L2 probes on code but different architecture.'
---

Probing Functional Correctness in Diffusion Language Models - ACL Anthology
Probing Functional Correctness in Diffusion Language Models
Guan-Ming Chiu
,
Jeng-Yue Liu
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
Diffusion language models generate text by iteratively denoising all tokens in parallel, but when and where their hidden states encode whether the output will be functionally correct remains unknown.We present the first probing study of DLM internals, training linear classifiers on hidden states to predict functional correctness.Across two models (LLaDA-8B, Dream-7B) and four tasks, we find that DLMs uniquely accumulate correctness signal across denoising steps (AUC gains of 0.08–0.11 on reasoning tasks), absent in single-pass AR decoding. However, step-0 signal reflects prompt difficulty rather than diffusion-specific computation. Signal emergence is task-dependent: structural tasks show flat profiles while reasoning tasks show gradual buildup. The two models exhibit distinct layer dynamics, with LLaDA concentrating signal in upper layers while Dream redistributes toward lower layers. We further show that probe confidence can identify likely failures, enabling selective generation that avoids 36–98% of wasted compute.
Anthology ID:
2026.acl-srw.15
Volume:
Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 4: Student Research Workshop)
Month:
July
Year:
2026
Address:
San Diego, California, United States
Editors:
Santosh T.Y.S.S.
,
Juan Diego Rodriguez
,
Ona de Gibert
Venues:
ACL
|
WS
SIG:
Publisher:
Association for Computational Linguistics
Note:
Pages:
163–172
Language:
URL:
https://aclanthology.org/2026.acl-srw.15/
DOI:
10.18653/v1/2026.acl-srw.15
Bibkey:
chiu-liu-2026-probing
Cite (ACL):
Guan-Ming Chiu and Jeng-Yue Liu. 2026.
Probing Functional Correctness in Diffusion Language Models
. In
Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 4: Student Research Workshop)
, pages 163–172, San Diego, California, United States. Association for Computational Linguistics.
Cite (Informal):
Probing Functional Correctness in Diffusion Language Models
(Chiu & Liu, ACL 2026)
Copy Citation:
BibTeX
Markdown
MODS XML
Endnote
More
options…
PDF:
https://aclanthology.org/2026.acl-srw.15.pdf
PDF
Cite
Search
Fix data
Export citation
BibTeX
MODS XML
Endnote
Preformatted
@inproceedings{chiu-liu-2026-probing,
    title = "Probing Functional Correctness in Diffusion Language Models",
    author = "Chiu, Guan-Ming  and
      Liu, Jeng-Yue",
    editor = "T.Y.S.S., Santosh  and
      Rodriguez, Juan Diego  and
      de Gibert, Ona",
    booktitle = "Proceedings of the 64th Annual Meeting of the {A}ssociation for {C}omputational {L}inguistics (Volume 4: Student Research Workshop)",
    month = jul,
    year = "2026",
    address = "San Diego, California, United States",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.acl-srw.15/",
    doi = "10.18653/v1/2026.acl-srw.15",
    pages = "163--172",
    ISBN = "979-8-89176-393-7",
    abstract = "Diffusion language models generate text by iteratively denoising all tokens in parallel, but when and where their hidden states encode whether the output will be functionally correct remains unknown.We present the first probing study of DLM internals, training linear classifiers on hidden states to predict functional correctness.Across two models (LLaDA-8B, Dream-7B) and four tasks, we find that DLMs uniquely accumulate correctness signal across denoising steps (AUC gains of 0.08{--}0.11 on reasoning tasks), absent in single-pass AR decoding. However, step-0 signal reflects prompt difficulty rather than diffusion-specific computation. Signal emergence is task-dependent: structural tasks show flat profiles while reasoning tasks show gradual buildup. The two models exhibit distinct layer dynamics, with LLaDA concentrating signal in upper layers while Dream redistributes toward lower layers. We further show that probe confidence can identify likely failures, enabling selective generation that avoids 36{--}98{\%} of wasted compute."
}
Download as
File
Copy to Clipboard
<?xml version="1.0" encoding="UTF-8"?>
<modsCollection xmlns="http://www.loc.gov/mods/v3">
<mods ID="chiu-liu-2026-probing">
    <titleInfo>
        <title>Probing Functional Correctness in Diffusion Language Models</title>
    </titleInfo>
    <name type="personal">
        <namePart type="given">Guan-Ming</namePart>
        <namePart type="family">Chiu</namePart>
        <role>
            <roleTerm authority="marcrelator" type="text">author</roleTerm>
        </role>
    </name>
    <name type="personal">
        <namePart type="given">Jeng-Yue</namePart>
        <namePart type="family">Liu</namePart>
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
            <title>Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 4: Student Research Workshop)</title>
        </titleInfo>
        <name type="personal">
            <namePart type="given">Santosh</namePart>
            <namePart type="family">T.Y.S.S.</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Juan</namePart>
            <namePart type="given">Diego</namePart>
            <namePart type="family">Rodriguez</namePart>
            <role>
                <roleTerm authority="marcrelator" type="text">editor</roleTerm>
            </role>
        </name>
        <name type="personal">
            <namePart type="given">Ona</namePart>
            <namePart type="family">de Gibert</namePart>
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
        <identifier type="isbn">979-8-89176-393-7</identifier>
    </relatedItem>
    <abstract>Diffusion language models generate text by iteratively denoising all tokens in parallel, but when and where their hidden states encode whether the output will be functionally correct remains unknown.We present the first probing study of DLM internals, training linear classifiers on hidden states to predict functional correctness.Across two models (LLaDA-8B, Dream-7B) and four tasks, we find that DLMs uniquely accumulate correctness signal across denoising steps (AUC gains of 0.08–0.11 on reasoning tasks), absent in single-pass AR decoding. However, step-0 signal reflects prompt difficulty rather than diffusion-specific computation. Signal emergence is task-dependent: structural tasks show flat profiles while reasoning tasks show gradual buildup. The two models exhibit distinct layer dynamics, with LLaDA concentrating signal in upper layers while Dream redistributes toward lower layers. We further show that probe confidence can identify likely failures, enabling selective generation that avoids 36–98% of wasted compute.</abstract>
    <identifier type="citekey">chiu-liu-2026-probing</identifier>
    <identifier type="doi">10.18653/v1/2026.acl-srw.15</identifier>
    <location>
        <url>https://aclanthology.org/2026.acl-srw.15/</url>
    </location>
    <part>
        <date>2026-07</date>
        <extent unit="page">
            <start>163</start>
            <end>172</end>
        </extent>
    </part>
</mods>
</modsCollection>
Download as
File
Copy to Clipboard
%0 Conference Proceedings
%T Probing Functional Correctness in Diffusion Language Models
%A Chiu, Guan-Ming
%A Liu, Jeng-Yue
%Y T.Y.S.S., Santosh
%Y Rodriguez, Juan Diego
%Y de Gibert, Ona
%S Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 4: Student Research Workshop)
%D 2026
%8 July
%I Association for Computational Linguistics
%C San Diego, California, United States
%@ 979-8-89176-393-7
%F chiu-liu-2026-probing
%X Diffusion language models generate text by iteratively denoising all tokens in parallel, but when and where their hidden states encode whether the output will be functionally correct remains unknown.We present the first probing study of DLM internals, training linear classifiers on hidden states to predict functional correctness.Across two models (LLaDA-8B, Dream-7B) and four tasks, we find that DLMs uniquely accumulate correctness signal across denoising steps (AUC gains of 0.08–0.11 on reasoning tasks), absent in single-pass AR decoding. However, step-0 signal reflects prompt difficulty rather than diffusion-specific computation. Signal emergence is task-dependent: structural tasks show flat profiles while reasoning tasks show gradual buildup. The two models exhibit distinct layer dynamics, with LLaDA concentrating signal in upper layers while Dream redistributes toward lower layers. We further show that probe confidence can identify likely failures, enabling selective generation that avoids 36–98% of wasted compute.
%R 10.18653/v1/2026.acl-srw.15
%U https://aclanthology.org/2026.acl-srw.15/
%U https://doi.org/10.18653/v1/2026.acl-srw.15
%P 163-172
Download as
File
Copy to Clipboard
Markdown (Informal)
[Probing Functional Correctness in Diffusion Language Models](https://aclanthology.org/2026.acl-srw.15/) (Chiu & Liu, ACL 2026)
Probing Functional Correctness in Diffusion Language Models
(Chiu & Liu, ACL 2026)
ACL
Guan-Ming Chiu and Jeng-Yue Liu. 2026.
Probing Functional Correctness in Diffusion Language Models
. In
Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 4: Student Research Workshop)
, pages 163–172, San Diego, California, United States. Association for Computational Linguistics.
Copy Markdown to
Clipboard
Copy ACL to
Clipboard