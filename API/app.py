from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from markupsafe import escape

import os
# MongoDB setup
client = MongoClient('mongodb://mongo:27017/')
db = client['mydatabase']
collection = db['options']
# Flask setup
app = Flask(__name__, static_folder='./buttons/',template_folder="./")
buttons = []

# Read spreadsheet from the xlsx file and create a list of folders
import pandas as pd
data_table= pd.read_excel('pictures.xlsx')
#there are 4 columns in the table: image1, image2, correct answer and test name
#for each test name, create a folder with the test name and put the images in it and Shrugging_kaomoji.jpg

data_table['test_name'] = data_table['test_name'].astype(str)
#replace spaces with underscores
data_table['test_name'] = data_table['test_name'].str.replace(" ", "_")
for test_name in data_table['test_name'].unique():
    test_name= test_name.replace(" ", "_")
    os.makedirs(os.path.join('buttons', test_name), exist_ok=True)
    #for each test name, create a folder with the test name and put the images in it and Shrugging_kaomoji.jpg
    for index, row in data_table[data_table['test_name'] == test_name].iterrows():
        # Copy the images to the folder
        for col in ['leftImage', 'rightImage']:
            image_path = row[col]
            if pd.notna(image_path):
                # Check if the image path is a string
                if isinstance(image_path, str):
                    # Create the destination path
                    dest_path = os.path.join('buttons', test_name, os.path.basename(image_path))
                    # Copy the image to the destination path
                    if not os.path.exists(dest_path):
                        os.system(f'cp {image_path} {dest_path}')
    os.system(f'cp pictures/Shrugging_kaomoji.jpg buttons/{test_name}/Shrugging_kaomoji.jpg')



@app.route('/')
def home():

    return render_template('index.html')

# @app.route('/buttons', methods=['GET'])
# def buttons():
#     files=[]
#     # Get all the options from the folder buttons and return them in a list
#     for file in os.listdir('buttons'):
#         if file.endswith('.png'):
#             files.append(file)

#     return jsonify({"icons": files})

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    if 'option' not in data:
        return jsonify({"error": "No option provided"}), 400
    
    option = data.get('option', None)
    participant_id = data.get('participantId', None)
    time_pressed = datetime.now()
    # Insert into MongoDB
    collection.insert_one({"folder": option.split("/")[-2],"option": option.split("/")[-1].split(".")[0],"participant":participant_id, "time_pressed": time_pressed})
    #next folder is the next test name in the list
    folder= option.split("/")[-2]
    index= data_table[data_table['test_name'] == folder].index[0]
    #check if the index is the last index
    if index == len(data_table)-1:
        folder= data_table['test_name'].unique()[0]
    else:
        folder= data_table['test_name'].unique()[index+1]
    #check if the folder exists
    if not os.path.exists(os.path.join('buttons', folder)):
        return jsonify({"error": "Folder does not exist"}), 400
    return jsonify({"message": "Option added successfully","folder":folder}), 200


@app.route('/buttons/<subpath>/')
def get_options(subpath):
    # Get all the options from the folder buttons and return them in a list
    folder_path = os.path.join('buttons', subpath)
    print(f"Looking for files in: {folder_path}")
    files = []
    assert os.path.exists(folder_path), "Folder does not exist"
    for file in os.listdir(os.path.join('buttons', subpath)):
        if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
            files.append(os.path.join(subpath, file))
    return jsonify({"icons": files})

@app.route('/listfolders', methods=['GET'])
def list_folders():
    # Get all the folders from test_names
    folders = data_table['test_name'].unique().tolist()
    for i in range(len(folders)):
        folders[i]= folders[i].replace(" ", "_")
    return jsonify({"folders": folders})


if __name__ == '__main__':
    app.run(debug=True)