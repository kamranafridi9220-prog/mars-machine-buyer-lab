"""
MARS — Machine-Agent Revenue Science

Experiment 006

Adaptive Negotiation Intelligence

Author: Kamran Khan

Purpose:
Enable an autonomous supplier to learn from
previous buyer negotiations and adapt future
commercial proposals.

The supplier does not access the buyer's
hidden internal purchasing policy.

Version:
Corrected negotiation memory persistence.
"""

from dataclasses import replace

from negotiation.negotiation_lab import (
    SupplierNegotiationAgent
)


# ==================================================
# NEGOTIATION MEMORY ENGINE
# ==================================================

class NegotiationMemoryEngine:

    def __init__(self):

        self.buyer_memories = {}

        self.total_learned_interventions = 0

    # --------------------------------------------------
    # LEARN FROM SUCCESSFUL NEGOTIATION
    # --------------------------------------------------

    def learn_from_negotiation(
        self,
        buyer_id,
        negotiation_result
    ):

        if not negotiation_result["agreement"]:

            print(
                "Negotiation unsuccessful. "
                "No winning policy stored."
            )

            return False

        # --------------------------------------------------
        # RETRIEVE EXISTING BUYER MEMORY
        # --------------------------------------------------

        # Important:
        # Previously learned buyer requirements must
        # survive subsequent successful negotiations.
        #
        # A negotiation with zero counteroffers must
        # not erase historical commercial intelligence.

        previous_memory = self.buyer_memories.get(
            buyer_id,
            {}
        )

        learned_requirements = previous_memory.get(
            "learned_requirements",
            {}
        ).copy()

        # Count only new observations from this
        # particular negotiation.

        new_observations = 0

        # --------------------------------------------------
        # LEARN FROM BUYER COUNTEROFFERS
        # --------------------------------------------------

        for event in negotiation_result["history"]:

            supplier_response = event[
                "supplier_response"
            ]

            if not supplier_response["accepted"]:

                continue

            counteroffer = event[
                "buyer_counteroffer"
            ]

            variable = counteroffer["variable"]

            requested_value = counteroffer[
                "requested_value"
            ]

            # Update the buyer's learned requirement.

            learned_requirements[
                variable
            ] = requested_value

            new_observations += 1

        # --------------------------------------------------
        # UPDATE PERSISTENT BUYER MEMORY
        # --------------------------------------------------

        self.buyer_memories[buyer_id] = {

            "learned_requirements":
                learned_requirements,

            "previous_agreement":
                negotiation_result[
                    "final_proposal"
                ],

            "previous_cost":
                negotiation_result[
                    "total_cost"
                ],

            "previous_rounds":
                negotiation_result[
                    "rounds"
                ]

        }

        self.total_learned_interventions += (
            new_observations
        )

        # --------------------------------------------------
        # DISPLAY MEMORY UPDATE
        # --------------------------------------------------

        print("\nNEGOTIATION MEMORY UPDATED")

        print("=" * 60)

        print(
            f"Buyer: {buyer_id}"
        )

        print(
            f"New observations: "
            f"{new_observations}"
        )

        print(
            f"Total remembered requirements: "
            f"{len(learned_requirements)}"
        )

        print(
            f"Total learned interventions: "
            f"{self.total_learned_interventions}"
        )

        for variable, value in (
            learned_requirements.items()
        ):

            print(
                f"{variable}: {value}"
            )

        return True

    # --------------------------------------------------
    # RETRIEVE BUYER MEMORY
    # --------------------------------------------------

    def retrieve_memory(
        self,
        buyer_id
    ):

        return self.buyer_memories.get(
            buyer_id
        )

    # --------------------------------------------------
    # CHECK WHETHER BUYER IS KNOWN
    # --------------------------------------------------

    def has_memory(
        self,
        buyer_id
    ):

        return buyer_id in self.buyer_memories


# ==================================================
# ADAPTIVE SUPPLIER AGENT
# ==================================================

class AdaptiveSupplierAgent(
    SupplierNegotiationAgent
):

    def __init__(
        self,
        original_proposal,
        memory_engine,
        buyer_id,
        maximum_intervention_cost=25000,
        minimum_annual_price=100000
    ):

        super().__init__(

            original_proposal,

            maximum_intervention_cost=
                maximum_intervention_cost,

            minimum_annual_price=
                minimum_annual_price

        )

        self.memory_engine = memory_engine

        self.buyer_id = buyer_id

        self.used_memory = False

    # --------------------------------------------------
    # PREPARE ADAPTIVE OPENING PROPOSAL
    # --------------------------------------------------

    def prepare_adaptive_proposal(self):

        print("\nADAPTIVE SUPPLIER INTELLIGENCE")

        print("=" * 60)

        memory = self.memory_engine.retrieve_memory(
            self.buyer_id
        )

        # --------------------------------------------------
        # UNKNOWN BUYER
        # --------------------------------------------------

        if memory is None:

            print(
                "Unknown buyer. "
                "Starting exploratory negotiation."
            )

            return self.current_proposal

        print(
            "Previous buyer negotiation "
            "memory discovered."
        )

        learned_requirements = memory[
            "learned_requirements"
        ]

        # --------------------------------------------------
        # BUILD ADAPTIVE PROPOSAL
        # --------------------------------------------------

        candidate = self.original_proposal

        # Apply previously accepted commercial
        # concessions to the new proposal.

        for variable, value in (
            learned_requirements.items()
        ):

            candidate = replace(

                candidate,

                **{variable: value}

            )

        # --------------------------------------------------
        # PROTECT SUPPLIER MINIMUM PRICE
        # --------------------------------------------------

        if (
            candidate.annual_price <
            self.minimum_annual_price
        ):

            print(
                "Learned proposal violates "
                "supplier minimum price."
            )

            return self.current_proposal

        # --------------------------------------------------
        # PROTECT SUPPLIER CONCESSION BUDGET
        # --------------------------------------------------

        estimated_cost = self.calculate_cost(
            candidate
        )

        if (
            estimated_cost >
            self.maximum_intervention_cost
        ):

            print(
                "Learned proposal exceeds "
                "supplier concession budget."
            )

            return self.current_proposal

        # --------------------------------------------------
        # APPLY LEARNED COMMERCIAL STRATEGY
        # --------------------------------------------------

        self.current_proposal = candidate

        self.used_memory = True

        print(
            "Adaptive opening proposal generated."
        )

        print(
            f"Estimated concession cost: "
            f"£{estimated_cost:,.2f}"
        )

        print(
            f"Annual price: "
            f"£{candidate.annual_price:,.2f}"
        )

        print(
            f"Service availability: "
            f"{candidate.service_availability}%"
        )

        print(
            f"Supplier reliability: "
            f"{candidate.supplier_reliability}%"
        )

        print(
            f"Contract duration: "
            f"{candidate.contract_months} months"
        )

        print(
            f"Payment period: "
            f"{candidate.payment_days} days"
        )

        return candidate
