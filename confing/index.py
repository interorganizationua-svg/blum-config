import cv2
import numpy as np
import mss
import pygetwindow as gw
import random
import time
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener, KeyCode
import sys
import threading

mouse = MouseController()

print("Owner: @ggkryptoua ")

print("\nВиберіть мову:")
print("1. Українська")
print("2. English")
print("3. Polish")

paused = False
freeze = False

click_index = 0 

def click(x, y):
    mouse.position = (x, y + random.randint(1, 3)) 
    mouse.press(Button.left)
    mouse.release(Button.left)

def on_press(key):
    global paused, freeze
    if key == KeyCode(char='q'):
        paused = not paused
        if paused:
            print(pause_message)
        else:
            print(continue_message)
    if key == KeyCode(char='w'):
        freeze = not freeze
        if freeze:
            print(freeze_on_message)
        else:
            print(freeze_off_message)

# Запускаємо слухач клавіатури
listener = Listener(on_press=on_press)
listener.start()


while True:
    try:
        laung_choose = int(input("Виберіть мову щоб продовжити:"))
        if laung_choose in [1, 2, 3]:
            break   
        else:
            print("Вибачте але ви не обрали мову, виберіть 1, 2 чи 3 ")
    except ValueError:
        print("Не правильно ви вписали, будь ласка повторіть знову")

if laung_choose == 1:
    window_input = "\n Введіть назву вікна (1 - TelegramDesktop): "
    window_none = "\n [❌] | Вікно - {} не знайдено"
    window_on = "\n [🟢] Вікно активне - {}\n Натисніть 'q' для паузи"
    pause_message = "Пауза\nНатисніть 'q' ще раз, щоб продовжити"
    continue_message = "Продовжую роботу"
    error_message = "Вибачте, ви забули вписати номер вікна '1' "
    freeze_on_message = "Заморозка увімкнена"
    freeze_off_message = "Заморозка вимкнена"

elif laung_choose == 2:
    window_input = "\n Enter name Window (2 - TelegramDesktop): "
    window_none = "\n [❌] | Window - {} none"
    window_on = "\n [🟢] Window on - {}\n Press 'q' to pause"
    pause_message = "Pause\nPause 'q' again continue"
    continue_message = "Continue working"
    error_message = "Sorry, you forgot to enter the window number '2' "
    freeze_on_message = "Freeze enabled"
    freeze_off_message = "Freeze disabled"

elif laung_choose == 3:
    window_input = "\n Podaj nazwę okna (3 - TelegramDesktop): "
    window_none = "\n [❌] | Brak okna - {}"
    window_on = "\n [🟢] Okno aktywne - {}\n Naciśnij 'q', aby wstrzymać"
    pause_message = "Pauza\nNaciśnij ponownie 'q', aby kontynuować"
    continue_message = "Kontynuuj pracę"
    error_message = "Przepraszamy, zapomniałeś podać numer okna '3' "
    freeze_on_message = "Zamrażanie włączone"
    freeze_off_message = "Zamrażanie wyłączone"

window_name = input(f'Введіть назву вікна: {window_input}')

if window_name in ['1', '2', '3']:
    window_name = "TelegramDesktop"
else:
    print(error_message)
    sys.exit()

def window_rest_none():
    windows = gw.getWindowsWithTitle(window_name)
    if not windows:
        print(window_none.format(window_name))
        return
    else:
        print(window_on.format(window_name))
        return
    
window_rest_none()

def find_green_object(image):
    # Перетворення кольору BGR в HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Визначення діапазону зеленого кольору в HSV
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    
    # Створення маски для зелених пікселів
    mask = cv2.inRange(hsv, lower_green, upper_green)

    kernel = np.ones((5, 5), np.uint8) 
    mask=cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    mask=cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    # Знаходження контурів зелених об'єктів
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    green_objects = []
    
    # Проходження крізь знайдені контури
    for contour in contours:
        # Визначення прямокутника, який охоплює контур
        x, y, w, h = cv2.boundingRect(contour)
        
        # Перевірка розміру прямокутника
        if cv2.contourArea(contour) > 100:  # Поріг для розміру об'єкту
            # Додавання координат та розмірів об'єкта у список
            green_objects.append((x, y, w, h))

    return green_objects


def find_freeze_object(freeze):
    hsv = cv2.cvtColor(freeze, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([108, 208, 221])
    
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    freeze_objects = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > 100:
            freeze_objects.append((x, y, w, h))
    
    return freeze_objects


def click_objects():   
    global click_index
    while True:
        if not paused:
                active_window = gw.getActiveWindow()
                if active_window and active_window.title == window_name:
                    with mss.mss() as sct:
                        windows = gw.getWindowsWithTitle(window_name)
                        if not windows:
                            print(window_none.format(window_name))
                        else:
                            window = windows[0]
                            monitor = {
                                "top": window.top,
                                "left": window.left,
                                "width": window.width,
                                "height": window.height,
                            }
                            img = np.array(sct.grab(monitor))
                            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                            green_objects = find_green_object(img_bgr)

                            if green_objects:
                                x, y, w, h = green_objects[click_index % len(green_objects)]
                                # Клікнути в центр зеленого об'єкта
                                x_click = monitor["left"] + x + w // 2
                                y_click = monitor["top"] + y + h // 2
                                click(x_click, y_click)

                            if freeze:
                                freeze_objects = find_freeze_object(img_bgr)
                                if freeze_objects:
                                    x, y, w, h = freeze_objects[click_index % len(freeze_objects)]
                                    # Клікнути в центр зеленого об'єкта
                                    x_click = monitor["left"] + x + w // 2
                                    y_click = monitor["top"] + y + h // 2
                                    click(x_click, y_click)


                            click_index += 1
                    time.sleep(0.08)
                else:
                    time.sleep(0.08)
        else:
            time.sleep(0.08)

obj_click = threading.Thread(target=click_objects)
obj_click.start()
