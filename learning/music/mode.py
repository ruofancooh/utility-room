import my_exceptions as e
from note import Note
from scale import Scale

CHURCH_MODES: dict[str, str] = {
    "Ionian": "Ionian",
    "Dorian": "Dorian",
    "Phrygian": "Phrygian",
    "Lydian": "Lydian",
    "Mixolydian": "Mixolydian",
    "Aeolian": "Aeolian",
    "Iocrian": "Iocrian",
    "Major": "Ionian",
    "Minor": "Aeolian",
}
CHURCH_MODE_SEMITONES: dict[str, tuple[int, ...]] = {
    "Ionian": (2, 2, 1, 2, 2, 2, 1),
    "Dorian": (2, 1, 2, 2, 2, 1, 2),
    "Phrygian": (1, 2, 2, 2, 1, 2, 2),
    "Lydian": (2, 2, 2, 1, 2, 2, 1),
    "Mixolydian": (2, 2, 1, 2, 2, 1, 2),
    "Aeolian": (2, 1, 2, 2, 1, 2, 2),
    "Iocrian": (1, 2, 2, 1, 2, 2, 2),
}


class Mode(Scale):
    """
    调式类
    - `name`：调式名
    - `aliases`：调式别名
    """

    name: str
    aliases: list[str]

    def __init__(self, arg: str | tuple[Note, ...]) -> None:
        """
        arg 传 str 为调式名，传 tuple 为音阶
        """
        if type(arg) is tuple:
            degrees = arg
            super().__init__(degrees)
        elif type(arg) is str:
            mode_name = arg
            self.convert_mode_name(mode_name)
        else:
            raise e.MyException("arg error")

    @staticmethod
    def convert_mode_name(mode_name: str) -> str:
        """
        把调名转换为 CHURCH_MODES 里的调名，不在 CHURCH_MODES 时抛出错误
        """
        mode_name = mode_name.capitalize()
        converted_mode_name = CHURCH_MODES.get(mode_name)
        if converted_mode_name is not None:
            return converted_mode_name
        else:
            raise e.MyException("mode name is not found")
