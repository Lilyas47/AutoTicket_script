from selenium import webdriver
import cv2
import numpy as np
from PIL import Image
import io
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import pyautogui
import requests
import bs4
user_name = "Бийбосунов Ильяс Алмазович"
user_phone_number = "+79955002286"
user_email = "iliasgoy@gmail.com"

# Указать путь к WebDriver
webdriver_path = 'D:\\Python_Problems\\chromedriver.exe'  # Убедитесь, что путь указан правильно

# Создание объекта Service с указанием пути к ChromeDriver
service = Service(executable_path=webdriver_path)

# Настройка опций браузера
options = webdriver.ChromeOptions()
options.add_argument("--start-fullscreen")
#options.add_argument("--start-maximized")
# Инициализация драйвера с использованием Service и опций
driver = webdriver.Chrome(service=service, options=options)
url = 'https://iframeab-pre9117.intickets.ru/seance/14731249/#abiframe'
driver.get(url)  # Перейти на нужную веб-страницу
time.sleep(10)

driver.find_element(By.CLASS_NAME, 'outline-x24-icon-plus').click()

# Создание скриншота страницы
screenshot = driver.get_screenshot_as_png()
driver.save_screenshot("screenshot.png")
# Преобразование скриншота в формат, который можно обработать с помощью OpenCV
image_cv = Image.open(io.BytesIO(screenshot))
image = cv2.cvtColor(np.array(image_cv), cv2.COLOR_RGB2BGR)

# Теперь image_cv является изображением, которое можно обрабатывать в OpenCV
# Например, вы можете отобразить изображение


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
x_coordinates = []
y_coordinates = []
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
    x_coordinates.append(cX)
    y_coordinates.append(cY)
    # Отрисовываем точку центра на исходном изображении
    cv2.circle(image, (cX, cY), 5, (0, 0, 0), -1)
    cv2.putText(image, "центр", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


# Создаем объект ActionChains


# Создаем экземпляр ActionChains
actions = ActionChains(driver)
dots = [(1374, 278), (1342, 278), (1309, 278), (1278, 278), (1246, 278), (1215, 278), (1183, 278), (991, 278), (768, 278), (737, 278), (705, 278), (672, 278), (641, 278), (609, 278), (578, 278), (546, 278), (1374, 245), (1278, 245), (1246, 246), (1215, 246), (1183, 245), (1150, 246), (1119, 246), (801, 245), (768, 246), (672, 245), (641, 245), (609, 246), (578, 246), (546, 245), (1342, 215), (1309, 215), (1278, 215), (1246, 215), (1215, 215), (1183, 215), (801, 215), (768, 215), (737, 215), (705, 215), (672, 215), (641, 215), (609, 215), (578, 215), (1342, 182), (1309, 182), (1278, 182), (1246, 182), (578, 182), (1202, 87)]
# Перемещаемся к верхнему левому углу элемента с небольшим отступом, чтобы учесть возможные рамки и отступы
# Возможно, вам придется подобрать значения offsetX и offsetY, чтобы курсор оказался именно в углу
for i in range(1):
    #ActionChains(driver).move_by_offset(dots[i][0], dots[i][1] + 40).click().perform()
    #ActionChains(driver).reset_actions()

    # Предположим, что у вас есть координаты относительно всего экрана
    absolute_x = dots[10][0]
    absolute_y = dots[10][1] + 55

    # Переместить мышь к абсолютным координатам и выполнить клик
    pyautogui.moveTo(absolute_x, absolute_y)
    pyautogui.click()
    time.sleep(2)
pyautogui.moveTo(1770, 960)
pyautogui.click()
time.sleep(4)

driver.find_element(By.NAME, 'name').send_keys(user_name)
driver.find_element(By.NAME, 'phone').send_keys(user_phone_number)
driver.find_element(By.NAME, 'email').send_keys(user_email)
pyautogui.moveTo(950, 800)
pyautogui.click()
screenshot = driver.get_screenshot_as_png()
time.sleep(4)
driver.save_screenshot("result.png")
time.sleep(1000)
#cv2.imshow('Result', image)
#cv2.imshow('Mask', mask)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
driver.quit()   # Закрытие браузера после создания скриншота