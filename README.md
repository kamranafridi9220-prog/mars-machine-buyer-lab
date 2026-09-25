# MARS — Machine-Agent Revenue Science

### Black-Box Buyer Intelligence for Autonomous B2B Commerce

**An Experimental AI Framework for Buyer Policy Inference, Autonomous Commercial Negotiation, and Minimum-Cost Revenue Intervention**

MARS is an experimental artificial intelligence framework designed to investigate how autonomous purchasing agents evaluate commercial proposals and how suppliers can adapt their strategies when the buyer's internal decision-making policies are unknown.

The project explores the intersection of autonomous AI agents, B2B procurement, commercial intelligence, experimental optimisation, and machine-to-machine negotiation.

Rather than developing another conventional sales automation application, MARS investigates a fundamental question concerning the future of autonomous commerce:

**Can an intelligent supplier system discover how an autonomous buyer makes purchasing decisions without accessing the buyer's internal decision-making process?**

The framework investigates this question through controlled computational experiments involving simulated purchasing agents, black-box policy inference, commercial intervention, adaptive learning, and adversarial negotiation.

---

## The Problem

Traditional B2B sales processes are designed around human decision-makers.

However, as organisations increasingly investigate autonomous AI agents for procurement and commercial decision support, suppliers may encounter purchasing systems whose internal objectives, evaluation criteria, and decision policies are inaccessible.

A supplier may observe whether a proposal is accepted or rejected without understanding which commercial conditions influenced the outcome.

For example, a supplier might submit a commercially competitive proposal that an autonomous purchasing agent rejects.

The supplier may not know whether the rejection resulted from:

- Pricing constraints
- Contract duration
- Supplier reliability
- Payment terms
- Service-level requirements
- Operational risk
- Hidden procurement preferences

Without understanding these decision patterns, suppliers may repeatedly modify proposals without knowing which changes are commercially necessary.

MARS investigates whether controlled experimentation can help infer hidden buyer decision patterns and identify commercially viable proposal modifications.

---

## Research Question

Can an AI system infer the decision policies of autonomous purchasing agents through controlled commercial experiments and identify minimum-cost interventions that improve supplier acceptance without accessing the buyer's internal decision-making process?

---

## Core Research Objectives

1. Develop a simulated autonomous B2B purchasing environment.
2. Construct purchasing agents with heterogeneous commercial objectives and constraints.
3. Implement a black-box experimentation framework for evaluating supplier proposals.
4. Investigate algorithms for inferring hidden buyer decision policies.
5. Develop a minimum-cost commercial intervention engine.
6. Investigate autonomous supplier-buyer negotiation.
7. Evaluate the framework against baseline commercial strategies.
8. Examine generalisation across previously unseen buyer policies.
9. Investigate adaptive commercial learning under changing procurement conditions.
10. Examine adversarial negotiation and buyer defence mechanisms.

---

# MARS Experimental Architecture

MARS is organised into interconnected research components that support the investigation of autonomous commercial decision-making.

The architecture has evolved through ten computational experiments.

## 1. Autonomous Buyer Laboratory

A simulated procurement environment containing autonomous purchasing agents with hidden commercial decision policies.

Commercial decision variables may include:

- Price
- Contract duration
- Service-level agreements
- Supplier reliability
- Payment terms
- Compliance requirements
- Operational risk
- Total cost of ownership

Buyer policies remain hidden from the supplier-facing intelligence system during black-box experimentation.

The laboratory provides a controlled environment for investigating how purchasing agents respond to commercial proposals.

**Implementation directory:** `buyer_lab/`

---

## 2. Black-Box Buyer Policy Inference Engine

The inference engine investigates purchasing-agent behaviour through observable proposal outcomes.

Instead of directly accessing the buyer's internal decision rules, the supplier-facing system conducts experiments and analyses the resulting purchasing decisions.

The research investigates both individual commercial variables and multi-dimensional purchasing policies.

Potential methods for further investigation include:

- Active learning
- Bayesian inference
- Preference learning
- Surrogate modelling
- Black-box optimisation

**Implementation directory:** `inference/`

---

## 3. Commercial Experimentation Engine

The experimentation framework provides a controlled environment for submitting commercial proposals and observing purchasing-agent responses.

Experiments investigate how changes in commercial attributes influence buyer behaviour.

The framework supports research into:

- Buyer decision patterns
- Hidden commercial constraints
- Proposal acceptance conditions
- Commercial intervention
- Adaptive learning
- Negotiation behaviour

**Implementation directory:** `experiments/`

---

## 4. Minimum Winning Intervention Engine

The optimisation component investigates how suppliers can identify commercially viable proposal modifications while minimising intervention costs.

Instead of automatically offering the largest discount or most generous contractual conditions, the system investigates which modifications may be necessary to satisfy a buyer's purchasing requirements.

Potential interventions include:

- Price adjustments
- Contract modifications
- Service-level improvements
- Payment-term adjustments
- Risk mitigation measures

**Implementation directory:** `optimization/`

---

## 5. Autonomous Negotiation Laboratory

The negotiation environment investigates commercial interactions between autonomous buyer and supplier systems.

The laboratory explores:

- Commercial proposal evaluation
- Negotiation strategies
- Adaptive counteroffers
- Buyer responses
- Adversarial negotiation
- Buyer defence mechanisms

The objective is to investigate how autonomous commercial systems behave when purchasing and supplier objectives differ.

**Implementation directory:** `negotiation/`

---

## 6. Commercial Learning and Evaluation

MARS investigates how commercial intelligence systems can adapt to purchasing behaviour observed through repeated experimentation.

The experimental programme includes contextual commercial learning, adaptive negotiation benchmarking, and buyer policy drift.

Potential evaluation metrics include:

- Buyer decision prediction accuracy
- Proposal acceptance rate
- Supplier intervention cost
- Commercial margin preservation
- Experiment efficiency
- Policy inference accuracy
- Generalisation to unseen buyer scenarios
- Adaptation to changing buyer policies

These metrics represent research evaluation objectives and should not be interpreted as reported performance results.

---

# Experimental Development

## Experiments 001–010

The initial MARS experimental programme consists of ten Python experiments investigating progressively more complex autonomous commercial decision-making problems.

The experiments are organised around buyer simulation, policy inference, commercial optimisation, adaptive learning, and negotiation.

### Experiment 001 — Autonomous Buyer Simulation

**File:** `experiments/test_buyer.py`

Establishes the autonomous buyer laboratory.

The experiment introduces a simulated purchasing agent with internal procurement decision policies.

It provides the foundational environment for investigating how autonomous buyers evaluate commercial proposals.

### Experiment 002 — Black-Box Buyer Price Inference

**File:** `experiments/test_policy_inference.py`

Investigates whether purchasing constraints associated with price can be inferred through controlled proposal experiments.

The experiment introduces the central black-box inference problem: learning about buyer decision policies from observable purchasing outcomes.

### Experiment 003 — Multi-Dimensional Buyer Policy Inference

**File:** `experiments/test_multidimensional_inference.py`

Extends buyer policy inference beyond a single commercial variable.

The experiment investigates purchasing decisions involving multiple commercial attributes.

Its objective is to explore how combinations of proposal characteristics influence autonomous buyer behaviour.

### Experiment 004 — Minimum Winning Commercial Intervention

**File:** `experiments/test_minimum_intervention.py`

Investigates how a supplier-facing intelligence system can identify proposal modifications that satisfy buyer requirements while controlling supplier-side intervention costs.

The experiment introduces commercial optimisation into the buyer intelligence framework.

### Experiment 005 — Autonomous Negotiation

**File:** `experiments/test_negotiation.py`

Introduces autonomous commercial negotiation into the experimental environment.

The experiment investigates interactions between buyer and supplier decision-making systems.

It extends MARS from observing purchasing decisions towards investigating commercial negotiation behaviour.

### Experiment 006 — Commercial Deal Rescue

**File:** `experiments/test_deal_rescue.py`

Investigates whether rejected commercial proposals can be reconsidered through targeted modifications.

The experiment explores the relationship between buyer policy inference and commercially viable deal recovery.

### Experiment 007 — Contextual Commercial Learning

**File:** `experiments/test_commercial_learning.py`

Introduces contextual commercial learning into the experimental programme.

The experiment investigates how information from commercial interactions can inform subsequent decision-making.

### Experiment 008 — Adaptive Negotiation Benchmark

**File:** `experiments/test_adaptive_negotiation.py`

Introduces an experimental benchmark for adaptive commercial negotiation.

The experiment investigates negotiation behaviour under conditions where strategies may need to respond to observed buyer behaviour.

### Experiment 009 — Buyer Policy Drift and Adaptive Recovery

**File:** `experiments/test_policy_drift.py`

Investigates changes in autonomous purchasing policies.

A buyer's commercial requirements may evolve over time, potentially reducing the usefulness of previously inferred decision patterns.

The experiment examines adaptive recovery in response to changing buyer policies.

### Experiment 010 — Adversarial Negotiation and Buyer Defence

**File:** `experiments/test_adversarial_negotiation.py`

Introduces adversarial negotiation into the experimental programme.

The experiment investigates interactions involving competing commercial objectives and buyer defence mechanisms.

It extends the research towards understanding how autonomous purchasing systems behave under strategically challenging negotiation conditions.

---

# Experimental Progression

The ten experiments represent a progression through five research stages.

| Research Stage | Experiments | Research Focus |
|---|---|---|
| Autonomous Buyer Modelling | 001 | Simulated purchasing decisions |
| Black-Box Policy Discovery | 002–003 | Hidden buyer decision patterns |
| Commercial Optimisation | 004–006 | Intervention, negotiation, and deal recovery |
| Adaptive Commercial Intelligence | 007–009 | Learning, negotiation adaptation, and policy drift |
| Adversarial Commercial Systems | 010 | Negotiation under competing objectives and buyer defence |

