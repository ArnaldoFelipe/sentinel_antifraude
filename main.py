import json 
from confluent_kafka import Consumer, Producer
import pandas as pd
import joblib

modelo_ia = joblib.load('modelo_antifraude.pkl')

conf = {
    'bootstrap.servers': 'kafka:29092'
}

conf_consumidor = conf.copy()
conf_consumidor['group.id'] = 'motor-python-group'
conf_consumidor['auto.offset.reset'] = 'earliest'

consumidor = Consumer(conf_consumidor)
produtor = Producer(conf)

topico_entrada = 'transacao-solicitada'
consumidor.subscribe([topico_entrada])

topico_saida = 'transacao-analisada'


try:
    while True:
        msg = consumidor.poll(timeout=1.0)

        if msg is None: continue
            
        if msg.error(): continue

        payload_string = msg.value().decode('utf-8')
        transacao = json.loads(payload_string)

        id_tx = transacao.get('id')
        valor = float(transacao.get('valor', 0))

        dados_para_ia = pd.DataFrame([{'valor': valor}])
        predicao = modelo_ia.predict(dados_para_ia)[0]

        if predicao == 1:
             status_decidido = 'RECUSADA'
        else:
             status_decidido = 'APROVADA'

        resultado_dto = {
            'idTransacao': id_tx,
            'statusTransacao': status_decidido
        }

        payload_resposta = json.dumps(resultado_dto).encode('utf-8')
        produtor.produce(topico_saida, value= payload_resposta)
        produtor.flush()

except KeyboardInterrupt:
    print("desligando o motor antifraude")
finally:
        consumidor.close