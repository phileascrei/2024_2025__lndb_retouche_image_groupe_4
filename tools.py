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
            self.display_image = self.original_image.resize(
                (int(self.original_image.width * self.zoom_factor), int(self.original_image.height * self.zoom_factor)),
                Image.Resampling.LANCZOS
            )
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

    def reset_sliders(self):
        self.exposure_slider.set(1.00)
        self.contrast_slider.set(1.00)
        self.saturation_slider.set(0.00)
        self.highlights_slider.set(1.00)
        self.shadows_slider.set(1.00)





    def adjust_exposure(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Brightness(self.original_image)
            self.display_image = enhancer.enhance(float(value))
            self.display_on_canvas()

    def adjust_contrast(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Contrast(self.original_image)
            self.display_image = enhancer.enhance(float(value))
            self.display_on_canvas()

    def adjust_saturation(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Color(self.original_image)
            self.display_image = enhancer.enhance(float(value) + 1)  # Décalage pour éviter des valeurs négatives
            self.display_on_canvas()

    def adjust_highlights(self, value):
        if self.original_image:
            img = np.array(self.original_image.convert("RGB"), dtype=np.float32) / 255.0
            img[:, :, 0:3] = np.clip(img[:, :, 0:3] * float(value), 0, 1)
            self.display_image = Image.fromarray((img * 255).astype(np.uint8))
            self.display_on_canvas()

    def adjust_shadows(self, value):
        if self.original_image:
            img = np.array(self.original_image.convert("RGB"), dtype=np.float32) / 255.0
            shadows_mask = img < 0.5  # On cible les basses lumières
            img[shadows_mask] = np.clip(img[shadows_mask] * float(value), 0, 1)
            self.display_image = Image.fromarray((img * 255).astype(np.uint8))
            self.display_on_canvas()






    def auto_adjust_exposure(self):
        self.adjust_exposure(self.determine_target_exposure())

    def auto_adjust_contrast(self):
        pass

    def auto_adjust_saturation(self):
        self.adjust_saturation(self.determine_target_saturation())

    def auto_adjust_highlights(self):
        pass

    def auto_adjust_shadows(self):
        pass






    def determine_target_exposure(self):
        if not self.original_image:
            return 1.0  # Retourne un facteur neutre par défaut

        # Convertir l'image en niveaux de gris
        gray_image = self.original_image.convert("L")
        image_array = np.array(gray_image)

        # Calculer la moyenne de la luminosité
        mean_brightness = np.mean(image_array)
        std_brightness = np.std(image_array)  # Écart-type pour voir la variation des niveaux de lumière

        # Analyse de l'exposition en fonction des seuils
        if mean_brightness < 50:  # Photo sous-exposée (très sombre, souvent de nuit)
            exposure_factor = 1.8 if std_brightness < 30 else 1.5  # Plus homogène = boost plus fort
        elif mean_brightness > 200:  # Photo surexposée (très claire, en plein soleil)
            exposure_factor = 0.7 if std_brightness > 50 else 0.8
        else:
            exposure_factor = 1.2 if mean_brightness < 120 else 0.9  # Ajustement fin

        # Appliquer automatiquement l'ajustement
        self.exposure_slider.set(exposure_factor)
        enhancer = ImageEnhance.Brightness(self.original_image)
        self.display_image = enhancer.enhance(exposure_factor)
        self.display_on_canvas()

        return exposure_factor  # Retourne la valeur appliquée pour information

    def determine_target_contrast(self):
        pass
    
    def determine_target_saturation(self):
        # Convertir l'image en mode HSV
        hsv_image = self.original_image.convert('HSV')
        hsv_array = np.array(hsv_image)

        # Extraire les composantes H, S, et V
        h, s, v = hsv_array[:, :, 0], hsv_array[:, :, 1], hsv_array[:, :, 2]

        # Calculer les statistiques nécessaires sur la saturation
        mean_s = np.mean(s)          # Moyenne de la saturation
        std_s = np.std(s)            # Écart-type de la saturation
        variance_s = np.var(s)       # Variance de la saturation

        # Calculer une formule mathématique pour obtenir un facteur de saturation
        # Formule simplifiée pour déterminer un ajustement dynamique basé sur les statistiques
        saturation_factor = (mean_s / 255) + (std_s / (255 * np.sqrt(2 * np.pi)))  # Ajustement par écart-type normalisé

        # Appliquer un calcul pour obtenir un facteur dans une plage acceptable
        saturation_factor = np.clip(saturation_factor, 0.5, 1.5)  # Assurer un facteur raisonnable

        # Retourner le facteur de saturation calculé
        return saturation_factor

    def determine_target_highlights(self):
        pass

    def determine_target_shadows(self):
        pass