"""Main bot logic for Cooking-Fever-Bot."""

import argparse
import logging
import os
import time

import keyboard
import pyautogui

# Find Ordered Item
# Location: 'items/ordered_item/<item>'
CONFIDENCE_THRESHOLD = 0.95
MOUSE_MOVE_DURATION = 0.13
COFFEE_LOCATIONS = [(337, 717), (406, 726), (480, 733)]
MILKSHAKE_LOCATIONS = [(637, 688), (678, 602), (702, 523)]
OVEN_LOCATIONS = [(1462, 591), (1437, 707), (1417, 816), (1393, 941)]

ORDER_DETECTION_REGIONS = [
    (280, 130, 160, 300),
    (630, 130, 160, 300),
    (970, 130, 160, 300),
    (1320, 130, 160, 300),
]

PAN_LOCATIONS = [
    (1058, 690)
]
MENU_ITEMS = [
    'vanilla', 'chocolate', 'custard',
    'strawberry_vanilla',  # 'strawberry_chocolate',
    'strawberry_custard',
    'peach_vanilla', 'peach_chocolate', 'peach_custard',
    'blueberry_vanilla',  # 'blueberry_chocolate',
    'blueberry_custard',
    'coffee', 'milkshake',
    'strawberry_blueberry_vanilla',
]
order_queue = []
cake_queue = []
MONEY_DETECTION_REGIONS = [
    (450, 380, 90, 90),
    (790, 380, 90, 90),
    (1130, 380, 90, 90),
    (1480, 380, 90, 90)
]
MONEY_LOCATIONS = [
    (500, 430),
    (830, 430),
    (1180, 430),
    (1530, 430)
]

SCREEN_RESOLUTION = (1920, 1080)
LOOP_COOLDOWN = 0.1
DRY_RUN = False

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Cake:
    """Represents a cake in progress."""

    def __init__(self, flavor, delivery_location, oven_location):
        """Initialize a cake with flavor and target locations."""
        self.frosting = None
        self.toppings = []
        self.flavor = flavor
        self.delivery_location = delivery_location
        self.oven_location = oven_location
        self.countdown = 29
        self.set_topping()
        self.make_cake()
        self.bake()

    def update(self, elapsed):
        """Decrease countdown by elapsed seconds."""
        self.countdown -= elapsed
        return self.countdown

    def set_topping(self):
        """Set frosting and topping coordinates based on flavor."""
        if self.flavor == 'vanilla':
            self.frosting = (1240, 623)
        if self.flavor == 'strawberry_vanilla':
            self.frosting = (1240, 623)
            self.toppings = [(960, 801)]
        if self.flavor == 'peach_vanilla':
            self.frosting = (1240, 623)
            self.toppings = [(860, 800)]
        if self.flavor == 'blueberry_vanilla':
            self.frosting = (1240, 623)
            self.toppings = [(1090, 800)]
        if self.flavor == 'chocolate':
            self.frosting = (1275, 716)
        if self.flavor == 'peach_chocolate':
            self.frosting = (1275, 716)
            self.toppings = [(860, 800)]
        if self.flavor == 'custard':
            self.frosting = (1216, 533)
        if self.flavor == 'peach_custard':
            self.frosting = (1216, 533)
            self.toppings = [(860, 800)]
        if self.flavor == 'blueberry_custard':
            self.frosting = (1216, 533)
            self.toppings = [(1090, 800)]
        if self.flavor == 'strawberry_custard':
            self.frosting = (1216, 533)
            self.toppings = [(960, 801)]
        if self.flavor == 'strawberry_blueberry_vanilla':
            self.frosting = (1240, 623)
            self.toppings = [(960, 801), (1090, 800)]

    def make_cake(self):
        """Assemble frosting and toppings on a pan."""
        click((953, 917))
        serve_item(self.frosting, PAN_LOCATIONS[0])
        for topping in self.toppings:
            serve_item(topping, PAN_LOCATIONS[0])

    def bake(self):
        """Move the cake to an oven and track baking time."""
        if len(cake_queue) == 4:
            remaining_time = 21
            for cake in cake_queue:
                if cake.countdown < remaining_time:
                    remaining_time = cake.countdown
            time.sleep(remaining_time * 0.15)
            update_queue(remaining_time)
        serve_item(PAN_LOCATIONS[0], self.oven_location)
        cake_queue.append(self)

    def serve_cake(self):
        """Deliver baked cake to customer."""
        serve_item(self.oven_location, self.delivery_location)


