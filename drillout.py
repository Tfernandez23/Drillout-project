import os
import tkinter as tk
from PIL import Image, ImageTk
from filescode.cameras import CameraScreen
from filescode.logs import LogScreen
from filescode.configurations import Configurations, ConfigurationScreen
from filescode.utils import EventLogger

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Camera Application")
        self.geometry("1550x800")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.configurations = Configurations(self)

        self.frames = {}
        for F in (CameraScreen, LogScreen, ConfigurationScreen):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.config_button = tk.Button(self.container, text="Configurations", command=lambda: self.show_frame("ConfigurationScreen"))
        self.config_button.grid(row=2, column=0, columnspan=2, sticky="se", padx=10, pady=10)

        self.show_frame("CameraScreen")

        try:
            original_image = Image.open('Emergent-2.png')
            resized_image = original_image.resize((150, 50), Image.LANCZOS)
            self.emergent_image = ImageTk.PhotoImage(resized_image)
        except FileNotFoundError:
            print("Error: No se pudo encontrar el archivo Emergent2.png.")
        except Exception as e:
            print(f"Error al cargar y redimensionar la imagen: {e}")

        self.emergent_label = tk.Label(self.container, image=self.emergent_image)
        self.emergent_label.grid(row=2, column=0, sticky="sw", padx=10, pady=10)

        self.event_logger = EventLogger()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name == "ConfigurationScreen":
            self.config_button.grid_remove()
        elif page_name == "LogScreen":
            self.config_button.grid_remove()
        else:
            self.config_button.grid()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
