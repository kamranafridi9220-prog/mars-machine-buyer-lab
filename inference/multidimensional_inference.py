"""
MARS — Machine-Agent Revenue Science

Experiment 003

Multi-Dimensional Black-Box Buyer Policy Inference

Author: Kamran Khan

Purpose:
Infer five hidden B2B purchasing constraints through
controlled commercial experimentation.

The inference engine does not access the buyer's
internal policy variables.
"""

from dataclasses import asdict, replace

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)


class MultiDimensionalInferenceEngine:

    def __init__(self, buyer):

        self.buyer = buyer

        self.history = []

        self.query_count = 0

        self.discovered_policies = {}


    # --------------------------------------------------
    # CREATE ACCEPTED REFERENCE PROPOSAL
    # --------------------------------------------------

    def create_reference_proposal(self):

        return CommercialProposal(

            annual_price=100000,

            contract_months=24,

            service_availability=99.0,

            payment_days=30,

            supplier_reliability=90.0

        )


    # --------------------------------------------------
    # SUBMIT PROPOSAL TO BLACK-BOX BUYER
    # --------------------------------------------------

    def evaluate(self, proposal, variable, value):

        response = self.buyer.evaluate_proposal(
            proposal
        )

        accepted = (
            response["decision"] == "ACCEPTED"
        )

        self.query_count += 1

        self.history.append({

            "query": self.query_count,

            "variable": variable,

            "tested_value": value,

            "decision": response["decision"],

            "proposal": asdict(proposal)

        })

        return accepted


    # --------------------------------------------------
    # DISCOVER HIDDEN COMMERCIAL THRESHOLD
    # --------------------------------------------------

    def infer_threshold(

        self,

        variable,

        lower,

        upper,

        direction,

        tolerance=0.01

    ):

        print("\n" + "=" * 60)

        print(
            f"DISCOVERING HIDDEN POLICY: {variable.upper()}"
        )

        print("=" * 60)

        reference = self.create_reference_proposal()

        # Test whether the reference proposal is accepted.

        if not self.evaluate(

            reference,

            variable,

            getattr(reference, variable)

        ):

            raise ValueError(

                "Reference proposal rejected. "
                "Cannot isolate individual constraints."

            )

        # Establish search boundaries.

        lower_proposal = replace(

            reference,

            **{variable: lower}

        )

        upper_proposal = replace(

            reference,

            **{variable: upper}

        )

        lower_accepted = self.evaluate(

            lower_proposal,

            variable,

            lower

        )

        upper_accepted = self.evaluate(

            upper_proposal,

            variable,

            upper

        )

        if direction == "maximum":

            if not lower_accepted or upper_accepted:

                raise ValueError(

                    f"Invalid maximum threshold boundaries "
                    f"for {variable}"

                )

        elif direction == "minimum":

            if lower_accepted or not upper_accepted:

                raise ValueError(

                    f"Invalid minimum threshold boundaries "
                    f"for {variable}"

                )

        else:

            raise ValueError(
                "Direction must be maximum or minimum."
            )

        experiment = 0

        while upper - lower > tolerance:

            experiment += 1

            midpoint = (lower + upper) / 2

            # Contract and payment periods are integers.

            if variable in [

                "contract_months",

                "payment_days"

            ]:

                midpoint = (lower + upper) // 2

                if midpoint == lower:

                    break

            proposal = replace(

                reference,

                **{variable: midpoint}

            )

            accepted = self.evaluate(

                proposal,

                variable,

                midpoint

            )

            print(

                f"Experiment {experiment} | "

                f"{variable}: {midpoint:.2f} | "

                f"{'ACCEPTED' if accepted else 'REJECTED'}"

            )

            if direction == "maximum":

                if accepted:

                    lower = midpoint

                else:

                    upper = midpoint

            else:

                if accepted:

                    upper = midpoint

                else:

                    lower = midpoint

        # For maximum constraints, lower is accepted.
        # For minimum constraints, upper is accepted.

        if direction == "maximum":

            estimated_threshold = lower

        else:

            estimated_threshold = upper

        self.discovered_policies[variable] = {

            "estimated_threshold": estimated_threshold,

            "lower_boundary": lower,

            "upper_boundary": upper,

            "uncertainty": upper - lower,

            "experiments": experiment

        }

        print("\nINFERENCE RESULT")

        print(

            f"Estimated threshold: "
            f"{estimated_threshold:.4f}"

        )

        print(

            f"Uncertainty interval: "
            f"{upper - lower:.4f}"

        )

        return self.discovered_policies[variable]


    # --------------------------------------------------
    # DISCOVER ALL BUYER POLICIES
    # --------------------------------------------------

    def discover_all_policies(self):

        print("\nMARS EXPERIMENT 003")

        print("MULTI-DIMENSIONAL BUYER POLICY DISCOVERY")

        print("=" * 60)

        configurations = [

            {

                "variable": "annual_price",

                "lower": 50000,

                "upper": 150000,

                "direction": "maximum",

                "tolerance": 1

            },

            {

                "variable": "service_availability",

                "lower": 90.0,

                "upper": 100.0,

                "direction": "minimum",

                "tolerance": 0.001

            },

            {

                "variable": "supplier_reliability",

                "lower": 60.0,

                "upper": 100.0,

                "direction": "minimum",

                "tolerance": 0.001

            },

            {

                "variable": "contract_months",

                "lower": 12,

                "upper": 60,

                "direction": "maximum",

                "tolerance": 1

            },

            {

                "variable": "payment_days",

                "lower": 7,

                "upper": 90,

                "direction": "minimum",

                "tolerance": 1

            }

        ]

        for configuration in configurations:

            self.infer_threshold(

                **configuration

            )

        print("\n" + "=" * 60)

        print("MARS DISCOVERED BUYER POLICY")

        print("=" * 60)

        for variable, result in (
            self.discovered_policies.items()
        ):

            print(

                f"{variable}: "

                f"{result['estimated_threshold']:.4f}"

            )

        print(

            f"\nTotal Buyer Queries: "
            f"{self.query_count}"

        )

        return self.discovered_policies
