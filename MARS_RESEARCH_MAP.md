# MARS — Machine-Agent Revenue Science

## Complete Research Programme Map

**Author:** Kamran Khan  
**Experimental Programme:** Experiments 001–025  
**Research Domain:** Autonomous AI Agents, Machine-to-Machine Commerce, Buyer Intelligence, Commercial Decision Science

---

## 1. Overview

MARS — Machine-Agent Revenue Science — is an experimental AI research system designed to investigate how an autonomous AI supplier can reason about, diagnose, negotiate with, and adapt to autonomous machine buyers whose internal purchasing policies are not directly observable.

The research programme consists of **25 sequential experiments**.

Rather than treating autonomous purchasing as a conventional prediction problem, MARS models machine-to-machine commerce as a partially observable commercial intelligence problem.

The supplier cannot directly inspect the buyer's internal procurement rules.

Instead, it must learn from observable behaviour.

MARS progressively investigates whether an AI supplier can:

- interact with autonomous buyers;
- infer hidden purchasing constraints;
- discover decision thresholds;
- optimise commercial proposals;
- reason about negotiation strategy;
- select informative commercial experiments;
- minimise the cost of policy discovery;
- operate under stochastic buyer behaviour;
- accumulate evidence adaptively;
- estimate latent buyer environments;
- select evidence policies dynamically;
- actively diagnose unfamiliar buyers;
- construct learned buyer world models;
- and determine whether continual online learning improves future commercial intelligence.

The complete programme progresses from basic black-box policy inference toward increasingly autonomous commercial reasoning.

---

# 2. Central Research Question

## Primary Research Question

**How can an AI supplier learn to make commercially effective decisions when interacting with autonomous purchasing agents whose internal decision policies, thresholds, uncertainty and behavioural environments are hidden?**

This question creates several subsidiary research problems.

An autonomous supplier may need to determine:

1. What constraints govern the buyer's purchasing decision?
2. Where are the buyer's hidden decision thresholds?
3. Which commercial variable caused a rejection?
4. What is the minimum intervention required to make a proposal acceptable?
5. Which experiment should be performed next?
6. How much commercial cost or risk should be accepted to obtain information?
7. How should evidence be interpreted when buyer behaviour is stochastic?
8. When should evidence collection stop?
9. Which evidence strategy is appropriate for a particular buyer environment?
10. Can the buyer's behavioural environment itself be inferred?
11. Can historical interactions be transformed into a learned buyer world model?
12. Should that world model continue learning after deployment?

These questions form the experimental progression of MARS.

---

# 3. Fundamental MARS Problem

The fundamental MARS interaction can be represented as:

```text
AUTONOMOUS SUPPLIER
        │
        │ Commercial Proposal
        ▼
AUTONOMOUS BUYER
        │
        │ Observable Decision
        ▼
ACCEPT / REJECT
        │
        ▼
SUPPLIER INFERENCE
        │
        ▼
What hidden buyer policy
could have produced this behaviour?
```

The supplier does not initially receive direct access to the buyer's private decision policy.

It must recover useful commercial intelligence from interaction.

This makes the problem fundamentally different from ordinary supervised prediction.

The supplier is simultaneously attempting to:

- learn the buyer;
- decide what evidence to collect;
- control the cost of experimentation;
- manage uncertainty;
- and choose commercially useful actions.

---

# 4. Research Evolution

The 25 MARS experiments can be organised into five major research layers.

```text
LAYER I
Hidden Buyer Policy Discovery
Experiments 001–005

        ↓

LAYER II
Commercial Intervention & Negotiation
Experiments 006–012

        ↓

LAYER III
Active Policy Discovery
Experiments 013–017

        ↓

LAYER IV
Stochastic Buyer Intelligence
Experiments 018–020

        ↓

LAYER V
Autonomous Environment Intelligence
Experiments 021–025
```

Each layer increases the autonomy and difficulty of the commercial intelligence problem.

---

# 5. Layer I — Hidden Buyer Policy Discovery

## Experiments 001–005

The first research layer establishes the autonomous buyer laboratory and the fundamental black-box inference problem.

The buyer contains hidden commercial constraints.

These may include variables such as:

