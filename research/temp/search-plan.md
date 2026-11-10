# Search plan (step 2.1)

The fixed query lists are in research/positioning/w4/QUERIES.md (76 queries: L1 20, L2 19, L3 15, L4 12, F 10), written before searching per POSITIONING_BRIEF_R1 A27. Lenses:
- Breadth (lens A): the core-claim queries per candidate (for example L1-01..05, L2-01..04, L3-01..03, L4-01..03, F-01..03).
- Depth (lens B): academic APIs only, by wave rule. OpenAlex (title and abstract plus partial full text), arXiv metadata, OpenReview v1. The seed leads are resolved by title in fetch batch 13. Citation chaining is done by Semantic Scholar forward-citation screens on close occupants (step 4 complement, w4/parts/fcs-*).
- Adversarial (lens C): queries that look for occupants of claims we would like to make, which is the adversarial direction for a novelty check. Examples are L2-05 "LLMs know more than they show", L2-14 trained verbal confidence, L2-15 faithfulness and steering, L1-13 test insufficiency, L1-15 ECE estimator bias, L3-13 capitulation, and F-05..F-08 existing decompositions. Count of adversarial queries: 12 (5 or more required).
- Lens D: not applicable (no time_periods).
Search execution log: research/positioning/w4/SEARCH_LOG.md. Candidates: research/positioning/w4/search/candidates.tsv (1,579 unique records).
