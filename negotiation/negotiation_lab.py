"""
MARS — Machine-Agent Revenue Science

Experiment 005

Autonomous Buyer-Supplier Negotiation Laboratory

Author: Kamran Khan

Purpose:
Simulate structured B2B negotiations between
autonomous buyer and supplier agents.

The buyer issues counteroffers.

The supplier evaluates commercial concessions
before accepting or rejecting them.
"""

from dataclasses import asdict, replace


# ==================================================
# BUYER NEGOTIATION AGENT
# ==================================================

class BuyerNegotiationAgent:

    def __init__(self, buyer, requirements):

        self.buyer = buyer

        # Buyer-side negotiation policy.
        # These values are not passed to the supplier.

        self._requirements = requirements.copy()

        self.negotiation_history = []


    def evaluate_offer(self, proposal):

        response = self.buyer.evaluate_proposal(
            proposal
        )

        accepted = (
            response["decision"] == "ACCEPTED"
        )

        if accepted:

            return {

                "decision": "ACCEPTED",

                "counteroffer": None,

                "message": "Commercial agreement accepted."

            }

        # The buyer selectively discloses one
        # commercial requirement per negotiation round.

        requirements = self._requirements

        checks = [

            (
                "annual_price",

                proposal.annual_price >
                requirements["annual_price"]

            ),

            (
                "service_availability",

                proposal.service_availability <
                requirements["service_availability"]

            ),

            (
                "supplier_reliability",

                proposal.supplier_reliability <
                requirements["supplier_reliability"]

            ),

            (
                "contract_months",

                proposal.contract_months >
                requirements["contract_months"]

            ),

            (
                "payment_days",

                proposal.payment_days <
                requirements["payment_days"]

            )

        ]

        for variable, violated in checks:

            if violated:

                target = requirements[variable]

                counteroffer = {

                    "variable": variable,

                    "requested_value": target

                }

                self.negotiation_history.append(
                    counteroffer
                )

                return {

                    "decision": "COUNTEROFFER",

                    "counteroffer": counteroffer,

                    "message": (
                        "Buyer requests modification "
                        f"to {variable}."
                    )

                }

        # This can occur if the negotiation policy
        # and underlying buyer policy disagree.

        return {

            "decision": "REJECTED",

            "counteroffer": None,

            "message": (
                "Buyer rejected the proposal without "
                "an available counteroffer."
            )

        }


# ==================================================
# SUPPLIER NEGOTIATION AGENT
# ==================================================

class SupplierNegotiationAgent:

    def __init__(

        self,

        original_proposal,

        maximum_intervention_cost=25000,

        minimum_annual_price=100000

    ):

        self.original_proposal = original_proposal

        self.current_proposal = original_proposal

        self.maximum_intervention_cost = (
            maximum_intervention_cost
        )

        self.minimum_annual_price = (
            minimum_annual_price
        )

        self.negotiation_history = []


    # --------------------------------------------------
    # CALCULATE COMMERCIAL CONCESSION COST
    # --------------------------------------------------

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


    # --------------------------------------------------
    # EVALUATE BUYER COUNTEROFFER
    # --------------------------------------------------

    def respond_to_counteroffer(

        self,

        counteroffer

    ):

        variable = counteroffer["variable"]

        requested_value = counteroffer[
            "requested_value"
        ]

        # Reject unknown commercial variables.

        if variable not in asdict(
            self.current_proposal
        ):

            return {

                "accepted": False,

                "reason": "Unknown commercial variable."

            }

        candidate = replace(

            self.current_proposal,

            **{variable: requested_value}

        )

        # Protect minimum acceptable annual price.

        if (

            candidate.annual_price <
            self.minimum_annual_price

        ):

            return {

                "accepted": False,

                "reason": (
                    "Requested price violates "
                    "supplier minimum price."
                )

            }

        # Calculate total cumulative concessions.

        estimated_cost = self.calculate_cost(
            candidate
        )

        if (

            estimated_cost >
            self.maximum_intervention_cost

        ):

            return {

                "accepted": False,

                "reason": (
                    "Requested concession exceeds "
                    "supplier intervention budget."
                ),

                "estimated_cost": estimated_cost

            }

        # Accept commercially feasible counteroffer.

        self.current_proposal = candidate

        self.negotiation_history.append({

            "variable": variable,

            "accepted_value": requested_value,

            "cumulative_cost": estimated_cost

        })

        return {

            "accepted": True,

            "proposal": candidate,

            "estimated_cost": estimated_cost

        }


