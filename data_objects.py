import sys, os, ast
from bson import ObjectId
from mongo_ import establish_connection

from time import time as tm

from module_specs import module_globals, modules

class heatmap_object(object):
	def __init__(self, object_):
		self.type_ = object_['type_']
		self.pv = modules[object_['pv_panel_selected']]
		self.year_window_selected = object_['year_window_selected']
		self.month_selected = int(object_['month_selected'])

	def get_month_data(self):
		t1 = tm()
		keys = map(lambda p: p+self.year_window_selected, ['solarradiation', 'airtemperature'])
		client = establish_connection()
		res = client.test_.ren_project_data.find(
				{'key': { '$in': keys } }, 
				{ 'data': { '$slice': [self.month_selected-1,  1] } }
			)
		data = self.map_([each for each in res], keys).values()
		client.close()
		t2 = tm()
		print t2 - t1
		return data

	def map_(self, data, keys):
		mapped = {}
		for each in data:
			id_ = each['code']
			key = each['key']
			if id_ in mapped:
				mapped[id_][key] = each['data'][0]
				for i in each:
					if i != 'data':
						mapped[id_][i] = each[i]
			else:
				mapped[id_] = {}
				mapped[id_][key] = each['data'][0]
				for i in each:
					if i != 'data':
						mapped[id_][i] = each[i]
			if len(mapped[id_]) == 9:
				solar_radiation = mapped[id_][keys[0]]
				air_temperature = mapped[id_][keys[1]]
				tcell = air_temperature + (module_globals['gamma'] * (solar_radiation/1000))
				voc = self.pv['rated_voc'] * (1 - 0.0037 * (tcell - self.pv['rated_tcell']))
				pmax = self.pv['rated_power'] * (1 - 0.005 * (tcell - self.pv['rated_tcell']))
				isc = self.pv['rated_isc'] * (1 - 0.0037 * (tcell - self.pv['rated_tcell']))
				mapped[id_]['tcell'] = tcell
				mapped[id_]['voc'] = voc
				mapped[id_]['pmax'] = pmax
				mapped[id_]['isc'] = isc
				mapped[id_]['solarradiation'] = solar_radiation
				mapped[id_]['airtemperature'] = air_temperature
		return mapped

	def t_cell(self, air_temperature):
		pass

	def solve_(self, point):
		return point
