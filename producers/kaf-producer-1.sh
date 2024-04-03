#!/bin/bash

# Kafka topic
TOPIC="my-topic"

# Brokers address
BROKERS="localhost:30664"

# Produce messages
while true; do
	plumber write kafka --input-file 1kb.txt --address $BROKERS --topics $TOPIC
	# cat 1kb.txt | kaf produce $TOPIC -b $BROKERS
	sleep 0.5
	echo "--------------"
done
