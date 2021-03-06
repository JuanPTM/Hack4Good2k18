import ast
import json
from datetime import datetime

from bson import json_util
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from pymongo import MongoClient
import yaml

app = Flask(__name__)
api = Api(app)



with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

cfgMongo = cfg['mongo']
client = MongoClient(cfgMongo['dbHostname'], 27017)
db = client.data

mysql = MySQL()

cfgMaria = cfg['maria']
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = cfgMaria['user']
app.config['MYSQL_DATABASE_PASSWORD'] = cfgMaria['password']
app.config['MYSQL_DATABASE_DB'] = cfgMaria['dbName']
app.config['MYSQL_DATABASE_HOST'] = cfgMaria['dbHostname']

mysql.init_app(app)


class Device(Resource):

    def get(self, user_id):
        if user_id is None:
            return "No Usuario"

        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM Device WHERE user_id = {}'.format(user_id))
        r = [dict((cursor.description[i][0], value)
                  for i, value in enumerate(row)) for row in cursor.fetchall()]
        return jsonify({'Devices': r})

    def post(self, user_id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('nombre', type=str, help='Email address to create user')
            args = parser.parse_args()

            _nombre = args['nombre']
            if user_id is None or _nombre is None:
                return "No Usuario o Nombre"
            cursor = mysql.get_db().cursor()
            cursor.execute(' INSERT INTO Device(nombre, user_id) VALUES (\'{}\', {})'.format(_nombre, user_id))
            mysql.get_db().commit()
            return {'estado': 'Actualizado'}

        except Exception as e:
            return {'error': str(e)}

    def put(self, user_id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('nombre', type=str)
            parser.add_argument('user_id', type=int)
            args = parser.parse_args()

            _nombre = args['nombre']
            _userid = args['user_id']
            if _userid is None or _nombre is None:
                return "No Usuario o Nombre"
            cursor = mysql.get_db().cursor()
            cursor.execute(" UPDATE Device SET nombre = \'{}\', user_id = \'{}\' WHERE device_id = {}".format(_nombre,
                                                                                                              _userid,
                                                                                                              user_id))
            mysql.get_db().commit()
            return {'device_id': cursor.lastrowid}

        except Exception as e:
            return {'error': str(e)}

    def delete(self, user_id):
        if user_id is None:
            return "No Dispositivo"
        cursor = mysql.get_db().cursor()
        cursor.execute(" DELETE FROM Device WHERE device_id = {} ".format(user_id))
        mysql.get_db().commit()
        return {'estado': 'Borrado'}


class User(Resource):
    def get(self):
        return {'hello': 'User'}


class Data(Resource):
    def post(self, device_id):
        collection = db.geofence
        parser = reqparse.RequestParser()
        parser.add_argument('alias', type=str)
        parser.add_argument('positions', type=str)
        parser.add_argument('init_time', type=str)
        parser.add_argument('end_time', type=str)

        args = parser.parse_args()

        _alias = args['alias']
        _initime = datetime.fromtimestamp(int(args['init_time'])).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        _endtime = datetime.fromtimestamp(int(args['end_time'])).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        _positions = args['positions']

        data = {
            'alias': _alias,
            'device_id': int(device_id),
            'init_time': _initime,
            'end_time': _endtime,
            'loc': {
                'type': "Polygon",
                'coordinates': "compadre"
            }
        }

        data2 = ast.literal_eval(json.dumps(data).replace('"compadre"', _positions))

        collection.insert(data2)
        # result = []
        # for data in collection.find():
        #     result.append(data)
        # return json.dumps(result, default=json_util.default)

    def get(self, device_id):
        collection = db.geofence
        print device_id
        return json_util.dumps(list(collection.find({'device_id': int(device_id)})))


class CheckFence(Resource):
    def post(self, device_id):
        parser = reqparse.RequestParser()
        parser.add_argument('lat', type=str)
        parser.add_argument('lon', type=str)
        args = parser.parse_args()

        _lat = args['lat']
        _lon = args['lon']

        collection = db.geofence
        return collection.find(
            {'device_id': device_id,
             'loc': {'$geoIntersects': {
                 '$geometry': {'type': "Point", 'coordinates': [float(_lon), float(_lat)]}}}}).count()


api.add_resource(Device, '/device/<user_id>')
api.add_resource(Data, '/fence/<device_id>')
api.add_resource(CheckFence, '/checkfence/<device_id>')
api.add_resource(User, '/user')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
