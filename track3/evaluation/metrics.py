from __future__ import annotations

import numpy as np


class ReIDEvaluator:
    """
    Evaluates Vehicle Re-ID performance.

    Metrics
    -------
    - Rank-1 Accuracy
    - Rank-5 Accuracy
    - Mean Average Precision (mAP)
    """

    @staticmethod
    def evaluate(
    similarity: np.ndarray,
    query_labels: np.ndarray,
    gallery_labels: np.ndarray,
    query_cameras: np.ndarray,
    gallery_cameras: np.ndarray,
) -> dict:

        num_queries = similarity.shape[0]

        rank1_correct = 0
        rank5_correct = 0

        average_precisions = []

        for i in range(num_queries):

            scores = similarity[i]

            ranked_indices = np.argsort(scores)[::-1]

            ranked_labels = gallery_labels[ranked_indices]
            ranked_cameras = gallery_cameras[ranked_indices]

            # Remove gallery images from the same camera
            valid = ranked_cameras != query_cameras[i]

            ranked_labels = ranked_labels[valid]

            matches = ranked_labels == query_labels[i]

            if len(matches) == 0:
                average_precisions.append(0.0)
                continue

            if matches[0]:
                rank1_correct += 1

            if np.any(matches[:5]):
                rank5_correct += 1

            correct_positions = np.where(matches)[0]

            precisions = []

            for position in correct_positions:

                precision = (
                    matches[: position + 1].sum()
                    / (position + 1)
                )

                precisions.append(precision)

            average_precisions.append(
                np.mean(precisions)
            )

        return {

            "rank1":
                rank1_correct / num_queries,

            "rank5":
                rank5_correct / num_queries,

            "mAP":
                np.mean(average_precisions),

        }