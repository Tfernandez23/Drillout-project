import tkinter as tk
from PIL import Image, ImageTk
import cv2
import threading
import time

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Camera Application")
        self.geometry("1350x700")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.frames["CameraScreen"] = CameraScreen(parent=self.container, controller=self)
        self.frames["CameraScreen"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("CameraScreen")

        try:
            original_image = Image.open('Emergent-2.png')
            resized_image = original_image.resize((150, 50), Image.LANCZOS)
            self.emergent_image = ImageTk.PhotoImage(resized_image)
        except FileNotFoundError:
            print("Error: No se pudo encontrar el archivo Emergent-2.png.")
        except Exception as e:
            print(f"Error al cargar y redimensionar la imagen: {e}")

        self.emergent_label = tk.Label(self.container, image=self.emergent_image)
        self.emergent_label.grid(row=2, column=0, sticky="sw", padx=10, pady=10)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

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

        self.cap1 = cv2.VideoCapture(0)
        self.cap2 = cv2.VideoCapture(0)

        self.current_frame1 = None
        self.current_frame2 = None

        self.prediction_thread = threading.Thread(target=self.run_predictions)
        self.prediction_thread.start()

        self.update_video_stream()

    def update_video_stream(self):
        ret1, frame1 = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        if ret1:
            frame1 = cv2.resize(frame1, (640, 480))
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            image1 = Image.fromarray(frame1)
            image1 = ImageTk.PhotoImage(image1)
            self.video_label1.config(image=image1)
            self.video_label1.image = image1
            self.current_frame1 = frame1

        if ret2:
            frame2 = cv2.resize(frame2, (640, 480))
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
                if self.current_frame1 is not None:
                    # Simule predicciones para la cámara 1
                    print("Predicción para cámara 1")

                if self.current_frame2 is not None:
                    # Simule predicciones para la cámara 2
                    print("Predicción para cámara 2")

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
    app = MyApp()
    app.mainloop()
