from PIL import Image

im = Image.open("logo.png")
box = (0, 28, 128, 100)
region = im.crop(box)
region.save('logo_cropped.png')
