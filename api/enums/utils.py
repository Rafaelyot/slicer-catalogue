from enum import Enum, EnumMeta as BaseEnumMeta


class EnumMeta(BaseEnumMeta):
    def __iter__(self):
        return (name for name in self._member_names_)


class AutoName(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    @classmethod
    def get_values(cls):
        return tuple([e.value for e in cls])
