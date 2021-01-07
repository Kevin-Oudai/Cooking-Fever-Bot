import pyautogui as p
import time
import os

# Find Ordered Item
# Location: 'items/ordered_item/<item>
CONF = 0.95
MOUSE_SPEED = 0.20
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
    'strawberry_vanilla',  # 'strawberry_chocolate', 'strawberry_custard',
    'peach_vanilla', 'peach_chocolate', 'peach_custard',
    # 'blueberry_vanilla', 'blueberry_chocolate', 'blueberry_custard',
    'coffee', 'milkshake'
]
ORDER = []
CAKE_QUEUE = []


class Cake:
    def __init__(self, flavor, location, oven):
        print("Making {}".format(flavor))
        self.frosting = None
        self.topping = None
        self.flavor = flavor
        self.delivery_location = location
        self.oven_location = oven
        self.countdown = 21
        self.set_topping()
        print("frosting: {}\t topping: {}".format(self.frosting, self.topping))
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
            self.topping = (960, 801)
        if self.flavor == 'peach_vanilla':
            self.frosting = (1240, 623)
            self.topping = (860, 800)
        if self.flavor == 'chocolate':
            self.frosting = (1275, 716)
        if self.flavor == 'peach_chocolate':
            self.frosting = (1275, 716)
            self.topping = (860, 800)
        if self.flavor == 'custard':
            self.frosting = (1216, 533)
        if self.flavor == 'peach_custard':
            self.frosting = (1216, 533)
            self.topping = (860, 800)

    def make_cake(self):
        addMold = click((953, 917))
        # Add Frosting
        serve_item(self.frosting, PAN_LOCATIONS[0])
        # Add self.topping
        if self.topping:
            serve_item(self.topping, PAN_LOCATIONS[0])
        print("Created Cake")

    def baking(self):
        if len(CAKE_QUEUE) == 4:
            print("Waiting for oven")
            remaining_time = 21
            for cake in CAKE_QUEUE:
                if cake.get_time() < remaining_time:
                    remaining_time = cake.get_time()
            time.sleep(remaining_time * 0.2)
            update_queue(remaining_time)
        print("Placing Cake in oven")
        serve_item(PAN_LOCATIONS[0], self.oven_location)
        CAKE_QUEUE.append(self)

    def serve_cake(self):
        print("Taking cake out of oven")
        serve_item(self.oven_location, self.delivery_location)
        print("Serving cake to customer")


def restart(location):
    time.sleep(5)
    prepare.coffee_count = 0
    prepare.mscounter = 0
    ORDER = []
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
    collect_money()


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
            p.screenshot("images/data/{}.png".format(rgn[0]), region=rgn)
            searchFor = 'images/menu/{}.png'.format(item)
            locateItem = p.locateCenterOnScreen(
                searchFor, region=rgn, confidence=CONF)
            if locateItem:
                data = {'item': item, 'location': locateItem}
                print("Found {}".format(data))
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
            if prepare.mscounter % 3 == 0:
                click((626, 834))
                ORDER.append({'item': item, 'location': a['location']})
                prepare.mscounter += 1
            else:
                msLocation = MS_LOCATIONS[prepare.mscounter % 3]
                prepare.mscounter += 1
                serve_item(msLocation, a['location'])
        else:
            Cake(item, a['location'], OVEN_LOCATIONS[prepare.cakecount % 4])
            prepare.cakecount += 1
    while len(CAKE_QUEUE) > 0:
        time.sleep(1)
        update_queue(5)


def collect_money():
    location = p.locateCenterOnScreen(
        'images/ref/money.png', confidence=CONF)
    # consider reducing the region when searching for money
    if location:
        click(location)
# Main Control


def main():
    delay = 6
    prepare.coffee_count = 0
    prepare.mscounter = 0
    prepare.cakecount = 0
    time.sleep(delay)
    click((626, 834))
    prepare.mscounter += 1
    while True:
        find_order()
        prepare()
        collect_money()
        restart_button = p.locateCenterOnScreen(
            'images/ref/restart.png')
        if restart_button:
            break
            # restart(restart_button)


main()
