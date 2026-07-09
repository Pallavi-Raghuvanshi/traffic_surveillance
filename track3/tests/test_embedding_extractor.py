from track3.data.dataloader import build_query_loader

from track3.models.osnet import OSNetModel

from track3.evaluation.embedding_extractor import EmbeddingExtractor


loader = build_query_loader(
    dataset_root="D:\Documents\\traffic_surveillance\\track3\VeRi",
    batch_size=32,
    num_workers=0,
)

dataset = loader.dataset

model = OSNetModel(
    num_classes=dataset.num_classes,
)

extractor = EmbeddingExtractor(model)

embeddings, labels = extractor.extract(loader)

print(embeddings.shape)

print(labels.shape)
