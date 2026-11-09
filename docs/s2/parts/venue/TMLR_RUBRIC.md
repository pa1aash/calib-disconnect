# TMLR rubric (author checklist and reviewer rubric)

Retrieved 2026-11-10 from https://jmlr.org/tmlr/ pages (saved under `sources/`). Every quotation below is copied verbatim from the saved source file at the URL given on the same line. Items marked (template) are quoted from the example `main.tex` in the upstream style repository (`sources/template-main-tex.txt`), whose URL is a GitHub pointer.

## Headline

- Length: no hard page limit. "Submissions may be any length", but length must be justified; unusually long main bodies (appendices excluded) risk delays, and reviewing timelines are set at a 12-page main-content threshold (2 weeks of review time up to 12 pages, 4 weeks above).
- Anonymity: double-blind and open reviewing. The PDF, supplementary material, and any linked artifacts must be anonymized. Preprints on arXiv are allowed, but the submission must not link to a version with author names.
- Required statements: a Broader Impact Statement is required only if the work "carries a significant risk of harm" (otherwise optional). Authors who use LLM tools must say so in a first-page footnote (FAQ). No mandatory reproducibility checklist was found on the pages fetched; code and data are encouraged.
- Certifications (awarded after acceptance, not by authors): Outstanding, Featured, Reproducibility, Survey, J2C, Expert. Survey papers are no longer considered for review as of 2026-09-01 (FAQ).
- Template: the TMLR LaTeX style file and template are mandatory; modifying formatting may cause rejection without review.

## 1. Author checklist

### Length and structure

- [ ] Keep the main body to a length justified by its content. — > Submissions may be any length, but a paper’s length should be justified by its content and papers that are unusually long (not counting any Appendices) are likely to result in reviewing delays. — https://jmlr.org/tmlr/author-guide.html
- [ ] Be aware that main bodies over 12 pages get longer review timescales. — > TMLR does not make any guarantees, and manuscripts whose main body exceeds 12 pages are subject to longer timescales, but in general the rolling review process aims to deliver a final decision approximately 9 weeks after submission. — https://jmlr.org/tmlr/faq.html
- [ ] Place any appendix after the references. — > The submission PDF may include an Appendix, after the references (for proofs, derivations or complimentary results). — https://jmlr.org/tmlr/author-guide.html
- [ ] Do not rely on the appendix for essential content. — > Looking at the Appendix is at the discretion of the reviewers. — https://jmlr.org/tmlr/author-guide.html
- [ ] The appendix may live in the main PDF. — > Appendices can be included in the main pdf. — https://jmlr.org/tmlr/faq.html

### Formatting and template

- [ ] Use the official TMLR LaTeX style file and template. — > Submissions must be PDF files generated using the TMLR LaTeX stylefile and template. — https://jmlr.org/tmlr/author-guide.html
- [ ] Do not alter the style file or template layout. — > Any changes to the stylefile or template that alters the formatting, font, or layout of the manuscript may result in rejection without review. — https://jmlr.org/tmlr/submissions.html
- [ ] Do not change formatting parameters (template). — > Do not change any aspects of the formatting parameters in the style files. — https://github.com/JmlrOrg/tmlr-style-file/blob/7bf90efe3a0debbba703c05c43f3ff7e4d4a2992/main.tex
- [ ] Use the current style files, not older versions (template). — > Please make sure you use the current files and not previous versions. — https://github.com/JmlrOrg/tmlr-style-file/blob/7bf90efe3a0debbba703c05c43f3ff7e4d4a2992/main.tex
- [ ] Number the pages (template). — > Please note that pages should be numbered. — https://github.com/JmlrOrg/tmlr-style-file/blob/7bf90efe3a0debbba703c05c43f3ff7e4d4a2992/main.tex
- [ ] Keep text inside the template rectangle (template). — > The text must be confined within a rectangle 6.5~inches wide and 9~inches long. — https://github.com/JmlrOrg/tmlr-style-file/blob/7bf90efe3a0debbba703c05c43f3ff7e4d4a2992/main.tex
- [ ] Format violations can cause desk rejection. — > They will evaluate the submission, and may reject it immediately for reasons including (but not limited to): being out of scope, TMLR having insufficient reviewer expertise to adequately handle, being poor quality or unlikely to meet TMLR's acceptance criteria, or having format violations (contingent on Editor-in-Chief approval). — https://jmlr.org/tmlr/editorial-policies.html

