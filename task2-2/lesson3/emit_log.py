import sys
import pika

parameters = pika.ConnectionParameters(
    host="127.0.0.1",
    credentials=pika.PlainCredentials("labuser", "labpass"),
)

message = " ".join(sys.argv[1:]) or "Hello subscribers!"

with pika.BlockingConnection(parameters) as connection:
    channel = connection.channel()
    channel.exchange_declare(exchange="logs", exchange_type="fanout")
    channel.basic_publish(
        exchange="logs",
        routing_key="",
        body=message.encode("utf-8"),
    )
    print(f"[x] Sent: {message}")
