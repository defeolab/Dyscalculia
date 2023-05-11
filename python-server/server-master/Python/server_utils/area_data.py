# This class defines the parameters needed for each area (the left one or the right one).
# As the Trial class, this class is Unity-compatible: this is why the paraeters
# that compose the Area are the ones of the Unity client, and not the Item Surface
# Area, Field Area and Number.

class AreaData:
    
    def __init__(self, circle_radius, size_of_chicken, average_space_between, number_of_chickens):
        self.circleRadius = circle_radius
        self.sizeOfChicken = size_of_chicken
        self.averageSpaceBetween = average_space_between
        self.numberOfChickens = number_of_chickens