"""
MARS — Machine-Agent Revenue Science

Experiment 009

Contextual Commercial Strategy Learning
Under Uncertainty

Author: Kamran Khan

Experimental Comparison:

Fixed Commercial Strategy
versus
Contextual Learning Strategy
"""

from negotiation.commercial_learning_engine import (

    LearningPackage,

    CommercialBuyerSimulator,

    ContextualCommercialLearningAgent,

    CommercialOutcomeEvaluator

)


# ==================================================
# EXPERIMENT CONFIGURATION
# ==================================================

NUMBER_OF_EPISODES = 240

RANDOM_SEED = 42

BUYER_SEGMENTS = [

    "Corporate",

    "Healthcare",

    "Industrial"

]


# ==================================================
# DEFINE COMMERCIAL PACKAGES
# ==================================================

packages = [

    LearningPackage(

        name="Standard",

        expected_saving=0,

        implementation_cost=0

    ),

    LearningPackage(

        name="Digital Operations",

        expected_saving=5000,

        implementation_cost=1000

    ),

    LearningPackage(

        name="Strategic Partnership",

        expected_saving=11500,

        implementation_cost=2000

    ),

    LearningPackage(

        name="Advanced Automation",

        expected_saving=14500,

        implementation_cost=3500

    )

]


# ==================================================
# INITIALISE EXPERIMENTAL ENVIRONMENT
# ==================================================

simulator = CommercialBuyerSimulator(

    seed=RANDOM_SEED

)

evaluator = CommercialOutcomeEvaluator(

    original_concession_cost=33100,

    supplier_budget=25000

)


# ==================================================
# INITIALISE LEARNING AGENT
# ==================================================

learning_agent = (
    ContextualCommercialLearningAgent(

        packages,

        exploration_strength=1800

    )
)


# ==================================================
# INITIALISE BASELINE STRATEGY
# ==================================================

fixed_package = next(

    package

    for package in packages

    if package.name == "Advanced Automation"

)


# ==================================================
# EXPERIMENTAL RESULTS
# ==================================================

baseline_results = []

learning_results = []


# ==================================================
# START EXPERIMENT
# ==================================================

print("\n" + "=" * 60)

print("MARS EXPERIMENT 009")

print(
    "CONTEXTUAL COMMERCIAL STRATEGY LEARNING"
)

print("=" * 60)


# ==================================================
# RUN EXPERIMENTAL EPISODES
# ==================================================

for episode in range(

    1,

    NUMBER_OF_EPISODES + 1

):

    buyer_segment = BUYER_SEGMENTS[

        (episode - 1)

        % len(BUYER_SEGMENTS)

    ]

    # --------------------------------------------------
    # GENERATE SHARED EXPERIMENTAL CONDITIONS
    # --------------------------------------------------

    # Generate potential outcomes before either
    # supplier selects its package.
    #
    # The learning agent cannot inspect these
    # outcomes before making its decision.

    episode_outcomes = {

        package.name:

            simulator.generate_outcome(

                buyer_segment,

                package

            )

        for package in packages

    }

    # --------------------------------------------------
    # FIXED SUPPLIER
    # --------------------------------------------------

    baseline_outcome = (
        episode_outcomes[
            fixed_package.name
        ]
    )

    baseline_result = evaluator.evaluate(

        fixed_package,

        baseline_outcome

    )

    baseline_result[
        "buyer_segment"
    ] = buyer_segment

    baseline_result[
        "package"
    ] = fixed_package.name

    baseline_results.append(
        baseline_result
    )

    # --------------------------------------------------
    # LEARNING SUPPLIER
    # --------------------------------------------------

    selected_package = (
        learning_agent.select_package(

            buyer_segment

        )
    )

    learning_outcome = (
        episode_outcomes[
            selected_package.name
        ]
    )

    learning_result = evaluator.evaluate(

        selected_package,

        learning_outcome

    )

    learning_result[
        "buyer_segment"
    ] = buyer_segment

    learning_result[
        "package"
    ] = selected_package.name

    learning_results.append(
        learning_result
    )

    # --------------------------------------------------
    # UPDATE COMMERCIAL MEMORY
    # --------------------------------------------------

    # Learning occurs only after the commercial
    # decision has been evaluated.

    learning_agent.learn(

        buyer_segment,

        selected_package,

        learning_result[
            "reward"
        ],

        learning_result[
            "successful"
        ]

    )

    # --------------------------------------------------
    # DISPLAY EXPERIMENTAL PROGRESS
    # --------------------------------------------------

    if episode % 40 == 0:

        print(

            f"\nCompleted episode: "
            f"{episode}"

        )


