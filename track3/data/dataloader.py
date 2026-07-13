from torch.utils.data import DataLoader

from track3.data.transforms import train_transform

from track3.data.veri_dataset import VeRiDataset
from track3.data.transforms import test_transform


def build_train_loader( 
    dataset_root,
    batch_size,
    num_workers,
):

    dataset = VeRiDataset(
        root=dataset_root,
        split="train",
        transform=train_transform,
        training=True,
    )

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=False,
    )


def build_query_loader(
    dataset_root,
    batch_size,
    num_workers,
):

    dataset = VeRiDataset(
        root=dataset_root,
        split="query",
        transform=test_transform,
        training=False,
    )
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=False,
    )


def build_gallery_loader(
    dataset_root,
    batch_size,
    num_workers,
):

    dataset = VeRiDataset(
        root=dataset_root,
        split="gallery",
        transform=test_transform,
        training=False,
    )

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=False,
    )