- maximum annual price;
- maximum contract duration;
- minimum service availability;
- minimum supplier reliability;
- minimum payment terms.

The supplier does not receive these constraints directly during policy-discovery experiments.

Instead, it submits commercial proposals and observes buyer decisions.

The central problem becomes:

> Can hidden commercial purchasing policies be reconstructed from observable buyer behaviour?

### Core Concepts Introduced

- autonomous buyer simulation;
- black-box decision making;
- commercial proposal evaluation;
- hidden procurement constraints;
- accept/reject behaviour;
- commercial probing;
- buyer policy inference;
- threshold discovery.

### Research Significance

This layer establishes the central MARS assumption:

> Commercial intelligence must be recovered from behaviour rather than direct access to the buyer's private decision rules.

This foundation enables all later experiments.

---

# 6. Layer II — Commercial Intervention and Negotiation

## Experiments 006–012

Once hidden buyer constraints can be approximated, MARS moves beyond passive policy discovery.

The research question changes from:

```text
"What does the buyer require?"
```

to:

```text
"What should the supplier do about it?"
```

The system therefore begins investigating commercially actionable reasoning.

### Research Themes

- minimum-cost commercial intervention;
- proposal optimisation;
- negotiation reasoning;
- buyer policy drift;
- deal rescue;
- commercial learning;
- adversarial negotiation;
- AI supplier strategy;
- evidence-based negotiation.

MARS begins using inferred buyer knowledge to determine how commercial proposals should change.

This creates the transition from:

```text
INFERENCE
```

to:

```text
INFERENCE
    +
DECISION
    +
COMMERCIAL ACTION
```

### Research Significance

The supplier is no longer simply attempting to understand the buyer.

It begins reasoning strategically about how to respond to the buyer.

This transforms MARS from a passive inference framework into an active commercial decision system.

---

# 7. Layer III — Active Policy Discovery

## Experiments 013–017

The third research layer introduces a major change.

Earlier policy-discovery systems can execute predetermined commercial tests.

MARS now investigates whether the AI itself can decide:

> Which commercial experiment should I perform next?

This introduces active experimentation.

---

## Experiment 013 — Active Buyer Policy Discovery

MARS introduces active query selection.

Instead of blindly evaluating proposals, the system chooses experiments according to their potential informational value.

The experiment demonstrated complete discovery of the tested buyer policy using **58 buyer queries**.

The recovered policy closely approximated the simulated hidden thresholds.

This establishes the principle that policy discovery can itself become an autonomous decision problem.

---

## Experiment 014 — Comparative Policy Discovery Benchmark

The active approach is compared with a fixed inference strategy.

The benchmark produced:

```text
Fixed inference:
73 buyer queries

Autonomous active selection:
58 buyer queries
```

This represents approximately:

```text
20.55% fewer buyer queries
```

while maintaining complete policy coverage in the tested environment.

The result demonstrates that intelligent experiment selection can reduce the interaction burden required for policy discovery.

---

## Experiment 015 — Advanced Active Discovery

The active discovery architecture is extended further.

The objective is no longer simply to recover hidden constraints.

MARS increasingly reasons about the value of different commercial experiments before executing them.

This contributes to the transition toward autonomous experimental design.

---

## Experiment 016 — Cost-Aware Commercial Experimentation

Information is not commercially free.

A highly informative proposal may expose the supplier to greater commercial cost or risk.

Experiment 016 therefore introduces cost-aware experimentation.

The system considers both:

```text
INFORMATION VALUE
```

and:

```text
COMMERCIAL COST / RISK
```

when selecting commercial probes.

Key experimental measurements included:

```text
Buyer Queries: 57
Resolved Variables: 5
Policy Coverage: 100%
Queries per Discovered Policy: 11.4
Total Modelled Probe Cost: £2,100
Average Modelled Probe Cost: £36.84
Maximum Single Probe Cost: £1,800
Average Commercial Risk: 0.12057
```

The experiment demonstrates that active commercial intelligence can be formulated as a trade-off between learning value and commercial exposure.

---

## Experiment 017 — Multi-Buyer Generalisation

MARS is then tested across multiple buyer configurations.

Different experimental strategies are compared.

The fixed strategy fails to generalise completely across the tested buyer environments.

More adaptive approaches achieve complete policy discovery across the evaluated buyers.

