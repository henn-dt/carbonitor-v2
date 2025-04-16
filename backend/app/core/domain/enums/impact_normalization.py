
from enum import Enum

class ImpactNormalization(str, Enum):
        QUANTITY = "quantity"
        BUILDING_FOOTPRINT = "building_footprint"
        BUILDING_MASS = "building_mass"
        BUILDING_USERS = "building_users"
        FLOORS_ABOVE_GROUND = "floors_above_ground"
        FLOORS_BELOW_GROUND = "floors_below_ground"
        GROSS_FLOOR_AREA = "gross_floor_area"
        HEATED_FLOOR_AREA = "heated_floor_area"