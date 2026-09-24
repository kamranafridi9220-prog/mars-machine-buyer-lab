"""
MARS — Machine-Agent Revenue Science

Experiment 010

Adversarial Buyer Behaviour and
Strategic Negotiation Defence

Author: Kamran Khan
"""

from negotiation.adversarial_buyer_engine import (

    NegotiationConfig,

    AdversarialBuyerSimulator,

    StrategicNegotiationDefence,

    NegotiationExperimentEngine

)


# ==================================================
# EXPERIMENT CONFIGURATION
# ==================================================

BUYER_TYPES = [

    "Cooperative",

    "Strategic",

    "Unpredictable"

]

EPISODES_PER_BUYER = 30


# ==================================================
# EXPERIMENTAL RESULTS
# ==================================================

results = {}


print("\n" + "=" * 60)

print("MARS EXPERIMENT 010")

print("ADVERSARIAL NEGOTIATION DEFENCE")

print("=" * 60)


# ==================================================
# RUN BUYER SIMULATIONS
# ==================================================

for buyer_type in BUYER_TYPES:

    print(

        f"\nBUYER TYPE: {buyer_type}"

    )

    print("-" * 50)

    agreements = 0

    total_concession = 0

    total_rounds = 0

    total_escalation_alerts = 0

    total_volatile_alerts = 0

    for episode in range(

        EPISODES_PER_BUYER

    ):

        config = NegotiationConfig()

        buyer = (

            AdversarialBuyerSimulator(

                buyer_type,

                seed=episode + 42

            )

        )

        supplier = (

            StrategicNegotiationDefence(

                config

            )

        )

        engine = (

            NegotiationExperimentEngine(

                buyer,

                supplier,

                config

            )

        )

        outcome = engine.run()

        total_rounds += outcome[

            "rounds"

        ]

        if outcome["agreement"]:

            agreements += 1

            total_concession += outcome[

                "final_concession"

            ]

        for record in outcome[

            "history"

        ]:

            if record[

                "classification"

            ] == "Escalating Demands":

                total_escalation_alerts += 1

            if record[

                "classification"

            ] == "Volatile Demands":

                total_volatile_alerts += 1

            assert record[

                "concession"

            ] <= config.maximum_concession

            assert record[

                "concession"

            ] >= 0

    success_rate = (

        agreements

        / EPISODES_PER_BUYER

    ) * 100

    average_rounds = (

        total_rounds

        / EPISODES_PER_BUYER

    )

    average_concession = (

        total_concession / agreements

        if agreements > 0

        else 0

    )

    results[buyer_type] = {

        "agreements": agreements,

        "success_rate":
            success_rate,

        "average_rounds":
            average_rounds,

        "average_concession":
            average_concession,

        "escalation_alerts":
            total_escalation_alerts,

        "volatile_alerts":
            total_volatile_alerts

    }

    print(

        f"Negotiations: "
        f"{EPISODES_PER_BUYER}"

    )

    print(

        f"Agreements: "
        f"{agreements}"

    )

    print(

        f"Agreement rate: "
        f"{success_rate:.2f}%"

    )

    print(

        f"Average rounds: "
        f"{average_rounds:.2f}"

    )

    print(

        f"Average accepted concession: "
        f"£{average_concession:,.2f}"

    )

    print(

        f"Escalating demand alerts: "
        f"{total_escalation_alerts}"

    )

    print(

        f"Volatile demand alerts: "
        f"{total_volatile_alerts}"

    )


# ==================================================
# EXPERIMENTAL VALIDATION
# ==================================================

print("\n" + "=" * 60)

print("EXPERIMENTAL VALIDATION")

print("=" * 60)


assert len(results) == 3


for buyer_type in BUYER_TYPES:

    result = results[buyer_type]

    assert (

        0 <= result["success_rate"] <= 100

    )

    assert (

        result["average_concession"]

        <= 15000

    )

    assert (

        result["average_rounds"]

        <= 8

    )


# Cooperative buyers should produce
# at least one agreement under the
# experimental configuration.

assert (

    results["Cooperative"][

        "agreements"

    ] > 0

)


# Strategic buyer demand escalation
# should be observable during at least
# one simulated negotiation.

assert (

    results["Strategic"][

        "escalation_alerts"

    ] > 0

)


print(

    "\nALL EXPERIMENTAL VALIDATIONS PASSED"

)

print(

    "\nMARS EXPERIMENT 010 PASSED"

)
