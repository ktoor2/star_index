import cv2
import pickle
from pathlib import Path
import os


"""
Functions to get histogram related details
Author: Kunwar Singh
"""

def getBaseImage():
	pickle_file_path = '/Users/okt/Desktop/my_project/scripts/baseimage'
	pickle_filename = 'baseimagehistogram.p'
	imagename = 'baseimage.jpg'

	'''
	check if pickle file already exists. If yes, send back the result
	'''

	pickle_file = os.path.join(pickle_file_path, pickle_filename)
	print("inside the hist function")
	if os.path.isfile(pickle_file):
		baseimagehistogram = pickle.load(open(pickle_file,'rb'))
		return baseimagehistogram

	'''
	file doesn't exist. get the histogram store it and return it
	'''

	image = cv2.imread(os.path.join(pickle_file_path, imagename))

	hist = cv2.calcHist([image], [0,1,2], None, [8, 8, 8],
		[0, 256, 0, 256, 0, 256])

	hist = cv2.normalize(hist, hist).flatten()
	print("creating new pickle file")
	pickle.dump(hist, open(pickle_file,'wb'))
	return hist



def getCorrelation(path, tag_dict = None):
	"""
	Generates a correlation value between baseimage and path image. Returns tag_dict or the correlation
	"""
	base_histogram = getBaseImage()

	ref_image = cv2.imread(path)
	histogram = cv2.calcHist([ref_image], [0, 1, 2], None, [8, 8, 8],
		[0, 256, 0, 256, 0, 256])
	histogram = cv2.normalize(histogram, histogram).flatten()

	'''
	compare the histogram of images using correlation. Higher the correlation, better the similarity
	'''

	d = cv2.compareHist(base_histogram, histogram, cv2.HISTCMP_CORREL)
	if tag_dict != None:
		tag_dict['correlation'] = d
		return tag_dict

	else:
		return d






