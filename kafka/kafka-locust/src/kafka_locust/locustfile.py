from locust import task, run_single_user
import os
import time
import functools
from locust import User
from locust_plugins import missing_extra
from confluent_kafka import Producer, Consumer, KafkaError


class AbstractKafkaProducer(User):
    abstract = True
    # overload these values in your subclass
    bootstrap_servers: str = None  # type: ignore

    def __init__(self, environment):
        super().__init__(environment)
        self.client: KafkaClient = KafkaClient(
            environment=environment, bootstrap_servers=self.bootstrap_servers
        )

    def on_stop(self):
        self.client.producer.flush(5)


def _on_delivery(
    environment,
    identifier,
    response_length,
    start_time,
    start_perf_counter,
    context,
    err,
    _msg,
):
    environment.events.request.fire(
        request_type="ENQUEUE",
        name=identifier,
        start_time=start_time,
        response_time=(time.perf_counter() - start_perf_counter) * 1000,
        response_length=response_length,
        context=context,
        exception=err,
    )


class KafkaConsumer:
    def __init__(self, *, environment, bootstrap_servers, group_id, topics):
        self.environment = environment
        self.consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_servers,
                "group.id": group_id,
                "auto.offset.reset": "earliest",
            }
        )
        self.topics = topics
        self.consumer.subscribe(self.topics)

    def consume(self, timeout=1.0):
        start_perf_counter = time.perf_counter()
        start_time = time.time()
        msg = self.consumer.poll(timeout=timeout)
        if msg is None:
            return
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                self.environment.events.request.fire(
                    request_type="CONSUME",
                    name="EOF",
                    start_time=start_time,
                    response_time=(time.perf_counter() - start_perf_counter) * 1000,
                    response_length=0,
                    context={},
                    exception=None,
                )
            else:
                # Error
                self.environment.events.request.fire(
                    request_type="CONSUME",
                    name="ERROR",
                    start_time=start_time,
                    response_time=(time.perf_counter() - start_perf_counter) * 1000,
                    response_length=0,
                    context={},
                    exception=msg.error(),
                )
        else:
            # Message is consumed
            self.environment.events.request.fire(
                request_type="CONSUME",
                name=msg.topic(),
                start_time=start_time,
                response_time=(time.perf_counter() - start_perf_counter) * 1000,
                response_length=len(msg.value()),
                context={},
                exception=None,
            )


class KafkaClient:
    def __init__(self, *, environment, bootstrap_servers):
        self.environment = environment
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})

    def send(
        self,
        topic: str,
        value: bytes,
        key=None,
        response_length_override=None,
        name=None,
        context={},
    ):
        start_perf_counter = time.perf_counter()
        start_time = time.time()
        identifier = name if name else topic
        response_length = (
            response_length_override if response_length_override else len(value)
        )
        callback = functools.partial(
            _on_delivery,
            self.environment,
            identifier,
            response_length,
            start_time,
            start_perf_counter,
            context,
        )
        self.producer.produce(topic, value, key, on_delivery=callback)
        response_length = (
            response_length_override if response_length_override else len(value)
        )

        self.producer.poll()


class MyUser(AbstractKafkaProducer):
    bootstrap_servers = os.environ["KAFKA_SERVERS"]
    group_id = "my-consumer-group"
    topics = ["lafp_test"]

    def __init__(self, environment):
        super().__init__(environment)
        self.consumer = KafkaConsumer(
            environment=environment,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            topics=self.topics,
        )

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
        self.client.producer.poll(1)  # Ensure the message is sent

        # Consume messages
        # self.consumer.consume(timeout=1.0)


if __name__ == "__main__":
    run_single_user(MyUser)
