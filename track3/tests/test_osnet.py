import torch

from track3.models.osnet import OSNetModel


model = OSNetModel()

dummy = torch.randn(1, 3, 256, 256)

embedding = model(dummy)

print(embedding.shape)