"""Legacy Cake helper module.

This module is not used directly by the main bot but is kept for reference.
"""

import pyautogui


class Cake:
    """Simplified representation of a cake.

    The logic here is incomplete and retained for historical purposes.
    """

    def __init__(self, flavor, delivery_location, oven_location):
        self.frosting = None
        self.topping = None
        self.flavor = flavor
        self.delivery_location = delivery_location
        self.oven_location = oven_location
        self.countdown = 21

    def update(self, elapsed):
        """Reduce the baking countdown."""
        self.countdown -= elapsed

    def set_topping(self):
        """Set frosting and topping coordinates based on flavor."""
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
        """Placeholder for cake-making logic."""
        pyautogui.click(953, 917)
        # The real implementation would interact with serve_item and other helpers.
