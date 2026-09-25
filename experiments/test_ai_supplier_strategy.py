"""
MARS — Machine-Agent Revenue Science

Experiment 011

Autonomous AI Supplier Strategy Experiment

Version 3:
Feasible vs Infeasible Commercial Negotiation

Author: Kamran Khan

Research Objective:
Investigate how an autonomous AI supplier adapts
commercial negotiation strategies under different
supplier-side intervention budgets.

Scenario A:
Commercially feasible negotiation.

Scenario B:
Commercially infeasible negotiation.
"""

from dataclasses import asdict

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)

from negotiation.ai_supplier_strategy_agent import (
    AISupplierStrategyAgent
)


# ==================================================
# EXPERIMENT CONFIGURATION
# ==================================================

MAX_ROUNDS = 5

MINIMUM_ANNUAL_PRICE = 100000


# ==================================================
# INITIAL COMMERCIAL PROPOSAL
# ==================================================

def create_initial_proposal():

    return CommercialProposal(

        annual_price=120000,

        contract_months=48,

        service_availability=95.0,

        payment_days=15,

        supplier_reliability=80.0

    )


# ==================================================
# RUN AUTONOMOUS NEGOTIATION SCENARIO
# ==================================================

def run_negotiation_scenario(

    scenario_name,

    maximum_intervention_cost

):

    print("\n" + "=" * 70)

    print("MARS — EXPERIMENT 011")

    print(scenario_name)

    print("=" * 70)

    print(

        "\nMaximum Intervention Budget: £"

        f"{maximum_intervention_cost:,.2f}"

    )

    print(

        "Minimum Annual Price: £"

        f"{MINIMUM_ANNUAL_PRICE:,.2f}"

    )

    # --------------------------------------------------
    # INITIALISE INDEPENDENT BUYER
    # --------------------------------------------------

    buyer = AutonomousBuyerAgent()

    # --------------------------------------------------
    # INITIALISE COMMERCIAL PROPOSAL
    # --------------------------------------------------

    initial_proposal = create_initial_proposal()

    # --------------------------------------------------
    # INITIALISE INDEPENDENT AI SUPPLIER
    # --------------------------------------------------

    supplier = AISupplierStrategyAgent(

        original_proposal=initial_proposal,

        maximum_intervention_cost=(
            maximum_intervention_cost
        ),

        minimum_annual_price=(
            MINIMUM_ANNUAL_PRICE
        )

    )

    # --------------------------------------------------
    # EXPERIMENT METRICS
    # --------------------------------------------------

    agreement = False

    buyer_evaluations = 0

    approved_strategies = 0

    rejected_strategies = 0

    # --------------------------------------------------
    # INITIAL BUYER EVALUATION
    # --------------------------------------------------

    buyer_response = buyer.evaluate_proposal(

        supplier.current_proposal

    )

    buyer_evaluations += 1

    supplier.record_buyer_feedback(

        supplier.current_proposal,

        buyer_response

    )

    print("\nINITIAL COMMERCIAL PROPOSAL")

    print(initial_proposal)

    print("\nINITIAL BUYER DECISION")

    print(buyer_response["decision"])

    if buyer_response["decision"] == "ACCEPTED":

        agreement = True

    # ==================================================
    # AUTONOMOUS AI NEGOTIATION
    # ==================================================

    for round_number in range(

        1,

        MAX_ROUNDS + 1

    ):

        if agreement:

            break

        print("\n" + "-" * 70)

        print(

            f"AI NEGOTIATION ROUND {round_number}"

        )

        print("-" * 70)

        print("\nCURRENT COMMERCIAL PROPOSAL")

        print(supplier.current_proposal)

        print(

            "\nREMAINING INTERVENTION BUDGET: £"

            f"{supplier.remaining_budget():,.2f}"

        )

        # ----------------------------------------------
        # GENERATE AI COMMERCIAL STRATEGY
        # ----------------------------------------------

        print("\nAI SUPPLIER GENERATING STRATEGY...")

        strategy = supplier.generate_strategy(

            buyer_feedback=buyer_response

        )

        print("\nAI STRATEGY REASONING")

        print(strategy["reasoning"])

        print("\nAI PROPOSED COMMERCIAL STRATEGY")

        print(strategy["candidate"])

        # ----------------------------------------------
        # COMMERCIAL VALIDATION
        # ----------------------------------------------

        validation = strategy["validation"]

        if not validation["valid"]:

            rejected_strategies += 1

            print("\nSTRATEGY COMMERCIALLY REJECTED")

            print(validation["reason"])

            print(

                "\nAI will use this failure "

                "in its next strategy attempt."

            )

            continue

        # ----------------------------------------------
        # APPROVED COMMERCIAL STRATEGY
        # ----------------------------------------------

        approved_strategies += 1

        print("\nSTRATEGY COMMERCIALLY APPROVED")

        print(

            "Intervention Cost: £"

            f"{validation['cost']:,.2f}"

        )

        print(

            "Remaining Budget: £"

            f"{supplier.remaining_budget():,.2f}"

        )

        # ----------------------------------------------
        # BUYER EVALUATES REVISED PROPOSAL
        # ----------------------------------------------

        buyer_response = buyer.evaluate_proposal(

            supplier.current_proposal

        )

        buyer_evaluations += 1

        supplier.record_buyer_feedback(

            supplier.current_proposal,

            buyer_response

        )

        print("\nBUYER DECISION")

        print(buyer_response["decision"])

        # ----------------------------------------------
        # AGREEMENT REACHED
        # ----------------------------------------------

        if buyer_response["decision"] == "ACCEPTED":

            agreement = True

            print("\nCOMMERCIAL AGREEMENT REACHED")

            print(

                "Final Annual Price: £"

                f"{supplier.current_proposal.annual_price:,.2f}"

            )

            print(

                "Total Intervention Cost: £"

                f"{supplier.calculate_cost(supplier.current_proposal):,.2f}"

            )

            break

    # ==================================================
    # FINAL SCENARIO RESULTS
    # ==================================================

    final_proposal = supplier.current_proposal

    final_cost = supplier.calculate_cost(

        final_proposal

    )

    result = {

        "scenario": scenario_name,

        "maximum_intervention_cost": (
            maximum_intervention_cost
        ),

        "agreement": agreement,

        "final_proposal": asdict(
            final_proposal
        ),

        "total_intervention_cost": (
            final_cost
        ),

        "remaining_budget": (
            supplier.remaining_budget()
        ),

        "strategies_generated": (
            len(supplier.strategy_history)
        ),

        "approved_strategies": (
            approved_strategies
        ),

        "rejected_strategies": (
            rejected_strategies
        ),

        "buyer_evaluations": (
            buyer_evaluations
        ),

        "buyer_feedback_records": (
            len(supplier.buyer_feedback_history)
        )

    }

    print("\n" + "=" * 70)

    print("SCENARIO RESULTS")

    print("=" * 70)

    for key, value in result.items():

        print(

            f"{key}: {value}"

        )

    return result


