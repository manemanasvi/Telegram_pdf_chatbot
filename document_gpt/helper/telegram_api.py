import requests
from config import config

BASE_URL = f'https://api.telegram.org/bot{config.TELEGRAM_TOKEN}'

def send_message(chat_id: int, message: str) -> bool:
    payload = {'chat_id': chat_id, 'text': message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{BASE_URL}/sendMessage', json=payload, headers=headers)
    if response.status_code == 200 and response.json().get('ok'):
        return True
    else:
        return False

def send_photo(chat_id: int, photo_url: str, caption: str = '') -> bool:
    payload = {'chat_id': chat_id, 'photo': photo_url}
    if caption:
        payload['caption'] = caption
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{BASE_URL}/sendPhoto', json=payload, headers=headers)
    if response.status_code == 200 and response.json().get('ok'):
        return True
    else:
        return False

def set_webhook(url: str, secret_token: str = '') -> bool:
    payload = {'url': url}
    if secret_token:
        payload['secret_token'] = secret_token
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{BASE_URL}/setWebhook', json=payload, headers=headers)
    if response.status_code == 200 and response.json().get('ok'):
        return True
    else:
        return False

def set_menu_commands(commands: list) -> bool:
    payload = {'commands': commands}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{BASE_URL}/setMyCommands', json=payload, headers=headers)
    if response.status_code == 200 and response.json().get('ok'):
        return True
    else:
        return False

def get_file_path(file_id: str) -> dict:
    response = requests.get(f'{BASE_URL}/getFile', params={'file_id': file_id})
    if response.status_code == 200 and response.json().get('ok'):
        result = response.json().get('result', {})
        return {'status': 'success', 'file_path': result.get('file_path')}
    else:
        return {'status': 'error', 'file_path': ''}