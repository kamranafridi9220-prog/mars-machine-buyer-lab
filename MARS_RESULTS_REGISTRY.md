# MARS — Machine-Agent Revenue Science

## Master Experimental Results Registry

**Author:** Kamran Khan  
**Programme:** Experiments 001–025  
**Status:** Experimental programme completed

---

# Purpose

This document is the central quantitative results registry for the MARS research programme.

It records the principal experimental measurements produced across the 25-experiment programme and separates quantitative benchmark results from architectural or exploratory experiments.

Results should be reported as produced by the corresponding experiment.

Negative results are retained.

No experiment is modified solely to improve its reported performance.

---

# Experimental Results Summary

| Experiment | Research Focus | Principal Result |
|---|---|---|
| 001–012 | Buyer simulation, policy inference, commercial intervention and negotiation | Foundational and architectural experimental progression |
| 013 | Active policy discovery | 58 buyer queries with complete tested policy discovery |
| 014 | Fixed vs active discovery | 73 → 58 queries; 20.55% reduction |
| 015 | Advanced active discovery | Extension of autonomous experiment-selection architecture |
| 016 | Cost-aware experimentation | 57 queries; 100% coverage; £2,100 modelled probe cost |
| 017 | Multi-buyer generalisation | Adaptive strategies achieved complete tested generalisation |
| 018 | Stochastic repeated evidence | ~99.91% relative error reduction versus single observation |
| 019 | Adaptive sequential evidence | 483 → 267 queries; 44.72% reduction |
| 020 | Statistical robustness | ~39.41% mean query reduction across robustness benchmark |
| 021 | Meta-policy learning | 100% validation coverage; 0 failed validation runs |
| 022 | Latent environment identification | 30/30 successful closed-loop runs; 100% final coverage |
| 023 | Active diagnostic intelligence | 240 → ~74.53 diagnostic queries; 68.94% reduction |
| 024 | Buyer world model | 45.00% held-out exact environment classification |
| 025 | Continual world model | 47.50% continual vs 54.17% static accuracy |

---

# Experiment 013 — Active Buyer Policy Discovery

## Core Result

```text
Total Buyer Queries: 58
Policy Variables Discovered: 5
Policy Coverage: 100%
```

Approximate recovered thresholds:

```text
Annual Price: ~104999.54
Contract Months: 36
Service Availability: ~98.00049
Payment Days: 30
Supplier Reliability: 85
```

## Interpretation

Active query selection demonstrated that MARS could recover the tested hidden buyer-policy structure while autonomously selecting informative commercial interactions.

---

# Experiment 014 — Comparative Policy Discovery Benchmark

## Results

```text
Fixed Inference Queries: 73
Autonomous Active Queries: 58
Queries Saved: 15
Query Reduction: 20.55%

Fixed Policy Coverage: 100%
Active Policy Coverage: 100%
```

## Interpretation

Active experiment selection reduced the number of buyer interactions required for complete tested policy discovery.

---

# Experiment 016 — Cost-Aware Experimentation

## Results

```text
Total Buyer Queries: 57

Resolved Variables: 5

Policy Coverage: 100%

Queries per Discovered Policy: 11.4

Total Modelled Probe Cost: £2,100

Average Modelled Probe Cost: £36.84

Maximum Single Modelled Probe Cost: £1,800

Average Commercial Risk: 0.12057

Total Information Value: 9.703961

Average Information Value: 0.170245

Total Cost-Aware Utility: 8.869019

Average Cost-Aware Utility: 0.155597

Total Realised Uncertainty Reduction: 4.967035
```

## Interpretation

Experiment 016 introduced explicit commercial cost and risk into autonomous experiment selection.

Information acquisition was therefore treated as a commercial optimisation problem rather than a purely statistical one.

---

# Experiment 017 — Multi-Buyer Generalisation

## Strategy-Level Outcome

```text
Fixed:
INCOMPLETE GENERALISATION

Uncertainty:
COMPLETE ACROSS ALL TESTED BUYERS

Expected Information Gain:
COMPLETE ACROSS ALL TESTED BUYERS

Cost-Aware:
COMPLETE ACROSS ALL TESTED BUYERS
```

Additional cost-aware results:

```text
Successful Buyers: 5

Total Modelled Probe Cost: £5,000

Average Cost per Successful Buyer: £1,000

Average Commercial Risk: 0.350075
```

## Interpretation

The benchmark demonstrated that a discovery strategy effective against one buyer configuration does not necessarily generalise across different buyer environments.

---

# Experiment 018 — Stochastic Buyer Diagnostics

## Single Observation

```text
Total Evaluations: 60

Noise Events: 6

Realised Noise: 0.10

Policy Coverage: 100%

Mean Normalised Error:
0.012207655
```

## Repeated Evidence

```text
Total Evaluations: 483

Noise Events: 43

Realised Noise:
0.089027

Policy Coverage: 100%

Mean Normalised Error:
0.00001068115234375
```

## Comparative Result

```text
Relative Error Reduction:
~99.91%
```

## Interpretation

Repeated evidence dramatically reduced threshold-estimation error under the tested stochastic buyer behaviour, but at the cost of substantially more buyer evaluations.

---

# Experiment 019 — Adaptive Sequential Evidence

## Results

```text
Fixed Repeated-Evidence Queries: 483

Adaptive Sequential Queries: 267

Queries Saved: 216

Query Reduction: 44.72%

Adaptive Early-Stop Rate: 91.18%

Average Observations per Candidate:
3.8824

Adaptive Mean Normalised Error:
0.00001068115234375
```

## Interpretation

Adaptive sequential evidence retained approximately the same measured error while substantially reducing buyer interactions relative to fixed repeated evidence.

---

# Experiment 020 — Statistical Robustness

## Experimental Scale

```text
Random Seeds: 20

Noise Levels: 6

Inference Architectures: 3

Total Discovery Runs: 360

Buyer Environments: 120
```

## Aggregate Query Results

```text
Fixed Mean Queries:
483.0583

Adaptive Mean Queries:
292.6667

Mean Queries Saved:
190.3917

Mean Query Reduction:
39.41%
```

## Aggregate Accuracy

```text
Fixed Mean Normalised Error:
0.000881302

Adaptive Mean Normalised Error:
0.000815353

Adaptive Error Difference:
-0.0000659
```

## High-Noise Example — Noise 0.30

```text
Single Observation Error:
0.01086648

Fixed Repeated Error:
0.00200791

Adaptive Error:
0.00272901
```

Queries:

```text
Single:
58.5

Fixed:
483.35

Adaptive:
335.9
```

## Interpretation

Adaptive evidence reduced mean query requirements substantially across the complete benchmark.

Aggregate mean error was slightly lower for adaptive evidence, but fixed repeated evidence could outperform adaptive evidence at individual high-noise conditions.

Therefore, the experiment does not establish that adaptive evidence is universally more accurate.

---

# Experiment 021 — Autonomous Meta-Policy Learning

## Experimental Scale

```text
Training Seeds: 15

Validation Seeds: 5

Noise Environments: 6

Training Runs: 360

Validation Runs: 30

Total Runs: 390
```

## Validation Results

```text
Mean Validation Coverage:
100%

Mean Validation Error:
0.0005840376479877844

Mean Validation Queries:
369.6

Failed Validation Runs:
0
```

## Learned Environment-to-Policy Mapping

```text
0.05 → BALANCED

0.10 → BALANCED

0.15 → HIGH_ASSURANCE

0.20 → ROBUST

0.25 → HIGH_ASSURANCE

0.30 → ROBUST
```

## Interpretation

The learned mapping was not monotonic.

Increasing stochasticity did not produce a trivial linear progression between evidence policies.

---

# Experiment 022 — Latent Buyer Environment Identification

## Results

```text
Meta-Policy Training Runs:
240

Closed-Loop Test Runs:
30

Successful Runs:
30/30

Success Rate:
100%

Mean Behavioural-Noise Estimation Error:
0.1547222222222222

Dynamic vs Oracle Policy Agreement:
66.67%

Mean Final Policy Coverage:
100%

Mean Final Normalised Error:
0.0006533958098017068

Mean Diagnostic Query Cost:
240

Mean Total Closed-Loop Queries:
870.4
```

## Autonomy Conditions