This experiment demonstrates that a discovery strategy effective against one buyer configuration may not automatically generalise to others.

### Layer III Research Contribution

Experiments 013–017 establish a new MARS objective:

> Recover hidden buyer policies using fewer, more informative and more commercially efficient interactions.

---

# 8. Layer IV — Stochastic Buyer Intelligence

## Experiments 018–020

Earlier experiments largely assume that buyer responses provide reliable evidence.

Real autonomous systems may not behave deterministically.

Buyer decisions may contain stochasticity arising from:

- probabilistic policies;
- changing internal states;
- uncertainty;
- model sampling;
- external conditions;
- incomplete information.

MARS therefore introduces stochastic buyer behaviour.

Now:

```text
SAME PROPOSAL
      │
      ▼
MAY NOT ALWAYS PRODUCE
THE SAME OBSERVED DECISION
```

This fundamentally changes the inference problem.

---

## Experiment 018 — Repeated Evidence Under Stochastic Behaviour

Experiment 018 investigates whether repeated observations can reduce inference error.

Results included:

```text
Single Observation Architecture

Total Evaluations: 60
Noise Events: 6
Realised Noise: 0.10
Policy Coverage: 100%
Mean Normalised Error: ~0.01221
```

Compared with:

```text
Repeated Evidence Architecture

Total Evaluations: 483
Noise Events: 43
Realised Noise: ~0.08903
Policy Coverage: 100%
Mean Normalised Error: ~0.00001068
```

The repeated-evidence architecture achieved approximately:

```text
99.91% relative error reduction
```

in the tested environment.

### Finding

Repeated evidence can dramatically improve threshold estimation under stochastic buyer behaviour.

However, it requires substantially more buyer interactions.

That creates the next problem:

> Can MARS obtain the robustness of repeated evidence without paying its full query cost?

---

# 9. Experiment 019 — Adaptive Sequential Evidence

Experiment 019 introduces adaptive sequential evidence collection.

Rather than collecting a fixed number of observations for every candidate proposal, MARS evaluates evidence sequentially.

When sufficient evidence has accumulated, sampling can stop.

Results included:

```text
Fixed Repeated-Evidence Queries: 483
Adaptive Sequential Queries: 267
Queries Saved: 216
Query Reduction: 44.72%
```

The adaptive system maintained approximately the same mean normalised error as the repeated-evidence architecture.

It also achieved:

```text
Adaptive Early Stop Rate: 91.18%
Average Observations per Candidate: ~3.88
```

### Finding

MARS does not need to spend an identical evidence budget on every commercial hypothesis.

Evidence acquisition itself can be adaptive.

---

# 10. Experiment 020 — Statistical Robustness

Experiment 020 expands evaluation across:

```text
20 random seeds
×
6 stochastic noise levels
×
3 inference architectures
=
360 discovery runs
```

covering:

```text
120 simulated buyer environments
```

Aggregate results included:

```text
Fixed Repeated Evidence
Mean Queries: ~483.06

Adaptive Sequential Evidence
Mean Queries: ~292.67

Mean Queries Saved: ~190.39
Mean Query Reduction: ~39.41%
```

Aggregate mean normalised errors were approximately:

```text
Fixed:
0.0008813

Adaptive:
0.0008154
```

However, results at individual high-noise conditions showed that fixed repeated evidence could sometimes achieve lower error.

### Important Interpretation

The correct conclusion is NOT:

```text
"Adaptive evidence is always more accurate."
```

Instead:

> Adaptive evidence substantially reduced average query requirements while maintaining competitive aggregate accuracy, but the relative accuracy of fixed and adaptive evidence varied across stochastic environments.

This result motivates environment-dependent strategy selection.

---

# 11. Layer V — Autonomous Environment Intelligence

## Experiments 021–025

The final research layer moves beyond individual buyer-policy inference.

MARS begins reasoning about the behavioural environment in which policy discovery occurs.

The question becomes:

> Can MARS learn how it should learn?

---

# 12. Experiment 021 — Autonomous Meta-Policy Learning

Experiment 021 introduces multiple evidence-collection policies.

Candidate strategies include:

```text
ECONOMICAL
BALANCED
ROBUST
HIGH_ASSURANCE
```

