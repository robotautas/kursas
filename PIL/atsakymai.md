### 1

```python
from PIL import Image

im = Image.open("logo.png")
box = (0, 28, 128, 100)
region = im.crop(box)
region.save('logo_cropped.png')
```

### 2

```python
from PIL import Image, ImageEnhance
import os

def enhance_image(pic, contrast, color, sharpness, brightness, save=False):
    im = Image.open(pic)
    enh = ImageEnhance.Contrast(im)
    im = enh.enhance(contrast)
    enh = ImageEnhance.Color(im)
    im = enh.enhance(color)
    enh = ImageEnhance.Brightness(im)
    im = enh.enhance(brightness)
    enh = ImageEnhance.Sharpness(im)
    im = enh.enhance(sharpness)
    if save:
        loc = os.path.splitext(pic)[0]
        ext = os.path.splitext(pic)[1]
        im.save(f'{loc}_modified{ext}')
    im.show()

enhance_image('dog.jpg', 2, 0, 5, 1, True)
```

### 3

```python
from PIL import Image
import os

def get_list(folder):
    files = os.listdir(folder)
    images = []
    for i in files:
        if i.endswith(('.jpg', '.png')):
           images.append(folder+'/'+i) 
    return images

def pic_resize(pic, height):
    im = Image.open(pic)
    width = round(im.size[1]/im.size[0]*height)
    im = im.resize((height, width))
    return im

def optimize_images(folder, height):
    os.mkdir(f'{folder}/optimized')
    logo = Image.open('logo_cropped.png')
    pic_num = 0
    for i in get_list(folder):
        pic = Image.open(i)
        pic = pic_resize(i, height)
        logo_location = (
            pic.size[0]-logo.size[0],
            pic.size[1]-logo.size[1], 
            pic.size[0], 
            pic.size[1])
        pic.paste(logo, logo_location, logo)
        pic_num += 1
        pic.save(f'{folder}/optimized/picture_{pic_num}.png')
```

### 4

```python
def ribos(sk):
    if sk < 0:
        return 0
    elif sk > 255:
        return 255
    return sk


def adjust_colors(img, r, g, b):
    img = Image.open(img)
    data = img.getdata()
    new_data = []
    for pixel in data:
        red = ribos(pixel[0] + r)
        green = ribos(pixel[1] + g)
        blue = ribos(pixel[2] + b)
        new_pixel = (red, green, blue)
        new_data.append(new_pixel)
    
    img.putdata(new_data)
    return img

new_img = adjust_colors('dog.jpg', 0, 0 , +80)
new_img.show()
```

### 5

```python
def turn_binary(img, r, g, b):
    img = Image.open(img)
    data = img.getdata()
    new_data = []
    black = 0, 0, 0
    white = 255, 255, 255
    for pixel in data:
        if pixel[0] >= r or pixel[1] >= g or pixel[2] >= b:
            new_data.append(black)
        else:
            new_data.append(white)
    
    img.putdata(new_data)
    return img

image = turn_binary('dog.jpg', 255, 255, 8)
image.show()
```