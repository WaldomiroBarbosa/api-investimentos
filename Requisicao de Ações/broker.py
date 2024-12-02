import pika
import json
import requests

# Conexão com RabbitMQ
conexao = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
canal = conexao.channel()

# Declaração do exchange e das filas
canal.queue_declare(queue='stock_updates')
canal.queue_declare(queue='cliente_inscrito')
canal.queue_declare(queue='acoes_abaixo_300')
canal.queue_declare(queue='acoes_strong_buy')
canal.queue_declare(queue='acoes_hold')
canal.queue_declare(queue='acoes_amazon')
canal.queue_declare(queue='acoes_por_setor')
print("Broker aguardando mensagens\n")

# ==================================================================================
# Configuração do Telegram
TOKEN_TELEGRAM = "7707956157:AAH1Gy1HsYMIsNhO7KDK63-htg7uC_LDpnI"
CHAT_ID = "6889128828"

# Função para enviar mensagem no telegram
def envia_msg_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem}
    resposta = requests.post(url, json=payload)
    if resposta.status_code == 200:
        print("Mensagem enviada ao Telegram com sucesso.\n")
    else:
        print(f"Erro ao enviar mensagem: {resposta.text}")
# ==================================================================================

# Função para verificar se o cliente está inscrito
def cliente_inscrito():
    metodo_consumir, propriedades, corpo = canal.basic_get(queue='cliente_inscrito', auto_ack=True)
    if metodo_consumir:
        print("Cliente inscrito detectado.\n")
        return True
    return False

# ==================================================================================
# Callback para processar as mensagens
def processa_mensagem(ch, method, properties, body):
    if not cliente_inscrito():
        print("Nenhum cliente inscrito. Mensagem ignorada.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    #print(f"Mensagem recebida (raw): {body.decode()}")
    try:
        dados = json.loads(body)
        #print(f"Dados: {dados}")
    except json.JSONDecodeError as e:
        #print(f"Erro: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Envia aos clientes inscritos na fila para receber acoes com preco menor que 300
    if dados['preco'] < 300:
        canal.basic_publish(exchange='', routing_key='acoes_abaixo_300', body=json.dumps(dados))
        print(f"Enviado para fila 'acoes_abaixo_300': {dados['ticker']} com preço abaixo de 300.")
        mensagem_telegram = (f"ALERTA: Ação abaixo de 300!\n"
                             f"Ticker: {dados['ticker']}\n"
                             f"Preço: {dados['preco']:.2f}")
        envia_msg_telegram(mensagem_telegram)
    
    # Envia aos clientes inscritos na fila para receber acoes com recomendação "strong_buy" 
    if dados['recomendacao'] == "strong_buy":
        canal.basic_publish(exchange='', routing_key='acoes_strong_buy', body=json.dumps(dados))
        print(f"Enviado para fila 'acoes_strong_buy': {dados['ticker']} com recomendação 'strong_buy'.")
        mensagem_telegram = (f"ALERTA: Recomendação 'STRONG BUY'!\n"
                             f"Ticker: {dados['ticker']}\n"
                             f"Preço: {dados['preco']:.2f}")
        envia_msg_telegram(mensagem_telegram)

    # Envia aos clientes inscritos na fila para receber acoes com recomendação "hold"
    if dados['recomendacao'] == "hold":
        canal.basic_publish(exchange='', routing_key='acoes_hold', body=json.dumps(dados))
        print(f"Enviado para fila 'acoes_hold': {dados['ticker']} com recomendação 'hold'.")
        mensagem_telegram = (f"ALERTA: Recomendação 'HOLD'!\n"
                             f"Ticker: {dados['ticker']}\n"
                             f"Preço: {dados['preco']:.2f}")
        envia_msg_telegram(mensagem_telegram)

    # Envia aos clientes inscritos na fila para receber acoes da Amazon
    if dados['empresa'] == "Amazon.com, Inc.":
        canal.basic_publish(exchange='', routing_key='acoes_amazon', body=json.dumps(dados))
        print(f"Enviado para fila 'acoes_amazon': {dados['ticker']}.")
        mensagem_telegram = (f"ALERTA: Ação da Amazon!\n"
                             f"Ticker: {dados['ticker']}\n"
                             f"Preço: {dados['preco']:.2f}")
        envia_msg_telegram(mensagem_telegram)

    # Envia aos clientes inscritos na fila para receber acoes do setor informado
    if 'setor' in dados:
        canal.basic_publish(exchange='', routing_key='acoes_por_setor', body=json.dumps(dados))
        print(f"Enviado para fila 'acoes_por_setor': {dados['setor']}.")
        mensagem_telegram = (f"ALERTA: Setor inscrito\n"
                             f"Ticker: {dados['ticker']}\n"
                             f"Preço: {dados['preco']:.2f}\n"
                             f"Setor: {dados['setor']}")
        envia_msg_telegram(mensagem_telegram)

    ch.basic_ack(delivery_tag=method.delivery_tag)

# Recebendo mensagens da fila de ações
canal.basic_qos(prefetch_count=1)
canal.basic_consume(queue='stock_updates', on_message_callback=processa_mensagem)
canal.start_consuming()