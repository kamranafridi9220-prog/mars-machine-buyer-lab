"""
MARS — Machine-Agent Revenue Science

Experiment 009

Contextual Commercial Strategy Learning
Under Uncertainty

Author: Kamran Khan

Research Objective:

Investigate whether an autonomous supplier
can learn commercially effective strategies
across different buyer segments.

Learning Method:

Contextual Multi-Armed Bandit
Upper Confidence Bound (UCB)

No external Python packages required.
"""

import math
import random

from dataclasses import dataclass


# ==================================================
# COMMERCIAL PACKAGE
# ==================================================

@dataclass(frozen=True)
class LearningPackage:

    name: str

    expected_saving: float

    implementation_cost: float


# ==================================================
# BUYER SEGMENT SIMULATOR
# ==================================================

class CommercialBuyerSimulator:

    def __init__(self, seed=42):

        self.random = random.Random(seed)

        # Hidden experimental buyer preferences.
        #
        # These probabilities are available to
        # the simulation environment only.
        #
        # They are not supplied to the learning
        # agent.

        self.buyer_preferences = {

            "Corporate": {

                "Standard": 0.95,

                "Digital Operations": 0.85,

                "Strategic Partnership": 0.90,

                "Advanced Automation": 0.35

            },

            "Healthcare": {

                "Standard": 0.95,

                "Digital Operations": 0.75,

                "Strategic Partnership": 0.85,

                "Advanced Automation": 0.65

            },

            "Industrial": {

                "Standard": 0.95,

                "Digital Operations": 0.70,

                "Strategic Partnership": 0.25,

                "Advanced Automation": 0.90

            }

        }

    # --------------------------------------------------
    # GENERATE EXPERIMENTAL OUTCOME
    # --------------------------------------------------

    def generate_outcome(
        self,
        buyer_segment,
        package
    ):

        acceptance_probability = (
            self.buyer_preferences[
                buyer_segment
            ][
                package.name
            ]
        )

        buyer_accepts = (

            self.random.random()

            < acceptance_probability

        )

        # Operational savings are uncertain.
        #
        # This is an illustrative statistical
        # assumption, not an empirical estimate
        # from actual commercial contracts.

        realised_saving = max(

            0,

            self.random.gauss(

                package.expected_saving,

                1200

            )

        )

        return {

            "buyer_accepts":
                buyer_accepts,

            "realised_saving":
                realised_saving

        }


# ==================================================
# CONTEXTUAL COMMERCIAL LEARNING AGENT
# ==================================================

class ContextualCommercialLearningAgent:

    def __init__(
        self,
        packages,
        exploration_strength=1800
    ):

        self.packages = packages

        self.exploration_strength = (
            exploration_strength
        )

        self.memory = {}

        self.total_decisions = 0

    # --------------------------------------------------
    # INITIALISE BUYER SEGMENT MEMORY
    # --------------------------------------------------

    def initialise_segment(
        self,
        buyer_segment
    ):

        if buyer_segment in self.memory:

            return

        self.memory[
            buyer_segment
        ] = {}

        for package in self.packages:

            self.memory[
                buyer_segment
            ][
                package.name
            ] = {

                "attempts": 0,

                "total_reward": 0.0,

                "successful_deals": 0,

                "failed_deals": 0

            }

    # --------------------------------------------------
    # SELECT COMMERCIAL STRATEGY
    # --------------------------------------------------

    def select_package(
        self,
        buyer_segment
    ):

        self.initialise_segment(
            buyer_segment
        )

        segment_memory = self.memory[
            buyer_segment
        ]

        # Explore every package at least once
        # for each buyer segment.

        for package in self.packages:

            attempts = segment_memory[
                package.name
            ][
                "attempts"
            ]

            if attempts == 0:

                return package

        total_segment_attempts = sum(

            item["attempts"]

            for item in segment_memory.values()

        )

        best_package = None

        best_score = float("-inf")

        # Upper Confidence Bound strategy.

        for package in self.packages:

            record = segment_memory[
                package.name
            ]

            attempts = record[
                "attempts"
            ]

            average_reward = (

                record["total_reward"]

                / attempts

            )

            exploration_bonus = (

                self.exploration_strength

                * math.sqrt(

                    math.log(
                        total_segment_attempts + 1
                    )

                    / attempts

                )

            )

            score = (

                average_reward

                + exploration_bonus

            )

            if score > best_score:

                best_score = score

                best_package = package

        return best_package

    # --------------------------------------------------
    # LEARN FROM COMMERCIAL OUTCOME
    # --------------------------------------------------

    def learn(
        self,
        buyer_segment,
        package,
        reward,
        successful
    ):

        self.initialise_segment(
            buyer_segment
        )

        record = self.memory[
            buyer_segment
        ][
            package.name
        ]

        record["attempts"] += 1

        record["total_reward"] += reward

        if successful:

            record["successful_deals"] += 1

        else:

            record["failed_deals"] += 1

        self.total_decisions += 1

    # --------------------------------------------------
    # DISPLAY LEARNED COMMERCIAL INTELLIGENCE
    # --------------------------------------------------

    def display_memory(self):

        print("\n" + "=" * 60)

        print(
            "LEARNED COMMERCIAL STRATEGY MEMORY"
        )

        print("=" * 60)

        for segment, packages in (
            self.memory.items()
        ):

            print(
                f"\nBUYER SEGMENT: {segment}"
            )

            for package_name, record in (
                packages.items()
            ):

                attempts = record[
                    "attempts"
                ]

                if attempts == 0:

                    continue

                average_reward = (

                    record["total_reward"]

                    / attempts

                )

                print(
                    f"\nPackage: {package_name}"
                )

                print(
                    f"Attempts: {attempts}"
                )

                print(
                    f"Successful deals: "
                    f"{record['successful_deals']}"
                )

                print(
                    f"Failed deals: "
                    f"{record['failed_deals']}"
                )

                print(
                    f"Average reward: "
                    f"£{average_reward:,.2f}"
                )


# ==================================================
# COMMERCIAL OUTCOME EVALUATOR
# ==================================================

class CommercialOutcomeEvaluator:

    def __init__(
        self,
        original_concession_cost=33100,
        supplier_budget=25000
    ):

        self.original_concession_cost = (
            original_concession_cost
        )

        self.supplier_budget = (
            supplier_budget
        )

    # --------------------------------------------------
    # EVALUATE COMMERCIAL DECISION
    # --------------------------------------------------

    def evaluate(
        self,
        package,
        outcome
    ):

        net_cost = (

            self.original_concession_cost

            - outcome["realised_saving"]

            + package.implementation_cost

        )

        net_cost = max(
            0,
            net_cost
        )

        buyer_accepts = outcome[
            "buyer_accepts"
        ]

        within_budget = (

            net_cost <=
            self.supplier_budget

        )

        successful = (

            buyer_accepts

            and within_budget

        )

        # Commercial reward:
        #
        # A feasible accepted agreement earns
        # a fixed agreement reward plus
        # remaining concession-budget capacity.
        #
        # Rejected or financially infeasible
        # agreements receive zero reward.

        if successful:

            reward = (

                2000

                + self.supplier_budget

                - net_cost

            )

        else:

            reward = 0.0

        return {

            "successful":
                successful,

            "buyer_accepts":
                buyer_accepts,

            "within_budget":
                within_budget,

            "net_cost":
                net_cost,

            "reward":
                reward

        }
