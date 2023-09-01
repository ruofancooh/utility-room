from pitch import Pitch
from note import Note
from scale import Scale
from mode import Mode


class FreqPrinter:
    @staticmethod
    def print_freq(pitch_name: str) -> None:
        """
        输出一个音名对应的频率
        """
        note = Note(pitch_name)
        pitch_name, pitch_freq = note.get()
        if pitch_freq is not None:
            print(f"{pitch_name} 的频率是 {pitch_freq:.3f}Hz")
        else:
            print("找不到音名，输入 all 以查看所有音名的频率")

    @staticmethod
    def print_all_freq() -> None:
        """
        输出所有音名对应的频率
        """
        notes = []
        for pitch_name in Pitch.ALL_PITCHS:
            notes.append(Note(pitch_name))
        print(notes)
        for note in notes:
            pitch_name, pitch_freq = note.get()
            print(f"{pitch_name:>3} 的频率是 {pitch_freq:.3f}Hz")


class ScalePrinter:
    @staticmethod
    def print_scale(mode: Mode) -> None:
        ...

    @staticmethod
    def print_all_mode_scale() -> None:
        ...
