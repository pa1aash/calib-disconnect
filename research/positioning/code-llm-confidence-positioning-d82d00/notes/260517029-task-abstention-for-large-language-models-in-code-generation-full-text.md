---
title: '[2605.17029] Task Abstention for Large Language Models in Code Generation
  — Full Text (PDF)'
id: 260517029-task-abstention-for-large-language-models-in-code-generation-full-text
tags:
- code-llm-calibration-aaai27-eabf3f
- locus-fallback-utility-of-collapsed-confidence
- abstention
- selective-generation
- code-llm-confidence-positioning-d82d00
created: '2026-07-17T19:02:32.812171Z'
updated: '2026-11-09T23:27:43.882987Z'
source: http://arxiv.org/pdf/2605.17029
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'CODEREFUSER (Zhou et al., arXiv 2605.17029): Learn-Then-Test risk-controlled
  abstention with execution-consistency cluster ratio/semantic entropy over generated
  tests; HumanEval and MBPP, four open code LLMs 7B-33B; +26.5 pp precision, +11.9
  pp F1 vs best baseline; MBPP Qwen2.5-Coder-32B at alpha=0.2 abstains ~30% vs >80%
  for PPL. Full text. CLOSE occupant for L3 abstention/selective use, not execution-budget
  routing vs random/oracle, no verbal update after failures.'
---

*Suggested by [[260517029-task-abstention-for-large-language-models-in-code-generation]] — Full-text follow-up fetch of the PDF; the original note only captured the arXiv abstract page, which gave no concrete accuracy/coverage numbers. This note extracts the concrete results tables.*

## Structured Claims Extraction (full-text, PDF-sourced)

**Paper**: Yanke Zhou, Yuhao Tan, Senrong Xu, Zenan Li, Yuan Yao, Taolue Chen, Xiaoxing Ma (Nanjing University / City, University of London). "Task Abstention for Large Language Models in Code Generation" — method name: **CODEREFUSER**. arXiv:2605.17029, submitted 16 May 2026.

**Method summary**: Built on the Learn-Then-Test (LTT) framework (Angelopoulos et al. 2025) applied to multiple hypothesis testing over a VECTOR of thresholds (not a single threshold like classical conformal risk control). Defines admission risk `R(x) = (1-r(x)) * H@k`, where `H@k` is the probability that k randomly generated samples are ALL incorrect (estimated via `C(n-c,k)/C(n,k)` from n generated samples with c correct ones). Refusal rule `r(x;lambda)` triggers abstention if ANY of N score functions `g_i(x) >= lambda_i`. Two scoring modes: **Cluster Ratio (CR)** — abstain if no execution-based semantic cluster of generated code samples reaches a minimum share `lambda_score` of all samples; **Semantic Entropy (SE)** — abstain if the entropy of the cluster distribution exceeds `lambda_score`. A **Sample-Test Dual Filtering (STDF)** mechanism prunes noisy/invalid LLM-generated test cases (by error rate and by output-diversity/entropy) before clustering, since raw generated tests are unreliable.

**Zero-oracle at test time — explicitly confirmed**: Oracle test cases ARE used during the CALIBRATION phase (`D_cal = {(x_i, t_i)}`, oracle tests needed to compute ground-truth H@k and pick valid thresholds `Lambda_valid`). At TEST/DEPLOYMENT time, the method uses ONLY LLM-generated test cases and execution-consistency clustering — "without reliance on oracle test cases or external databases" (verbatim from abstract), confirmed in Section 3.4: the testing phase "generat[es] n code samples Y and test cases T for the input prompt x" with no oracle involved, filtered via STDF. So: **not a fully zero-oracle method overall** (calibration needs oracle tests once, offline) but **zero-oracle at inference/test time**, which is the practically relevant claim.

**Benchmarks**: HumanEval (164 hand-crafted Python problems, 5-10 oracle tests each) and MBPP (~1000 Python problems, 3 oracle tests each). Cross-dataset transfer also tested (calibrate on MBPP, test on HumanEval). Only Python is evaluated (explicitly listed as a limitation).

**Code LLMs (all open-source, matches "no oracle" framing)**: DeepSeek-Coder-33B, Qwen2.5-Coder-32B, CodeLlama-7B, WizardCoder-33B-V1.1. Sampling temperature 0.8, top-p 0.95.

**Default hyperparameters**: risk tolerance **alpha = 0.2**, significance level **delta = 0.1** (90% confidence), **k = 3** for the H@k pass criterion, **60%/40% calibration/test split**. For calibration+testing score computation, 64 code samples and 64 test cases are generated per problem (N=64); ground-truth labels for evaluation use 256 generated samples checked against ORACLE tests (this 256-sample check is only for constructing ground truth abstention labels, not part of the deployed method).

**Evaluation metric — Precision and F1 of the ABSTENTION DECISION itself, not accuracy-among-accepted-outputs**: Ground truth abstention label = true if H@k (computed from 256 oracle-checked samples) exceeds alpha. Precision = fraction of tasks the method predicts should-abstain that are truly hallucination-prone (ground-truth label = abstain). The paper explicitly avoids Recall as a primary metric because trivially refusing everything inflates it. **Note: this is a different quantity than CIC's FDR/coverage framing** — CODEREFUSER's Precision/F1 measure the quality of the abstain/answer CLASSIFICATION against a ground-truth pass-rate label, not the error rate remaining among the accepted (non-abstained) outputs. The paper does NOT report a direct "accuracy of accepted outputs" number in the same style as CIC.

**Exact result numbers — Table 1 (Precision / F1, %), main comparison, N=64 samples**:

| Dataset | Model | Method | Precision | F1 |
|---|---|---|---|---|
| HumanEval | DeepSeek-Coder | Execution (baseline) | 39.28 | 55.27 |
| HumanEval | DeepSeek-Coder | **CR+STDF (ours, best)** | **72.00** | **69.92** |
| HumanEval | Qwen2.5-Coder | Execution (baseline) | 24.29 | 38.23 |
| HumanEval | Qwen2.5-Coder | **CR+STDF (ours, best)** | **73.33** | **53.85** |
| HumanEval | CodeLlama | Execution (baseline) | 72.15 | 83.82 |
| HumanEval | CodeLlama | **CR+STDF (ours, best)** | **91.67** | **91.70** |
| HumanEval | WizardCoder | Execution (baseline) | 35.46 | 51.55 |
| HumanEval | WizardCoder | **SE+STDF (ours, best)** | **62.71** | 66.67 |
| MBPP | DeepSeek-Coder | Execution (baseline) | 41.31 | 57.42 |
| MBPP | DeepSeek-Coder | **SE+STDF (ours, best)** | **72.65** | **72.88** |
| MBPP | Qwen2.5-Coder | Execution (baseline) | 31.50 | 46.11 |
| MBPP | Qwen2.5-Coder | **CR+STDF (ours, best)** | **48.94** | 47.44 |
| MBPP | CodeLlama | Execution (baseline) | 58.35 | 73.01 |
| MBPP | CodeLlama | **CR+STDF (ours, best)** | **79.40** | **79.69** |
| MBPP | WizardCoder | Execution (baseline) | 36.08 | 51.75 |
| MBPP | WizardCoder | **CR+STDF (ours, best)** | **69.23** | 63.07 |

Cross-dataset transfer (calibrate MBPP -> test HumanEval), CR+STDF: DeepSeek-Coder P=66.67/F1=66.67; Qwen2.5-Coder P=40.63/F1=40.00; CodeLlama P=91.51/F1=91.23; WizardCoder P=72.10/F1=62.39 — "close performance to the in-distribution case in most cases," confirming the theoretical i.i.d. guarantee degrades gracefully under moderate distribution shift.

**Headline aggregate claim (verbatim from text)**: averaged across models/datasets, CODEREFUSER (best variant) achieves **26.5 percentage points absolute improvement in abstention precision** and **11.9 points absolute improvement in F1** over the best existing competitor baseline (Execution / CodeHalu / PPL / NLI / CLM).

