"""
MARS — Machine-Agent Revenue Science

Experiment 006

Adaptive Negotiation Intelligence Benchmark

Author: Kamran Khan

Research Question:

Can a supplier agent use previous negotiation
experience to reduce future negotiation rounds?
"""

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)

from negotiation.negotiation_lab import (
    BuyerNegotiationAgent,
    SupplierNegotiationAgent,
    AutonomousNegotiationEnvironment
)

from negotiation.adaptive_negotiation import (
    NegotiationMemoryEngine,
    AdaptiveSupplierAgent
)


# ==================================================
# EXPERIMENTAL CONFIGURATION
# ==================================================

BUYER_ID = "CORPORATE_BUYER_001"

NUMBER_OF_EPISODES = 3

MAXIMUM_INTERVENTION_COST = 25000

MINIMUM_ANNUAL_PRICE = 100000


# ==================================================
# CREATE ORIGINAL COMMERCIAL PROPOSAL
# ==================================================

def create_original_proposal():

    return CommercialProposal(

        annual_price=120000,

        contract_months=48,

        service_availability=95.0,

        payment_days=14,

        supplier_reliability=90.0

    )


# ==================================================
# CREATE BUYER NEGOTIATION AGENT
# ==================================================

def create_buyer():

    buyer = AutonomousBuyerAgent()

    # These requirements are supplied only to
    # the buyer-side negotiation interface.
    #
    # The adaptive supplier receives no direct
    # access to this dictionary.

    buyer_requirements = {

        "annual_price": 105000,

        "service_availability": 98.0,

        "supplier_reliability": 85.0,

        "contract_months": 36,

        "payment_days": 30

    }

    buyer_negotiator = BuyerNegotiationAgent(

        buyer,

        buyer_requirements

    )

    return buyer, buyer_negotiator


# ==================================================
# BASELINE NEGOTIATION
# ==================================================

def run_baseline_negotiation():

    buyer, buyer_negotiator = create_buyer()

    supplier = SupplierNegotiationAgent(

        create_original_proposal(),

        maximum_intervention_cost=
            MAXIMUM_INTERVENTION_COST,

        minimum_annual_price=
            MINIMUM_ANNUAL_PRICE

    )

    environment = AutonomousNegotiationEnvironment(

        buyer_negotiator,

        supplier,

        maximum_rounds=10

    )

    result = environment.negotiate()

    assert result["agreement"], (
        "Baseline negotiation failed."
    )

    return result


# ==================================================
# ADAPTIVE NEGOTIATION
# ==================================================

def run_adaptive_negotiation(
    memory_engine
):

    buyer, buyer_negotiator = create_buyer()

    supplier = AdaptiveSupplierAgent(

        create_original_proposal(),

        memory_engine,

        BUYER_ID,

        maximum_intervention_cost=
            MAXIMUM_INTERVENTION_COST,

        minimum_annual_price=
            MINIMUM_ANNUAL_PRICE

    )

    # Retrieve and apply previous experience.

    supplier.prepare_adaptive_proposal()

    environment = AutonomousNegotiationEnvironment(

        buyer_negotiator,

        supplier,

        maximum_rounds=10

    )

    result = environment.negotiate()

    assert result["agreement"], (
        "Adaptive negotiation failed."
    )

    # Verify agreement against the underlying
    # autonomous buyer.

    final_response = buyer.evaluate_proposal(

        result["final_proposal"]

    )

    assert (
        final_response["decision"] ==
        "ACCEPTED"
    )

    # Protect supplier financial constraints.

    assert (
        result["total_cost"] <=
        MAXIMUM_INTERVENTION_COST
    )

    assert (
        result["final_proposal"].annual_price >=
        MINIMUM_ANNUAL_PRICE
    )

    result["used_memory"] = (
        supplier.used_memory
    )

    # Learn only after the negotiation has ended.

    memory_engine.learn_from_negotiation(

        BUYER_ID,

        result

    )

    return result


# ==================================================
# INITIALISE EXPERIMENT
# ==================================================

print("\n" + "=" * 60)

print("MARS EXPERIMENT 006")

print("ADAPTIVE NEGOTIATION INTELLIGENCE")

print("=" * 60)


memory_engine = NegotiationMemoryEngine()

baseline_results = []

adaptive_results = []


# ==================================================
# RUN EXPERIMENTAL EPISODES
# ==================================================

