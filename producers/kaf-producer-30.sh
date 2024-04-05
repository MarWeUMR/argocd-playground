#!/bin/bash

# Kafka topic
TOPIC="my-topic-30"

# Brokers address
BROKERS="localhost:30664"

# Produce messages
while true; do
	for i in {1..60}; do
		cat 1kb.txt | kafka-console-producer.sh --broker-list $BROKERS --topic $TOPIC --property "linger.ms=0" --property "batch.size=1"
	done
	echo "sleeping for 30s ..."
	sleep 30
done
