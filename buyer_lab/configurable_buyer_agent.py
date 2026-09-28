"""
MARS — Machine-Agent Revenue Science

Experiment 017

Configurable Autonomous Buyer Laboratory

Author: Kamran Khan

Purpose:
Create multiple autonomous B2B buyer environments
with different hidden procurement policies.

This module enables MARS discovery algorithms to be
evaluated across heterogeneous buyer configurations
rather than against a single fixed buyer policy.

The hidden procurement thresholds remain private to
the buyer agent and are not exposed to discovery
algorithms during experimentation.
"""

from dataclasses import dataclass
from typing import Dict


# ============================================================
# COMMERCIAL PROPOSAL
# ============================================================

@dataclass
class ConfigurableCommercialProposal:

    annual_price: float

    contract_months: int

    service_availability: float

    payment_days: int

    supplier_reliability: float


# ============================================================
# CONFIGURABLE AUTONOMOUS BUYER
# ============================================================

class ConfigurableAutonomousBuyer:

    def __init__(
        self,
        buyer_name,
        max_budget,
        maximum_contract_months,
        minimum_service_availability,
        minimum_payment_days,
        minimum_supplier_reliability
    ):

        self._buyer_name = buyer_name

        self._max_budget = max_budget

        self._maximum_contract_months = (
            maximum_contract_months
        )

        self._minimum_service_availability = (
            minimum_service_availability
        )

        self._minimum_payment_days = (
            minimum_payment_days
        )

        self._minimum_supplier_reliability = (
            minimum_supplier_reliability
        )


    # ========================================================
    # PRIVATE BUYER POLICY
    # ========================================================

    def _evaluate_hidden_policy(
        self,
        proposal
    ) -> Dict:

        violations = []


        if (
            proposal.annual_price
            >
            self._max_budget
        ):

            violations.append(
                "PRICE_CONSTRAINT"
            )


        if (
            proposal.contract_months
            >
            self._maximum_contract_months
        ):

            violations.append(
                "CONTRACT_CONSTRAINT"
            )


        if (
            proposal.service_availability
            <
            self._minimum_service_availability
        ):

            violations.append(
                "SERVICE_CONSTRAINT"
            )


        if (
            proposal.payment_days
            <
            self._minimum_payment_days
        ):

            violations.append(
                "PAYMENT_CONSTRAINT"
            )


        if (
            proposal.supplier_reliability
            <
            self._minimum_supplier_reliability
        ):

            violations.append(
                "RELIABILITY_CONSTRAINT"
            )


        return {

            "accepted":
                len(violations) == 0,

            "violations":
                violations

        }


    # ========================================================
    # PUBLIC BLACK-BOX INTERFACE
    # ========================================================

    def evaluate_proposal(
        self,
        proposal
    ) -> Dict:

        result = (
            self._evaluate_hidden_policy(
                proposal
            )
        )


        decision = (

            "ACCEPTED"

            if result["accepted"]

            else "REJECTED"

        )


        return {

            "buyer":
                self._buyer_name,

            "decision":
                decision,

            "message":
                (
                    "Proposal accepted."

                    if result["accepted"]

                    else
                    "Proposal does not satisfy "
                    "procurement requirements."
                )

        }


# ============================================================
# BUYER CONFIGURATION FACTORY
# ============================================================

class BuyerConfigurationFactory:

    @staticmethod
    def create_buyers():

        return {

            # =================================================
            # BUYER A — PRICE SENSITIVE
            # =================================================

            "price_sensitive":

                ConfigurableAutonomousBuyer(

                    buyer_name=(
                        "Price Sensitive "
                        "Procurement Agent"
                    ),

                    max_budget=90000,

                    maximum_contract_months=42,

                    minimum_service_availability=96.0,

                    minimum_payment_days=21,

                    minimum_supplier_reliability=80.0

                ),


            # =================================================
            # BUYER B — SERVICE SENSITIVE
            # =================================================

            "service_sensitive":

                ConfigurableAutonomousBuyer(

                    buyer_name=(
                        "Service Sensitive "
                        "Procurement Agent"
                    ),

                    max_budget=120000,

                    maximum_contract_months=48,

                    minimum_service_availability=99.5,

                    minimum_payment_days=21,

                    minimum_supplier_reliability=82.0

                ),


            # =================================================
            # BUYER C — RELIABILITY SENSITIVE
            # =================================================

            "reliability_sensitive":

                ConfigurableAutonomousBuyer(

                    buyer_name=(
                        "Reliability Sensitive "
                        "Procurement Agent"
                    ),

                    max_budget=115000,

                    maximum_contract_months=48,

                    minimum_service_availability=97.0,

                    minimum_payment_days=21,

                    minimum_supplier_reliability=95.0

                ),


            # =================================================
            # BUYER D — CONTRACT SENSITIVE
            # =================================================

            "contract_sensitive":

                ConfigurableAutonomousBuyer(

                    buyer_name=(
                        "Contract Sensitive "
                        "Procurement Agent"
                    ),

                    max_budget=115000,

                    maximum_contract_months=18,

                    minimum_service_availability=97.0,

                    minimum_payment_days=21,

                    minimum_supplier_reliability=82.0

                ),


            # =================================================
            # BUYER E — BALANCED
            # =================================================

            "balanced":

                ConfigurableAutonomousBuyer(

                    buyer_name=(
                        "Balanced Procurement Agent"
                    ),

                    max_budget=105000,

                    maximum_contract_months=36,

                    minimum_service_availability=98.0,

                    minimum_payment_days=30,

                    minimum_supplier_reliability=85.0

                )

        }


    # ========================================================
    # EVALUATION-ONLY GROUND TRUTH
    # ========================================================
    #
    # IMPORTANT:
    #
    # Discovery engines must never receive this dictionary.
    #
    # It exists only so Experiment 017 can evaluate estimates
    # after black-box discovery has completed.
    # ========================================================

    @staticmethod
    def ground_truth():

        return {

            "price_sensitive": {

                "annual_price": 90000,

                "contract_months": 42,

                "service_availability": 96.0,

                "payment_days": 21,

                "supplier_reliability": 80.0

            },


            "service_sensitive": {

                "annual_price": 120000,

                "contract_months": 48,

                "service_availability": 99.5,

                "payment_days": 21,

                "supplier_reliability": 82.0

            },


            "reliability_sensitive": {

                "annual_price": 115000,

                "contract_months": 48,

                "service_availability": 97.0,

                "payment_days": 21,

                "supplier_reliability": 95.0

            },


            "contract_sensitive": {

                "annual_price": 115000,

                "contract_months": 18,

                "service_availability": 97.0,

                "payment_days": 21,

                "supplier_reliability": 82.0

            },


            "balanced": {

                "annual_price": 105000,

                "contract_months": 36,

                "service_availability": 98.0,

                "payment_days": 30,

                "supplier_reliability": 85.0

            }

        }
