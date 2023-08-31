from converter import convert_mode_name, convert_pitch_name
import my_exceptions as e


while True:
    entered_value = input("输入调名，比如 C Major 或者 D# Dorian：\n")
    tonic_name: str
    mode_name: str
    try:
        tonic_name, mode_name = entered_value.split()
    except ValueError:
        raise e.MyException("input format error")
    else:
        tonic_name = convert_pitch_name(tonic_name)
        mode_name = convert_mode_name(mode_name)
        print(tonic_name, mode_name)
