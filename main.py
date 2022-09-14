import json
import openai
from flask import Flask, jsonify
from requests import request
from gpt import GPT
from gpt import Example
from flask import request
from flask_pymongo import pymongo
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



app = Flask(__name__)
cors = CORS(app)
CONNECTION_STRING = "REPLACE YOUR DATABSE LINK"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')

def getData():
    data = db.db.collection.find({})
    return data

@app.route('/', methods = ['POST'])
@cross_origin()
def index():
    
    data = json.loads(request.data)

    openai.api_key = "OPEN AI API KEY"
   
    Gpt = GPT(engine="davinci",
            temperature=0.5,
            max_tokens=100)

    dbDatas = list(getData())
   

    for dbData in dbDatas:


        Gpt.add_example(Example(dbData['ques'], 
                                dbData['ans']))
    

    prompt = data['msg']
    output = Gpt.get_top_reply(prompt)
    return output.partition('\n')[0]

@app.route('/learn', methods = ['POST'])
@cross_origin()
def learn():
    data = json.loads(request.data)

    db.db.collection.insert_one({"ques": data['ques'], "ans" : data['ans']})


    return "SUCCESS"

db1 = client.get_database('chat')
@app.route('/chat', methods = ['POST'])
@cross_origin()
def chat():
    data = json.loads(request.data)
    print(data)
    db1.db.collection.insert_one({"ques": data['msg'], "ans" : data['byBot']})


    return "SUCCESS"

@app.route('/getChat', methods = ['GET'])
@cross_origin()
def getchat():
    
    data = db1.db.collection.find({})
    data = list(data)
    data = JSONEncoder().encode(data)
    return json.dumps(data)


 
  
app.run(host='0.0.0.0', port=8800)
