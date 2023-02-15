import cv2
import numpy as np
# Define the center point of the polygons
center = (150, 150)
# Define the first polygon vertices as a numpy array of shape (n,2)
polygon1_vertices = np.array([[100, 100], [150, 50], [200, 100]], dtype=np.int32)
# Define the second polygon vertices as a numpy array of shape (n,2)
polygon2_vertices = np.array([[100, 200], [150, 250], [200, 200]], dtype=np.int32)
# Create an empty image to draw the polygons on
img = np.zeros((300, 300, 3), dtype=np.uint8)
# Draw the first polygon on the image
cv2.fillPoly(img, [polygon1_vertices + center], (255, 0, 0))
# Draw the second polygon on the image
cv2.fillPoly(img, [polygon2_vertices + center], (0, 255, 0))
# Display the image
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
