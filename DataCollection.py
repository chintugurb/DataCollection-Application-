import cv2
import os
import json
import time
import platform
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime

try:
    from pygrabber.dshow_graph import FilterGraph
    HAS_PYGRABBER = True
except ImportError:
    HAS_PYGRABBER = False

class LedgerCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ledger Document Capture System")
        self.root.geometry("1100x750")
        self.root.configure(bg="#1e1e1e")
        
        # Apply Professional Styling
        self.apply_theme()
        
        # Application State
        self.cap = None
        self.is_running = False
        self.save_directory = os.path.join(os.getcwd(), "raw_ledger_images")
        self.current_page = 1
        self.camera_dict = {}
        
        # Cooldown State
        self.last_capture_time = 0
        self.capture_cooldown = 0.5
        
        os.makedirs(self.save_directory, exist_ok=True)
        self.setup_ui()
        self.refresh_cameras()

    def apply_theme(self):
        style = ttk.Style(self.root)
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        bg_dark = "#2b2b2b"
        fg_light = "#f0f0f0"
        accent_blue = "#007acc"
        accent_blue_hover = "#005f9e"
        bg_entry = "#3c3c3c"
        
        style.configure("Control.TFrame", background=bg_dark)
        style.configure("TLabel", background=bg_dark, foreground=fg_light, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 10, "bold"), padding=(0, 5, 0, 2))
        
        style.configure("TEntry", fieldbackground=bg_entry, foreground="white", borderwidth=0)
        style.configure("TCombobox", fieldbackground=bg_entry, background=bg_dark, foreground="white", arrowcolor="white")
        
        style.configure("TButton", background=accent_blue, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=6)
        style.map("TButton", background=[("active", accent_blue_hover), ("disabled", "#555555")], foreground=[("disabled", "#888888")])
        
        style.configure("Status.TLabel", foreground="#4caf50", font=("Segoe UI", 9, "bold"))

    def setup_ui(self):
        control_frame = ttk.Frame(self.root, style="Control.TFrame", padding="20")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(control_frame, text="Save Directory:", style="Header.TLabel").pack(anchor=tk.W)
        self.dir_var = tk.StringVar(value=self.save_directory)
        dir_entry = ttk.Entry(control_frame, textvariable=self.dir_var, state="readonly", width=35)
        dir_entry.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(control_frame, text="Browse Folder", command=self.select_directory).pack(fill=tk.X, pady=(0, 20))

        ttk.Label(control_frame, text="Select USB Camera:", style="Header.TLabel").pack(anchor=tk.W)
        self.camera_var = tk.StringVar()
        self.camera_combo = ttk.Combobox(control_frame, textvariable=self.camera_var, state="readonly")
        self.camera_combo.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(control_frame, text="Refresh Cameras", command=self.refresh_cameras).pack(fill=tk.X, pady=(0, 20))

        ttk.Label(control_frame, text="Camera Aspect Factor:", style="Header.TLabel").pack(anchor=tk.W)
        self.orientation_var = tk.StringVar(value="Landscape")
        self.orientation_combo = ttk.Combobox(control_frame, textvariable=self.orientation_var, state="readonly")
        self.orientation_combo['values'] = ["Landscape", "Portrait"]
        self.orientation_combo.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(control_frame, text="Ledger Book ID:", style="Header.TLabel").pack(anchor=tk.W)
        self.ledger_id_entry = ttk.Entry(control_frame)
        self.ledger_id_entry.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(control_frame, text="Page Number:", style="Header.TLabel").pack(anchor=tk.W)
        self.page_entry = ttk.Entry(control_frame)
        self.page_entry.insert(0, "1")
        self.page_entry.pack(fill=tk.X, pady=(0, 25))

        self.start_btn = ttk.Button(control_frame, text="Start Camera", command=self.start_camera)
        self.start_btn.pack(fill=tk.X, pady=5)

        self.capture_btn = ttk.Button(control_frame, text="Capture [SPACE]", command=self.capture_image, state=tk.DISABLED)
        self.capture_btn.pack(fill=tk.X, pady=5)

        self.stop_btn = ttk.Button(control_frame, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED)
        self.stop_btn.pack(fill=tk.X, pady=5)

        self.status_var = tk.StringVar(value="System Ready.")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, wraplength=250, style="Status.TLabel")
        status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.video_container = tk.Frame(self.root, bg="black", bd=2, relief=tk.SUNKEN)
        self.video_container.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        self.video_label = tk.Label(self.video_container, bg="black")
        self.video_label.pack(expand=True)

        self.root.bind('<space>', lambda event: self.capture_image() if self.is_running else None)

    def refresh_cameras(self):
        self.status_var.set("Scanning for cameras...")
        self.root.update()
        
        self.camera_dict.clear()
        system = platform.system()

        if system == "Windows" and HAS_PYGRABBER:
            graph = FilterGraph()
            try:
                devices = graph.get_input_devices()
                for index, name in enumerate(devices):
                    self.camera_dict[f"{name} (Port {index})"] = index
            except Exception as e:
                print(f"Pygrabber error: {e}")

        if not self.camera_dict:
            backend = cv2.CAP_DSHOW if system == "Windows" else cv2.CAP_V4L2 if system == "Linux" else cv2.CAP_ANY
            
            for i in range(4): 
                cap = cv2.VideoCapture(i, backend)
                if cap.isOpened():
                    name = f"Camera {i}"
                    if system == "Linux":
                        try:
                            with open(f"/sys/class/video4linux/video{i}/name", "r") as f:
                                name = f.read().strip()
                        except FileNotFoundError:
                            pass
                            
                    self.camera_dict[f"{name} (Port {i})"] = i
                    cap.release()

        if not self.camera_dict:
            self.camera_dict["No Cameras Found"] = -1
            
        device_list = list(self.camera_dict.keys())
        self.camera_combo['values'] = device_list
        self.camera_combo.current(0)
        self.status_var.set("Camera list updated.")

    def select_directory(self):
        selected_dir = filedialog.askdirectory(initialdir=self.save_directory, title="Select Save Folder")
        if selected_dir:
            self.save_directory = selected_dir
            self.dir_var.set(selected_dir)

    def start_camera(self):
        selected_name = self.camera_var.get()
        cam_index = self.camera_dict.get(selected_name, -1)
        
        if cam_index == -1:
            messagebox.showerror("Camera Error", "No valid camera selected.")
            return

        system = platform.system()
        backend = cv2.CAP_DSHOW if system == "Windows" else cv2.CAP_V4L2 if system == "Linux" else cv2.CAP_ANY

        self.cap = cv2.VideoCapture(cam_index, backend)

        if not self.cap.isOpened():
            messagebox.showerror("Camera Error", f"Cannot open {selected_name}. Verify hardware connection.")
            return

        # Enforce maximum resolution requests for dense pixel capture
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4000) 
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3000)

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.camera_combo.config(state=tk.DISABLED)
        self.capture_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set(f"Active: {selected_name}")

        self.update_video_feed()

    def update_video_feed(self):
        if self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                if self.orientation_var.get() == "Portrait":
                    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                
                container_width = self.video_container.winfo_width()
                container_height = self.video_container.winfo_height()
                
                if container_width < 10: container_width = 700
                if container_height < 10: container_height = 500

                width_ratio = container_width / img.width
                height_ratio = container_height / img.height
                scale_factor = min(width_ratio, height_ratio)
                
                new_width = int(img.width * scale_factor)
                new_height = int(img.height * scale_factor)

                img = img.resize((new_width, new_height), Image.LANCZOS)
                
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
                
                self.root.after(15, self.update_video_feed)
            else:
                self.stop_camera()
                messagebox.showerror("Feed Error", "Lost connection to the active camera.")

    def capture_image(self):
        current_time = time.time()
        if current_time - self.last_capture_time < self.capture_cooldown:
            return 
        self.last_capture_time = current_time

        if not self.is_running or not self.cap.isOpened():
            return

        ledger_id = self.ledger_id_entry.get().strip()
        page_text = self.page_entry.get().strip()

        if not ledger_id:
            messagebox.showwarning("Input Error", "Ledger Book ID is mandatory for proper naming.")
            return
        
        if not page_text.isdigit():
            messagebox.showwarning("Input Error", "Page Number requires a numeric integer value.")
            return

        self.current_page = int(page_text)
        ret, frame = self.cap.read()

        if ret:
            if self.orientation_var.get() == "Portrait":
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            # Convert BGR OpenCV frame to RGB for PIL processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"{timestamp}_{ledger_id}_{self.current_page:04d}"
            
            image_filepath = os.path.join(self.save_directory, f"{base_filename}.png")
            meta_filepath = os.path.join(self.save_directory, f"{base_filename}.json")

            # Save via PIL to strictly enforce 300 DPI physical metadata in the PNG header
            pil_image.save(image_filepath, format="PNG", dpi=(300, 300))

            metadata = {
                "timestamp": timestamp,
                "ledger_book_id": ledger_id,
                "page_number": self.current_page,
                "file_format": "PNG",
                "resolution": f"{frame.shape[1]}x{frame.shape[0]}",
                "dpi": 300,
                "color_space": "RGB",
                "orientation": self.orientation_var.get(),
                "camera_name": self.camera_var.get(),
                "environmental_conditions": "Controlled Copy Stand",
                "lighting_parameters": "Constant LED Ring Light",
                "digital_zoom": "Disabled"
            }
            
            with open(meta_filepath, 'w') as meta_file:
                json.dump(metadata, meta_file, indent=4)

            self.status_var.set(f"Archived: {base_filename}.png")

            self.current_page += 1
            self.page_entry.delete(0, tk.END)
            self.page_entry.insert(0, str(self.current_page))

    def stop_camera(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        
        self.video_label.configure(image='')
        
        self.start_btn.config(state=tk.NORMAL)
        self.camera_combo.config(state=tk.NORMAL)
        self.capture_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("Camera feed terminated.")

    def on_close(self):
        self.stop_camera()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LedgerCaptureApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()