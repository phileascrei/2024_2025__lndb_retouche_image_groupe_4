# from PIL import Image, ImageEnhance
# import numpy as np

# def ajuster_exposition_dynamique(image_path):
#     # Ouvrir l'image
#     image = Image.open(image_path)

#     # Convertir l'image en mode grayscale (niveaux de gris) pour analyser l'exposition
#     image_grayscale = image.convert('L')

#     # Convertir l'image en tableau numpy pour analyser les pixels
#     image_array = np.array(image_grayscale)

#     # Calculer l'histogramme de l'image (nombre de pixels pour chaque niveau de gris)
#     histogram = np.histogram(image_array, bins=np.arange(257))[0]

#     # Calculer la luminosité moyenne
#     luminosite_moyenne = np.mean(image_array)

#     # Définir un seuil pour ajuster l'exposition
#     # Si la luminosité moyenne est faible, l'image est sous-exposée, sinon elle est bien exposée
#     if luminosite_moyenne < 128:
#         # Image sous-exposée, augmenter l'exposition
#         facteur_exposition = 1 + (128 - luminosite_moyenne) / 128
#     else:
#         # Image bien exposée ou surexposée, ajuster à la baisse si nécessaire
#         facteur_exposition = 1 - (luminosite_moyenne - 128) / 128

#     # Appliquer le facteur d'exposition
#     image_enhanced = ImageEnhance.Brightness(image).enhance(facteur_exposition)

#     return image_enhanced

# # Exemple d'utilisation
# image_path = 'test_image/tour_eiffel.jpg'  # Remplacez par le chemin de votre image

# # Appliquer l'ajustement dynamique de l'exposition
# image_ajustee = ajuster_exposition_dynamique(image_path)

# # Sauvegarder ou afficher l'image ajustée
# image_ajustee.show()  # Affiche l'image ajustée



# from PIL import Image

# # Ouvrir l'image
# im1 = Image.open("test_image/tour_eiffel.jpg")

# # Récupérer la taille de l'image
# largeur, hauteur = im1.size

# # Créer une nouvelle image pour l'image en niveaux de gris
# im2 = Image.new("RGB", (largeur, hauteur))

# # Convertir l'image en niveaux de gris
# for y in range(hauteur):
#     for x in range(largeur):
#         p = im1.getpixel((x, y))
#         # Calculer la valeur moyenne des trois canaux (R, G, B) pour obtenir une image en niveaux de gris
#         gris = (p[0] + p[1] + p[2]) // 3  # Moyenne des trois couleurs
#         im2.putpixel((x, y), (gris, gris, gris))  # Appliquer la même valeur pour R, G, et B

# # Créer une nouvelle image pour les résultats de la détection des bords
# im3 = Image.new("RGB", (largeur, hauteur))

# # Appliquer un filtre de détection des bords basique (noyau 3x3)
# for y in range(1, hauteur - 1):  # Eviter les bords
#     for x in range(1, largeur - 1):
#         # Récupérer les valeurs des pixels voisins
#         pix0 = im2.getpixel((x, y))
#         pix1 = im2.getpixel((x - 1, y - 1))
#         pix2 = im2.getpixel((x, y - 1))
#         pix3 = im2.getpixel((x + 1, y - 1))
#         pix4 = im2.getpixel((x - 1, y))
#         pix5 = im2.getpixel((x + 1, y))
#         pix6 = im2.getpixel((x - 1, y + 1))
#         pix7 = im2.getpixel((x, y + 1))
#         pix8 = im2.getpixel((x + 1, y + 1))

#         # Appliquer un noyau de détection des bords simple
#         r = 8 * pix0[0] - (pix1[0] + pix2[0] + pix3[0] + pix4[0] + pix5[0] + pix6[0] + pix7[0] + pix8[0])
#         r = r // 1  # Normaliser (vous pouvez ajuster cette étape)
#         r = r + 128  # Décaler pour ramener la valeur dans une plage valide
#         r = max(0, min(255, r))  # Limiter la valeur entre 0 et 255

#         # Appliquer la même valeur de gris pour les canaux V et B
#         v = r
#         b = r

#         # Mettre à jour l'image de sortie avec la nouvelle valeur de pixel
#         im3.putpixel((x, y), (r, v, b))

# # Afficher l'image traitée
# im3.show()



# from PIL import Image, ImageDraw
# import numpy as np

# # Charger l'image
# image = Image.open("test_image/tour_eiffel.jpg")

# # Convertir l'image en niveaux de gris
# gray_image = image.convert("L")

# # Convertir l'image en tableau numpy pour faciliter les calculs
# image_array = np.array(gray_image)

# # Définir une taille de fenêtre pour observer les variations locales
# window_size = 5

# # Initialiser les variables pour stocker le point d'intérêt
# max_variation = 0
# point_of_interest = (0, 0)

# # Parcourir l'image et observer les variations locales de luminosité
# for y in range(window_size, image_array.shape[0] - window_size):
#     for x in range(window_size, image_array.shape[1] - window_size):
#         # Obtenir une fenêtre autour du pixel actuel
#         window = image_array[y - window_size:y + window_size, x - window_size:x + window_size]
        
#         # Calculer la variation de luminosité dans la fenêtre (écart-type)
#         variation = np.std(window)
        
#         # Si la variation est plus grande que la précédente, on enregistre le point
#         if variation > max_variation:
#             max_variation = variation
#             point_of_interest = (x, y)

# # Afficher le point d'intérêt trouvé
# print("Point d'intérêt détecté à :", point_of_interest)

# # Dessiner un cercle autour du point d'intérêt sur l'image
# draw = ImageDraw.Draw(image)
# draw.ellipse((point_of_interest[0] - 10, point_of_interest[1] - 10, point_of_interest[0] + 10, point_of_interest[1] + 10), outline="red", width=3)

# # Afficher l'image modifiée
# image.show()


# import cv2
# print(cv2.__version__)









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
            self.canvas.create_image(400, 300, image=img_tk)  # Centrer l'image
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
