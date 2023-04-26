from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

myclient = MongoClient("mongodb://mymongo:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

mydict = [{ "name": "John", "address": "a 37" },{ "name": "John", "address": "Highway 37" },{ "name": "John", "address": "Highway 37" }]

@app.route("/")
def index():
    # Add data to MongoDB
    x=mycol.insert_many(mydict)

    # Return response
    return {"message":"rohan"}

@app.route("/data")
def data():
    # Get data from MongoDB
    # Return response
    data=mycol.find_one()
    return {"This is the output": str(data)}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