Each policy represents a different evidence-collection configuration.

The system evaluates these strategies across different stochastic environments and learns an environment-to-policy mapping.

The experiment used:

```text
15 training seeds
5 validation seeds
6 noise regimes
360 training runs
30 validation runs
390 total runs
```

Held-out validation achieved:

```text
Mean Policy Coverage: 100%
Mean Normalised Error: ~0.000584
Mean Validation Queries: 369.6
Failed Validation Runs: 0
```

The learned policy mapping was:

```text
0.05 → BALANCED
0.10 → BALANCED
0.15 → HIGH_ASSURANCE
0.20 → ROBUST
0.25 → HIGH_ASSURANCE
0.30 → ROBUST
```

### Important Finding

The mapping is not simply monotonic.

Increasing stochasticity does not produce a trivial progression from weaker to stronger evidence policies.

This supports learning the meta-policy rather than encoding a simplistic rule manually.

---

# 13. Experiment 022 — Latent Buyer Environment Identification

Experiment 021 assumes the environment is known when selecting the evidence policy.

Experiment 022 removes that assumption.

MARS must now:

```text
UNKNOWN BUYER
      │
      ▼
Diagnostic Interaction
      │
      ▼
Estimate Behavioural Environment
      │
      ▼
Select Learned Meta-Policy
      │
      ▼
Perform Policy Discovery
```

Across the completed experiment:

```text
Meta-Policy Training Runs: 240
Closed-Loop Test Runs: 30
Successful Runs: 30/30
Policy Coverage: 100%
```

The true simulator environment was not supplied to the estimator or controller during operational inference.

It was retained for evaluation.

This creates a more autonomous closed-loop system.

---

# 14. Experiment 023 — Active Diagnostic Intelligence

Experiment 022 used a relatively expensive fixed diagnostic process.

Experiment 023 asks:

> Can MARS determine which diagnostic evidence it needs and stop when it has enough?

The active diagnostic system sequentially evaluates buyer behaviour and determines whether additional diagnostic evidence is necessary.

Across 30 matched simulated buyer environments:

```text
Experiment 022 Mean Diagnostic Queries:
240

Experiment 023 Mean Diagnostic Queries:
~74.53

Mean Queries Saved:
~165.47

Diagnostic Query Reduction:
68.94%
```

Environment-estimation error also decreased:

```text
Experiment 022:
~0.17028

Experiment 023:
~0.03894
```

Oracle policy agreement changed from:

```text
Experiment 022:
60.00%

Experiment 023:
66.67%
```

Both systems maintained:

```text
100% final policy coverage
```

The active system's final normalised policy-discovery error remained similar to the fixed-diagnostic architecture.

Active stopping results included:

```text
CONFIDENT_AND_STABLE: 29
MAXIMUM_QUERY_BUDGET: 1
```

Thus approximately **96.67%** of runs stopped autonomously rather than reaching the maximum diagnostic-query ceiling.

### Finding

Active diagnostic intelligence substantially reduced the diagnostic interaction burden while preserving downstream policy-discovery coverage in the matched simulated benchmark.

---

# 15. Experiment 024 — Buyer World Model Learning

Experiment 024 introduces a learned buyer world model.

Instead of relying exclusively on manually specified environment inference at the final prediction layer, historical buyer interactions are converted into behavioural representations.

The world model uses nine behavioural features derived from diagnostic interactions.

The experimental dataset contained:

```text
Historical Training Episodes: 120
Held-Out Validation Episodes: 60
Total Buyer Episodes: 180
Environment Classes: 6
Behavioural Features: 9
```

Training and validation seeds were separated.

The model achieved:

```text
Held-Out Validation Runs: 60
Correct Environment Classifications: 27
Exact Classification Accuracy: 45.00%
Mean Absolute Environment Error: ~0.03776
Mean Prediction Confidence: ~0.61948
Mean Prediction Entropy: ~1.10670
Mean Diagnostic Queries: 73.7
```

The experiment therefore did not produce artificially perfect classification.

Performance varied substantially by environment.

