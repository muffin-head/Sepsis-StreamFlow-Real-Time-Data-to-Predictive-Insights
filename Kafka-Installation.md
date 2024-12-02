## **Apache Kafka Setup Wiki**

This guide provides a **detailed and beginner-friendly tutorial** for setting up **Apache Kafka** on **Ubuntu**. By the end of this guide, you will have a running Kafka broker connected to Zookeeper and ready for use.

---

### **What is Apache Kafka?**
Apache Kafka is a distributed event streaming platform designed for:
- **Real-time data streaming**.
- Building **event-driven applications**.
- Supporting **publish/subscribe messaging**.

---

### **Prerequisites**

1. **Operating System**: Ubuntu (18.04, 20.04, or later recommended).
2. **Java Installed**:
   - Ensure Java is installed:
     ```bash
     java -version
     ```
   - If not installed, run:
     ```bash
     sudo apt update
     sudo apt install default-jdk -y
     ```

3. **Zookeeper Installed**:
   Kafka requires Zookeeper for coordination. If Zookeeper is not installed, [follow this guide](https://zookeeper.apache.org/) or install it via the following:
   ```bash
   wget https://dlcdn.apache.org/zookeeper/zookeeper-3.8.1/apache-zookeeper-3.8.1-bin.tar.gz
   tar -xvzf apache-zookeeper-3.8.1-bin.tar.gz
   mv apache-zookeeper-3.8.1-bin /opt/zookeeper
   cd /opt/zookeeper
   bin/zkServer.sh start
   ```

---

### **Step 1: Download and Install Kafka**

1. **Download Kafka Binary**:
   Visit the [official Kafka downloads page](https://kafka.apache.org/downloads) and download the latest stable binary distribution:
   ```bash
   wget https://downloads.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz
   ```

2. **Extract Kafka**:
   Extract the downloaded file:
   ```bash
   tar -xvzf kafka_2.13-3.5.0.tgz
   ```

3. **Move Kafka to `/opt/kafka`**:
   For better organization, move Kafka to the `/opt` directory:
   ```bash
   sudo mv kafka_2.13-3.5.0 /opt/kafka
   ```

---

### **Step 2: Set Up Environment Variables**

1. **Edit the `.bashrc` File**:
   Add Kafka’s `bin` directory to your PATH to run Kafka commands globally:
   ```bash
   nano ~/.bashrc
   ```

2. **Add the Following Lines**:
   ```bash
   export KAFKA_HOME=/opt/kafka
   export PATH=$PATH:$KAFKA_HOME/bin
   ```

3. **Reload `.bashrc`**:
   Apply the changes by reloading the `.bashrc` file:
   ```bash
   source ~/.bashrc
   ```

4. **Verify Kafka Commands**:
   Test if Kafka commands are accessible:
   ```bash
   kafka-topics.sh --help
   ```

---

### **Step 3: Configure Kafka**

1. **Open Kafka’s Configuration File**:
   Edit the main configuration file for the Kafka broker:
   ```bash
   nano /opt/kafka/config/server.properties
   ```

2. **Modify Key Settings**:
   - Set the broker ID (unique for each Kafka broker in a cluster):
     ```properties
     broker.id=1
     ```
   - Configure the Zookeeper connection:
     ```properties
     zookeeper.connect=127.0.0.1:2181
     ```
   - Define where Kafka stores its data:
     ```properties
     log.dirs=/opt/kafka/logs
     ```
   - Set the port Kafka will listen on:
     ```properties
     listeners=PLAINTEXT://:9092
     ```

3. **Save and Exit** (`Ctrl+O`, then `Ctrl+X`).

4. **Create the Logs Directory**:
   ```bash
   mkdir -p /opt/kafka/logs
   ```

---

### **Step 4: Start Kafka**

1. **Start Zookeeper**:
   If Zookeeper is not already running, start it:
   ```bash
   /opt/zookeeper/bin/zkServer.sh start
   ```

2. **Start the Kafka Broker**:
   Run the following command in a terminal:
   ```bash
   kafka-server-start.sh /opt/kafka/config/server.properties
   ```

   - This will start the Kafka broker and connect it to Zookeeper.
   - Leave this terminal open to monitor logs.

---

### **Step 5: Test Kafka**

#### **5.1 Create a Topic**
1. Create a topic named `test-topic`:
   ```bash
   kafka-topics.sh --create \
   --topic test-topic \
   --bootstrap-server 127.0.0.1:9092 \
   --partitions 1 \
   --replication-factor 1
   ```

2. Verify the topic was created:
   ```bash
   kafka-topics.sh --list --bootstrap-server 127.0.0.1:9092
   ```
   Output:
   ```
   test-topic
   ```

---

#### **5.2 Produce Messages**
1. Start a Kafka producer to send messages to the topic:
   ```bash
   kafka-console-producer.sh --topic test-topic --bootstrap-server 127.0.0.1:9092
   ```

2. Type some messages:
   ```
   Hello, Kafka!
   First message test.
   ```

3. Exit the producer with `Ctrl+C`.

---

#### **5.3 Consume Messages**
1. Start a Kafka consumer to read messages:
   ```bash
   kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server 127.0.0.1:9092
   ```

2. You should see:
   ```
   Hello, Kafka!
   First message test.
   ```

3. Exit the consumer with `Ctrl+C`.

---

### **Step 6: Monitor Kafka**

- **Check Active Brokers**:
   Use Zookeeper CLI to list active brokers:
   ```bash
   /opt/zookeeper/bin/zkCli.sh -server 127.0.0.1:2181
   ls /brokers/ids
   ```

- **Kafka Logs**:
   Monitor Kafka logs for issues:
   ```bash
   tail -f /opt/kafka/logs/server.log
   ```

---

### **Step 7: Multi-Broker Kafka Cluster (Optional)**

To set up a multi-broker cluster on a single machine:
1. Copy `server.properties` for each broker:
   ```bash
   cp /opt/kafka/config/server.properties /opt/kafka/config/server-2.properties
   ```

2. Modify the second broker’s configuration:
   ```properties
   broker.id=2
   log.dirs=/opt/kafka/logs-2
   listeners=PLAINTEXT://:9093
   ```

3. Start the second broker:
   ```bash
   kafka-server-start.sh /opt/kafka/config/server-2.properties
   ```

4. Verify the cluster:
   ```bash
   /opt/zookeeper/bin/zkCli.sh -server 127.0.0.1:2181
   ls /brokers/ids
   ```

---

### **Troubleshooting**

1. **Zookeeper Not Running**:
   Ensure Zookeeper is running before starting Kafka:
   ```bash
   /opt/zookeeper/bin/zkServer.sh start
   ```

2. **Port Conflict**:
   If port `9092` is in use, change it in `server.properties`:
   ```properties
   listeners=PLAINTEXT://:9093
   ```

3. **Log Directory Issues**:
   Ensure log directories are created and writable:
   ```bash
   mkdir -p /opt/kafka/logs
   ```

---

### **Next Steps**
- Explore Kafka Streams for real-time processing.
- Integrate Kafka with your applications (Python, Java).
- Monitor Kafka using tools like Prometheus and Grafana.

Let me know if you have questions or need clarification on any step! 😊
