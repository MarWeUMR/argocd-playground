from locust import task, run_single_user, constant_throughput, constant_pacing
import os
import time
import functools
from locust import User, between
from locust_plugins import missing_extra
from confluent_kafka import Producer, Consumer

from kafka_locust.users.my_producer_user import MyUser
from kafka_locust.shapes.wave_shape import WaveShape

# from kafka_locust.shapes.single_burst_shape import SingleBurstShape

# class KafkaConsumer:
#     def __init__(self, *, environment, bootstrap_servers, group_id, topics):
#         self.environment = environment
#         self.consumer = Consumer(
#             {
#                 "bootstrap.servers": bootstrap_servers,
#                 "group.id": group_id,
#                 "auto.offset.reset": "earliest",
#             }
#         )
#         self.topics = topics
#         self.consumer.subscribe(self.topics)
#
#     def consume(self, timeout=1.0):
#         start_perf_counter = time.perf_counter()
#         start_time = time.time()
#         msg = self.consumer.poll(timeout=timeout)
#         if msg is None:
#             return
#         if msg.error():
#             if msg.error().code() == KafkaError._PARTITION_EOF:
#                 # End of partition event
#                 self.environment.events.request.fire(
#                     request_type="CONSUME",
#                     name="EOF",
#                     start_time=start_time,
#                     response_time=(time.perf_counter() - start_perf_counter) * 1000,
#                     response_length=0,
#                     context={},
#                     exception=None,
#                 )
#             else:
#                 # Error
#                 self.environment.events.request.fire(
#                     request_type="CONSUME",
#                     name="ERROR",
#                     start_time=start_time,
#                     response_time=(time.perf_counter() - start_perf_counter) * 1000,
#                     response_length=0,
#                     context={},
#                     exception=msg.error(),
#                 )
#         else:
#             # Message is consumed
#             self.environment.events.request.fire(
#                 request_type="CONSUME",
#                 name=msg.topic(),
#                 start_time=start_time,
#                 response_time=(time.perf_counter() - start_perf_counter) * 1000,
#                 response_length=len(msg.value()),
#                 context={},
#                 exception=None,
#             )


# class MyOtherUser(AbstractKafkaProducer):
#     bootstrap_servers = os.environ["KAFKA_SERVERS"]
#     group_id = "my-other-consumer-group"
#     topics = ["lafp_test_other"]
#     wait_time = constant_pacing(5)
#
#     def __init__(self, environment):
#         super().__init__(environment)
#         self.consumer = KafkaConsumer(
#             environment=environment,
#             bootstrap_servers=self.bootstrap_servers,
#             group_id=self.group_id,
#             topics=self.topics,
#         )
#
#     @task
#     def produce_and_consume_other(self):
#         # Read the content of a different file
#         try:
#             with open("1kb.txt", "rb") as file:  # Open the file in binary mode
#                 file_content = file.read()
#         except IOError as e:
#             print(f"Error reading file: {e}")
#             return  # Exit the task if the file cannot be read
#
#         # Produce a message with the file content to a different topic
#         self.client.send("lafp_test_other", file_content)
#         self.client.producer.poll(1)  # Ensure the message is sent
#
#         # Consume messages from the other topic
#         self.consumer.consume(timeout=1.0)


# if __name__ == "__main__":
#     user_classes = [MyUser, MyOtherUser, MyOtherUser]
#     for user_class in user_classes:
#         run_single_user(user_class)
