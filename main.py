import tkinter as tk
from PIL import Image,ImageTk
import os
import arUcoTracking
import cv2
import threading
import time
import json
import serial


class UserInterface:
    def __init__(self,window):
        self.window = window
        self.window.title("User Interface")
        
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
            time.sleep(2)
            print("Serial connection!")
        except Exception as e:
            print(f"Serial Error: {e}")
            self.ser = None


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

        self.lock = threading.Lock()
        self.currentX = 0
        self.currentY = 0

        motorThread = threading.Thread(target=self.motorLoop, daemon=True)
        motorThread.start()

        self.latestFrame = None
        self.frameLock = threading.Lock()

        cameraThreading = threading.Thread(target=self.cameraLoop, daemon=True)
        cameraThreading.start()
        
        self.window.after(10, self.update)

    def getButtonClickCordinates():
        pass

    def start(self):
        self.tracking=True

    def stop(self):
        self.tracking=False

    def correctTarget(self):
        if self.correctTargetAttack:
            self.correctTargetAttack = False
            self.lockOn.configure(text="Lock onto the target")
            return

        targetWindow = tk.Toplevel(self.window)
        targetWindow.geometry("300x200")
        targetWindow.title("Activate Laser")

        tk.Label(targetWindow, text="Key 1:").grid(row=0, column= 0, pady=5, padx=5)
        key1 = tk.Entry(targetWindow)
        key1.grid(row=0, column=1)
        tk.Label(targetWindow, text="Key 2:").grid(row=1, column= 0, pady=5, padx=5)
        key2 = tk.Entry(targetWindow)
        key2.grid(row=1, column=1)

        tk.Label(targetWindow, text="Key 3:").grid(row=2, column= 0, pady=5, padx=5)
        key3 = tk.Entry(targetWindow)
        key3.grid(row=2, column=1)

        def testKeys():
            if  key1.get() == "admin" and key2.get() == "1234" and key3.get() == "Fire":
                self.correctTargetAttack = True
                self.lockOn.configure(text="Target destrojed")
                targetWindow.destroy()
            else:
                wrongWindow = tk.Toplevel(targetWindow)
                wrongWindow.geometry("200x100")
                wrongWindow.title("Wrong entry")
                tk.Label(wrongWindow, text="Inccorect Keys!").pack(pady=10)
                tk.Button(wrongWindow, text="OK", command=wrongWindow.destroy).pack()

        buttonFrame = tk.Frame(targetWindow)
        buttonFrame.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(buttonFrame, text="ACTIVATE", command=testKeys, bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(buttonFrame, text="CANCEL", command=targetWindow.destroy).pack(side=tk.LEFT, padx=5)

    def send(self, payload):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write((payload + '\n').encode())
            except Exception as e:
                print(f"Send failed: {e}")

    def close(self):
        closeWindow = tk.Toplevel(self.window)
        closeWindow.geometry("250x150")
        closeWindow.title("Shutting down")

        tk.Label(closeWindow, text="Are you sure you want \nto shut down the program").pack(pady=20)
        
        buttonFrame = tk.Frame(closeWindow)
        buttonFrame.pack()

        tk.Button(buttonFrame, text="YES", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        tk.Button(buttonFrame, text="NO", command=closeWindow.destroy).pack(side=tk.LEFT, padx=5)



    def cameraLoop(self):
        while True:
            frame, x, y = arUcoTracking.get_frame(self.tracking)
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                with self.frameLock:
                    self.latestFrame = frame
            with self.lock:
                if x is not None and y is not None:
                    self.currentX = x
                    self.currentY = y
            
            time.sleep(0.01)

    def update(self):
        with self.frameLock:
            frame = self.latestFrame

        if frame is not None:
            canvas_w = self.camera.winfo_width()
            canvas_h = self.camera.winfo_height()

            if canvas_w < 50 or canvas_h < 50:
                canvas_w, canvas_h = 800, 600

            frame = cv2.resize(frame, (canvas_w, canvas_h))

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.camera.imgtk = imgtk
            self.camera.delete("all")
            self.camera.create_image(0,0, anchor=tk.NW, image=imgtk)

        self.window.after(30, self.update)

    def motorLoop(self):

        while True:
            with self.lock:
                x = self.currentX
                y = self.currentY

            if self.correctTargetAttack:
                data = {
                    "active" : self.tracking,
                    "x" : x,
                    "y" : y,
                    "laser": True
                }
            else:
                data = {
                    "active" : self.tracking,
                    "x" : x,
                    "y" : y,
                    "laser": False
                }


            self.send(json.dumps(data))

            # if self.ser and self.ser.in_waiting > 0:
            #     try:
            #         response = self.ser.readline().decode('utf-8').strip()
            #         if response:
            #             print(f"ESP32 says: {response}")
            #     except Exception as e:
            #         print(f"Read error: {e}")

            



            time.sleep(0.05)
    




root = tk.Tk()
app = UserInterface(root)
root.mainloop()
arUcoTracking.stop()