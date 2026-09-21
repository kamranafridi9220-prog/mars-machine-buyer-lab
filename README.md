# MARS — Machine-Agent Revenue Science

### Black-Box Buyer Intelligence for Autonomous B2B Commerce

MARS is an experimental artificial intelligence framework designed to investigate how autonomous purchasing agents evaluate commercial proposals and how suppliers can adapt their strategies when the buyer's internal decision-making policies are unknown.

The project explores the intersection of autonomous AI agents, B2B procurement, commercial intelligence, experimental optimisation, and machine-to-machine negotiation.

---

## The Problem

Traditional B2B sales processes are designed around human decision-makers.

However, as organisations increasingly investigate autonomous AI agents for procurement and commercial decision support, suppliers may encounter purchasing systems whose internal objectives, evaluation criteria, and decision policies are inaccessible.

A supplier may observe whether a proposal is accepted or rejected without understanding which commercial conditions influenced the outcome.

MARS investigates whether controlled experimentation can help infer these hidden decision patterns and identify commercially viable proposal modifications.

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

---

## Proposed System Architecture

MARS will consist of six interconnected research components.

### 1. Autonomous Buyer Laboratory

A simulated procurement environment containing autonomous purchasing agents with different commercial objectives.

Potential decision variables include:

- Price
- Contract duration
- Service-level agreements
- Supplier reliability
- Payment terms
- Compliance requirements
- Operational risk
- Total cost of ownership

Buyer policies will remain hidden from the supplier-facing intelligence system during experimentation.

### 2. Black-Box Buyer Policy Inference Engine

An experimental inference system that investigates purchasing-agent behaviour using observable proposal outcomes.

The engine will examine relationships between commercial proposal attributes and purchasing decisions.

Potential research methods include:

- Active learning
- Bayesian inference
- Preference learning
- Surrogate modelling
- Black-box optimisation

### 3. Commercial Experimentation Engine

A controlled environment for submitting commercial proposals and observing purchasing-agent responses.

The engine will support systematic experimentation with proposal attributes and record the resulting outcomes.

### 4. Minimum Winning Intervention Engine

An optimisation component designed to identify commercially viable proposal modifications that satisfy buyer requirements while minimising supplier-side intervention costs.

Potential interventions include:

- Price adjustments
- Contract modifications
- Service-level improvements
- Payment-term adjustments
- Risk mitigation measures

### 5. Autonomous Negotiation Laboratory

A multi-agent environment for investigating commercial negotiation between autonomous buyer and supplier agents.

The laboratory will examine how agents exchange proposals, respond to counteroffers, and converge towards mutually acceptable commercial arrangements.

### 6. Commercial Learning and Evaluation Engine

An experimental evaluation component for measuring the effectiveness of inferred buyer policies and proposed commercial interventions.

Potential evaluation metrics include:

- Buyer decision prediction accuracy
- Proposal acceptance rate
- Supplier intervention cost
- Commercial margin preservation
- Experiment efficiency
- Policy inference accuracy
- Generalisation to unseen buyer scenarios

---

## Example Research Scenario

A supplier submits a commercial proposal to an autonomous purchasing agent.

The proposal contains:

| Variable | Initial Proposal |
|---|---|
| Annual contract value | £100,000 |
| Contract duration | 24 months |
| Service availability | 95% |
| Payment terms | 30 days |
| Supplier reliability | 90% |

The purchasing agent rejects the proposal.

MARS conducts controlled experiments to investigate which commercial attributes influence the buyer's decision.

The system then searches for a minimum-cost modification that could satisfy the buyer's requirements while preserving supplier profitability.

This scenario is illustrative and does not represent an experimentally validated result.

---

## Proposed Technology Stack

- Python
- OpenAI API
- NumPy
- Pandas
- Scikit-learn
- SciPy
- Streamlit
- Plotly
- SQLite

Additional technologies will be selected as the experimental architecture develops.

---

## Research and Development Roadmap

### Phase 1 — Autonomous Buyer Simulation

Develop configurable purchasing agents with hidden commercial decision policies.

### Phase 2 — Black-Box Experimentation

Implement proposal submission, decision observation, and experimental data collection.

### Phase 3 — Buyer Policy Inference

Investigate algorithms for learning buyer decision patterns from experimental observations.

### Phase 4 — Minimum Winning Intervention

Develop an optimisation engine for identifying minimum-cost proposal modifications.

### Phase 5 — Autonomous Negotiation

Introduce multi-agent buyer-supplier negotiation.

### Phase 6 — Experimental Evaluation

Evaluate inference accuracy, intervention efficiency, commercial outcomes, and generalisation.

---

## Research Positioning

MARS is an experimental research and engineering project.

Its objective is to investigate the technical challenges of autonomous B2B procurement intelligence rather than claim that existing purchasing-agent technologies or negotiation algorithms are entirely new.

The project's research contribution will be assessed through literature review, system implementation, controlled experimentation, and comparison with established baseline methods.

---

## Project Status

Research architecture and initial development.

The proposed components are under development and should not be interpreted as completed or experimentally validated capabilities.

---

## Author

Kamran Khan

AI Decision Intelligence | B2B Sales | Business Intelligence | Autonomous Commercial Systems