# ==================================================
# AUTONOMOUS NEGOTIATION ENVIRONMENT
# ==================================================

class AutonomousNegotiationEnvironment:

    def __init__(

        self,

        buyer_agent,

        supplier_agent,

        maximum_rounds=10

    ):

        self.buyer = buyer_agent

        self.supplier = supplier_agent

        self.maximum_rounds = maximum_rounds

        self.history = []


    # --------------------------------------------------
    # RUN AUTONOMOUS NEGOTIATION
    # --------------------------------------------------

    def negotiate(self):

        print("\nMARS EXPERIMENT 005")

        print("AUTONOMOUS B2B NEGOTIATION")

        print("=" * 60)

        for round_number in range(

            1,

            self.maximum_rounds + 1

        ):

            print(

                f"\nNEGOTIATION ROUND {round_number}"

            )

            proposal = (
                self.supplier.current_proposal
            )

            buyer_response = (
                self.buyer.evaluate_offer(
                    proposal
                )
            )

            print(

                "Buyer Decision: " +

                buyer_response["decision"]

            )

            # --------------------------------------
            # AGREEMENT REACHED
            # --------------------------------------

            if (

                buyer_response["decision"] ==
                "ACCEPTED"

            ):

                final_cost = (
                    self.supplier.calculate_cost(
                        proposal
                    )
                )

                print("\nAGREEMENT REACHED")

                print(

                    f"Final Annual Price: "
                    f"£{proposal.annual_price:,.2f}"

                )

                print(

                    f"Total Intervention Cost: "
                    f"£{final_cost:,.2f}"

                )

                return {

                    "agreement": True,

                    "rounds": round_number,

                    "final_proposal": proposal,

                    "total_cost": final_cost,

                    "history": self.history

                }

            # --------------------------------------
            # BUYER REJECTED WITHOUT COUNTEROFFER
            # --------------------------------------

            if (

                buyer_response["decision"] !=
                "COUNTEROFFER"

            ):

                print(

                    "Negotiation ended: " +
                    buyer_response["message"]

                )

                break

            counteroffer = (
                buyer_response["counteroffer"]
            )

            print(

                "Buyer requests: " +

                str(counteroffer)

            )

            # --------------------------------------
            # SUPPLIER EVALUATES COUNTEROFFER
            # --------------------------------------

            supplier_response = (
                self.supplier.respond_to_counteroffer(
                    counteroffer
                )
            )

            self.history.append({

                "round": round_number,

                "buyer_counteroffer": counteroffer,

                "supplier_response": supplier_response

            })

            if not supplier_response["accepted"]:

                print(

                    "Supplier rejected counteroffer."

                )

                print(

                    supplier_response["reason"]

                )

                break

            print(

                "Supplier accepted counteroffer."

            )

            print(

                f"Cumulative Concession Cost: "
                f"£{supplier_response['estimated_cost']:,.2f}"

            )

        # ------------------------------------------
        # NEGOTIATION FAILED
        # ------------------------------------------

        print("\nNEGOTIATION ENDED WITHOUT AGREEMENT")

        return {

            "agreement": False,

            "rounds": len(self.history),

            "final_proposal": (
                self.supplier.current_proposal
            ),

            "total_cost": (
                self.supplier.calculate_cost(
                    self.supplier.current_proposal
                )
            ),

            "history": self.history

        }
