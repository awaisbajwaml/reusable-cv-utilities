import os
import sys
import json
from PIL import Image
from hurry.filesize import size


config_path = "config.json"

config_details = {}
with open(config_path) as config:
	config_details = json.load(config)

# print(config_details)

images_path = config_details['directory_path']
image_exts = config_details['image_ext']
images_list = []
images_size = []
images_width = []
images_height = []
for file_path in os.listdir(images_path):
	name, ext = os.path.splitext(file_path)
	if ext in image_exts:
		path = os.path.join(images_path, file_path)
		image = Image.open(path)
		images_list.append(path)
		file_size = os.path.getsize(path)
		images_size.append(file_size)
		width, height = image.size
		images_width.append(width)
		images_height.append(height)

print("==="*10)
print(f"No of images {len(images_list)}")
print(f"The average of image size is {size(sum(images_size)/len(images_list))}")
print(f"The average of image width is {sum(images_width)/len(images_list)}")
print(f"The average of image height is {sum(images_height)/len(images_list)}")