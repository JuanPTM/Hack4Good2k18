from flask import Flask

import pika # RabbitMQ connector
import mysql.connector as mariadb # MariaDB connector
from pymongo import MongoClient


# mariadb_connection = mariadb.connect(user='python_user', password='some_pass', database='employees') # CONNECT TO DB
# client = MongoClient('localhost', 27017) # CHANGE HOSTNAME TO DEPLOYED SERVICE NAME


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World from Hack4Food! I\'m alive.\n'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)