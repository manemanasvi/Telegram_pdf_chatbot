from flask import Flask, request, jsonify
from dotenv import load_dotenv
from document_gpt.helper.telegram_api import handle_update
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    return "The bot is running!"




@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    print("Received update:", update)  # Print the received data
    if update:
        handle_update(update)  # Process the incoming message if data is received
        print("Received message:", update)  # Log the update received
        return jsonify(success=True)
    else:
        print("No data received in the update.")
        return jsonify(success=False, error="No data received in the update.")



if __name__ == '__main__':
    app.run(debug=True)
