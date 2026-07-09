from __future__ import annotations

from track3.data.dataloader import (
    build_query_loader,
    build_gallery_loader,
)

from track3.evaluation.embedding_extractor import (
    EmbeddingExtractor,
)

from track3.evaluation.metrics import ReIDEvaluator
from track3.evaluation.similarity import Similarity

from track3.models.osnet import OSNetModel

DATASET_ROOT = r"D:\Documents\\traffic_surveillance\\track3\VeRi"
BATCH_SIZE = 64
NUM_WORKERS = 4

def evaluate_model(
    model,
    dataset_root,
    batch_size=64,
    num_workers=4,
):

    query_loader = build_query_loader(
        dataset_root=dataset_root,
        batch_size=batch_size,
        num_workers=num_workers,
    )

    gallery_loader = build_gallery_loader(
        dataset_root=dataset_root,
        batch_size=batch_size,
        num_workers=num_workers,
    )

    extractor = EmbeddingExtractor(model)

    query_embeddings, query_labels, query_cameras = extractor.extract(
        query_loader
    )

    gallery_embeddings, gallery_labels, gallery_cameras = extractor.extract(
        gallery_loader
    )

    similarity = Similarity.cosine(
        query_embeddings,
        gallery_embeddings,
    )

    metrics = ReIDEvaluator.evaluate(
        similarity,
        query_labels,
        gallery_labels,
        query_cameras,
        gallery_cameras,
    )

    return metrics
def main():

    model = OSNetModel(
        num_classes=576,
    )

    metrics = evaluate_model(
        model=model,
        dataset_root=DATASET_ROOT,
    )

    print("\n========== Vehicle Re-ID ==========")

    print(f"Rank-1 : {metrics['rank1']*100:.2f}%")
    print(f"Rank-5 : {metrics['rank5']*100:.2f}%")
    print(f"mAP    : {metrics['mAP']*100:.2f}%")
if __name__ == "__main__":
    main()