### Anonymity and preprints

- [ ] Anonymize the submission. — > TMLR uses a double blind review process and submissions must be anonymized. — https://jmlr.org/tmlr/author-guide.html
- [ ] Anonymize supplementary material too. — > Like submissions, supplementary material must be anonymized. — https://jmlr.org/tmlr/author-guide.html
- [ ] Keep the default (anonymous) style option for the submission; use `preprint` only for de-anonymized postings (template). — > To de-anonymize and remove mentions to TMLR (for example for posting to preprint servers), use the preprint option, — https://github.com/JmlrOrg/tmlr-style-file/blob/7bf90efe3a0debbba703c05c43f3ff7e4d4a2992/main.tex
- [ ] Do not link from the TMLR submission to a de-anonymized version. — > though double blind of the TMLR submission itself must be maintained by not linking to another version that includes the authors' names. — https://jmlr.org/tmlr/author-guide.html
- [ ] Existing arXiv or website preprints are fine. — > You can still submit, even if a preprint of your work already is available online somewhere (as long as it's not in official proceedings for some other publishing venue). — https://jmlr.org/tmlr/faq.html
- [ ] Use the `preprint` option when posting the TMLR-styled paper to arXiv. — > However, make sure to use the "preprint" option of the stylefile if you do. — https://jmlr.org/tmlr/faq.html

### Supplementary material, code, and reproducibility

- [ ] Respect the supplementary size and format limits. — > Authors may submit up to 100MB of supplementary material, such data, source code or illustrative videos; all supplementary materials must be in PDF or ZIP format. — https://jmlr.org/tmlr/author-guide.html
- [ ] Supplementary material must be authors' own and supportive. — > Supplementary material should be material created by the authors that directly supports the submission content. — https://jmlr.org/tmlr/author-guide.html
- [ ] Do not rely on supplementary material for essential content. — > Looking at supplementary material is at the discretion of the reviewers. — https://jmlr.org/tmlr/author-guide.html
- [ ] Upload reproducibility materials (data, code) where possible. — > We encourage authors to, whenever possible, upload materials that improve reproducibility. — https://jmlr.org/tmlr/author-guide.html
- [ ] Put code or videos in the supplementary zip, not the PDF. — > The supplementary zip file should contain additional material such as videos or code. — https://jmlr.org/tmlr/faq.html
- [ ] Code can be attached after acceptance. — > Code and videos may be uploaded and associated with camera ready papers. — https://jmlr.org/tmlr/faq.html

### Required and conditional statements

- [ ] Include a Broader Impact Statement if the work carries significant risk of harm. — > If their work carries a significant risk of harm, authors are required to include a Statement of Broader Impact. — https://jmlr.org/tmlr/author-guide.html
- [ ] The statement should cover benefits, harms, and mitigations. — > The statement should include a concise, concrete description of potential positive and negative societal impact, as well as a discussion of possible mitigations. — https://jmlr.org/tmlr/author-guide.html
- [ ] Otherwise the statement is optional but encouraged where applicable. — > Submissions which describe work with the potential for harm should clearly describe the risks and mitigations in an (otherwise optional) Broader Impact Statement. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] Discuss negative societal impacts and mitigations when applicable. — > Submissions to TMLR are expected, when applicable, to include a discussion about potential negative societal impacts of the proposed research artifact or application. — https://jmlr.org/tmlr/ethics.html
- [ ] Follow data ethics practice (consent, PII, human subjects). — > Submissions must adhere to ethical standards for responsible research practice and due diligence in the conduct. — https://jmlr.org/tmlr/ethics.html
- [ ] Disclose LLM tool use in a first-page footnote. — > Additionally, transparency is always good, so we also require that authors mention explicitly in their submission that they have used this tool, as a footnote on the first page. — https://jmlr.org/tmlr/faq.html
- [ ] Authors remain fully responsible for LLM-assisted content. — > Whichever tools are used, authors are fully responsible for content on which they are listed as (co-) authors. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] Do not list an LLM as an author. — > LLMs are not eligible for authorship. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] An author-contributions statement is optional. — > Authors may choose to include a statement indicating author contributions. — https://jmlr.org/tmlr/editorial-policies.html

### Prior publication, dual submission, and originality

