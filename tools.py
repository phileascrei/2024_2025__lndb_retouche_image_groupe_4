import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import numpy as np


class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PYXEL")
        self.iconbitmap("H:\\NSI\\projet2\\2024_2025__lndb_retouche_image_groupe_4\\Logo_Pyxel\\logo_Pyxel_vdef_icon.ico")
        self.geometry("1000x700")
        self.configure(bg="#263238")

        self.image_path = None
        self.original_image = None
        self.display_image = None
        self.zoom_factor = 1.0
        
        # Paramètres de retouches
        self.exposure_factor = 1.0
        self.contrast_factor = 1.0
        self.saturation_factor = 1.0
        self.highlights_factor = 1.0
        self.shadows_factor = 1.0

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

        

    def create_controls(self):
        # Définir la police en gras
        bold_font_text = ("Helvetica", 8, "bold")
        bold_font_title = ("Helvetica", 12, "bold")
        # Sliders et boutons "auto"
        tk.Label(self.controls_frame, text="Exposition", bg="#263238", fg="#eceff1", font=bold_font_title).pack(anchor="w", pady=5)
        self.exposure_slider = tk.Scale(self.controls_frame, from_=0.00, to=2.00, resolution= 0.01, orient=tk.HORIZONTAL, command=self.adjust_exposure, bg="#3b4d56", fg="white", font=bold_font_text)
        self.exposure_slider.pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Auto Exposition", command=self.auto_adjust_exposure, bg="#3b4d56", fg="white", font=bold_font_text).pack(fill=tk.X, pady=5)

        tk.Label(self.controls_frame, text="Contraste", bg="#263238", fg="#eceff1", font=bold_font_title).pack(anchor="w", pady=5)
        self.contrast_slider = tk.Scale(self.controls_frame, from_=0.00, to=2.00, resolution= 0.01, orient=tk.HORIZONTAL, command=self.adjust_contrast, bg="#3b4d56", fg="white", font=bold_font_text)
        self.contrast_slider.pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Auto Contraste", command=self.auto_adjust_contrast, bg="#3b4d56", fg="white", font=bold_font_text).pack(fill=tk.X, pady=5)

        tk.Label(self.controls_frame, text="Saturation", bg="#263238", fg="#eceff1", font=bold_font_title).pack(anchor="w", pady=5)
        self.saturation_slider = tk.Scale(self.controls_frame, from_=-4.00, to=5.00, resolution=0.01, orient=tk.HORIZONTAL, command=self.adjust_saturation, bg="#3b4d56", fg="white", font=bold_font_text)
        self.saturation_slider.pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Auto Saturation", command=self.auto_adjust_saturation, bg="#3b4d56", fg="white", font=bold_font_text).pack(fill=tk.X, pady=5)


        tk.Label(self.controls_frame, text="Hautes Lumières", bg="#263238", fg="#eceff1", font=bold_font_title).pack(anchor="w", pady=5)
        self.highlights_slider = tk.Scale(self.controls_frame, from_=0.00, to=2.00, resolution= 0.01, orient=tk.HORIZONTAL, command=self.adjust_highlights, bg="#3b4d56", fg="white", font=bold_font_text)
        self.highlights_slider.pack(fill=tk.X, pady=5)
        tk.Button(self.controls_frame, text="Auto Hautes Lumières", command=self.auto_adjust_highlights, bg="#3b4d56", fg="white", font=bold_font_text).pack(fill=tk.X, pady=5)

        tk.Label(self.controls_frame, text="Basses Lumières", bg="#263238", fg="#eceff1", font=bold_font_title).pack(anchor="w", pady=5)
        self.shadows_slider = tk.Scale(self.controls_frame, from_=0.00, to=2.00, resolution= 0.01, orient=tk.HORIZONTAL, command=self.adjust_shadows, bg="#3b4d56", fg="white", font=bold_font_text)
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





    def zoom_image(self, value):
        self.zoom_factor = float(value)
        if self.original_image:
            self.display_image = self.display_image.resize(
                (int(self.
                original_image.width * self.zoom_factor), int(self.original_image.height * self.zoom_factor)),
                Image.Resampling.LANCZOS
            )
            self.display_on_canvas()

    def reset_sliders(self):
        self.exposure_slider.set(1.00)
        self.contrast_slider.set(1.00)
        self.saturation_slider.set(1.00)
        self.highlights_slider.set(1.00)
        self.shadows_slider.set(1.00)


    def update_image(self):
        if self.original_image:
            # Appliquer les ajustements de l'exposition
            enhancer = ImageEnhance.Brightness(self.original_image)
            updated_image = enhancer.enhance(self.exposure_factor)

            # Appliquer les ajustements du contraste
            enhancer = ImageEnhance.Contrast(updated_image)
            updated_image = enhancer.enhance(self.contrast_factor)

            # Appliquer les ajustements de la saturation
            enhancer = ImageEnhance.Color(updated_image)
            updated_image = enhancer.enhance(self.saturation_factor)

            # Appliquer les ajustements des hautes lumières
            img = np.array(updated_image.convert("RGB"), dtype=np.float32) / 255.0
            img[:, :, 0:3] = np.clip(img[:, :, 0:3] * self.highlights_factor, 0, 1)
            updated_image = Image.fromarray((img * 255).astype(np.uint8))

            # Appliquer les ajustements des basses lumières
            img = np.array(updated_image.convert("RGB"), dtype=np.float32) / 255.0
            shadows_mask = img < 0.5  # On cible les basses lumières
            img[shadows_mask] = np.clip(img[shadows_mask] * self.shadows_factor, 0, 1)
            updated_image = Image.fromarray((img * 255).astype(np.uint8))

            self.display_image = updated_image
            self.zoom_image(self.zoom_factor)
            self.display_on_canvas()

    def display_on_canvas(self):
        if self.display_image:
            self.display_image.thumbnail((self.zoom_factor * 700, self.zoom_factor * 500))
            img_tk = ImageTk.PhotoImage(self.display_image)
            self.canvas.delete("all")
            self.canvas.create_image(
                self.canvas.winfo_width() // 2,
                self.canvas.winfo_height() // 2,
                anchor=tk.CENTER,
                image=img_tk
            )
            self.canvas.image = img_tk






    def adjust_exposure(self, value):
        self.exposure_factor = float(value)
        self.update_image()

    def adjust_contrast(self, value):
        self.contrast_factor = float(value)
        self.update_image()

    def adjust_saturation(self, value):
        self.saturation_factor = float(value)
        self.update_image()

    def adjust_highlights(self, value):
        self.highlights_factor = float(value)
        self.update_image()

    def adjust_shadows(self, value):
        self.shadows_factor = float(value)
        self.update_image()





    def auto_adjust_exposure(self):
        exposure_factor = self.determine_target_exposure()
        self.exposure_slider.set(exposure_factor)
        self.adjust_exposure(self.determine_target_exposure())

    def auto_adjust_contrast(self):
        contrast_factor = self.determine_target_contrast()
        self.contrast_slider.set(contrast_factor)
        self.adjust_contrast(contrast_factor)

    def auto_adjust_saturation(self):
        saturation_factor = self.determine_target_saturation()
        self.saturation_slider.set(saturation_factor)
        self.adjust_saturation(self.determine_target_saturation())
        
    def auto_adjust_highlights(self):
        highlights_factor = self.determine_target_highlights()
        self.highlights_slider.set(highlights_factor)
        self.adjust_highlights(highlights_factor)

    def auto_adjust_shadows(self):
        shadows_factor = self.determine_target_shadows()
        self.shadows_slider.set(shadows_factor)
        self.adjust_shadows(shadows_factor)




    def calculate_image_statistics(self, image):
        """Calculer les statistiques de base (moyenne et écart-type) sur une image en niveaux de gris."""
        gray_image = image.convert("L")
        image_array = np.array(gray_image)
        mean_brightness = np.mean(image_array)
        std_brightness = np.std(image_array)
        return mean_brightness, std_brightness
    



    def determine_target_exposure(self):
        """Déterminer le facteur d'exposition en fonction de la luminosité et de la variation de l'image."""
        if not self.display_image:
            return 1.0  # Retourne un facteur neutre par défaut

        mean_brightness, std_brightness = self.calculate_image_statistics(self.display_image)

        # Ajustement basé sur la luminosité moyenne
        if mean_brightness < 50:  # Image sous-exposée
            exposure_factor = 2.0 if std_brightness < 30 else 1.8
        elif mean_brightness > 200:  # Image surexposée
            exposure_factor = 0.8 if std_brightness > 50 else 0.7
        else:  # Exposition correcte, ajustement plus précis
            exposure_factor = 1.2 if mean_brightness < 120 else 1.0

        # Appliquer l'exposition à l'image
        enhancer = ImageEnhance.Brightness(self.display_image)
        self.display_image = enhancer.enhance(exposure_factor)

        return exposure_factor

    def determine_target_contrast(self):
        """Calculer et ajuster le contraste de l'image."""
        if not self.display_image:
            return 1.0  # Retourne un facteur neutre par défaut

        mean_brightness, std_brightness = self.calculate_image_statistics(self.display_image)

        # Formule simple pour ajuster le contraste
        contrast_factor = (std_brightness / 128) + (mean_brightness / 255)

        # Retourner un facteur de contraste dans une plage raisonnable
        return np.clip(contrast_factor, 0.5, 1.5)

    def determine_target_saturation(self):
        """Calculer et ajuster la saturation de l'image."""
        if not self.display_image:
            return 1.0  # Retourne un facteur neutre par défaut

        hsv_image = self.display_image.convert('HSV')
        hsv_array = np.array(hsv_image)
        s = hsv_array[:, :, 1]  # Saturation

        # Calculer les statistiques de saturation
        mean_s = np.mean(s)
        std_s = np.std(s)

        # Formule pour ajuster la saturation
        saturation_factor = (mean_s / 255) + (std_s / (255 * np.sqrt(2 * np.pi)))

        return np.clip(saturation_factor, 0.5, 1.5)

    def determine_target_highlights(self):
        """Calculer et ajuster les hautes lumières de l'image."""
        if not self.display_image:
            return 1.0  # Retourne un facteur neutre par défaut

        mean_brightness, std_brightness = self.calculate_image_statistics(self.display_image)

        # Calculer un facteur dynamique des hautes lumières
        highlights_factor = (mean_brightness + 2 * std_brightness) / 255  # Facteur basé sur la moyenne et l'écart-type

        return np.clip(highlights_factor, 0.5, 2.0)  # Permettre des valeurs plus élevées si nécessaire

    def determine_target_shadows(self):
        """Calculer et ajuster les ombres de l'image."""
        if not self.display_image:
            return 1.0  # Retourne un facteur neutre par défaut

        mean_brightness, std_brightness = self.calculate_image_statistics(self.display_image)

        # Calculer un facteur dynamique pour ajuster les ombres
        shadows_factor = (1 - (mean_brightness - 2 * std_brightness) / 255)

        return np.clip(shadows_factor, 0.5, 1.5)