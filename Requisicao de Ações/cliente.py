import pika
import json

# Funções para processar mensagens de cada fila
def processa_acao_abaixo_300(ch, method, properties, body):
    dados = json.loads(body)
    print(f"ALERTA: Ação com preço menor que 300!\n"
          f"Ticker: {dados['ticker']}\n"
          f"Empresa: {dados['empresa']}\n"
          f"Preço: {dados['preco']:.2f}\n"
          f"Setor: {dados['setor']}\n"
          f"Recomendação: {dados['recomendacao']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def processa_recomendacao_strong_buy(ch, method, properties, body):
    dados = json.loads(body)
    print(f"ALERTA: Ação com recomendação 'STRONG BUY'\n"
          f"Ticker: {dados['ticker']}\n"
          f"Empresa: {dados['empresa']}\n"
          f"Preço: {dados['preco']:.2f}\n"
          f"Setor: {dados['setor']}\n"
          f"Recomendação: {dados['recomendacao']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def processa_recomendacao_hold(ch, method, properties, body):
    dados = json.loads(body)
    print(f"ALERTA: Ação com recomendação 'HOLD'!\n"
          f"Ticker: {dados['ticker']}\n"
          f"Empresa: {dados['empresa']}\n"
          f"Preço: {dados['preco']:.2f}\n"
          f"Setor: {dados['setor']}\n"
          f"Recomendação: {dados['recomendacao']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def processa_amazon(ch, method, properties, body):
    dados = json.loads(body)
    print(f"ALERTA: Recomendação de ação da Amazon!\n"
          f"Ticker: {dados['ticker']}\n"
          f"Empresa: {dados['empresa']}\n"
          f"Preço: {dados['preco']:.2f}\n"
          f"Setor: {dados['setor']}\n"
          f"Recomendação: {dados['recomendacao']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def processa_por_setor(ch, method, properties, body):
    dados = json.loads(body)
    print(f"ALERTA: Ação do setor informado\n"
          f"Ticker: {dados['ticker']}\n"
          f"Empresa: {dados['empresa']}\n"
          f"Preço: {dados['preco']:.2f}\n"
          f"Setor: {dados['setor']}\n"
          f"Recomendação: {dados['recomendacao']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Configuração do cliente
def cliente():
    # Conexão com RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Menu de inscrição para o cliente
    print("Escolha uma opção para se inscrever:")
    print("1: Ações com valor abaixo de 300")
    print("2: Ações com recomendação 'strong_buy'")
    print("3: Ações com recomendação 'hold'")
    print("4: Ações da empresa Amazon")
    print("5: Filtrar por setor")
    escolha = input("Digite o número da opção: ")

    # Inscrever o cliente na fila de controle para indicar que ele está pronto para consumir
    channel.queue_declare(queue='cliente_inscrito')
    channel.basic_publish(exchange='', routing_key='cliente_inscrito', body='inscrito')
    print("Cliente inscrito. Aguardando mensagens...")

    if escolha == '1':
        # Inscrição na fila de ações com preço abaixo de 300
        channel.queue_declare(queue='acoes_abaixo_300')
        channel.basic_consume(queue='acoes_abaixo_300', on_message_callback=processa_acao_abaixo_300)
        print("Cliente inscrito para ações com valor abaixo de 300.")
    elif escolha == '2':
        # Inscrição na fila de ações com recomendação 'strong_buy'
        channel.queue_declare(queue='acoes_strong_buy')
        channel.basic_consume(queue='acoes_strong_buy', on_message_callback=processa_recomendacao_strong_buy)
        print("Cliente inscrito para ações com recomendação 'strong_buy'.")
    elif escolha == '3':
        # Inscrição na fila de ações com recomendação 'hold'
        channel.queue_declare(queue='acoes_hold')
        channel.basic_consume(queue='acoes_hold', on_message_callback=processa_recomendacao_hold)
        print("Cliente inscrito para ações com recomendação 'hold'.")
    elif escolha == '4':
        # Inscrição na fila de ações da Amazon
        channel.queue_declare(queue='acoes_amazon')
        channel.basic_consume(queue='acoes_amazon', on_message_callback=processa_amazon)
        print("Cliente inscrito para ações da empresa Amazon.")
    elif escolha == '5':
        # Inscrição na fila de ações por setor
        setor = input("Digite o setor desejado: ")
        channel.queue_declare(queue='acoes_por_setor')
        channel.basic_consume(queue='acoes_por_setor', on_message_callback=processa_por_setor)
        print(f"Cliente inscrito para ações do setor '{setor}'.")
    else:
        print("Opção inválida.")
        return

    # Começa a receber mensagens da fila selecionada
    print("Aguardando mensagens...")
    channel.start_consuming()

if __name__ == '__main__':
    cliente()