- [ ] Submit only original contributions; no expanded conference papers. — > In particular, we do not accept submissions that are expanded versions of conference papers. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] No text, figure, or result reuse with archival venues. — > There should not be any reuse of written text, figures or results between the submitted paper and any paper which has been published, accepted for publication, or submitted in parallel at another archival, peer-reviewed venue. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] Overlap with non-archival workshops and preprints is allowed. — > It is acceptable for a submission to overlap with the author's previous work if it was shared at venues or tracks that are publicly declared, in writing, to be non-archival, such as workshops, or on preprint servers such as arXiv and bioRxiv. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] Thesis-based work is allowed and treated like a preprint. — > Yes, we have no policy that precludes submission of thesis work; for our purposes, a thesis is considered similarly to a pre-print, e.g., on arXiv. — https://jmlr.org/tmlr/faq.html
- [ ] Survey papers are out of scope for new submissions. — > As of September 1, 2026, TMLR no longer considers survey papers for review. — https://jmlr.org/tmlr/faq.html
- [ ] Check that the paper is in scope (see scope list). — > TMLR’s objective is to publish original papers that contribute to the understanding of the computational and mathematical principles that enable intelligence through learning, be it in brains or in machines. — https://jmlr.org/tmlr/editorial-policies.html

### Authors, profiles, and quotas

- [ ] All authors need complete, active OpenReview profiles. — > All authors must have complete and active OpenReview profiles, including information such as affiliations, conflicts of interest, and publication history. — https://jmlr.org/tmlr/author-guide.html
- [ ] Provide action editor suggestions, IRB, funding, and competing-interest information at submission. — > They also must provide information on appropriate action editors for the submission, as well as on human subjects reporting (IRB), funding, competing interests and any conflict of interest not covered by the institutional history of the authors. — https://jmlr.org/tmlr/author-guide.html
- [ ] Author list is final at submission. — > No authors may be added or removed after submission. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] Every author must have remaining yearly quota. — > All authors must have sufficient budget remaining for the year in order to make a submission. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] Declare only genuine conflicts. — > It is forbidden to state a false conflict in order to block potentially negative reviewers from an institution. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] Read the policies before submitting. — > Authors are required to also read and be familiar with the Editorial Policies, the Acceptance Criteria, the Ethics Guidelines, and the Code of Conduct — https://jmlr.org/tmlr/author-guide.html

### LaTeX and OpenReview submission mechanics

- [ ] Submit through OpenReview. — > We are using the reviewing and publication system of OpenReview for openness and transparency: https://openreview.net/group?id=TMLR — https://jmlr.org/tmlr/submissions.html
- [ ] After submitting, recommend action editors when emailed. — > You will receive an email once your submission has been made, asking you to recommend potential Action Editors that would be appropriate for your submission. — https://jmlr.org/tmlr/submissions.html
- [ ] Expect licensing under CC BY 4.0 from submission onward. — > All TMLR submissions, from the time of submission to final publication, are licensed under CC BY 4.0. — https://jmlr.org/tmlr/author-guide.html
- [ ] Respond to reviews on time; wait for all three reviews before posting a revised PDF. — > Authors can respond to a review as soon as it is posted, however we recommend waiting until all 3 reviews have been submitted before submitting any revised version of the PDF manuscript. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] Respond within two weeks of the third review. — > We strongly recommend that authors submit responses, including any revisions, no later than 2 weeks after the submission of the 3rd review. — https://jmlr.org/tmlr/faq.html
- [ ] Alert reviewers to each revision with a comment. — > Yes. It is also recommended to leave a comment on the OpenReview page, visible to reviewers and the AE, to alert them to the revision. — https://jmlr.org/tmlr/faq.html
- [ ] If resubmitting after rejection, link the earlier submission and describe the changes. — > Authors of a rejected submission may revise and resubmit their paper, but it will need to be entered as a new submission and a link provided to the previously rejected submission as well as a description of the changes made since. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] Revealing identity after rejection precludes resubmission. — > Doing so will preclude them from submitting a revised version of the manuscript to TMLR. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] The resubmission link does not breach anonymity. — > Only the action editor (not the reviewers) will see the previous submission URL, so including it will not violate our guidelines. — https://jmlr.org/tmlr/faq.html

### Camera ready

