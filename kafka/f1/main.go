package main

import (
	"context" // Used for managing deadlines, cancellations, and other request-scoped values across API boundaries.
	"fmt"     // Implements formatted I/O with functions analogous to C's printf and scanf.
	"sync"    // Provides basic synchronization primitives like mutual exclusion locks.

	"github.com/form3tech-oss/f1/v2/pkg/f1"         // Importing the f1 load testing framework.
	"github.com/form3tech-oss/f1/v2/pkg/f1/testing" // Importing the testing package from f1 for creating test scenarios.
	"github.com/twmb/franz-go/pkg/kgo"              // Importing the franz-go package for Kafka operations.
)

func main() {
	// Initialize a new f1 testing instance and add our Kafka load test scenario.
	// The scenario is identified by the name "kafkaLoadTest".
	f1.New().Add("kafkaLoadTest", setupKafkaLoadTestScenario).Execute()
}

// setupKafkaLoadTestScenario initializes the Kafka client and defines the setup and teardown actions for the load test.
func setupKafkaLoadTestScenario(t *testing.T) testing.RunFn {
	fmt.Println("Setup Kafka load test scenario")

	// Define the Kafka broker addresses. Adjust these as needed for your Kafka cluster.
	kafkaBrokerAddresses := []string{"127.0.0.1:30985"}

	// Initialize the Kafka client with the broker addresses.
	kafkaClient, err := kgo.NewClient(kgo.SeedBrokers(kafkaBrokerAddresses...))
	if err != nil {
		t.Fatalf("Failed to create Kafka client: %v", err)
	}

	// Register a cleanup function to close the Kafka client at the end of the scenario.
	// This ensures resources are properly released once the test is complete.
	t.Cleanup(func() {
		fmt.Println("Clean up Kafka load test scenario")
		kafkaClient.Close()
	})

	// Define the function to run on every iteration of the load test.
	runIteration := func(t *testing.T) {
		fmt.Println("Run Kafka load test iteration")

		// Context to manage the lifecycle of the Kafka produce operation.
		operationContext := context.Background()

		// Use a WaitGroup to wait for the asynchronous produce operation to complete.
		var produceWaitGroup sync.WaitGroup
		produceWaitGroup.Add(1)

		// Define the Kafka record to be produced.
		kafkaRecord := &kgo.Record{Topic: "lafp_test", Value: []byte("test-message")}

		// Produce the record to Kafka.
		kafkaClient.Produce(operationContext, kafkaRecord, func(_ *kgo.Record, err error) {
			defer produceWaitGroup.Done() // Signal that the produce operation is complete.
			if err != nil {
				t.Errorf("Record had a produce error: %v", err)
			}
		})

		// Wait for the produce operation to complete before proceeding.
		produceWaitGroup.Wait()

		// Register a cleanup function for each test iteration.
		// This can be used to clean up resources specific to the iteration.
		t.Cleanup(func() {
			fmt.Println("Clean up Kafka load test iteration")
		})
	}

	// Return the function to run on every iteration of the load test.
	return runIteration
}
