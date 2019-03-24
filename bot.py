import json
import os

from flask import Flask
from flask import request
from flask import make_response

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("lorabot-firebase-adminsdk-rkp0u-5a6cea0466.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access.
    req_dict = json.loads(request.data)
    print(req_dict)
    # Accessing the fields on the POST request boduy of API.ai invocation of the webhook
    intent = req_dict["queryResult"]["intent"]["displayName"]

    if intent == 'ความหมายของ LoRa':
        doc_ref = db.collection(u'ความหมายของ LoRa').document(u'0zNx5yghCTkkTKvLUV7e')
        doc = doc_ref.get().to_dict()

        lora_meaning = doc['lora_meaning']
        picture = doc['picture']
        speech = f'{lora_meaning} \n{picture}'

    elif intent == 'ไม่เกี่ยวกับ LoRa' :
        doc_ref = db.collection(u'ไม่เกี่ยวกับ LoRa').document(u'T4EiYrOKRxqATjfJyyhK')
        doc = doc_ref.get().to_dict()
        
        asking = doc['asking']
        speech = f'{asking}'
    
    else: 
        speech = "กรุณาลองใหม่อีกครั้ง"

    res = makeWebhookResult(speech)

    return res


def makeWebhookResult(speech):

    return {
  "fulfillmentText": speech
    }


if __name__ == '__main__':
    app.run()