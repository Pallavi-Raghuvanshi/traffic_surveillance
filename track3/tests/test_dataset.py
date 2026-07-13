from track3.data.dataloader import build_train_loader

loader = build_train_loader(

    dataset_root="D:\Documents\\traffic_surveillance\\track3\VeRi",

    batch_size=8,

    num_workers=0,

)

batch = next(iter(loader))

print(batch["image"].shape)

print(batch["vehicle_id"])

print(batch["camera_id"])
