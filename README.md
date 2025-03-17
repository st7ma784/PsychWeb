# PsychWeb Application

## Overview

PsychWeb is a simple web application designed to collect and store participant clicks and responses. The application is built using Flask for the backend and MongoDB for data storage. The frontend is served using a React application.

## Features

- **Data Collection**: Collects participant clicks and responses.
- **MongoDB Integration**: Stores collected data in a MongoDB database.
- **RESTful API**: Provides endpoints to retrieve stored data.
- **Proxy Configuration**: Uses Nginx to route requests to the appropriate services.

## Architecture

- **Backend**: Flask application that handles API requests and interacts with MongoDB.
- **Frontend**: React application that provides the user interface.
- **Database**: MongoDB for storing participant data.
- **Proxy Server**: Nginx for routing requests to the Flask and React applications.

## Setup

1. **Nginx Configuration**: Routes requests to the Flask and React applications.
    ```properties
    server {
        listen 8080;

        location /vis {
            proxy_pass http://react_vis:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location / {
            proxy_pass http://python_api:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

2. **Flask Application**: Handles API requests and interacts with MongoDB.
    ```python
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
        data = mongo.db.collection.find({}, {'_id': 0, 'options': 1})
        return dumps(data)

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
    ```

## Usage

- **Accessing the Application**: Navigate to `http://<server-ip>:8080` to access the React frontend.
- **API Endpoints**:
  - `GET /vis/data`: Retrieve stored participant data.

## License

This project is licensed under the MIT License.