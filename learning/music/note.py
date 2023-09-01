import re

import my_exceptions as e
from pitch import Pitch


class Note:
    """
    音符类
    - `pitch_name`：音名
    - `pitch_freq`：频率
    """

    pitch_name: str
    pitch_freq: float | None

    def __init__(self, pitch_name: str) -> None:
        self.pitch_name = pitch_name
        self.convert_pitch_name()
        print(self.pitch_name)
        self.pitch_freq = Note.calc_freq(self.pitch_name)

    @staticmethod
    def calc_semitones(pitch_name1: str, pitch_name2: str) -> int:
        """
        计算 pitch_name2 与 pitch_name1 相隔的半音数，pitch_name2 频率高时返回正数
        """
        semitones = Pitch.ALL_PITCHS.index(pitch_name2) - Pitch.ALL_PITCHS.index(pitch_name1)
        return semitones

    @staticmethod
    def calc_freq(pitch_name: str) -> float | None:
        """
        - 计算并返回 Pitch.ALL_PITCHS 里音名的频率
        - 如果是 Pitch.OCTAVE_PITCHS 里的音名，返回 None
        """
        if len(pitch_name) == 1:
            f_pitch_name = None
        else:
            # 计算相隔的半音数
            semitones = Note.calc_semitones("A4", pitch_name)
            # 计算频率
            f_pitch_name = Pitch.FREQ_A4 * 2 ** (semitones / 12)
        return f_pitch_name

    def get(self) -> tuple[str, float | None]:
        return (self.pitch_name, self.pitch_freq)

    def sharp(self, semitones: int = 1) -> None:
        """
        - 把 pitch_name 升高或降低若干个半音数，semitones 为正时升高
        - 结果不在 Pitch.ALL_PITCHS 里时抛出错误
        """
        if self.pitch_name[-1].isdigit():
            original_index = Pitch.ALL_PITCHS.index(self.pitch_name)
            changed_index = original_index + semitones
            if changed_index in range(Pitch.ALL_PITCHS_NUM):
                self.pitch_name = Pitch.ALL_PITCHS[changed_index]
            else:
                raise e.MyException("pitch_name is not in Pitch.ALL_PITCHS")
        else:
            original_index = Pitch.OCTAVE_PITCHS.index(self.pitch_name)
            changed_index = original_index + semitones
            changed_index %= Pitch.OCTAVE_PITCHS_NUM
            self.pitch_name = Pitch.OCTAVE_PITCHS[changed_index]

    def convert_pitch_name(self) -> None:
        """
        - 把形如 `#C` `#c` `##B` `ebbb` `bD` `Db` `bd` `db` 的音名转换为 Pitch.OCTAVE_PITCHS 里的音名 "C#"
        - 把形如 `#C4` `#c4` `##B3` `ebbb4` `bD4` `Db4` `bd4` `db4` 的音名转换为 Pitch.ALL_PITCHS 里的音名 "C#4"
        - 其中音名 B 必须大写，为了和降号区分
        - 找不到时抛出错误
        """

        PATTERN_STR = "^[#b]*([A-Ga-g][#b]*[1-7]?|[ABab][#b]*0?|[Cc][#b]*8?)$"
        PATTERN = re.compile(PATTERN_STR)
        num_of_found = len(PATTERN.findall(self.pitch_name))
        if num_of_found == 1:
            # 按升降号的个数计算升降次数
            num_of_sharps = self.pitch_name.count("#") - self.pitch_name.count("b")
            # 移除所有升降号并转换为大写
            self.pitch_name = re.sub("[#b]", "", self.pitch_name).upper()
            # 升降音
            return self.sharp(num_of_sharps)
        else:
            raise e.MyException("pitch name is not found")