**Concrete abstention-rate / coverage number (Fig. 3, the closest analogue to CIC's "coverage at a risk level")**: On MBPP with Qwen2.5-Coder-32B, at admission-risk tolerance **alpha=0.2**, CODEREFUSER's CR variant needs to abstain on only **~30% of tasks** (i.e., ~70% coverage/answering rate) to keep the admission risk under 0.2, whereas the PPL static baseline must abstain on **over 80% of tasks** (< 20% coverage) to meet the same risk bound. This is the single clearest "coverage at a given alpha" figure reported.

**Risk-control validity check (Fig. 2, in-distribution, DeepSeek-Coder + Qwen2.5-Coder on HumanEval, alpha in {0.10,0.15,0.20,0.25}, delta=0.1, k=3)**: empirical admission risk is reliably controlled below the target alpha; the paper states the method "remains effective in over 90% of cases in terms of keeping the risk below the desired tolerance level" (i.e., ~90%+ of the probability mass of admitted tasks has risk under alpha; this is looser language than a hard 1-delta guarantee check across many repeated trials, unlike CIC's 100-split mean/std reporting).

**Sensitivity to k (Table 3, k=5 instead of k=3)**: negligible change from the k=3 results — e.g., HumanEval CodeLlama not reported at k=5 in the visible table (only DeepSeek-Coder/Qwen2.5-Coder/WizardCoder shown), CR+STDF Qwen2.5-Coder P=70.33/F1=53.90 (vs. 73.33/53.85 at k=3) — confirms robustness to the k choice.

**Sample-efficiency claim (Table 2)**: giving static baselines (PPL, CLM) 4x more samples (N=256 vs. CODEREFUSER's N=64) does NOT close the gap — e.g. PPL(N=256) on DeepSeek-Coder: P=37.02/F1=54.36 vs. CODEREFUSER(N=64) P=72.00/F1=69.92. This is used to argue the gap is qualitative (execution vs. static token-probability signals), not just a sampling-budget artifact.

**No explicit FDR-style "hallucination rate among accepted outputs" number is reported** in the extracted text — the paper's primary metrics are abstention-decision Precision/F1 against a 256-sample oracle-derived ground truth label, plus the Fig. 2/Fig. 3 admission-risk-distribution and abstention-rate plots. This is a genuine format mismatch versus CIC's FDR/coverage tables and should be flagged if directly comparing "coverage at alpha" numbers across the two papers.

---

## Full Extracted Text (PDF, pdfplumber)

--- PAGE 1 ---
TASK ABSTENTION FOR LARGE LANGUAGE MODELS
IN CODE GENERATION
YankeZhou YuhaoTan SenrongXu
StateKeyLaboratoryof StateKeyLaboratoryof StateKeyLaboratoryof
NovelSoftwareTechnology NovelSoftwareTechnology NovelSoftwareTechnology
NanjingUniversity NanjingUniversity NanjingUniversity
ZenanLi YuanYao TaolueChen
StateKeyLaboratoryof StateKeyLaboratoryof SchoolofComputingand
NovelSoftwareTechnology NovelSoftwareTechnology MathematicalSciences
NanjingUniversity NanjingUniversity UniversityofLondon
XiaoxingMa
StateKeyLaboratoryof
NovelSoftwareTechnology
NanjingUniversity
ABSTRACT
Largelanguagemodels(LLMs)haverevolutionizedautomatedcodegeneration. Oneseriouscon-
cern, however, istheso-called“hallucination”, i.e., LLMsmaygenerateseeminglyplausiblebut
functionallyincorrectcode. Inthispaper,westudythetaskabstentionproblem,i.e.,determining
whetheragivenLLMshouldabstainfromperformingaspecificcodegenerationtasktoavoidlikely
hallucination. Ourapproachfeaturesacalibratedabstentionrule,groundedintheprinciplesofmulti-
plehypothesistesting. Theruleassessesgenerationconsistencythroughcodeexecutionoutcomes,
allowingittohandlesyntacticdiversityofsemanticallyequivalentcodewithoutrelianceonoracle
testcasesorexternaldatabases. Weprovethatourapproachprovidesarigorous,distribution-free
theoreticalguaranteeonitsabstentiondecisions. Weevaluateourmethodonbenchmarkdatasets
usingseveralopen-sourcecodeLLMs. Resultsshowthatourmethodallowsgenerativemodelsto
moreaccuratelyandefficientlyidentifyandabstainfromtasksthatinducehallucinationcomparedto
existingtechniques,providingareliablemechanismforsaferandmorerobustcodegeneration.
1 Introduction
Therecentadvancementsinlargelanguagemodels(LLMs)arerevolutionizingthefieldofcodegenerationLietal.
[2022],Chenetal.[2021],Roziereetal.[2023]. Asthesemodelsareincreasinglyintegratedintosoftwaredevelopment
workflows,ensuringtheirtrustworthinessandreliabilityhasbecomeapressingrequirement. However,currentLLMs
tendtohallucinate,i.e.,theymayproduceoutputsthatareseeminglyplausiblebutareactuallyincorrectHuangetal.
[2025a]. Thispaperisparticularlyconcernedwithmitigatinghallucinationinthecontextofcodegeneration,forwhich
Leeetal.[2025]providedarecentsurvey.
Existingworkoncodehallucinationdetectionhaspredominantlyfocusedonsamplehallucination,thatis,agenerated
codesnippetthatfailstoexecuteasexpectedormeetspecifiedrequirements,despitebeingsyntacticallycorrectoreven
semanticallyplausibleTianetal.[2025]. However,thereisanarguablymorefundamentalsourceofhallucination,i.e.,
thetaskitself. Thismightbecausedbyambiguousorunclearprompts,orbytheinherentlimitationofcurrentLLMs
whicharedoomedtofailoncertainproblems. Tothisend,weproposetostudythetaskabstentionproblemforcode
generation,whichaimstofaithfullydetectcodegenerationtasksthatanLLMisunlikelytosolve.
Tobespecific,weformulatethebasicconceptoftaskabstentionandproposeacomprehensiveapproach,CODERE-
FUSER,tocontrolitsassociatedriskswiththeoreticalguarantees. OurapproachisbuiltupontheLTTframeworkAn-
gelopoulosetal.[2025]andconsistsoftwophases: calibrationandtesting. Duringthecalibrationphase,different
E-mail:yankezhou@smail.nju.edu.cn
6202
yaM
61
]ES.sc[
1v92071.5062:viXra
--- PAGE 2 ---
PREPRINT
fromtraditionalNLPtasks,weproposetousetestcaseswhenconstructingthecalibrationset. Theintuitionisthat
syntacticallydifferentprogramsmayexhibitthesamesemantics,andthecorrectnessofprogramsshouldbebetter
determinedbyrunningthetestcases. ScoringfunctionliesattheheartoftheLTTframework. Wethendefinetwoscore
functionsleveragingtheexecution-basedresults. Oneissuehereisthatoracletestcasesarenotusuallyavailableduring
thetestingphase. Tothisend,weprompttheLLMtogeneratenotonlycodesolutionsbutalsocorrespondingtestcases,
andproposeasample-testdualfilteringmechanismtodealwithpotentiallyflawed,model-generatedtestcases.
We conduct evaluations across several representative code LLMs and code generation benchmarks. The results
demonstrate the effectiveness of our method on the task abstention problem for LLM-based code generation. For
example,onaverage,ourmethodachieves26.5%absoluteimprovementcomparedtothebestexistingcompetitorin
termsofabstentionprecision. Byanalyzingtheresults,wefindthat: 1)staticmethodsthatadopttraditionalNLPscore
functionsareinsufficientforaccurateabstention;and2)runningthegeneratedcodeisnecessarybutheavilyrelieson
thequalityofgeneratedtests,andoursample-testdualfilteringmechanismiscrucialfortheeffectiveness. Additionally,
thetheoreticalguaranteesareconfirmedbyourempiricalexperiments.
Ourcontributionscanbesummarizedasfollows. (1)Weintroduceandformalizetheconceptoftaskabstentioninthe
contextofLLM-basedcodegeneration,incontrasttothesample-levelhallucination. (2)Weproposeanovelapproach
foraccuratetaskabstention,enablingthemodeltoanswer“Idon’tknow”whenencounteringtasksitisunlikelyto
solve. The approach features two advantages: i) rigorous theoretical guarantees grounded in multiple hypothesis
testing,andii)aminimalrelianceontheoracletestcasesorexternalreferences.
2 ProblemFormulation
Throughoutthepaper,weuseX tostandfortheinputspaceconsistingofasetoftasks(i.e.,prompts)forLLMs,andY
fortheoutputspace. Typically,y ∈Y isacodesnippetgeneratedbytheLLM.Thetaskabstentionproblemisdefined
asfollows.
Definition1(TaskAbstentionforLLM-basedCodeGeneration). Consideracodegenerationtask(prompt)x∈X
andanLLMM : X → Y whichgeneratesacodesnippety ∈ Y. Taskabstentionaimstofindarefusalfunction
r :X →{0,1}forM,wherer(x)=1indicatesMshouldabstainfromansweringandr(x)=0indicatesotherwise.
Whentorefusethetask. Inthiswork,forcodehallucinationweadoptthedefinitionofTianetal.Tianetal.[2025],
consideringaplausiblebutfunctionallyincorrectcodesnippetashallucination,althoughtheproposedapproachcanbe
adaptedtohandleothertypesofhallucinationLeeetal.[2025]. Asaresult,adesirablerefusalfunctionrshouldbeable
toidentifythecasewhenthegivenLLMisunlikelytoproduceafunctionallycorrectcodesnippetforthegiventask.
Taskabstentionvs. samplehallucinationdetection. Samplehallucinationdetectionaimstodetectindividualcode
snippetsgeneratedbythemodelthatcannotbeexecutedasexpected. Incontrast,taskabstentionaimstoidentifythe
promptsforwhichanLLMisunlikelytogeneratethecorrectanswer,eveniftheLLMisallowedtoproduceahigh
volumeofsamples.
Evaluation Criterion. We instantiate the refusal function by defining a criterion. Specifically, for a given prompt
x,M(x)givesadistributionontheoutputspaceY,andthusarandomoutputis(functionally)correctforacertain
probability(whichisunknowningeneral). WedefineanewmetricH@k,whichistheprobabilitythatkrandomly
generatedsamplesareallincorrect.
Ideally,whentheoracletestcasesareavailable,wecandetermineifageneratedcodesampleiscorrectbyexecuting
these test cases. We consider the process of first generating a sample of n (n > k) instances, and then count the
numberofincorrectsamples. Assumingthatthesengeneratedsamplescontainccorrectinstances,H@kmetriccanbe
estimatedby
(cid:0)n−c(cid:1)
H@k := k . (1)
(cid:0)n(cid:1)
k
Definition2((k,α)-CriterionforTaskAbstention). ThegivenLLMshouldrefusethecodegenerationtaskifitsH@k
metricexceedsathresholdα,i.e.,H@k >α.
Henceforthαisreferredtoastherisktolerance,whichisfixedinadvance. Forexample,H@k >0.8meansthatthe
LLMcannotgenerateacorrectcodesnippetinkattemptswithprobabilitygreaterthan0.8.
2
--- PAGE 3 ---
PREPRINT
Calibration Set Calibration Phase
Task prompt Test cases Generated code samples
C nu he m c b k e i r f s, in ar g e iv … enlistof Testcases Ca 𝜆( n 1) d : i { d 0 a ,0 te .1 P ,0 a .2 ra ,⋯ Se ,1 t } 𝜦 Multiple Valid 𝜆 P (1 a ) r : a {0 S , e 0 t .1 𝜦 } 𝑣𝑎𝑙𝑖𝑑
Hypothesis
Y d o ep u o 'r s e it g a i n v d en … a list of Testcases 𝜆 𝜆 ( ( 2 3 ) ) : : { { 0 2 , 0 1 % 0, , 1 3 0 0 0 % , , ⋯ ⋯ , } } Testing 𝜆 𝜆 (3 (2 ): ): {2 {0 0 , % 10 ,3 ,2 0 0 % } }
Inputtothisfunctionis
Testcases
astring…
F n o u r m a be g r i s … v , e … n … … listofinput Tes … tca … ses C LL o M de 𝜆 𝜆 ( ( 1 2 ) ) = = 0 4 . 0 2 Risk Distribution A to b le o r v a e n r c i e sk B to e l l e o r w an r c is e k Risk Distribution 𝜆 𝜆 ( ( 1 2 ) ) = = 0 1 . 0 1
𝜆(3)=60% 𝜆(3)=20%
Writeafunctiontofindtheminimum
costpathtoreach(m,n)from(0,0)for Score Function Computation Abstention Score1 <𝜆(1)
thegivencostmatrixcost[][]anda Generated code samples Test Case Sample-Test Score Rule Score2 < 𝜆(2)
position(m,n)incost[][]. Generation
Dual Filtering Computation Application Score3 < 𝜆(3)
Abstention Rules
Test Task Prompt 𝒙 𝒕𝒆𝒔𝒕 Testing Phase
Figure1: TheOverviewofCODEREFUSER.
3 Methodology
3.1 Overview
Inthiswork,webuildourtaskabstentionapproachupontheLearnThenTest(LTT)frameworkAngelopoulosetal.
[2025]. We choose LTT as it can provide statistical guarantees for machine learning models by simply adding a
post-processingstepafterthemodelistrained. Specifically,LTTallowsustocalibrateathresholdλusingacalibration
setD ;itguaranteesthatforanewtesttaskx ,theriskofacceptinganincompetenttaskiscontrolledwithhigh
cal test
probability:
(cid:16) (cid:17)
P E[R(x ;λˆ)|D ]≤α ≥1−δ, (2)
test cal
whereRistheadmissionrisk(discussedlaterinSection3.2),αistheuser-specifiedrisktolerance,and1−δisthe
confidencelevel(e.g.,90%). WereferreaderstoAppendixBforthetheoreticalpreliminariesofLTTandthemultiple
hypothesistestingprocedureusedtoderiveλˆ.
AnoverviewoftheproposedapproachCODEREFUSERisdepictedinFig.1,whichisdividedintocalibrationphase
andtestingphase.
Thecalibrationphasetakesasinputacalibrationset,whichcontainsasetoftaskdescriptionsandthecorresponding
testcases. Theoutputofthecalibrationphaseisasetofabstentionrules. Specifically,followingtheLTTframework,
CODEREFUSERfirstdefinesanadmissionriskmeasuringtheriskthattheLLMcannotgeneratethecorrectcodeforan
admittedtask. Then,CODEREFUSERdefinesasetofscorefunctions,andderivesthecomputedscoresforeachtask
inthecalibrationset. Foreachscorefunction,acorrespondingabstentionruleisobtained,byselectingthesuitable
parameters(i.e.,asetofvalidthresholds,Λ )sothattheadmissionriskisbelowagiventolerancelevel(i.e.,α),
valid
under multiple hypothesis testing with a given significance level (i.e., δ). The abstention rules are in the form of
a conjunction of inequalities, each describing the relationship between a score function applied on the input code
generationtaskandthecorrespondingvalidthreshold.
Thetestingphasetakesthecurrentcodegenerationtaskasinput,anddetermineswhethertheLLMshouldabstainfrom
generatingthecode. Foranygiventesttask(prompt),CODEREFUSERfirstgeneratesasetoftestcases,basedonwhich
thescorefunctionscanbeapplied. Akeyissueisthatthegeneratedtestcasesmaybeinvalid. Tomitigatethisissue,
weproposeasample-testdualfilteringmechanism. CODEREFUSERthenappliestheabstentionrulesonthetesttask,
basedonwhichtheabstentiondecisionismade.
Note that the calibration phase can be done in advance. Once the abstention rules are obtained, we can guarantee
that, duringthetestingphasewhenani.i.d. codegenerationtaskisgiven,1 theperformanceof CODEREFUSER is
theoreticallyguaranteedbyEq.(2),i.e.,theLLMensuresthatoncethecodegenerationtaskisadmitted,theriskof
failingthetaskisbelowthetoleranceαwithprobabilityatleast1−δ.
1Onemayarguethatthei.i.d.assumption,whichisessentialforthestatisticalguarantee,istoostronginpractice.However,as
willbeshownintheexperimentslater,weobservethattheabstentionrulesobtainedfromonedatasettransferwellwhentheyare
testedonotherdatasets.
3
--- PAGE 4 ---
PREPRINT
3.2 TheCalibrationPhase
Thecalibrationphaseconsistsofseveralkeycomponents,includingthecalibrationsetconstruction,theadmissionrisk
definitionandevaluation,thedeterminationofvalidthresholdset,andthedefinitionofscorefunctions. Wemainly
describetheformerthreecomponentshere,andleavethescorefunctionsinSection3.3,astheywillbereusedbythe
testingphase.
CalibrationSetConstruction. Incodegeneration,akeydifferencefromthestandardLTTframeworkliesintheoutput
space,whichisgenerallyinfinite. Asaresult,insteadofprovidingthecodegenerationpromptandthecorresponding
correctcodeasthecalibrationset,weusethecodegenerationpromptandthecorrespondingoracletestcases. Thatis,
D ={(x ,t )}m . Ingeneral,thecorrectnessofthegeneratedcodesnippety forx isdeterminedbyexecutingy
cal i i i=1 i i i
onthetestcasest .
i
AdmissionRisk. RecallthatourgoalistoensurethatmodelM’sriskonanygiventaskxisbelowtherisktoleranceα.
Werefertothisriskasadmissionrisk,anddefineitas
R(x)=(1−r(x))·H@k, (3)
wherer(x)istherefusalfunctioninDefinition1,andH@kisdefinedinEq.(1). Essentially,Eq.(3)measurestherisk
whenacodegenerationtaskisadmitted(i.e.,r(x)=0),buttheLLMcannotgeneratethecorrectcodewithprobability
H@kinkattempts.
Duringthecalibrationphase,sincewehavetheoracletestcases,H@kcanbeaccuratelyevaluated. Forr(x),wealso
resorttothecalibrationsetanddesignabstentionrulesparameterizedbytheparametersλλλ=(λ ,··· ,λ )asfollows:
1 N
(cid:26)
1, if∀1≤i≤N.g (x)<λ ,
rˆ(x;λλλ)= i i (4)
0, o.w.
whereeachg (x)∈Ryieldsascoreforthecurrentcodegenerationtaskx,andggg =(g ,···g )representsthevector
i 1 N
ofsuchscorefunctions. Inthecalibrationphase,thecomputedscoresareusedtodeterminethevalidthresholds,sothat
theadmissionriskiscontrolledbelowthepre-specifiedrisktoleranceαwithahighprobability. Specifically,giventhe
scorefunctions,thechoiceofλλλdictatesrˆ,whichinturninfluencestheadmissionrisk,denotedasRˆ(x;λλλ).
DeterminingΛ . Givencandidateparametersλλλ,theadmissionriskforeachsample(x ,t )∈D iscomputedas
valid i i cal
follows. Forthepromptx ,wefirstusethecurrentLLMtogeneratencodesamples. Next,weidentifythenumber
i
ofcorrectsamples,c,byapplyingthetestcases. ThenH@kcanbecalculatedbyEq.(1). Oncetheriskvalueshave
beencomputedacrossthecalibrationsetfortheentirerangeofcandidateparameters,weapplythestandardmultiple
hypothesistestingproceduretoidentifythesetΛ ofvalidthresholds.
valid
Letx beanewtestprompt;forthegivenδ ∈(0,1),ifλλλ∈Λ ,ourabstentionrulecandeterminewhetherto
test valid
abstainonx ,satisfyingthefollowingguarantee,
test
(cid:16) (cid:17)
P Rˆ(x ;λλλ)≤α ≥1−δ. (5)
test
Eq.(5)statesthatforanytaskfromthetestset,ourabstentionruleprovidesthefollowingprobabilisticguarantee: with
aconfidenceofatleast1−δ,themodelwilleitheradmitthetask,inwhichcaseH@kiscontrolledtobebelowα,orit
willabstain. ThisguaranteedirectlysatisfiesthecriterionfortaskabstentionestablishedinDefinition 2.
3.3 ScoreFunction
ThescorefunctionplaysavitalroleintheLTTperformanceAngelopoulosetal.[2025]. Whilecodegenerationisatype
ofgenerativetask,codeisauniquemodalitywherecodesampleswithidenticalsemanticmeaningcanpossessvastly
differentsyntacticforms. Consequently,wearguethatexistingscorefunctionsoperatingatalinguisticlevelQuachetal.
[2023]orasemanticreasoninglevelManakuletal.[2023]areunsuitableforthecodegenerationtask. Wetherefore
proposeascoringschemebasedonruntimedetection,whichleveragesgeneratedtestcases.
Specifically,foragiventaskx,thegeneratedcodesamplesY ={y ,··· ,y }andasetoftestcasesT ={t ,··· ,t },
1 n 1 l
weclusterthecodesamplesinY basedontestcases,resultinginapartitionY = C ⊎···⊎C suchthatallcode
1 h
samplesfromthesameclusteryieldidenticaloutputsforeverytestcaset∈T.2 Clusteringbasedonexecutionoutputs
providesanintrinsicmeasureofsemanticequivalenceamongcodesamples. Leveragingtheseexecution-basedclusters,
2Note that we use both the test cases in the calibration set and the LLM-generated test cases during calibration, and only
LLM-generatedtestcasesinthetestingphase.MoredetailscanbefoundinSection3.3.1.
4
--- PAGE 5 ---
PREPRINT
weemploytwocomplementaryscorefunctions: confidence-basedscore,whichmeasuresthedegreetowhichacode
sample’ssemanticbehaviorissupportedbyothergeneratedsamples(i.e.,thesizeofitsclusterrelativeton)Chen
etal.[2022]; semanticentropy-basedscore, whichquantifiestheoveralluncertaintyofthetaskbymeasuringthe
diversityoftheresultingclusterdistributionKuhnetal.[2023]. Bothmetricsarerootedinsemanticequivalencebut
servedifferentgranularities(sample-levelvs. task-level). Theformaldefinitionsandmathematicalformulationsfor
thesescorefunctionsaredetailedinAppendixC.
3.3.1 Sample-TestDualFiltering
TheabovescorefunctionsrelyonclusteringbasedonLLM-generatedtestcases. Akeyissueinthisapproachisthatthe
generatedtestcasesmaycontaininvalidinputs. Executingcodesamplesontheseinvalidinputsmayleadtoundefined
behavior. Asaresult,twosemanticallyidenticalcodesamplescouldbeassignedtodifferentclusters.
Asanexample,considerthetaskofgeneratingthen-thFibonaccinumber. Bydefault,avalidinputrequiresn ≥ 0
forthistask, makinganynegativeinputinvalid. Theproblemstatementdoesnotspecifyhowtheseinvalidinputs
shouldbehandled. Now,assumethemodelgeneratesthreesolutionsthatareallfunctionallycorrectforvalidinputsbut
handleinvalidinputsdifferently. E.g.,onesamplemightcheckfornegativeinputsandraiseanAssertError;another
couldhandleallexceptionsbyreturningadefaultvalue0;athird,lackinganyspecificerrorhandling,mightenteran
unterminatedrecursionthattriggersRuntimeError.
Theexampleillustratesthatevenwhendifferentcodesamplesshareconsistentlogicforatask,theirinteractionwitha
diverse(andpotentiallyimperfect)setofgeneratedtestcasescanexposevariationsintheirbehavior. Thisinflatesthe
measureofinconsistency. Asaresult,theabstentionrulemaybetriggered,makingLLMrefusetoprovideananswer,
eventhoughthemodelhadalreadydemonstrateditsabilitytosolvetheproblemcorrectly.
ToaddressthequalityissuesinherentinLLM-generatedtestcases,weproposetheSample-TestDualFiltering(STDF)
mechanism. ThecoreofSTDFliesinareciprocalvalidationprocess. Werelyonsemanticconsistencytoevaluatecode
quality,butwealsoleveragethecollectivebehaviorofthesecodesamplestoauditthetestcases.
This design is grounded in the principle that for a deterministic program, valid inputs yield deterministic outputs,
whereasinvalidinputstriggerundefinedbehaviors(UB),resultinginhighlydivergentexecutionoutcomes. Bydetecting
testcasesthatinducehighoutputentropyacrossthesamplepopulation,wecanidentifyandpruneinvalidinputs. This
refinedtestsuite,inturn,eliminatesevaluationnoise,allowingforamoreaccurateassessmentofthecodesamples’
semantic consistency. The mechanism consists of two filtering steps, with algorithm implementation detailed in
AppendixD.
1. FilteringbyErrorRate: Pruningteststhatcausewidespreadexecutionfailures.
2. Filtering by Output Diversity: Pruning tests that yield high semantic entropy (indicative of invalid inputs
triggeringUB).
3.4 TestingPhase
Whentheabstentionrulesareobtainedonthecalibrationset,inthetestingphase,theserulesareappliedtomakethe
abstentiondecisions. AsoutlinedinAlg.1,theprocessbeginsbygeneratingncodesamplesY andtestcasesT forthe
inputpromptx. Crucially, CODEREFUSERappliestheSTDFmechanism(Line3)topurgeinvalidtestcasesusing
thresholds[λ ,λ ,λ ]. ThecodesamplesarethenpartitionedintosemanticclustersC basedontheirexecutionoutputs
1 2 3
ontheremainingvalidtestcases. Thefinalabstentiondecisiondependsontheselectedscoringmode.
ClusterRatio(CR).Thismodeenforcesmodelconsensus. CODEREFUSERfiltersthesemanticclusters,retaining
onlythosethataccountforasufficientproportionofthetotalsamples(i.e.,|C |/|Y|≥λ ). Ifnoclustermeetsthis
i score
confidencethreshold(i.e.,thefilteredsetY becomesempty),themodelimpliesalackofconsensusandabstains.
SemanticEntropy(SE).Thismodelimitsuncertainty. CODEREFUSERcalculatesthesemanticentropyofthecluster
distribution. Iftheentropyexceedsλ ,indicatinghighsemanticdiversityandconfusion,themodelabstains. Ifthe
score
tasksatisfiesthecriterionofthechosenmode,itisadmitted.
4 Experiments
Inthissection,wepresenttheempiricalevaluationofCODEREFUSER,focusingontwoprimarydimensions. First,we
assesstheeffectivenessofourapproachonthetaskabstentionproblembybenchmarkingitagainstexistingcounterparts.
5
--- PAGE 6 ---
PREPRINT
Algorithm1CODEREFUSERInferenceProcedure
Input: LLMM;promptx;samplesn;calibratedthresholdsλλλ=[λ ,λ ,λ ,λ ]
1 2 3 score
Output: Abstentiondecision
1: procedureCODEREFUSER(M,x,n,λλλ)
2: Y,T ←Generate(M,n)
3: T ←STDF(Y,T,[λ 1 ,λ 2 ,λ 3 ])
4: C ←ClusteringY byExec(Y,T)
5: ifModeisCRthen
(cid:83)
6: Y ← {C i ∈C :|C i |/|Y|≥λ score }
7: ifY =∅thenreturnAbstain
8: endif
9: endif
10: ifModeisSEthen
11: ifSE(C)>λ score thenreturnAbstain
12: endif
13: returnAdmit
14: endprocedure
Second,weexaminethetheoreticalguaranteetoverifywhethertheriskcontrolpromisedbythecalibrationphaseis
empiricallysupported.
4.1 ExperimentalSetup
Datasets. OurexperimentsareconductedontwostandardPythoncodegenerationdatasets: HumanEvalChenetal.
[2021]andMBPPAustinetal.[2021]. HumanEvalconsistsof164hand-craftedprogrammingproblems. Eachproblem
isassociatedwith5−10oracletestcases. MBPPisalargerdatasetofnearly1,000problems. Eachtaskisdefinedbya
shortdescriptionandincludesthreetestcasestoverifyitscorrectness.
EvaluationMetrics. WeusePrecisionandF1-scoretoevaluatetheperformanceonthetaskabstentionproblem. To
obtaintheground-truthlabel,wegenerate256samplesforeachtask,andchecksthemtheontheoracletestcases. The
abstentionlabelistureiftheH@kisabovethegivenrisktolerance. WedeliberatelyavoidusingRecallasaprimary
metricduetothefollowingfact. Ahighrecallvaluecanbeeasilyobtainedforanabstentionrule,bysimplyrefusing
mosttasks. Thisismisleading,asithaslittlepracticalutility.
Baselines. Sincenopriorworkdirectlyaddressestaskabstentionforcodegeneration,weadaptthefollowingbaselines
forcomparison.
• Execution. ThismethoddirectlycalculatestheH@kscoreusinggeneratedtestcasesandabstainsifitexceedsthe
risktolerancethreshold. Itcanbeseenasanexecution-basedbaselinewithoutadoptingtheproposedframework.
• PPLHuangetal.[2025b]andNLI Manakuletal.[2023]. WeintegratethesemetricsintoourLTTframeworkas
alternativescorefunctions. PPL usesmodelperplexity(static), whileNLI queriestheLLMforself-consistency
checking.
• CLM Quachetal.[2023]. Thismethodisoriginallyproposedfornaturallanguagegeneration. Weadaptittoour
codegenerationcontext,andrefusethetaskifthecalibratedvalidresponsesetisempty.3
• CodeHaluTianetal.[2025]. Thisisanexecution-basedsample-levelhallucinationdetectorrelyingonoracletests.
We adapt it by employing LLM-generated tests as pseudo-oracles, and applying the algorithm to identify valid
samplesandaggregatethesepredictionstoestimatethetask-levelH@kfortheabstentiondecision.
ImplementationDetails. WeconducttheexperimentswithPython3.9.19,Pytorch2.4.0andvLLM0.6.1,runningon
NVIDIAH800GPUswithCUDA12.7. WeevaluatetheperformanceofthefollowingfourcodeLLMs: Deepseek-
Coder-33B Guo et al. [2024], Qwen2.5-Coder-32B Hui et al. [2024], CodeLlama-7B Roziere et al. [2023] and
WizardCoder-33B-V1.1Luoetal.[2024]. ForallthesecodeLLMs,weuseasamplingtemperatureof0.8andatop-p
of0.95. Foreachdataset,werandomlyallocate60%ofthedataforcalibration,andusetherestfortesting. Weset
α=0.2,δ =0.1,k =3bydefault.
3WeusethemaxversionofCLMasitdemonstratesthebestempiricalperformance.
6
--- PAGE 7 ---
PREPRINT
Table 1: Task abstention results on HumanEval and MBPP. Our approaches (i.e., ‘SE+STDF’ and ‘CR+STDF’)
generally outperform the competitors. Similarly, when the calibration is conducted on MBPP and the testing is
conductedonHumanEval(‘MBPP→HumanEval’),ourapproachesstilloutperformthecompetitorsandevenachieve
closeperformancetothein-distributioncaseinmostcases.
Model DeepSeek-Coder Qwen2.5-Coder CodeLlama WizardCoder
Method P F1 P F1 P F1 P F1
HumanEval
Execution 39.28 55.27 24.29 38.23 72.15 83.82 35.46 51.55
CodeHalu 38.56 55.66 22.76 36.84 73.10 82.88 33.11 49.01
PPL 36.41 53.39 22.22 21.43 72.29 81.67 40.90 37.11
NLI 49.25 52.38 17.68 30.05 77.92 62.82 31.70 48.15
CLM 36.41 53.39 22.22 21.42 71.27 64.42 37.71 51.49
SE 61.19 65.07 38.23 41.67 85.95 88.51 52.63 62.01
CR 60.52 68.14 44.44 49.23 89.47 89.47 47.99 56.00
SE+STDF 63.63 66.67 47.36 50.91 91.67 89.19 62.71 66.67
CR+STDF 72.00 69.92 73.33 53.85 91.67 91.70 61.40 66.14
MBPP
Execution 41.31 57.42 31.50 46.11 58.35 73.01 36.08 51.75
CodeHalu 40.48 57.08 30.21 45.32 57.33 72.60 32.70 48.60
PPL 37.16 51.11 39.28 34.55 71.24 55.47 38.46 34.33
NLI 39.40 49.88 30.50 39.61 67.95 58.29 33.13 36.98
CLM 36.32 53.28 31.60 44.25 56.60 72.28 35.10 50.00
SE 64.70 64.61 40.74 45.65 71.77 79.02 60.16 61.26
CR 61.99 66.28 40.00 45.58 67.24 65.67 62.99 62.50
SE+STDF 72.65 72.88 48.41 52.84 72.70 76.69 60.26 64.70
CR+STDF 66.43 66.48 48.94 47.44 79.40 79.69 69.23 63.07
MBPP→HumanEval
SE 60.27 62.11 32.65 41.50 76.03 78.63 60.00 58.99
CR 63.01 65.08 32.65 37.68 79.79 79.48 57.41 56.88
SE+STDF 71.11 70.00 39.39 50.00 80.28 77.27 68.42 59.65
CR+STDF 66.67 66.67 40.63 40.00 91.51 91.23 72.10 62.39
Table2: Performancecomparisonwhensignificantmoresamplesareusedforstaticmethods(N =256vs. N =64).
Staticmethodsfailtonarrowtheperformancegapevenwith4×samplebudget.
DeepSeek-Coder Qwen2.5-Coder WizardCoder
Method
P F1 P F1 P F1
PPL(N =256) 37.02 54.36 17.79 30.21 39.42 52.22
CLM(N =256) 36.41 53.39 20.32 32.89 36.29 51.64
CODEREFUSER(N =64) 72.00 69.92 73.33 53.85 61.40 66.14
4.2 EffectivenessResults
Forthescorefunctioncomputationinboththecalibrationandtestingphases,wegenerate64codesamplesand64test
casesforeachproblem. TheresultsontheHumanEvalandMBPPbenchmarksarepresentedinTable1,whicharethe
averageresultsofthreeindependentruns. Inthetable,‘SE’standsforCODEREFUSERwithsemanticentropy,‘CR’
standsforCODEREFUSERwithclusterratio,and‘SE+STDF’and‘CR+STDF’standfortheversionwhentheSTDF
mechanismisincluded.
(1)Thequalityofgeneratedtestsmatters. ThepoorperformanceofbothExecutionandCodeHaludemonstratesthat
LLM-generated tests cannot reliably replace oracle test suites. Execution fails to accurately estimate the pass rate
(H@k),whileCodeHalu’sperformancedegradessignificantlywhenforcedtotreatpotentiallyflawedgeneratedtests
as ground truth. These results confirm a critical quality gap, indicating that naive reliance on raw generated tests
withoutrigorousfiltering,isinsufficientforeffectiveabstention. Incontrast,whentheSTDFmechanismisintegrated,
CODEREFUSERconsistentlyyieldsthebestperformanceacrossbenchmarks. Comparedwiththebestexistingresults,
CODEREFUSER achieves an average of 26.5% and 11.9% absolute improvements w.r.t. abstention precision and
F1-score,respectively.
7
--- PAGE 8 ---
PREPRINT
DeepSeek-Coder-33B DeepSeek-Coder-33B DeepSeek-Coder-33B DeepSeek-Coder-33B
SE SE SE SE
CR CR CR CR
SE+STDF SE+STDF SE+STDF SE+STDF
CR+STDF CR+STDF CR+STDF CR+STDF
0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4
= 0.10 = 0.15 = 0.20 = 0.25
Qwen2.5-Coder-32B Qwen2.5-Coder-32B Qwen2.5-Coder-32B Qwen2.5-Coder-32B
SE SE SE SE
CR CR CR CR
SE+STDF SE+STDF SE+STDF SE+STDF
CR+STDF CR+STDF CR+STDF CR+STDF
0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4
= 0.10 = 0.15 = 0.20 = 0.25
Figure 2: Admission risk distribution on HumanEval under different risk tolerance α. The thickness of each plot
correspondstothedensityoftasksatthatrisklevel. Mostoftheadmissionrisksarecontrolledunderthegiventolerance
(thereddashedline).
(2)Staticscorefunctionsarelesseffectiveincodegenerationtasks. Amongthebaselines,PPL,CLM,andNLI are
staticmethodsproposedfornaturallanguagegeneration,withoutactuallyrunningthecode. Theexperimentalresult
showsthatthesemethodsconsistentlyunderperformcomparedtoourexecution-basedmethods(thefourbottomrows
inthetable). ThisconfirmsthattraditionalNLPmetricsfailtocapturethesemanticcorrectnessofcode,reinforcingthe
necessityofexecutionforreliableriskestimation.
Onemightarguethatexecution-basedapproachesinherentlyincurhighercomputationalcoststhanstaticbaselines. To
demonstrateitsnecessity,weconductedanexperimentwherewesignificantlyincreasedthesamplingbudgetforthe
staticbaselines. Specifically,weallowedPPLandCLMtogenerateN =256samples,whilekeepingCODEREFUSER
(CR+STDF)withtheoriginalN = 64samples. TheresultsaresummarizedinTable2,whereweuseHumanEval
andthreecodeLLMsforsimplicity. Theresultrevealsthatevenwithquadrupledsamples,theperformanceofstatic
methodsremainssignificantlylowerthanCODEREFUSER. Thisconfirmsthatthelimitationsofstaticmethodsstem
fromtheirinabilitytocapturesemanticcorrectness,afundamentaldeficitthatcannotbeovercomesimplybyscalingup
thesamplesize.
(3)CODEREFUSERtransferseffectivelyacrossdifferentdatasets. WealsoshowinTable1theresultswhenthecalibra-
tionisconductedonMBPPandthetestingisconductedonHumanEval. Despitethedistributionshift,CODEREFUSER
maintains robust performance, consistently outperforming baselines even when they are evaluated in-distribution
(comparedwithresultsof‘HumanEval’). Thisdemonstratesthatthecalibrationresultsof CODEREFUSER exhibit
transferabilityacrossdifferentdatasets.
4.3 RiskControlGuarantee
Wenextverifythetheoreticalriskcontrolguarantee. We
focusonthein-distributionsetting(calibratedandtestedon PPL CR
HumanEval)usingDeepSeek-CoderandQwen2.5-Coder. 0 1 . . 8 0 valid A A b ve st r e a n g t e io R n i s R k ate 0 0 0 . . . 6 7 8 A A b ve st r e a n g t e io R n i s R k ate valid
For each tolerance level α (with fixed δ = 0.1,k = 3), 0.6 0.5
0.4
we select the valid threshold λ ∈ Λ that yields the 0.4 0.3
valid 0.2 0.2
lowest abstention rate. Fig. 2 illustrates the distribution 0.1
0.0 0.0
oftheresultingadmissionrisks. Theresultsconfirmthat 1.0 1.2 Candi 1 d .4 ate Thre 1. s 6 holds 1.8 2.0 0.0 0.2 Candi 0 d .4 ate Thre 0. s 6 holds 0.8 1.0
theempiricalriskisreliablycontrolledbelowthetargetα. PPL CR
Similar results are observed in the transferability setting Figure3: Trade-offbetweenabstentionrateandadmis-
(calibratedonMBPPandtestedonHumanEval),asdetailed sionriskonMBPP(Qwen2.5-Coder-32B).Bothmethods
inAppendixE.1. Insummary,CODEREFUSERsuccessfully controlriskwithinthevalidrange(thicklines);PPLre-
meetsthetheoreticalguarantees.Itremainseffectiveinover quiresamuchhigherabstentionrate(80%vs.30%).
90%casesintermsofkeepingtheriskbelowthedesired
tolerancelevel(theareaontheleftsideoftheredtolerancelineaccountsformorethan90%ofthetotalarea).
Notethatonemethodmaysimplyrefusemostcodegenerationtaskstokeeptheadmissionrisklow. Here,wealso
analyzeΛ tounderstandthetrade-offbetweenadmissionriskandabstentionrate. Wesetthetoleranceα=0.2,
valid
8
--- PAGE 9 ---
PREPRINT
andcomparetheresultsofCODEREFUSERwithclusterratio4(i.e.,‘CR’)andPPL.TheresultsofQwen-Coder-32Bon
theMBPPdatasetareshowninFig.3. Itcanbeobservedthattheadmissionriskisundercontrolforbothmethods.
However,PPLmustrefusealargenumberoftasks(over80%)tomeettherisktolerance;incontrast,ourmethodonly
needstorefuse30%oftasks.
5 Conclusion
Inthispaper,weintroduceandstudythetaskabstentionproblemforLLM-basedcodegeneration,i.e.,determining
whetheragivenLLMshouldabstainfromperformingaspecificcodegenerationtasktoavoidpotentialhallucination.
Our approach features a calibrated abstention rule, grounded in the principles of multiple hypothesis testing. A
distinguishedadvantageisthatitprovidesarigorous,distribution-freetheoreticalguaranteeonitsabstentiondecisions,
whoseeffectivenessisalsoconfirmedbytheexperiments. Ourworkrepresentsprogressinthepursuitofprovably
correctLLMcodegeneration.
Limitations
Generalizationtoout-of-distributiontasks. Ourtheoreticalguaranteereliesontheassumptionthatthecalibrationand
testdataareindependentandidenticallydistributed. However,inreal-worldscenarios,theproblemasystemencounters
maydifferfromthoseitseesduringcalibration. Thispotentialdistributionshiftcouldintroducebiasandweakenthe
riskcontrolguaranteesinpractice. Tomitigatethisthreat,wehaveconductedexperimentsusingMBPPascalibration
dataandHumanEvalastestdata,andtheresultsshowthattherewasnosignificantdeclineinperformance.
Applicability to non-deterministic systems. The core of our approach–both the score functions and the STDF
mechanism—assumes that all tasks have deterministic solutions. The assumption may not hold for complex, in-
teractivesoftwaresystems,whichmayexhibitnondeterminism. Asourmethodreliesonclusteringidenticaloutputs,its
applicabilityiscurrentlylimitedtodeterministicproblemdomains.
Evaluationlimitedtoasingleprogramminglanguage. CurrentexperimentsareconductedinPython,alanguagewhere
modern LLMs have demonstrated strong performance HUANG et al. [2024], Twist et al. [2025]. However, many
real-worldsystemsarebuiltusingotherlanguagessuchasJavaorC,whichmayhavedifferentcharacteristics(e.g.,
pointerandmemorymanagementinC).Theeffectivenessofourmethodintheseprogramminglanguagesrequires
furtherevaluation.
References
YujiaLi,DavidChoi,JunyoungChung,NateKushman,JulianSchrittwieser,RémiLeblond,TomEccles,JamesKeeling,
FelixGimeno,AgustinDalLago,ThomasHubert,PeterChoy,CypriendeMassond’Autume,IgorBabuschkin,
XinyunChen,Po-SenHuang,JohannesWelbl,SvenGowal,AlexeyCherepanov,JamesMolloy,DanielJ.Mankowitz,
EsmeSutherlandRobson,PushmeetKohli,NandodeFreitas,KorayKavukcuoglu,andOriolVinyals. Competition-
level code generation with alphacode. Science, 378(6624):1092–1097, December 2022. ISSN 1095-9203. doi:
10.1126/science.abq1158. URLhttp://dx.doi.org/10.1126/science.abq1158.
MarkChen,JerryTworek,HeewooJun,QimingYuan,etal. EvaluatingLargeLanguageModelsTrainedonCode,July
2021.
BaptisteRoziere,JonasGehring,FabianGloeckle,StenSootla,ItaiGat,XiaoqingEllenTan,YossiAdi,JingyuLiu,
RomainSauvestre,TalRemez,etal.Codellama:Openfoundationmodelsforcode.arXivpreprintarXiv:2308.12950,
2023.
LeiHuang,WeijiangYu,WeitaoMa,WeihongZhong,ZhangyinFeng,HaotianWang,QianglongChen,WeihuaPeng,
XiaochengFeng,BingQin,andTingLiu. Asurveyonhallucinationinlargelanguagemodels: Principles,taxonomy,
challenges, and open questions. ACM Transactions on Information Systems, 43(2):1–55, January 2025a. ISSN
1558-2868. doi: 10.1145/3703155. URLhttp://dx.doi.org/10.1145/3703155.
YunseoLee,JohnYoungeunSong,DongsunKim,JindaeKim,MijungKim,andJaechangNam. Hallucinationbycode
generationllms: Taxonomy,benchmarks,mitigation,andchallenges. arXivpreprintarXiv:2504.20799,2025.
YuchenTian,WeixiangYan,QianYang,XuandongZhao,QianChen,WenWang,ZiyangLuo,LeiMa,andDawn
Song. Codehalu: Investigatingcodehallucinationsinllmsviaexecution-basedverification. InProceedingsofthe
AAAIConferenceonArtificialIntelligence,volume39,pages25300–25308,2025.
4Wechoose‘CR’inthisexperimentforinterpretation,asithasonlyoneparameter.
9
--- PAGE 10 ---
PREPRINT
AnastasiosNAngelopoulos,StephenBates,EmmanuelJCandès,MichaelIJordan,andLihuaLei. Learnthentest:
Calibratingpredictivealgorithmstoachieveriskcontrol. TheAnnalsofAppliedStatistics,19(2):1641–1662,2025.
VictorQuach,AdamFisch,TalSchuster,AdamYala,JaeHoSohn,TommiSJaakkola,andReginaBarzilay. Conformal
languagemodeling. InTheTwelfthInternationalConferenceonLearningRepresentations,2023.
PotsaweeManakul,AdianLiusie,andMarkGales. Selfcheckgpt: Zero-resourceblack-boxhallucinationdetectionfor
generativelargelanguagemodels. InThe2023ConferenceonEmpiricalMethodsinNaturalLanguageProcessing,
2023.
BeiChen,FengjiZhang,AnhNguyen,DaoguangZan,ZeqiLin,Jian-GuangLou,andWeizhuChen. Codet: Code
generationwithgeneratedtests,2022. URLhttps://arxiv.org/abs/2207.10397.
LorenzKuhn,YarinGal,andSebastianFarquhar.Semanticuncertainty:Linguisticinvariancesforuncertaintyestimation
innaturallanguagegeneration. InTheEleventhInternationalConferenceonLearningRepresentations,2023.
JacobAustin,AugustusOdena,MaxwellNye,MaartenBosma,HenrykMichalewski,DavidDohan,EllenJiang,Carrie
Cai,MichaelTerry,QuocLe,etal. Programsynthesiswithlargelanguagemodels. arXivpreprintarXiv:2108.07732,
2021.
YuhengHuang,JiayangSong,ZhijieWang,ShengmingZhao,HuamingChen,FelixJuefei-Xu,andLeiMa. Look
beforeyouleap: Anexploratorystudyofuncertaintyanalysisforlargelanguagemodels. IEEETransactionson
SoftwareEngineering,2025b.
DayaGuo,QihaoZhu,DejianYang,ZhendaXie,KaiDong,WentaoZhang,GuantingChen,XiaoBi,YuWu,YKLi,
etal. Deepseek-coder: Whenthelargelanguagemodelmeetsprogramming–theriseofcodeintelligence. arXiv
preprintarXiv:2401.14196,2024.
BinyuanHui,JianYang,ZeyuCui,JiaxiYang,DayihengLiu,LeiZhang,TianyuLiu,JiajunZhang,BowenYu,Keming
Lu,etal. Qwen2.5-codertechnicalreport. arXivpreprintarXiv:2409.12186,2024.
ZiyangLuo,CanXu,PuZhao,QingfengSun,XiuboGeng,WenxiangHu,ChongyangTao,JingMa,QingweiLin,and
DaxinJiang. Wizardcoder: Empoweringcodelargelanguagemodelswithevol-instruct. InTheTwelfthInternational
ConferenceonLearningRepresentations,2024. URLhttps://openreview.net/forum?id=UnUwSIgK5W.
DongHUANG,YuhaoQING,WeiyiShang,HemingCui,andJieZhang. Effibench: Benchmarkingtheefficiencyof
automaticallygeneratedcode. InTheThirty-eightConferenceonNeuralInformationProcessingSystemsDatasets
andBenchmarksTrack,2024. URLhttps://openreview.net/forum?id=30XanJanJP.
LukasTwist,JieMZhang,MarkHarman,DonSyme,JoostNoppen,andDetlefNauck. Llmslovepython: Astudyof
llms’biasforprogramminglanguagesandlibraries. arXivpreprintarXiv:2503.17181,2025.
Angela Fan, Beliz Gokkaya, Mark Harman, Mitya Lyubarskiy, Shubho Sengupta, Shin Yoo, and Jie M. Zhang.
Largelanguagemodelsforsoftwareengineering: Surveyandopenproblems. In2023IEEE/ACMInternational
Conference on Software Engineering: Future of Software Engineering (ICSE-FoSE), pages 31–53, 2023a. doi:
10.1109/ICSE-FoSE59343.2023.00008.
VibhorAgarwal,YulongPei,SalwaAlamir,andXiaomoLiu. Codemirage: Hallucinationsincodegeneratedbylarge
languagemodels. arXivpreprintarXiv:2408.08333,2024.
AryazEghbaliandMichaelPradel. De-hallucinator: Mitigatingllmhallucinationsincodegenerationtasksviaiterative
grounding. arXivpreprintarXiv:2401.01701,2024.
LakshyaAgrawal,AdityaKanade,NavinGoyal,ShuvenduKLahiri,andSriramRajamani.Monitor-guideddecodingof
codeLMswithstaticanalysisofrepositorycontext. InThirty-seventhConferenceonNeuralInformationProcessing
Systems,2023. URLhttps://openreview.net/forum?id=qPUbKxKvXq.
ZhiyuFan,XiangGao,MartinMirchev,AbhikRoychoudhury,andShinHweiTan. Automatedrepairofprograms
fromlargelanguagemodels. InProceedingsofthe45thInternationalConferenceonSoftwareEngineering,ICSE
’23, page1469–1481.IEEEPress, 2023b. ISBN9781665457019. doi: 10.1109/ICSE48619.2023.00128. URL
https://doi.org/10.1109/ICSE48619.2023.00128.
ZhijieWang,ZijieZhou,DaSong,YuhengHuang,ShengmaiChen,LeiMa,andTianyiZhang. Towardsunderstanding
thecharacteristicsofcodegenerationerrorsmadebylargelanguagemodels,2025. URLhttps://arxiv.org/abs/
2406.08731.
Fang Liu, Yang Liu, Lin Shi, Houkun Huang, Ruifeng Wang, Zhen Yang, Li Zhang, Zhongqi Li, and Yuchi Ma.
Exploringandevaluatinghallucinationsinllm-poweredcodegeneration. arXivpreprintarXiv:2404.00971,2024a.
ZiyaoZhang,ChongWang,YanlinWang,EnshengShi,YuchiMa,WanjunZhong,JiachiChen,MingzhiMao,and
ZibinZheng. Llmhallucinationsinpracticalcodegeneration: Phenomena,mechanism,andmitigation. Proc.ACM
Softw.Eng.,2(ISSTA),June2025. doi: 10.1145/3728894. URLhttps://doi.org/10.1145/3728894.
10
--- PAGE 11 ---
PREPRINT
Federico Cassano, John Gouwar, Daniel Nguyen, Sydney Nguyen, Luna Phipps-Costin, Donald Pinckney, Ming-
HoYee,YangtianZi,CarolynJaneAnderson,MollyQFeldman,ArjunGuha,MichaelGreenberg,andAbhinav
Jangda. Multipl-e: A scalable and polyglot approach to benchmarking neural code generation. IEEE Trans.
Softw. Eng., 49(7):3675–3691, July 2023. ISSN 0098-5589. doi: 10.1109/TSE.2023.3267446. URL https:
//doi.org/10.1109/TSE.2023.3267446.
Yue Liu, Thanh Le-Cong, Ratnadira Widyasari, Chakkrit Tantithamthavorn, Li Li, Xuan-Bach D. Le, and David
Lo. Refiningchatgpt-generatedcode: Characterizingandmitigatingcodequalityissues. ACMTrans.Softw.Eng.
Methodol., 33(5), June 2024b. ISSN 1049-331X. doi: 10.1145/3643674. URL https://doi.org/10.1145/
3643674.
ShubhamUgare,TarunSuresh,HangooKang,SasaMisailovic,andGagandeepSingh. Syncode: LLMgeneration
withgrammaraugmentation. TransactionsonMachineLearningResearch,2025. ISSN2835-8856. URLhttps:
//openreview.net/forum?id=HiUZtgAPoH.
Fangwen Mu, Lin Shi, Song Wang, Zhuohao Yu, Binquan Zhang, ChenXue Wang, Shichao Liu, and Qing Wang.
Clarifygpt: Aframeworkforenhancingllm-basedcodegenerationviarequirementsclarification. Proc.ACMSoftw.
Eng.,1(FSE),July2024. doi: 10.1145/3660810. URLhttps://doi.org/10.1145/3660810.
Bingbing Wen, Jihan Yao, Shangbin Feng, Chenjun Xu, Yulia Tsvetkov, Bill Howe, and Lucy Lu Wang. Know
yourlimits: Asurveyofabstentioninlargelanguagemodels. TransactionsoftheAssociationforComputational
Linguistics,13:529–556,2025. doi: 10.1162/tacl_a_00754. URLhttps://aclanthology.org/2025.tacl-1.26/.
NeerajVarshney,PavelDolin,AgastyaSeth,andChittaBaral.Theartofdefending:Asystematicevaluationandanalysis
ofLLMdefensestrategiesonsafetyandover-defensiveness. InLun-WeiKu,AndreMartins,andVivekSrikumar,
editors, Findings of the Association for Computational Linguistics: ACL 2024, pages 13111–13128, Bangkok,
Thailand,August2024.AssociationforComputationalLinguistics. doi: 10.18653/v1/2024.findings-acl.776. URL
https://aclanthology.org/2024.findings-acl.776/.
YuxiaWang,HaonanLi,XudongHan,PreslavNakov,andTimothyBaldwin. Do-not-answer: Evaluatingsafeguardsin
LLMs. InYvetteGrahamandMatthewPurver,editors,FindingsoftheAssociationforComputationalLinguistics:
EACL2024, pages896–911, St.Julian’s, Malta, March2024.AssociationforComputationalLinguistics. URL
https://aclanthology.org/2024.findings-eacl.61/.
Hanning Zhang, Shizhe Diao, Yong Lin, Yi Fung, Qing Lian, Xingyao Wang, Yangyi Chen, Heng Ji, and Tong
Zhang. R-tuning: Instructing large language models to say ‘I don’t know’. In Kevin Duh, Helena Gomez, and
StevenBethard,editors,Proceedingsofthe2024ConferenceoftheNorthAmericanChapteroftheAssociationfor
ComputationalLinguistics: HumanLanguageTechnologies(Volume1: LongPapers),pages7113–7139,Mexico
City,Mexico,June2024.AssociationforComputationalLinguistics. doi: 10.18653/v1/2024.naacl-long.394. URL
https://aclanthology.org/2024.naacl-long.394/.
GustafAhdritz,TianQin,NikhilVyas,BoazBarak,andBenjaminL.Edelman. Distinguishingtheknowablefromthe
unknowablewithlanguagemodels. ICML’24.JMLR.org,2024.
MinsuKimandJamesThorne. Epistemologyoflanguagemodels: Dolanguagemodelshaveholisticknowledge? In
Lun-WeiKu,AndreMartins,andVivekSrikumar,editors,FindingsoftheAssociationforComputationalLinguistics:
ACL2024,pages12644–12669,Bangkok,Thailand,August2024.AssociationforComputationalLinguistics. doi:
10.18653/v1/2024.findings-acl.751. URLhttps://aclanthology.org/2024.findings-acl.751/.
LangCao. Learntorefuse: Makinglargelanguagemodelsmorecontrollableandreliablethroughknowledgescope
limitationandrefusalmechanism. InYaserAl-Onaizan,MohitBansal,andYun-NungChen,editors,Proceedingsof
the2024ConferenceonEmpiricalMethodsinNaturalLanguageProcessing,pages3628–3646,Miami,Florida,
USA,November2024.AssociationforComputationalLinguistics. doi: 10.18653/v1/2024.emnlp-main.212. URL
https://aclanthology.org/2024.emnlp-main.212/.
EllaNeeman,RoeeAharoni,OrHonovich,LeshemChoshen,IdanSzpektor,andOmriAbend.DisentQA:Disentangling
parametricandcontextualknowledgewithcounterfactualquestionanswering. InAnnaRogers,JordanBoyd-Graber,
andNaoakiOkazaki,editors,Proceedingsofthe61stAnnualMeetingoftheAssociationforComputationalLin-
guistics(Volume1: LongPapers),pages10056–10070,Toronto,Canada,July2023.AssociationforComputational
Linguistics. doi: 10.18653/v1/2023.acl-long.559. URLhttps://aclanthology.org/2023.acl-long.559/.
YuqingYang,EthanChern,XipengQiu,GrahamNeubig,andPengfeiLiu. Alignmentforhonesty. InTheThirty-eighth
AnnualConferenceonNeuralInformationProcessingSystems,2024. URLhttps://openreview.net/forum?id=
67K3Xlvw8L.
StephanieLin,JacobHilton,andOwainEvans. Teachingmodelstoexpresstheiruncertaintyinwords. Transactionson
MachineLearningResearch,2022. ISSN2835-8856. URLhttps://openreview.net/forum?id=8s8K2UZGTZ.
11
--- PAGE 12 ---
PREPRINT
KatherineTian,EricMitchell,AllanZhou,ArchitSharma,RafaelRafailov,HuaxiuYao,ChelseaFinn,andChristo-
pherDManning. Justaskforcalibration: Strategiesforelicitingcalibratedconfidencescoresfromlanguagemodels
fine-tunedwithhumanfeedback. InThe2023ConferenceonEmpiricalMethodsinNaturalLanguageProcessing,
2023.
VaishnaviShrivastava,PercyLiang,andAnanyaKumar. LlamasknowwhatGPTsdon’tshow: Surrogatemodelsfor
selectiveclassification,2024. URLhttps://openreview.net/forum?id=D8DAQhpznu.
ShangbinFeng,WeijiaShi,YikeWang,WenxuanDing,VidhishaBalachandran,andYuliaTsvetkov. Don’thallucinate,
abstain: IdentifyingLLMknowledgegapsviamulti-LLMcollaboration. InLun-WeiKu,AndreMartins,andVivek
Srikumar,editors,Proceedingsofthe62ndAnnualMeetingoftheAssociationforComputationalLinguistics(Volume
1: LongPapers),pages14664–14690,Bangkok,Thailand,August2024.AssociationforComputationalLinguistics.
doi: 10.18653/v1/2024.acl-long.786. URLhttps://aclanthology.org/2024.acl-long.786/.
BochengChen,AdvaitPaliwal,andQibenYan. Jailbreakerinjail: Movingtargetdefenseforlargelanguagemodels.
In Proceedings of the 10th ACM Workshop on Moving Target Defense, MTD ’23, page 29–32, New York, NY,
USA,2023.AssociationforComputingMachinery. ISBN9798400702563. doi: 10.1145/3605760.3623764. URL
https://doi.org/10.1145/3605760.3623764.
Ryan J. Tibshirani, Rina Foygel Barber, Emmanuel J. Candès, and Aaditya Ramdas. Conformal prediction under
covariateshift. CurranAssociatesInc.,RedHook,NY,USA,2019.
RinaFoygelBarber,EmmanuelJ.Candès,AadityaRamdas,andRyanJ.Tibshirani. Conformalpredictionbeyond
exchangeability. The Annals of Statistics, 51(2):816 – 845, 2023. doi: 10.1214/23-AOS2276. URL https:
//doi.org/10.1214/23-AOS2276.
Isaac Gibbs and Emmanuel Candes. Adaptive conformal inference under distribution shift. In A. Beygelzimer,
Y.Dauphin,P.Liang,andJ.WortmanVaughan,editors,AdvancesinNeuralInformationProcessingSystems,2021.
URLhttps://openreview.net/forum?id=6vaActvpcp3.
AnastasiosNikolasAngelopoulos,StephenBates,AdamFisch,LihuaLei,andTalSchuster. Conformalriskcontrol. In
TheTwelfthInternationalConferenceonLearningRepresentations,ICLR2024,Vienna,Austria,May7-11,2024.
OpenReview.net,2024. URLhttps://openreview.net/forum?id=33XGfHLtZg.
JiahuiGeng,FengyuCai,YuxiaWang,HeinzKoeppl,PreslavNakov,andIrynaGurevych. Asurveyofconfidence
estimationandcalibrationinlargelanguagemodels. InProceedingsofthe2024ConferenceoftheNorthAmerican
ChapteroftheAssociationforComputationalLinguistics: HumanLanguageTechnologies(Volume1: LongPapers),
pages6577–6595,2024.
ChujieZheng,HaoZhou,FandongMeng,JieZhou,andMinlieHuang. Largelanguagemodelsarenotrobustmultiple
choiceselectors. InTheTwelfthInternationalConferenceonLearningRepresentations,2024.
SébastienBubeck,VarunChandrasekaran,RonenEldan,JohannesGehrke,EricHorvitz,EceKamar,PeterLee,YinTat
Lee,YuanzhiLi,ScottLundberg,etal. Sparksofartificialgeneralintelligence: EarlyexperimentswithGPT-4. arXiv
preprintarXiv:2303.12712,2023.
JinhaoDuan,HaoCheng,ShiqiWang,AlexZavalny,ChenanWang,RenjingXu,BhavyaKailkhura,andKaidiXu.
Shiftingattentiontorelevance: Towardsthepredictiveuncertaintyquantificationoffree-formlargelanguagemodels.
In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
Papers),pages5050–5063,2024.
StanleyFChen,DouglasBeeferman,andRoniRosenfeld. Evaluationmetricsforlanguagemodels. 1998.
David M. Blei, Andrew Y. Ng, and Michael I. Jordan. Latent dirichlet allocation. Journal of Machine Learning
Research,3(1):993–1022,2003.
SauravKadavath,TomConerly,AmandaAskell,TomHenighan,DawnDrain,EthanPerez,NicholasSchiefer,Zac
Hatfield-Dodds,NovaDasSarma,EliTran-Johnson,etal. Languagemodels(mostly)knowwhattheyknow. arXiv
preprintarXiv:2207.05221,2022.
Miao Xiong, Zhiyuan Hu, Xinyang Lu, YIFEI LI, Jie Fu, Junxian He, and Bryan Hooi. Can llms express their
uncertainty? anempiricalevaluationofconfidenceelicitationinllms. InTheTwelfthInternationalConferenceon
LearningRepresentations,2024.
YasinAbbasiYadkori,IljaKuzborskij,AndrásGyörgy,andCsabaSzepesvari. Tobelieveornottobelieveyourllm:
Iterativepromptingforestimatingepistemicuncertainty. AdvancesinNeuralInformationProcessingSystems,37:
58077–58117,2024.
EvanBeckerandStefanoSoatto. Cyclesofthought: MeasuringLLMconfidencethroughstableexplanations. arXiv
preprintarXiv:2406.03441,2024.
12
--- PAGE 13 ---
PREPRINT
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H Chi, Sharan Narang, Aakanksha Chowdhery, and
DennyZhou. Self-consistencyimproveschainofthoughtreasoninginlanguagemodels. InProceedingsofthe11th
InternationalConferenceonLearningRepresentations,2022.
XinyunChen,RenatAksitov,UriAlon,JieRen,KefanXiao,PengchengYin,SushantPrakash,CharlesSutton,Xuezhi
Wang,andDennyZhou.Universalself-consistencyforlargelanguagemodels.InICML2024WorkshoponIn-Context
Learning,2024.
FuruiCheng,VilémZouhar,SimranArora,MrinmayaSachan,HendrikStrobelt,andMennatallahEl-Assady. Relic:
Investigating large language model responses using self-consistency. In Proceedings of the CHIConference on
HumanFactorsinComputingSystems,pages1–18,2024.
A RelatedWork
CodeHallucination. Thephenomenonofcodehallucination,whereLLMsgeneratecodethatisillogical,incorrect,or
unfaithfultouserrequirementsFanetal.[2023a],presentsachallengetoensuretheaccuracy,reliabilityandsecurityof
AI-generatedcodeAgarwaletal.[2024],EghbaliandPradel[2024],Tianetal.[2025]. Existingresearchhasexplored
codehallucinationfromseveralangles,oftencategorizingfailuresbasedonwhentheyoccur. Thesecategoriesprimarily
includesyntactichallucination,whichareerrorsthatviolatetheprogramminglanguage’ssyntaxandpreventcodefrom
beingcompiledorinterpretedAgrawaletal.[2023],Fanetal.[2023b],Wangetal.[2025]; runtimehallucination,
wherethecodeissyntacticallyvalidbutproduceserrorssuchasexceptionsorcrashesFanetal.[2023b],Liuetal.
[2024a],Tianetal.[2025],Zhangetal.[2025],andfunctionalhallucination,wherecodethatrunswithouterrorfailsto
meettheprogram’sintendedrequirementsFanetal.[2023b],Liuetal.[2024a],Wangetal.[2025],Zhangetal.[2025],
amongothers.
To facilitate a more rigorous evaluation of hallucination in LLM-based code generation, a number of benchmarks
havebeendeveloped. NotableexamplesincludeCodeHaluEvalTianetal.[2025],CodeMirageAgarwaletal.[2024],
MultiPL-ECassanoetal.[2023],HalluCodeLiuetal.[2024a],etc. Priorworkhasalsoproposedvariousstrategiesto
mitigatecodehallucination. TheDe-hallucinatorEghbaliandPradel[2024]pre-indexesaproject’scodebaseanduses
Retrieval-AugmentedGeneration(RAG)toinjectrelevantAPIsintoprompts;Liuetal.Liuetal.[2024b]leverage
the LLM’s self-revision capabilities by providing it with feedback based on static analysis; SynCode Ugare et al.
[2025]usesaformalgrammarrepresentation(EBNF)toguidethemodel’sdecodingandensuresyntacticvalidity;
ClarifyGPTMuetal.[2024]introducedaframeworkwheretheLLMproactivelyasksclarifyingquestionstohelpusers
refinetheirinitialprompts. Differentfromtheaboveworkthatfocusesonthesample-levelhallucinationproblem,we
studythetaskabstentionproblem.
LLMAbstention. Abstentionisincreasinglyrecognizedforitspotentialtomitigatehallucinationandenhancesafety
inLLMsystemsWenetal.[2025],Varshneyetal.[2024],Wangetal.[2024],Zhangetal.[2024]. Aguidingprinciple
isthatasystemshouldabstainwhenitisinsufficientlyconfidentinthecorrectnessofitsoutputorifthereisahigh
probabilityoferrorAhdritzetal.[2024],KimandThorne[2024],Cao[2024]. Existingworkhasproposedvarious
strategiestodeterminewhentheLLMshouldabstain,targetingdifferentstagesofthemodellifecycle.
During the training and alignment phase, Neeman et al. Neeman et al. [2023] use data augmentation to fine-tune
modelstorecognizeunanswerablequestions. Yangetal.Yangetal.[2024]construct“honesty”alignmentdatasetsby
substitutingamodel’sincorrectresponsewith“Idon’tknow”andthenfine-tuningonthisreviseddata. Atinference
time,acommonapproachistousepost-processingtechniquesbasedonmodeluncertainty. Theseincludecalculating
thelogprobabilityofa‘True’tokenviaindirectlogitmethodsLinetal.[2022],Tianetal.[2023],usingasurrogate
LLMtoapproximatetheconfidenceofablack-boxmodelShrivastavaetal.[2024],orassessingthesemanticentropy
ofresponsesKuhnetal.[2023]. Adifferentinference-timestrategyinvolvesLLMcollaboration,whereasecond“test”
LLMisemployedtoexaminetheoutputofthefirst,helpingidentifyharmfulqueriesorcorrecttheinitialresponse
beforeitisshowntotheusersFengetal.[2024],Chenetal.[2023]. Theexistingmethodsaremainlyproposedforthe
naturallanguagegenerationproblem. Inthiswork,wearguethattestcodegenerationandexecutionareessentialfor
thecodegenerationtaskabstentionproblem.
ConformalRiskControl. ApproachesbasedonConformalPrediction(CP)areknownfortheirabilitytoselecta
guaranteedthresholdbyanalyzingtheGuantiledistributionofrisktermonacalibrationsetTibshiranietal.[2019],
Barberetal.[2023],GibbsandCandes[2021]. However,standardCPmethodsareoftenconstrainedtooperatingona
singlecandidatethresholdatatime. Theyarenotequippedtohandleavectorofthresholdsderivedsimultaneously
frommultiplescorefunctions,whichlimitstheirapplicabilityinscenariosrequiringmultifacetedevaluation.
Arelatedframework,ConformalRiskControl(CRC),alsoefficientlyutilizescalibrationsetstomanagetheprediction
riskAngelopoulosetal.[2024]. Itsprimarylimitation,however,istherequirementofamonotonicrelationshipbetween
13
--- PAGE 14 ---
PREPRINT
the risk function and the threshold. This monotonicity assumption frequently does not hold for the intricate score
functionsusedincomplexgenerativetasks,posingasignificantchallengetoadaptingCRCtoourdomain.
Confidence Estimation for LLMs. Confidence estimation for LLMs aims to provide a measure of predictive
uncertaintyforLLMoutputs. Well-calibratedconfidencecanfurthercontributetomigratingthebiasandalleviating
thehallucinationGengetal.[2024],Zhengetal.[2024],Bubecketal.[2023]. RecentresearchonLLMconfidence
estimationbroadlyfallsintothefollowingveins. PerplexityconfidenceHuangetal.[2025b],Duanetal.[2024]derives
confidencefromtheprobabilitiesassignedtogeneratedtokens,employingthegeometricmean(i.e.,perplexityChen
etal.[1998],Bleietal.[2003])tomitigatesensitivitytooutputlength;verbalizedconfidenceKadavathetal.[2022],
Xiongetal.[2024],Tianetal.[2023]directlypromptstheLLMtoexplicitlyexpressitsconfidencealongsideitsanswer
(e.g.,“Readthequestionandgiveyouranswerandcorrespondingconfidencescore”);self-consistencyconfidenceXiong
etal.[2024],AbbasiYadkorietal.[2024],BeckerandSoatto[2024]assessesconfidencebyhavingtheLLMgenerate
multipleanswersforthesameinputandthenmeasuringtheconsistencyamongthemWangetal.[2022],Chenetal.
[2024],Chengetal.[2024],withhigherconsistencyindicatinggreaterconfidence.
B TheLTTFramework
TheLearnThenTest(LTT)frameworkAngelopoulosetal.[2025]isdesignedtoprovidestatisticalguaranteesfor
machinelearningmodelsbysimplyaddingapost-processingsteponacalibrationsetafterthemodelistrained.Consider
thetaskwhereeachinstancex∈X isassociatedwithaground-truthlabely ∈Y. LetD ={(x ,y )}m ⊆X ×Y
cal i i i=1
be a calibration set composed of the input x and its ground-truth label y, which are independently and identically
distributed(i.i.d.) drawn. Apost-processingfunctionT :X →Y′withparameterλisdesignedtomapX toanyspace
λ
Y′. (Forinstance,inclassificationY′maybedefinedas2Y,i.e.,allpossiblesubsetsofY.) Inotherwords,insteadof
predictingalabelforeachinstance,LTTaimstopredictasubsetoflabelssothatthetruelabeliswithinthesubsetwith
ahighprobability. Thechoiceofthesubsetsisdecidedbyλ(e.g.,labelswithpredictiveprobabilitygreaterthanλare
includedinthesubset).
Basedonthepost-processingfunctionT ,ariskR(T (x))∈Ronagivenxcanbedefinedtomeasurethetask-specific
λ λ
statistical error (e.g., the miscoverage rate of true labels in Y′ for the classification task). Since the risk is mainly
decidedbyparameterλ,werewriteR(T (x))asR(x;λ)forbrevity.
λ
ThegoalofLTTistoensuretheguaranteeasstatedinEq. (2). Usingtheclassificationtaskasanexample,intuitively
Eq.(2)assertsthattheriskofawrongclassification(e.g.,thetruelabelisnotintheoutputsubset)isbelowthethreshold
αwithprobabilityatmostδ.
ThecoreofLTTistoobtainthesetΛ . Forthispurpose,wecantraversealltheplausible{T } andestimate
valid λ λ∈Λ
their risk on the calibration set D using multiple hypothesis testing. Specifically, for each λ in a discrete set
cal j
Λ = {λ ,··· ,λ }, we have a null hypothesis H : R(λ ) > α and H is rejected when λ controls the risk,
1 N j j j j
i.e., λ ∈ Λ . For each null hypothesis, we can compute a finite-sample valid p-value using a concentration
j valid
inequalityAngelopoulosetal.[2025]. Λ canthenbecalculatedbyapplyinganyfamily-wiseerrorrate(FWER)-
valid
controllingalgorithm,whichreceivesthesetofp-valuesandreturnsthesetofλthatweshouldrejecttheassociated
null hypothesis. For example, the Bonferroni correction is a typical FWER-controlling algorithm which yields
(cid:110) (cid:111)
Λ = λ :p ≤ δ .
valid j j |Λ|
OnceΛ isobtainedonthecalibrationset,LTTensuresthatthefollowingtheoremholdsforani.i.d. testsample
valid
x .
test
Theorem1(LearnThenTestAngelopoulosetal.[2025]). Supposep issuper-uniformforallj underH ,andassume
j j
avalidFWER-controllingalgorithmatlevelδ. ThenEq.(2)holdsforthetestsamplex .
test
Key insight of applying LTT. The key insights of using LTT in our task abstention problem for LLM-based code
generationareasfollows. LTTwasoriginallyproposedtogenerateasetofresponses,insteadofasingleresponse,so
thatthetrueresponseiswithintheresponsesetwithaguaranteedprobability. Incodegeneration,theLLMcanrefuse
thecodegenerationtaskiftheresponsesetisemptyafterafewattempts. Meanwhile,thestatisticalguaranteefrom
LTTstillstands.
C ScoreFunctionDefinitions
InSection3.3,weintroducedtwoscorefunctionsbasedonexecution-basedclustering. Here,weprovidetheirformal
definitions. LetY ={y ,...,y }bethegeneratedcodesamplesandC ={C ,...,C }bethepartitionofY derived
1 n 1 h
fromexecutionresultsontestcasesT.
14
--- PAGE 15 ---
PREPRINT
DeepSeek-Coder-33B DeepSeek-Coder-33B DeepSeek-Coder-33B DeepSeek-Coder-33B
SE SE SE SE
CR CR CR CR
SE+STDF SE+STDF SE+STDF SE+STDF
CR+STDF CR+STDF CR+STDF CR+STDF
0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4
= 0.10 = 0.15 = 0.20 = 0.25
Qwen2.5-Coder-32B Qwen2.5-Coder-32B Qwen2.5-Coder-32B Qwen2.5-Coder-32B
SE SE SE SE
CR CR CR CR
SE+STDF SE+STDF SE+STDF SE+STDF
CR+STDF CR+STDF CR+STDF CR+STDF
0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4 0.0 0.1 0.2 0.3 0.4
= 0.10 = 0.15 = 0.20 = 0.25
Figure4: AdmissionriskdistributiononHumanEvalunderdifferentrisktoleranceα,whentheLLMiscalibratedon
MBPP.Mostoftheadmissionrisksarestillunderthegiventolerance.
C.1 Confidence-basedScoreFunction
TheconsistencyfunctionI(y ,y ;C)betweentwocodesamplesisdefinedas:
1 2
(cid:26)
1, ∃C ∈C,{y ,y }⊆C
I(y ,y ;C)= j 1 2 j (6)
1 2 0, otherwise
Theconfidencescoreforasampley ∈Y istheaverageconsistencywithallothersamples:
n
1 (cid:88)
Conf(y)= I(y,y ;C). (7)
n i
i=1
A high confidence score indicates that the sample belongs to a dominant semantic cluster, reflecting the model’s
convictioninthatspecificlogicChenetal.[2022].
C.2 SemanticEntropy-basedScoreFunction
Semanticentropymeasuresthediversityofthesemanticclusters. Forataskx,itisdefinedas:
(cid:88)
SE(x)=− p(C |x)logp(C |x)
i i
Ci∈C
(8)
(cid:88)
≈−|C|−1 logp(C |x).
i
Ci∈C
Ahigherentropyvaluesignifiesgreaterinconsistencyamongthegeneratedsolutions,suggestingahigherlikelihoodof
task-levelhallucinationKuhnetal.[2023].
D ImplementationDetailsofSTDF
Inthissection,weprovidetheformalprocedurefortheSample-TestDualFiltering(STDF)mechanism,asoutlinedin
Algorithm2.
Thealgorithmrequiresthreecalibratedthresholds: λ (maximumerrorratetolerance),λ (maximumpruningratio),
1 2
andλ (maximumentropytolerance). Theprocessconsistsoftwophases:
3
Phase1: ErrorRatePruning(Lines4–6). Wefirstcalculatetheerrorrateforeachtestcasetacrossallgenerated
codesamplesY. Iftheproportionofsamplesthatcrashorfailontexceedsλ ,thetestcaseisimmediatelydiscarded.
1
Thisstepeffectivelyremoves"toxic"inputsthatcausewidespreadcrashes.
Phase2: Diversity-basedPruning(Lines8–16). Forthesurvivingtestcases,wecomputethesemanticentropy(SE)
oftheirexecutionoutputs. AhighSEimpliesthatthecodesamplesproduceawidevarietyofinconsistentoutputs
forthisspecificinput,suggestingthetestcaseisambiguousorinvalid. However,highvariancemightalsostemfrom
themodel’sownuncertaintyratherthanthetest’sflaw. Toavoidaggressivelydiscardingvalidtests(whichwould
artificiallyinflatetheconsensusscore),weimposeasafetylimit: wesortthetestcasesbytheirentropyandremoveat
most⌊λ ·|T|⌋testcases,andonlyiftheirentropyexceedsλ .
2 3
15
--- PAGE 16 ---
PREPRINT
Algorithm2Sample-TestDualFilteringMechanism
Input: GeneratedcodesamplesY;generatedtestcasesT;thresholdsλλλ=[λ ,λ ,λ ]
1 2 3
Output: TherefinedtestcasesT′
1: procedureSTDF(Y,T,λλλ)
2: res←Exec(Y,T)
3: FilterSet←∅
4: foreachtestcaset∈T do
5: ifErrorRate(res[t])>λ 1 then
6: ErasetfromT
7: else
8: C t ←ClusteringY byres[t]
9: add{t,SE(C t )}toFilterSet
10: endif
11: endfor
12: sortFilterSetindescendingorderofSE
13: max num ←⌊λ 2 ·|T|⌋
14: fort,SE t intopmax num elementsofFilterSetdo
15: ifSE t >λ 3 then
16: ErasetfromT
17: endif
18: endfor
19: returnT
20: endprocedure
E AdditionalExperimentalAnalysis
Inthissection,weprovidefurtheranalysistovalidatetherobustnessandefficiencyofCODEREFUSER. Specifically,we
investigate: (1)thetransferabilityofourmethodunderdistributionshifts(i.e.,cross-datasetevaluation);and(2)the
sensitivityofourapproachtodifferentriskdefinitions(i.e.,varyingk).
E.1 TransferabilityAnalysis
Toassessthegeneralizationcapabilityof CODEREFUSER toout-of-distributiontasks,wefurtherexaminewhether
thetheoreticalriskcontrolholdsunderdistributionshifts. Figure4illustratesthedistributionofadmissionriskson
HumanEvalusingthresholdscalibratedonMBPP.
Althoughtherigoroustheoreticalguaranteereliesonthei.i.d. assumption,empiricalresultsshowthattheadmission
riskremainslargelycontrolledbelowthetargettoleranceα. ThisindicatesthatCODEREFUSERispracticallyrobustto
moderatedistributionshifts.
E.2 SensitivitytoRiskDefinition(k =5)
Inthemainexperiments,wedefinedtheriskbasedonthepassrateH@kwithk = 3. Toevaluatethesensitivityof
CODEREFUSERtothishyperparameter,weconductedadditionalexperimentssettingk =5. Thisadjustmentimpliesa
slightlymorerelaxedcriterionforsuccess,effectivelyallowingthemodelmoreattemptstoyieldacorrectsolution.
We re-calibrated and evaluated CODEREFUSER under this new setting. As shown in Table 3, the results exhibit
negligible variance compared to the k = 3 case. CODEREFUSER continues to robustly identify and abstain from
unsolvable tasks, maintaining its performance advantage over other methods. This consistency confirms that the
effectivenessofCODEREFUSERisnotdependentonaspecificchoiceofk,demonstratingitsrobustnesstodifferent
riskdefinitions.
16
--- PAGE 17 ---
PREPRINT
Table 3: Task abstention results on HumanEval and MBPP with k = 5. Our approaches (i.e., ‘SE+STDF’ and
‘CR+STDF’)generallyoutperformthecompetitors.
Model DeepSeek-Coder Qwen2.5-Coder WizardCoder
Method P F1 P F1 P F1
HumanEval
PPL 36.41 53.39 17.79 30.20 39.42 52.23
CLM 36.97 53.67 20.32 32.89 37.71 51.49
CodeHalu 28.68 42.68 16.09 26.16 27.27 41.25
SE 60.27 66.66 28.57 41.51 52.43 63.70
CR 59.49 68.11 41.02 47.06 51.19 62.77
SE+STDF 56.71 64.95 46.66 50.91 53.33 62.50
CR+STDF 68.75 71.54 70.33 53.90 60.00 61.11
MBPP
PPL 36.32 53.28 26.15 41.04 31.75 47.45
CLM 36.32 53.28 31.60 44.25 35.10 50.00
CodeHalu 33.43 48.63 28.12 41.02 32.74 47.32
SE 51.12 64.60 34.80 45.65 50.00 61.26
CR 59.18 66.28 31.95 45.57 60.99 63.70
SE+STDF 66.13 72.88 46.76 52.84 60.26 64.99
CR+STDF 59.39 66.47 47.22 47.44 62.59 63.08
17