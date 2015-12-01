import sys, os, ast, json, gc
import numpy as np
from netCDF4 import Dataset, num2date
import pylab as pl
import matplotlib.pyplot as plt


class netcdf(object):
	def __init__(self):
		self.data_dir = '../location_data/'
		self.coordinates_file = 'location_data/locations_R1.json' 
		self.coordinates = self.read_coordinates()

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
					print filename
					var_name = variables[filename.split('_')[0]]
					filepath = os.path.join(root, filename)
					self.read_data(filepath, var_name)
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

	def read_data(self, filepath, vname):
		
		for loc in self.coordinates:
			loni = loc['lon']
			lati = loc['lat']

			#loni = -97.69
			#lati = 31.85

			nc = Dataset(filepath, 'r')
			lat = nc.variables['latitude'][:]
			lon = nc.variables['longitude'][:]

			times = nc.variables['time']

			ix = self.near(lon, loni)
			iy = self.near(lat, lati)

			#vname = 'AirTemperature'
			var = nc.variables[vname]
			h = var[:,iy,ix]
			points = []
			for _, i in enumerate(h):
				p = np.isnan(float(i))
				if not p:
					#print float(i), loc['name']
					points.append(float(i))
				else:
					print loc['name'], p
					points.append(0) 
			loc[vname] = points
		return
				
		"""
			# for u in i.data:
			# 	#u = list(u)
			# 	#print filter(lambda n: n != -9999.0, u)
		"""
		
		
		# df = Dataset(filepath, 'r')
		# temp = df.variables['AirTemperature']
		# for i in range(len(temp)):
		# 	pl.clf()
		# 	pl.contourf(temp[i])
		# 	pl.show()

		"""
		df = Dataset(filepath, 'r')

		# Extract data from NetCDF file
		lat = df.variables['latitude'][:]
		lon = df.variables['longitude'][:]
		temp = df.variables['AirTemperature'][:,:,:]
			
		lat_idx = np.where(lat==lat[20])[0][0]
		lon_idx = np.where(lon==lon[12])[0][0]
		tmp_crd = temp[:,lat_idx,lon_idx]
		print set(tmp_crd.data)
		"""
		

if __name__ == '__main__':
	obj = netcdf()
	obj.aggregate_coords_data()

		
		

	


