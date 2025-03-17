from flask import Flask, jsonify, render_template
app = Flask(__name__)
from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB setup
client = MongoClient('mongodb://mongo_db:27017/')
db = client['mydatabase']
collection = db['options']


@app.route('/')
def home():
    return render_template('index.html',title='Home')

@app.route('/data', methods=['GET'])
def get_data():
    #creates a dictionary of {class: count} from the database "options" column.
    data = {}
    for option in collection.find():
        if option['option'] not in data:
            data[option['option']] = 1
        else:
            data[option['option']] += 1
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)