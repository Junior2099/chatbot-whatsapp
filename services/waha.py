import requests

class WahaChat:
    def __init__(self):
        self._api_url = 'http://waha:3000'

    def send_message(self, chat_id, message):
        url = f'{self._api_url}/api/sendText'
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'session': 'default',
            'chatId': chat_id,
            'text': message,
        }
        try:
            response = requests.post(url=url, json=payload, headers=headers)
            return response
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return None
