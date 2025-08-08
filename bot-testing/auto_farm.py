import keyboard
import time
import sys
import cv2
import numpy as np
import pyautogui

def get_game_area():
    # Adjust these coordinates to your game area location and size
    x, y, w, h = 200, 100, 1200, 700  # Example values for 1600x900, tune as needed!
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    cv2.imshow("Game Area", frame)
    cv2.waitKey(1)
    return frame

def find_mobs(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Brown (spider) HSV range (tune as needed)
    lower_brown = np.array([10, 80, 40])
    upper_brown = np.array([25, 255, 200])
    # Blue/white (skeleton) HSV range (tune as needed)
    lower_blue = np.array([90, 10, 180])
    upper_blue = np.array([120, 80, 255])
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.bitwise_or(mask_brown, mask_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:  # Larger area for mobs
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centers.append((cx, cy))
    # Debug: Print number of detected mobs
    print("Detected mob centers:", centers)
    return centers

def move_toward(center, target):
    dx = target[0] - center[0]
    dy = target[1] - center[1]
    # Determine which keys to press for movement
    keys_to_press = []
    if abs(dx) > 10:
        if dx > 0:
            keys_to_press.append('d')  # right
        else:
            keys_to_press.append('a')  # left
    if abs(dy) > 10:
        if dy > 0:
            keys_to_press.append('s')  # down
        else:
            keys_to_press.append('w')  # up
    # Release keys not needed
    for key in ['w', 'a', 's', 'd']:
        if key not in keys_to_press:
            keyboard.release(key)
    # Press required keys
    for key in keys_to_press:
        keyboard.press(key)

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
    debug = True  # Set to True to show minimap and detection
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

            # Mob detection and movement
            frame = get_game_area()
            mob_centers = find_mobs(frame)
            game_center = (frame.shape[1] // 2, frame.shape[0] // 2)

            if debug:
                debug_frame = frame.copy()
                # Draw game center
                cv2.circle(debug_frame, game_center, 5, (255, 255, 0), -1)
                # Draw detected mobs
                for c in mob_centers:
                    cv2.circle(debug_frame, c, 5, (0, 0, 255), -1)
                cv2.imshow("Game Debug", debug_frame)
                cv2.waitKey(1)

            if mob_centers:
                # Move toward the closest mob
                closest = min(mob_centers, key=lambda c: (c[0]-game_center[0])**2 + (c[1]-game_center[1])**2)
                dx = closest[0] - game_center[0]
                dy = closest[1] - game_center[1]
                keys_to_press = set()
                if abs(dx) > 20:
                    keys_to_press.add('d' if dx > 0 else 'a')
                if abs(dy) > 20:
                    keys_to_press.add('s' if dy > 0 else 'w')
                # Release keys not needed
                for key in held_keys - keys_to_press:
                    keyboard.release(key)
                # Press new keys
                for key in keys_to_press - held_keys:
                    keyboard.press(key)
                held_keys = keys_to_press
            else:
                # Release movement keys if no mobs detected
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