from enum import Enum


class BaseChoice(Enum):
    """ """

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def members(cls):
        return [member.name for member in cls]

    @classmethod
    def choices_dict(cls):
        return [{"name": key.value} for key in cls]
