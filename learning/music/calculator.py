import re

from code_tester import t
from my_constants import (
    FREQ_A4,
    NUM_OCTAVE_KEYS,
    NUM_PIANO_KEYS,
    OCTAVE_KEYS,
    PIANO_KEYS,
)


def sharp(pitch_name: str, semitones: int = 1) -> str:
    """
    - 把一个在 OCTAVE_KEYS 或者 PIANO_KEYS 里的音升高或降低若干个半音数，semitones 为正时升高
    - 返回新的音名，不在 OCTAVE_KEYS 和 PIANO_KEYS 里时返回空字符串
    """
    if pitch_name[-1].isdigit():
        original_index = PIANO_KEYS.index(pitch_name)
        changed_index = original_index + semitones
        ret = (
            PIANO_KEYS[changed_index] if changed_index in range(NUM_PIANO_KEYS) else ""
        )
    else:
        original_index = OCTAVE_KEYS.index(pitch_name)
        changed_index = original_index + semitones
        changed_index %= NUM_OCTAVE_KEYS
        ret = OCTAVE_KEYS[changed_index]
    return ret


def convert_pitch_name(pitch_name: str) -> str:
    """
    - 把形如 `c` `#C` `##B` `ebbb` `bD` `Db` `bd` `db`的音名转换为 OCTAVE_KEYS 里的音名 "C#"
    - 把形如 `c4` `#C4` `##B3` `ebbb4` `bD4` `Db4` `bd4` `db4`的音名转换为 PIANO_KEYS 里的音名 "C#4"
    """

    PITCH_WITHOUT_NUM = "[#b]*[A-Ga-g][#b]*"
    PITCH_WITH_NUM = "[#b]*([A-Ga-g][1-7]?|[ABab]0?|[Cc]8?)[#b]*"

    pattern = f"^({PITCH_WITHOUT_NUM}|{PITCH_WITH_NUM})$"
    pattern = re.compile(pattern)

    num_of_found = len(pattern.findall(pitch_name))
    if num_of_found == 0:
        ret = ""
    elif num_of_found == 1:
        # 按升降号的个数计算升降次数
        num_of_sharps = pitch_name.count("#") - pitch_name.count("b")
        # 移除所有升降号并转换为大写
        pitch_name = re.sub("[#b]", "", pitch_name).upper()
        # 升降音
        ret = sharp(pitch_name, num_of_sharps)
    return ret


t(convert_pitch_name)


def calc_semitones(pitch_name1: str, pitch_name2: str) -> int:
    """
    计算 pitch_name2 与 pitch_name1 相隔的半音数，pitch_name2 频率高时返回正数
    """
    semitones = PIANO_KEYS.index(pitch_name2) - PIANO_KEYS.index(pitch_name1)
    return semitones


def calc_freq(pitch_name: str) -> float:
    """
    计算音名的频率，音名需要已经在88键钢琴内，返回频率
    """
    # 计算相隔的半音数
    semitones = calc_semitones("A4", pitch_name)
    # 计算频率
    f_pitch_name = FREQ_A4 * 2 ** (semitones / 12)
    return f_pitch_name
