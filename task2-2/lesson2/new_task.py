import sys
import pika

parameters = pika.ConnectionParameters(
    host="127.0.0.1",
    credentials=pika.PlainCredentials("labuser", "labpass"),
)

message = " ".join(sys.argv[1:]) or "Hello World!"

with pika.BlockingConnection(parameters) as connection:
    channel = connection.channel()
    channel.queue_declare(
        queue="task_queue",
        durable=True,
        arguments={"x-queue-type": "quorum"},
    )
    channel.confirm_delivery()
    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=message.encode("utf-8"),
        properties=pika.BasicProperties(delivery_mode=2),
        mandatory=True,
    )
    print(f"[x] Sent: {message}")
