"""
MARS — Machine-Agent Revenue Science

Experiment 012

Buyer Policy Belief Model

Author: Kamran Khan

Purpose:
Maintain structured estimates of hidden buyer
procurement requirements using experimental
evidence from black-box policy inference.

The belief model does not access the buyer's
private decision policy.
"""

from dataclasses import asdict


# ==================================================
# BUYER POLICY BELIEF MODEL
# ==================================================

class BuyerPolicyBeliefModel:

    def __init__(self):

        self.policy_beliefs = {}

        self.belief_history = []

        self.commercial_variables = [

            "annual_price",

            "contract_months",

            "service_availability",

            "payment_days",

            "supplier_reliability"

        ]


    # ==================================================
    # UPDATE BELIEFS FROM INFERENCE RESULTS
    # ==================================================

    def update_from_inference(
        self,
        inference_results
    ):

        for variable, result in (
            inference_results.items()
        ):

            if variable not in self.commercial_variables:

                continue

            belief = {

                "estimated_threshold": (
                    result["estimated_threshold"]
                ),

                "lower_boundary": (
                    result["lower_boundary"]
                ),

                "upper_boundary": (
                    result["upper_boundary"]
                ),

                "uncertainty": (
                    result["uncertainty"]
                ),

                "experiments": (
                    result["experiments"]
                )

            }

            self.policy_beliefs[variable] = belief

            self.belief_history.append({

                "variable": variable,

                "belief": belief.copy()

            })

        return self.policy_beliefs


    # ==================================================
    # RETRIEVE ESTIMATED BUYER POLICY
    # ==================================================

    def get_estimated_policy(self):

        return {

            variable: result["estimated_threshold"]

            for variable, result in (
                self.policy_beliefs.items()
            )

        }


    # ==================================================
    # RETRIEVE UNCERTAINTY
    # ==================================================

    def get_policy_uncertainty(self):

        return {

            variable: result["uncertainty"]

            for variable, result in (
                self.policy_beliefs.items()
            )

        }


    # ==================================================
    # EVALUATE PROPOSAL AGAINST ESTIMATED POLICY
    # ==================================================

    def evaluate_against_beliefs(
        self,
        proposal
    ):

        proposal_data = asdict(proposal)

        estimated_policy = (
            self.get_estimated_policy()
        )

        directions = {

            "annual_price": "maximum",

            "contract_months": "maximum",

            "service_availability": "minimum",

            "payment_days": "minimum",

            "supplier_reliability": "minimum"

        }

        violations = []

        for variable, threshold in (
            estimated_policy.items()
        ):

            value = proposal_data[variable]

            direction = directions[variable]

            if direction == "maximum":

                if value > threshold:

                    violations.append({

                        "variable": variable,

                        "proposed_value": value,

                        "estimated_threshold": threshold

                    })

            else:

                if value < threshold:

                    violations.append({

                        "variable": variable,

                        "proposed_value": value,

                        "estimated_threshold": threshold

                    })

        return {

            "estimated_acceptance": (
                len(violations) == 0
            ),

            "estimated_violations": violations,

            "evaluated_variables": len(
                estimated_policy
            )

        }


    # ==================================================
    # GENERATE BELIEF REPORT
    # ==================================================

    def generate_belief_report(self):

        print("\n" + "=" * 65)

        print("MARS BUYER POLICY BELIEF REPORT")

        print("=" * 65)

        for variable, belief in (
            self.policy_beliefs.items()
        ):

            print(

                f"\nVariable: {variable}"

            )

            print(

                "Estimated Threshold:",

                belief["estimated_threshold"]

            )

            print(

                "Uncertainty:",

                belief["uncertainty"]

            )

            print(

                "Experimental Queries:",

                belief["experiments"]

            )

        print("\n" + "=" * 65)

        return self.get_estimated_policy()
