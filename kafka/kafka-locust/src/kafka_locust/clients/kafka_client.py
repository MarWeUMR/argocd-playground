import time
import functools
from confluent_kafka import Producer


class KafkaClient:
    def __init__(self, *, environment, bootstrap_servers):
        """
        Initializes the KafkaClient.

        :param environment: The environment context from locust, used for event firing.
        :param bootstrap_servers: A string representing the Kafka bootstrap servers.
        """
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
        """
        Sends a message to a specified Kafka topic.

        This method sends a message asynchronously to a Kafka topic and uses a callback
        function to handle delivery reports. It also fires a request event in the locust
        environment to log the request metrics.

        :param topic: The Kafka topic to which the message will be sent.
        :param value: The message payload as bytes.
        :param key: The key for the message, used for partitioning. Default is None.
        :param response_length_override: If provided, this value will be used as the
                                         response length for metrics instead of the
                                         message length. Default is None.
        :param name: An optional identifier for the message. If not provided, the topic
                     name will be used. Default is None.
        :param context: A dictionary containing additional context information that will
                        be passed to the request event. Default is an empty dict.

        Note: The method measures the time taken to enqueue the message and reports it
        along with the message size (or the overridden response length) to the locust
        environment for performance metrics.
        """
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
