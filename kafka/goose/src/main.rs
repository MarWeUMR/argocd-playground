use goose::prelude::*;
use rdkafka::config::ClientConfig;
use rdkafka::producer::{FutureProducer, FutureRecord};
use std::time::Duration;
use url::Url;

// Load test function to produce messages to Kafka
async fn kafka_producer(user: &mut GooseUser) -> TransactionResult {
    // let _ = user.get("boostrapservers").await?;

    let mut goose = user.get("404").await?;

    if let Ok(response) = &goose.response {
        // We expect a 404 here.
        if response.status() == 404 {
            return user.set_success(&mut goose.request);
        }
    }

    // Retrieve the host configured for Goose
    let parsed_url = Url::parse(&user.config.host).expect("Failed to parse host URL");

    let x = format!(
        "{}:{}",
        parsed_url.host_str().unwrap_or_default(),
        parsed_url.port().unwrap_or_default()
    );

    // Configure Kafka producer
    let producer: FutureProducer = ClientConfig::new()
        .set("bootstrap.servers", &x)
        .create()
        .expect("Producer creation error");

    // Define the topic and the message to produce
    let topic = "my-topic";
    let message = "test_message";

    // Asynchronously produce a message to the Kafka topic
    let produce_future = producer.send(
        FutureRecord::to(topic).payload(message).key("test_key"),
        Duration::from_secs(0),
    );

    // Await the result of the message production
    match produce_future.await {
        Ok(delivery) => println!("Delivered message to {:?}", delivery),
        Err((e, _)) => println!("Error producing message: {:?}", e),
    }

    // sleep(Duration::from_secs(1)).await;

    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), GooseError> {
    GooseAttack::initialize()?
        .register_scenario(
            scenario!("KafkaProducerScenario").register_transaction(transaction!(kafka_producer)),
        )
        .execute()
        .await?;

    Ok(())
}
