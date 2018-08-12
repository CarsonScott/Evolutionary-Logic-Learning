import pickle
import sys
import io
import os

def get_filenames(path):
	return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
def save(data, file):
	filename, extension = os.path.splitext(file)
	extension = '.bin'
	if extension == '':extension = ext
	b = io.FileIO(filename+extension, 'wb')
	pickle.dump(data, b)
def load(file, ext='.bin'):
	filename, extension = os.path.splitext(file)
	extension = '.bin'
	b = io.FileIO(filename+extension, 'rb')
	print(b)
	return pickle.load(b)