```text
Environment 0.05
Accuracy: 100%
Mean Absolute Error: ~0.00784

Environment 0.10
Accuracy: 30%
Mean Absolute Error: ~0.03279

Environment 0.15
Accuracy: 50%
Mean Absolute Error: ~0.03462

Environment 0.20
Accuracy: 30%
Mean Absolute Error: ~0.04370

Environment 0.25
Accuracy: 20%
Mean Absolute Error: ~0.04022

Environment 0.30
Accuracy: 40%
Mean Absolute Error: ~0.06738
```

### Autonomy Conditions

During held-out prediction:

```text
True environment supplied during prediction: NO

Hidden buyer thresholds supplied to world model: NO

Private buyer decision rules supplied to world model: NO

Predictions generated from observable behavioural features: YES

Training and validation seeds separated: YES

True validation environment used for evaluation only: YES
```

### Finding

Historical buyer interactions contain sufficient behavioural structure for a learned model to infer aspects of the simulated buyer environment.

However, exact environment classification remains difficult, particularly where behavioural distributions overlap.

---

# 16. Experiment 025 — Self-Improving Buyer World Model

Experiment 025 asks the final question in the MARS experimental programme:

> Should the buyer world model continue learning from new buyers after deployment?

Two architectures are created.

```text
STATIC WORLD MODEL

vs

CONTINUAL WORLD MODEL
```

Both systems begin with exactly the same historical memory.

Both receive the same unseen diagnostic buyer episodes.

The difference is:

```text
STATIC MODEL
Predicts but does not learn from new buyers.

CONTINUAL MODEL
Predicts first,
receives delayed supervisory feedback,
detects experience gaps,
and selectively adds new experiences to memory.
```

The prediction is always recorded before feedback is used.

This protects causal evaluation.

---

# 17. Experiment 025 Results

The benchmark contained:

```text
Historical Training Episodes: 120
Matched Online Buyer Episodes: 120
Static Online Predictions: 120
Continual Online Predictions: 120
Environment Classes: 6
Behavioural Features: 9
```

The static model achieved:

```text
Exact Classification Accuracy:
54.17%

Mean Absolute Environment Error:
0.03093181780115231

Mean Prediction Confidence:
0.5917610281261403
```

The continual model achieved:

```text
Exact Classification Accuracy:
47.50%

Mean Absolute Environment Error:
0.032140016954918874

Mean Prediction Confidence:
0.6222319330325458
```

The resulting change was:

```text
Accuracy Change:
-6.67 percentage points

Mean Error Change:
+0.001208199153766562
```

### Critical Finding

The continual model became:

```text
MORE CONFIDENT
```

while becoming:

```text
LESS ACCURATE
```

This is an important negative experimental result.

---

# 18. Experiment 025 — Early vs Late Performance

The static model produced:

```text
Early Accuracy: 50.00%
Late Accuracy: 58.33%

Early Mean Error:
0.029003050764290262

Late Mean Error:
0.032860584838014364
```

The continual model produced:

```text
Early Accuracy: 46.67%
Late Accuracy: 48.33%

Early Mean Error:
0.0316921050637643

Late Mean Error:
0.03258792884607345
```

The continual system therefore did not demonstrate meaningful progressive improvement despite accumulating additional experience.

---

# 19. Experiment 025 — Memory Growth

The continual learner began with:

```text
120 historical experiences
```

and finished with:

```text
191 experiences
```

It detected:

```text
71 experience gaps
```

and performed:

```text
71 continual updates
```

while skipping:

```text
49 episodes
```

Learning by environment was:

```text
0.05 → 4 episodes
0.10 → 6 episodes
0.15 → 16 episodes
0.20 → 16 episodes
0.25 → 13 episodes
0.30 → 16 episodes
```

The model therefore acquired substantial additional experience.

However, the additional memory did not improve overall predictive performance.

---

# 20. Final Experimental Finding

Experiment 025 exposes a fundamental distinction:

```text
UNFAMILIAR EXPERIENCE
```

is not necessarily:

```text
USEFUL EXPERIENCE
```

A novel observation may represent:

- genuinely useful information;
- stochastic noise;
- an ambiguous boundary observation;
- an outlier;
- redundant experience;
- or behaviour that should not be permanently consolidated.

The naive continual-learning architecture effectively followed:

```text
Experience Gap
      │
      ▼
Store Experience
      │
      ▼
Update World Model
```

