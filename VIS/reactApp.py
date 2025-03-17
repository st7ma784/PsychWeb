from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/mydatabase"
mongo = PyMongo(app)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    #creates a dictionary of {class: count} from the database "options" column.
    data = mongo.db.options.aggregate([
        {
            "$group": {
                "_id": "$option",
                "count": {"$sum": 1}
            }
        }
    ])
    
    return dumps(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)