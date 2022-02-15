# This class defines the parameters needed for each area (the leaft one or the right one).
# So, basically, for each area, we define the Number of Chickens, the Field Area and the
# Item Surface Area parameters.

class AreaData:
    
    def __init__(self, number_of_chickens, field_area, item_surface_area):
        self.numberOfChickens = number_of_chickens
        self.fieldArea = field_area
        self.itemSurfaceArea = item_surface_area