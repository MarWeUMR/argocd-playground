from locust import User
from ..clients.kafka_client import KafkaClient


class AbstractKafkaProducer(User):
    abstract = True
    # overload these values in your subclass
    bootstrap_servers: str = None  # type: ignore

    def __init__(self, environment):
        super().__init__(environment)
        self.client: KafkaClient = KafkaClient(
            environment=environment, bootstrap_servers=self.bootstrap_servers
        )

    def on_start(self):
        print("Starting abstract producer")

    def on_stop(self):
        self.client.producer.flush(5)
