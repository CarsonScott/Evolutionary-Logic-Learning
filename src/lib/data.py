import pickle
import sys
import io
import os

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
	return pickle.load(b)
