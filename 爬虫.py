import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.constants import END

a = requests.get('https://www.baidu.com/')
a.encoding = 'utf-8'
html = a.text

soup = BeautifulSoup(html, 'html.parser')

output = soup.title.string

tk.Tk()

text = ScrolledText()
text.grid(row=0, column=0)
text.insert(END, output)
tk.mainloop()