The results show that this assumption is insufficient.

### Final Research Insight

> More autonomous learning does not automatically produce better commercial intelligence.

A system can collect more information, accumulate more memory and become more confident while simultaneously becoming less accurate.

This establishes memory quality and confidence calibration as important future research problems for autonomous commercial agents.

---

# 21. Complete MARS Research Architecture

The final MARS architecture can be conceptualised as:

```text
                    AUTONOMOUS BUYER
                           │
                           ▼
                COMMERCIAL INTERACTION
                           │
                           ▼
                 OBSERVABLE BEHAVIOUR
                           │
                           ▼
                  DIAGNOSTIC PROBES
                           │
                           ▼
                 POLICY INFERENCE
                           │
                           ▼
                UNCERTAINTY ESTIMATION
                           │
                           ▼
              ACTIVE EVIDENCE ACQUISITION
                           │
                           ▼
               ENVIRONMENT ESTIMATION
                           │
                           ▼
                 META-POLICY SELECTION
                           │
                           ▼
                  BUYER WORLD MODEL
                           │
                           ▼
              SUPPLIER DECISION INTELLIGENCE
                           │
                           ▼
            COMMERCIAL STRATEGY / NEGOTIATION
```

---

# 22. Complete Experimental Progression

```text
AUTONOMOUS BLACK-BOX BUYER
            │
            ▼
HIDDEN POLICY DISCOVERY
            │
            ▼
THRESHOLD INFERENCE
            │
            ▼
COMMERCIAL INTERVENTION
            │
            ▼
PROPOSAL OPTIMISATION
            │
            ▼
NEGOTIATION INTELLIGENCE
            │
            ▼
ACTIVE EXPERIMENT SELECTION
            │
            ▼
INFORMATION-GAIN OPTIMISATION
            │
            ▼
COST-AWARE DISCOVERY
            │
            ▼
MULTI-BUYER GENERALISATION
            │
            ▼
STOCHASTIC BUYER BEHAVIOUR
            │
            ▼
REPEATED EVIDENCE
            │
            ▼
ADAPTIVE SEQUENTIAL EVIDENCE
            │
            ▼
STATISTICAL ROBUSTNESS
            │
            ▼
META-POLICY LEARNING
            │
            ▼
LATENT ENVIRONMENT IDENTIFICATION
            │
            ▼
ACTIVE DIAGNOSTIC INTELLIGENCE
            │
            ▼
BUYER WORLD MODEL
            │
            ▼
CONTINUAL WORLD-MODEL LEARNING
```

---

# 23. Research Principles

The MARS experimental programme follows several methodological principles.

## 23.1 Black-Box Interaction

When an experiment evaluates buyer-policy discovery, the hidden policy should not simply be supplied to the inference mechanism.

The supplier must derive useful information from observable buyer behaviour.

---

## 23.2 Causal Evaluation

Information revealed after a prediction must not be allowed to influence the prediction being evaluated.

This principle becomes particularly important in Experiment 025.

The sequence is:

```text
Observe Buyer
      │
      ▼
Make Prediction
      │
      ▼
Record Prediction
      │
      ▼
Reveal Feedback
      │
      ▼
Potentially Learn
      │
      ▼
Influence Future Buyers Only
```

---

## 23.3 Matched Benchmarking

When architectures are compared, they should encounter equivalent buyer environments and evidence wherever possible.

This allows differences in performance to be attributed more clearly to architectural differences.

---

## 23.4 Hold-Out Evaluation

Training and validation environments should be separated where the experiment evaluates generalisation.

Experiment 024 uses distinct historical training and held-out validation seeds.

---

## 23.5 Query Efficiency

Accuracy alone is not sufficient.

MARS also measures how many buyer interactions are required to obtain useful commercial intelligence.

---

## 23.6 Commercial Cost

Information gathering may itself carry commercial consequences.

MARS therefore introduces modelled probe cost and commercial risk in cost-aware experimentation.

---

## 23.7 Negative Results Are Retained

An experimental architecture is not modified simply because it underperforms a baseline.

Experiment 025 is intentionally retained as a negative result.

The continual learner performed worse than the static baseline despite accumulating additional experience.

This is treated as evidence about the limitations of naive continual learning.

