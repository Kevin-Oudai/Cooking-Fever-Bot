import pyautogui
import time
import os

# Find Ordered Item
# Location: 'items/ordered_item/<item>
CONF = 0.8
MOUSE_SPEED = 0.20
COFFEE_LOCATIONS = [(337, 717), (406, 726), (480, 733)]
MS_LOCATIONS = [(635, 703), (671, 617), (706, 537)]
OVEN_LOCATIONS = [(1462, 591), (1437, 707), (1417, 816), (1393, 941)]
# ORDER_REGIONS = [
#     (282, 130, 156, 266),
#     (632, 139, 161, 273),
#     (974, 136, 156, 268),
#     (1321, 138, 160, 272)
# ]

ORDER_REGIONS = [
    (300, 120, 128, 128),
    (300, 150, 128, 128),
    (300, 200, 128, 128),
    (300, 230, 128, 128),
    (300, 280, 128, 128),

    (650, 120, 128, 128),
    (650, 150, 128, 128),
    (650, 200, 128, 128),
    (650, 230, 128, 128),
    (650, 280, 128, 128),

    (990, 120, 128, 128),
    (990, 150, 128, 128),
    (990, 200, 128, 128),
    (990, 230, 128, 128),
    (990, 280, 128, 128),

    (1340, 120, 128, 128),
    (1340, 150, 128, 128),
    (1340, 200, 128, 128),
    (1340, 230, 128, 128),
    (1340, 280, 128, 128),
]

PAN = (1057, 690)


def restart(location):
    time.sleep(5)
    create_order.counter = 0
    create_order.mscounter = 0
    pyautogui.click(1360, 941)
    time.sleep(6)
    pyautogui.click(626, 834)


def carry_it(start, stop):
    pyautogui.moveTo(start[0], start[1], MOUSE_SPEED)
    pyautogui.dragTo(stop[0], stop[1], MOUSE_SPEED, button='left')


def find_order(rgn):
    possibleItems = ['vanilla.png', 'chocolate.png', 'custard.png',
                     'strawberry_vanilla.png', 'coffee.png', 'milk_shake.png', 'coffee.png', 'milk_shake.png']
    restart_button = pyautogui.locateCenterOnScreen(
        'items/served_items/restart.png')
    if restart_button:
        restart(restart_button)
    for item in possibleItems:
        searchFor = 'items/ordered_item/{}'.format(item)
        locateItem = pyautogui.locateCenterOnScreen(
            searchFor, region=rgn, confidence=CONF)
        if locateItem:
            print("Position: {}".format(locateItem))
            itemCenter = create_order(item)
            serve_item(locateItem, itemCenter)
    return


def make_cake(flavor):
    make_cake.counter += 1
    # Mold 953, 917
    frosting = None
    topping = None
    if flavor == 'vanilla':
        frosting = (1240, 623)
    if flavor == 'strawberry_vanilla':
        frosting = (1240, 623)
        topping = (960, 801)
    if flavor == 'chocolate':
        frosting = (1275, 716)
    if flavor == 'peach_chocolate':
        frosting = (1275, 716)
        topping = (831, 814)
    if flavor == 'custard':
        frosting = (1216, 533)
    addMold = pyautogui.click(953, 917)

    # Add Frosting
    carry_it(frosting, PAN)

    # Add Topping
    if topping:
        carry_it(topping, PAN)
    ovenCenter = OVEN_LOCATIONS[make_cake.counter % 4]
    pyautogui.dragTo(ovenCenter[0], ovenCenter[1],
                     MOUSE_SPEED, button='left')
    collect_money()
    time.sleep(4.1)
    return ovenCenter


def create_order(item):
    print("**Creating: {}".format(item))
    if item == 'coffee.png':
        locateItem = COFFEE_LOCATIONS[create_order.counter % 3]
        create_order.counter += 1
        return locateItem
    elif item == 'milk_shake.png':
        locateItem = MS_LOCATIONS[create_order.mscounter % 3]
        if create_order.mscounter % 3 == 0:
            pyautogui.click(626, 834)
        create_order.mscounter += 1
        return locateItem
    elif item == 'vanilla.png':
        return make_cake('vanilla')
    elif item == 'strawberry_vanilla.png':
        return make_cake('strawberry_vanilla')
    elif item == 'chocolate.png':
        return make_cake('chocolate')
    elif item == 'peach_chocolate.png':
        return make_cake('peach_chocolate')
    elif item == 'custard.png':
        return make_cake('custard')
    else:
        print("{} was not found...".format(item))


# Serve Ordered Item
def serve_item(orderCenter, itemCenter):
    print("***Serving: {}".format(itemCenter))
    carry_it(itemCenter, orderCenter)


def collect_money():
    locations = pyautogui.locateCenterOnScreen(
        'items/served_items/money.png', confidence=CONF)
    if locations:
        print("****Collecting Money")
        pyautogui.click(locations)
# Main Control


def main():
    create_order.counter = 0
    create_order.mscounter = 0
    make_cake.counter = 0
    count = 0
    time.sleep(10)
    pyautogui.click(1360, 941)
    while True:
        find_order(ORDER_REGIONS[count % 4])
        # itemCenter = create_order(item)
        # serve_item(orderCenter, itemCenter)
        collect_money()
        count += 1


main()
