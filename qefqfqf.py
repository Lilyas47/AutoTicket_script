from selenium import webdriver
import cv2
import numpy as np
from PIL import Image
import io
from selenium.webdriver.chrome.service import Service
import time

# Указать путь к WebDriver
webdriver_path = 'D:\\Python_Problems\\chromedriver.exe'  # Убедитесь, что путь указан правильно

# Создание объекта Service с указанием пути к ChromeDriver
service = Service(executable_path=webdriver_path)

# Инициализация драйвера с использованием Service и опций
driver = webdriver.Chrome(service=service)

# Устанавливаем размер окна браузера
driver.set_window_size(1200, 800)

driver.get('https://iframeab-pre9117.intickets.ru/seance/14731249/#abiframe')  # Перейти на нужную веб-страницу
time.sleep(10)
# Создание скриншота страницы
screenshot = driver.get_screenshot_as_png()
#driver.quit()  # Закрытие браузера после создания скриншота

# Преобразование скриншота в формат, который можно обработать с помощью OpenCV
image_cv = Image.open(io.BytesIO(screenshot))
image = cv2.cvtColor(np.array(image_cv), cv2.COLOR_RGB2BGR)

# Теперь image_cv является изображением, которое можно обрабатывать в OpenCV
# Например, вы можете отобразить изображение
#cv2.imshow('Screenshot', image)

# Здесь вы можете добавить дополнительный код обработки с использованием OpenCV...
# Преобразуем BGR в HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Задаем диапазон красного цвета в HSV
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

# Создаем маску для выделения красного цвета
mask = cv2.inRange(hsv, lower_red, upper_red)

# Находим контуры на маске
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Отрисовываем контуры на исходном изображении
for cnt in contours:
    # Используем моменты контуров для вычисления центра
    M = cv2.moments(cnt)
    # Проверяем, чтобы избежать деления на ноль
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    # Выводим координаты центра на консоль
    print("Центр контура находится в точке: X:", cX, "Y:", cY)

    # Отрисовываем точку центра на исходном изображении
    cv2.circle(image, (cX, cY), 5, (0, 0, 0), -1)
    cv2.putText(image, "центр", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# Отображаем исходное изображение с отмеченными центрами контуров
cv2.imshow('Result', image)
cv2.imshow('Mask', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()