from my_constants import PIANOKEY_FREQ


class FreqPrinter:
    @staticmethod
    def print_freq(pitch_name: str) -> None:
        """
        输出一个音名对应的频率
        """
        f_pitch_name = PIANOKEY_FREQ.get(pitch_name)
        if f_pitch_name is not None:
            print(f"{pitch_name} 的频率是 {f_pitch_name:.3f}Hz")
        else:
            print("找不到音名，输入 all 以查看所有音名的频率")

    @staticmethod
    def print_all_freq() -> None:
        """
        输出所有音名对应的频率
        """
        for pitch_name, freq in PIANOKEY_FREQ.items():
            print(f"{pitch_name:>3} 的频率是 {freq:.3f}Hz")
