#!/bin/bash

# Datadog API Key
DD_API_KEY="your_datadog_api_key"

# Kafka Broker Address
KAFKA_BROKER="localhost:9092"

# Datadog Metric Name
METRIC_NAME="kafka.messages.in.per.second"

# Function to fetch MessagesInPerSec from Kafka
fetch_messages_in_per_sec() {
	# Replace this with the actual command to fetch the MessagesInPerSec metric from Kafka.
	# This is a placeholder and needs to be replaced based on your Kafka setup and how you can fetch metrics.
	# For example, you might use kafka-consumer-groups.sh, JMX, or any Kafka management tool you have.
	echo "100" # Placeholder value
}

# Function to send metric to Datadog
send_metric_to_datadog() {
	local value=$1
	local current_time=$(date +%s)

	curl -X POST "https://api.datadoghq.com/api/v1/series" \
		-H "Content-Type: application/json" \
		-H "DD-API-KEY: ${DD_API_KEY}" \
		-d "{
               \"series\": [
                  {
                    \"metric\": \"${METRIC_NAME}\",
                    \"points\": [
                       [
                          ${current_time},
                          ${value}
                       ]
                    ],
                    \"type\": \"gauge\",
                    \"host\": \"my.kafka.broker\",
                    \"tags\": [
                        \"environment:production\"
                    ]
                  }
               ]
             }"
}

# Main loop to fetch and send the metric every second
while true; do
	messages_in_per_sec=$(fetch_messages_in_per_sec)
	send_metric_to_datadog "$messages_in_per_sec"
	sleep 1
done
