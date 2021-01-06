import pyautogui as p


class Cake:
    def __init__(self, flavor, location, oven):
        self.frosting = None
        self.topping = None
        self.flavor = flavor
        self.delivery_location = location
        self.oven_location = oven
        self.countdown = 21

    def update(self, val):
        self.countdown -= val

    def set_topping(self):
        if self.flavor == 'vanilla':
            self.frosting = (1240, 623)
        if self.flavor == 'strawberry_vanilla':
            self.frosting = (1240, 623)
            self.topping = (960, 801)
        if self.flavor == 'chocolate':
            self.frosting = (1275, 716)
        if self.flavor == 'peach_chocolate':
            self.frosting = (1275, 716)
            self.topping = (831, 814)
        if self.flavor == 'custard':
            self.frosting = (1216, 533)

    def make_cake(self):

        addMold = p.click(953, 917)

        # Add Frosting
        serve_item(frosting, PAN_LOCATIONS)

        # Add self.topping
        if self.topping:
            serve_item(self.topping, PAN_LOCATIONS)
        ovenCenter = OVEN_LOCATIONS[make_cake.counter % 4]
        p.dragTo(ovenCenter[0], ovenCenter[1],
                 MOUSE_SPEED, button='left')
        collect_money()
        time.sleep(4.1)
        return ovenCenter