This experimental structure allows MARS to investigate commercial decision-making at increasing levels of complexity.

---

# Example Research Scenario

A supplier submits a commercial proposal to an autonomous purchasing agent.

| Variable | Initial Proposal |
|---|---|
| Annual contract value | £100,000 |
| Contract duration | 24 months |
| Service availability | 95% |
| Payment terms | 30 days |
| Supplier reliability | 90% |

The purchasing agent rejects the proposal.

MARS conducts controlled experiments to investigate which commercial attributes influence the buyer's decision.

The system then investigates whether a minimum-cost modification could satisfy the buyer's requirements while preserving supplier profitability.

For example, the research may investigate whether improving service availability, adjusting payment terms, or modifying contract duration could influence the purchasing decision without requiring an unnecessarily large price reduction.

This scenario is illustrative and does not represent an experimentally validated commercial result.

---

# Repository Structure

```text
mars-machine-buyer-lab/
│
├── .github/
│   └── workflows/
│
├── buyer_lab/
│
├── inference/
│
├── optimization/
│
├── negotiation/
│
├── experiments/
│   │
│   ├── test_buyer.py
│   ├── test_policy_inference.py
│   ├── test_multidimensional_inference.py
│   ├── test_minimum_intervention.py
│   ├── test_negotiation.py
│   ├── test_deal_rescue.py
│   ├── test_commercial_learning.py
│   ├── test_adaptive_negotiation.py
│   ├── test_policy_drift.py
│   └── test_adversarial_negotiation.py
│
└── README.md
```

---

# Automated Experiment Execution

MARS includes GitHub Actions workflow integration.

Experiment 010 has been integrated into the repository's automated execution infrastructure.

This provides a foundation for reproducible computational experimentation and future continuous integration of the experimental framework.

The automation infrastructure will continue to evolve as additional research experiments and evaluation procedures are introduced.

---

# Technology Stack

The initial experimental implementation is developed in Python.

The broader research technology stack includes:

- Python
- NumPy
- Pandas
- Scikit-learn
- SciPy
- OpenAI API
- Streamlit
- Plotly
- SQLite
- GitHub Actions

Not all listed technologies are necessarily integrated into the current experimental implementation.

Additional technologies will be selected as the architecture develops.

---

# Research and Development Roadmap

### Phase 1 — Autonomous Buyer Simulation

Develop configurable purchasing agents with hidden commercial decision policies.

### Phase 2 — Black-Box Experimentation

Implement proposal submission, decision observation, and experimental data collection.

### Phase 3 — Buyer Policy Inference

Investigate algorithms for learning buyer decision patterns from experimental observations.

### Phase 4 — Minimum Winning Intervention

Develop an optimisation engine for identifying minimum-cost proposal modifications.

### Phase 5 — Autonomous Negotiation

Investigate buyer-supplier negotiation and adaptive commercial interactions.

### Phase 6 — Adaptive Commercial Intelligence

Investigate contextual learning, changing purchasing policies, and adaptive recovery.

### Phase 7 — Adversarial Commercial Systems

Investigate strategic negotiation behaviour and buyer defence mechanisms.

### Phase 8 — Experimental Evaluation

Evaluate inference accuracy, intervention efficiency, commercial outcomes, and generalisation against appropriate baselines.

---

# Research Positioning

MARS is an experimental research and engineering project.

Its objective is to investigate the technical challenges of autonomous B2B procurement intelligence rather than claim that existing purchasing-agent technologies or negotiation algorithms are entirely new.

The project's research contribution will be assessed through literature review, system implementation, controlled experimentation, and comparison with established baseline methods.

The current experiments use a simulated commercial environment.

Findings from simulated purchasing agents should not be interpreted as evidence of equivalent behaviour in real-world procurement systems without additional validation.

---

# Project Status

**Active Research and Experimental Development**

The initial experimental programme has progressed through Experiment 010.

Current repository development includes:

- Autonomous buyer simulation
- Black-box buyer policy inference
- Multi-dimensional commercial inference
- Minimum winning intervention
- Autonomous negotiation
- Commercial deal rescue
- Contextual commercial learning
- Adaptive negotiation benchmarking
- Buyer policy drift and recovery
- Adversarial negotiation and buyer defence
- GitHub Actions experiment integration

The framework remains under active development.

Further work will investigate experimental robustness, AI agent integration, comparative evaluation, and generalisation across more complex commercial environments.

---

# Author

**Kamran Khan**

AI Decision Intelligence | B2B Sales | Business Intelligence | Autonomous Commercial Systems

Research interests include autonomous AI agents, commercial decision intelligence, multi-agent systems, revenue optimisation, and machine-to-machine commerce.
