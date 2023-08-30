from printer import FreqPrinter


while True:
    entered_value = input("输入音名：")
    if entered_value == "all":
        FreqPrinter.print_all_freq()
    else:
        FreqPrinter.print_freq(entered_value)
    print()
