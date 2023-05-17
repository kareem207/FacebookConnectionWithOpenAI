from flask import Flask, request
import requests
import os
from OpenAIModel import OpenAIModel

app = Flask(__name__)

VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]
PAGE_ACCESS_TOKEN = os.environ["PAGE_ACCESS_TOKEN"]

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args["hub.challenge"], 200
        else:
            return "Verification token mismatch", 403
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):  
                    sender_id = messaging_event['sender']['id']  
                    send_message(sender_id, "Hello, World!")

    return "ok", 200


def send_message(recipient_id, message_text):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }
    requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, json=data)

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
