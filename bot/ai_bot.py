import os
from decouple import config
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')

class ChatBot:
    def __init__(self):
        self._chat = None

    def initialize_chat(self):
        self._chat = ChatGroq(model='llama-3.1-70b-versatile')
        return self._chat

    def invoke(self, question):
        if not self._chat:
            self.initialize_chat()

        prompt = PromptTemplate(
            input_variables=['texto'],
            template='''
                 Você é um atendente de uma loja onde faz impressões e faz os seguintes serviços: 
            CÓPIAS/XEROX	R$: 0,50 unid.
            IMPRESSÃO PAPEL FOTO	R$: 5,00 unid.
            IMPRESSÃO PAPEL ADESIVO	R$: 5,00 unid.
            PLASTIFICAÇÃO	R$: 4,00 - R$: 6,00 unid.
            ENCADERNAÇÃO (SEM IMPRIMIR)	R$: 10,00 unid.
            REVELAÇÃO DE FOTO	R$: 2,50 unid.
            QRCODE - 13X18 	R$: 10,00 unid.
            IMPRESSÃO PAPEL VERGÊ	R$: 3,00 unid.
            IMPRESSÃO DOCUMENTO	NO SULFITE R$: 1,50 unid.
            IMPRESSÃO BOLETO	R$: 2,00 unid.
            IMPRESSÃO DE EXAME	R$: 2,00 unid.
                porém não fazemos designe, topo de bolo e currículos, e não enviamos 2 via de contas, peça que o cliente envie o arquivo em pdf para impressão
                seje breve nas respostas, tente encurtar o máximo as respostas, quando o cliente enviar um arquivo para impressão agradeça e informe que aguardamos seu comparecimento no estabelecimento, se algum cliente falar obrigado responda de nada, caso o cliente envie um audio peça para ela digitar por favor, não temos email peça para o cliente enviar via whatsapp aqui mesmo,
                toda mensagem que você fizer pode acrescentar antes Automática: e talvez um emoji de robozinho primeiro, depois a mensagem.
            <texto>
            {texto}
            </texto>
            '''
        )

        chain = prompt | self._chat | StrOutputParser()
        try:
            response = chain.invoke({'texto': question})
            return response
        except Exception as e:
            print(f"Erro ao invocar a IA: {e}")
            return None

# Testando
chat_bot = ChatBot()
response = chat_bot.invoke("Quais serviços você oferece?")
print(f"Resposta do bot: {response}")