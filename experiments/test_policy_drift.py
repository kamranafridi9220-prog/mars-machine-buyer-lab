"""
MARS — Machine-Agent Revenue Science

Experiment 007

Buyer Policy Drift and Adaptive Recovery

Author: Kamran Khan

Controlled experiment with changing autonomous
buyer procurement requirements.
"""

from dataclasses import replace

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)

from negotiation.adaptive_negotiation import (
    NegotiationMemoryEngine
)

from negotiation.policy_drift_engine import (
    BuyerPolicyDriftEngine
)

from negotiation.negotiation_lab import (
    SupplierNegotiationAgent
)


# ==================================================
# EXPERIMENT CONFIGURATION
# ==================================================

BUYER_ID = "CORPORATE_BUYER_001"

SUPPLIER_BUDGET = 25000

SUPPLIER_MINIMUM_PRICE = 100000


# ==================================================
# CREATE ORIGINAL COMMERCIAL PROPOSAL
# ==================================================

original_proposal = CommercialProposal(

    annual_price=120000,

    service_availability=95.0,

    supplier_reliability=90.0,

    contract_months=48,

    payment_days=14

)


# ==================================================
# PREVIOUS SUCCESSFUL AGREEMENT
# ==================================================

previous_agreement = replace(

    original_proposal,

    annual_price=105000,

    service_availability=98.0,

    contract_months=36,

    payment_days=30

)


# ==================================================
# INITIALISE COMMERCIAL MEMORY
# ==================================================

memory_engine = NegotiationMemoryEngine()

memory_engine.buyer_memories[
    BUYER_ID
] = {

    "learned_requirements": {

        "annual_price": 105000,

        "service_availability": 98.0,

        "contract_months": 36,

        "payment_days": 30

    },

    "previous_agreement":
        previous_agreement,

    "previous_cost": 24100,

    "previous_rounds": 5

}


# ==================================================
# CREATE NEW BUYER POLICY
# ==================================================

class ChangedPolicyBuyer(
    AutonomousBuyerAgent
):

    def evaluate_proposal(
        self,
        proposal
    ):

        accepted = (

            proposal.annual_price <= 102000

            and

            proposal.service_availability >= 99.0

            and

            proposal.supplier_reliability >= 85.0

            and

            proposal.contract_months <= 24

            and

            proposal.payment_days >= 45

        )

        return {

            "decision": (
                "ACCEPTED"
                if accepted
                else "REJECTED"
            )

        }


buyer = ChangedPolicyBuyer()


# ==================================================
# INITIALISE POLICY DRIFT ENGINE
# ==================================================

engine = BuyerPolicyDriftEngine(

    buyer,

    memory_engine,

    BUYER_ID

)


# ==================================================
# EXPERIMENT 007 — PHASE 1
# ==================================================

print("\n" + "=" * 60)

print("MARS EXPERIMENT 007")

print("BUYER POLICY DRIFT DETECTION")

print("=" * 60)


drift_detected = engine.detect_drift()

assert drift_detected is True


# ==================================================
# EXPERIMENT 007 — PHASE 2
# ==================================================

print("\nCONTROLLED POLICY RECOVERY")


candidate_values = {

    "annual_price": [

        105000,

        104000,

        103000,

        102000

    ],

    "service_availability": [

        98.0,

        98.5,

        99.0

    ],

    "contract_months": [

        36,

        30,

        24

    ],

    "payment_days": [

        30,

        40,

        45

    ]

}


recovered = engine.recover_proposal(
    candidate_values
)

assert recovered is not None


# ==================================================
# VALIDATE BUYER ACCEPTANCE
# ==================================================

buyer_response = buyer.evaluate_proposal(
    recovered
)

assert (
    buyer_response["decision"] ==
    "ACCEPTED"
)


print("\nBUYER POLICY RECOVERY SUCCESSFUL")

print(
    f"Annual price: "
    f"£{recovered.annual_price:,.2f}"
)

print(
    f"Service availability: "
    f"{recovered.service_availability}%"
)

print(
    f"Contract duration: "
    f"{recovered.contract_months} months"
)

print(
    f"Payment terms: "
    f"{recovered.payment_days} days"
)


# ==================================================
# SUPPLIER COMMERCIAL VALIDATION
# ==================================================

print("\n" + "=" * 60)

print("SUPPLIER COMMERCIAL VALIDATION")

print("=" * 60)


supplier = SupplierNegotiationAgent(

    original_proposal,

    maximum_intervention_cost=
        SUPPLIER_BUDGET,

    minimum_annual_price=
        SUPPLIER_MINIMUM_PRICE

)


estimated_cost = supplier.calculate_cost(
    recovered
)


print(

    f"Estimated concession cost: "
    f"£{estimated_cost:,.2f}"

)

print(

    f"Supplier concession budget: "
    f"£{SUPPLIER_BUDGET:,.2f}"

)


# ==================================================
# DETERMINE COMMERCIAL FEASIBILITY
# ==================================================

commercially_feasible = (

    estimated_cost <= SUPPLIER_BUDGET

    and

    recovered.annual_price >=
    SUPPLIER_MINIMUM_PRICE

)


if commercially_feasible:

    print(
        "\nCOMMERCIAL DECISION: "
        "AGREEMENT FEASIBLE"
    )

else:

    print(
        "\nCOMMERCIAL DECISION: "
        "AGREEMENT NOT FEASIBLE"
    )

    print(
        "Buyer requirements exceed "
        "supplier commercial constraints."
    )


# ==================================================
# EXPERIMENTAL VALIDATION
# ==================================================

print("\n" + "=" * 60)

print("EXPERIMENTAL VALIDATION")

print("=" * 60)


assert recovered.annual_price <= 102000

assert recovered.service_availability >= 99.0

assert recovered.contract_months <= 24

assert recovered.payment_days >= 45

assert engine.query_count > 0


print(
    f"Total buyer queries: "
    f"{engine.query_count}"
)

print(
    "\nALL EXPERIMENTAL VALIDATIONS PASSED"
)

print(
    "\nMARS EXPERIMENT 007 PASSED"
)
