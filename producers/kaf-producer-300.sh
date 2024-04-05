#!/bin/bash

# Kafka topic
TOPIC="my-topic-300"

# Brokers address
BROKERS="localhost:30664"

# Produce messages
while true; do
	for i in {1..600}; do
		plumber write kafka --input-file 1kb.txt --address $BROKERS --topics $TOPIC
	done
	sleep 300
	echo "--------------"
done
