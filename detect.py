from PIL import Image, ImageDraw
from sample_analysis import *
from ast import literal_eval
from os import listdir
import csv
with open("data/cbcr_histo3.csv", newline='') as f:
	datareader = csv.reader(f)
	cbcr_data = Counter({literal_eval(row[0]): int(row[1]) for row in datareader})
	
def skin_detect(img, tolerance=60, highlight=(255,255,255), dimlight=(0,0,0), exclude=False):
	skin = [cbcr[0] for cbcr in cbcr_data.most_common()[:tolerance]]
	w,h = img.size
	pix = img.load()
	detected = []
	for x in range(w):
		for y in range(h):
			if rgb_to_ycbcr(pix[x,y])[1:3] in skin:
				pix[x,y] = highlight
				detected.append((x,y))
			elif exclude:
				pix[x,y] = dimlight
	return detected
	
if __name__ == '__main__':
	tests = listdir("groups/")
	if "Thumbs.db" in tests:
		tests.remove("Thumbs.db")
	for name in tests:
	#name = "2008dec.png"
		test = Image.open("groups/%s"%name)
		print(test.size)
		detected = skin_detect(test, exclude=True)
		test.save("results/%s"%name)