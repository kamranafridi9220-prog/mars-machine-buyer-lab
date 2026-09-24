"""
MARS — Machine-Agent Revenue Science

Experiment 010

Adversarial Buyer Behaviour and
Strategic Negotiation Defence

Author: Kamran Khan

Research Objective:

Investigate whether an autonomous supplier
can adapt to different buyer negotiation
behaviours while protecting commercial value.

This module uses synthetic buyer behaviours.
It does not infer the intentions of real people.
"""

import random

from dataclasses import dataclass


# ==================================================
# NEGOTIATION CONFIGURATION
# ==================================================

@dataclass
class NegotiationConfig:

    contract_value: float = 120000

    maximum_concession: float = 15000

    initial_concession: float = 3000

    concession_step: float = 2000

    maximum_rounds: int = 8


# ==================================================
# AUTONOMOUS BUYER SIMULATOR
# ==================================================

class AdversarialBuyerSimulator:

    def __init__(
        self,
        buyer_type,
        seed=42
    ):

        self.buyer_type = buyer_type

        self.random = random.Random(seed)

        self.round_number = 0

        self.previous_concession = 0

        self.demand_history = []

        self.hidden_thresholds = {

            "Cooperative": 6000,

            "Strategic": 10000,

            "Unpredictable": 8000

        }

    # --------------------------------------------------
    # GENERATE BUYER DEMAND
    # --------------------------------------------------

    def generate_demand(self):

        self.round_number += 1

        if self.buyer_type == "Cooperative":

            demand = 6000

        elif self.buyer_type == "Strategic":

            demand = (

                5000

                + self.previous_concession * 0.5

                + self.round_number * 1000

            )

        elif self.buyer_type == "Unpredictable":

            demand = self.random.randint(

                3000,

                14000

            )

        else:

            raise ValueError(

                "Unknown buyer type"

            )

        demand = min(

            15000,

            demand

        )

        self.demand_history.append(

            demand

        )

        return demand

    # --------------------------------------------------
    # EVALUATE SUPPLIER OFFER
    # --------------------------------------------------

    def evaluate_offer(
        self,
        concession
    ):

        self.previous_concession = concession

        threshold = self.hidden_thresholds[

            self.buyer_type

        ]

        if self.buyer_type == "Strategic":

            # A strategic buyer may continue
            # negotiating despite an offer
            # satisfying its underlying threshold.

            if concession >= threshold:

                acceptance_probability = 0.65

            else:

                acceptance_probability = 0.05

        elif self.buyer_type == "Unpredictable":

            if concession >= threshold:

                acceptance_probability = 0.75

            else:

                acceptance_probability = 0.15

        else:

            acceptance_probability = (

                1.0

                if concession >= threshold

                else 0.0

            )

        accepted = (

            self.random.random()

            < acceptance_probability

        )

        return {

            "accepted": accepted,

            "buyer_type": self.buyer_type,

            "concession": concession,

            "round": self.round_number

        }


# ==================================================
# BUYER BEHAVIOUR INTELLIGENCE
# ==================================================

class BuyerBehaviourIntelligence:

    def __init__(self):

        self.demand_history = []

    # --------------------------------------------------
    # OBSERVE BUYER
    # --------------------------------------------------

    def observe(
        self,
        demand
    ):

        self.demand_history.append(

            demand

        )

    # --------------------------------------------------
    # ANALYSE BEHAVIOUR
    # --------------------------------------------------

    def analyse(self):

        if len(
            self.demand_history
        ) < 3:

            return {

                "classification": "Insufficient Data",

                "risk_score": 0.0

            }

        recent = self.demand_history[-3:]

        changes = [

            recent[index + 1]

            - recent[index]

            for index in range(2)

        ]

        increasing = all(

            change > 0

            for change in changes

        )

        volatility = (

            max(recent)

            - min(recent)

        )

        if increasing:

            classification = (

                "Escalating Demands"

            )

            risk_score = 0.85

        elif volatility > 4000:

            classification = (

                "Volatile Demands"

            )

            risk_score = 0.65

        else:

            classification = (

                "Stable Demands"

            )

            risk_score = 0.15

        return {

            "classification":
                classification,

            "risk_score":
                risk_score

        }


# ==================================================
# SUPPLIER NEGOTIATION DEFENCE
# ==================================================

class StrategicNegotiationDefence:

    def __init__(
        self,
        config
    ):

        self.config = config

        self.current_concession = (

            config.initial_concession

        )

        self.intelligence = (

            BuyerBehaviourIntelligence()

        )

        self.concession_history = []

    # --------------------------------------------------
    # SELECT NEGOTIATION ACTION
    # --------------------------------------------------

    def select_action(
        self,
        buyer_demand
    ):

        self.intelligence.observe(

            buyer_demand

        )

        analysis = (

            self.intelligence.analyse()

        )

        classification = analysis[

            "classification"

        ]

        if classification == (

            "Escalating Demands"

        ):

            action = "HOLD_POSITION"

        elif classification == (

            "Volatile Demands"

        ):

            action = "CONTROLLED_CONCESSION"

        else:

            action = "STANDARD_CONCESSION"

        if action == "STANDARD_CONCESSION":

            proposed = (

                self.current_concession

                + self.config.concession_step

            )

        elif action == "CONTROLLED_CONCESSION":

            proposed = (

                self.current_concession

                + self.config.concession_step / 2

            )

        else:

            proposed = (

                self.current_concession

            )

        self.current_concession = min(

            proposed,

            self.config.maximum_concession

        )

        self.concession_history.append(

            self.current_concession

        )

        return {

            "action": action,

            "concession":
                self.current_concession,

            "classification":
                classification,

            "risk_score":
                analysis["risk_score"]

        }


# ==================================================
# NEGOTIATION EXPERIMENT ENGINE
# ==================================================

class NegotiationExperimentEngine:

    def __init__(
        self,
        buyer,
        supplier,
        config
    ):

        self.buyer = buyer

        self.supplier = supplier

        self.config = config

        self.history = []

    # --------------------------------------------------
    # RUN NEGOTIATION
    # --------------------------------------------------

    def run(self):

        for round_number in range(

            1,

            self.config.maximum_rounds + 1

        ):

            demand = (

                self.buyer.generate_demand()

            )

            supplier_action = (

                self.supplier.select_action(

                    demand

                )

            )

            concession = supplier_action[

                "concession"

            ]

            buyer_result = (

                self.buyer.evaluate_offer(

                    concession

                )

            )

            record = {

                "round": round_number,

                "buyer_demand": demand,

                "supplier_action":
                    supplier_action["action"],

                "concession":
                    concession,

                "classification":
                    supplier_action[
                        "classification"
                    ],

                "risk_score":
                    supplier_action[
                        "risk_score"
                    ],

                "accepted":
                    buyer_result[
                        "accepted"
                    ]

            }

            self.history.append(

                record

            )

            if buyer_result["accepted"]:

                return {

                    "agreement": True,

                    "rounds": round_number,

                    "final_concession":
                        concession,

                    "history":
                        self.history

                }

        return {

            "agreement": False,

            "rounds":
                self.config.maximum_rounds,

            "final_concession":
                self.supplier.current_concession,

            "history":
                self.history

        }
