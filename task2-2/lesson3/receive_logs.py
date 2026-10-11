import os
import pika

parameters = pika.ConnectionParameters(
    host="127.0.0.1",
    credentials=pika.PlainCredentials("labuser", "labpass"),
)


def callback(channel, method, properties, body):
    print(f"[{os.getpid()}] Received: {body.decode('utf-8')}", flush=True)


def main():
    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange="logs", exchange_type="fanout")

        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange="logs", queue=queue_name)

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True,
        )
        print(f"[*] Subscriber PID: {os.getpid()}", flush=True)
        print(f"[*] Queue: {queue_name}", flush=True)
        print("[*] Waiting for logs. Press Ctrl+C to exit.", flush=True)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            print("Subscriber stopped.")


if __name__ == "__main__":
    main()
