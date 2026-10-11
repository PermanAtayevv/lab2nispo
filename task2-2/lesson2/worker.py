import os
import time
import pika

parameters = pika.ConnectionParameters(
    host="127.0.0.1",
    credentials=pika.PlainCredentials("labuser", "labpass"),
)


def callback(channel, method, properties, body):
    message = body.decode("utf-8")
    print(f"[{os.getpid()}] Received: {message}", flush=True)
    time.sleep(message.count("."))
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print(f"[{os.getpid()}] Done", flush=True)


def main():
    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()
        channel.queue_declare(
            queue="task_queue",
            durable=True,
            arguments={"x-queue-type": "quorum"},
        )
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue="task_queue",
            on_message_callback=callback,
            auto_ack=False,
        )
        print(f"[*] Worker PID: {os.getpid()}. Waiting for tasks.", flush=True)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            print("Worker stopped.")


if __name__ == "__main__":
    main()
