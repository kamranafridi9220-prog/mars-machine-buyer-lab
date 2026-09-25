"""
MARS — Machine-Agent Revenue Science

Experiment 011

Autonomous AI Supplier Strategy Agent
Version 2 — Strategy Memory and Constraint-Aware Reasoning

Author: Kamran Khan

Purpose:
Investigate whether a generative AI supplier agent
can adapt commercial negotiation strategies using
previous experimental outcomes while respecting
supplier-side financial constraints.
"""

import json
import os

from dataclasses import asdict, replace

from openai import OpenAI


# ==================================================
# AUTONOMOUS AI SUPPLIER STRATEGY AGENT
# ==================================================

class AISupplierStrategyAgent:

    def __init__(
        self,
        original_proposal,
        maximum_intervention_cost=25000,
        minimum_annual_price=100000,
        model="gpt-4.1-mini"
    ):

        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

        self.model = model

        self.original_proposal = original_proposal

        self.current_proposal = original_proposal

        self.maximum_intervention_cost = (
            maximum_intervention_cost
        )

        self.minimum_annual_price = (
            minimum_annual_price
        )

        # Persistent within this agent instance.
        self.strategy_history = []

        self.buyer_feedback_history = []


    # ==================================================
    # CALCULATE COMMERCIAL INTERVENTION COST
    # ==================================================

    def calculate_cost(self, proposal):

        original = self.original_proposal

        price_cost = max(
            0,
            original.annual_price -
            proposal.annual_price
        )

        service_cost = max(
            0,
            proposal.service_availability -
            original.service_availability
        ) * 1500

        reliability_cost = max(
            0,
            proposal.supplier_reliability -
            original.supplier_reliability
        ) * 1000

        contract_cost = max(
            0,
            original.contract_months -
            proposal.contract_months
        ) * 250

        payment_cost = max(
            0,
            proposal.payment_days -
            original.payment_days
        ) * 100

        return (
            price_cost +
            service_cost +
            reliability_cost +
            contract_cost +
            payment_cost
        )


    # ==================================================
    # CALCULATE REMAINING INTERVENTION BUDGET
    # ==================================================

    def remaining_budget(self):

        current_cost = self.calculate_cost(
            self.current_proposal
        )

        return max(
            0,
            self.maximum_intervention_cost -
            current_cost
        )


    # ==================================================
    # VALIDATE AI COMMERCIAL STRATEGY
    # ==================================================

    def validate_strategy(self, proposal):

        if proposal.annual_price < self.minimum_annual_price:

            return {
                "valid": False,
                "reason": (
                    "AI strategy violates supplier "
                    "minimum annual price."
                )
            }

        cost = self.calculate_cost(proposal)

        if cost > self.maximum_intervention_cost:

            return {
                "valid": False,
                "reason": (
                    "AI strategy exceeds supplier "
                    "intervention budget."
                ),
                "cost": cost,
                "budget": self.maximum_intervention_cost
            }

        return {
            "valid": True,
            "cost": cost,
            "remaining_budget": (
                self.maximum_intervention_cost - cost
            )
        }


    # ==================================================
    # BUILD STRATEGY MEMORY
    # ==================================================

    def get_strategy_memory(self):

        memory = []

        for index, record in enumerate(
            self.strategy_history,
            start=1
        ):

            candidate = record["candidate"]

            validation = record["validation"]

            memory.append({

                "attempt": index,

                "proposal": asdict(candidate),

                "reasoning": record["reasoning"],

                "valid": validation["valid"],

                "validation_reason": validation.get(
                    "reason",
                    "Commercially feasible."
                ),

                "estimated_cost": validation.get(
                    "cost",
                    None
                )

            })

        return memory


    # ==================================================
    # RECORD BUYER FEEDBACK
    # ==================================================

    def record_buyer_feedback(
        self,
        proposal,
        feedback
    ):

        self.buyer_feedback_history.append({

            "proposal": asdict(proposal),

            "feedback": feedback

        })


    # ==================================================
    # GENERATE AI COMMERCIAL STRATEGY
    # ==================================================

    def generate_strategy(
        self,
        buyer_feedback
    ):

        current = asdict(
            self.current_proposal
        )

        original = asdict(
            self.original_proposal
        )

        memory = self.get_strategy_memory()

        current_cost = self.calculate_cost(
            self.current_proposal
        )

        remaining = self.remaining_budget()

        # ------------------------------------------
        # CONSTRUCT AI REASONING CONTEXT
        # ------------------------------------------

        context = {

            "original_proposal": original,

            "current_proposal": current,

            "latest_buyer_feedback": buyer_feedback,

            "previous_strategy_attempts": memory,

            "buyer_feedback_history": (
                self.buyer_feedback_history
            ),

            "supplier_constraints": {

                "minimum_annual_price": (
                    self.minimum_annual_price
                ),

                "maximum_intervention_cost": (
                    self.maximum_intervention_cost
                ),

                "current_intervention_cost": (
                    current_cost
                ),

                "remaining_intervention_budget": (
                    remaining
                )

            }

        }

        prompt = f"""

You are an autonomous AI supplier negotiation agent
operating within the MARS research environment.

Your objective is to formulate commercially viable
B2B negotiation strategies.

You must improve the probability of buyer acceptance
while protecting supplier financial constraints.

You do not have access to the buyer's hidden
procurement policy.

You may only use observable buyer feedback and
previous experimental outcomes.

EXPERIMENTAL CONTEXT:

{json.dumps(context, indent=2)}

IMPORTANT COMMERCIAL RULES:

1. Never propose an annual price below the
   supplier minimum annual price.

2. Never exceed the maximum cumulative
   intervention budget.

3. Review previous rejected strategies.

4. Avoid repeating previously unsuccessful
   commercial proposals.

5. Consider the cost of each commercial concession.

6. Do not assume that buyer rejection reveals
   which individual commercial constraint failed.

7. Generate a revised proposal using the
   available experimental evidence.

You may modify:

annual_price
contract_months
service_availability
payment_days
supplier_reliability

Return a valid JSON object containing:

annual_price
contract_months
service_availability
payment_days
supplier_reliability
reasoning

"""

        # ------------------------------------------
        # OPENAI STRATEGY GENERATION
        # ------------------------------------------

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[

                {

                    "role": "system",

                    "content": (
                        "You are an autonomous AI "
                        "commercial negotiation agent. "
                        "Generate commercially feasible "
                        "strategies using experimental "
                        "memory and buyer feedback. "
                        "Return valid JSON only."
                    )

                },

                {

                    "role": "user",

                    "content": prompt

                }

            ],

            response_format={
                "type": "json_object"
            }

        )

        strategy = json.loads(
            response.choices[0].message.content
        )

        reasoning = strategy.pop(
            "reasoning",
            "No reasoning provided."
        )

        allowed_fields = set(
            asdict(self.current_proposal)
        )

        proposed_fields = {

            key: value

            for key, value in strategy.items()

            if key in allowed_fields

        }

        candidate = replace(
            self.current_proposal,
            **proposed_fields
        )

        # ------------------------------------------
        # VALIDATE GENERATED STRATEGY
        # ------------------------------------------

        validation = self.validate_strategy(
            candidate
        )

        result = {

            "candidate": candidate,

            "reasoning": reasoning,

            "validation": validation

        }

        # ------------------------------------------
        # STORE STRATEGY IN MEMORY
        # ------------------------------------------

        self.strategy_history.append(
            result
        )

        # ------------------------------------------
        # UPDATE CURRENT PROPOSAL
        # ------------------------------------------

        if validation["valid"]:

            self.current_proposal = candidate

        return result
