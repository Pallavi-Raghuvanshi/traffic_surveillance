import cv2

from track3.core.reid_service import ReIDService

image = cv2.imread("track3/VeRi/image_query/0002_c002_00030600_0.jpg")

service = ReIDService()

embedding = service.extract_embedding(image)

print(type(embedding))
print(embedding.shape)
print(embedding.dtype)