```text
True Noise Supplied to Estimator:
NO

True Noise Supplied to Controller:
NO

Hidden Thresholds Supplied to Estimator:
NO

Probes Generated from Inferred Policy:
YES

Policy Selected from Observed Behaviour:
YES

True Simulator Noise Used for Evaluation Only:
YES
```

---

# Experiment 023 — Active Diagnostic Intelligence

## Matched Benchmark

```text
Matched Buyer Environments:
30
```

## Diagnostic Query Comparison

```text
Experiment 022 Mean Diagnostic Queries:
240

Experiment 023 Mean Diagnostic Queries:
74.53333333333333

Mean Diagnostic Queries Saved:
165.46666666666667

Diagnostic Query Reduction:
68.94%
```

## Environment Estimation

```text
Experiment 022 Mean Noise Error:
0.1702777777777778

Experiment 023 Mean Noise Error:
0.03893970555442008
```

## Oracle Agreement

```text
Experiment 022:
60.00%

Experiment 023:
66.67%
```

## Final Policy Discovery

```text
Experiment 022 Coverage:
100%

Experiment 023 Coverage:
100%

Experiment 022 Final Normalised Error:
0.0011483134687186244

Experiment 023 Final Normalised Error:
0.0011587199628592495
```

## Total Interaction Cost

```text
Experiment 022 Mean Total Queries:
872.0333333333333

Experiment 023 Mean Total Queries:
689.4333333333333
```

## Active Stopping

```text
CONFIDENT_AND_STABLE:
29

MAXIMUM_QUERY_BUDGET:
1

Autonomous Stop Rate:
96.67%
```

## Interpretation

Across the 30 matched simulated buyer environments, active diagnosis substantially reduced diagnostic interaction requirements while maintaining complete final policy coverage.

The final policy-discovery error remained similar rather than demonstrating a large accuracy improvement.

---

# Experiment 024 — Buyer World Model Learning

## Experimental Scale

```text
Historical Training Episodes:
120

Held-Out Validation Episodes:
60

Environment Classes:
6

Behavioural Features:
9

Training/Validation Seed Overlap:
NONE
```

## Held-Out Results

```text
Correct Exact Classifications:
27 / 60

Exact Environment Classification Accuracy:
45.00%

Mean Absolute Environment Error:
0.03775808843478146

Mean Prediction Confidence:
0.6194818648606951

Mean Prediction Entropy:
1.1067022653689782

Mean Diagnostic Queries:
73.7
```

## Per-Environment Results

```text
Environment 0.05
Accuracy: 100%
MAE: 0.007837222168729313
Confidence: 0.8432555566254137

Environment 0.10
Accuracy: 30%
MAE: 0.032793117251689145
Confidence: 0.7213478114573979

Environment 0.15
Accuracy: 50%
MAE: 0.034623777301634136
Confidence: 0.6492519429491624

Environment 0.20
Accuracy: 30%
MAE: 0.04369773212144311
Confidence: 0.4910847044460554

Environment 0.25
Accuracy: 20%
MAE: 0.04021941928717043
Confidence: 0.4933881706985588

Environment 0.30
Accuracy: 40%
MAE: 0.06737726247802263
Confidence: 0.5185630029875823
```

## Methodological Boundary

The world model was trained using historical supervised environment labels.

It should therefore not be described as an unsupervised learning system.

During held-out prediction, however, the validation environment label was not supplied to the model.

---

# Experiment 025 — Self-Improving Buyer World Model

## Experimental Scale

```text
Historical Training Episodes:
120

Matched Online Buyer Episodes:
120

Static Online Predictions:
120

Continual Online Predictions:
120

Environment Classes:
6

Behavioural Features:
9
```

## Static World Model

```text
Exact Classification Accuracy:
54.17%

Mean Absolute Environment Error:
0.03093181780115231

Mean Prediction Confidence:
0.5917610281261403
```

## Continual World Model

```text
Exact Classification Accuracy:
47.50%

Mean Absolute Environment Error:
0.032140016954918874

Mean Prediction Confidence:
0.6222319330325458
```

## Comparative Result

```text
Continual Accuracy Change:
-6.67 percentage points

Continual Error Change:
+0.001208199153766562
```

## Early vs Late Performance

Static model:

```text
Early Accuracy:
50.00%

Late Accuracy:
58.33%

Early Mean Error:
0.029003050764290262

Late Mean Error:
0.032860584838014364
```

