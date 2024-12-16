import tkinter as tk
from tkinter import filedialog, messagebox
from vehicle_counter import VehicleCounter

class VehicleCounterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Contador de Veículos")
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

        # Limiar de Confiança #parete do principicil de aprenizagem de IA
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

        # Botão para Selecionar e Processar Vídeos
        self.process_button = tk.Button(self.root, text="Selecionar e Processar Vídeos", command=self.select_and_process_videos)
        self.process_button.pack()
    def select_and_process_videos(self):
        video_paths = filedialog.askopenfilenames(filetypes=[("Video files", "*.dav")])
        output_folder = filedialog.askdirectory(title="Selecione a pasta de saída")
        frame_skip = int(self.frame_skip_entry.get())
        resolution = (int(self.width_entry.get()), int(self.height_entry.get()))
        confidence_threshold = float(self.confidence_entry.get())
        show_video = self.show_video_var.get()
        output_format = self.output_format_var.get()
        
        for video_path in video_paths:
            excel_filename = self.counter.process_video(video_path, output_folder, frame_skip, show_video, resolution, confidence_threshold, output_format)
            messagebox.showinfo("Processamento Concluído", f"Arquivo salvo como {excel_filename}")

    def run(self):
        self.root.mainloop()
