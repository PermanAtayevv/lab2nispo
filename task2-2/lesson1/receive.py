import pika

parameters = pika.ConnectionParameters(
    host="127.0.0.1",
    credentials=pika.PlainCredentials("labuser", "labpass"),
)


def callback(channel, method, properties, body):
    print(f"[x] Received: {body.decode('utf-8')}", flush=True)


def main():
    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()
        channel.queue_declare(
            queue="hello",
            durable=True,
            arguments={"x-queue-type": "quorum"},
        )
        channel.basic_consume(
            queue="hello",
            on_message_callback=callback,
            auto_ack=True,
        )
        print("[*] Waiting for messages. Press Ctrl+C to exit.", flush=True)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            print("Receiver stopped.")


if __name__ == "__main__":
    main()
