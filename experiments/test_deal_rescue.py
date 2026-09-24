"""
MARS — Machine-Agent Revenue Science

Experiment 008

Autonomous Commercial Deal Rescue

Author: Kamran Khan

Research Question:

Can alternative commercial delivery packages
rescue buyer-acceptable but financially
infeasible B2B agreements?
"""

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)

from negotiation.negotiation_lab import (
    SupplierNegotiationAgent
)

from negotiation.deal_rescue_engine import (
    CommercialPackage,
    CommercialDealRescueEngine
)


# ==================================================
# EXPERIMENTAL CONFIGURATION
# ==================================================

SUPPLIER_BUDGET = 25000

MINIMUM_ANNUAL_PRICE = 100000


# ==================================================
# CREATE AUTONOMOUS BUYER
# ==================================================

class CommercialBuyer(
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


buyer = CommercialBuyer()


# ==================================================
# ORIGINAL SUPPLIER PROPOSAL
# ==================================================

original_proposal = CommercialProposal(

    annual_price=120000,

    service_availability=95.0,

    supplier_reliability=90.0,

    contract_months=48,

    payment_days=14

)


# ==================================================
# BUYER-ACCEPTABLE RECOVERED PROPOSAL
# ==================================================

recovered_proposal = CommercialProposal(

    annual_price=102000,

    service_availability=99.0,

    supplier_reliability=90.0,

    contract_months=24,

    payment_days=45

)


# ==================================================
# INITIALISE SUPPLIER
# ==================================================

supplier = SupplierNegotiationAgent(

    original_proposal,

    maximum_intervention_cost=
        SUPPLIER_BUDGET,

    minimum_annual_price=
        MINIMUM_ANNUAL_PRICE

)


# ==================================================
# INITIALISE DEAL RESCUE ENGINE
# ==================================================

engine = CommercialDealRescueEngine(

    buyer,

    supplier,

    concession_budget=
        SUPPLIER_BUDGET

)


# ==================================================
# DEFINE EXPERIMENTAL COMMERCIAL PACKAGES
# ==================================================

packages = [

    CommercialPackage(

        name="Standard",

        operational_saving=0,

        implementation_cost=0,

        description=(
            "Traditional commercial "
            "delivery model"
        )

    ),

    CommercialPackage(

        name="Digital Operations",

        operational_saving=5000,

        implementation_cost=1000,

        description=(
            "Technology-enabled "
            "service delivery"
        )

    ),

    CommercialPackage(

        name="Strategic Partnership",

        operational_saving=8000,

        implementation_cost=2000,

        description=(
            "Integrated commercial "
            "partnership model"
        )

    ),

    CommercialPackage(

        name="Advanced Automation",

        operational_saving=12000,

        implementation_cost=2000,

        description=(
            "Automation-supported "
            "operational delivery"
        )

    )

]


# ==================================================
# SIMULATED BUYER PACKAGE ACCEPTANCE
# ==================================================

# These acceptance values represent a controlled
# experimental assumption.
#
# In a production system, package acceptance
# would need to be confirmed by the buyer.

package_acceptance = {

    "Standard": True,

    "Digital Operations": True,

    "Strategic Partnership": True,

    "Advanced Automation": True

}


# ==================================================
# EXPERIMENT 008
# ==================================================

print("\n" + "=" * 60)

print("MARS EXPERIMENT 008")

print("AUTONOMOUS COMMERCIAL DEAL RESCUE")

print("=" * 60)


# ==================================================
# VALIDATE INITIAL COMMERCIAL PROBLEM
# ==================================================

initial_cost = supplier.calculate_cost(
    recovered_proposal
)

assert initial_cost > SUPPLIER_BUDGET

print(

    f"\nInitial concession cost: "
    f"£{initial_cost:,.2f}"

)

print(

    f"Supplier concession budget: "
    f"£{SUPPLIER_BUDGET:,.2f}"

)

print(
    "\nInitial agreement is commercially "
    "infeasible."
)


# ==================================================
# EXECUTE COMMERCIAL DEAL RESCUE
# ==================================================

result = engine.rescue_deal(

    recovered_proposal,

    packages,

    package_acceptance

)


# ==================================================
# EXPERIMENTAL VALIDATION
# ==================================================

print("\n" + "=" * 60)

print("EXPERIMENTAL VALIDATION")

print("=" * 60)


assert result is not None

assert result[
    "commercially_feasible"
] is True

assert result[
    "buyer_accepts_terms"
] is True

assert result[
    "buyer_accepts_package"
] is True

assert result[
    "within_budget"
] is True

assert result[
    "price_acceptable"
] is True

assert result[
    "net_cost"
] <= SUPPLIER_BUDGET

assert len(
    engine.evaluated_packages
) == 4


# ==================================================
# VALIDATE COMMERCIAL PACKAGE SELECTION
# ==================================================

assert result[
    "package"
] == "Advanced Automation"


assert abs(

    result["net_cost"] - 23100

) < 0.01


# ==================================================
# DISPLAY FINAL RESULTS
# ==================================================

print(
    "\nCOMMERCIAL RESCUE VALIDATED"
)

print(

    f"Selected package: "
    f"{result['package']}"

)

print(

    f"Original concession cost: "
    f"£{result['original_cost']:,.2f}"

)

print(

    f"Net concession cost: "
    f"£{result['net_cost']:,.2f}"

)

print(

    f"Remaining supplier budget: "
    f"£{SUPPLIER_BUDGET - result['net_cost']:,.2f}"

)

print(

    f"Total package evaluations: "
    f"{len(engine.evaluated_packages)}"

)

print(

    f"Total buyer queries: "
    f"{engine.buyer_queries}"

)

print(
    "\nALL EXPERIMENTAL VALIDATIONS PASSED"
)

print(
    "\nMARS EXPERIMENT 008 PASSED"
)
