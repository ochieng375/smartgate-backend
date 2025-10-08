from pyzbar.pyzbar import decode
from PIL import Image

def decode_barcode(image_path):
    image = Image.open(image_path)
    result = decode(image)
    return result[0].data.decode("utf-8") if result else None
