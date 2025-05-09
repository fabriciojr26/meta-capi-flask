from flask import Flask, request, jsonify
import requests
import hashlib
import time

app = Flask(__name__)

ACCESS_TOKEN = 'EAAIFsqIgjhoBOZBwSUlhZBu6ZCgHY0FZBJIkwD4CylnNZBZCzhDfjh1ii2VoXRn6BKQt42VKpKS6zM7XzdZCf6KZBH7NCd7lqlLugkb8aItWHayfmGXRmAjgucVODKJ7iplwIHsNvbNkFNQX7IGhAP3ZBORO7Yz70sQEuC7HtXCxmI2BSneyhv5hOIQ9catgAY6F9FQZDZD'
PIXEL_ID = '1799701637171612'

def hash_sha256(value):
    return hashlib.sha256(value.strip().lower().encode()).hexdigest()

@app.route('/send_purchase_event', methods=['POST'])
def send_purchase_event():
    data = request.json
    payload = {
        "data": [
            {
                "event_name": data.get("event_name", "Purchase"),
                "event_time": data.get("event_time", int(time.time())),
                "action_source": data.get("action_source", "website"),
                "event_source_url": data.get("event_source_url", ""),
                "event_id": data.get("event_id", ""),
                "user_data": {
                    "client_ip_address": request.remote_addr,
                    "client_user_agent": request.headers.get("User-Agent"),
                    "fbc": data["user_data"].get("fbc"),
                    "fbp": data["user_data"].get("fbp")
                },
                "custom_data": {
                    "value": data["custom_data"].get("value", 10.00),
                    "currency": data["custom_data"].get("currency", "BRL")
                }
            }
        ]
    }

    response = requests.post(
        f"https://graph.facebook.com/v19.0/{PIXEL_ID}/events",
        params={"access_token": ACCESS_TOKEN},
        json=payload
    )

    return jsonify({
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "response": response.json()
    })
