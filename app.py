from flask import Flask, request, jsonify
from bot.ai_bot import ChatBot
from services.waha import WahaChat


app = Flask(__name__)

class ChatbotApp:
    def __init__(self):
        self._chat_bot = None
        self._waha_chat = None

    @property
    def chat_bot(self):
        if not self._chat_bot:
            raise ValueError('Bot não inicializado')
        return self._chat_bot

    @property
    def waha_chat(self):
        if not self._waha_chat:
            raise ValueError('Waha Chat não inicializado')
        return self._waha_chat

    def initialize(self, chat_bot: ChatBot, waha_chat: WahaChat):
        self._chat_bot = chat_bot
        self._waha_chat = waha_chat

    def webhook(self, data):
        print(f'EVENTO RECEBIDO: {data}')

        try:
            chat_id = data['payload']['from']
            received_message = data['payload']['body']

            response = self.chat_bot.invoke(question=received_message)

            if response is None:
                return jsonify({'status': 'error', 'message': 'Erro ao invocar a IA'}), 500

            self.waha_chat.send_message(chat_id, response)
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500


chatbot_app = ChatbotApp()

chatbot_app.initialize(ChatBot(), WahaChat())

@app.route('/chatbot/webhook/', methods=['POST'])
def chatbot_webhook():
    data = request.json
    
    return chatbot_app.webhook(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)