# ==================================================
# SCENARIO A — FEASIBLE NEGOTIATION
# ==================================================

scenario_a = run_negotiation_scenario(

    scenario_name=(
        "SCENARIO A — FEASIBLE NEGOTIATION"
    ),

    maximum_intervention_cost=35000

)


# ==================================================
# SCENARIO B — INFEASIBLE NEGOTIATION
# ==================================================

scenario_b = run_negotiation_scenario(

    scenario_name=(
        "SCENARIO B — INFEASIBLE NEGOTIATION"
    ),

    maximum_intervention_cost=25000

)


# ==================================================
# COMPARATIVE EXPERIMENT RESULTS
# ==================================================

print("\n" + "=" * 70)

print("MARS — EXPERIMENT 011")

print("COMPARATIVE EXPERIMENT RESULTS")

print("=" * 70)


print("\nSCENARIO A — FEASIBLE")

print(

    "Agreement Reached:",

    scenario_a["agreement"]

)

print(

    "Strategies Generated:",

    scenario_a["strategies_generated"]

)

print(

    "Intervention Cost: £"

    f"{scenario_a['total_intervention_cost']:,.2f}"

)


print("\nSCENARIO B — INFEASIBLE")

print(

    "Agreement Reached:",

    scenario_b["agreement"]

)

print(

    "Strategies Generated:",

    scenario_b["strategies_generated"]

)

print(

    "Intervention Cost: £"

    f"{scenario_b['total_intervention_cost']:,.2f}"

)


print("\n" + "=" * 70)

print("EXPERIMENT 011 COMPLETED")

print("=" * 70)
