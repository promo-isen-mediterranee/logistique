import pika

channel = None

def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    print("Connected to RabbitMQ")
    connection.channel(on_open_callback=on_channel_open)

def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    channel.queue_declare(queue="test", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)
    print("Connected to the channel")

def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
    channel.basic_consume('test', handle_delivery)

def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    print(body)

def on_close(connection, exception):
    connection.ioloop.stop()
    print("Closing connection")

credential = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(host="localhost", port=5672, credentials=credential)
connection = pika.SelectConnection(on_open_callback=on_connected, on_close_callback=on_close)

try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
    connection.ioloop.start()

# Look at https://github.com/pika/pika/blob/main/examples/asynchronous_publisher_example.py
# for publishing example