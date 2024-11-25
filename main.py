from PIL import Image, ImageOps
from tools import *
import matplotlib.pyplot as plt
import numpy as np


# image_path = "test_image/tour_eiffel.jpg"  # Remplacez par le chemin correct de votre image
# print(moyenne_luminosite(image_path))  # Cela affichera la valeur complète (ex. 123.456789)

# image_path = put_in_highlight_gray(image_path)


# histogram = image_path.histogram()

# plt.bar(range(256), histogram, width=1.0, color='black')
# plt.title("Histogramme des pixels")
# plt.xlabel("Valeur des pixels (0-255)")
# plt.ylabel("Fréquence")
# plt.show()

# image_path = "test_image/image_surexposee.png"

# # Charger l'image avec Pillow
# image = Image.open(image_path)

# # Si vous souhaitez un histogramme en niveaux de gris, convertissez l'image en mode "L" (niveau de gris)
# image_gray = image.convert("L")

# # Obtenez l'histogramme des pixels
# histogram = image_gray.histogram()
# image.show()
# # Affichage de l'histogramme avec matplotlib
# plt.bar(range(256), histogram, width=1.0, color='black')
# plt.title("Histogramme des pixels")
# plt.xlabel("Valeur des pixels (0-255)")
# plt.ylabel("Fréquence")
# plt.show()

# im = Image.open("test_image/image_surexposee.png")
# image = Image.open("test_image/image_surexposee.png").convert('L')  # Convertir en niveaux de gris
# pixels = np.array(image)

# # Calcul de la médiane
# median_value = np.median(pixels)
# print(f"Médiane des gris : {median_value}")




# image_equalized = ImageOps.equalize(image)

# # Afficher ou sauvegarder l'image égalisée
# image_equalized.show()



from PIL import Image, ImageOps
import numpy as np

# Ouvrir l'image en couleur
image = Image.open("test_image/tour_eiffel.jpg")

# Convertir l'image en mode RGB (si ce n'est pas déjà fait)
image_rgb = image.convert('RGB')

# Séparer les canaux R, G, B
r, g, b = image_rgb.split()

# Appliquer l'égalisation sur chaque canal
r_eq = ImageOps.equalize(r)
g_eq = ImageOps.equalize(g)
b_eq = ImageOps.equalize(b)

# Recomposer l'image avec les canaux égalisés
image_equalized = Image.merge('RGB', (r_eq, g_eq, b_eq))

# Afficher l'image égalisée
image_equalized.show()
