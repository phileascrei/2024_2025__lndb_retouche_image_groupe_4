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



# from PIL import Image, ImageOps
# import numpy as np

# # Ouvrir l'image en couleur
# image = Image.open("test_image/image_sousexposee_leger.jpg")

# # Convertir l'image en mode RGB (si ce n'est pas déjà fait)
# image_rgb = image.convert('RGB')

# # Séparer les canaux R, G, B
# r, g, b = image_rgb.split()

# # Appliquer l'égalisation sur chaque canal
# r_eq = ImageOps.equalize(r)
# g_eq = ImageOps.equalize(g)
# b_eq = ImageOps.equalize(b)

# # Recomposer l'image avec les canaux égalisés
# image_equalized = Image.merge('RGB', (r_eq, g_eq, b_eq))

# # Afficher l'image égalisée
# image_equalized.show()



# from PIL import Image
# import numpy as np
# import matplotlib.pyplot as plt

# def apply_clahe(image, clip_limit=3.0, tile_grid_size=(8, 8)):
#     """
#     Applique une égalisation d'histogramme localisée sur une image (similaire à CLAHE).

#     :param image: Image PIL (en mode 'RGB' ou 'L')
#     :param clip_limit: Limite de contraste pour l'égalisation (plus élevé = plus de contraste)
#     :param tile_grid_size: Taille des blocs pour l'égalisation locale
#     :return: Image après égalisation d'histogramme localisée
#     """
#     # Convertir l'image PIL en tableau numpy
#     image_np = np.array(image)
    
#     # Taille des blocs
#     block_height, block_width = tile_grid_size
    
#     # Fonction d'égalisation d'un bloc d'image
#     def equalize_block(block):
#         """
#         Egalisation d'histogramme d'un bloc d'image.
#         """
#         # Calculer l'histogramme du bloc
#         hist, bins = np.histogram(block.flatten(), bins=256, range=(0, 255))
        
#         # Calculer la fonction de distribution cumulée (CDF)
#         cdf = np.cumsum(hist)
#         cdf = np.ma.masked_equal(cdf, 0)  # Masquer les valeurs égales à 0
#         cdf = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())  # Normaliser la CDF
        
#         # Appliquer l'égalisation
#         block_equalized = np.interp(block.flatten(), bins[:-1], cdf)
        
#         # Remettre l'image dans sa forme d'origine
#         return block_equalized.reshape(block.shape)
    
#     # Appliquer l'égalisation locale sur chaque bloc
#     for y in range(0, image_np.shape[0], block_height):
#         for x in range(0, image_np.shape[1], block_width):
#             block = image_np[y:y + block_height, x:x + block_width]
#             image_np[y:y + block_height, x:x + block_width] = equalize_block(block)
    
#     # Retourner l'image après traitement
#     return Image.fromarray(image_np.astype(np.uint8))

# # Chargement de l'image
# image = Image.open("test_image/image_surexposee.png")

# # Appliquer CLAHE sur l'image
# image_clahe = apply_clahe(image, clip_limit=3.0, tile_grid_size=(8, 8))

# # Afficher l'image originale et l'image après CLAHE
# fig, ax = plt.subplots(1, 2, figsize=(10, 5))

# # Afficher l'image originale
# ax[0].imshow(image)
# ax[0].set_title('Image Originale')
# ax[0].axis('off')

# # Afficher l'image après CLAHE
# ax[1].imshow(image_clahe)
# ax[1].set_title('Image après CLAHE')
# ax[1].axis('off')

# plt.show()

import cv2
print(cv2.__version__())