from enum import Enum

class CategoryPropertyFormat(str, Enum):
    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    DATE = 'DATE'