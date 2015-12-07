import sys, os, ast, json
from bson import ObjectId
from flask import Flask, request, render_template

from mongo_ import get_data_key as get
from data_objects import heatmap_object, timeseries_object

app = Flask(__name__)
app.debug = True

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/ren_project/')
def ren_project():
	return render_template('ren_project.html')

@app.route('/get_data_key/')
def get_data_key():
	key = request.args['key'].encode('utf-8')
	data = get(key)
	return JSONEncoder().encode(data)

@app.route('/get_heatmap_data/')
def get_heatmap_data():
	response = heatmap_object(request.args).get_month_data()
	return JSONEncoder().encode(response)

@app.route('/get_timeseries_data/')
def get_timeseries_data():
	response = timeseries_object(request.args).get_timeseries_data()
	return JSONEncoder().encode(response)



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)

