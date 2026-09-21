"""
MARS — Machine-Agent Revenue Science

Module:
Black-Box Buyer Policy Inference Engine

Experiment 002:
Discovering hidden buyer price constraints.

Author:
Kamran Khan
"""

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)


class BuyerPolicyInferenceEngine:

    def __init__(self, buyer):

        self.buyer = buyer

        self.experiment_history = []


    def create_proposal(self, price):

        return CommercialProposal(

            annual_price=price,

            contract_months=24,

            service_availability=99.0,

            payment_days=30,

            supplier_reliability=90.0

        )


    def test_price(self, price):

        proposal = self.create_proposal(price)

        response = self.buyer.evaluate_proposal(proposal)

        accepted = response["decision"] == "ACCEPTED"

        self.experiment_history.append({

            "price": price,

            "accepted": accepted

        })

        return accepted


    def infer_maximum_price(

        self,

        minimum_price=50000,

        maximum_price=150000,

        tolerance=1

    ):

        print("\nMARS BLACK-BOX BUYER POLICY INFERENCE")

        print("=" * 55)

        lower = minimum_price

        upper = maximum_price

        experiment = 0

        # Validate the initial search boundaries.

        if not self.test_price(lower):

            raise ValueError(
                "Minimum price was rejected. "
                "Cannot establish an accepted lower boundary."
            )

        if self.test_price(upper):

            raise ValueError(
                "Maximum price was accepted. "
                "Increase the upper search boundary."
            )

        print(f"\nAccepted lower boundary: £{lower:,.2f}")

        print(f"Rejected upper boundary: £{upper:,.2f}")

        while upper - lower > tolerance:

            experiment += 1

            midpoint = (lower + upper) / 2

            accepted = self.test_price(midpoint)

            decision = (

                "ACCEPTED"

                if accepted

                else "REJECTED"

            )

            print(f"\nExperiment {experiment}")

            print(f"Tested Price: £{midpoint:,.2f}")

            print(f"Buyer Decision: {decision}")

            if accepted:

                lower = midpoint

            else:

                upper = midpoint

        print("\n" + "=" * 55)

        print("INFERENCE COMPLETED")

        print(f"\nEstimated Maximum Accepted Price: £{lower:,.2f}")

        print(f"First Rejected Boundary: £{upper:,.2f}")

        print(f"Final Uncertainty Interval: £{upper - lower:,.2f}")

        print(f"Binary Search Experiments: {experiment}")

        print(f"Total Buyer Queries: {len(self.experiment_history)}")

        return {

            "estimated_maximum_price": lower,

            "rejected_boundary": upper,

            "uncertainty": upper - lower,

            "experiments": experiment,

            "total_queries": len(self.experiment_history),

            "history": self.experiment_history

        }
