from PIL import Image, ImageFilter, ImageEnhance

dog = Image.open('dog.jpg')
enh = ImageEnhance.Color(dog)
enh.enhance(0.2).save('test.png')