# ==================================================
# AGGREGATE EXPERIMENTAL RESULTS
# ==================================================

baseline_successes = sum(

    result["successful"]

    for result in baseline_results

)

learning_successes = sum(

    result["successful"]

    for result in learning_results

)


baseline_reward = sum(

    result["reward"]

    for result in baseline_results

)

learning_reward = sum(

    result["reward"]

    for result in learning_results

)


baseline_success_rate = (

    baseline_successes

    / NUMBER_OF_EPISODES

) * 100


learning_success_rate = (

    learning_successes

    / NUMBER_OF_EPISODES

) * 100


# ==================================================
# DISPLAY BENCHMARK
# ==================================================

print("\n" + "=" * 60)

print("COMMERCIAL LEARNING BENCHMARK")

print("=" * 60)


print(

    f"\nTotal episodes: "
    f"{NUMBER_OF_EPISODES}"

)

print(

    f"Baseline successful deals: "
    f"{baseline_successes}"

)

print(

    f"Learning successful deals: "
    f"{learning_successes}"

)

print(

    f"Baseline success rate: "
    f"{baseline_success_rate:.2f}%"

)

print(

    f"Learning success rate: "
    f"{learning_success_rate:.2f}%"

)

print(

    f"Baseline total reward: "
    f"£{baseline_reward:,.2f}"

)

print(

    f"Learning total reward: "
    f"£{learning_reward:,.2f}"

)


# ==================================================
# SEGMENT-LEVEL BENCHMARK
# ==================================================

print("\n" + "=" * 60)

print("BUYER SEGMENT ANALYSIS")

print("=" * 60)


for segment in BUYER_SEGMENTS:

    baseline_segment = [

        result

        for result in baseline_results

        if result["buyer_segment"] == segment

    ]

    learning_segment = [

        result

        for result in learning_results

        if result["buyer_segment"] == segment

    ]

    baseline_segment_successes = sum(

        result["successful"]

        for result in baseline_segment

    )

    learning_segment_successes = sum(

        result["successful"]

        for result in learning_segment

    )

    print(
        f"\nBuyer segment: {segment}"
    )

    print(

        f"Fixed strategy successes: "
        f"{baseline_segment_successes}"

    )

    print(

        f"Learning strategy successes: "
        f"{learning_segment_successes}"

    )


# ==================================================
# DISPLAY COMMERCIAL MEMORY
# ==================================================

learning_agent.display_memory()


# ==================================================
# EXPERIMENTAL VALIDATION
# ==================================================

print("\n" + "=" * 60)

print("EXPERIMENTAL VALIDATION")

print("=" * 60)


assert len(
    baseline_results
) == NUMBER_OF_EPISODES


assert len(
    learning_results
) == NUMBER_OF_EPISODES


assert (

    learning_agent.total_decisions

    == NUMBER_OF_EPISODES

)


# Successful agreements must always
# satisfy the supplier's concession budget.

assert all(

    result["net_cost"] <= 25000

    for result in learning_results

    if result["successful"]

)


# Successful agreements must have
# buyer acceptance.

assert all(

    result["buyer_accepts"]

    for result in learning_results

    if result["successful"]

)


# Every buyer segment must have
# its own commercial memory.

assert len(
    learning_agent.memory
) == 3


# The learning agent must explore
# every package in every segment.

assert all(

    record["attempts"] > 0

    for segment_memory
    in learning_agent.memory.values()

    for record
    in segment_memory.values()

)


print(
    "\nALL EXPERIMENTAL VALIDATIONS PASSED"
)

print(
    "\nMARS EXPERIMENT 009 PASSED"
)
