"""
MARS — Machine-Agent Revenue Science

Experiment 011

Autonomous AI Supplier Strategy Agent

Author: Kamran Khan

Purpose:
Investigate whether a generative AI supplier agent
can formulate commercial negotiation strategies
using observable buyer feedback while respecting
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

        self.strategy_history = []


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
    # VALIDATE AI COMMERCIAL STRATEGY
    # ==================================================

    def validate_strategy(self, proposal):

        if (

            proposal.annual_price <
            self.minimum_annual_price

        ):

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

                "cost": cost

            }

        return {

            "valid": True,

            "cost": cost

        }


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

        prompt = f"""

You are an autonomous B2B supplier negotiation agent.

Your objective is to develop a commercially viable
proposal that satisfies buyer requirements while
protecting supplier profitability.

ORIGINAL PROPOSAL:

{json.dumps(original, indent=2)}

CURRENT PROPOSAL:

{json.dumps(current, indent=2)}

BUYER FEEDBACK:

{json.dumps(buyer_feedback, indent=2)}

SUPPLIER CONSTRAINTS:

Minimum annual price:
{self.minimum_annual_price}

Maximum intervention cost:
{self.maximum_intervention_cost}

You must propose a revised commercial strategy.

You may modify:

annual_price
contract_months
service_availability
payment_days
supplier_reliability

Do not assume access to the buyer's hidden
procurement decision policy.

Return a JSON object containing:

annual_price
contract_months
service_availability
payment_days
supplier_reliability
reasoning

"""

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[

                {

                    "role": "system",

                    "content": (
                        "You are an autonomous commercial "
                        "negotiation strategy agent. "
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

        validation = self.validate_strategy(
            candidate
        )

        result = {

            "candidate": candidate,

            "reasoning": reasoning,

            "validation": validation

        }

        self.strategy_history.append(
            result
        )

        if validation["valid"]:

            self.current_proposal = candidate

        return result
