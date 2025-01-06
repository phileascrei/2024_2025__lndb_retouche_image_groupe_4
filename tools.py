import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy as np

class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Application de Retouche d'Image")
        self.geometry("1000x700")

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

        # PanedWindow pour séparer la zone d'affichage de l'image et la zone des contrôles de réglage
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Frame d'affichage de l'image
        self.image_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.image_frame, stretch="always")

        self.canvas = tk.Canvas(self.image_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Barre de réglages
        self.adjustment_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.adjustment_frame, stretch="never")

        # Sliders et boutons "auto"
        self.create_adjustment_controls()

    def create_adjustment_controls(self):
        self.exposure_slider = self.create_slider("Exposition", self.adjust_exposure)
        self.create_auto_button("Auto Exposition", self.auto_adjust_exposure)

        self.contrast_slider = self.create_slider("Contraste", self.adjust_contrast)
        self.create_auto_button("Auto Contraste", self.auto_adjust_contrast)

        self.saturation_slider = self.create_slider("Saturation", self.adjust_saturation)
        self.create_auto_button("Auto Saturation", self.auto_adjust_saturation)

        self.highlights_slider = self.create_slider("Hautes Lumières", self.adjust_highlights)
        self.create_auto_button("Auto Hautes Lumières", self.auto_adjust_highlights)

        self.shadows_slider = self.create_slider("Basses Lumières", self.adjust_shadows)
        self.create_auto_button("Auto Basses Lumières", self.auto_adjust_shadows)

    def create_slider(self, label, command):
        frame = tk.Frame(self.adjustment_frame)
        frame.pack(fill=tk.X, pady=5)

        label = tk.Label(frame, text=label)
        label.pack(side=tk.LEFT)

        slider = ttk.Scale(frame, from_=0, to=255, orient=tk.HORIZONTAL, command=command)
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        return slider

    def create_auto_button(self, label, command):
        button = tk.Button(self.adjustment_frame, text=label, command=command)
        button.pack(fill=tk.X, pady=5)

    def open_image(self):
        file_path = filedialog.askopenfilename(title="Choisissez une image")
        if not file_path:
            print("Aucun fichier sélectionné.")
            return

        self.image_path = file_path
        self.original_image = Image.open(file_path)
        self.display_image = self.original_image.copy()
        self.display_on_canvas()

    def save_image(self):
        if self.display_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                     filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if save_path:
                self.display_image.save(save_path)
                print(f"Image enregistrée sous {save_path}")

    def display_on_canvas(self):
        self.tk_image = ImageTk.PhotoImage(self.display_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def adjust_exposure(self, value):
        if self.original_image:
            target_exposure = float(value)
            self.display_image = adjust_exposure(self.original_image, target_exposure)
            self.display_on_canvas()

    def auto_adjust_exposure(self):
        if self.original_image:
            target_exposure = determine_target_exposure(self.original_image)
            self.exposure_slider.set(target_exposure)
            self.adjust_exposure(target_exposure)

    def adjust_contrast(self, value):
        if self.original_image:
            target_contrast = float(value)
            self.display_image = adjust_contrast(self.original_image, target_contrast)
            self.display_on_canvas()

    def auto_adjust_contrast(self):
        if self.original_image:
            target_contrast = determine_target_contrast(self.original_image)
            self.contrast_slider.set(target_contrast)
            self.adjust_contrast(target_contrast)

    def adjust_saturation(self, value):
        if self.original_image:
            target_saturation = float(value)
            self.display_image = adjust_saturation(self.original_image, target_saturation)
            self.display_on_canvas()

    def auto_adjust_saturation(self):
        if self.original_image:
            target_saturation = determine_target_saturation(self.original_image)
            self.saturation_slider.set(target_saturation)
            self.adjust_saturation(target_saturation)

    def adjust_highlights(self, value):
        if self.original_image:
            factor = float(value) / 128  # Normaliser la valeur
            self.display_image = adjust_highlights(self.original_image, factor)
            self.display_on_canvas()

    def auto_adjust_highlights(self):
        if self.original_image:
            factor = 0.8  # Exemple de facteur pour les hautes lumières
            self.highlights_slider.set(factor * 128)  # Dé-normaliser la valeur
            self.adjust_highlights(factor * 128)

    def adjust_shadows(self, value):
        if self.original_image:
            factor = float(value) / 128  # Normaliser la valeur
            self.display_image = adjust_shadows(self.original_image, factor)
            self.display_on_canvas()

    def auto_adjust_shadows(self):
        if self.original_image:
            factor = 1.2  # Exemple de facteur pour les basses lumières
            self.shadows_slider.set(factor * 128)  # Dé-normaliser la valeur
            self.adjust_shadows(factor * 128)

def adjust_exposure(image, target_exposure):
    enhancer = ImageEnhance.Brightness(image)
    current_exposure = analyse_exposition(image)
    factor = target_exposure / current_exposure
    return enhancer.enhance(factor)

def adjust_contrast(image, target_contrast):
    enhancer = ImageEnhance.Contrast(image)
    current_contrast = analyse_contrast(image)
    factor = target_contrast / current_contrast
    return enhancer.enhance(factor)

def adjust_saturation(image, target_saturation):
    enhancer = ImageEnhance.Color(image)
    current_saturation = analyse_saturation(image)
    factor = target_saturation / current_saturation
    return enhancer.enhance(factor)

def adjust_highlights(image, factor):
    image = image.convert("RGB")
    np_image = np.array(image)
    mask = np_image > 128  # Masque pour les hautes lumières
    np_image[mask] = np.clip(np_image[mask] * factor, 0, 255).astype(np.uint8)
    return Image.fromarray(np_image)

def adjust_shadows(image, factor):
    image = image.convert("RGB")
    np_image = np.array(image)
    mask = np_image < 128  # Masque pour les basses lumières
    np_image[mask] = np.clip(np_image[mask] * factor, 0, 255).astype(np.uint8)
    return Image.fromarray(np_image)

def determine_target_exposure(image):
    current_exposure = analyse_exposition(image)
    target_exposure = 128  # Valeur cible pour une exposition moyenne
    return target_exposure

def determine_target_contrast(image):
    current_contrast = analyse_contrast(image)
    target_contrast = 50  # Valeur cible pour un contraste moyen
    return target_contrast

def determine_target_saturation(image):
    current_saturation = analyse_saturation(image)
    target_saturation = 1  # Valeur cible pour une saturation moyenne
    return target_saturation

def analyse_exposition(image):
    image = image.convert("L")
    np_image = np.array(image)
    mean_brightness = np.mean(np_image)
    return mean_brightness

def analyse_contrast(image):
    image = image.convert("L")
    np_image = np.array(image)
    contrast = np.std(np_image)
    return contrast 

def analyse_saturation(image):
    image = image.convert("RGB")
    np_image = np.array(image)
    r, g, b = np_image[:,:,0], np_image[:,:,1], np_image[:,:,2]
    max_val = np.maximum(np.maximum(r, g), b)
    min_val = np.minimum(np.minimum(r, g), b)
    saturation = (max_val - min_val) / (max_val + 1e-10)  # Ajout d'une petite valeur pour éviter la division par zéro
    mean_saturation = np.mean(saturation)
    return mean_saturation

if __name__ == "__main__":
    app = ImageEditor()
    app.mainloop()












class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Application de Retouche d'Image")
        self.geometry("800x600")

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

        # Frame d'affichage de l'image
        self.image_frame = tk.Frame(self)
        self.image_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.image_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Barre de réglages
        self.adjustment_frame = tk.Frame(self)
        self.adjustment_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.brightness_label = tk.Label(self.adjustment_frame, text="Luminosité")
        self.brightness_label.pack()
        self.brightness_slider = tk.Scale(self.adjustment_frame, from_=0, to_=2, orient=tk.HORIZONTAL, resolution=0.1, command=self.adjust_brightness)
        self.brightness_slider.set(1)
        self.brightness_slider.pack()

        self.contrast_label = tk.Label(self.adjustment_frame, text="Contraste")
        self.contrast_label.pack()
        self.contrast_slider = tk.Scale(self.adjustment_frame, from_=0, to_=2, orient=tk.HORIZONTAL, resolution=0.1, command=self.adjust_contrast)
        self.contrast_slider.set(1)
        self.contrast_slider.pack()

        # Boutons de transformation
        self.rotate_button = tk.Button(self.adjustment_frame, text="Rotation", command=self.rotate_image)
        self.rotate_button.pack()

        self.crop_button = tk.Button(self.adjustment_frame, text="Recadrer", command=self.crop_image)
        self.crop_button.pack()

        # Filtres
        self.filter_label = tk.Label(self.adjustment_frame, text="Filtres")
        self.filter_label.pack()
        self.filter_button_bw = tk.Button(self.adjustment_frame, text="Noir & Blanc", command=self.apply_black_white_filter)
        self.filter_button_bw.pack()
        self.filter_button_sepia = tk.Button(self.adjustment_frame, text="Sépia", command=self.apply_sepia_filter)
        self.filter_button_sepia.pack()

        # Zoom
        self.zoom_label = tk.Label(self.adjustment_frame, text="Zoom")
        self.zoom_label.pack()
        self.zoom_slider = tk.Scale(self.adjustment_frame, from_=0.1, to_=3.0, orient=tk.HORIZONTAL, resolution=0.1, command=self.zoom_image)
        self.zoom_slider.set(1)
        self.zoom_slider.pack()

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
            self.display_image.thumbnail((self.zoom_factor * 700, self.zoom_factor * 500))
            img_tk = ImageTk.PhotoImage(self.display_image)
            self.canvas.delete("all")
            self.canvas.create_image(1000, 500, image=img_tk)  # Centrer l'image
            self.canvas.image = img_tk

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
            self.display_image = self.display_image.convert("L")  # Convertir en noir et blanc
            self.display_on_canvas()

    def apply_sepia_filter(self):
        if self.display_image:
            width, height = self.display_image.size
            pixels = self.display_image.load()

            for py in range(height):
                for px in range(width):
                    r, g, b = self.display_image.getpixel((px, py))

                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                    if tr > 255:
                        tr = 255

                    if tg > 255:
                        tg = 255

                    if tb > 255:
                        tb = 255

                    pixels[px, py] = (tr, tg, tb)

            self.display_on_canvas()

    def zoom_image(self, value):
        self.zoom_factor = float(value)
        if self.original_image:
            self.display_image = self.original_image.resize(
                (int(self.original_image.width * self.zoom_factor), int(self.original_image.height * self.zoom_factor)),
                Image.Resampling.LANCZOS
            )
            self.display_on_canvas()

