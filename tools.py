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
        self.configure(bg="#263238")

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
        self.main_frame = tk.Frame(self, bg="#263238")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas pour afficher l'image
        self.canvas_frame = tk.Frame(self.main_frame, bg="#3b4d56", relief=tk.RIDGE, bd=2)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#3b4d56")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Barre de réglages
        self.controls_frame = tk.Frame(self.main_frame, bg="#263238")
        self.controls_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.create_controls()

        self.crop_button = tk.Button(self.controls_frame, text="Crop Image", command=self.open_crop_window)
        self.crop_button.pack(fill=tk.X, pady=5)

    def create_controls(self):
        # Définir la police en gras
        bold_font_text = ("Helvetica", 8, "bold")
        bold_font_title = ("Helvetica", 12, "bold")
        # Sliders et boutons "auto"
        tk.Label(self.controls_frame, text="Exposition", bg="#263238", fg="#eceff1", font=bold_font_title).pack(anchor="w", pady=5)
        self.exposure_slider = tk.Scale(self.controls_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self.adjust_exposure, bg="#3b4d56", fg="white", font=bold_font_text)
        self.exposure_slider.pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Auto Exposition", command=self.auto_adjust_exposure, bg="#3b4d56", fg="white", font=bold_font_text).pack(fill=tk.X, pady=5)

        tk.Label(self.controls_frame, text="Contraste", bg="#263238", fg="#eceff1", font=bold_font_title).pack(anchor="w", pady=5)
        self.contrast_slider = tk.Scale(self.controls_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self.adjust_contrast, bg="#3b4d56", fg="white", font=bold_font_text)
        self.contrast_slider.pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Auto Contraste", command=self.auto_adjust_contrast, bg="#3b4d56", fg="white", font=bold_font_text).pack(fill=tk.X, pady=5)

        tk.Label(self.controls_frame, text="Saturation", bg="#263238", fg="#eceff1", font=bold_font_title).pack(anchor="w", pady=5)
        self.saturation_slider = tk.Scale(self.controls_frame, from_=-4, to=5, resolution=0.01, orient=tk.HORIZONTAL, command=self.adjust_saturation, bg="#3b4d56", fg="white", font=bold_font_text)
        self.saturation_slider.pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Auto Saturation", command=self.auto_adjust_saturation, bg="#3b4d56", fg="white", font=bold_font_text).pack(fill=tk.X, pady=5)


        tk.Label(self.controls_frame, text="Hautes Lumières", bg="#263238", fg="#eceff1", font=bold_font_title).pack(anchor="w", pady=5)
        self.highlights_slider = tk.Scale(self.controls_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self.adjust_highlights, bg="#3b4d56", fg="white", font=bold_font_text)
        self.highlights_slider.pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Auto Hautes Lumières", command=self.auto_adjust_highlights, bg="#3b4d56", fg="white", font=bold_font_text).pack(fill=tk.X, pady=5)

        tk.Label(self.controls_frame, text="Basses Lumières", bg="#263238", fg="#eceff1", font=bold_font_title).pack(anchor="w", pady=5)
        self.shadows_slider = tk.Scale(self.controls_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self.adjust_shadows, bg="#3b4d56", fg="white", font=bold_font_text)
        self.shadows_slider.pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Auto Basses Lumières", command=self.auto_adjust_shadows, bg="#3b4d56", fg="white", font=bold_font_text).pack(fill=tk.X, pady=5)

        # Zoom
        tk.Label(self.controls_frame, text="Zoom", bg="#263238", fg="#eceff1", font=bold_font_title).pack(anchor="w", pady=5)
        self.zoom_slider = tk.Scale(self.controls_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.zoom_image, bg="#3b4d56", fg="white", font=bold_font_text)
        self.zoom_slider.set(1)
        self.zoom_slider.pack(fill=tk.X, pady=5)

        # Bouton reset 
        tk.Button(self.controls_frame, text="Réinitialiser", command=self.reset_sliders, bg="#3b4d56", fg="#eceff1", font=bold_font_title).pack(fill=tk.X, pady=5)


    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.display_image = self.original_image
            self.reset_sliders()
            self.display_on_canvas()

    def save_image(self):
        if self.display_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if file_path:
                self.display_image.save(file_path)

    def display_on_canvas(self):
        if self.display_image:
            img_tk = ImageTk.PhotoImage(self.display_image)
            self.canvas.delete("all")
            
            # Obtenir les dimensions du canvas et de l'image
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image_width = img_tk.width()
            image_height = img_tk.height()
            
            # Calculer les coordonnées pour centrer l'image
            x = (canvas_width - image_width) // 2
            y = (canvas_height - image_height) // 2
            
            self.canvas.create_image(x, y, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk


    def reset_sliders(self):
            self.exposure_slider.set(128)
            self.contrast_slider.set(128)
            self.saturation_slider.set(1)
            self.highlights_slider.set(128)
            self.shadows_slider.set(128)
            #self.zoom_slider.set(1)

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
        if self.display_image:
            # Calculer la saturation moyenne de l'image
            img_array = np.array(self.display_image.convert("RGB"))
            r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
            avg_saturation = np.mean([r, g, b]) / 255.0
            
            # Ajuster la saturation pour qu'elle soit autour de 1.0
            target_saturation = 1.0 / avg_saturation
            enhancer = ImageEnhance.Color(self.display_image)
            self.display_image = enhancer.enhance(target_saturation)
            self.show_image()

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

    def apply_blur_filter(self):
        if self.display_image:
            self.display_image = self.display_image.filter(ImageFilter.BLUR)
            self.display_on_canvas()

    def zoom_image(self, value):
        self.zoom_factor = float(value)
        if self.original_image:
            self.display_image = self.original_image.resize(
                (int(self.original_image.width * self.zoom_factor), int(self.original_image.height * self.zoom_factor)),
                Image.Resampling.LANCZOS
            )
            self.display_on_canvas()

    def open_crop_window(self):
        if not self.original_image:
            return

        crop_window = tk.Toplevel(self)
        crop_window.title("Crop Image")

        def update_crop():
            try:
                x1 = int(entry_x1.get())
                y1 = int(entry_y1.get())
                x2 = int(entry_x2.get())
                y2 = int(entry_y2.get())
                cropped_image = self.original_image.crop((x1, y1, x2, y2))
                self.display_image = ImageTk.PhotoImage(cropped_image)
                self.canvas.config(image=self.display_image)
                self.canvas.image = self.display_image
            except ValueError:
                pass

        def sync_entries_with_sliders(*args):
            entry_x1.delete(0, tk.END)
            entry_x1.insert(0, slider_x1.get())
            entry_y1.delete(0, tk.END)
            entry_y1.insert(0, slider_y1.get())
            entry_x2.delete(0, tk.END)
            entry_x2.insert(0, slider_x2.get())
            entry_y2.delete(0, tk.END)
            entry_y2.insert(0, slider_y2.get())
            update_crop()

        slider_x1 = tk.Scale(crop_window, from_=0, to=self.original_image.width, orient=tk.HORIZONTAL, label="x1", command=sync_entries_with_sliders)
        slider_x1.pack()
        slider_y1 = tk.Scale(crop_window, from_=0, to=self.original_image.height, orient=tk.HORIZONTAL, label="y1", command=sync_entries_with_sliders)
        slider_y1.pack()
        slider_x2 = tk.Scale(crop_window, from_=0, to=self.original_image.width, orient=tk.HORIZONTAL, label="x2", command=sync_entries_with_sliders)
        slider_x2.pack()
        slider_y2 = tk.Scale(crop_window, from_=0, to=self.original_image.height, orient=tk.HORIZONTAL, label="y2", command=sync_entries_with_sliders)
        slider_y2.pack()

        tk.Label(crop_window, text="x1:").pack()
        entry_x1 = tk.Entry(crop_window)
        entry_x1.pack()
        entry_x1.bind("<Return>", lambda event: update_crop())

        tk.Label(crop_window, text="y1:").pack()
        entry_y1 = tk.Entry(crop_window)
        entry_y1.pack()
        entry_y1.bind("<Return>", lambda event: update_crop())

        tk.Label(crop_window, text="x2:").pack()
        entry_x2 = tk.Entry(crop_window)
        entry_x2.pack()
        entry_x2.bind("<Return>", lambda event: update_crop())

        tk.Label(crop_window, text="y2:").pack()
        entry_y2 = tk.Entry(crop_window)
        entry_y2.pack()
        entry_y2.bind("<Return>", lambda event: update_crop())

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