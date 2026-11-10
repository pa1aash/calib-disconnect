# Scored URLs (step 2.3)

Utility scoring is done by five candidate-specific screeners, who read every record's title and abstract: research/positioning/w4/parts/screen-{L1,L2,L3,L4,F}/SELECTION.md.
- The merged queue has 134 unique papers: 59 CLOSE and 75 RELATED.
- 126 of them have arXiv ids. 29 already have vault notes from earlier runs; these are re-tagged rather than refetched when the existing note holds full text.
- Batches: 12, round-robin, with CLOSE papers spread evenly (4 or 5 per batch). The queue is in research/positioning/w4/parts/batches.json.
- Lead resolution: batch 13, which resolves 34 named seed leads by title.
