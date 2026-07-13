from __future__ import annotations

from track3.evaluation.evaluate import evaluate_model


class Validator:

    def __init__(
        self,
        model,
        dataset_root,
    ):

        self.model = model
        self.dataset_root = dataset_root

    def validate(self):

        metrics = evaluate_model(
            model=self.model,
            dataset_root=self.dataset_root,
        )

        return metrics