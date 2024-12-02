## **Detailed Wiki: Starting Zookeeper, Kafka, and Communicating with Producer and Consumer**

This guide explains how to **start Zookeeper**, **start Kafka**, and **set up a Producer and Consumer** to send and receive messages in Apache Kafka. It assumes you already have Zookeeper and Kafka installed and configured.

---

### **Step 1: Start Zookeeper**

Zookeeper is required for Kafka to coordinate brokers, manage metadata, and elect leaders. Start it first.

#### **1.1 Start Zookeeper**
1. Navigate to the Zookeeper `bin` directory:
   ```bash
   cd /opt/zookeeper/bin
   ```

2. Start the Zookeeper server:
   ```bash
   ./zkServer.sh start
   ```

3. Verify that Zookeeper is running:
   ```bash
   ./zkServer.sh status
   ```

   - **Expected Output**:
     - If this is the only Zookeeper node:
       ```
       Mode: standalone
       ```
     - If in a cluster, one will show **Leader**, and others will show **Follower**.

---

### **Step 2: Start Kafka Broker**

Once Zookeeper is running, you can start the Kafka broker.

#### **2.1 Start Kafka**
1. Navigate to the Kafka `bin` directory:
   ```bash
   cd /opt/kafka/bin
   ```

2. Start the Kafka broker using the configuration file:
   ```bash
   ./kafka-server-start.sh ../config/server.properties
   ```

3. Keep this terminal open to monitor Kafka logs.

#### **2.2 Verify Kafka is Running**
In another terminal, verify the broker is accessible:
```bash
kafka-broker-api-versions.sh --bootstrap-server 127.0.0.1:9092
```

**Expected Output**:
```
muffin:9092 (id: 1 rack: null) -> (
    Produce(0): 0 to 11 [usable: 11],
    Fetch(1): 0 to 17 [usable: 17],
    ...
)
```

---

### **Step 3: Create a Kafka Topic**

Kafka organizes messages into **topics**. Producers send messages to a topic, and consumers read messages from a topic.

#### **3.1 Create a Topic**
Run the following command to create a topic named `test-topic`:
```bash
kafka-topics.sh --create \
--topic test-topic \
--bootstrap-server 127.0.0.1:9092 \
--partitions 1 \
--replication-factor 1
```

#### **3.2 Verify the Topic**
List all existing topics to ensure `test-topic` was created:
```bash
kafka-topics.sh --list --bootstrap-server 127.0.0.1:9092
```

**Expected Output**:
```
test-topic
```

---

### **Step 4: Start a Kafka Producer**

A **Producer** sends messages to a Kafka topic.

#### **4.1 Start the Producer**
1. Run the producer for the `test-topic`:
   ```bash
   kafka-console-producer.sh --topic test-topic --bootstrap-server 127.0.0.1:9092
   ```

2. Type messages directly into the terminal (one per line). For example:
   ```
   Hello, Kafka!
   This is a test message.
   ```

3. Press **Enter** after each message. These messages are now sent to the `test-topic`.

4. Leave this terminal open if you want to continue sending messages.

---

### **Step 5: Start a Kafka Consumer**

A **Consumer** reads messages from a Kafka topic.

#### **5.1 Start the Consumer**
1. Open a new terminal.
2. Run the consumer to read messages from `test-topic`:
   ```bash
   kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server 127.0.0.1:9092
   ```

3. The consumer will display all messages from `test-topic`. If the producer is still running, you can send more messages, and the consumer will display them in real-time.

**Expected Output**:
```
Hello, Kafka!
This is a test message.
```

---

### **Step 6: Stopping Zookeeper and Kafka**

When you're done testing, stop Kafka and Zookeeper gracefully.

#### **6.1 Stop Kafka**
1. In the terminal where Kafka is running, press `Ctrl+C`.
2. Alternatively, run:
   ```bash
   kafka-server-stop.sh
   ```

#### **6.2 Stop Zookeeper**
1. Stop Zookeeper with the following command:
   ```bash
   ./zkServer.sh stop
   ```

2. Verify Zookeeper has stopped:
   ```bash
   ./zkServer.sh status
   ```
   - **Expected Output**:
     ```
     Error contacting service. It is probably not running.
     ```

---

### **Troubleshooting**

#### **Issue 1: Kafka Broker Fails to Start**
- **Check Zookeeper**:
  Ensure Zookeeper is running before starting Kafka:
  ```bash
  ./zkServer.sh status
  ```
- **Port Conflict**:
  If port `9092` is in use, change it in `server.properties`:
  ```properties
  listeners=PLAINTEXT://:9093
  ```

#### **Issue 2: Consumer Doesn’t Receive Messages**
- Ensure the consumer is listening to the correct topic.
- Check if the producer and consumer are connected to the same Kafka broker.

#### **Issue 3: Zookeeper Connectivity Error**
- Ensure `zookeeper.connect` in `server.properties` points to the correct Zookeeper address:
  ```properties
  zookeeper.connect=127.0.0.1:2181
  ```

---

### **Summary of Commands**

| **Task**                           | **Command**                                                                                 |
|------------------------------------|---------------------------------------------------------------------------------------------|
| Start Zookeeper                    | `/opt/zookeeper/bin/zkServer.sh start`                                                     |
| Start Kafka                        | `kafka-server-start.sh /opt/kafka/config/server.properties`                                |
| Create a Topic                     | `kafka-topics.sh --create --topic test-topic --bootstrap-server 127.0.0.1:9092`            |
| List Topics                        | `kafka-topics.sh --list --bootstrap-server 127.0.0.1:9092`                                  |
| Start a Producer                   | `kafka-console-producer.sh --topic test-topic --bootstrap-server 127.0.0.1:9092`           |
| Start a Consumer                   | `kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server 127.0.0.1:9092` |
| Stop Kafka                         | `kafka-server-stop.sh`                                                                     |
| Stop Zookeeper                     | `/opt/zookeeper/bin/zkServer.sh stop`                                                     |

---

### **Next Steps**
- Experiment with **multiple partitions** and **consumer groups**.
- Set up **Kafka Streams** for real-time data processing.
- Monitor Kafka with **Prometheus** and **Grafana**.

Let me know if you’d like guidance on advanced setups! 😊
