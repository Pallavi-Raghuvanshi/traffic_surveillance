import cv2

from track3.core.preprocessing import ImagePreprocessor

image = cv2.imread("track3/VeRi/image_query/0002_c002_00030600_0.jpg")

preprocessor = ImagePreprocessor()

tensor = preprocessor(image)

print(tensor.shape)
print(tensor.dtype)