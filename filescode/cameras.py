import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import threading
from .models import ModelPredictor  # Asegúrate de que esta importación sea correcta
import time

class CameraScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Live Video", font=("Helvetica", 24)).grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.video_label1 = tk.Label(self)
        self.video_label1.grid(row=1, column=0, padx=10, pady=10)

        self.video_label2 = tk.Label(self)
        self.video_label2.grid(row=1, column=1, padx=10, pady=10)

        video_live1 = 'rtsp://admin:csdUzHir14$@192.168.1.100:554/Streaming/Channels/102'
        video_live2 = 'rtsp://admin:csdUzHir14$@192.168.1.101:554/Streaming/Channels/102'

        #self.cap1 = cv2.VideoCapture(video_live1)
        #self.cap2 = cv2.VideoCapture(video_live2)

        self.cap1 = cv2.VideoCapture(0)
        self.cap2 = cv2.VideoCapture(0)

        self.model_predictor1 = ModelPredictor('drillout_model.h5')
        self.model_predictor2 = ModelPredictor('drillout_model_2.h5')

        self.current_frame1 = None
        self.current_frame2 = None

        self.prediction_thread = threading.Thread(target=self.run_predictions)
        self.prediction_thread.start()

        self.switch_button = tk.Button(self, text="View Logs", command=lambda: self.controller.show_frame("LogScreen"))
        self.switch_button.grid(row=4, column=0, columnspan=2, pady=20)

        self.update_video_stream()

    def update_video_stream(self):
        ret1, frame1 = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        if ret1:
            frame1 = cv2.resize(frame1, (740, 580))
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            image1 = Image.fromarray(frame1)
            image1 = ImageTk.PhotoImage(image1)
            self.video_label1.config(image=image1)
            self.video_label1.image = image1
            self.current_frame1 = frame1

        if ret2:
            frame2 = cv2.resize(frame2, (740, 580))
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            image2 = Image.fromarray(frame2)
            image2 = ImageTk.PhotoImage(image2)
            self.video_label2.config(image=image2)
            self.video_label2.image = image2
            self.current_frame2 = frame2

        self.after(10, self.update_video_stream)

    def run_predictions(self):
        def prediction_loop():
            while True:
                status = self.controller.configurations.status_var.get()
                print(f"Estado actual: {status}")
                if status == "operative":
                    if self.current_frame1 is not None:
                        label1, conf1 = self.model_predictor1.predict(self.current_frame1, "Camera 1")
                        print(f"Predicción para cámara 1: {label1} - Confianza: {conf1}")

                    if self.current_frame2 is not None:
                        label2, conf2 = self.model_predictor2.predict(self.current_frame2, "Camera 2")
                        print(f"Predicción para cámara 2: {label2} - Confianza: {conf2}")
                else:
                    print("No se realizan predicciones en estado:", status)

                time.sleep(20)

        thread = threading.Thread(target=prediction_loop)
        thread.daemon = True
        thread.start()

    def __del__(self):
        if self.cap1.isOpened():
            self.cap1.release()
        if self.cap2.isOpened():
            self.cap2.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraScreen(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
