# Cooking-Fever-Bot

## Overview
Cooking-Fever-Bot is an automation script for the **Cooking Fever** game. The bot uses
image detection and simulated mouse events to prepare cakes, coffees, and milkshakes
on stage 2 of the game. It automatically recognizes incoming orders and prepares the
corresponding items, aiming to survive levels beyond 35.

## Setup
1. Install Python 3.8 or newer.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the game (1920x1080 resolution recommended on Windows or an emulator).
4. Start the bot:
   ```bash
   python CFBot.py
   ```
   - Use `--dry-run` to log actions without clicking.

> **Note:** If your game assets differ, replace images in `images/menu` with updated
templates to improve detection.

## Project Structure
| Path        | Description                                   |
|-------------|-----------------------------------------------|
| `CFBot.py`  | Main entry point of the bot.                  |
| `Cake.py`   | Legacy cake logic (kept for reference).       |
| `calibrate.py` | Capture helper to test click regions.      |
| `images/`   | Template images used for order recognition.   |

## Platform Support
The bot has been tested on **Windows** with a 1920x1080 screen. PyAutoGUI's
screenshot features may not work reliably on other platforms without additional
configuration.

## Screenshots
_Add a screenshot or GIF of the bot running here to showcase detections and actions._

## History
- **v1.0** – Initial release: worked up to level 20 of stage 2.
- **v2.0** – Improved logic but still unstable.
- **v2.1** – Stable up to level 35 with various fixes.

