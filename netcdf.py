import sys, os, ast, json
import numpy as np
from netCDF4 import Dataset, num2date

from location_data.raw_locations import raw_locations

class netcdf(object):
	def __init__(self):
		self.data_dir = '../location_data/data/'
		self.coordinates_file = 'location_data/locations_R1.json' 
		self.coordinates = self.read_coordinates()

	def convert_raw_locs(self):
		self.code_map = {}
		for each in raw_locations:
			name = each['name'].replace('County', '').replace('Municipio', '')
			self.code_map [name] = each['code']
		return

	def aggregate_coords_data(self):
		"""
		THE PURPOSE OF THIS METHOD IS TO ITERATE OVER ALL THE DATASET AND AGGREGATE
		THE DATA FOR EACH OF THE AVAILABLE COORDINATES AND SAVE THEM IF POSSIBLE. 
		THIS WAY, WE WILL HAVE DATA READILY AVAILABLE FOR OUR WEB APP AND WE WONT 
		HAVE TO DEAL WITH ONLINE NETCDF4 READING AND ALL OTHER RELATED CRAP.
		"""
		variables = {'solarradiation': 'SolarRadiation', 'airtemperature': 'AirTemperature'}
		for root, directories, files in os.walk(self.data_dir):
			for filename in files:
				splitted = filename.split('.')
				if len(splitted) > 1 and splitted[1] == 'nc':
					var_name = variables[filename.split('2')[0]]
					filepath = os.path.join(root, filename)
					self.read_data(filepath, var_name, filename.split('nc')[0].strip('.'))
		self.save_data()
		return

	def save_data(self):
		f = open('location_data/data_final.json', 'wb')
		f.write(json.dumps(self.coordinates))
		f.close()
		return

	def near(self, array,value):
		idx=(np.abs(array-value)).argmin()
		return idx

	def read_coordinates(self):
		coordinates = []
		f = open(self.coordinates_file, 'rb')
		for a in f:
			coordinates.append(a)
		f.close()
		coordinates = ast.literal_eval(coordinates[0])
		return coordinates

	def read_data(self, filepath, vname, filename):
		for loc in self.coordinates:
			loni = loc['lon']
			lati = loc['lat']

			nc = Dataset(filepath, 'r')
			lat = nc.variables['latitude'][:]
			lon = nc.variables['longitude'][:]
			times = nc.variables['time'][:]

			ix = self.near(lon, loni)
			iy = self.near(lat, lati)

			var = nc.variables[vname]
			h = var[:,iy,ix]
			points = []
			for _, i in enumerate(h):
				p = np.isnan(float(i))
				if not p:
					points.append(float(i))
				else:
					points.append(0)

			loc[filename] = points
			loc['code'] = self.code_map[loc['name']]


if __name__ == '__main__':
	obj = netcdf()
	obj.convert_raw_locs()
	obj.aggregate_coords_data()
