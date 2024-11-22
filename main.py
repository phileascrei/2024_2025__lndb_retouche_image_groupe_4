# from tools import *

# a = Image.open('tour_eiffel.jpg')



# a.convert(mode="L")

# # Récupérer tous les pixels de l'image en niveaux de gris
# pixels = list(a.getdata())
    
#     # Calculer la moyenne des valeurs des pixels (luminosité)
# moyenne = sum(pixels) / len(pixels)
    
# print(moyenne)





from PIL import Image
from tools import *

def moyenne_luminosite(image_path):
    """
    Calcule la moyenne de luminosité des pixels d'une image.
    La luminosité est calculée même si l'image est en couleur, en utilisant la conversion en niveaux de gris.
    
    :param image_path: Chemin de l'image.
    :return: Moyenne de luminosité (float).
    """
    # Charger l'image
    image = Image.open(image_path)
    
    # S'assurer que l'image est bien en niveaux de gris (L pour luminosité)
    grayscale_image = image.convert("L")
    
    # Récupérer tous les pixels de l'image en niveaux de gris
    pixels = grayscale_image.getdata()
    
    # Vérifier que chaque pixel est un entier
    if isinstance(pixels[0], tuple):
        raise ValueError("L'image semble être en mode couleur ou incompatible avec la conversion en niveaux de gris.")

    # Calculer la moyenne des valeurs des pixels (luminosité)
    moyenne = sum(pixels) / len(pixels)
    
    return moyenne


# image_path = "test_image/tour_eiffel.jpg"  # Remplacez par le chemin correct de votre image
# print(moyenne_luminosite(image_path))  # Cela affichera la valeur complète (ex. 123.456789)

# put_in_highlight_gray(image_path).show()

