import os
import pickle
import math
from flask import Flask, request, jsonify

app = Flask(__name__)

# File to store our pickle database
DB_FILE = 'users.pickle'

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_users(users):
    with open(DB_FILE, 'wb') as f:
        pickle.dump(users, f)

def round_coordinates(lat, long):
    # Round to nearest 0.5 degree (roughly 55 km at the equator)
    return round(lat * 2) / 2, round(long * 2) / 2

@app.route('/', methods=['POST'])
def register_or_update_user():
    data = request.json
    users = load_users()
    
    user = data.get('user')
    lat = data.get('lat')
    long = data.get('long')
    
    if not all([user, lat, long]):
        return jsonify({"error": "Missing required fields"}), 400
    
    if user in users:
        # Update existing user
        users[user]['lat'] = lat
        users[user]['long'] = long
    else:
        # Register new user
        users[user] = {
            'type': 'NOTSTARTED',
            'lat': lat,
            'long': long
        }
    
    save_users(users)
    
    return jsonify({"type": users[user]['type']})

@app.route('/', methods=['GET'])
def get_users():
    users = load_users()
    if not users:
        return jsonify({"error": "No users found"}), 404
    
    result = []
    for user, data in users.items():
        user_type = data['type']
        if user_type == 'HUNTER':
            result.append({
                "user": user,
                "type": user_type,
                "lat": data['lat'],
                "long": data['long']
            })
        elif user_type == 'SPEEDRUNNER':
            rounded_lat, rounded_long = round_coordinates(data['lat'], data['long'])
            result.append({
                "user": user,
                "type": user_type,
                "lat": rounded_lat,
                "long": rounded_long
            })
        else:  # NOTSTARTED
            result.append({
                "user": user,
                "type": user_type
            })
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