for episode in range(

    1,

    NUMBER_OF_EPISODES + 1

):

    print("\n" + "#" * 60)

    print(
        f"EXPERIMENTAL EPISODE {episode}"
    )

    print("#" * 60)

    # ----------------------------------------------
    # BASELINE SUPPLIER
    # ----------------------------------------------

    print("\nBASELINE NEGOTIATION")

    baseline = run_baseline_negotiation()

    baseline_results.append(
        baseline
    )

    # ----------------------------------------------
    # ADAPTIVE SUPPLIER
    # ----------------------------------------------

    print("\nADAPTIVE NEGOTIATION")

    adaptive = run_adaptive_negotiation(

        memory_engine

    )

    adaptive_results.append(
        adaptive
    )

    print("\nEPISODE RESULTS")

    print(

        f"Baseline rounds: "
        f"{baseline['rounds']}"

    )

    print(

        f"Adaptive rounds: "
        f"{adaptive['rounds']}"

    )

    print(

        f"Adaptive memory used: "
        f"{adaptive['used_memory']}"

    )


# ==================================================
# BENCHMARK ANALYSIS
# ==================================================

baseline_total_rounds = sum(

    result["rounds"]

    for result in baseline_results

)

adaptive_total_rounds = sum(

    result["rounds"]

    for result in adaptive_results

)


baseline_counteroffers = sum(

    len(result["history"])

    for result in baseline_results

)

adaptive_counteroffers = sum(

    len(result["history"])

    for result in adaptive_results

)


rounds_saved = (

    baseline_total_rounds -
    adaptive_total_rounds

)


round_reduction_percentage = (

    rounds_saved /

    baseline_total_rounds

) * 100


# ==================================================
# DISPLAY BENCHMARK
# ==================================================

print("\n" + "=" * 60)

print("MARS ADAPTIVE NEGOTIATION BENCHMARK")

print("=" * 60)


for episode in range(
    NUMBER_OF_EPISODES
):

    print(

        f"\nEpisode {episode + 1}"

    )

    print(

        f"Baseline rounds: "
        f"{baseline_results[episode]['rounds']}"

    )

    print(

        f"Adaptive rounds: "
        f"{adaptive_results[episode]['rounds']}"

    )


print("\n" + "=" * 60)

print("AGGREGATE RESULTS")

print("=" * 60)


print(

    f"Baseline Total Rounds: "
    f"{baseline_total_rounds}"

)

print(

    f"Adaptive Total Rounds: "
    f"{adaptive_total_rounds}"

)

print(

    f"Negotiation Rounds Saved: "
    f"{rounds_saved}"

)

print(

    f"Round Reduction: "
    f"{round_reduction_percentage:.2f}%"

)

print(

    f"Baseline Counteroffers: "
    f"{baseline_counteroffers}"

)

print(

    f"Adaptive Counteroffers: "
    f"{adaptive_counteroffers}"

)


# ==================================================
# EXPERIMENTAL VALIDATION
# ==================================================

print("\n" + "=" * 60)

print("EXPERIMENTAL VALIDATION")

print("=" * 60)


# The first adaptive negotiation must start
# without any prior buyer memory.

assert (
    adaptive_results[0]["used_memory"]
    is False
)


# The supplier must learn after episode one.

assert memory_engine.has_memory(
    BUYER_ID
)


# Subsequent negotiations must use memory.

assert (
    adaptive_results[1]["used_memory"]
    is True
)

assert (
    adaptive_results[2]["used_memory"]
    is True
)


# Expected deterministic benchmark results.

assert baseline_total_rounds == 15

assert adaptive_total_rounds == 7

assert rounds_saved == 8

assert baseline_counteroffers == 12

assert adaptive_counteroffers == 4


# Every negotiation must produce agreement.

assert all(

    result["agreement"]

    for result in adaptive_results

)


# All adaptive agreements must remain
# within supplier financial limits.

assert all(

    result["total_cost"] <=
    MAXIMUM_INTERVENTION_COST

    for result in adaptive_results

)


# The buyer policy is unchanged across episodes,
# so the final concession cost should remain equal.

assert all(

    abs(result["total_cost"] - 24100)
    < 0.01

    for result in adaptive_results

)


print("\nALL VALIDATION TESTS PASSED")

print("\nMARS EXPERIMENT 006 PASSED")
