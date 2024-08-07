# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:20:33 2024
@author: tomas
"""

import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from datetime import datetime
import os
from filescode.utils import save_txt_to_s3

class Configurations:
    def __init__(self, parent):
        self.status_var = tk.StringVar(parent, value="rig up")  # Default state
        self.status_var.trace("w", self.status_changed)  # Trace changes

    def create_status_menu(self, parent, controller):
        status_frame = tk.Frame(parent)
        status_frame.pack(pady=10)

        status_label = tk.Label(status_frame, text="Operation State:")
        status_label.pack(side="left")

        status_menu = tk.OptionMenu(status_frame, self.status_var, "rig up", "operative", "rig down")
        status_menu.pack(side="left")

    def status_changed(self, *args):
        print(f"Status changed to: {self.status_var.get()}")

class ConfigurationScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Configuration Screen", font=("Arial", 18))
        label.pack(side="top", pady=10)

        # Create status menu in the configuration screen
        controller.configurations.create_status_menu(self, controller)

        # Button to simulate the test
        test_button = tk.Button(self, text="Test Conection", command=self.simulate_test)
        test_button.pack(pady=10)

        # Button to simulate the test
        test_button = tk.Button(self, text="Test Cameras", command=self.simulate_test)
        test_button.pack(pady=10)

        # Button to return to the main screen
        button = tk.Button(self, text="Back to Cameras", command=lambda: controller.show_frame("CameraScreen"))
        button.pack(pady=10)

    def simulate_test(self):
        # Nombre del archivo que deseas subir
        file_name = datetime.now().strftime("%d%m%Y") + '.txt'
    
        # Nombre del bucket en S3
        bucket_name = 'ftp-data-images'
    
        # Carpeta dentro del bucket de S3
        s3_folder = 'drilloutProyectTxt'
    
        # Llamar a la función para subir el archivo
        success, message = save_txt_to_s3(file_name, bucket_name, s3_folder)
        
        # Mostrar un popup con el estado de la operación
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

# Resto del código para inicializar y mostrar la ventana principal...
if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    controller = tk.Tk()  # Esta es una implementación simple, debes modificarla según tu controlador actual
    controller.configurations = Configurations(controller)
    frame = ConfigurationScreen(root, controller)
    frame.pack(fill="both", expand=True)
    root.mainloop()
