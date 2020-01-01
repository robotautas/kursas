import json

with open('uzduotis.json', 'r') as f:
    data = json.load(f)

color_list = []
for item in data['colors']:
    new_format = {}
    color = item['color']
    rgba_list = item['code']['rgba']
    rgb = ''.join(str(rgba_list))[1:-4]
    hexx = item['code']['hex']
    new_format.update({'color': color, 'rgb': rgb, 'hex': hexx})
    color_list.append(new_format)


new_dict = {'colors': color_list}
with open('uzduotis_ivykdyta.json', 'w') as file:
    json.dump(new_dict, file, indent=2)

