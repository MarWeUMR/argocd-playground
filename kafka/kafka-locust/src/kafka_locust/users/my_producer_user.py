from locust import task, constant_pacing
import os
from .abstract_kafka_producer import AbstractKafkaProducer


class MyUser(AbstractKafkaProducer):
    bootstrap_servers = os.environ["KAFKA_SERVERS"]
    group_id = "my-consumer-group"
    topics = ["lafp_test"]
    wait_time = constant_pacing(1)

    def __init__(self, environment):
        super().__init__(environment)
        # self.consumer = KafkaConsumer(
        #     environment=environment,
        #     bootstrap_servers=self.bootstrap_servers,
        #     group_id=self.group_id,
        #     topics=self.topics,
        # )

    def on_start(self):
        print("user started")

    @task
    def produce_and_consume(self):
        # Read the content of the file
        try:
            with open("1kb.txt", "rb") as file:  # Open the file in binary mode
                file_content = file.read()
        except IOError as e:
            print(f"Error reading file: {e}")
            return  # Exit the task if the file cannot be read

        # Produce a message with the file content
        self.client.send("lafp_test", file_content)
        # self.client.producer.poll()  # Ensure the message is sent

        # Consume messages
        # self.consumer.consume(timeout=1.0)
