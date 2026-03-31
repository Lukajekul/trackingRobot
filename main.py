import tkinter as tk
from PIL import Image,ImageTk
import os
import arUcoTracking
import cv2


class UserInterface:
    def __init__(self,window):
        self.window = window
        self.window.title("User Interface")
        
        

        self.tracking=False
        self.correctTargetAttack=False
        
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=0)
        self.window.grid_rowconfigure(2, weight=0) 

        self.camera = tk.Canvas(window)
        self.camera.grid(row=0, column=0, sticky="nsew")

        self.radar = tk.Canvas(window)
        self.radar.grid(row=0, column=1, sticky="nsew")

        self.startBtn = tk.Button(window, text="START", bg="green", fg="blue", command=self.start)
        self.startBtn.grid(row=1, column=0, sticky="nsew")

        self.stopBtn = tk.Button(window, text="STOP", bg="red", fg="blue", command=self.stop)
        self.stopBtn.grid(row=1, column=1, sticky="nsew")

        self.lockOn = tk.Button(window, text="Lock onto the target", command=self.correctTarget)
        self.lockOn.grid(row=2, column=0, sticky="nsew")

        self.shutDown = tk.Button(window, text="Stur Down", command=self.close)
        self.shutDown.grid(row=2, column=1, sticky="nsew")
    
        self.window.update_idletasks()

        self.window.attributes('-fullscreen', True)

        self.update()


    def getButtonClickCordinates():
        pass

    def start(self):
        self.tracking=True

    def stop(self):
        self.tracking=False

    def correctTarget(self):
        self.correctTargetAttack=True

    def close(self):
        closeWindow = tk.Toplevel(self.window)
        closeWindow.geometry("250x150")
        closeWindow.title("Shutting down")

        tk.Label(closeWindow, text="Are you sure you want \nto shut down the program").pack(pady=20)
        
        buttonFrame = tk.Frame(closeWindow)
        buttonFrame.pack()

        tk.Button(buttonFrame, text="YES", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        tk.Button(buttonFrame, text="NO", command=closeWindow.destroy).pack(side=tk.LEFT, padx=5)



    def update(self):
        frame = arUcoTracking.get_frame(self.tracking)

        canvas_w = self.camera.winfo_width()
        canvas_h = self.camera.winfo_height()

        if canvas_w < 50 or canvas_h < 50:
            canvas_w, canvas_h = 800, 600

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