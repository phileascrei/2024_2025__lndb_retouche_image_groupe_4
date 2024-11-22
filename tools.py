from PIL import Image

def analyse_exposition (image) :
    pass

def analyse_contrast (image) :
    pass 

def analyse_saturation (image) : 
    pass

def put_in_highlight_gray (image) : # converti une image de couleur en une image en valeur de gris

    image = Image.open(image)
    image = image.convert("L")
    
    return image

def get_average_gray_value (gray_image) :
    pass

def is_in_highlight_gray (image) : 
    image = Image.open(image)

    if image.mode == "L" :
        return True
    else :
        return False