---

## 23.8 Simulation Boundaries

MARS currently evaluates autonomous commercial intelligence within simulated buyer environments.

Results must not be interpreted as demonstrating equivalent performance against real-world procurement systems.

---

# 24. Major Quantitative Findings

Several important quantitative findings emerged across the later MARS experiments.

### Active Policy Discovery

```text
Fixed Policy Discovery:
73 queries

Active Policy Discovery:
58 queries

Query Reduction:
20.55%
```

---

### Cost-Aware Discovery

```text
Buyer Queries:
57

Policy Coverage:
100%

Resolved Variables:
5

Total Modelled Probe Cost:
£2,100
```

---

### Stochastic Evidence

```text
Single Observation Mean Normalised Error:
~0.01221

Repeated Evidence Mean Normalised Error:
~0.00001068

Relative Error Reduction:
~99.91%
```

---

### Adaptive Sequential Evidence

```text
Fixed Repeated Queries:
483

Adaptive Queries:
267

Queries Saved:
216

Query Reduction:
44.72%
```

---

### Statistical Robustness

```text
Mean Fixed Queries:
~483.06

Mean Adaptive Queries:
~292.67

Mean Query Reduction:
~39.41%
```

---

### Meta-Policy Validation

```text
Policy Coverage:
100%

Mean Normalised Error:
~0.000584

Mean Queries:
369.6

Failed Validation Runs:
0
```

---

### Active Diagnostic Intelligence

```text
Fixed Diagnostic Queries:
240

Active Diagnostic Queries:
~74.53

Diagnostic Query Reduction:
68.94%

Final Policy Coverage:
100%
```

---

### Buyer World Model

```text
Training Episodes:
120

Held-Out Episodes:
60

Exact Environment Accuracy:
45.00%

Mean Absolute Environment Error:
~0.03776

Mean Diagnostic Queries:
73.7
```

---

### Continual Buyer World Model

```text
Static Accuracy:
54.17%

Continual Accuracy:
47.50%

Accuracy Change:
-6.67 percentage points

Static Mean Error:
~0.03093

Continual Mean Error:
~0.03214

Initial Continual Memory:
120

Final Continual Memory:
191
```

---

# 25. Core Research Contributions

The MARS experimental programme investigates several interconnected capabilities.

## Contribution 1 — Black-Box Commercial Policy Discovery

MARS demonstrates an experimental framework in which hidden buyer
constraints can be investigated through observable commercial
interactions.

---

## Contribution 2 — Active Commercial Experimentation

The supplier can select informative commercial probes rather than relying
only on predetermined experiments.

---

## Contribution 3 — Cost-Aware Information Acquisition

MARS incorporates the idea that commercial information has an acquisition
cost and that informative experiments may also create commercial risk.

---

## Contribution 4 — Stochastic Buyer Reasoning

The framework explicitly studies noisy buyer decisions and the need to
accumulate evidence before inferring hidden policies.

---

## Contribution 5 — Adaptive Evidence Collection

MARS investigates when sufficient evidence has been collected and whether
additional buyer queries remain necessary.

---

## Contribution 6 — Meta-Policy Learning

The system learns which evidence strategy should be used under different
simulated behavioural environments.

---

## Contribution 7 — Latent Environment Identification

MARS removes the assumption that the buyer's behavioural environment is
known in advance and attempts to estimate it from observed behaviour.

---

## Contribution 8 — Active Diagnostic Intelligence

The system actively determines how much diagnostic evidence is necessary
before selecting a downstream inference strategy.

---

## Contribution 9 — Buyer World Models

Historical buyer interactions are converted into behavioural
representations that support learned environment prediction.

---

## Contribution 10 — Continual-Learning Failure Analysis

The final experiment demonstrates that indiscriminate accumulation of
novel experience can degrade predictive performance.

This identifies memory quality as a separate problem from memory quantity.

---

# 26. Key Scientific Lesson

The progression of MARS produces an important general lesson.

Early experiments ask:

```text
Can the AI learn more?
```

Later experiments ask:

```text
Can the AI learn with fewer interactions?
```

Then:

```text
Can the AI decide how to learn?
```

And finally:

```text
Should the AI learn from every new experience?
```

