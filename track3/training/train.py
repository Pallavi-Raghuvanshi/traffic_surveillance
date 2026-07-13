from track3.data.dataloader import build_train_loader
from track3.data.veri_dataset import VeRiDataset
from track3.models.osnet import OSNetModel
from track3.training.trainer import Trainer


DATASET_ROOT = r"D:\Documents\traffic_surveillance\track3\VeRi"
BATCH_SIZE = 32
NUM_WORKERS = 0
EPOCHS = 60

def main():

    dataset = VeRiDataset(
        root=DATASET_ROOT,
        split="train",
        training=True,
    )

    loader = build_train_loader(
    dataset_root=DATASET_ROOT,
    batch_size=BATCH_SIZE,
    num_workers=NUM_WORKERS,
)

    model = OSNetModel(
        num_classes=dataset.num_classes,
        loss="softmax",
    )

    trainer = Trainer(
        model=model,
        train_loader=loader,
        dataset_root=DATASET_ROOT,
    )

    trainer.train(
        epochs=1,
    )


if __name__ == "__main__":
    main()