- [ ] Provide a camera-ready version verified by the action editor, including the review-page link. — > Authors of accepted papers must provide a “camera ready” version, verified by the action editor, which would include a link to the review page for the paper. — https://jmlr.org/tmlr/editorial-policies.html
- [ ] Switch to the `accepted` option (template). — > If your paper is ultimately accepted, use option {\tt accepted} with the {\tt tmlr} package to adjust the format to the camera ready requirements, as follows: — https://github.com/JmlrOrg/tmlr-style-file/blob/7bf90efe3a0debbba703c05c43f3ff7e4d4a2992/main.tex
- [ ] Set month and year variables (template). — > You also need to specify the month and year by defining variables {\tt month} and {\tt year}, which respectively should be a 2-digit and 4-digit number. — https://github.com/JmlrOrg/tmlr-style-file/blob/7bf90efe3a0debbba703c05c43f3ff7e4d4a2992/main.tex
- [ ] The action editor checks stylefile compliance, author information, and the OpenReview link. — > As your final task for an accepted paper, you are asked to quickly verify that the camera ready manuscript complies with TMLR stylefile, with all author information inserted in the manuscript as well as the link to the OpenReview page for the submission. — https://jmlr.org/tmlr/ae-guide.html
- [ ] "Accept with minor revision" changes go into the camera-ready. — > The required revisions should be made in the camera ready submission. — https://jmlr.org/tmlr/faq.html
- [ ] Treat the camera-ready as final. — > In general, camera ready versions of papers are considered to be final, and changes are not allowed. — https://jmlr.org/tmlr/faq.html

## 2. Acceptance criteria as a reviewer rubric

