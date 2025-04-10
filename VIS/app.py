from flask import Flask, jsonify, render_template
app = Flask(__name__,template_folder="./")
from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB setup
client = MongoClient('mongodb://mongo:27017/')
db = client['mydatabase']
collection = db['options']
#read spreadsheet from the xlsx file and create a list of folders
import pandas as pd
data_table= pd.read_excel('pictures.xlsx')
# again 
data_table['test_name'] = data_table['test_name'].str.replace(" ", "_")

#table will have image columns and a correct answer column




@app.route('/')
def home():
    return render_template('index.html',title='Home')

@app.route('/data', methods=['GET'])
def get_data():
    #creates a dictionary of {class: count} from the database "options" column.
    data = {"Researcher Agrees":0,"Researcher Disagrees":0}
    for option in collection.find():
        #the logic is that option has a column for folder and a option for the file name clicked. 
        # print(option)
        folder= option.get('folder',"")
        option= option['option']
        #check the correct answer in the database by finding the row with the folder name in the test_name column
        row_dict= data_table[data_table['test_name'] == folder].to_dict(orient='records')
        if len(row_dict)==0:
            # print("No row found for folder: ",folder)
            continue
        row=row_dict[0]
        #check if the option is in the row
        #find the CorrectAnswer column in the row
        correct_answer= row['Correct']
        if correct_answer == "imageA":
            answer= row["leftImage"]
        elif correct_answer == "imageB":
            answer= row["rightImage"]
        else: 
            answer="Shrugging_kaomoji" ## this isn't working ? 
        answer=answer.split("/")[-1].split(".")[0]
        if answer==option:
            data['Researcher Agrees']+=1
        else:
            answer=answer.split(".")[0]
            data['Researcher Disagrees']+=1           

    # print(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)