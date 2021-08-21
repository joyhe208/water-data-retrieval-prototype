import flask
from flask import Flask, Response, render_template, request, jsonify, make_response
import json
import GetData
from GetData import *
import numpy as np
import config
from config import *
app = Flask(__name__)

mapLayerFiles = {
    "watersheds": "./static/data/Watersheds.json",
    "counties": "./static/data/CACounties.json",
    "urbanArea": "./static/data/CAUrbanArea.json",
    "urbanAreaPopulation": "./static/data/CAUrbanAreaPopulation.csv",
    "swp":"./static/data/SWPPath.json",
    "services":"./static/data/ServiceAreas.json",
    "contractors": "./static/data/Contractors.csv",
    "stations":"./static/data/testStationSnowflake.csv",
    "powerPlants":"./static/data/CAPowerPlants.csv" 
}

def convert(o):
    if isinstance(o, np.int64): return int(o)  

#for the map visualization
@app.route('/',methods=["POST","GET"])
@app.route('/index',methods=["POST","GET"])
def index():
    if(request.method == "POST"):
        req = request.get_json()
        layer = req['name']
        if(layer == "getStreamflow"):
            stations = req['stations']
            dateRange = req['dateRange']
            params = {
                'categorical':False,
                'columnList':['streamflow'],
                'filters':
                {
                    'staid':{'type': 'equal',
                            'values':stations}
                },
                'aggregateBy':'day',
                'aggregate':{'streamflow':'sum'},
                'dateRange':dateRange
            }
            getData = GetDatabaseTableData('streamflow.csv',config,params)
            data = getData.accessData()
            res = Response(json.dumps(data,default=convert), mimetype='application/json')
        else:
            if("json" in mapLayerFiles[layer]):
                getData = GetJsonData(mapLayerFiles[layer])
                
            else:
                getData = GetTableData(mapLayerFiles[layer])
            data = getData.accessData()
            if("csv" in mapLayerFiles[layer]):
                res = Response(json.dumps(data,default=convert), mimetype='application/json')
            else:
                res = make_response(jsonify(data),200)
        return res
    return render_template('index.html')

    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
