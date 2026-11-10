---
title: '[2404.10100] TiCoder LLM-based test-driven interactive code generation (full
  text)'
id: 240410100-ticoder-llm-based-test-driven-interactive-code-generation-full-text
tags:
- code-llm-confidence-positioning-d82d00
- related
created: '2026-11-09T23:11:31.939727Z'
updated: '2026-11-09T23:27:44.739788Z'
source: https://arxiv.org/pdf/2404.10100
status: review
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'FULL TEXT. TiCoder (Fakhoury et al.): test-driven clarification, +45.97%
  absolute pass@1 within 5 simulated interactions on MBPP and HumanEval, 15-person
  user study. Related to L4 test adequacy.'
---

1
 LLM-based Test-driven Interactive Code
 Generation: User Study and Empirical Evaluation
 Sarah Fakhoury∗ , Aaditya Naik† , Georgios Sakkas‡ , Saikat Chakraborty∗ and Shuvendu K. Lahiri∗
 ∗ Microsoft Research
 {sfakhoury, saikatc, shuvendu}@microsoft.com
 † University of Pennsylvania
 asnaik@seas.upenn.edu
 † University of California, San Diego
 gsakkas@eng.ucsd.edu
arXiv:2404.10100v2 [cs.SE] 2 Oct 2024
 Abstract—Large language models (LLMs) have shown great
 potential in automating significant aspects of coding by produc- 1 def text_lowercase_underscore(text):
 2 """Write a function that returns true if the
 ing natural code from informal natural language (NL) intent. input string contains sequences of lowercase
 However, given NL is informal, it does not lend easily to checking letters joined with an underscore and false
 that the generated code correctly satisfies the user intent. otherwise""
 In this paper, we propose a novel interactive workflow
 T I C ODER for guided intent clarification (i.e., partial formaliza-
 tion) through tests to support the generation of more accu- While the intent may seem obvious at first, it is not
 rate code suggestions. Through a mixed methods user study immediately clear how to check the correctness of a potential
 with 15 programmers, we present an empirical evaluation of solution. Querying an LLM such as text-davinci-003 [11]
 the effectiveness of the workflow to improve code generation yields several plausibly correct code implementations that pass
 accuracy. We find that participants using the proposed workflow simple tests such as rejecting the empty string “ ”, or accepting
 are significantly more likely to correctly evaluate AI generated
 code, and report significantly less task-induced cognitive load. the string "aa_bb". However, it may also produce subtly
 Furthermore, we test the potential of the workflow at scale with buggy code solutions that accept strings such as "aa_bb_cc",
 four different state-of-the-art LLMs on two python datasets, which is inconsistent with the original user intent that expects
 using an idealized proxy for a user feedback. We observe an the string to consist entirely of two sequences of lowercase
 average absolute improvement of 45.97% in the pass@1 code letters joined by an underscore (as defined by the accompa-
 generation accuracy for both datasets and across all LLMs within
 5 user interactions, in addition to the automatic generation of nying hidden reference solution and the validation tests from
 accompanying unit tests. MBPP). In practice, this can often lead to users accepting code
 with subtle bugs while using LLMs [12], [13]. The apparent
 Index Terms—Intent Disambiguation, Code Generation,
 LLMs, Human Factors, Cognitive Load, Test Generation. ambiguity in this particular docstring, and more importantly
 the informal nature of natural language, highlights the inability
 I. I NTRODUCTION to immediately ascertain the correctness of the code generated
 by an LLM. Instead, it would be desirable to avoid surfacing
 L ARGE Language Models (LLMs) have shown tremen-
 dous potential in generating natural-looking programs
 from informal intent expressed in natural language. There has
 such subtly incorrect codes by first clarifying, and partially
 formalizing, the user intent into a checkable specification.
 This issue can be compounded when users are presented
 been a surge in research around training LLMs over program-
 with a list of candidate suggestions from LLMs, such as
 ming language artifacts in just the last couple of years [1], [2],
 in the Copilot VSCode IDE suggestions pane, which can
 [3], [4], [5]. Commercial offerings such as GitHub Copilot [6]
 display up to 10 suggestions. Users often have to linearly
 are widely available, and have been shown to generate a non-
 scan the list of code suggestions, review them, and reject
 trivial fraction of code in real-world scenarios [7].
 However, there are several challenges that arise when gen- the incorrect ones until arriving at one that satisfies their
 erating code from natural language specifications.[8], [9]. For intent. In such situations, subtle bugs may be overlooked,
 example, natural language prompts crafted by users may not with significant downstream impacts. In fact, several recent
 always fully capture a their intent, as they may contain am- works exploring developer-AI interaction have highlighted the
 biguous language and lack of nuance. More importantly, it is need for mechanisms to facilitate verification of AI-generated
 not possible to automatically evaluate whether code generated code[14], [9], such as those that allow users to use tests that
 from a natural language prompt is correct. Natural language disambiguate between the different code suggestions [15].
 is inherently ambiguous and enforcing the user intent through However, prior research has shown that it can be difficult
 some mechanical process (such as testing, static analysis or for users to manually provide a sufficient number of test cases
 formal verification) is not immediately possible. to disambiguate suggestions upfront [16].
 Consider the following docstring, taken from MBPP [10], Inspired by findings around example generation and
 a popular Python programming tasks benchmark: disambiguation techniques in Programming By Examples
 2
(PBE) [17], and recent emerging ability of LLMs to generate Python benchmarks for code generation. This paper makes
tests [18], [19], [20] in this paper, we propose leveraging the following contributions:
user-feedback through LLM-generated tests to improve the 1) We propose an interactive workflow, T I C ODER, for guiding
trust and correctness of LLM-generated code. Specifically, user intent clarification through automatically-generated
we propose the workflow of test-driven interactive code gen- tests and improving code generation accuracy of LLMs.
eration (T I C ODER) to (a) clarify (i.e., partially formalize) user T I C ODER leverages off-the-shelf LLMs for generating
intent through generated tests, and (b) generate a ranked list code and tests, and provides a mechanism to check AI-
of code that is consistent with such tests. generated code through user-approved tests.
 Let us demonstrate a simple instantiation of this framework 2) We evaluate the effectiveness of T I C ODER by conducting a
using the earlier example, where a user prompts an hypothet- mixed-methods user study comparing two different variants
ical LLM to generate code satisfying their natural language of T I C ODER for generating and evaluating code sugges-
intent. Instead of directly displaying a list of plausible code tions, including a baseline condition representing existing
suggestions, our framework T I C ODER would query the user developer-AI interaction workflows. We observe a signifi-
with a question: cant reduction in cognitive effort reported by participants
 using either variant of T I C ODER over existing interaction
 text_lowercase_underscore("aa_bb_cc") == True?
 mechanisms.
 Let us assume that the user answers ’no’, since they 3) We further evaluate the performance of the T I C ODER
expect only two sequences of lowercase letters, joined by one workflow at scale by simulating user feedback, using the
underscore, as mentioned earlier. The workflow would likely reference code solution as an idealized proxy. T I C ODER
query the user again with the following question: is evaluated on on two Python datasets, MBPP and Hu-
 manEval, and a mixture of four open and closed sourced
 text_lowercase_underscore("aa_bb") == True? LLMs. We demonstrate that T I C ODER contributes to im-
 proving the code generation accuracy of all LLMs con-
 If the user says ’yes’, then the system would output the list sidered. We observe an average absolute improvement of
of approved tests, as well as a set of semantically ranked code 45.73% in pass@1 code generation accuracy within 5 user
suggestions that are consistent with those tests. Once the user interactions across both benchmarks. In fact, we observe
chooses a suggestion from such a list, it would generate code T I C ODER can boost smaller model pass@1 accuracy
along with accompanying tests. to levels comparable to much larger models, such as
 def text_lowercase_underscore(text): GPT-4-32k, within just one user interaction.
 return True if bool(re.search(r’ˆ[a-z]_[a-z]+$
 ’, text)) else False II. R ELATED W ORK
 def test_text_lowercase_underscore():
 assert text_lowercase_underscore("aa_bb")== 1) Improving Code Generation Accuracy: Techniques for
 True improving code generation accuracy is a rapidly growing
 test_text_lowercase_underscore()
 field of work. Unlike the work proposed in this paper, these
 In the case of LLM-based code generation, the generated techniques do not consider user feedback, or guide users in
tests not only help make natural language intent more precise clarifying their intent formally; we cover them briefly.
and prune incorrect suggestions generated by the LLM, but AlphaCode [21] and CodeT [22] both propose techniques
can also serves as debugging aid for remaining suggestions to improve code generation accuracy by generating tests using
and regression tests for future code edits [7]. LLMs, and then grouping code suggestions by the set of tests
 While the proposed framework appears intuitive, it may not that they satisfy. CodeT [22] refines the approach by scoring
scale to more complex code generation tasks. For example, tests and code suggestions simultaneously by prioritizing tests
in cases where the user is unable to validate tests, e.g. for that satisfy many code suggestions and prioritizing codes that
tests that require intricate testing frameworks, the a workflow satisfy many tests. While there are similarities with CodeT
may not be tenable. Furthermore, the utility of the interactive in using LLM generated tests to rerank generated code that
framework is contingent upon (a) the ability of LLMs to results in code generation accuracy on benchmarks, T I C ODER
generate useful tests, and (b) the cost-benefit trade-off of the is complementary as one can apply T I C ODER after CodeT.
overhead of user interaction versus the benefit on pruning and But more importantly, we argue that a user cannot trust
ranking of code suggestions. the generated code from CodeT any more than using LLM
 To this end, we seek to understand: How does the proposed directly. This is because the user is still presented with a
workflow impact the performance of developers evaluating set of code suggestions. In contrast, with T I C ODER, we first
AI generated code? In addition, the proposed framework formalize the user intent through tests allowing the user to
should scale, augmenting the code generation accuracy of constrain the code that the user will need to eventually sample
several open and closed-source LLMs. Thus we also seek to from. T I C ODER also allows users to modify test output in one
answer: Does proposed workflow augment the accuracy of setting, which is not possible in the CodeT approach, where
code generation models? the tests are fixed throughout. As part of future work, we plan
 To answer these questions, we explore the effectiveness to explore if our approach may benefit from code and test
of our proposed framework through a (1) mixed-effects user ranking algorithms in CodeT.
study and (2) a large scale evaluation of the approach on two
 3
 Similarly, work on program synthesis [23], [24] generates III. R ESEARCH Q UESTIONS AND PAPER O RGANIZATION
code that satisfies a formal specification either expressed as We briefly introduce the research questions and discuss
a logical specification or input-output tests [25]. Our work paper organization. In the following Section IV-A we introduce
differs in that we use LLMs to generate code from informal our proposed approach: TiCoder. Then we answer two distinct
specifications, i.e. natural language intent. However, it would research questions:
be interesting for future work to leverage user-provided tests
 RQ1 How does TiCoder impact the performance of python
to improve the quality of code generation, as explored in
 developers evaluating AI generated code, in terms of
recent works [26], [27]. In this work, to evaluate our proposed
 task correctness, time, and cognitive load? To answer
approach at scale, we simulate user feedback using the code
 RQ1, we conduct a user study, where participants use
reference implementation as an idealized proxy, similar to
 AI assistants augmented with the TiCoder workflow. We
prior works in oracle-guided inductive synthesis [15], [28] and
 evaluate the cost benefit tradeoff of the proposed ap-
interactive program synthesis [29], [30] where an an oracle
 proach on developer effort when evaluating AI generated
(reference implementation or users) is queried to identify the
 code.
output for a given input. However, prior works in this area
 RQ2 Does the TiCoder workflow improve the accuracy
appeal to an automatic symbolic engine (such as a constraint
 of generated code suggestions? To answer RQ2, we
solver [30] or automata construction [17]) to generate dis-
 explore the code generation accuracy of LLMs augmented
tinguishing example inputs for a pair of programs, which
 with the TiCoder workflow on two code generation
is inconceivable for general purpose imperative programming
 benchmarks in python.
languages such as Python.
 2) Usability of AI Programming Assistants: There exists The methodology, evaluation, and results of each research
several prior works exploring the usability of AI programming question are organized in the following sections: Sections V
assistants. In this section, we focus on recent work that and VI describe the methodology and results for RQ1, and
identifies challenges related to the expressing of intent and Section VII describes the methodology and results for RQ2.
control over the generation suggestions of AI assistants. We separate methods and results of RQs into distinct sections
 Liang et al. [8] identify that giving up on incorporating for clarity. We conclude with a Discussion (Sec. VIII) of the
generated code, and lack of ability to provide feedback, are implications of our work to the broader research community,
the most common usability issues encountered when using and the Limitations of the presented experiments (Sec. IX).
completion-based AI programming assistants. This often oc-
curs because the code does not implement the desired function- IV. P ROPOSED A PPROACH : T I C ODER
ality, participants do not know why certain code was generated
and had trouble controlling the output to be aligned with their
desired intent.
 McNutt et al. [31] enumerate a design space of interactions
with code assistants, including how users should be able
to disambiguate candidate programs or refine their initial
specifications, echoing prior studies have indicated that dis-
ambiguation can be valuable in the context of assistants like
GitHub Copilot [32] and traditional program synthesis tools
[33]. Similarly, Xu et al. [9] explored challenges of IDE-based
AI assistants, including how well specified the queries that
users formulate are. They find that participants frequently have
trouble expressing intent in their natural language queries to
the assistant, and issues of under specification often relate to
ambiguous instructions, such as omitting variable names.
 Mozannar et al. [34] identify 12 core activities associated
with using GitHub Copilot and find that programmers often
iterate on their prompts until they obtain the suggestion they
desire, and spend a significant amount of time verifying code
 Fig. 1: T I C ODER workflow.
suggestions. In fact, recent work by Bird et al. [14] shows
that as result of AI-powered tools, developer roles are shifting In this section, we outline a proposed workflow for leverag-
so that more time is spent time reviewing code than actually ing test generation and user feedback to clarify (i.e., partially
writing code. Several recent works[35], [36], [37] identify formalize) user intent. We refer to this approach as T I C ODER
clear opportunities for improving the accuracy of LLM code (Test-Driven Interactive Code Generation), and define two
generation techniques. Our work builds upon observations of variants of the workflow and surface this interaction to users
previous studies, and explores mechanisms to support code in the following subsections.
evaluation tasks.
 4
 import re Prefix prfxp a) [19]. On the other hand, T I C ODER -O UTPUT puts less
Code Prompt
 def text_lowercase_underscore(text): Header hp burden on an LLM to create the correct output for a given test
 Test Prompt
 input; relying instead on the user. However, it may require the
 """Write a function that returns true if the input string
 contains only lowercase letters joined with an underscore, user to specify a possibly non-trivial test oracle when used
 and false otherwise.""" Description sp beyond input-output examples.
 pass Prompt Body b'p
 1 A test violates a precondition if the function is undefined on the test input.
 def test_text_lowercase_underscore():
 Test Body t'p For example, the test assert SquareRoot(-4) == -2 undefined on
 assert text_lowercase_underscore(
 negative numbers.
Fig. 2: Example format, as well as code and test prompts for
the running example. B. TiCoder Implementation
A. High-level Workflow In this section, we discuss one possible implementation of
 Figure 1 describes the high-level workflow of Test-Driven the T I C ODER workflow. Specifically, we outline the approach
Interactive Code Generation (T I C ODER). to generating code and test suggestions, ranking candidate tests
1) The user requests the AI programming assistant to generate to surface to the user, pruning and ranking code suggestions
 a function, given optional code context including an exist- by user response. To simplify the presentation, we restrict
 ing prefix in a file, a natural language description, and the ourselves to the case of single function synthesis, where the
 function header containing method name, parameters and user input consists of a natural language comment sp , the
 returns. function header hp , as well as any optional prefix prfx p needed
2) The AI programming assistant internally generates a set of to generate the body of the function p. Figure 2 shows an
 candidate code and test suggestions by prompting an LLM. example for our running example. In addition, we also assume
3) The set of generated tests are executed for each candidate the presence of a set of hidden tests Tp (input-output pairs for
 code suggestion. The set of tests that pass or fail on each simplicity) to evaluate the correctness of the generated code,
 code suggestion are stored. as well as a hidden reference (oracle) implementation of p,
4) Using execution information, the AI programming assistant namely bp . Our workflow does not have access to either Tp or
 ranks (according to some heuristics) the set of generated bp .
 tests and then surfaces the top ranked test to the user as a 1) Generating Code and Tests: We outline one possible
 query; asking the user if a test is consistent with the user’s choice for implementing the prompt generation for generating
 intent. code and test suggestions for an example.
5) The user responds either PASS, U NDEFINED, or FAIL sig- Figure 2 presents a possible code prompt (in the gray
 nifying if the test is respectively: consistent, precondition- boxes) that can be used to query an LLM to produce a set
 violating1 , or inconsistent with the user intent. Optionally, of code suggestions for our running example. Querying a
 in the case of FAIL, the user can provide the correct test LLM with the code generation prompt will result in a set
 output O UTPUT. of code suggestions similar to ones shown in Figure 3. Code
6) The AI programming assistant leverages the user response suggestion c3 is a valid solution to the problem, while c1 is an
 to prune, and rank the set of code and test suggestions. incorrect code suggestion (since it allows the first substring to
7) Interaction steps 4-6 can be repeated for multiple iterations, start with an uppercase letter) and c2 is also incorrect (since
 until a predefined termination criteria (e.g., fixed number it allows more than one sequence of lowercase letters joined
 of steps, absence of tests) has been satisfied. with an underscore). Similarly, the green boxes in Figure 2
8) Once the interaction terminates, the AI programming as- shows one possible test prompt that augments the code prompt
 sistant outputs (a) a set of tests that the user has approved with the statement pass as the method body (corresponding
 or specified, and (b) a ranked list of code suggestions that to a placeholder implementation in Python) along with the
 are consistent with the user responses. assertion to be completed within a test function. We use the
 We define two variants of the workflow: T I C ODER - generated test suggestions (Figure 3) to present the user with
PASS FAIL and T I C ODER -O UTPUT. The first scenario rep- a set of tests. Some of these are consistent with the user intent
resents the case where the user provides only a Boolean (t3 ); while others are inconsistent with the user intent (t1 and
PASS ,FAIL response. The second scenario, T I C ODER - t2 ).
O UTPUT, extends the first scenario and represents the case 2) Ranking test suggestions: After obtaining the set of
where the user provides the expected output O UTPUT in the tests produced by an LLM, the user is presented with a
case of a FAIL test. sequence of tests. The user response to these proposed tests in
 We present both the scenarios as they enjoy comple- both T I C ODER scenarios (T I C ODER -PASS FAIL, T I C ODER -
mentary benefits. The T I C ODER -PASS FAIL scenario is more O UTPUT) are used to prune and rank code suggestions. To
lightweight, in terms of user feedback, as well as, generalizes minimize the number of user interactions, it is desirable
well for richer tests beyond input-output examples. For exam- to prioritize tests that would result in the most number of
ple, tests for stateful APIs comprises of a test-prefix as input incorrect code suggestions being pruned away [15], [29]. To
and the output oracle consists of a non-trivial predicate (e.g., achieve this, the set of tests are executed against the set of
checking functional correctness of a stack object using the possible code suggestions generated by the LLM.
predicate s.pop() == a on a stack object s and element Then, using this execution information, we adopt a
 discriminative test ranking policy that prioritizes tests
 5
Fig. 3: Code and test suggestions for the running example in Figure 2 generated from a LLM. Code suggestion c3 and test
suggestion t3 are both correct, while code suggestions c1 , c2 and test suggestions t1 , t2 are incorrect (appear shaded), i.e. they
don’t satisfy the problem prompts in Figure 2.
that can discriminate best among the set of code suggestions behavior on tests is contradictory to user expectation. Let us
 .
generated by the LLM. If a test t can discriminate between first consider the case of code pruning. Let t = (i, o) be a test
code suggestions well (i.e., splits the set of code suggestions in the form of an input-output example presented to the user.
into roughly equal halves), then it would prune away a If the user responds PASS, then we prune any code c ∈ G for
substantial fraction of the code suggestions irrespective of the which executing c(i) ̸= o. Similarly, if the user responds FAIL,
user response (either PASS or FAIL). then we prune any code c ∈ G for which executing c(i) = o.
 More precisely, let U be the set of test suggestions and G In addition, for T I C ODER -O UTPUT if the user provides the
be the set of code suggestions that have not been pruned away desired output o′ for the input i, then we can further prune any
after k ≥ 0 user interactions. For each test t ∈ U , we split the code suggestion c for which c(i) ̸= o′ . Note that we cannot
 −
set of code suggestions G into the sets G+ t and Gt of code soundly prune any code if the user responds with U NDEFINED.
suggestions that pass and fail the assertion in t, respectively. Finally, we define a simple code ranking strategy that uses
Note that we ignore codes that results in a crash on a test t the tests in U to determine a ranking on code suggestions in G
instead of failing with an assertion failure. We treat these as as follows: Each generated code c ∈ G is executed with each
precondition violation. We then prioritize tests where the ratio test t ∈ U and gets assigned as a score the number of passing
of the sizes of these two set is closest to 1. In other words, we tests dc . The codes are then ranked based on the decreasing
rank the tests in decreasing order using the following scoring order of dc .
metric sdiscr : Following from the example in the previous section, rep-
  resented in Figure 3, code suggestion c1 passes on all tests
 0 if max(|G+ −
 t |, |Gt |) = 0,
 {t1 , t2 , t3 }, code suggestion c2 passes on {t2 , t3 } and code
 sdiscr (t) = + − suggestion c3 passes on {t3 }. Our ranking would therefore
  min(|Gt+|,|Gt−|) otherwise. rank c1 highest initially in the absence of any feedback from
 max(|Gt |,|Gt |)
 the user.
 Note that the test ranking strategy is uniform for both the
scenarios, although the test output will be possibly mutated V. RQ1: U SER S TUDY M ETHODOLOGY
by the user response in T I C ODER -O UTPUT.
 Consider the example in Figure 3. Consider the two tests t1 We aim to understand how the T I C ODER workflow may
and t2 : Two code suggestions {c2 , c3 } FAIL on test suggestion support software developers as they use AI-programming
t1 while one suggestion {c1 } PASS, making sdiscr (t1 ) = assistants to generate and evaluate code suggestions. We are
min(1, 2)/max(1, 2) = 1/2. Similarly, two code suggestions seeking to answer the following research question:
{c1 , c2 } PASS on test suggestion t2 while one suggestion RQ1 How does TiCoder impact the performance of python
{c3 } FAIL and sdiscr (t2 ) = 1/2. All code suggestions in this developers evaluating AI generated code, in terms of
example PASS on test t3 making sdiscr (t3 ) = 0. task correctness, time, and cognitive load?
 3) Pruning and ranking code suggestions: T I C ODER re- To answer our research question we conduct a controlled
turns a ranked list of code suggestions, whose behavior is study with 15 participants consisting of 3 coding evaluation
consistent with all the user responses, and prunes the other tasks. To complete each task, participants are asked to interact
code suggestions generated by the LLM, whose execution with one of the following AI assistants: Assistant 1 with no
 6
user intent refinement, Assistant 2 representing T I C ODER - We make this decision to reflect the current user experi-
PASS FAIL workflow, or Assistant 3 representing T I C ODER - ence scenario of several real-world AI code generation tools,
O UTPUT workflow. Participants use each assistant to generate such as GitHub Copilot’s completion panel. For example, the
and evaluate a set of code suggestions. GitHub Copilot completion panel in VSCode shows the user
 We recruit participants using a mix of distribution lists and up to 10 possible code suggestions at a time. Our decision is
personal contacts. 3 of 18 participants were used as part of also informed by research pointing to the benefit of surfacing
the pilot study to inform our design, and the remaining 15 multiple code suggestions[31], [33], [32], [8]. We limit the
are used in the final experiment. Table I contains participant maximum number of codes to 5 so as to allow the participant
demographic information. 8 participants are either professional to complete each task within 15 minutes.
software engineers or researchers at Microsoft, and the re- 2) Treatment condition: AI Programming Assistant 2:
maining 10 participants are PhD students from academia. The Assistant 2 represents the T I C ODER -PASS FAIL (Sec. IV-A)
study was IRB approved with voluntary participation and paid scenario, where a user provides instructions in the form of a
$15. All interviews were conducted over a video-conferencing prompt, and then the Assistant generates test cases that the user
platform and lasted approximately 45-minutes. must validate. The user validates each test by indicating if the
 Participants were asked to complete each code evaluation test should pass or fail. Assistant 2 then uses the tests to prune
tasks with one of the three different AI code generation any of the 5 code suggestions that differ in behaviour validated
assistants. Each task had a time limit of 15 minutes. We use by the user. For example, if the user decides that the test should
a within subject design, such that each participant uses all pass, only codes that pass the test are retained. These retained
three assistants, i.e. a different assistant for each task. Each code suggestions are shown to the user, in random order.
AI assistant represents one treatment under study, which we 3) Treatment condition: AI Programming Assistant
describe in the next subsection. 3: Assistant 3 represents the T I C ODER -O UTPUT scenario
 (Sec. IV-A). Instead of indicating whether a test should
 Python Python AI Programming
 ID Occupation pass/fail (i.e. Assistant 2 interaction mechanism), users must
 Experience Frequency Assistant Use
 provide the expected output of the test. Assistant 3 then uses
Pilot >5 years Daily Daily Industry
Pilot >5 years Monthly Monthly Industry the tests completed by the user to prune any of the 5 code
Pilot >5 years Daily Daily Industry suggestions that do not generate an output consistent with what
P1 >5 years Monthly Daily Industry the participant defined.
P2 >5 years Weekly Monthly Industry
P3 >5 years Rarely or never Rarely or never Industry Both Assistants 2 and 3 use the tests to prune away
P4 >5 years Daily Daily Industry generated codes that do not match the behaviour specified by
P5 3 - 5 years Weekly Weekly Academia the participant. We restrict the number of pruned codes in each
P6 >5 years Weekly Weekly Academia
 task so that a participant using Assistant 2 or 3 will always
P7 >5 years Weekly Monthly Industry
P8 >5 years Monthly Rarely or never Academia see between 3-4 code suggestions if they correctly evaluate
P9 >5 years Daily Monthly Academia the tests shown to them. We make this decision to reflect the
P10 1 - 2 years Weekly Daily Academia potential real-world scenario where T I C ODER is able to prune
P11 >5 years Daily Daily Academia
P12 3 - 5 years Weekly Rarely or never Academia away at least 1 of the candidate code suggestions generated
P13 >5 years Weekly Rarely or never Academia by an AI Assistant. However, a participant may see less than
P14 3 - 5 years Rarely or never Rarely or never Academia 3 code suggestions if they specify a contradictory or incorrect
P15 >5 years Daily Daily Industry
 program behaviour through their answers to the tests.
 Participants interact with the assistants in an online survey
TABLE I: *Weekly denotes a few times a week, *Monthly platform, but they are able to copy and paste the generated
denotes a few times a month. code and tests into an IDE of their choice during the task.
A. Treatments All code is formatted so as to not introduce external factors
 The experiment includes one control condition and two into the participants’ time. The interactive nature of the AI
distinct treatment conditions, implemented as different AI pro- Assistants in encoded into the survey logic, to mimic real-
gramming assistants. Each assistant differs in it’s interaction world execution and pruning of code suggestions based on
mechanism with the developer and dictates the method in a user’s answers. Participants can maintain their view of the
which to surface the final set of code suggestions shown to tests they validated in the survey throughout the task.
each user. To ensure that the same set of codes is shown to all
participants across treatments, we pre-select the prompt used B. Task Design
to generate code suggestions. Second, to ensure we measure We selected coding tasks that would satisfy the following
the impact of our dependent variables on only the process of criteria, for each of the three tasks: (1) evaluating 5 AI-
evaluating AI generated code, we also restrict the ability to edit generated code suggestions could be completed in fifteen
the AI generated code suggestions. The interaction framework minutes, (2) there are syntactically valid but semantically
of each Assistant is described below: incorrect code completions given by the LLM (GPT-3.5)
 1) Control condition: AI Programming Assistant 1: with a diversity of error types across tasks (3) they varied
Assistant 1 represents the control condition for the experiment. in problem domain and complexity, and (4) the LLM could
Given the pre-selected prompt, Assistant 1 generates 5 code generate reasonable tests that capture the diverse error types.
suggestions for the user, surfaced in a random order. Partici-
pants using Assistant 1 always see 5 unique code suggestions.
 7
Task Task Name Description Treatments
 Write a function that returns true if the input string consists of two sequences of lowercase letters joined
T1 L OWERU NDERSCORE A1, A2, A3
 with a single underscore and false otherwise.
T2 F IRST M ISSING Write a function that finds the smallest missing number from a sorted list of integers, starting from 0. A1, A2, A3
 Write a function to find the maximum product formed by multiplying numbers
T3 M AX P RODUCT A1, A2, A3
 of an increasing contiguous subsequence of that array. The sequence may include negative numbers.
TABLE II: Tasks included in the user study, derived from the MBPP dataset. A1 represents the control treatment, A2 represents
the T I C ODER -PASS FAIL treatment, and A3 represents the T I C ODER -O UTPUT treatment.
 1) Identifying Task Candidates: We select task candidates in Figure 4. Participants are able to view the coding task
from the MBPP dataset [38], a popular code generation bench- description, and depending on the treatment received, they can
mark, consisting of short Python functions designed to be answer the AI Assistant’s question, around the validation of
solved by entry-level programmers. MBPP provides a natural a test case, directly in the survey. Once code suggestions are
language instruction, a set of tests, and a ground truth code surfaced by the Assistant, participants are allowed to copy the
implementation for each problem. We cluster functions from code and run it for debugging, along with the set of provided
MBPP based on problem domain, complexity as measured tests, depending on the treatment. For each task, participants
by cyclomatic complexity and size of the function in terms were asked to identify if the AI Assistant had returned a correct
of lines of code. From each cluster we identified a set code suggestion, and if yes, which one.
of candidate functions for which we generated a code and We employ a Latin Square Design to systematically vary the
test completions for using a LLM. We finally selected 3 pairing of tasks and AI assistants. Each participant completes
problems for the code completion tasks that best satisfied three tasks (T1, T2, and T3), each with a different AI assistant
the selection criteria. These problems represent three dis- (Assistant 1, Assistant 2, Assistant 3). The order in which the
tinct styles: M AX P RODUCT is an algorithmic task involving participants use the AI assistants for each task is randomized to
dynamic programming, L OWERU NDERSCORE involves using account for learning effects. This design ensures that each AI
regex for string manipulation, and F IRST M ISSING involves a assistant is used an equal number of times across all tasks and
recursive binary search. The tasks are detailed in Table II. positions, thus balancing potential order effects and providing
 2) Generating Code and Test Suggestions: To generate a robust comparison of the AI assistants
the code and test candidates, we give the natural language For each task, participants are encouraged to ask any ques-
instructions from the MBPP dataset as a prompt to the OpenAI tions around the task instructions. Our aim is to approximate
GPT-3.5-turbo chat completion endpoint with the default the scenario where the user clearly understands what they
API parameters (temperature = 1.0). We then sample a set of want the AI Assistant to generate, such that they would query
5 incorrect codes using the tests from the MBPP dataset, to the AI Assistant with the same or similar prompt originally
identify buggy programs. We also run the set of generated used to generate code and test suggestions. Although the real
tests against the set of codes to make sure at least 1 and at world usage of the workflow would differ, as developers often
most 2 code suggestions are caught by the test, to restrict edit their prompts, we choose to fix the prompt to control for
the number of codes that would be pruned away. Rather than the generated code and tests across participants. Furthermore,
manually inject bugs into the ground truth program, we choose we are not interested in the task of code generation, rather
to sample the set of buggy codes from the LLM to reflect the code validation, i.e. not if the user can edit the prompt to get
nature of bugs users may encounter in AI generated code. different suggestions, but rather how the T I C ODER workflow
 The final set of tests and codes are fixed per task, regardless can help refine user provided natural language specification
of the treatment used. For each task there are 5 suggestions: 4 through tests, and how it may impact a developer’s ability to
buggy codes and 1 code that is extracted as the ground truth validate code, and locate a correct suggestion out of a set of
from the MBPP dataset. If the ground truth program extracted generated codes. While T I C ODER may help reduce the number
from MBPP does not handle certain pre-condition violations, of times a user must edit their original prompt, we save this
we augment the code to match the task intent. For Assistants exploration for future work.
2 and 3, we show exactly 2 of the AI generated tests for each
task. The final set of codes are either directly shown to the user D. Measured Variables
by Assistant 1, or first pruned based on the user’s evaluation
of the tests for Assistants 2 and 3. From the study recordings and user-submitted survey data,
 we collect a set of metrics on each task completed by the
C. Study Protocol participants:
 At the start of the study, participants are given general Time. We measured time taken to complete each task from
instructions around how to interact with each AI assistant, the recordings of each participant interview. Time for each task
the differences between them, and how to validate generated includes time taken to evaluate any tests. We measure time on
tests. Participants are also given time to set up their Python task to determine if the T I C ODER workflow adds significant
interpreter or environment before the start of the study. The time overhead due to validation of tests, as compared to the
survey interface used to interact with the AI assistants is shown control condition.
 8
Fig. 4: From left to right: Examples of different interaction sequences invoked by Assistant 1 on task T1 (directly display all
code suggestions), Assistant 2 on T2 (validate the test output on a given input), and Assistant 3 on T3 (specify the output for
a given input).
 Correctness. The correctness is dependant on 1) the correct for pairs of conditions for which the results are statistically
evaluation of the generated tests, relative to the oracle code significant.
implementation and 2) the correct selection of the code sug-
gestion whose behaviour reflects the intent of the prompt. Each Assistant 1 Assistant 2 Assistant 3 Pairwise
 Metric
 (mean) (mean) (mean) Significance
task has at most 1 correct answer: either one of the generated a1<a2(p = 0.001)
 Correctness* (0,1) 0.40 0.84 0.64
code suggestions is correct or none of suggestions are correct.
 Time (seconds) 327.7 284.15 253.88 -
 Cognitive Load. The T I C ODER workflow aims to improve
 Cognitive a1>a2(p = 0.007)
code generation accuracy and reduce the number of candidate Load* (0-100)
 45.46 28.00 29.52
 a1>a3(p = 0.012)
code snippets that a user needs to review, ultimately reducing Mental a1>a2(p = 0.001)
 12.5 7.50 7.6
the cognitive effort of code evaluation. However, T I C ODER Demand* (0-20) a1>a3(p = 0.004)
may also add additional cognitive effort, stemming from the Stress* (0-20) 8.26 3.84 6.35 a1>a2(p = 0.02)
effort required to validate tests. To test the impact of the Pace* (0-20) 8.13 5.38 4.70 a1>a3(p = 0.04)
workflow on cognitive effort, after each task we measure Confidence (0-20) 13.5 15.92 15.88 -
participants’ self-reported cognitive load via their responses Effort* (0-20) 11.00 7.15 6.7
 a1>a2(p = 0.02)
 a1>a3(p = 0.014)
to five NASA TLX questions [39], a standardized approach
to measuring self-reported cognitive load used widely across
disciplines [40]. We measure the following metrics using the TABLE III: Mixed-effects model analysis results for control
standard 20 point scale: mental demand, effort, perceived (Assistant 1) and treatment (Assistant 2, 3) conditions. (*
success, pace, and stress. denotes a significant observation. – indicates no significance.)
E. Evaluation of Measured Variables
 For each measured variable, time, correctness, and dimen- A. Impact on Task Correctness
sions of cognitive load, we run a mixed-effects regression Using the mixed-effects regression model with the cor-
model. We use with either linear or logistic models depending rectness of the task (coded as 0 or 1), as the dependent
on the data type. We use the treatment condition as the fix- variable: The mean correctness was 0.40 for participants using
effects independent variable, and participant ID and coding Assistant 1, 0.84 Assistant 2, and 0.64 Assistant 3. Although
task as the random-effects variables. the mean is higher in Assistant 2 and 3, the effect is significant
 We conduct an omnibus test using ANOVA to calculate the for Assistant 2 only with (p=0.001). Looking at the set of
p-value of the treatment condition (the assistant used) against mistakes made by participants, we notice several interesting
the measured metrics. To correct for multiple comparisons observations. In general, participants using Assistant 1 are less
and conduct False Discovery Rate (FDR) correction[41] for likely to identify the correct code suggestion from the set of
significant pairs of conditions. We only report Omnibus p- 5 suggestions.
values for pairs of conditions for which the results are statis- For example, for Task 1, 3/4 participants that failed to
tically significant, and the direction of significance. We chose identify the correct suggestion were using Assistant 1. Looking
mixed-effects models to account for individual variability at their responses, all 3 participants identified different sug-
(participants) and hierarchical data structures (task treatment gestions as correct. One participant, P7 chose to not execute
pairs), using ANOVA for omnibus to test the significance any of the code suggestions, while the other two participants
of fixed effects (the assistant used), and conducted FDR to P3, P5 did write tests to evaluate the code suggestions,
provide a comprehensive assessment of treatment effects while they were not able to find a test to characterize the bug.
controlling for Type I errors. Similarly, for task 3, 2/4 participants that failed to identify
 VI. RQ1: U SER S TUDY R ESULTS the correct suggestion were using Assistant 1, and chose
 Our key quantitative results are summarized in Table III. different candidate suggestions. Interestingly, both participants
The last column of Table III provides Omnibus p-values
 9
also only tested a subset of the codes, based on an initial guess 1 is 327.7 seconds, 284.15 for Assistant 2, and 253.88 for
of the correct suggestion. Assistant 3. Although the means differ slightly across Assis-
 Looking at the differences between Assistant 2 and 3, we tants, on average participants using TiCoder take less time to
notice that mistakes stem from both incorrect evaluations of complete the code evaluation tasks. However, this effect is not
the surfaced tests and incorrect evaluation of the code sugges- significant.
tions. For example, in Task 2 F IRST M ISSING, the first test case This indicates that the additional overhead of requesting
surfaced to participants by Assistant 2 is shown shown in Fig- participants to verify or provide the output for a test case
ure 2.b: assert find_First_Missing([1,2,4,6])==0. does not add significantly to the time taken to complete the
All participants shown this test correctly answered that this test task. The time taken to evaluate code suggestions may be
should pass. However, when the output == 0 is obfuscated on tempered by the number of code suggestions pruned, and the
the same test by Assistant 3, 50% of the participants indicated fact that Assistants 2 and 3 provide test cases to support
that the test should evaluate to 0, and the other 50% indicated the code evaluation process. One indicator of how long a
that it should (incorrectly) evaluate to 3. It is interesting to note participant takes to complete a task may be tied to their code
that given a correct test by Assistant 2, participants are able evaluation strategy. We notice that, regardless of the treatment,
to correctly evaluate it, however, if Assistant 2 had generated participants that choose to execute and test every single code
an incorrect test output ( == 3) it may not always be the case suggestion, take much longer than participants that scan the
that participants are able to catch this bug. code suggestions and selectively execute and test candidate
 However, not all tests surfaced by Assistant 2 are correct. suggestions that ’look’ correct to them.
In Task 1, both tests surfaced by Assistant 2 had incorrect test For example, (P2) had relatively longer task times when
outputs; testing edge case scenarios that should fail. For exam- using all 3 assistants, and chose to mentally execute every
ple text_lowercase_underscore("Hello_world") == suggestion, identify the bug in each suggestion, and then pro-
True. For Assistant 2, all participants were able to correctly ceeded to programmatically execute and test their hypothesis.
identify that the test should fail. For participants using Assis- Due to their thorough evaluation strategy, P2 was correct on
tant 2, 4/5 indicated that it should evaluate to ’False’ while all tasks. However, we do not observe a correlation between
one participant indicated that it should (incorrectly) evaluate time on task and correctness, both within, and across tasks
to ’True’. (Pearson’s Correlation Coefficient r = 0.016, p = 0.911).
 In Task 3, all participants using Assistant 2 and Assistant Key Findings The time taken to validate test cases,
3 were able to correctly evaluate the tests surfaced by the introduced by TiCoder, does not introduce significant over-
Assistants. However, 2 of the participants using Assistant 3 head to total task time. Participants using TiCoder take, on
were not able to identify the correct code suggestion, whereas average, less time to complete the code evaluation tasks,
all participants using Assistant 2 were successful. however, this effect is not significant.
 By construction, upon the erroneous evaluation of a test case
by a user, the TiCoder workflow will prune all valid programs
that pass on the test. Therefore, participants that incorrectly C. Impact on Task Induced Cognitive Load
evaluate a test case will no longer see any valid AI-generated We analyze the self-reported cognitive load of participants
programs and cannot correctly complete the task, unless they across 5 dimensions, outlined by the NASA TLX: mental
specify that none of the code suggestions are correct. In demand, effort, pace, stress, and confidence of the task correct-
the TiCoder workflow, noisy user response guarantees that ness. Cognitive load is reported as the cumulative sum across
generated code does not match the ’ground truth’ user intended all 5 dimensions. Using a mixed-effects regression model
specifications. Therefore, in practice, the option to skip a test with the cognitive load as the dependent variable, we observe
evaluation is imperative to the usability of the workflow, and that participants using Assistants 2 and 3 report significantly
to reduce uncertainty as the source of noisy input by the user. less cognitive load. Looking more closely at the different
Though TiCoder may significantly support users in correctly dimensions, for Assistant 2 participants report significantly
evaluating code suggestions, the potential for noisy feedback less mental demand, stress, and effort required to complete
is a critical risk to consider. the task. For Assistant 3 participants report significantly less
 Key Findings Participants using TiCoder Assistant 2 are mental demand, effort, and better pace.
 significantly more likely to correctly evaluate AI generated Overall, we posit that this effect might be observed due
 code. Participants using Assistant 3 were, on average, more to the the reduced number of code suggestions that the user
 likely to correctly evaluate code suggestions compared to must evaluate, and that tests serve as concrete mechanisms
 participants that were not using TiCoder. However, par- for which to reason about the code; as well as provide a
 ticipants were also more prone to making mistakes while starting point for more extensive testing of the candidate
 providing test outputs that dealt with edge cases. functions, making it easier to get the task started. For example,
 when asking clarifying questions about the prompt used in
 a task, participants using Assistant 1 struggle to articulate
B. Impact on Task Time
 their question before coming up with an illustrative test case.
 To test the effect of each Assistant on time, we used a For Task 3 M AX P RODUCT, participants using Assistant 1
mixed-effects regression model, with time as the dependent had difficulty conceptualizing ’increasing contiguous subse-
variable. The mean time taken by participants using Assistant quence’. The interviewer made sure to answer any questions
 10
 the participant had, but took care to not give concrete examples is correct. Given that the list of code suggestions from TiCoder
 to not bias the participant. For example, P19 first asked are ordered, our metric pass@k@m is not a statistical measure
 ”so you’re multiplying just two numbers, but it has to be (unlike pass@k which measures the statistical odds of any
 next to each other?”. When the interviewer clarified that it sample of size k containing a correct code solution), but
 could be more than two numbers, given that the sequence is deterministically check if any one of the top k ranked code
 increasing, the participant articulated their question with an suggestions is correct.
 example ”...so if I have, 1 2 4 1, it would be 1 by 2 by 4?”.
 In contrast, participants that had similar questions, but were C. Models and Baselines
 using Assistants 2 or 3, were able to more easily articulate
 T I C ODER augments AI assistant workflows to improve the
 their questions using test cases generated by the AI Assistant.
 code generation accuracy of the underlying LLM. To assess
 Key Findings Participants using TiCoder, in both Assistant T I C ODER’s benefits across various LLMs, we’ve chosen four
 2 and 3 settings, report significantly less task-induced cog- state-of-the-art completion models, which include a mix of
 nitive load while evaluating AI generated code. This effect closed-source and open-source models. We provide a brief
 may be explained by the code pruning and test clarification description of each model next.
 mechanisms offered by TiCoder. • OpenAI code-davinci-002, text-davinci-003 [1]
 is a closed source LLM specifically designed for code
 VII. RQ2: B ENCHMARK E VALUATION completion tasks. It is based on the GPT-3 architecture
 Results from our user study, Section 5, indicate that TiCoder containing 175B parameters.2 text-davinci-003 is
 can significantly improve correctness of participants evaluating also a closed source model of size 175B parameters,
 AI generated code, and that the workflow helps to reduce however, it is based on the GPT-3.5 architecture and
 task-induced cognitive load. However, it is unclear if the InstructGPT [11] and can be used for a variety of nat-
 proposed workflow is able to effectively generate tests that, ural language tasks. Compared to other non-chat based
 once validated, can prune and rank a set of code suggestions completion models, text-davinci-003 demonstrates
 with higher accuracy, on a large set of problems. To eval- highly competitive performance on a number of tasks.
 uate the potential utility of the TiCoder workflow at scale, • OpenAI GPT-3.5-turbo, GPT-4-turbo, GPT-4-32k
 we implement T I C ODER -PASS FAIL and T I C ODER -O UTPUT, The OpenAI chat models are based on the pre-trained
 and conduct an empirical evaluation on two state-of-the-art GPT-3 model, which is fine-tuned using Reinforcement
 benchmarks for code generation in python. We aim to answer Learning with Human Feedback (RLHF) [11]. While
 the following research question: these models are not explicitly fine-tuned for code gen-
RQ2 Does the TiCoder workflow improve the accuracy of eration, they have demonstrated strong capabilities on
 generated code suggestions? several related tasks [42], [43]. We use OpenAI APIs for
 the gpt-3.5-turbo, gpt-4-32k, and gpt-4-turbo
 endpoints.
 A. Datasets
 • Salesforce CodeGen-6B, CodeGen2.5-7B [3] is an
 We use two Python programming datasets for our evalua- open source LLM, with 6B parameters, trained specif-
 tion, including the sanitized version of the MBPP dataset [38], ically to translate natural language instructions to
 dataset from Google, and the HumanEval dataset, introduced code. CodeGen2.5-7B [44] is an improvement on
 in the Codex paper [1], to answer the research questions. CodeGen-6B and is slightly larger, with 7B parameters.
 MBPP consists of 427 and HumanEval of 164 examples in Currently, this model is the state-of-the-art for code
 the format described in Sec IV-B, along with the hidden generation compared to other models of similar parameter
 tests and reference implementations. We modify the original size.
 HumanEval dataset to remove any (non-hidden) input-output Our aim is to understand how TiCoder can help improve
 examples that are included in the docstring to avoid making code generation accuracy across different LLMs, and not to
 the test generation task trivial. identify the best performing model. Therefore, we use default
 configurations for each model, and only alter temperature.
 B. Evaluation metric We experimented with different temperature configurations to
 For evaluating the correctness of the generated code sug- optimize performance and diversity of generated code and
 gestions, we use the popular metric pass@k for evaluating test suggestions. Intuitively, a temperature closer to 1 allows
 the accuracy of code-generation by LLMs with respect to the LLMs to provide a more diverse set of solutions, whereas a
 hidden tests provided by each dataset [1]. A code suggestion temperature closer to 0 forces LLMs to only generate fewer
 is correct if it passes all the hidden tests, and pass@k solutions with the highest confidence. Following [1], [45],
 determines the mean expected value of an arbitrary sample [46] for all models we settle on a temperature of 0.8, as it
 of size k to contain at least one correct solution. To evaluate maximizes the number of examples for which at least one
 TiCoder, we define the metric pass@k@m to denote the ranked correct code is produced within 100 suggestions for k > 1
 pass@k for the code suggestions after m ≥ 1 user queries. in pass@k. To account for the non-determinism of the LLM
 Recall that TiCoder outputs a ranked list of code suggestions, 2 Access to this model was removed to the public by OpenAI in March 2023,
 so pass@k@m measures if any of the top k code suggestions but continues to be made free and available to researchers upon request.
 11
 Baseline T I C ODER -PASS FAIL T I C ODER -O UTPUT
 Dataset Model pass@k pass@1@m pass@1@m
 1 100 1 2 3 4 5 1 2 3 4 5
 text-davinci-003 49.16 86.88 68.04 75.26 77.33 77.88 78.08 77.00 82.20 83.38 83.59 83.75
 MBPP
 code-davinci-002 48.25 89.75 68.42 76.21 79.37 81.18 81.97 76.97 85.51 87.10 87.56 87.71
 CodeGen-6B 14.85 69.55 28.62 37.91 45.18 49.97 53.67 39.64 54.01 62.34 65.30 66.56
 CodeGen2.5-7B 28.32 84.74 50.27 59.70 65.02 67.84 69.58 62.78 73.84 78.10 79.52 80.42
 GPT-3.5-turbo 61.91 84.77 75.12 77.31 78.21 79.04 79.03 78.24 80.86 81.06 81.76 81.78
 GPT-4-turbo 69.80 86.88 80.71 81.90 82.38 83.20 83.12 83.91 84.63 84.97 85.65 85.65
 GPT-4-32k 67.13 87.35 81.56 82.62 82.97 83.11 83.70 84.78 85.28 85.31 85.40 85.79
 text-davinci-003 44.13 87.80 60.70 67.54 71.41 72.18 72.81 65.02 75.48 78.04 79.34 80.18
 HumanEval
 code-davinci-002 30.49 91.49 51.66 62.65 70.30 73.11 74.37 57.25 74.5 81.99 83.70 84.50
 CodeGen-6B 11.41 43.55 15.32 19.29 24.64 28.11 29.56 26.34 32.81 39.08 44.23 48.12
 CodeGen2.5-7B 21.39 76.21 32.82 41.03 46.51 49.47 52.33 35.86 51.60 61.54 65.02 68.25
 GPT-3.5-turbo 59.45 89.02 73.16 76.48 77.01 77.75 79.22 73.44 76.60 78.45 78.45 79.51
 GPT-4-turbo 62.62 89.63 78.36 80.42 80.92 80.84 81.34 82.22 83.17 83.42 83.62 83.84
 GPT-4-32k 60.72 89.02 76.10 78.43 79.07 79.48 79.49 81.37 82.46 82.49 82.49 82.54
TABLE IV: Model baseline and TiCoder results for two python datasets: MBPP and HumanEval. User interaction results are
simulated for up to m=5 test evaluation interactions. We highlight, in blue, the highest accuracy in each column.
generations, for each dataset, we only query each model once code suggestion within 100 suggestions. The second and
to generate an initial set of 100 code and 50 test suggestions third columns contain the results for each model, augmented
into a cache of responses. We use the same cache across all with TiCoder in T I C ODER -PASS FAIL and T I C ODER -O UTPUT
experiments that involve the specific LLM. settings respectively. We report the pass@1@m metric, with
 m, the number of test-validation user interactions, ranging
D. Simulating User Response
 from 1 to 5. We report pass@k@m only for the case of
 Our proposed workflow requires real-time user response to k = 1 as it is the strictest setting for assessing the impact
determine if a generated test is consistent with the user’s intent. of TiCoder. TiCoder improves the accuracy of pass@k@m for
Therefore, in order to evaluate T I C ODER offline with large- higher values of k as well, but we do not present them in the
scale benchmark datasets, we define a proxy to simulate real- interest of space.
time user response. All three chat models, GPT-3.5-turbo, GPT-4-turbo and
 Similar to oracle-guided inductive synthesis [15], [29], [28], GPT-4-32k demonstrate the highest accuracy for pass@1
we use the reference implementation bp as an oracle to answer with comparable performance across datasets. As expected,
if a test (i, o) is consistent with the user intent, and provide the text-davinci-003 and code-davinci-002, the two
expected output bp (i) when the test output o does not match largest completion models, achieve the fourth and fifth baseline
the user intent (for T I C ODER -O UTPUT). In other words, we performance on both datasets. However, code-davinci-002
assume that the intent of the user is precisely captured by the achieves the highest pass@100 across all models and both
semantics of the (hidden) reference implementation. Further, datasets.
if a test input crashes the reference code, we treat the user Overall, we observe that both TiCoder in the T I C ODER -
response as U NDEFINED to model a precondition violation. PASS FAIL and T I C ODER -O UTPUT settings significantly im-
However, this models an idealized user interaction because, in prove pass@1 performance, across all models. As the number
practice, users may sometimes be unable to answer a test query of test validation queries increase from m = 1 to m = 5 we
in a reasonable amount of time (say, when asked about the also observe consistent improvement in pass@1 performance.
value of the 100th prime number). As observed in the results Although the improvement is most pronounced at m = 1,
of the user study, unlike an idealized user, real participants compared to baseline.
may sometimes provide noisy input. For example, we observe For example, on MBPP, T I C ODER -PASS FAIL improves
that participants are more prone to making mistakes while pass@1 baseline performance of text-davinci-003 from
providing test outputs that dealt with edge cases. Therefore, 49.16% to 68.04%, an absolute improvement of 18.88% within
using the oracle as a proxy indicates that our empirical one user query. T I C ODER -O UTPUT improves performance
evaluation represents an upper bound on the improvement that to 77.00%, which is an absolute pass@1 improvement of
TiCoder can have on the benchmarks with real users. 27.84% within one user query. This increases to 38.55%
E. Results with 5 queries. While smaller models achieve lower pass@1
 To answer RQ2, we evaluate the performance of four and pass@100 accuracy, TiCoder still provides modest boosts
different models, with and without TiCoder in the T I C ODER - in accuracy. For the worst performing model, CodeGen-6B
PASS FAIL and T I C ODER -O UTPUT settings on MBPP and on HumanEval, T I C ODER -PASS FAIL provides an absolute
HumanEval datasets. Table IV contains all results for each pass@1 improvement of 3.91% within one interaction, and
model. T I C ODER -O UTPUT provides an absolute improvement of
 The first column contains the baseline pass@1 and 14.93%.
pass@100 for each model on MBPP and HumanEval In fact, we observe that T I C ODER can boost code generation
datasets. Note that pass@100 denotes the fraction of ex- accuracy of smaller models to comparable performance of
amples for which an LLM generates at least one correct
 12
much larger SOTA LLMs. For example, after just one user possible code suggestions, providing a concrete mechanism
interaction code-davinci-002 on MBPP achieves 68.42% for identifying potential ambiguities in natural language used
accuracy in the T I C ODER -PASS FAIL setting, which is in fact to prompt LLMs. Furthermore, recent work has shown that
higher than the pass@1 accuracy of all three SOTA chat developers spend significant amount of time verifying code
models: GPT-4-32k, GPT-4-turbo, and GPT-3.5-turbo. suggestions [34][14]. While we do not observe a statistically
 Finally, as expected T I C ODER -O UTPUT consistently pro- significant impact on the time taken to evaluate AI-generated
vides higher accuracy compared to T I C ODER -PASS FAIL, code suggestions when using T I C ODER, we do observe a
since the former allows users to fix the incorrect test output. significant reduction in the amount of cognitive effort required.
T I C ODER -O UTPUT achieves an average absolute improve- We hypothesize that tests, which provide tangible artifacts
ment of 45.73% in the code generation accuracy for both for developers to reason about the code, can serve as a
datasets and across all LLMs within 5 user interactions. facilitating mechanism for constructing mental models of code
However, it is worth noting that T I C ODER -PASS FAIL, even functionality. Ultimately, this supports developers in the task
with its lightweight feedback (that generalizes to richer tests of code evaluation. Future work should explore this in more
or specifications), always stays within 9% of the benefits of detail.
T I C ODER -O UTPUT. This demonstrates the power of LLMs to
generate test cases that satisfy user intent. B. Improving LLM code generation capabilities with verified
 Key Findings TiCoder significantly improves pass@1 test cases
 performance for all studied LLMs on both benchmarks, with Results of our benchmark evaluation indicate that, across
 performance improvements increasing with every test val- all models studied, both implementations of T I C ODER,
 idation interaction. TiCoder can boost small model perfor- T I C ODER -PASS FAIL and T I C ODER -O UTPUT, can be used to
 mance within one user interaction, outperforming pass@1 augment the accuracy of an LLM through improved ranking
 accuracy of larger models like GPT-4-32k. Additionally, and pruning. Specifically, we observe that using tests to better
 the lightweight T I C ODER -PASS FAIL scenario always stays constrain the space of possible code suggestions can improve
 within 9% of the performance of T I C ODER -O UTPUT even pass@k accuracy. This highlights the fact that current LLM ca-
 in this idealized simulated user setting. pabilities may not be fully realized in practice: when prompted
 for multiple code suggestions, LLMs often are capable of
 VIII. D ISCUSSION generating a correct answer, but mechanisms to better rank
A. Tests as a developer-AI disambiguation mechanism the set of suggestions is needed. However, the performance
 Results of our user study indicate that using tests as an boost provided by T I C ODER is contingent on a set of high
interactive mechanism to formalize user intent, and then prune quality tests used by discriminative test ranking policy
and rank AI generated code suggestions, can meaningfully (Sec. IV).
improve programmer performance. Results show that both As- If the underlying LLM is unable to generate high quality
sistant 2 (T I C ODER -PASS FAIL) and Assistant 3 (T I C ODER - tests, the ranking and pruning mechanism may not be as
O UTPUT) are statistically distinguishable from Assistant 1 (the helpful. Future work should explore more sophisticated mech-
control condition without T I C ODER), where no interactive anisms for generating high quality tests that capture important
test case verification or code pruning is used. Participants specifications about the code. In this work, we explore the
using Assistant 2 are significantly more likely to correctly user study scenario where T I C ODER prunes away some, but
evaluate AI generated code suggestions, and report reduced not all of the AI generated code suggestions.
task induced cognitive load, without negative impact on time It is worth noting that if the code suggestions generated
to complete each task. However, compared to Assistant 2, by the underlying LLM predominantly exhibit consistent be-
participants made more mistakes when validating tests with havior, T I C ODER can still be valuable to a user by providing
Assistant 3. meaningful tests alongside the code suggestions. For example,
 Further research to explore a trade-off between the ap- in a scenario where all of the suggestions are correct with
proaches, in practice, should be considered. However, we find respect to the user’s intent, T I C ODER may not prune away
that surfacing test cases in both forms might serve as a helpful any of the code suggestions, but provides some guarantees
mechanism for which to reason about generated code. While about program behaviour to the user.
it is true that correctness likely depends on the evaluation
strategies used by each participant, participants that were C. The Value of Execution Based Pruning
shown test cases by the AI Assistants performed significantly
better. Tests in prompt
 T I C ODER -
 Recent work has shown that current developer-AI inter- Dataset Model PASS FAIL Single (pass@k) All (pass@k)
action workflows, as simulated by Assistant 1 in our study, pass@1@1 k=1 k=5 k=1 k=5
have raised new issues in the way that developers write code. MBPP GPT-4-32k 81.56 78.26 87.81 80.88 91.58
Results suggest a need for interaction mechanisms that can HumanEval GPT-4-32k 76.10 65.25 81.37 70.39 86.99
support disambiguation; a critical feature of the usability of
 TABLE V: Results of prompting GPT-4 with validation tests
AI-Assistants [31], [32]. We observed how T I C ODER can
surface a ranked list of tests that delineate the space of in the prompt
 13
 The T I C ODER workflow helps users by automatically gen- 9 else:
erating and ranking interesting test cases, instead of requiring 10 None
 11 return n1/(n-n1)
the user to manually write them. However, users may have
a set of test cases already in mind when querying a LLM.
 The following test is ranked highest by the discriminative
We explore how such a scenario compares to the T I C ODER
 ranking strategy:
workflow by adding the set of validation tests, i.e. the ground
truth test set provided in each dataset, to the code generation 1 assert zero_count([]) == 0, "Empty List"
prompt. We instruct GPT-4-32k to generate a code suggestion
that passes on the set of validation tests provided in the For this test, out of the (deduplicated) 80 code suggestions
prompt. We then evaluate the pass@k accuracy at k = 1 and from code-davinci-002, 8 suggestions pass the test, 11
k = 5 and compare to the T I C ODER pass@1@m accuracy suggestions fail the test and 61 suggestions crash on this
from Table IV. Table V contains the result of this experiment, test. The score for this test is 8/11 = 0.73, which is the
showing both experiments where a single test is added in the highest among all tests. However, this test does not lead to
prompt, as well as an experiment where all available validation any code pruning as the user responds U NDEFINED in both
tests are added in the prompt, the exact number of tests varies the T I C ODER -PASS FAIL and T I C ODER -O UTPUT scenarios
across both datasets. since the empty array causes the reference implementation
 On both MBPP and HumanEval we observe a boost in above to fail. Thus, our results in RQ2 account for tests
pass@k accuracy over the baseline prompt used Table IV. with U NDEFINED responses, reflecting the possible real world
For example, on MBPP GPT-4-32k achieves a pass@1 of impact of pre-condition violating tests on the accuracy boost
67.13% with the baseline prompt (no tests) and 78.26% when provided by TiCoder.
including a single test in the prompt. This increases to a
pass@1 of 80.88% when all tests are added in the prompt. IX. L IMITATIONS AND T HREATS
As expected, this demonstrates that adding tests in the prompt Generalizability of user study results. We evaluate
does help improve model performance. However, recalling the T I C ODER under highly controlled experimental conditions,
pass@1@1 accuracy of the T I C ODER -PASS FAIL, within one and the ability of developers to validate tests in more com-
user feedback loop, accuracy reaches 81.56%, out performing plex code generation scenarios may not scale. Our study
the pass@1 accuracy where a single test is included in the explores two distinct test validation mechanisms surfaced in
prompt by 3.31%. T I C ODER even performs slightly better the T I C ODER workflow: T I C ODER -PASS FAIL and T I C ODER -
(0.68%) compared to the case when all tests are in the prompt. O UTPUT. On the selected tasks, we observe that, in general,
 This indicates that even if the user supplies all test, there participants were able to successfully evaluate tests in both
is no guarantee that the underlying LLM will fulfill the interaction scenarios. However, in practice specifying the out-
user intent and generate a code suggestion that passes on put of generated tests may not always be a straightforward or
the tests. Conversely, with only one user interaction on a simple task. In addition, we restrict participants abilities to edit
highly distinguishing test, obtained by ranking LLM generated the code prompt and code suggestions, to control for variables
tests, code generation accuracy greatly improves, matching the across participants. However, this is not a true reflection of
scenario where several tests are provided to the LLM without real-world interaction behaviours. Future work should explore
the added burden on the user to manually come up with test the impact of T I C ODER on developer productivity in real-
cases. world code settings, with broader audiences. In addition,
 we only explored how T I C ODER impacts the correctness of
D. Considerations for AI-Generated Tests: Precondition Vio- code evaluation, i.e. how well users can disambiguate code
lations suggestions. For example, a future experiment might examine
 Tests generated by LLMs may contain pre-condition vio- how T I C ODER impacts online metrics such as code acceptance
lating inputs that would cause the reference implementation rates, or the total proportion of code contributed by the
to crash or fail, and would result in a U NDEFINED response AI system, accommodating for solutions that provide partial
from the user, resulting in no pruning of code. correctness.
 As an illustrative case, consider from MBPP, the example Generalization of benchmark evaluation results. We also
of a reference implementation with (implicit) precondition empirically evaluate T I C ODER using two popular and state-of-
that the argument nums array is non-empty, and throws a the-art research Python benchmarks for code generation tasks:
divisionByZero at the return statement for an empty MBPP and HumanEval. While both benchmarks exercise
nums array. common programming patterns, they may not be representative
 of real-world software development. Our findings may not
1 from array import array generalize to a different set of programs across different
2 def zero_count(nums):
3 """Write a function to find the ratio of zeroes languages and problem domains.
 to non-zeroes in an array of integers.""" Test execution overhead. The proposed T I C ODER work-
4 n = len(nums) flow incurs the cost of additional LLM inference, to generate
5 n1 = 0
6 for x in nums: candidate tests, as well as resource costs related to execut-
7 if x == 0: ing tests for generated code suggestions. Cost of execution
8 n1 += 1 may be non-trivial, and might not scale in scenarios where
 14
users wish to use an AI assistant to generate complex code. [7] A. Ziegler, E. Kalliamvakou, X. A. Li, A. Rice, D. Rifkin, S. Simister,
Nevertheless, the potential reliability guarantees and reduced G. Sittampalam, and E. Aftandilian, “Productivity assessment of
 neural code completion,” in MAPS@PLDI 2022: 6th ACM SIGPLAN
effort for code verification represent a valuable trade-off when International Symposium on Machine Programming, San Diego, CA,
weighed against the costs of inference and execution in real- USA, 13 June 2022, S. Chaudhuri and C. Sutton, Eds. ACM, 2022, pp.
world scenarios. Future work should examine practical use of 21–29. [Online]. Available: https://doi.org/10.1145/3520312.3534864
 [8] J. T. Liang, C. Yang, and B. A. Myers, “Understanding the usability of
T I C ODER at scale. ai programming assistants,” arXiv preprint arXiv:2303.17125, 2023.
 [9] F. F. Xu, B. Vasilescu, and G. Neubig, “In-ide code generation from
 natural language: Promise and challenges,” ACM Transactions on Soft-
 X. C ONCLUSION ware Engineering and Methodology (TOSEM), vol. 31, no. 2, pp. 1–47,
 In this work, we propose the workflow of test-driven interac- 2022.
 [10] J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan,
tive code generation using LLMs, and study it’s effectiveness E. Jiang, C. Cai, M. Terry, Q. Le et al., “Program synthesis with large
through a user study and empirical evaluation on code gen- language models,” arXiv preprint arXiv:2108.07732, 2021.
eration benchmarks. Our findings provide encouraging results [11] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin,
 C. Zhang, S. Agarwal, K. Slama, A. Ray et al., “Training language
around guiding user intent clarification for generating more models to follow instructions with human feedback,” Advances in Neural
correct programs. Information Processing Systems, vol. 35, pp. 27 730–27 744, 2022.
 In future work, we plan to extend and evaluate our im- [12] O. Asare, M. Nagappan, and N. Asokan, “Is github’s copilot as bad
 as humans at introducing vulnerabilities in code?” arXiv preprint
plementation reflecting real-world scenarios including: more arXiv:2204.04741, 2022.
complex programs, an in-situ user study for various software [13] N. Perry, M. Srivastava, D. Kumar, and D. Boneh, “Do users write more
development tasks, and an empirical evaluation on realistic insecure code with ai assistants?” arXiv preprint arXiv:2211.03622,
 2022.
benchmarks such as CoderEval [47] and NL2Fix [43]. Finally, [14] C. Bird, D. Ford, T. Zimmermann, N. Forsgren, E. Kalliamvakou,
we plan to explore if T I C ODER can be extended to richer T. Lowdermilk, and I. Gazit, “Taking flight with copilot: Early in-
forms of formal specifications beyond tests, such as property sights and opportunities of ai-powered pair-programming tools,” Queue,
 vol. 20, no. 6, pp. 35–57, 2022.
based tests or pre- and post-conditions generated from user- [15] S. Jha, S. Gulwani, S. A. Seshia, and A. Tiwari, “Oracle-guided
defined prompts [48]. component-based program synthesis,” in Proceedings of the 32nd
 ACM/IEEE International Conference on Software Engineering - Volume
 1, ICSE 2010, Cape Town, South Africa, 1-8 May 2010, J. Kramer,
 R EFERENCES J. Bishop, P. T. Devanbu, and S. Uchitel, Eds. ACM, 2010, pp.
 [1] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, 215–224. [Online]. Available: https://doi.org/10.1145/1806799.1806833
 H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, [16] T. Lau, “Why programming-by-demonstration systems fail: Lessons
 G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, learned for usable ai,” AI Magazine, vol. 30, no. 4, pp. 65–65, 2009.
 S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, [17] T. Zhang, L. Lowmanstone, X. Wang, and E. L. Glassman, “Interactive
 C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, program synthesis by augmented examples,” in Proceedings of the 33rd
 E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, Annual ACM Symposium on User Interface Software and Technology,
 J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, 2020, pp. 627–648.
 A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, [18] C. Lemieux, J. P. Inala, S. K. Lahiri, and S. Sen, “Codamosa: Escaping
 M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, coverage plateaus in test generation with pre-trained large language
 B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba, models,” in 45th International Conference on Software Engineering, ser.
 “Evaluating large language models trained on code,” 2021. [Online]. ICSE, 2023.
 Available: https://arxiv.org/abs/2107.03374 [19] E. Dinella, G. Ryan, T. Mytkowicz, and S. Lahiri, “Toga: A neural
 [2] A. Chowdhery, S. Narang, J. Devlin, M. Bosma, G. Mishra, method for test oracle generation,” in ICSE 2022. ACM, May
 A. Roberts, P. Barham, H. W. Chung, C. Sutton, S. Gehrmann, 2022. [Online]. Available: https://www.microsoft.com/en-us/research/
 P. Schuh, K. Shi, S. Tsvyashchenko, J. Maynez, A. Rao, P. Barnes, publication/toga-a-neural-method-for-test-oracle-generation/
 Y. Tay, N. Shazeer, V. Prabhakaran, E. Reif, N. Du, B. Hutchinson, [20] M. Schäfer, S. Nadi, A. Eghbali, and F. Tip, “Adaptive test generation
 R. Pope, J. Bradbury, J. Austin, M. Isard, G. Gur-Ari, P. Yin, using a large language model,” arXiv preprint arXiv:2302.06527, 2023.
 T. Duke, A. Levskaya, S. Ghemawat, S. Dev, H. Michalewski, [21] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond,
 X. Garcia, V. Misra, K. Robinson, L. Fedus, D. Zhou, D. Ippolito, T. Eccles, J. Keeling, F. Gimeno, A. D. Lago, T. Hubert, P. Choy,
 D. Luan, H. Lim, B. Zoph, A. Spiridonov, R. Sepassi, D. Dohan, C. d. M. d’Autume, I. Babuschkin, X. Chen, P.-S. Huang, J. Welbl,
 S. Agrawal, M. Omernick, A. M. Dai, T. S. Pillai, M. Pellat, S. Gowal, A. Cherepanov, J. Molloy, D. J. Mankowitz, E. S.
 A. Lewkowycz, E. Moreira, R. Child, O. Polozov, K. Lee, Z. Zhou, Robson, P. Kohli, N. de Freitas, K. Kavukcuoglu, and O. Vinyals,
 X. Wang, B. Saeta, M. Diaz, O. Firat, M. Catasta, J. Wei, “Competition-level code generation with alphacode,” 2022. [Online].
 K. Meier-Hellstern, D. Eck, J. Dean, S. Petrov, and N. Fiedel, “Palm: Available: https://arxiv.org/abs/2203.07814
 Scaling language modeling with pathways,” 2022. [Online]. Available: [22] B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J.-G. Lou, and
 https://arxiv.org/abs/2204.02311 W. Chen, “Codet: Code generation with generated tests,” 2022.
 [3] E. Nijkamp, B. Pang, H. Hayashi, L. Tu, H. Wang, Y. Zhou, [Online]. Available: https://arxiv.org/abs/2207.10397
 S. Savarese, and C. Xiong, “A conversational paradigm for program [23] S. Gulwani, O. Polozov, and R. Singh, “Program synthesis,” Found.
 synthesis,” 2022. [Online]. Available: https://arxiv.org/abs/2203.13474 Trends Program. Lang., vol. 4, no. 1-2, pp. 1–119, 2017. [Online].
 [4] D. Fried, A. Aghajanyan, J. Lin, S. Wang, E. Wallace, F. Shi, R. Zhong, Available: https://doi.org/10.1561/2500000010
 W.-t. Yih, L. Zettlemoyer, and M. Lewis, “Incoder: A generative [24] A. Solar-Lezama, “The sketching approach to program synthesis,” in
 model for code infilling and synthesis,” 2022. [Online]. Available: Programming Languages and Systems, Z. Hu, Ed. Berlin, Heidelberg:
 https://arxiv.org/abs/2204.05999 Springer Berlin Heidelberg, 2009, pp. 4–13.
 [5] F. F. Xu, U. Alon, G. Neubig, and V. J. Hellendoorn, “A systematic [25] S. Gulwani, “Automating string processing in spreadsheets
 evaluation of large language models of code,” in Proceedings using input-output examples,” in PoPL’11, January 26-
 of the 6th ACM SIGPLAN International Symposium on Machine 28, 2011, Austin, Texas, USA, January 2011. [Online].
 Programming, ser. MAPS 2022. New York, NY, USA: Association Available: https://www.microsoft.com/en-us/research/publication/
 for Computing Machinery, 2022, p. 1–10. [Online]. Available: automating-string-processing-spreadsheets-using-input-output-examples/
 https://doi.org/10.1145/3520312.3534862 [26] N. Jain, S. Vaidyanath, A. Iyer, N. Natarajan, S. Parthasarathy,
 [6] GitHub, “Github copilot,” 2022, accessed August 5, 2022. https://github. S. Rajamani, and R. Sharma, “Jigsaw: Large language
 com/features/copilot/. models meet program synthesis,” in International Confer-
 ence on Software Engineering (ICSE), May 2022. [On-
 line]. Available: https://www.microsoft.com/en-us/research/publication/
 jigsaw-large-language-models-meet-program-synthesis/
 15
[27] K. Rahmani, M. Raza, S. Gulwani, V. Le, D. Morris, A. Radhakrishna, [37] S. Imai, “Is github copilot a substitute for human pair-programming? an
 G. Soares, and A. Tiwari, “Multi-modal program inference: a marriage empirical study,” in Proceedings of the ACM/IEEE 44th International
 of pre-trained language models and component-based synthesis,” Proc. Conference on Software Engineering: Companion Proceedings, 2022,
 ACM Program. Lang., vol. 5, no. OOPSLA, pp. 1–29, 2021. [Online]. pp. 319–321.
 Available: https://doi.org/10.1145/3485535 [38] J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan,
[28] S. Jha and S. A. Seshia, “A theory of formal synthesis via inductive E. Jiang, C. Cai, M. Terry, Q. Le, and C. Sutton, “Program
 learning,” Acta Informatica, vol. 54, no. 7, pp. 693–726, 2017. [Online]. synthesis with large language models,” 2021. [Online]. Available:
 Available: https://doi.org/10.1007/s00236-017-0294-5 https://arxiv.org/abs/2108.07732
[29] V. Le, D. Perelman, O. Polozov, M. Raza, A. Udupa, and S. Gulwani, [39] S. G. Hart and L. E. Staveland, “Development of nasa-tlx (task load
 “Interactive program synthesis,” arXiv preprint arXiv:1703.03539, 2017. index): Results of empirical and theoretical research,” in Advances in
[30] R. Ji, J. Liang, Y. Xiong, L. Zhang, and Z. Hu, “Question psychology. Elsevier, 1988, vol. 52, pp. 139–183.
 selection for interactive program synthesis,” in Proceedings of the 41st [40] S. G. Hart, “Nasa-task load index (nasa-tlx); 20 years later,” in Pro-
 ACM SIGPLAN Conference on Programming Language Design and ceedings of the human factors and ergonomics society annual meeting,
 Implementation, ser. PLDI 2020. New York, NY, USA: Association vol. 50, no. 9. Sage publications Sage CA: Los Angeles, CA, 2006,
 for Computing Machinery, 2020, p. 1143–1158. [Online]. Available: pp. 904–908.
 https://doi.org/10.1145/3385412.3386025 [41] Y. Benjamini and Y. Hochberg, “Controlling the false discovery rate:
[31] A. M. McNutt, C. Wang, R. A. Deline, and S. M. Drucker, “On the a practical and powerful approach to multiple testing,” Journal of the
 design of ai-powered code assistants for notebooks,” in Proceedings of Royal statistical society: series B (Methodological), vol. 57, no. 1, pp.
 the 2023 CHI Conference on Human Factors in Computing Systems, 289–300, 1995.
 2023, pp. 1–16. [42] T. X. Olausson, J. P. Inala, C. Wang, J. Gao, and A. Solar-Lezama,
[32] S. Barke, M. B. James, and N. Polikarpova, “Grounded copilot: How “Demystifying gpt self-repair for code generation,” arXiv preprint
 programmers interact with code-generating models,” Proceedings of the arXiv:2306.09896, 2023.
 ACM on Programming Languages, vol. 7, no. OOPSLA1, pp. 85–111, [43] S. Fakhoury, S. Chakraborty, M. Musuvathi, and S. K. Lahiri, “Towards
 2023. generating functionally correct code edits from natural language issue
[33] M. Mayer, G. Soares, M. Grechkin, V. Le, M. Marron, O. Polozov, descriptions,” arXiv preprint arXiv:2304.03816, 2023.
 R. Singh, B. Zorn, and S. Gulwani, “User interaction models for [44] E. Nijkamp, H. Hayashi, C. Xiong, S. Savarese, and Y. Zhou, “Code-
 disambiguation in programming by example,” in Proceedings of the gen2: Lessons for training llms on programming and natural languages,”
 28th Annual ACM Symposium on User Interface Software & Technology, arXiv preprint arXiv:2305.02309, 2023.
 2015, pp. 291–301. [45] R. Li, L. B. Allal, Y. Zi, N. Muennighoff, D. Kocetkov, C. Mou,
[34] H. Mozannar, G. Bansal, A. Fourney, and E. Horvitz, “Reading between M. Marone, C. Akiki, J. Li, J. Chim et al., “Starcoder: may the source
 the lines: Modeling user behavior and costs in ai-assisted programming,” be with you!” arXiv preprint arXiv:2305.06161, 2023.
 arXiv preprint arXiv:2210.14306, 2022. [46] B. Roziere, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi,
[35] P. Vaithilingam, T. Zhang, and E. L. Glassman, “Expectation vs. J. Liu, T. Remez, J. Rapin et al., “Code llama: Open foundation models
 experience: Evaluating the usability of code generation tools powered for code,” arXiv preprint arXiv:2308.12950, 2023.
 by large language models,” in Extended Abstracts of the 2022 CHI [47] H. Yu, B. Shen, D. Ran, J. Zhang, Q. Zhang, Y. Ma, G. Liang,
 Conference on Human Factors in Computing Systems, ser. CHI EA Y. Li, T. Xie, and Q. Wang, “Codereval: A benchmark of pragmatic
 ’22. New York, NY, USA: Association for Computing Machinery, code generation with generative pre-trained models,” arXiv preprint
 2022. [Online]. Available: https://doi.org/10.1145/3491101.3519665 arXiv:2302.00288, 2023.
[36] N. Nguyen and S. Nadi, “An empirical evaluation of github copilot’s [48] M. Endres, S. Fakhoury, S. Chakraborty, and S. K. Lahiri, “Formalizing
 code suggestions,” in Proceedings of the 19th International Conference natural language intent into program specifications via large language
 on Mining Software Repositories, 2022, pp. 1–5. models,” arXiv preprint arXiv:2310.01831, 2023.
