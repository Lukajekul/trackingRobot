import tkinter as tk
from PIL import Image,ImageTk
import os
import arUcoTracking
import cv2


class UserInterface:
    def __init__(self,window):
        self.window = window
        self.window.title("User Interface")
        self.window.attributes('-zoomed', True)
        
        self.window.geometry("1280x720")

#width=1280,height=720
       # make columns and rows expand to fill the window
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        window.grid_rowconfigure(0, weight=1)

        self.camera = tk.Canvas(window, width=int(window.winfo_screenwidth()/2), height=int(window.winfo_screenheight()/2))
        self.camera.grid(row=0, column=0, sticky="nsew")

        self.radar = tk.Canvas(window, width=int(window.winfo_screenwidth()/2), height=int(window.winfo_screenheight()/2))
        self.radar.grid(row=0, column=1, sticky="nsew")

        self.start = tk.Button(window, text="START", bg="green", fg="blue")
        self.start.grid(row=1, column=0, sticky="nsew")

        self.stop = tk.Button(window, text="STOP", bg="red", fg="blue")
        self.stop.grid(row=1, column=1, sticky="nsew")

        self.lockOn = tk.Button(window, text="Lock onto the target")
        self.lockOn.grid(row=2, column=0, sticky="nsew")

        self.shutDown = tk.Button(window, text="Stur Down")
        self.shutDown.grid(row=2, column=1, sticky="nsew")

        self.update()

    def update(self):
        frame = arUcoTracking.get_frame()

        canvas_w = self.camera.winfo_width()
        canvas_h = self.camera.winfo_height()

        frame = cv2.resize(frame, (canvas_w, canvas_h))

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        self.camera.imgtk = imgtk
        self.camera.create_image(0,0, anchor=tk.NW, image=imgtk)

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





