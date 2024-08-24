from enum import Enum as PyEnum

def extend_enum(inherited_enums: list):
    def wrapper(added_enum):
        joined = {}
        for inherited_enum in inherited_enums:
            for item in inherited_enum:
                joined[item.name] = item.value
            for item in added_enum:
                joined[item.name] = item.value
        return PyEnum(added_enum.__name__, joined)
    return wrapper