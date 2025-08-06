"""Calibration helper for Cooking-Fever-Bot.

Press 'c' to capture a small screenshot around the current mouse
position. Press 'q' to quit.
"""

import os
import time

import keyboard
import pyautogui

CAPTURE_DIR = "calibration"


def main():
    os.makedirs(CAPTURE_DIR, exist_ok=True)
    count = 0
    print("Press 'c' to capture region, 'q' to quit.")
    while True:
        if keyboard.is_pressed('c'):
            x, y = pyautogui.position()
            region = (x - 50, y - 50, 100, 100)
            path = os.path.join(CAPTURE_DIR, f"capture_{count}.png")
            screenshot = pyautogui.screenshot(region=region)
            screenshot.save(path)
            print(f"Captured {path}")
            count += 1
            time.sleep(0.5)
        if keyboard.is_pressed('q'):
            break
        time.sleep(0.1)


if __name__ == "__main__":
    main()
