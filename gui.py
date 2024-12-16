import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from vehicle_counter import VehicleCounter
import cv2
from PIL import Image, ImageTk

class VehicleCounterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Contador de Veículos")
        self.root.state('zoomed')
        self.counter = VehicleCounter()

        # Frame Skip
        self.frame_skip_label = tk.Label(self.root, text="Frame Skip:")
        self.frame_skip_label.pack()
        self.frame_skip_entry = tk.Entry(self.root)
        self.frame_skip_entry.pack()
        self.frame_skip_entry.insert(0, "15")

        # Resolução
        self.resolution_label = tk.Label(self.root, text="Resolução (Largura x Altura):")
        self.resolution_label.pack()
        self.width_entry = tk.Entry(self.root)
        self.width_entry.pack()
        self.width_entry.insert(0, "640")
        self.height_entry = tk.Entry(self.root)
        self.height_entry.pack()
        self.height_entry.insert(0, "480")

        # Limiar de Confiança
        self.confidence_label = tk.Label(self.root, text="Limiar de Confiança:")
        self.confidence_label.pack()
        self.confidence_entry = tk.Entry(self.root)
        self.confidence_entry.pack()
        self.confidence_entry.insert(0, "0.5")

        # Mostrar Vídeo
        self.show_video_var = tk.BooleanVar(value=True)
        self.show_video_check = tk.Checkbutton(self.root, text="Mostrar Vídeo", variable=self.show_video_var)
        self.show_video_check.pack()

        # Formato de Saída
        self.output_format_label = tk.Label(self.root, text="Formato de Saída:")
        self.output_format_label.pack()
        self.output_format_var = tk.StringVar(value="xlsx")
        self.output_format_option = tk.OptionMenu(self.root, self.output_format_var, "xlsx", "csv")
        self.output_format_option.pack()

        # Labels para Contagem de Veículos
        self.count_frame = tk.Frame(self.root)
        self.count_frame.pack()
        self.car_count_label = tk.Label(self.count_frame, text="Carros: 0")
        self.car_count_label.grid(row=0, column=0)
        self.truck_count_label = tk.Label(self.count_frame, text="Caminhões: 0")
        self.truck_count_label.grid(row=0, column=1)
        self.bus_count_label = tk.Label(self.count_frame, text="Ônibus: 0")
        self.bus_count_label.grid(row=0, column=2)
        self.motorcycle_count_label = tk.Label(self.count_frame, text="Motocicletas: 0")
        self.motorcycle_count_label.grid(row=0, column=3)

        # Botão para Selecionar e Processar Vídeos
        self.process_button = tk.Button(self.root, text="Selecionar e Processar Vídeos", command=self.select_and_process_videos)
        self.process_button.pack()

    def update_counts(self, car_count, truck_count, bus_count, motorcycle_count):
        self.car_count_label.config(text=f"Carros: {car_count}")
        self.truck_count_label.config(text=f"Caminhões: {truck_count}")
        self.bus_count_label.config(text=f"Ônibus: {bus_count}")
        self.motorcycle_count_label.config(text=f"Motocicletas: {motorcycle_count}")

    def show_frame(self, frame):
        cv2.imshow('Vehicle Detection', frame)
        cv2.waitKey(1)

    def select_and_process_videos(self):
        video_paths = filedialog.askopenfilenames(filetypes=[("Video files", "*.dav")])
        output_folder = filedialog.askdirectory(title="Selecione a pasta de saída")
        frame_skip = int(self.frame_skip_entry.get())
        resolution = (int(self.width_entry.get()), int(self.height_entry.get()))
        confidence_threshold = float(self.confidence_entry.get())
        show_video = self.show_video_var.get()
        output_format = self.output_format_var.get()
        
        for video_path in video_paths:
            self.counter.process_video(video_path, output_folder, frame_skip, show_video, resolution, confidence_threshold, output_format, self.show_frame, self.update_counts)
            messagebox.showinfo("Processamento Concluído", f"Arquivo salvo como {video_path}")

    def run(self):
        self.root.mainloop()