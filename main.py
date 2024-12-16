import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

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
        self.adjustment_frame.pack(side=tk.LEFT, padx=5, pady=5)

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

if __name__ == "__main__":
    app = ImageEditor()
    app.mainloop()



""" TEST AUTOMATISATIONS"""
# from PIL import Image, ImageEnhance
# import numpy as np

# def calculate_brightness_and_contrast(img):
#     # Convertir l'image en un tableau numpy (matrice)
#     img_array = np.array(img)

#     # Calculer la luminosité moyenne (moyenne des valeurs RVB)
#     brightness = np.mean(img_array)

#     # Calculer l'écart-type (mesure de la dispersion, donc du contraste)
#     contrast = np.std(img_array)

#     return brightness, contrast

# def auto_enhance(image_path):
#     # Ouvrir l'image
#     img = Image.open(image_path)

#     # Calculer la luminosité et le contraste
#     brightness, contrast = calculate_brightness_and_contrast(img)

#     # Ajuster le facteur de luminosité
#     # On utilise un facteur ajusté en fonction de la luminosité, avec des limites plus souples
#     brightness_target = 128  # Cible pour la luminosité (valeur neutre)
#     brightness_factor = (brightness_target / brightness)  # Applique un ajustement linéaire

#     # Ajuster le facteur de contraste
#     # Si l'écart-type est faible, on l'augmente proportionnellement
#     contrast_target = 50  # Valeur cible pour un bon contraste moyen (tu peux tester cette valeur)
#     contrast_factor = contrast_target / contrast if contrast > contrast_target else 1.5

#     # Appliquer l'ajustement de la luminosité et du contraste
#     enhancer_brightness = ImageEnhance.Brightness(img)
#     img_brightness = enhancer_brightness.enhance(brightness_factor)

#     enhancer_contrast = ImageEnhance.Contrast(img_brightness)
#     img_enhanced = enhancer_contrast.enhance(contrast_factor)

#     # Afficher l'image améliorée
#     img_enhanced.show()

# # Exemple d'utilisation
# auto_enhance("test_image/image_sousexposee.jpg")

