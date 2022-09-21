import os, sys
import shutil
import json
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET


config_json = "config.json"

config = {}
with open(config_json) as cj:
	config = json.load(cj)

chart_label=config['chart-title']
class_folder = config['annotation-folder']
all_boxess = []


def getting_bbox_value_from_xml(xml_path):
	bboxes = []
	tree = ET.parse(xml_path)
	root = tree.getroot()
	for member in root.findall('object'):
		xmin, ymin, xmax, ymax = int(member[4][0].text), int(member[4][1].text), int(member[4][2].text), int(member[4][3].text)
		bboxes.append([member[0].text, xmin, ymin, xmax, ymax])
	return bboxes

def class_lable_count(bboxes, lables = {}):
	for box in bboxes:
		class_name = box[0]
		if class_name not in lables:
			lables[class_name] = 0
		lables[class_name] += 1
	return lables

def display_bar_chart(lables_count):
	# lables_count.update({'A': 10, 'B': 20})
	x_axies = list(lables_count.keys())
	y_axies = list(lables_count.values())

	# Normal Bar chart
	# fig = plt.figure(figsize = (10, 5))
	# plt.bar(x_axies, y_axies,  width = 0.4)
	# plt.xlabel("Class Names") 
	# plt.ylabel("Count of class") 
	# plt.title("List of class with count") 
	# plt.show()

	fig, ax = plt.subplots(figsize =(16, 9))
	ax.barh(x_axies, y_axies)
	for s in ['top', 'bottom', 'left', 'right']:
		ax.spines[s].set_visible(False)
	ax.xaxis.set_ticks_position('none') 
	ax.yaxis.set_ticks_position('none') 
	ax.xaxis.set_tick_params(pad = 5) 
	ax.yaxis.set_tick_params(pad = 10)
	ax.grid(b = True, color ='grey', 
        linestyle ='-.', linewidth = 0.5, 
        alpha = 0.2) 
  
	# Show top values  
	ax.invert_yaxis() 
	  
	# Add annotation to bars 
	for i in ax.patches: 
	    plt.text(i.get_width()+0.2, i.get_y()+0.5,  
	             str(round((i.get_width()), 2)), 
	             fontsize = 10, fontweight ='bold', 
	             color ='grey') 
	  
	# Add Plot Title 
	ax.set_title(chart_label,
	             loc ='center', ) 
	  
	# Show Plot 
	plt.show() 


def main():
	try:
		annotation_files = [os.path.join(class_folder, xml_file) for xml_file in os.listdir(class_folder) if xml_file.endswith('.xml')]
	except FileNotFoundError as ex:
		print(f"[ERROR] Folder {class_folder} doesn't exists")
		sys.exit()
	except Exception as ex:
		print(str(ex))
		sys.exit()


	lables = {}
	for xml_file in annotation_files:
		print(f"[INFO] Processing {xml_file} file")
		try:
			bboxes = getting_bbox_value_from_xml(xml_file)
			all_boxess.extend(bboxes)
			lables = class_lable_count(bboxes, lables)
		except Exception as ex:
			print(f"[ERROR] File {xml_file} error")
	print(lables)
	display_bar_chart(lables)

if __name__ == '__main__':
	main()