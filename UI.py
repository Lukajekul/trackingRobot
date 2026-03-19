import tkinter as tk

window = tk.Tk()

height = window.winfo_screenheight()
width = window.winfo_screenwidth()
size = f"{width}x{height}"

window.geometry(size)
window.state('zoomed')

def start():
    print("pressed")

startup = tk.Button(
    window,
    text = "START",
    width = 30,
    height = 30,
    bg = "green",
    fg = "blue",
    command=start
)
startup.pack()

password = tk.Entry(fg="yellow", bg="blue", width=50)



window.mainloop()
