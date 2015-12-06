import sys, os, ast, json

import pymongo
from pymongo import MongoClient
from bson import ObjectId

def establish_connection():
	client = MongoClient('localhost')
	return client


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def read_data():
	location = 'location_data/data_final.json'
	f = open(location, 'rb')
	for a in f:
		data = a
	f.close()
	data = ast.literal_eval(a)
	return data

def mapped_data(data):
	mapped = []
	keys = ['solarradiation2005_2015', 
			'solarradiation2035_2064', 
			'solarradiation2060_2089', 
			'airtemperature2005_2015', 
			'airtemperature2035_2064', 
			'airtemperature2060_2089', 
			]
	for each in data:
		
		for k in keys:
			t = {'code': each['code'], 'name': each['name'], 'lat': each['lat'], 'lon': each['lon'], 'state_name': each['state_name'], 'key': k, 'data': each[k]}
			mapped.append(t)
	return mapped

def ingest_():
	"THE INGEST SCRIPT FOR DATA"
	client = establish_connection()
	data = read_data()
	clean_data = mapped_data(data)
	for each in clean_data:
		client.test_.ren_project_data.save(each)
	return

def get_data_key(key):
	"RETURNS DATA FOR THE QUERIED KEY"
	data = []
	client = establish_connection()
	cur = client.test_.ren_project_data.find(
			{'key': key},  
			#{ 'data': { '$slice': [5, 1] } } 
			)
	for a in cur:
		data.append(a)
	client.close()
	return data

