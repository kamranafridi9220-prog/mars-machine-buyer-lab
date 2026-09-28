"""
MARS — Machine-Agent Revenue Science

Experiment 018

Probabilistic Autonomous Buyer Laboratory

Author: Kamran Khan

Purpose:
Simulate autonomous B2B purchasing agents whose
commercial decisions become probabilistic near
hidden procurement-policy boundaries.

Unlike the deterministic buyer environments used
in earlier MARS experiments, this buyer can return
different decisions for commercially similar or
identical proposals when those proposals lie near
a hidden policy threshold.

Research Objective:
Evaluate whether black-box policy-discovery
algorithms remain reliable when individual buyer
decisions are noisy observations of an underlying
commercial policy.

Important:
The buyer's hidden thresholds remain private.
Discovery algorithms receive only observable
ACCEPTED / REJECTED decisions.
"""

import math
import random

from buyer_lab.buyer_agent import (
    CommercialProposal
)


# ============================================================
# PROBABILISTIC AUTONOMOUS BUYER
# ============================================================

class ProbabilisticAutonomousBuyer:

    def __init__(
        self,
        buyer_name="Probabilistic Enterprise Procurement Agent",
        max_budget=105000,
        maximum_contract_months=36,
        minimum_service_availability=98.0,
        minimum_payment_days=30,
        minimum_supplier_reliability=85.0,
        noise_strength=0.15,
        boundary_width=0.05,
        random_seed=42
    ):

        self._buyer_name = buyer_name

        # ----------------------------------------------------
        # PRIVATE PROCUREMENT POLICY
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # STOCHASTIC DECISION PARAMETERS
        # ----------------------------------------------------

        self._noise_strength = (
            noise_strength
        )

        self._boundary_width = (
            boundary_width
        )


        # ----------------------------------------------------
        # REPRODUCIBLE RANDOM GENERATOR
        # ----------------------------------------------------

        self._random = random.Random(
            random_seed
        )


        # ----------------------------------------------------
        # OBSERVATION COUNTERS
        # ----------------------------------------------------

        self._evaluation_count = 0

        self._noise_event_count = 0


    # ========================================================
    # NORMALISED DISTANCE
    # ========================================================

    @staticmethod
    def _normalised_distance(
        value,
        threshold,
        scale
    ):

        if scale <= 0:

            return 0.0


        return (

            abs(
                value - threshold
            )
            /
            scale

        )


    # ========================================================
    # DISTANCE FROM NEAREST POLICY BOUNDARY
    # ========================================================

    def _nearest_boundary_distance(
        self,
        proposal
    ):

        distances = []


        # ----------------------------------------------------
        # PRICE
        # ----------------------------------------------------

        distances.append(

            self._normalised_distance(

                proposal.annual_price,

                self._max_budget,

                100000.0

            )

        )


        # ----------------------------------------------------
        # CONTRACT LENGTH
        # ----------------------------------------------------

        distances.append(

            self._normalised_distance(

                proposal.contract_months,

                self._maximum_contract_months,

                48.0

            )

        )


        # ----------------------------------------------------
        # SERVICE AVAILABILITY
        # ----------------------------------------------------

        distances.append(

            self._normalised_distance(

                proposal.service_availability,

                self._minimum_service_availability,

                10.0

            )

        )


        # ----------------------------------------------------
        # PAYMENT DAYS
        # ----------------------------------------------------

        distances.append(

            self._normalised_distance(

                proposal.payment_days,

                self._minimum_payment_days,

                83.0

            )

        )


        # ----------------------------------------------------
        # SUPPLIER RELIABILITY
        # ----------------------------------------------------

        distances.append(

            self._normalised_distance(

                proposal.supplier_reliability,

                self._minimum_supplier_reliability,

                40.0

            )

        )


        return min(
            distances
        )


    # ========================================================
    # DETERMINISTIC HIDDEN POLICY
    # ========================================================

    def _deterministic_policy(
        self,
        proposal
    ):

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
    # NOISE PROBABILITY
    # ========================================================

    def _calculate_noise_probability(
        self,
        proposal
    ):

        distance = (
            self._nearest_boundary_distance(
                proposal
            )
        )


        # ----------------------------------------------------
        # Outside the boundary region, decisions are stable.
        # ----------------------------------------------------

        if (
            distance
            >=
            self._boundary_width
        ):

            return 0.0


        # ----------------------------------------------------
        # Noise becomes stronger as the proposal approaches
        # the nearest hidden policy boundary.
        # ----------------------------------------------------

        proximity = (

            1.0
            -
            (
                distance
                /
                self._boundary_width
            )

        )


        probability = (

            self._noise_strength
            *
            proximity

        )


        return max(

            0.0,

            min(
                probability,
                0.49
            )

        )


    # ========================================================
    # PUBLIC BLACK-BOX BUYER INTERFACE
    # ========================================================

    def evaluate_proposal(
        self,
        proposal
    ):

        self._evaluation_count += 1


        deterministic_result = (
            self._deterministic_policy(
                proposal
            )
        )


        deterministic_acceptance = (
            deterministic_result[
                "accepted"
            ]
        )


        noise_probability = (
            self._calculate_noise_probability(
                proposal
            )
        )


        noise_event = (

            self._random.random()
            <
            noise_probability

        )


        if noise_event:

            self._noise_event_count += 1

            observed_acceptance = (
                not deterministic_acceptance
            )

        else:

            observed_acceptance = (
                deterministic_acceptance
            )


        decision = (

            "ACCEPTED"

            if observed_acceptance

            else "REJECTED"

        )


        # ----------------------------------------------------
        # IMPORTANT
        #
        # The public response intentionally does NOT expose:
        #
        # - hidden thresholds
        # - deterministic decision
        # - violations
        # - noise probability
        # - whether a noise event occurred
        #
        # The discovery algorithm sees only black-box output.
        # ----------------------------------------------------

        return {

            "buyer":
                self._buyer_name,

            "decision":
                decision,

            "message":
                (
                    "Proposal accepted."

                    if observed_acceptance

                    else
                    "Proposal does not satisfy "
                    "procurement requirements."
                )

        }


    # ========================================================
    # EVALUATION-ONLY DIAGNOSTICS
    # ========================================================
    #
    # These diagnostics are intended for the Experiment 018
    # benchmark AFTER discovery.
    #
    # They must not be supplied to the discovery algorithm.
    # ========================================================

    def get_diagnostics(
        self
    ):

        noise_rate = (

            self._noise_event_count
            /
            self._evaluation_count

            if self._evaluation_count

            else 0.0

        )


        return {

            "total_evaluations":
                self._evaluation_count,

            "noise_events":
                self._noise_event_count,

            "realised_noise_rate":
                noise_rate

        }


# ============================================================
# PROBABILISTIC BUYER FACTORY
# ============================================================

class ProbabilisticBuyerFactory:

    @staticmethod
    def create_buyer(
        random_seed=42,
        noise_strength=0.15,
        boundary_width=0.05
    ):

        return ProbabilisticAutonomousBuyer(

            buyer_name=(
                "Probabilistic Enterprise "
                "Procurement Agent"
            ),

            max_budget=105000,

            maximum_contract_months=36,

            minimum_service_availability=98.0,

            minimum_payment_days=30,

            minimum_supplier_reliability=85.0,

            noise_strength=(
                noise_strength
            ),

            boundary_width=(
                boundary_width
            ),

            random_seed=(
                random_seed
            )

        )


    # ========================================================
    # EVALUATION-ONLY GROUND TRUTH
    # ========================================================

    @staticmethod
    def ground_truth():

        return {

            "annual_price":
                105000,

            "contract_months":
                36,

            "service_availability":
                98.0,

            "payment_days":
                30,

            "supplier_reliability":
                85.0

        }
