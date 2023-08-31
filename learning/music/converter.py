import re

from code_tester import t
from calculator import sharp
from my_constants import (
    CHURCH_MODES,
)
import my_exceptions as e


def convert_pitch_name(pitch_name: str) -> str:
    """
    - 把形如 `#C` `#c` `##B` `ebbb` `bD` `Db` `bd` `db` 的音名转换为 OCTAVE_KEYS 里的音名 "C#"
    - 把形如 `#C4` `#c4` `##B3` `ebbb4` `bD4` `Db4` `bd4` `db4` 的音名转换为 PIANO_KEYS 里的音名 "C#4"
    - 其中音名 B 必须大写，为了和降号区分
    - 返回转换后的音名，找不到时返回 None
    """

    PITCH_WITHOUT_DIGIT = "[#b]*[A-Ga-g][#b]*"
    PITCH_WITH_DIGIT = "[#b]*([A-Ga-g][1-7]?|[ABab]0?|[Cc]8?)[#b]*"

    PATTERN_STR = f"^({PITCH_WITHOUT_DIGIT}|{PITCH_WITH_DIGIT})$"
    PATTERN = re.compile(PATTERN_STR)

    num_of_found = len(PATTERN.findall(pitch_name))
    if num_of_found == 0:
        raise e.MyException("pitch name is not found")
    elif num_of_found == 1:
        # 按升降号的个数计算升降次数
        num_of_sharps = pitch_name.count("#") - pitch_name.count("b")
        # 移除所有升降号并转换为大写
        pitch_name = re.sub("[#b]", "", pitch_name).upper()
        # 升降音
        return sharp(pitch_name, num_of_sharps)
    else:
        raise e.MyException("pitch name is not found")


def convert_mode_name(mode_name: str) -> str:
    """
    把调名转换为 CHURCH_MODES 里的调名，不在 CHURCH_MODES 时抛出错误
    """
    mode_name = mode_name.capitalize()
    converted_mode_name = CHURCH_MODES.get(mode_name)
    if converted_mode_name is None:
        raise e.MyException("mode name is not found")
    else:
        return converted_mode_name
