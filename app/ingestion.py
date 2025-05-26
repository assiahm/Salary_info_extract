import os
from pdf2image import convert_from_path
from PIL import Image

def load_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.pdf']:
        images = convert_from_path(file_path)
        return images
    elif ext in ['.jpg', '.jpeg', '.png']:
        return [Image.open(file_path)]
    else:
        raise ValueError("Unsupported file type")