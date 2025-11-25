import tkinter as tk
from tkinter import *
from tkinter import font as tkFont
import sys

class ConsoleRedirector:
        def __init__(self, widget):
            self.widget = widget

        def write(self, text):
            self.widget.insert(tk.END, text)
            self.widget.see(tk.END)
            

def Calc_Open():
    
    def compute():
        cost = 8.8156
        pow = int(power_entry.get())
        time = int(time_entry.get())
        t_cost = cost*(pow*(time/60))
        print("₱",t_cost)
        
    Calc_App = Tk()
    root.destroy()
    Calc_App.geometry("480x720")
    Calc_App.title("Energy Cost Calculator")
    Calc_App.config(background="#2f373e")
    
    Instruct = Label(Calc_App,text = "Enter Desired Values",
              font=('Retro Gaming',15),
              fg='#72C24C',
              bg='#2f373e')
    Instruct.pack(pady=40)
    
    power_entry = Entry(Calc_App,font=('Retro Gaming',15))
    power_entry.pack(pady=15)
    power = Label(Calc_App,text = "Power (Kw)",
              font=('Retro Gaming',15),
              fg='#5FCCFA',
              bg='#2f373e')
    power.pack()
    time_entry = Entry(Calc_App,font=('Retro Gaming',15))
    time_entry.pack(pady=15)
    time = Label(Calc_App,text = "Time (Minutes)",
              font=('Retro Gaming',15),
              fg='#5FCCFA',
              bg='#2f373e')
    time.pack()
    
    Calculate = Button(Calc_App,text="-> Calculate <-",
                        command=compute,
                        font=('Retro Gaming',15),
                        fg='#FCDEFF',
                        bg='#2f373e',
                        activebackground='#2f373e',
                         activeforeground='#FCDEFF',
                        relief=FLAT)
    Calculate.pack(pady=30)
    
    title = Label(Calc_App,text = "---Output---",
              font=('Retro Gaming',15),
              fg='#72C24C',
              bg='#2f373e',
              pady=15)
    title.pack()
    
    output_text = Text(Calc_App,
                          wrap="word",
                          width=10,
                          height=1.5,
                          font=('Retro Gaming',15),
                          relief=RIDGE)
    output_text.pack(pady=20)
    sys.stdout = ConsoleRedirector(output_text)

    
root = Tk()
root.geometry("480x720")
root.title("Energy Cost Calculator")

logo = PhotoImage(file='efficiency.png')
icon = PhotoImage(file='logo.png')
root.iconphoto(True,icon)
root.config(background="#2f373e")

title = Label(root,text = "Energy Cost Calculator",
              font=('Retro Gaming',15),
              fg='#72C24C',
              bg='#2f373e',
              image=logo,
              compound='top',
              pady=15)
title.pack()

Start_Game = Button(root,text="> Start Game <",
                     font=('Retro Gaming',15),
                     fg='#FCDEFF',
                     bg='#2f373e',
                     activebackground='#2f373e',
                     activeforeground='#FCDEFF',
                     relief=FLAT)
Start_Game.pack()
Calc_Init = Button(root,text="> Use Calculator <",
                    command=Calc_Open,
                    font=('Retro Gaming',15),
                    fg='#5FCCFA',
                    bg='#2f373e',
                    activebackground='#2f373e',
                    activeforeground='#5FCCFA',
                    relief=FLAT)
Calc_Init.pack()

root.mainloop()