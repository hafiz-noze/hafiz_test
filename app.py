from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pika

app = Flask(__name__)

@app.route('/')
def index():
    return "Ok"


@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        message = request.form['message']
        if message:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))  # Connect to RabbitMQ
            channel = connection.channel()  # Open a channel
            channel.queue_declare(queue='hello')  # Declare a queue
            channel.basic_publish(exchange='', routing_key='hello', body=message)  # Send a message
            properties = pika.BasicProperties(content_type='text/plain', delivery_mode=2)
            channel.basic_publish(exchange='', routing_key='hello', body=message, properties=properties)
            connection.close()  # Close the connection
            flash('Message sent')
            return redirect(url_for('index'))
        else:
            flash('Message is empty')
            return redirect(url_for('index'))
    else:
        flash('Invalid request')
        return redirect(url_for('index'))


@app.route('/receive', methods=['GET'])
def receive():
    if request.method == 'GET':
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='message')
        print(' [*] Waiting for messages. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            cmd = body.decode('utf-8')

            if cmd == 'hey':
                print('hey there')
            elif cmd == 'hello':
                print('hello there')
            elif cmd == 'goodbye':
                print('goodbye')
            print(' [x] Done')
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        channel.basic_consume(callback, queue='message', no_ack=False)
        channel.start_consuming()
        return 'ok'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
