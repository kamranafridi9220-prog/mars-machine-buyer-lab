"""
MARS — Machine-Agent Revenue Science

Module:
Autonomous Buyer Laboratory

Purpose:
Simulate an autonomous B2B purchasing agent with
hidden commercial decision policies.

Author:
Kamran Khan
"""

from dataclasses import dataclass
from typing import Dict


# -------------------------------------------------
# COMMERCIAL PROPOSAL
# -------------------------------------------------

@dataclass
class CommercialProposal:

    annual_price: float

    contract_months: int

    service_availability: float

    payment_days: int

    supplier_reliability: float


# -------------------------------------------------
# AUTONOMOUS BUYER AGENT
# -------------------------------------------------

class AutonomousBuyerAgent:

    def __init__(self):

        # Hidden buyer decision policy

        self._max_budget = 105000

        self._minimum_service_availability = 98.0

        self._minimum_supplier_reliability = 85.0

        self._maximum_contract_months = 36

        self._minimum_payment_days = 30

        self._buyer_name = "Enterprise Procurement Agent"


    # -------------------------------------------------
    # PRIVATE BUYER POLICY
    # -------------------------------------------------

    def _evaluate_hidden_policy(
        self,
        proposal: CommercialProposal
    ) -> Dict:

        violations = []

        if proposal.annual_price > self._max_budget:

            violations.append("PRICE_CONSTRAINT")


        if proposal.service_availability < self._minimum_service_availability:

            violations.append("SERVICE_CONSTRAINT")


        if proposal.supplier_reliability < self._minimum_supplier_reliability:

            violations.append("RELIABILITY_CONSTRAINT")


        if proposal.contract_months > self._maximum_contract_months:

            violations.append("CONTRACT_CONSTRAINT")


        if proposal.payment_days < self._minimum_payment_days:

            violations.append("PAYMENT_CONSTRAINT")


        accepted = len(violations) == 0

        return {

            "accepted": accepted,

            "violations": violations

        }


    # -------------------------------------------------
    # PUBLIC BUYER RESPONSE
    # -------------------------------------------------

    def evaluate_proposal(
        self,
        proposal: CommercialProposal
    ) -> Dict:

        result = self._evaluate_hidden_policy(proposal)

        if result["accepted"]:

            decision = "ACCEPTED"

        else:

            decision = "REJECTED"


        return {

            "buyer": self._buyer_name,

            "decision": decision,

            "message": (
                "Proposal accepted."
                if result["accepted"]
                else "Proposal does not satisfy procurement requirements."
            )

        }
