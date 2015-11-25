import sys, os, ast, json
import numpy as np
from netCDF4 import Dataset


class netcdf(object):
	def __init__(self):
		self.data_dir = '../data/'
	
	def aggregate_coords_data(self):
		"""
		THE PURPOSE OF THIS METHOD IS TO ITERATE OVER ALL THE DATASET AND AGGREGATE
		THE DATA FOR EACH OF THE AVAILABLE COORDINATES AND SAVE THEM IF POSSIBLE. 
		THIS WAY, WE WILL HAVE DATA READILY AVAILABLE FOR OUR WEB APP AND WE WONT 
		HAVE TO DEAL WITH ONLINE NETCDF4 READING AND ALL OTHER RELATED CRAP.
		"""
		for root, directories, files in os.walk(self.data_dir):
			for filename in files:
				splitted = filename.split('.')
				if len(splitted) > 1 and splitted[1] == 'nc4':
					print filename
					filepath = os.path.join(root, filename)
					self.read_data(filepath)
		return
	

	def read_data(self, filepath):
		df = Dataset(filepath, 'r')
		print df.variables.keys()
		# Extract data from NetCDF file
		lats = df.variables['lat'][:]  # extract/copy the data
		lons = df.variables['lon'][:]
		time = df.variables['time'][:]
		tas = df.variables['tas'][]  # shape is time, lat, lon as shown above
		


if __name__ == '__main__':
	obj = netcdf()
	obj.aggregate_coords_data()
		
		


