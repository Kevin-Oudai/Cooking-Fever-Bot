import pyautogui as p
import time
import os

# Find Ordered Item
# Location: 'items/ordered_item/<item>
CONF = 0.95
MOUSE_SPEED = 0.13
COFFEE_LOCATIONS = [(337, 717), (406, 726), (480, 733)]
MS_LOCATIONS = [(637, 688), (678, 602), (702, 523)]
OVEN_LOCATIONS = [(1462, 591), (1437, 707), (1417, 816), (1393, 941)]

ORDER_REGIONS = [
    (280, 130, 160, 300),
    (630, 130, 160, 300),
    (970, 130, 160, 300),
    (1320, 130, 160, 300),
]

PAN_LOCATIONS = [
    # (846, 688),
    # (866, 582),
    # (1046, 586),
    (1058, 690)
]
MENU = [
    'vanilla', 'chocolate', 'custard',
    'strawberry_vanilla',  # 'strawberry_chocolate',
    'strawberry_custard',
    'peach_vanilla', 'peach_chocolate', 'peach_custard',
    'blueberry_vanilla',  # 'blueberry_chocolate',
    'blueberry_custard',
    'coffee', 'milkshake',
    'strawberry_blueberry_vanilla',
]
ORDER = []
CAKE_QUEUE = []
MONEY_REGIONS = [
    (450, 380, 90, 90),
    (790, 380, 90, 90),
    (1130, 380, 90, 90),
    (1480, 380, 90, 90)
]
MONEY = [
    (500, 430),
    (830, 430),
    (1180, 430),
    (1530, 430)
]


class Cake:
    def __init__(self, flavor, location, oven):
        self.frosting = None
        self.topping = None
        self.flavor = flavor
        self.delivery_location = location
        self.oven_location = oven
        self.countdown = 29
        self.set_topping()
        self.make_cake()
        self.baking()

    def update(self, val):
        self.countdown -= val
        return self.countdown

    def set_topping(self):
        if self.flavor == 'vanilla':
            self.frosting = (1240, 623)
        if self.flavor == 'strawberry_vanilla':
            self.frosting = (1240, 623)
            self.topping = [(960, 801)]
        if self.flavor == 'peach_vanilla':
            self.frosting = (1240, 623)
            self.topping = [(860, 800)]
        if self.flavor == 'blueberry_vanilla':
            self.frosting = (1240, 623)
            self.topping = [(1090, 800)]
        if self.flavor == 'chocolate':
            self.frosting = (1275, 716)
        if self.flavor == 'peach_chocolate':
            self.frosting = (1275, 716)
            self.topping = [(860, 800)]
        if self.flavor == 'custard':
            self.frosting = (1216, 533)
        if self.flavor == 'peach_custard':
            self.frosting = (1216, 533)
            self.topping = [(860, 800)]
        if self.flavor == 'blueberry_custard':
            self.frosting = (1216, 533)
            self.topping = [(1090, 800)]
        if self.flavor == 'strawberry_custard':
            self.frosting = (1216, 533)
            self.topping = [(960, 801)]
        if self.flavor == 'strawberry_blueberry_vanilla':
            self.frosting = (1240, 623)
            self.topping = [(960, 801), (1090, 800)]

    def make_cake(self):
        addMold = click((953, 917))
        serve_item(self.frosting, PAN_LOCATIONS[0])
        if self.topping:
            for topping in self.topping:
                serve_item(topping, PAN_LOCATIONS[0])

    def baking(self):
        if len(CAKE_QUEUE) == 4:
            remaining_time = 21
            for cake in CAKE_QUEUE:
                if cake.countdown < remaining_time:
                    remaining_time = cake.countdown
            time.sleep(remaining_time * 0.15)
            update_queue(remaining_time)
        serve_item(PAN_LOCATIONS[0], self.oven_location)
        CAKE_QUEUE.append(self)

    def serve_cake(self):
        serve_item(self.oven_location, self.delivery_location)


def restart(location):
    time.sleep(6)
    prepare.coffee_count = 0
    prepare.mscounter = 0
    p.click(1360, 941)
    time.sleep(6)
    p.click(626, 834)


def store_data():
    """This will be used to capture images of a particular region to test a machine learning
    algorithm if the tests are successful"""
    pass


def click(loc):
    # Takes 0.2 secs to execute
    p.moveTo(loc[0], loc[1], MOUSE_SPEED)
    p.click()
    update_queue(1)


def serve_item(start, stop):
    """
    This function moves to a location and drags an object from that location to another.
    input:  start -> tuple containing the coordinates for the start point.
            stop -> tuple containing the coordinates for the end point.
    output: None
    """
    # Takes 0.4 secs to execute.
    p.moveTo(start[0], start[1], MOUSE_SPEED)
    p.dragTo(stop[0], stop[1], MOUSE_SPEED, button='left')
    update_queue(2)


def update_queue(val):
    if len(CAKE_QUEUE) > 0:
        rem = 5
        for i in range(len(CAKE_QUEUE)):
            re = CAKE_QUEUE[i].update(val)
            if re <= 0:
                rem = i
        if rem < 5:
            CAKE_QUEUE.pop(rem).serve_cake()


def find_order():
    """
    This function searches a particular region to determine if a menu item exists in that location
    """
    for item in MENU:
        for rgn in ORDER_REGIONS:
            # p.screenshot("images/data/{}.png".format(rgn[0]), region=rgn)
            searchFor = 'images/menu/{}.png'.format(item)
            locateItem = p.locateCenterOnScreen(
                searchFor, region=rgn, confidence=CONF)
            if locateItem:
                data = {'item': item, 'location': locateItem}
                ORDER.append(data)


def prepare():
    while len(ORDER) > 0:
        a = ORDER.pop(0)
        item = a['item']
        if item == 'coffee':
            coffeeLocation = COFFEE_LOCATIONS[prepare.coffee_count % 3]
            prepare.coffee_count += 1
            serve_item(coffeeLocation, a['location'])
        elif item == 'milkshake':
            msLocation = MS_LOCATIONS[prepare.mscounter % 3]
            if prepare.mscounter % 3 == 0:
                click((626, 834))
                serve_item(msLocation, a['location'])
                prepare.mscounter += 1
            else:
                prepare.mscounter += 1
                serve_item(msLocation, a['location'])
        else:
            Cake(item, a['location'], OVEN_LOCATIONS[prepare.cakecount % 4])
            prepare.cakecount += 1
    collect_money()
    while len(CAKE_QUEUE) > 0:
        time.sleep(MOUSE_SPEED)
        update_queue(1)
    collect_money()


def collect_money():
    for rgn in MONEY:
        p.click(rgn)
# Main Control


def main():
    delay = 6
    prepare.coffee_count = 0
    prepare.mscounter = 0
    prepare.cakecount = 0
    print("Starting CFBot...")
    time.sleep(delay)
    click((626, 834))
    prepare.mscounter += 1
    while True:
        find_order()
        prepare()
        restart_button = p.locateCenterOnScreen(
            'images/ref/restart.png')
        if restart_button:
            # break
            restart(restart_button)


main()
