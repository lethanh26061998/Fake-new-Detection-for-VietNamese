import pika
import process
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='simulations')
channel.queue_declare(queue='results')

def callback(ch, method, properties, body):
    requestParams = json.loads(body.decode('utf-8'))
    print(requestParams)
    message = str(requestParams[0])
    results = process.simulate(message, message)
    channel.basic_publish(exchange='', routing_key='results', body=json.dumps(results, ensure_ascii=False))


channel.basic_consume(queue='simulations', on_message_callback=callback, auto_ack=True)
channel.start_consuming()