Reviewers answer Yes or No to two questions and give requested changes and broader impact concerns (https://jmlr.org/tmlr/reviewer-guide.html).

| Reviewer question | Grounding quotation | URL |
|---|---|---|
| Are the claims supported by accurate, convincing, and clear evidence? Is there any gap between claims and evidence, and could it be closed by more experiments or by reduced claims? | "This is the most important criterion." and "Another is for the authors to adjust (reduce) their claims." | https://jmlr.org/tmlr/acceptance-criteria.html |
| Would at least some individuals in the TMLR audience be interested in the findings? (Do not penalize modest significance or lack of novelty.) | "Generally, a reviewer who is unsure as to whether a submission satisfies this criterion should assume that it does." | https://jmlr.org/tmlr/acceptance-criteria.html |
| Does the paper clearly communicate what it found and why it may interest researchers? | "Problems of presentation should be evaluated in terms of whether they materially impede a reader's ability to understand the work and its relevance." | https://jmlr.org/tmlr/acceptance-criteria.html |
| Does the paper make bold unsupported claims, fail to be clear, claim novelty incorrectly, or merely re-implement a known reproduction? | "Papers that should not be accepted include papers that make bold statements unsupported by empirical or rigorous evidence, papers that aren’t clearly written, papers that incorrectly claim novelty over existing published work, and papers that merely re-implement an idea that has already been reproduced before." | https://jmlr.org/tmlr/editorial-policies.html |
| Is the paper largely AI-generated with little human involvement? | "If a paper fully is AI generated with little or no human involvement, then at least with current AI systems, it is unlikely to meet this criterion." | https://jmlr.org/tmlr/acceptance-criteria.html |
| Are there ethical concerns requiring a Broader Impact Statement, or is the existing one insufficient? | "Brief description of any concerns on the ethical implications of the work that would require adding a Broader Impact Statement (if one is not present) or that are not sufficiently addressed in the Broader Impact Statement section (if one is present)." | https://jmlr.org/tmlr/reviewer-guide.html |
| Is the contribution accepted even if modest? | "Papers should be accepted if they meet the criteria, even if the contribution or significance of the work is modest." | https://jmlr.org/tmlr/editorial-policies.html |
| Which requested changes are critical versus merely strengthening? | "List of proposed adjustments to the submission, specifying for each whether they are critical to securing your recommendation for acceptance or would simply strengthen the work in your view." | https://jmlr.org/tmlr/reviewer-guide.html |

## 3. Certifications as a reviewer rubric

| Certification | Reviewer questions | Grounding quotation | URL |
|---|---|---|---|
| Outstanding | Is the work exceptionally high quality and broadly significant for the field, comparable to a best paper at a top-tier conference? (Jointly awarded by the editorial board, possibly a year or more later.) | "The editorial board of TMLR jointly awards this certification to papers which are deemed to be exceptionally high quality and broadly significant for the field." | https://jmlr.org/tmlr/editorial-policies.html |
| Featured | Are the contributions significant, novel, clearly explained, and well supported by evidence, theory, or analysis? Would it be an oral or spotlight at a top-tier conference? | "These papers present significant contributions which are novel, clearly explained, and well supported with evidence, theory, or analysis." | https://jmlr.org/tmlr/editorial-policies.html |
| Reproducibility | Is the primary purpose reproduction of published work, and does it add significant value (baselines, analysis, ablations, insights) beyond verification? | "Beyond simple verification, the paper must contribute significant added value through additional baselines, analysis, ablations, or insights." | https://jmlr.org/tmlr/editorial-policies.html |
| Survey | Beyond meeting acceptance criteria, is the survey exceptionally thorough or insightful? (New survey submissions are no longer considered as of 2026-09-01.) | "Papers that not only meet the criteria for acceptance but also provide an exceptionally thorough or insightful survey of the topic or approach may be awarded this certification." | https://jmlr.org/tmlr/editorial-policies.html |
| J2C | Would the work be appropriate for the joint NeurIPS/ICLR/ICML Journal-to-Conference Track? | "Awarded to publications based on responses by the AE and reviewers, to the question of whether the work would be appropriate for the joint NeurIPS/ICLR/ICML Journal-to-Conference Track." | https://jmlr.org/tmlr/editorial-policies.html |
| Expert | Is the paper authored by highly-rated TMLR reviewers? (Not author-controllable.) | "Awarded to papers that are authored by highly-rated TMLR reviewers (i.e. our Expert Reviewers), to recognize their contributions and expertise." | https://jmlr.org/tmlr/editorial-policies.html |

Certification process notes, each quoted: "Certification selection is the responsibility of the AE, however you are asked to submit your recommendation." (https://jmlr.org/tmlr/reviewer-guide.html); "TMLR instead relies on certifications (such as “Featured” and “Outstanding”) to provide annotations on submissions that pertain to (more speculative) assertions on significance or potential for impact." (https://jmlr.org/tmlr/acceptance-criteria.html).

## 4. Review timeline facts (for planning)

- Reviewers are asked to finish in two weeks (up to 12 pages of main content) or four weeks (longer). — > reviews must be submitted within 2 weeks of their assignment by the AE for submissions up to 12 pages (of main content, before references), and 4 weeks for submissions over 12 pages. — https://jmlr.org/tmlr/reviewer-guide.html
- Decision outcomes. — > The discussion period ends when the action editor enters a decision for the paper, which is one of the following: — https://jmlr.org/tmlr/editorial-policies.html

## Outstanding actions

These pages or details could not be verified headlessly with the permitted hosts. None of their content was reconstructed.

1. OpenReview submission form (https://openreview.net/group?id=TMLR): the page returned HTTP 200 but is a JavaScript shell (`<title>TMLR | OpenReview</title>`); the actual submission-form fields, any checkboxes, and the exact camera-ready upload form could not be read. Pointer: open the TMLR venue page while logged in and read the "New Submission" form before submitting.
2. Journal-to-Conference track eligibility lists: https://neurips.cc/public/JournalToConference, https://icml.cc/public/JournalToConference, https://iclr.cc/public/JournalToConference (host not permitted). Pointer only.
3. Certification announcements: https://medium.com/@TmlrOrg/tmlr-joins-neurips-icml-iclr-journal-to-conference-track-937a898eab3d and the 2024 and 2025 Outstanding Certification posts (https://medium.com/@TmlrOrg/announcing-the-2024-tmlr-outstanding-certification-65f25d05c37c, https://medium.com/@TmlrOrg/announcing-the-2025-tmlr-outstanding-certification-e26d548ff011) (host not permitted). Pointers only.
4. Quota tool and rule: https://www.cs.cmu.edu/~nihars/quota/author.html?rule=generalized&N1=2&A=9&NA=9 and https://arxiv.org/abs/2606.10293 (hosts not permitted). Authors should check remaining budget there before submitting.
5. Revision-comparison guide: https://kyunghyuncho.me/tmlr-how-to-check-the-difference-between-revisions/ (host not permitted).
6. Other referenced pages not fetched: https://tmlr.infinite-conf.org/index.html, https://tmlr-beyond-pdf.org, https://openreview.net/group?id=TMLR/Expert_Reviewers (not required for authors).
7. No page fetched states a mandatory reproducibility checklist, a minimum or maximum page count, or a dedicated limitations section requirement. If a checklist appears in the OpenReview form (item 1), add it here.