def restart(location):
    """Restart the level after failure."""
    time.sleep(6)
    prepare.coffee_count = 0
    prepare.milkshake_count = 0
    pyautogui.click(1360, 941)
    time.sleep(6)
    pyautogui.click(626, 834)


def store_data():
    """Capture images for future machine-learning experiments."""
    # Placeholder for future work
    pass


def click(location):
    """Move the mouse and click a location.

    Args:
        location (tuple): Target coordinates.
    """
    logging.debug("Click %s", location)
    if DRY_RUN:
        return
    pyautogui.moveTo(location[0], location[1], MOUSE_MOVE_DURATION)
    pyautogui.click()
    update_queue(1)


def serve_item(start, stop):
    """Drag from start to stop locations.

    Args:
        start (tuple): Starting coordinates.
        stop (tuple): Ending coordinates.
    """
    logging.debug("Drag %s -> %s", start, stop)
    if DRY_RUN:
        return
    pyautogui.moveTo(start[0], start[1], MOUSE_MOVE_DURATION)
    pyautogui.dragTo(stop[0], stop[1], MOUSE_MOVE_DURATION, button='left')
    update_queue(2)


def update_queue(elapsed):
    """Update countdown for cakes in the oven."""
    if len(cake_queue) > 0:
        index_to_remove = 5
        for idx in range(len(cake_queue)):
            remaining = cake_queue[idx].update(elapsed)
            if remaining <= 0:
                index_to_remove = idx
        if index_to_remove < 5:
            cake_queue.pop(index_to_remove).serve_cake()


def find_order():
    """Search order regions for known menu items."""
    for item in MENU_ITEMS:
        for region in ORDER_DETECTION_REGIONS:
            image_path = f'images/menu/{item}.png'
            location = pyautogui.locateCenterOnScreen(
                image_path, region=region, confidence=CONFIDENCE_THRESHOLD)
            if location:
                order_queue.append({'item': item, 'location': location})


def prepare():
    """Prepare items from the order queue."""
    while len(order_queue) > 0:
        order_entry = order_queue.pop(0)
        item = order_entry['item']
        if item == 'coffee':
            coffee_location = COFFEE_LOCATIONS[prepare.coffee_count % 3]
            prepare.coffee_count += 1
            serve_item(coffee_location, order_entry['location'])
        elif item == 'milkshake':
            shake_location = MILKSHAKE_LOCATIONS[prepare.milkshake_count % 3]
            if prepare.milkshake_count % 3 == 0:
                click((626, 834))
            serve_item(shake_location, order_entry['location'])
            prepare.milkshake_count += 1
        else:
            Cake(item, order_entry['location'],
                 OVEN_LOCATIONS[prepare.cake_count % 4])
            prepare.cake_count += 1
    collect_money()
    while len(cake_queue) > 0:
        time.sleep(MOUSE_MOVE_DURATION)
        update_queue(1)
    collect_money()


def collect_money():
    """Click on money icons to collect earnings."""
    for location in MONEY_LOCATIONS:
        click(location)


def check_resolution(expected=SCREEN_RESOLUTION):
    """Validate screen resolution before running."""
    width, height = pyautogui.size()
    if (width, height) != expected:
        logging.error("Screen resolution %s does not match expected %s", (width, height), expected)
        return False
    return True


def main():
    """Entry point for running the bot."""
    parser = argparse.ArgumentParser(description="Cooking Fever Bot")
    parser.add_argument("--dry-run", action="store_true", help="Run without performing clicks")
    args = parser.parse_args()
    global DRY_RUN
    DRY_RUN = args.dry_run
    prepare.coffee_count = 0
    prepare.milkshake_count = 0
    prepare.cake_count = 0
    if not check_resolution():
        return
    logging.info("Starting CFBot%s", " in dry-run mode" if DRY_RUN else "")
    time.sleep(6)
    click((626, 834))
    prepare.milkshake_count += 1
    while True:
        if keyboard.is_pressed("esc"):
            logging.info("Stopping bot")
            break
        find_order()
        prepare()
        restart_button = pyautogui.locateCenterOnScreen('images/ref/restart.png')
        if restart_button:
            restart(restart_button)
        time.sleep(LOOP_COOLDOWN)


if __name__ == "__main__":
    main()
