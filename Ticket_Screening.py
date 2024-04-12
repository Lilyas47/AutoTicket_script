import numpy as np
import cv2

# Load the image
image_path = 'D:\\Python_Problems\\screenshot.png'
image = cv2.imread(image_path)

# Convert the image to the HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# Define the range of red color in HSV
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# Create masks for red color
mask1 = cv2.inRange(hsv, lower_red, upper_red)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
red_mask = cv2.bitwise_or(mask1, mask2)

# Find contours in the mask
contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Calculate the center of each contour
red_centers = []
for contour in contours:
    # Calculate the moments of the contour
    M = cv2.moments(contour)
    # Calculate the center
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        red_centers.append((cX, cY))
# Draw contours on the original image
for i, center in enumerate(red_centers):
    cv2.drawContours(image, contours, i, (0, 255, 0), 2)
    cv2.circle(image, center, 5, (255, 0, 0), -1)

# Save the resulting image
contoured_image_path = 'D:\\Python_Problems\\contoured_screenshot.png'
cv2.imwrite(contoured_image_path, image)


print(red_centers)