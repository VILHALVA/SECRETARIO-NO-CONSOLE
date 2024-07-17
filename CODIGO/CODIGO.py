from TOKEN import TOKEN
import os
import requests
import json

class ConsoleSecretary:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}/"
        self.dir_atual = os.path.dirname(os.path.abspath(__file__))
        self.arquivo_conversas = os.path.join(self.dir_atual, "CONVERSAS.txt")

    def iniciar(self):
        print("🤖SECRETARIO INICIADO...AGUARDANDO MENSAGENS DOS USUÁRIOS...")
        last_update_id = None
        while True:
            update = self.obter_novas_mensagens(last_update_id)
            if update:
                for mensagem in update:
                    last_update_id = mensagem['update_id']
                    if 'message' in mensagem and 'text' in mensagem['message']:
                        chat_id = mensagem['message']['chat']['id']
                        user_name = mensagem['message']['from']['username']
                        mensagem_usuario = mensagem['message']['text']
                        
                        if mensagem_usuario.strip().lower() == '/start':
                            self.enviar_resposta("😀OLÁ! EU SOU O BOT SECRETÁRIO. ENVIE A SUA MENSAGEM AQUI E AGUARDE, QUE ASSIM QUE O ADM ESTIVER DISPONIVEL, ELE IRÁ TE RESPONDER!", chat_id)
                            continue  
                        
                        print(f"\n👤MENSAGEM DO USUÁRIO ({user_name}): {mensagem_usuario}")
                        resposta = input("🤖RESPONDA AO USUÁRIO:\n>>>")
                        
                        self.enviar_resposta(resposta, chat_id)
                        self.registrar_conversa(mensagem_usuario, resposta, user_name)

    def obter_novas_mensagens(self, update_id):
        link_req = f"{self.base_url}getUpdates"
        if update_id:
            link_req += f"?offset={update_id + 1}"
        resposta = requests.get(link_req)
        return json.loads(resposta.content)['result']

    def enviar_resposta(self, resposta, chat_id):
        link_req = f"{self.base_url}sendMessage?chat_id={chat_id}&text={resposta}"
        requests.get(link_req)

    def registrar_conversa(self, mensagem_usuario, resposta, usuario):
        with open(self.arquivo_conversas, "a", encoding="utf-8") as arquivo:
            arquivo.write("=" * 50 + "\n")
            arquivo.write(f"👤USUÁRIO DISSE: @{usuario}\n👄 DISSE: {mensagem_usuario}\n🤖SECRETÁRIO RESPONDEU: {resposta}\n")
            arquivo.write("=" * 50 + "\n")

secretario = ConsoleSecretary(TOKEN)
secretario.iniciar()
