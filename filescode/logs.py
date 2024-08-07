import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime

class LogScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.current_page = 0
        self.logs_per_page = 20
        self.filtered_logs = []
        self.image_references = {}  # To keep references of image objects

        self.create_widgets()
        self.load_icons()
        self.create_status_bars()

        # Initialize with today's logs
        today = datetime.now().strftime("%d%m%Y")
        self.fake_logs = self.read_logs_from_file(f"{today}.txt")
        self.filtered_logs = self.fake_logs
        self.display_logs()

    def create_widgets(self):
        columns = ('camera', 'date', 'colour')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('camera', text='Camera')
        self.tree.heading('date', text='Date and Time')
        self.tree.heading('colour', text='Color')

        self.tree.grid(row=1, column=0, sticky='nsew', columnspan=3)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.filter_vars = {col: tk.StringVar() for col in columns}
        self.filter_vars['camera'].set('All')
        self.filter_vars['colour'].set('All')

        filter_frame = tk.Frame(self)
        filter_frame.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        tk.Label(filter_frame, text="Camera:").grid(row=0, column=0, padx=5, pady=5)
        self.camera_menu = tk.OptionMenu(filter_frame, self.filter_vars['camera'], 'All')
        self.camera_menu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="Date:").grid(row=0, column=2, padx=5, pady=5)
        self.date_entry = DateEntry(filter_frame, textvariable=self.filter_vars['date'], date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)
        self.date_entry.bind('<<DateEntrySelected>>', self.apply_filters)

        tk.Label(filter_frame, text="Color:").grid(row=0, column=4, padx=5, pady=5)
        self.colour_menu = tk.OptionMenu(filter_frame, self.filter_vars['colour'], 'All')
        self.colour_menu.grid(row=0, column=5, padx=5, pady=5)

        self.prev_button = tk.Button(self, text="Previous", command=self.prev_page)
        self.prev_button.grid(row=2, column=0, sticky='w', padx=10, pady=10)

        self.next_button = tk.Button(self, text="Next", command=self.next_page)
        self.next_button.grid(row=2, column=2, sticky='e', padx=10, pady=10)

        self.switch_button = tk.Button(self, text="View Cameras", command=lambda: self.controller.show_frame("CameraScreen"))
        self.switch_button.grid(row=4, column=0, columnspan=3, pady=20)

    def load_icons(self):
        try:
            self.icons = {
                'Water': ImageTk.PhotoImage(Image.open('icons8-100--40.png').resize((15, 15))),
                'BlueWater': ImageTk.PhotoImage(Image.open('icons8-100--16.png').resize((15, 15))),
                'Empthy': ImageTk.PhotoImage(Image.open('icons8-circle-40.png').resize((15, 15))),
            }
        except Exception as e:
            print(f"Error loading icons: {e}")

    def read_logs_from_file(self, filename):
        logs = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        camera, date, color = parts[:3]
                        log = {
                            'camera': camera,
                            'date': date,
                            'colour': color,
                        }
                        logs.append(log)
                    else:
                        print(f"Skipping invalid log line: {line.strip()}")
        except FileNotFoundError:
            print(f"File {filename} not found.")
        return logs

    def apply_filters(self, event=None):
        self.filtered_logs = [
            log for log in self.fake_logs
            if (self.filter_vars['camera'].get() == 'All' or self.filter_vars['camera'].get() == log['camera']) and
               (self.filter_vars['colour'].get() == 'All' or self.filter_vars['colour'].get() == log['colour']) and
               (self.filter_vars['date'].get() in log['date'])
        ]
        self.current_page = 0
        self.display_logs()
        self.update_status_bars()

    def display_logs(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        start = self.current_page * self.logs_per_page
        end = start + self.logs_per_page
        for log in self.filtered_logs[start:end]:
            self.tree.insert('', 'end', values=(
                log['camera'],
                log['date'],
                '',
            ))

        self.add_icon_images()
        self.update_status_bars()

    def add_icon_images(self):
        for label in self.image_references.values():
            label.destroy()
        self.image_references.clear()

        logs = self.filtered_logs[self.current_page * self.logs_per_page:(self.current_page + 1) * self.logs_per_page]

        for idx, log in enumerate(logs):
            if log['colour']:
                icon = self.icons[log['colour']]
                item_id = self.tree.get_children()[idx]
                label = tk.Label(self.tree, image=icon)
                label.image = icon
                label.place(relx=0.83, rely=0.5, anchor='center', y=idx * 20 - 185)
                self.image_references[item_id] = label

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_logs()

    def next_page(self):
        if (self.current_page + 1) * self.logs_per_page < len(self.filtered_logs):
            self.current_page += 1
            self.display_logs()

    def update_status_bars(self):
        camera1_logs = [log for log in self.filtered_logs if log['camera'] == 'Camera 1']
        camera2_logs = [log for log in self.filtered_logs if log['camera'] == 'Camera 2']
        
        self.create_segmented_progressbar_style(self.camera1_bar, camera1_logs)
        self.create_segmented_progressbar_style(self.camera2_bar, camera2_logs)
        
    def create_segmented_progressbar_style(self, progressbar, logs):
        progressbar.delete("all")
        if not logs:
            return

        color_map = {'BlueWater': '#0000FF', 'Water': '#A52A2A', 'Empthy': '#FFFFFF'}
        
        segment_length = 1320 / len(logs)
        position = 0

        for log in logs:
            color = color_map.get(log['colour'], 'gray')
            progressbar.create_rectangle(
                position, 0, position + segment_length, 20,
                fill=color, outline=color
            )
            position += segment_length

    def create_status_bars(self):
        self.status_frame = tk.Frame(self)
        self.status_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky='ew')

        self.camera1_label = tk.Label(self.status_frame, text="Camera 1")
        self.camera1_label.grid(row=0, column=0, padx=5, pady=2, sticky='ew')
        self.camera1_bar = tk.Canvas(self.status_frame, height=20)
        self.camera1_bar.grid(row=1, column=0, padx=5, pady=2, sticky='ew')

        self.camera2_label = tk.Label(self.status_frame, text="Camera 2")
        self.camera2_label.grid(row=2, column=0, padx=5, pady=2, sticky='ew')
        self.camera2_bar = tk.Canvas(self.status_frame, height=20)
        self.camera2_bar.grid(row=3, column=0, padx=5, pady=2, sticky='ew')

        self.status_frame.grid_columnconfigure(0, weight=1)
