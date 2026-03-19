import tkinter as tk
from PIL import Image,ImageTk
import os
import arUcoTracking


class UserInterface:
    def __init__(self,window):
        self.window = window
        self.window.title("User Interface")
        self.window.attributes('-zoomed', True)
        
        self.window.geometry("1280x720")

        self.canvas = tk.Canvas(window,width=1280,height=720)
        self.canvas.pack()

        self.update()

    def update(self):
        frame = arUcoTracking.get_frame()

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        self.canvas.imgtk = imgtk
        self.canvas.create_image(0,0, anchor=tk.NW, image=imgtk)

        self.window.after(10, self.update)

root = tk.Tk()

app = UserInterface(root)

root.mainloop()

arUcoTracking.stop()


# window = tk.Tk()

# height = window.winfo_screenheight()
# width = window.winfo_screenwidth()
# size = f"{width}x{height}"

# window.geometry(size)
# window.state('zoomed')

# def start():
#     print("pressed")

# startup = tk.Button(
#     window,
#     text = "START",
#     width = 30,
#     height = 30,
#     bg = "green",
#     fg = "blue",
#     command=start
# )
# startup.pack()

# password = tk.Entry(fg="yellow", bg="blue", width=50)



# window.mainloop()





