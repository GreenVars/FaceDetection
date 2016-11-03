# http://web.stanford.edu/class/ee368/Project_03/Project/reports/ee368group02.pdf
# http://www.cs.columbia.edu/CAVE/databases/pubfig/
# Analyse Samples
from os import listdir
from collections import Counter
from PIL import Image, ImageDraw
import csv
def rgb_to_ycbcr(rgb):
	return (int(.299*rgb[0]+.587*rgb[1]+.114*rgb[2]),
			int(-.169*rgb[0]-.332*rgb[1]+.5*rgb[2]),
			int(.5*rgb[0]-.419*rgb[1]-.081*rgb[2]))
			
def pixel_list(img):
	w,h = v.size
	pix = v.load()
	return [pix[x,y] for x in range(w) for y in range(h) if pix[x,y][3]]
	
def ycbcr_data(pixels):
	return [rgb_to_ycbcr(p) for p in pixels]
	
def stripped_counter(count, strip=False, threshold=4):
	h = Counter(count)
	if strip:
		for k in list(h):
			if h[k] < threshold:
				del h[k]
	return h
faces = listdir("training/")
if 'Thumbs.db' in faces:
	faces.remove('Thumbs.db')
samples = {pic: Image.open("training/"+pic) for pic in faces}
if __name__ == '__main__':
	pixels = []
	for v in samples.values():
		pixels.extend(pixel_list(v))
	colors = ycbcr_data(pixels)
	histo = stripped_counter(colors,strip=True)
	y_histo = Counter([c[0] for c in colors])
	cb_histo = Counter([c[1] for c in colors])
	cr_histo = Counter([c[2] for c in colors])
	cbcr_histo = Counter([(c[1],c[2]) for c in colors])
	# WRITE HISTO DATA TO CSV
	
	with open("cb_histo3.csv", 'w',newline='') as fp:
		a = csv.writer(fp, delimiter=',')
		a.writerows(cb_histo.most_common())
	with open("cr_histo3.csv", 'w',newline='') as fp:
		a = csv.writer(fp, delimiter=',')
		a.writerows(cr_histo.most_common())
	with open("cbcr_histo3.csv", 'w',newline='') as fp:
		a = csv.writer(fp, delimiter=',')
		a.writerows(cbcr_histo.most_common())
		
	# PLOT CBCR DATA
	plot = Image.new("RGB", (201,201), "white")
	points = plot.load()
	draw = ImageDraw.Draw(plot)
	for k,v in cbcr_histo.items():
		point = (101 + k[1],101 - k[0])
		m = max(cbcr_histo.values())*10//v
		if m >= 255: m = 250
		color = ((m),)*3
		try:
			points[point] = color
		except:
			pass
	draw.line([(101,0),(101,201)], fill=(0,0,0))
	draw.line([(0,101),(201,101)], fill=(0,0,0))