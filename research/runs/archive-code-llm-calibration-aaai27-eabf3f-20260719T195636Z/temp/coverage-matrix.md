## Coverage Matrix — query phrase → atomic item mapping

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "extend this paper" | Sub-Q3 (where current paper falls short + prescriptive extension); entity: candidate paper idea | OK — anchored to actual v3 manuscript in query file | No |
| "make it AAAI 27 main track level" | Sub-Q3; scope_condition (AAAI-27 novelty bar); required §5-§9 | OK — main-track = novelty + confident positive contribution | No |
| "Go through previous works within this field" | Sub-Q1 (frontier); §1; §10 shortlist; all lit-cluster entities | OK — full field scope, not narrowed to one sub-area | No |
| "look for caveats and holes that we can write a paper in" | Sub-Q2 (holes/open problems); §2 | OK | No |
| "shortlist ~5-10 papers" | required_format (shortlist); §10; Sub-Q4 | OK — explicit count preserved | No |
| "synthesize ... one final paper idea" | Sub-Q5; §5 (committed recommendation); entity: candidate paper idea | OK — exactly ONE, synthesize modality | No |
| "confident headline result" | Sub-Q5, Sub-Q6, Sub-Q7; §6, §7 | OK — headline + why it lands | No |
| "extremely novel" | scope_condition (P1 novelty); §9 novelty defense | OK — novelty is priority 1, defended vs closest work | No |
| "dont want to ... waste time and money ... dead paper" | Sub-Q7 (feasibility, failure mode, fallback); §7, §8; compute scope_condition | OK — confidence/feasibility is priority 2 | No |
| "priority 1 novelty / priority 2 confidence" | scope_condition (binding rank); drives §4 scoring axes | OK — both axes explicit and ordered | No |
| "this field" (code-LLM calibration) | all lit clusters: calibration, train-time cal, self-consistency/semantic uncertainty, selective generation/abstention, trust calibration | OK — field read broadly across 5 sub-literatures, not just "calibration for code" | No |
| implicit: single-GPU compute ceiling | scope_condition; §7 | OK — pulled from grounding (A100/GH200 only) | No |
