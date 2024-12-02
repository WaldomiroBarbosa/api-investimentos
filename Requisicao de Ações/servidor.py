import pika
import json
import yfinance as yf
import time

# Configuração de ações a monitorar
acoes = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "BRK-A", "V"]

# Função para acessar o yfinance e obter os dados das ações
def obter_dados_acao(ticker):
    try:
        acao = yf.Ticker(ticker)
        preco = float(acao.history(period="1d")['Close'].iloc[-1])
        info = acao.info
        return {
            "ticker": ticker,
            "preco": preco,
            "empresa": info.get("shortName", "Empresa desconhecida"),
            "setor": info.get("sector", "Setor desconhecido"),
            "recomendacao": info.get("recommendationKey", "sem_recomendacao")
        }
    except Exception as e:
        print(f"Erro ao obter dados para {ticker}: {e}")
        return None

# Conexão com RabbitMQ
conexao = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
canal = conexao.channel()
canal.queue_declare(queue='stock_updates')

# Monitoramento contínuo
while True:
    for ticker in acoes:
        dados = obter_dados_acao(ticker)
        if dados:
            mensagem = json.dumps(dados)
            canal.basic_publish(exchange='', routing_key='stock_updates', body=mensagem)
            print(f"Publicado: {mensagem}")
    time.sleep(10) # Intervalo de 10 segundos para evitar excesso de requisições

connection.close()
