import keyboard
import time
import cv2
import numpy as np
import pyautogui
import os

def get_game_area():
    x, y, w, h = 165, 85, 1595, 720
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return frame

def load_templates(folder):
    templates = []
    for filename in os.listdir(folder):
        if filename.lower().endswith('.png'):
            path = os.path.join(folder, filename)
            img = cv2.imread(path)
            if img is not None:
                templates.append(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    return templates

def find_mobs_with_templates(frame, templates, threshold=0.7):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    centers = []
    for template in templates:
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            centers.append((pt[0] + w//2, pt[1] + h//2))
    return centers

def main():
    print("===== Space Button Auto-Clicker with Mob Detection =====")
    print("Controls: 'q' - Quit | '+' - Faster | '-' - Slower")
    delay = 0.1
    input("Press ENTER to start...")
    print("\nStarting in 5 seconds...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print(f"\nAuto-clicking space started with {delay:.2f}s delay!")

    held_keys = set()
    mob_template_folder = r"c:\Users\Sibiya Gaming\Desktop\python-bot-learning\mob_templates"
    templates = load_templates(mob_template_folder)
    try:
        while True:
            if keyboard.is_pressed('q'):
                print("\nStopping auto-clicker...")
                break
            elif keyboard.is_pressed('+') or keyboard.is_pressed('='):
                delay = max(0.01, delay - 0.01)
                print(f"\nSpeed increased! New delay: {delay:.2f}s")
                time.sleep(0.2)
            elif keyboard.is_pressed('-') or keyboard.is_pressed('_'):
                delay = min(1.0, delay + 0.01)
                print(f"\nSpeed decreased! New delay: {delay:.2f}s")
                time.sleep(0.2)

            frame = get_game_area()
            mob_centers = find_mobs_with_templates(frame, templates)
            game_center = (frame.shape[1] // 2, frame.shape[0] // 2)

            if mob_centers:
                closest = min(mob_centers, key=lambda c: (c[0]-game_center[0])**2 + (c[1]-game_center[1])**2)
                dx = closest[0] - game_center[0]
                dy = closest[1] - game_center[1]
                keys_to_press = set()
                if abs(dx) > 20:
                    keys_to_press.add('d' if dx > 0 else 'a')
                if abs(dy) > 20:
                    keys_to_press.add('s' if dy > 0 else 'w')
                for key in held_keys - keys_to_press:
                    keyboard.release(key)
                for key in keys_to_press - held_keys:
                    keyboard.press(key)
                held_keys = keys_to_press
            else:
                for key in held_keys:
                    keyboard.release(key)
                held_keys.clear()

            keyboard.press_and_release('space')
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

    print("Auto-clicker stopped.")

if __name__ == "__main__":
    main()