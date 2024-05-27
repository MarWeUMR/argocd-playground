# Application Description

This app deploys two pods with a running kafka producer.
A script `kafka-chit-chat.sh` is provided via configMap to generate traffic in the kafka cluster.
The idea is to generate a constant load with different patterns in order to have some baseline for any sort of metrics evaluation.
