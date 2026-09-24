"""
MARS — Machine-Agent Revenue Science

Experiment 007

Buyer Policy Drift Detection and Adaptive Recovery

Author: Kamran Khan

Research objective:

Detect changes in autonomous buyer purchasing
requirements and selectively update previously
learned commercial intelligence.

This module uses a simulated buyer evaluation
interface rather than direct access to hidden
buyer policies.
"""

from dataclasses import replace
from copy import deepcopy


# ==================================================
# POLICY DRIFT DETECTION ENGINE
# ==================================================

class BuyerPolicyDriftEngine:

    def __init__(
        self,
        buyer,
        memory_engine,
        buyer_id
    ):

        self.buyer = buyer

        self.memory_engine = memory_engine

        self.buyer_id = buyer_id

        self.query_count = 0

        self.detected_changes = {}

    # --------------------------------------------------
    # QUERY AUTONOMOUS BUYER
    # --------------------------------------------------

    def query_buyer(self, proposal):

        self.query_count += 1

        response = self.buyer.evaluate_proposal(
            proposal
        )

        return response

    # --------------------------------------------------
    # DETECT POLICY DRIFT
    # --------------------------------------------------

    def detect_drift(self):

        memory = self.memory_engine.retrieve_memory(
            self.buyer_id
        )

        if memory is None:

            raise ValueError(
                "No previous buyer memory available."
            )

        previous_agreement = memory[
            "previous_agreement"
        ]

        response = self.query_buyer(
            previous_agreement
        )

        decision = response[
            "decision"
        ]

        print("\nPOLICY DRIFT DETECTION")

        print("=" * 60)

        print(
            f"Previous agreement decision: "
            f"{decision}"
        )

        if decision == "ACCEPTED":

            print(
                "Previous commercial agreement "
                "remains acceptable."
            )

            return False

        print(
            "Previously accepted proposal rejected."
        )

        print(
            "Potential buyer policy drift detected."
        )

        return True

    # --------------------------------------------------
    # DISCOVER CHANGED REQUIREMENTS
    # --------------------------------------------------

    def discover_changes(
        self,
        candidate_values
    ):

        memory = self.memory_engine.retrieve_memory(
            self.buyer_id
        )

        if memory is None:

            raise ValueError(
                "No buyer memory available."
            )

        previous_agreement = memory[
            "previous_agreement"
        ]

        self.detected_changes = {}

        print("\nSELECTIVE POLICY REDISCOVERY")

        print("=" * 60)

        # The candidate values represent commercial
        # terms the supplier is willing to investigate.
        #
        # They are not supplied directly by the buyer.

        for variable, values in (
            candidate_values.items()
        ):

            print(
                f"\nInvestigating: {variable}"
            )

            successful_value = None

            for value in values:

                candidate = replace(

                    previous_agreement,

                    **{variable: value}

                )

                response = self.query_buyer(
                    candidate
                )

                if (
                    response["decision"] ==
                    "ACCEPTED"
                ):

                    successful_value = value

                    break

            if successful_value is not None:

                original_value = getattr(

                    previous_agreement,

                    variable

                )

                if (
                    successful_value !=
                    original_value
                ):

                    self.detected_changes[
                        variable
                    ] = successful_value

                    print(
                        f"Potential change: "
                        f"{original_value} -> "
                        f"{successful_value}"
                    )

        return deepcopy(
            self.detected_changes
        )

    # --------------------------------------------------
    # RECOVER COMMERCIAL PROPOSAL
    # --------------------------------------------------

    def recover_proposal(
        self,
        candidate_values
    ):

        memory = self.memory_engine.retrieve_memory(
            self.buyer_id
        )

        if memory is None:

            raise ValueError(
                "No previous buyer memory available."
            )

        previous_agreement = memory[
            "previous_agreement"
        ]

        # Begin with the previously accepted
        # commercial proposal.

        recovered = previous_agreement

        print("\nADAPTIVE POLICY RECOVERY")

        print("=" * 60)

        # Investigate candidate modifications
        # incrementally.
        #
        # A single changed variable may not be
        # sufficient to satisfy the buyer.

        for variable, values in (
            candidate_values.items()
        ):

            for value in values:

                candidate = replace(

                    recovered,

                    **{variable: value}

                )

                response = self.query_buyer(
                    candidate
                )

                recovered = candidate

                if (
                    response["decision"] ==
                    "ACCEPTED"
                ):

                    print(
                        "Buyer acceptance recovered."
                    )

                    return recovered

        final_response = self.query_buyer(
            recovered
        )

        if (
            final_response["decision"] ==
            "ACCEPTED"
        ):

            print(
                "Buyer acceptance recovered."
            )

            return recovered

        print(
            "No acceptable proposal found "
            "within candidate search."
        )

        return None
