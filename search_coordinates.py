import numpy as np
import cv2

# Загрузка изображения
image_path = 'D:\\Python_Problems\\screenshot.png'
image = cv2.imread(image_path)

# Функция для преобразования RGB порогов в HSV
def convert_rgb_to_hsv_thresholds(lower_rgb, upper_rgb):
    # Преобразование RGB порогов в HSV пороги
    lower_hsv = cv2.cvtColor(np.uint8([[lower_rgb]]), cv2.COLOR_RGB2HSV)[0][0]
    upper_hsv = cv2.cvtColor(np.uint8([[upper_rgb]]), cv2.COLOR_RGB2HSV)[0][0]
    return lower_hsv, upper_hsv

# Опредение диапазона цвета, который вы хотите найти
lower_rgb = np.array([190, 0, 0])  # Например, [60, 100, 50]
upper_rgb = np.array([229, 0, 0])  # Например, [100, 140, 90]

# Преобразование RGB порогов в HSV пороги
lower_hsv, upper_hsv = convert_rgb_to_hsv_thresholds(lower_rgb, upper_rgb)

# Преобразование изображения в HSV цветовое пространство
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Создание маски для выбранного цвета
color_mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

# Нахождение контуров в маске
contours, _ = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Расчет центра каждого контура
color_centers = []
for contour in contours:
    # Расчет моментов контура
    M = cv2.moments(contour)
    # Расчет центра
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        color_centers.append((cX, cY))

# Рисование контуров на оригинальном изображении
for i, center in enumerate(color_centers):
    cv2.drawContours(image, contours, i, (0, 255, 0), 2)
    cv2.circle(image, center, 5, (255, 0, 0), -1)

# Сохранение результата
contoured_image_path = 'D:\\Python_Problems\\contoured_screenshot.png'
cv2.imwrite(contoured_image_path, image)

print(color_centers)
