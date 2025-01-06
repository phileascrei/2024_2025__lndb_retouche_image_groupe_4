import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter



import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Application de Retouche d'Image")
        self.geometry("1000x700")
        self.configure(bg="#f4f4f4")

        self.image_path = None
        self.original_image = None
        self.display_image = None
        self.zoom_factor = 1.0

        # Barre de menu
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Menu Fichier
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)
        self.file_menu.add_command(label="Ouvrir", command=self.open_image)
        self.file_menu.add_command(label="Enregistrer", command=self.save_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", command=self.quit)

        # Section principale
        self.main_frame = tk.Frame(self, bg="#f4f4f4")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas pour afficher l'image
        self.canvas_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.RIDGE, bd=2)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#e6e6e6")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Panneau de réglages
        self.controls_frame = tk.Frame(self.main_frame, bg="#f4f4f4", width=250)
        self.controls_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.create_controls()

    def create_controls(self):
        # Luminosité
        tk.Label(self.controls_frame, text="Luminosité", bg="#f4f4f4").pack(anchor="w", pady=5)
        self.brightness_slider = tk.Scale(self.controls_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.adjust_brightness, bg="#f4f4f4")
        self.brightness_slider.set(1)
        self.brightness_slider.pack(fill=tk.X, pady=5)

        # Contraste
        tk.Label(self.controls_frame, text="Contraste", bg="#f4f4f4").pack(anchor="w", pady=5)
        self.contrast_slider = tk.Scale(self.controls_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.adjust_contrast, bg="#f4f4f4")
        self.contrast_slider.set(1)
        self.contrast_slider.pack(fill=tk.X, pady=5)

        # Netteté
        tk.Label(self.controls_frame, text="Netteté", bg="#f4f4f4").pack(anchor="w", pady=5)
        self.sharpness_slider = tk.Scale(self.controls_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.adjust_sharpness, bg="#f4f4f4")
        self.sharpness_slider.set(1)
        self.sharpness_slider.pack(fill=tk.X, pady=5)

        # Zoom
        tk.Label(self.controls_frame, text="Zoom", bg="#f4f4f4").pack(anchor="w", pady=5)
        self.zoom_slider = tk.Scale(self.controls_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.zoom_image, bg="#f4f4f4")
        self.zoom_slider.set(1)
        self.zoom_slider.pack(fill=tk.X, pady=5)

        # Boutons de transformation
        tk.Button(self.controls_frame, text="Rotation 90°", command=self.rotate_image, bg="#e0e0e0").pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Recadrer", command=self.crop_image, bg="#e0e0e0").pack(fill=tk.X, pady=5)

        # Filtres
        tk.Label(self.controls_frame, text="Filtres", bg="#f4f4f4").pack(anchor="w", pady=5)
        tk.Button(self.controls_frame, text="Noir & Blanc", command=self.apply_black_white_filter, bg="#e0e0e0").pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Sépia", command=self.apply_sepia_filter, bg="#e0e0e0").pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Flou", command=self.apply_blur_filter, bg="#e0e0e0").pack(fill=tk.X, pady=5)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.display_image = self.original_image
            self.display_on_canvas()

    def save_image(self):
        if self.display_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if file_path:
                self.display_image.save(file_path)

    def display_on_canvas(self):
        if self.display_image:
            resized_image = self.display_image.copy()
            resized_image.thumbnail((self.canvas.winfo_width(), self.canvas.winfo_height()))
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas.delete("all")
            self.canvas.create_image(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, image=self.tk_image, anchor=tk.CENTER)

    def adjust_brightness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Brightness(self.original_image)
            self.display_image = enhancer.enhance(float(value))
            self.display_on_canvas()

    def adjust_contrast(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Contrast(self.original_image)
            self.display_image = enhancer.enhance(float(value))
            self.display_on_canvas()

    def adjust_sharpness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Sharpness(self.original_image)
            self.display_image = enhancer.enhance(float(value))
            self.display_on_canvas()

    def rotate_image(self):
        if self.display_image:
            self.display_image = self.display_image.rotate(90, expand=True)
            self.display_on_canvas()

    def crop_image(self):
        if self.display_image:
            width, height = self.display_image.size
            self.display_image = self.display_image.crop((width//4, height//4, 3*width//4, 3*height//4))
            self.display_on_canvas()

    def apply_black_white_filter(self):
        if self.display_image:
            self.display_image = self.display_image.convert("L")
            self.display_on_canvas()

    def apply_sepia_filter(self):
        if self.display_image:
            sepia_image = self.display_image.convert("RGB")
            pixels = sepia_image.load()
            for y in range(sepia_image.height):
                for x in range(sepia_image.width):
                    r, g, b = pixels[x, y]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))
            self.display_image = sepia_image
            self.display_on_canvas()

    def apply_blur_filter(self):
        if self.display_image:
            self.display_image = self.display_image.filter(ImageFilter.BLUR)
            self.display_on_canvas()

    def zoom_image(self, value):
        self.zoom_factor = float(value)
        if self.original_image:
            width = int(self.original_image.width * self.zoom_factor)
            height = int(self.original_image.height * self.zoom_factor)
            self.display_image = self.original_image.resize((width, height), Image.Resampling.LANCZOS)
            self.display_on_canvas()

if __name__ == "__main__":
    app = ImageEditor()
    app.mainloop()


