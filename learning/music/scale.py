from note import Note
from pitch import Pitch
import my_exceptions as e


class Scale:
    """
    音阶类
    - `degrees_num`：音级数量
    - `degrees`：各音级
    """

    degrees_num: int
    degrees: tuple[Note, ...]

    def __init__(self, degrees: tuple) -> None:
        self.degrees = degrees
        self.degrees_num = len(self.degrees)
