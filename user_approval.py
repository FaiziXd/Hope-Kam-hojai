import os
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

# Default route to indicate that the app is running
@app.route('/')
def home():
    return jsonify({"message": "App is running"}), 200

# Approval request handling route
@app.route('/send_approval', methods=['POST'])
def send_approval():
    user_data = request.json
    unique_key = generate_unique_key(user_data)
    return jsonify({"message": "Approval request sent", "key": unique_key})

# Function to generate a unique key for the user
def generate_unique_key(user_data):
    return str(uuid.uuid4())  # Generates a unique key for each request

if __name__ == "__main__":
    # Get the port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
