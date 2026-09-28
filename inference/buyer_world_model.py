"""
MARS — Machine-Agent Revenue Science

Experiment 024

Autonomous Buyer World Model

Author: Kamran Khan

Purpose:
Learn a predictive representation of autonomous buyer
behaviour from historical black-box interaction episodes.

Unlike earlier MARS experiments, this model does not use
a manually specified Gaussian mapping between observed
instability and latent buyer environments.

Instead, it learns relationships between observable
behavioural features and buyer-environment labels from
training episodes.

The world model can then:

1. Learn from historical buyer interactions.
2. Predict the latent environment of a new buyer.
3. Estimate predictive uncertainty.
4. measure similarity to previously observed environments.
5. Update itself with new interaction episodes.

True environment labels are required during supervised
training/evaluation, but are NOT required when predicting
a new buyer environment.
"""

import math
import statistics
from collections import Counter, defaultdict


# ============================================================
# BUYER WORLD MODEL
# ============================================================

class BuyerWorldModel:

    def __init__(
        self,
        k_neighbors=7,
        distance_epsilon=1e-9
    ):

        if k_neighbors < 1:

            raise ValueError(
                "k_neighbors must be at least 1."
            )

        self.k_neighbors = (
            k_neighbors
        )

        self.distance_epsilon = (
            distance_epsilon
        )

        self.training_examples = []

        self.feature_names = [

            "mean_acceptance_rate",
            "acceptance_rate_stdev",
            "mean_minority_rate",
            "mean_disagreement",
            "maximum_disagreement",
            "mean_entropy",
            "maximum_entropy",
            "stable_probe_fraction",
            "unstable_probe_fraction"
        ]

        self.feature_means = {}

        self.feature_stdevs = {}

        self.environment_counts = Counter()

        self.is_fitted = False


    # ========================================================
    # BINARY ENTROPY
    # ========================================================

    @staticmethod
    def _binary_entropy(
        probability
    ):

        probability = float(
            probability
        )

        if (
            probability <= 0.0
            or
            probability >= 1.0
        ):

            return 0.0

        return -(
            probability
            *
            math.log2(
                probability
            )
            +
            (
                1.0
                -
                probability
            )
            *
            math.log2(
                1.0
                -
                probability
            )
        )


    # ========================================================
    # SAFE MEAN
    # ========================================================

    @staticmethod
    def _safe_mean(
        values,
        default=0.0
    ):

        values = [

            float(value)

            for value in values

            if value is not None
        ]

        if not values:

            return float(
                default
            )

        return statistics.mean(
            values
        )


    # ========================================================
    # SAFE STDEV
    # ========================================================

    @staticmethod
    def _safe_stdev(
        values
    ):

        values = [

            float(value)

            for value in values

            if value is not None
        ]

        if len(values) < 2:

            return 0.0

        return statistics.stdev(
            values
        )


    # ========================================================
    # EXTRACT PROBE STATISTICS
    # ========================================================

    @staticmethod
    def _extract_probe_statistics(
        diagnostic_result
    ):

        probe_statistics = (
            diagnostic_result.get(
                "probe_statistics",
                []
            )
        )

        if isinstance(
            probe_statistics,
            dict
        ):

            return list(
                probe_statistics.values()
            )

        if isinstance(
            probe_statistics,
            list
        ):

            return probe_statistics

        raise ValueError(
            "Unsupported probe_statistics format."
        )


    # ========================================================
    # EXTRACT FEATURES
    # ========================================================

    def extract_features(
        self,
        diagnostic_result
    ):

        """
        Convert a diagnostic interaction episode into
        a fixed-dimensional behavioural representation.

        Only observable buyer decisions are used.
        """

        probe_statistics = (
            self._extract_probe_statistics(
                diagnostic_result
            )
        )

        if not probe_statistics:

            raise ValueError(
                "Diagnostic result contains no "
                "probe statistics."
            )

        acceptance_rates = []

        minority_rates = []

        disagreements = []

        entropies = []

        stable_probe_count = 0

        unstable_probe_count = 0

        observed_probe_count = 0


        for probe in (
            probe_statistics
        ):

            observations = (
                probe.get(
                    "observations",
                    0
                )
                or
                0
            )

            if observations <= 0:

                continue

            observed_probe_count += 1

            acceptance_rate = (
                probe.get(
                    "acceptance_rate"
                )
            )

            if acceptance_rate is None:

                accepted = (
                    probe.get(
                        "accepted",
                        0
                    )
                    or
                    0
                )

                acceptance_rate = (
                    accepted
                    /
                    observations
                )

            acceptance_rate = float(
                acceptance_rate
            )

            minority_rate = (
                probe.get(
                    "minority_rate"
                )
            )

            if minority_rate is None:

                minority_rate = min(
                    acceptance_rate,
                    1.0 - acceptance_rate
                )

            minority_rate = float(
                minority_rate
            )

            disagreement = (
                probe.get(
                    "disagreement"
                )
            )

            if disagreement is None:

                disagreement = (
                    2.0
                    *
                    minority_rate
                )

            disagreement = float(
                disagreement
            )

            entropy = (
                probe.get(
                    "entropy"
                )
            )

            if entropy is None:

                entropy = (
                    self._binary_entropy(
                        acceptance_rate
                    )
                )

            entropy = float(
                entropy
            )

            acceptance_rates.append(
                acceptance_rate
            )

            minority_rates.append(
                minority_rate
            )

            disagreements.append(
                disagreement
            )

            entropies.append(
                entropy
            )


            if disagreement <= 0.20:

                stable_probe_count += 1


            if disagreement >= 0.50:

                unstable_probe_count += 1


        if observed_probe_count <= 0:

            raise ValueError(
                "No observed diagnostic probes "
                "were available for feature extraction."
            )


        features = {

            "mean_acceptance_rate":
                self._safe_mean(
                    acceptance_rates
                ),

            "acceptance_rate_stdev":
                self._safe_stdev(
                    acceptance_rates
                ),

            "mean_minority_rate":
                self._safe_mean(
                    minority_rates
                ),

            "mean_disagreement":
                self._safe_mean(
                    disagreements
                ),

            "maximum_disagreement":
                max(
                    disagreements
                )
                if disagreements
                else 0.0,

            "mean_entropy":
                self._safe_mean(
                    entropies
                ),

            "maximum_entropy":
                max(
                    entropies
                )
                if entropies
                else 0.0,

            "stable_probe_fraction":
                (
                    stable_probe_count
                    /
                    observed_probe_count
                ),

            "unstable_probe_fraction":
                (
                    unstable_probe_count
                    /
                    observed_probe_count
                )
        }

        return features


    # ========================================================
    # ADD TRAINING EPISODE
    # ========================================================

    def add_training_episode(
        self,
        diagnostic_result,
        environment_label,
        metadata=None
    ):

        features = (
            self.extract_features(
                diagnostic_result
            )
        )

        example = {

            "features":
                features,

            "environment_label":
                float(
                    environment_label
                ),

            "metadata":
                metadata
                if metadata is not None
                else {}
        }

        self.training_examples.append(
            example
        )

        self.environment_counts[
            float(
                environment_label
            )
        ] += 1

        self.is_fitted = False

        return example


    # ========================================================
    # FIT FEATURE NORMALISATION
    # ========================================================

    def fit(
        self
    ):

        if not self.training_examples:

            raise ValueError(
                "World model has no training examples."
            )

        for feature_name in (
            self.feature_names
        ):

            values = [

                example[
                    "features"
                ][
                    feature_name
                ]

                for example in (
                    self.training_examples
                )
            ]

            mean_value = (
                statistics.mean(
                    values
                )
            )

            if len(values) >= 2:

                stdev_value = (
                    statistics.stdev(
                        values
                    )
                )

            else:

                stdev_value = 0.0


            if stdev_value <= 0.0:

                stdev_value = 1.0


            self.feature_means[
                feature_name
            ] = mean_value

            self.feature_stdevs[
                feature_name
            ] = stdev_value


        self.is_fitted = True

        return self.generate_training_summary()


    # ========================================================
    # STANDARDISE FEATURES
    # ========================================================

    def _standardise_features(
        self,
        features
    ):

        if not self.is_fitted:

            raise ValueError(
                "World model must be fitted before prediction."
            )

        vector = []

        for feature_name in (
            self.feature_names
        ):

            value = float(
                features[
                    feature_name
                ]
            )

            mean_value = (
                self.feature_means[
                    feature_name
                ]
            )

            stdev_value = (
                self.feature_stdevs[
                    feature_name
                ]
            )

            standardised = (
                value
                -
                mean_value
            ) / stdev_value

            vector.append(
                standardised
            )

        return vector


    # ========================================================
    # EUCLIDEAN DISTANCE
    # ========================================================

    @staticmethod
    def _euclidean_distance(
        first,
        second
    ):

        return math.sqrt(
            sum(
                (
                    a
                    -
                    b
                ) ** 2

                for a, b in zip(
                    first,
                    second
                )
            )
        )


    # ========================================================
    # BUILD TRAINING VECTOR
    # ========================================================

    def _training_vector(
        self,
        example
    ):

        return (
            self._standardise_features(
                example[
                    "features"
                ]
            )
        )


    # ========================================================
    # FIND NEAREST EXPERIENCES
    # ========================================================

    def find_nearest_experiences(
        self,
        diagnostic_result,
        k=None
    ):

        if not self.is_fitted:

            raise ValueError(
                "World model must be fitted before prediction."
            )

        if k is None:

            k = (
                self.k_neighbors
            )

        features = (
            self.extract_features(
                diagnostic_result
            )
        )

        query_vector = (
            self._standardise_features(
                features
            )
        )

        distances = []

        for index, example in enumerate(
            self.training_examples
        ):

            training_vector = (
                self._training_vector(
                    example
                )
            )

            distance = (
                self._euclidean_distance(
                    query_vector,
                    training_vector
                )
            )

            distances.append(
                {
                    "index":
                        index,

                    "distance":
                        distance,

                    "environment_label":
                        example[
                            "environment_label"
                        ],

                    "metadata":
                        example[
                            "metadata"
                        ]
                }
            )


        distances.sort(
            key=lambda item: (
                item[
                    "distance"
                ],
                item[
                    "environment_label"
                ]
            )
        )

        k = min(
            int(
                k
            ),
            len(
                distances
            )
        )

        return distances[
            :k
        ]


    # ========================================================
    # PREDICT ENVIRONMENT
    # ========================================================

    def predict_environment(
        self,
        diagnostic_result
    ):

        neighbors = (
            self.find_nearest_experiences(
                diagnostic_result
            )
        )

        if not neighbors:

            raise ValueError(
                "No training experiences available."
            )


        environment_weights = defaultdict(
            float
        )

        total_weight = 0.0


        for neighbor in (
            neighbors
        ):

            distance = (
                neighbor[
                    "distance"
                ]
            )

            weight = (
                1.0
                /
                (
                    distance
                    +
                    self.distance_epsilon
                )
            )

            environment = (
                neighbor[
                    "environment_label"
                ]
            )

            environment_weights[
                environment
            ] += weight

            total_weight += weight


        if total_weight <= 0.0:

            raise ValueError(
                "Unable to calculate environment weights."
            )


        environment_probabilities = {

            environment:
                weight
                /
                total_weight

            for environment, weight in (
                environment_weights.items()
            )
        }


        predicted_environment = max(
            environment_probabilities,
            key=environment_probabilities.get
        )


        expected_environment = sum(

            environment
            *
            probability

            for environment, probability in (
                environment_probabilities.items()
            )
        )


        confidence = (
            environment_probabilities[
                predicted_environment
            ]
        )


        prediction_entropy = 0.0

        for probability in (
            environment_probabilities.values()
        ):

            if probability > 0.0:

                prediction_entropy -= (
                    probability
                    *
                    math.log2(
                        probability
                    )
                )


        nearest_distance = (
            neighbors[
                0
            ][
                "distance"
            ]
        )


        mean_neighbor_distance = (
            statistics.mean(
                neighbor[
                    "distance"
                ]
                for neighbor in (
                    neighbors
                )
            )
        )


        return {

            "predicted_environment":
                predicted_environment,

            "expected_environment":
                expected_environment,

            "confidence":
                confidence,

            "prediction_entropy":
                prediction_entropy,

            "nearest_distance":
                nearest_distance,

            "mean_neighbor_distance":
                mean_neighbor_distance,

            "environment_probabilities":
                dict(
                    sorted(
                        environment_probabilities.items()
                    )
                ),

            "neighbors":
                neighbors
        }


    # ========================================================
    # UPDATE WORLD MODEL
    # ========================================================

    def update(
        self,
        diagnostic_result,
        environment_label,
        metadata=None,
        refit=True
    ):

        example = (
            self.add_training_episode(
                diagnostic_result=diagnostic_result,
                environment_label=environment_label,
                metadata=metadata
            )
        )

        if refit:

            self.fit()

        return example


    # ========================================================
    # TRAINING SUMMARY
    # ========================================================

    def generate_training_summary(
        self
    ):

        environments = sorted(
            self.environment_counts.keys()
        )

        return {

            "training_examples":
                len(
                    self.training_examples
                ),

            "environment_classes":
                len(
                    environments
                ),

            "environments":
                environments,

            "examples_per_environment":
                {
                    environment:
                        self.environment_counts[
                            environment
                        ]

                    for environment in (
                        environments
                    )
                },

            "feature_count":
                len(
                    self.feature_names
                ),

            "feature_names":
                list(
                    self.feature_names
                ),

            "fitted":
                self.is_fitted
        }


    # ========================================================
    # PRINT TRAINING SUMMARY
    # ========================================================

    def print_training_summary(
        self
    ):

        summary = (
            self.generate_training_summary()
        )

        print(
            "\n"
            +
            "=" * 80
        )

        print(
            "MARS — BUYER WORLD MODEL"
        )

        print(
            "=" * 80
        )

        print(
            "Training Examples:",
            summary[
                "training_examples"
            ]
        )

        print(
            "Environment Classes:",
            summary[
                "environment_classes"
            ]
        )

        print(
            "Feature Count:",
            summary[
                "feature_count"
            ]
        )

        print(
            "Model Fitted:",
            summary[
                "fitted"
            ]
        )

        print(
            "\nExamples Per Environment"
        )

        for environment, count in (
            summary[
                "examples_per_environment"
            ].items()
        ):

            print(
                f"{environment:.2f}: "
                f"{count}"
            )

        print(
            "=" * 80
        )
