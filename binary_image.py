import bitstring
from PIL import Image
import math

path = "/home/kuba/Pobrane/PortRptr.exe"

binary_data = bitstring.BitArray(filename=path).bin[2:]
bytes_data = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]

pixel_value = []

for i in bytes_data:
    pixel_value.append(int(i, 2))

amount_of_pixels = math.sqrt(len(pixel_value))
image_width_height = round(amount_of_pixels) - 1

img = Image.new('RGB', (image_width_height, image_width_height), "black")
pixels = img.load()

iteration = 0

for i in range(img.size[0]):
    for j in range(img.size[1]):
        pixels[i, j] = (pixel_value[iteration], pixel_value[iteration], pixel_value[iteration])
        iteration += 1

img.show()

