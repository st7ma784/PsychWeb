from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from flask import render_template
import os
app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['options']

@app.route('/')
def home():
    #load the index.html file
    return render_template('index.html')

@app.route('/buttons', methods=['GET'])
def buttons():
    '''
    the javascript code to generate the button
    data.icons.forEach(icon => {
                    const img = document.createElement('img');
                    img.src = `/buttons/${icon}`;
                    img.alt = icon;
                    img.className = 'icon';
                    container.appendChild(img);
                });
    '''
    # Get all the options from the folder buttons and return them in a list
    for file in os.listdir('buttons'):
        if file.endswith('.png'):
            buttons.append(file)

    return jsonify({"icons": buttons})

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    if 'option' not in data:
        return jsonify({"error": "No option provided"}), 400
    
    option = data.get('option', None)
    participant_id = data.get('participantId', None)
    time_pressed = datetime.now()

    # Insert into MongoDB
    collection.insert_one({"option": option,"participant":participant_id, "time_pressed": time_pressed})

    return jsonify({"message": "Option added successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)