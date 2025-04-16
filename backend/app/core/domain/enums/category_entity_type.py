
from enum import Enum


class CategoryEntityType(str, Enum):
    Product = "Product"
    Buildup = "Buildup"
    Model = "Model"
    Project = "Project"
    Other = "Other"