import requests
import uuid
from document_gpt.helper.gpt import generate_response
from document_gpt.helper.pdfUtils import extract_text_from_pdf  # Import the new function
import os

# Define the base URL for sending messages using the Telegram API
TELEGRAM_BASE_URL = "https://api.telegram.org/bot7103842876:AAHI99e0H4RhREoIqcNsvSahJPxW5K2M-mk/"
TELEGRAM_FILE_URL = "https://api.telegram.org/file/bot7103842876:AAHI99e0H4RhREoIqcNsvSahJPxW5K2M-mk/"


def send_message(chat_id, text):
    """Send a message to a Telegram user specified by chat_id."""
    url = f"{TELEGRAM_BASE_URL}sendMessage"  # URL for sending messages
    payload = {
        'chat_id': chat_id,
        'text': text[:4096],  # Telegram messages have a max length of 4096 characters
    }
    try:
        response = requests.post(url, json=payload)
        response_data = response.json()

        # Check if Telegram API indicates an error
        if not response.ok or not response_data.get("ok"):
            error_message = response_data.get("description", "Failed to send message without a specific error.")
            print(f"Telegram API Error: {error_message}")
    except requests.exceptions.RequestException as e:
        # Handle connection errors
        print(f"Request Exception: {e}")


def get_file_path(file_id):
    """Fetches the file path of a file on Telegram's servers."""
    url = f"{TELEGRAM_BASE_URL}getFile?file_id={file_id}"
    response = requests.get(url)
    if response.ok:
        file_path = response.json().get("result", {}).get("file_path")
        if file_path:
            return file_path
    return None  # Return None or handle it appropriately if the file path isn't found



def download_file(file_path, save_path):
    """Downloads a file from Telegram's servers and checks for success."""
    url = f"{TELEGRAM_FILE_URL}{file_path}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            # Check if the file is not empty
            if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
                print(f"File successfully downloaded and saved at {save_path}")
                return True
            else:
                print("File downloaded but seems to be empty.")
                return False
        else:
            print("Failed to download the file from Telegram.")
            return False
    except Exception as e:
        print(f"Error downloading the file: {e}")
        return False


def handle_update(update):
    """Handle an incoming update from Telegram."""
    message = update.get('message', {})
    chat_id = message.get('chat', {}).get('id')

    # Handle document uploads
    document = message.get('document')
    if document and document.get('mime_type') == 'application/pdf':
        file_id = document.get('file_id')
        send_message(chat_id, "PDF uploaded successfully! We are preparing your summary, please wait...")

        file_path = get_file_path(file_id)

        # Generate a unique file name with the original file extension
        file_extension = os.path.splitext(document.get('file_name', 'document.pdf'))[1]
        unique_file_name = f"{uuid.uuid4()}{file_extension}"
        save_path = f"./data/input/{unique_file_name}"  # Using the unique file name

        # Attempt to download the file
        if download_file(file_path, save_path):
            extracted_text = extract_text_from_pdf(save_path)

            # Use the extracted text to generate a summary
            summary = generate_response(extracted_text)

            # Send the generated summary/response
            send_message(chat_id, summary if summary else "Sorry, I couldn't generate a summary.")
        else:
            # If the file wasn't downloaded successfully, inform the user
            send_message(chat_id, "Sorry, there was an issue processing your PDF. Please try again.")
    else:
        # Handle non-PDF documents or other messages
        send_message(chat_id, "Please upload a PDF file.")