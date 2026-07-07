from torchreid.models import build_model

model = build_model(
    name="osnet_x1_0",
    num_classes=1000,
    pretrained=True,
)

print(type(model))
print("Model created successfully!")