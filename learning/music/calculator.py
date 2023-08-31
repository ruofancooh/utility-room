from my_constants import (
    FREQ_A4,
    OCTAVE_KEYS,
    OCTAVE_KEYS_NUM,
    PIANO_KEYS,
    PIANO_KEYS_NUM,
)
import my_exceptions as e


def sharp(pitch_name: str, semitones: int = 1) -> str:
    """
    - 把一个在 OCTAVE_KEYS 或者 PIANO_KEYS 里的音升高或降低若干个半音数，semitones 为正时升高
    - 返回新的音名，不在 PIANO_KEYS 里时抛出错误
    """
    if pitch_name[-1].isdigit():
        original_index = PIANO_KEYS.index(pitch_name)
        changed_index = original_index + semitones
        if changed_index in range(PIANO_KEYS_NUM):
            ret = PIANO_KEYS[changed_index]
        else:
            raise e.MyException("pitch_name is not in PIANO_KEYS")
    else:
        original_index = OCTAVE_KEYS.index(pitch_name)
        changed_index = original_index + semitones
        changed_index %= OCTAVE_KEYS_NUM
        ret = OCTAVE_KEYS[changed_index]
    return ret


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


def calc_mode_scale(tonic_name: str, mode_name: str) -> tuple[str, ...]:
    """
    计算并返回某一种调式的音阶
    """
    ...