Detailed Wiki: Starting Zookeeper, Kafka, and Communicating with Producer and Consumer
This guide explains how to start Zookeeper, start Kafka, and set up a Producer and Consumer to send and receive messages in Apache Kafka. It assumes you already have Zookeeper and Kafka installed and configured.
________________________________________
Step 1: Start Zookeeper
Zookeeper is required for Kafka to coordinate brokers, manage metadata, and elect leaders. Start it first.
1.1 Start Zookeeper
1.	Navigate to the Zookeeper bin directory:
2.	cd /opt/zookeeper/bin
3.	Start the Zookeeper server:
4.	./zkServer.sh start
5.	Verify that Zookeeper is running:
6.	./zkServer.sh status
o	Expected Output: 
	If this is the only Zookeeper node: 
	Mode: standalone
	If in a cluster, one will show Leader, and others will show Follower.
________________________________________
Step 2: Start Kafka Broker
Once Zookeeper is running, you can start the Kafka broker.
2.1 Start Kafka
1.	Navigate to the Kafka bin directory:
2.	cd /opt/kafka/bin
3.	Start the Kafka broker using the configuration file:
4.	./kafka-server-start.sh ../config/server.properties
5.	Keep this terminal open to monitor Kafka logs.
2.2 Verify Kafka is Running
In another terminal, verify the broker is accessible:
kafka-broker-api-versions.sh --bootstrap-server 127.0.0.1:9092
Expected Output:
muffin:9092 (id: 1 rack: null) -> (
    Produce(0): 0 to 11 [usable: 11],
    Fetch(1): 0 to 17 [usable: 17],
    ...
)
________________________________________
Step 3: Create a Kafka Topic
Kafka organizes messages into topics. Producers send messages to a topic, and consumers read messages from a topic.
3.1 Create a Topic
Run the following command to create a topic named test-topic:
kafka-topics.sh --create \
--topic test-topic \
--bootstrap-server 127.0.0.1:9092 \
--partitions 1 \
--replication-factor 1
3.2 Verify the Topic
List all existing topics to ensure test-topic was created:
kafka-topics.sh --list --bootstrap-server 127.0.0.1:9092
Expected Output:
test-topic
________________________________________
Step 4: Start a Kafka Producer
A Producer sends messages to a Kafka topic.
4.1 Start the Producer
1.	Run the producer for the test-topic:
2.	kafka-console-producer.sh --topic test-topic --bootstrap-server 127.0.0.1:9092
3.	Type messages directly into the terminal (one per line). For example:
4.	Hello, Kafka!
5.	This is a test message.
6.	Press Enter after each message. These messages are now sent to the test-topic.
7.	Leave this terminal open if you want to continue sending messages.
________________________________________
Step 5: Start a Kafka Consumer
A Consumer reads messages from a Kafka topic.
5.1 Start the Consumer
1.	Open a new terminal.
2.	Run the consumer to read messages from test-topic:
3.	kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server 127.0.0.1:9092
4.	The consumer will display all messages from test-topic. If the producer is still running, you can send more messages, and the consumer will display them in real-time.
Expected Output:
Hello, Kafka!
This is a test message.
________________________________________
Step 6: Stopping Zookeeper and Kafka
When you're done testing, stop Kafka and Zookeeper gracefully.
6.1 Stop Kafka
1.	In the terminal where Kafka is running, press Ctrl+C.
2.	Alternatively, run: 
3.	kafka-server-stop.sh
6.2 Stop Zookeeper
1.	Stop Zookeeper with the following command:
2.	./zkServer.sh stop
3.	Verify Zookeeper has stopped:
4.	./zkServer.sh status
o	Expected Output: 
o	Error contacting service. It is probably not running.
________________________________________
Troubleshooting
Issue 1: Kafka Broker Fails to Start
•	Check Zookeeper: Ensure Zookeeper is running before starting Kafka: 
•	./zkServer.sh status
•	Port Conflict: If port 9092 is in use, change it in server.properties: 
•	listeners=PLAINTEXT://:9093
Issue 2: Consumer Doesn’t Receive Messages
•	Ensure the consumer is listening to the correct topic.
•	Check if the producer and consumer are connected to the same Kafka broker.
Issue 3: Zookeeper Connectivity Error
•	Ensure zookeeper.connect in server.properties points to the correct Zookeeper address: 
•	zookeeper.connect=127.0.0.1:2181
________________________________________
Summary of Commands
Task	Command
Start Zookeeper	/opt/zookeeper/bin/zkServer.sh start
Start Kafka	kafka-server-start.sh /opt/kafka/config/server.properties
Create a Topic	kafka-topics.sh --create --topic test-topic --bootstrap-server 127.0.0.1:9092
List Topics	kafka-topics.sh --list --bootstrap-server 127.0.0.1:9092
Start a Producer	kafka-console-producer.sh --topic test-topic --bootstrap-server 127.0.0.1:9092
Start a Consumer	kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server 127.0.0.1:9092
Stop Kafka	kafka-server-stop.sh
Stop Zookeeper	/opt/zookeeper/bin/zkServer.sh stop


To delete an already created topic in Kafka, follow these steps:________________________________________
2. Delete the Topic
Run the following command to delete a Kafka topic:
bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic <topic_name>
Replace <topic_name> with the name of the topic you want to delete.
Example:
bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic my-topic
________________________________________
3. Verify Deletion
To confirm the topic is deleted, list all the topics:
bin/kafka-topics.sh --bootstrap-server localhost:9092 –list





