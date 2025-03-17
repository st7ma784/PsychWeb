from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

import os
# MongoDB setup
client = MongoClient('mongodb://mongo:27017/')
db = client['mydatabase']
collection = db['options']
# Flask setup
app = Flask(__name__, static_folder='./buttons/',template_folder="./")
buttons = []


@app.route('/')
def home():
    # print(os.system('ls'))
    
    return render_template('index.html')

@app.route('/buttons', methods=['GET'])
def buttons():
    files=[]
    # Get all the options from the folder buttons and return them in a list
    for file in os.listdir('buttons'):
        if file.endswith('.png'):
            files.append(file)

    return jsonify({"icons": files})

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    if 'option' not in data:
        return jsonify({"error": "No option provided"}), 400
    
    option = data.get('option', None)
    participant_id = data.get('participantId', None)
    time_pressed = datetime.now()

    # Insert into MongoDB
    collection.insert_one({"option": option.split("/")[-1],"participant":participant_id, "time_pressed": time_pressed})

    return jsonify({"message": "Option added successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)