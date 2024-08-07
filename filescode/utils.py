from dotenv import load_dotenv
import os
import boto3
from datetime import datetime
from tkinter import messagebox

def save_txt_to_s3(file_name, bucket_name, s3_folder):
    # Cargar variables de entorno
    load_dotenv()
    
    # Obtener credenciales y configuraciones de las variables de entorno
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )
    
    s3_path = f"{s3_folder}/{file_name}"
    
    try:
        # Subir archivo a S3
        s3_client.upload_file(file_name, bucket_name, s3_path)
        print(f"Archivo {file_name} guardado en s3://{bucket_name}/{s3_path}")
        return True, f"Archivo {file_name} guardado en s3://{bucket_name}/{s3_path}"
    except Exception as e:
        print(f"Error al subir el archivo: {e}")
        return False, f"Error al subir el archivo: {e}"

class EventLogger:
    def __init__(self):
        self.bucket_name = 'ftp-data-images'
        self.s3_folder = 'drilloutProyectTxt'
        self.current_date = datetime.now().strftime("%d%m%Y")
        self.file_name = f"{self.current_date}.txt"
        self.check_and_create_file()
        self.upload_and_remove_old_files()

    def check_and_create_file(self):
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w') as file:
                file.write("Camera 1,2024-07-17 09:33:42,Empthy,99.99%\n")
    
    def log_event(self, event):
        new_date = datetime.now().strftime("%d%m%Y")
        if new_date != self.current_date:
            self.upload_and_switch_file()
            self.current_date = new_date
            self.file_name = f"{self.current_date}.txt"
            self.check_and_create_file()
        
        with open(self.file_name, 'a') as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} - {event}\n")
    
    def upload_and_switch_file(self):
        success, message = save_txt_to_s3(self.file_name, self.bucket_name, self.s3_folder)
        if success:
            os.remove(self.file_name)
        else:
            print(message)
            messagebox.showerror("Error", message)

    def upload_and_remove_old_files(self):
        current_date = datetime.now().strftime("%d%m%Y")
        for file_name in os.listdir():
            if file_name.endswith(".txt") and file_name != f"{current_date}.txt":
                success, message = save_txt_to_s3(file_name, self.bucket_name, self.s3_folder)
                if success:
                    os.remove(file_name)
                else:
                    print(message)
                    messagebox.showerror("Error", message)

if __name__ == "__main__":
    logger = EventLogger()
    # Registrar un evento de ejemplo
    logger.log_event("Evento de prueba")
