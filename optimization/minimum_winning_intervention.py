"""
MARS — Machine-Agent Revenue Science

Experiment 004

Minimum Winning Intervention Engine

Author: Kamran Khan

Purpose:
Identify minimum-cost commercial modifications
that transform a rejected supplier proposal
into an acceptable proposal.

The engine uses inferred buyer requirements,
not the buyer's hidden internal policy.
"""

from dataclasses import asdict, replace


class MinimumWinningInterventionEngine:

    def __init__(self, buyer, discovered_policies):

        self.buyer = buyer

        self.discovered_policies = discovered_policies

        self.interventions = []

    # --------------------------------------------------
    # GET INFERRED BUYER REQUIREMENT
    # --------------------------------------------------

    def get_threshold(self, variable):

        return self.discovered_policies[
            variable
        ]["estimated_threshold"]

    # --------------------------------------------------
    # EVALUATE ORIGINAL PROPOSAL
    # --------------------------------------------------

    def evaluate_proposal(self, proposal):

        response = self.buyer.evaluate_proposal(
            proposal
        )

        return response["decision"] == "ACCEPTED"

    # --------------------------------------------------
    # OPTIMISE COMMERCIAL PROPOSAL
    # --------------------------------------------------

    def optimise(self, original_proposal):

        print("\nMARS EXPERIMENT 004")

        print("MINIMUM WINNING INTERVENTION")

        print("=" * 60)

        self.interventions = []

        original = asdict(original_proposal)

        modified = original.copy()

        # ----------------------------------------------
        # INFERRED BUYER REQUIREMENTS
        # ----------------------------------------------

        max_price = self.get_threshold(
            "annual_price"
        )

        min_service = self.get_threshold(
            "service_availability"
        )

        min_reliability = self.get_threshold(
            "supplier_reliability"
        )

        max_contract = self.get_threshold(
            "contract_months"
        )

        min_payment = self.get_threshold(
            "payment_days"
        )

        # ----------------------------------------------
        # PRICE INTERVENTION
        # ----------------------------------------------

        if modified["annual_price"] > max_price:

            old_value = modified["annual_price"]

            # Use the inferred accepted price boundary.

            modified["annual_price"] = round(
                max_price,
                2
            )

            self.interventions.append({

                "variable": "annual_price",

                "original": old_value,

                "modified": modified["annual_price"],

                "cost": (
                    old_value -
                    modified["annual_price"]
                )

            })

        # ----------------------------------------------
        # SERVICE INTERVENTION
        # ----------------------------------------------

        if modified["service_availability"] < min_service:

            old_value = modified[
                "service_availability"
            ]

            # Round upward to avoid falling below
            # the inferred minimum requirement.

            new_value = (
                int(min_service * 100 + 0.999999)
                / 100
            )

            modified[
                "service_availability"
            ] = new_value

            improvement = (
                new_value - old_value
            )

            estimated_cost = (
                improvement * 1500
            )

            self.interventions.append({

                "variable": "service_availability",

                "original": old_value,

                "modified": new_value,

                "cost": estimated_cost

            })

        # ----------------------------------------------
        # RELIABILITY INTERVENTION
        # ----------------------------------------------

        if modified["supplier_reliability"] < min_reliability:

            old_value = modified[
                "supplier_reliability"
            ]

            new_value = (
                int(min_reliability * 100 + 0.999999)
                / 100
            )

            modified[
                "supplier_reliability"
            ] = new_value

            improvement = (
                new_value - old_value
            )

            estimated_cost = (
                improvement * 1000
            )

            self.interventions.append({

                "variable": "supplier_reliability",

                "original": old_value,

                "modified": new_value,

                "cost": estimated_cost

            })

        # ----------------------------------------------
        # CONTRACT INTERVENTION
        # ----------------------------------------------

        if modified["contract_months"] > max_contract:

            old_value = modified[
                "contract_months"
            ]

            new_value = int(
                max_contract
            )

            modified[
                "contract_months"
            ] = new_value

            estimated_cost = (
                old_value - new_value
            ) * 250

            self.interventions.append({

                "variable": "contract_months",

                "original": old_value,

                "modified": new_value,

                "cost": estimated_cost

            })

        # ----------------------------------------------
        # PAYMENT INTERVENTION
        # ----------------------------------------------

        if modified["payment_days"] < min_payment:

            old_value = modified[
                "payment_days"
            ]

            new_value = int(
                min_payment + 0.999999
            )

            modified[
                "payment_days"
            ] = new_value

            estimated_cost = (
                new_value - old_value
            ) * 100

            self.interventions.append({

                "variable": "payment_days",

                "original": old_value,

                "modified": new_value,

                "cost": estimated_cost

            })

        # ----------------------------------------------
        # CREATE MODIFIED PROPOSAL
        # ----------------------------------------------

        winning_proposal = replace(

            original_proposal,

            **modified

        )

        # ----------------------------------------------
        # VERIFY BUYER ACCEPTANCE
        # ----------------------------------------------

        accepted = self.evaluate_proposal(
            winning_proposal
        )

        total_cost = sum(

            intervention["cost"]

            for intervention in self.interventions

        )

        print("\nORIGINAL PROPOSAL")

        for variable, value in original.items():

            print(f"{variable}: {value}")

        print("\nRECOMMENDED INTERVENTIONS")

        for intervention in self.interventions:

            print(

                f"\n{intervention['variable']}"

                f"\nOriginal: {intervention['original']}"

                f"\nModified: {intervention['modified']}"

                f"\nEstimated Cost: "
                f"£{intervention['cost']:,.2f}"

            )

        print("\n" + "=" * 60)

        print("OPTIMISATION RESULT")

        print("=" * 60)

        print(

            f"Total Estimated Intervention Cost: "
            f"£{total_cost:,.2f}"

        )

        print(

            f"Buyer Decision: "
            f"{'ACCEPTED' if accepted else 'REJECTED'}"

        )

        return {

            "original_proposal": original_proposal,

            "winning_proposal": winning_proposal,

            "interventions": self.interventions,

            "total_cost": total_cost,

            "accepted": accepted

        }
