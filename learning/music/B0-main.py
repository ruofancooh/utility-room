from mode import Mode

while True:
    entered_value = input("输入调名，比如 C Major 或者 D# Dorian：\n")
    mode = Mode(entered_value)
