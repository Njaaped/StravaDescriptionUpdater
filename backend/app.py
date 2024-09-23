from flask import Flask, jsonify, request
from flask_cors import CORS
from userhandler import UserHandler
import sqlite3
from activityhandling import handle_activity
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": f"{os.getenv('ORIGIN')}"}})
userhandler = UserHandler()

@app.route('/api/data', methods=['GET', 'POST', 'OPTIONS'])
def get_data():
    return jsonify({'message': 'Hello from Flask with CORS enabled!'})
    
@app.route('/api/senduserdata', methods=['POST'])
def send_data():
    data = request.get_json()
    result = userhandler.check_login(data)
    haveAuthorized = ["no","yes"][result[1]]
    if result[0]:
        return jsonify({'message': 'Login successful!', 
                        'status' : 'success', 
                        'username' : data['username'], 
                        'haveAuthorized' : haveAuthorized}), 200
    else:
        return jsonify({'message': 'Login failed!', 'status' : 'failed'}), 401
    
@app.route('/api/createuser', methods=['POST']) 
def create_user():
    data = request.get_json()
    result = userhandler.add_user(data)
    if result:
        return jsonify({'message': 'User created!', 'status' : 'success'}), 200
    else:
        return jsonify({'message': 'User creation failed!', 'status' : 'failed'}), 401
    
@app.route('/api/userwithcode', methods=['POST'])
def user_with_code():
    data = request.get_json()
    print(data, "len data: ", len(data))
    result = userhandler.add_user_with_code(data)
    print(result)
    if result:
        return jsonify({'message': 'Refresh Token added!', 'status' : 'success'}), 200
    else:
        return jsonify({'message': 'failed!', 'status' : 'failed'}), 401
    
@app.route('/api/receive_description', methods=['POST'])
def receive_description():
    data = request.get_json()
    try:
        insertDescriptionIntoTable(data)
        return jsonify({'message': 'Description received!', 'status' : 'success'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Description not received!', 'status' : 'failed'}), 401
    

@app.route('/webhook', methods=['POST'])
def webhook():
    print("webhook event received!", request.args, request.json)
    strava_user_id = request.json['owner_id']
    activity_id = request.json['object_id']
    aspect_type = request.json['aspect_type']
    if aspect_type == 'create':
        handle_activity(activity_id, strava_user_id)
    return 'EVENT_RECEIVED', 200

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('WEBHOOK_VERIFIED')
            return jsonify({"hub.challenge": challenge})
        else:
            return 'Forbidden', 403


def insertDescriptionIntoTable(data):
    type = data['type']
    description = data['description']
    username = data['username']
    print(type, description, username)
    db = os.getenv('DB')
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    query = "UPDATE description SET description=? WHERE username=? AND type=?"
    cursor.execute(query, (description, username, type))
    conn.commit()


if __name__ == '__main__':
    app.run(debug=True, port=5001)