Experiment 025 demonstrates that the answer to the final question is not
automatically yes.

The broader lesson is:

> Autonomous intelligence requires mechanisms for controlling not only
> what an agent learns, but also what it chooses not to learn.

---

# 27. Future Research

The MARS 25-experiment programme is complete.

Potential extensions are intentionally classified as future research
rather than additional experiments in the current programme.

Possible directions include:

- protected continual learning;
- memory consolidation;
- experience-quality estimation;
- confidence calibration;
- out-of-distribution buyer detection;
- non-stationary buyer environments;
- temporal buyer-policy drift;
- multi-agent buyer populations;
- strategic buyer deception;
- competing autonomous suppliers;
- reinforcement learning for commercial experimentation;
- learned diagnostic probe generation;
- causal buyer world models;
- long-horizon commercial strategy;
- autonomous contract negotiation;
- human-versus-machine negotiation studies;
- real-world procurement-agent benchmarks;
- privacy-preserving buyer intelligence;
- adversarial robustness;
- multi-market buyer behaviour;
- autonomous commercial memory management.

A particularly important future direction follows directly from
Experiment 025:

```text
NEW EXPERIENCE
      │
      ▼
EXPERIENCE QUALITY ASSESSMENT
      │
      ├───────────────┐
      ▼               ▼
UNRELIABLE          RELIABLE
      │               │
      ▼               ▼
REJECT /          MEMORY
QUARANTINE       CONSOLIDATION
                      │
                      ▼
               LONG-TERM MEMORY
```

This would investigate whether autonomous agents can learn continuously
without allowing unreliable experiences to contaminate established
knowledge.

---

# 28. Research Scope and Limitations

MARS is an experimental AI research environment.

It investigates machine-to-machine commercial reasoning using simulated
autonomous buyers.

The experiments do not establish equivalent performance against
production procurement systems.

Several limitations remain.

These include:

- simulated buyer environments;
- predefined commercial variables;
- limited environment classes;
- synthetic stochastic behaviour;
- simplified buyer objectives;
- absence of real procurement organisations;
- limited long-horizon interaction;
- simplified feedback mechanisms;
- and controlled experimental conditions.

These limitations are important because MARS should be interpreted as an
experimental framework for studying autonomous commercial intelligence,
not as evidence that the same results will automatically transfer to
real-world purchasing systems.

---

# 29. Final Conclusion

MARS begins with a simple problem:

> Can an AI supplier infer why an autonomous buyer rejected a commercial
> proposal?

Across 25 experiments, that question evolves substantially.

The supplier progresses from basic black-box inference toward:

- hidden policy discovery;
- commercial optimisation;
- negotiation reasoning;
- active experimentation;
- information-gain optimisation;
- cost-aware evidence acquisition;
- stochastic evidence reasoning;
- adaptive stopping;
- statistical robustness;
- meta-policy learning;
- latent environment estimation;
- active diagnostic intelligence;
- buyer world-model learning;
- and continual adaptation.

The final experiment reveals an important boundary.

More learning is not necessarily better learning.

The continual buyer world model accumulated additional experience and
became more confident, but it did not outperform the static world model.

This demonstrates that autonomous commercial intelligence requires more
than increasingly powerful learning mechanisms.

It also requires:

```text
EVIDENCE QUALITY
       +
UNCERTAINTY CONTROL
       +
CAUSAL INTEGRITY
       +
MEMORY GOVERNANCE
       +
ROBUST EVALUATION
```

MARS therefore concludes not with a claim that autonomous commercial
intelligence has been solved, but with a more precise research problem:

> How can autonomous commercial agents determine which observations are
> sufficiently reliable, informative and causally valid to become part
> of their long-term understanding of other machine agents?

That question provides the foundation for future research beyond the
completed 25-experiment MARS programme.

---

# MARS — Machine-Agent Revenue Science

**25 Experiments Completed**

**Research progression:**

```text
Buyer Behaviour
      ↓
Policy Intelligence
      ↓
Commercial Intelligence
      ↓
Active Experimentation
      ↓
Uncertainty Intelligence
      ↓
Environment Intelligence
      ↓
World-Model Intelligence
      ↓
Continual Learning
      ↓
Memory Reliability Problem
```

**Author:** Kamran Khan
