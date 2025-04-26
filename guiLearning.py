from tkinter import *
from tkinter import ttk

lst = ['a', 'b', 'c', 'd', 'e']

def shiftList():
    lst = lst[1:] + lst[:1]

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
root.Button(frm, text='Shift', command=shiftList).grid(row=0, column=0)
t = Text(root)
for i in lst:
    t.insert(END, i + '\n')
t.pack()
root.mainloop()