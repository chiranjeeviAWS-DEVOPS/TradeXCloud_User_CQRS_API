import boto3
import json
import os
from flask import Flask, jsonify, request


def uploadfile(file_name):
        s3_client = boto3.client('s3')
        try:
                s3_client.upload_file(file_name, "tradexcloudcqrseventlogs", file_name)
                print("file uploaded successfully")
                os.remove(file_name)
                print("file removed from project directory successfully")
        except Exception as e:
                print(e)


def createfile(data):
    file_name = f'{data['UserID']}_{data['Action']}.json'

    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

    uploadfile(file_name)
       
app = Flask(__name__)

@app.route('/api', methods=["GET"])
def home():
    return jsonify({"message": "Hello from Flask"})

@app.route('/api/watchlistaction', methods=['POST'])
def create_data():
    data = request.json
    createfile(data)
    return jsonify({"message": "Data received!", "data": data}), 201



if __name__  == "__main__":
        app.run(debug=True)
