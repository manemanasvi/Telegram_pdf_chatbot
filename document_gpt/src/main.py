from flask import Flask, request, jsonify
import json
from document_gpt.helper.telegram_api import send_message
from document_gpt.helper.conversation import create_conversation
# from document_gpt.helper.process_telegram_data import process_telegram_data
# from document_gpt.helper.generate_response import generate_text_response, generate_file_response

app = Flask(_name_)

def process_telegram_data(data):
    # Initialize response structure
    response_data = {
        'is_text': False,
        'is_document': False,
        'is_unknown': True,  # Default to unknown type
        'sender_id': data['message']['from']['id']
    }

    if 'text' in data['message']:
        response_data.update({
            'is_text': True,
            'is_unknown': False,
            'text': data['message']['text']
        })
    elif 'document' in data['message']:
        response_data.update({
            'is_document': True,
            'is_unknown': False,
            'file_id': data['message']['document']['file_id'],
            'mime_type': data['message']['document']['mime_type']
        })

    return response_data




def generate_text_response(text):
    qa = create_conversation()  # Assuming this initializes your NLP model
    response = qa.ask(text)  # Assuming this method sends the text to your model and gets a response
    return response


import requests
from config import config
from document_gpt.helper.telegram_api import get_file_path
import PyMuPDF  # or any other library for processing the document

def download_file(file_path):
    url = f"https://api.telegram.org/file/bot{config.TELEGRAM_TOKEN}/{file_path}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def extract_text_from_pdf(pdf_content):
    # This is a placeholder for extracting text from the PDF content
    # Implementation depends on the library you choose
    pass

def generate_file_response(file_id, mime_type, sender_id):
    file_path_response = get_file_path(file_id)
    if file_path_response['status'] == 'success':
        file_path = file_path_response['file_path']
        file_content = download_file(file_path)
        if mime_type == 'application/pdf':
            text = extract_text_from_pdf(file_content)
            # Use text to generate a response, e.g., summary, using an NLP model
            response = "Generated response based on the document."
            return response
    return "Failed to process document."


@app.route('/telegram', methods=['POST'])
def telegram_api():
    if request.is_json:
        data = request.get_json()
        print(json.dumps(data, indent=4))  # For debugging

        try:
            telegram_data = process_telegram_data(data)

            if 'is_unknown' in telegram_data and telegram_data['is_unknown']:
                return jsonify({'status': 'ignored unknown message'}), 200
            
            sender_id = telegram_data.get('sender_id')

            if 'is_text' in telegram_data and telegram_data['is_text']:
                response = generate_text_response(telegram_data['text'])
                send_message(sender_id, response)
                return jsonify({'status': 'text processed'}), 200
            
            if 'is_document' in telegram_data and telegram_data['is_document']:
                response = generate_file_response(telegram_data['file_id'], telegram_data.get('mime_type'), sender_id)
                send_message(sender_id, response)
                return jsonify({'status': 'document processed'}), 200

        except Exception as e:
            print(f"Error processing the Telegram request: {e}")  # For debugging
            # Consider logging the error for production
            return jsonify({'error': 'Internal server error'}), 500

    return jsonify({'error': 'Bad request'}), 400



@app.route('/set-telegram-webhook', methods=['POST'])
def setup_telegram_webhook():
    data = request.json
    if data and 'url' in data:
        success = set_webhook(data['url'], data.get('secret_token', ''))
        if success:
            return jsonify({'status': 'Webhook set successfully'}), 200
        else:
            return jsonify({'error': 'Failed to set webhook'}), 500
    return jsonify({'error': 'Bad request, missing URL'}), 400

@app.route('/set-telegram-menu-commands', methods=['POST'])
def setup_telegram_menu_commands():
    data = request.json
    if data and 'commands' in data:
        success = set_menu_commands(data['commands'])
        if success:
            return jsonify({'status': 'Commands set successfully'}), 200
        else:
            return jsonify({'error': 'Failed to set commands'}), 500
    return jsonify({'error': 'Bad request, missing commands'}), 400


if _name_ == '_main_':
    app.run(debug=True)