Continual model:

```text
Early Accuracy:
46.67%

Late Accuracy:
48.33%

Early Mean Error:
0.0316921050637643

Late Mean Error:
0.03258792884607345
```

## Continual Memory

```text
Initial Memory:
120

Final Memory:
191

Memory Growth:
71

Experience Gaps Detected:
71

Continual Updates:
71

Learned Episodes:
71

Skipped Learning Episodes:
49
```

## Learning Counts by Environment

```text
0.05 → 4

0.10 → 6

0.15 → 16

0.20 → 16

0.25 → 13

0.30 → 16
```

## Causal Evaluation

```text
Static and Continual Models Start
from Identical Historical Memory:
YES

Both Models Receive Identical
Diagnostic Episodes:
YES

True Environment Supplied Before
Static Prediction:
NO

True Environment Supplied Before
Continual Prediction:
NO

Feedback Occurs Only After the
Current Prediction Is Recorded:
YES

Current Feedback Can Influence
Future Buyers Only:
YES

Experience-Gap Decision Uses
Hidden Environment Label:
NO

Hidden Buyer Thresholds Supplied
to Continual World Model:
NO
```

## Interpretation

The continual learner accumulated 71 additional experiences but did not outperform the static baseline.

Its exact classification accuracy decreased from 54.17% to 47.50%.

At the same time, its mean prediction confidence increased.

The experiment therefore demonstrates that additional online learning does not necessarily produce better buyer-environment inference.

Novel experience should not automatically be treated as reliable long-term knowledge.

---

# Cross-Experiment Research Progression

```text
Fixed Policy Discovery
        ↓
Active Policy Discovery
        ↓
Cost-Aware Discovery
        ↓
Stochastic Evidence
        ↓
Adaptive Evidence
        ↓
Statistical Robustness
        ↓
Meta-Policy Learning
        ↓
Latent Environment Identification
        ↓
Active Diagnostic Intelligence
        ↓
Buyer World Model
        ↓
Continual Buyer World Model
```

---

# Principal Quantitative Milestones

| Research Stage | Principal Measurement |
|---|---:|
| Active vs Fixed Policy Discovery | 20.55% fewer queries |
| Adaptive vs Fixed Repeated Evidence | 44.72% fewer queries |
| Robustness Benchmark | 39.41% mean query reduction |
| Active vs Fixed Diagnosis | 68.94% fewer diagnostic queries |
| Buyer World Model | 45.00% held-out exact classification |
| Static World Model — Exp. 025 | 54.17% online accuracy |
| Continual World Model — Exp. 025 | 47.50% online accuracy |
| Continual Memory Growth | 120 → 191 episodes |

---

# Final Experimental Finding

The complete MARS programme demonstrates that increasing autonomy creates additional research problems rather than automatically improving performance.

The progression can be summarised as:

```text
Can MARS discover the buyer?
            ↓
Can MARS choose how to investigate the buyer?
            ↓
Can MARS reduce the cost of investigation?
            ↓
Can MARS reason under noisy buyer behaviour?
            ↓
Can MARS determine how much evidence it needs?
            ↓
Can MARS learn which inference strategy to use?
            ↓
Can MARS infer the buyer environment?
            ↓
Can MARS learn a world model from historical buyers?
            ↓
Can MARS improve that model continuously?
            ↓
Not necessarily.
```

Experiment 025 demonstrates that additional memory and increased model confidence can coexist with reduced predictive accuracy.

This motivates future research into:

```text
Memory Quality
Confidence Calibration
Protected Continual Learning
Experience Validation
Memory Consolidation
Out-of-Distribution Detection
```

without extending the current 25-experiment programme.

---

# Experimental Boundary

All results in this registry were produced within the simulated MARS experimental environment.

They should not be interpreted as evidence of equivalent performance against real-world autonomous procurement systems.

The registry documents experimental behaviour within the implemented simulation framework.

---

# Programme Status

```text
MARS — Machine-Agent Revenue Science

Experiments Completed: 25

Experimental Programme: COMPLETE

Next Phase:
Research Documentation
Results Visualisation
Repository Presentation
Technical Paper / Portfolio Presentation
```

**Author:** Kamran Khan
