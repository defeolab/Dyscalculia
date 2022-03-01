# This class defines the parameters needed for each area (the leaft one or the right one).
# So, basically, for each area, we define the Number of Chickens, the Field Area and the
# Item Surface Area parameters.

class AreaData:
    
    def __init__(self, circle_radius, size_of_chicken, average_space_between, number_of_chickens):
        self.circleRadius = circle_radius
        self.sizeOfChicken = size_of_chicken
        self.averageSpaceBetween = average_space_between
        self.numberOfChickens = number_of_chickens