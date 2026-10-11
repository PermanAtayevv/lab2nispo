import pika

parameters = pika.ConnectionParameters(
    host="127.0.0.1",
    credentials=pika.PlainCredentials("labuser", "labpass"),
)

with pika.BlockingConnection(parameters) as connection:
    channel = connection.channel()
    channel.queue_declare(
        queue="hello",
        durable=True,
        arguments={"x-queue-type": "quorum"},
    )
    channel.basic_publish(
        exchange="",
        routing_key="hello",
        body="Hello World!",
    )
    print("[x] Sent: Hello World!")
