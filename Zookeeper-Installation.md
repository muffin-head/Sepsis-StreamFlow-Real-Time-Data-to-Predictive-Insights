## **Detailed Wiki for Setting Up Zookeeper in a Production Cluster**

This guide will walk you through **setting up a multi-node Zookeeper cluster** for high availability (HA), ensuring fault tolerance and scalability. We'll also integrate Zookeeper with **Kafka** for distributed coordination.

---

### **What is Zookeeper?**
Apache Zookeeper is a distributed coordination service used for:
- Managing configurations.
- Maintaining state across distributed systems.
- Handling leader election and fault tolerance.

In a **multi-node setup**, Zookeeper ensures high availability by replicating its state across multiple servers.

---

### **High-Level Overview**

1. **Multi-Node Setup**:
   - Configure 3 or more Zookeeper servers.
   - Each server will have a unique ID and contribute to the cluster.

2. **Configuration**:
   - Each node communicates using specific ports for leader election and synchronization.

3. **Start the Cluster**:
   - Start Zookeeper on all nodes and verify the cluster.

4. **Integration with Kafka**:
   - Point Kafka brokers to the Zookeeper cluster.

---

### **1. Prerequisites**

#### **System Requirements**
- At least **3 servers** (or virtual machines) for the cluster.
  - Example IPs: `192.168.1.1`, `192.168.1.2`, `192.168.1.3`.
- **Java Installed**:
  - Verify Java installation:
    ```bash
    java -version
    ```
  - Install Java if not already installed:
    ```bash
    sudo apt update
    sudo apt install default-jdk -y
    ```

#### **Download Zookeeper**
On each node, download and extract Zookeeper:
1. **Download Zookeeper**:
   ```bash
   wget https://dlcdn.apache.org/zookeeper/zookeeper-3.8.1/apache-zookeeper-3.8.1-bin.tar.gz
   ```

2. **Extract and Move Zookeeper**:
   ```bash
   tar -xvzf apache-zookeeper-3.8.1-bin.tar.gz
   sudo mv apache-zookeeper-3.8.1-bin /opt/zookeeper
   ```

---

### **2. Configure Zookeeper on Each Node**

1. **Navigate to Configuration Directory**:
   ```bash
   cd /opt/zookeeper/conf
   ```

2. **Copy the Sample Config File**:
   ```bash
   cp zoo_sample.cfg zoo.cfg
   ```

3. **Edit `zoo.cfg`**:
   Open the configuration file:
   ```bash
   nano zoo.cfg
   ```

   Add or modify the following settings:
   ```properties
   tickTime=2000
   initLimit=5
   syncLimit=2
   dataDir=/opt/zookeeper/data
   clientPort=2181

   # Cluster Configuration
   server.1=192.168.1.1:2888:3888
   server.2=192.168.1.2:2888:3888
   server.3=192.168.1.3:2888:3888
   ```

   - **`tickTime`**: Basic time unit (ms) for heartbeats.
   - **`initLimit`**: Time for a follower to connect to a leader.
   - **`syncLimit`**: Time for a follower to sync with the leader.
   - **`dataDir`**: Directory to store metadata.
   - **`server.X`**: Define each server in the cluster with:
     - IP address.
     - `2888`: Port for follower-to-leader communication.
     - `3888`: Port for leader election.

4. **Create the Data Directory**:
   ```bash
   mkdir -p /opt/zookeeper/data
   ```

5. **Set Unique IDs for Each Node**:
   On each node, create a file named `myid` in the `dataDir` directory:
   - On Node 1 (`192.168.1.1`):
     ```bash
     echo "1" > /opt/zookeeper/data/myid
     ```
   - On Node 2 (`192.168.1.2`):
     ```bash
     echo "2" > /opt/zookeeper/data/myid
     ```
   - On Node 3 (`192.168.1.3`):
     ```bash
     echo "3" > /opt/zookeeper/data/myid
     ```

---

### **3. Start Zookeeper on Each Node**

1. **Start Zookeeper**:
   On each server, navigate to the `bin` directory and start Zookeeper:
   ```bash
   cd /opt/zookeeper/bin
   ./zkServer.sh start
   ```

2. **Verify the Status**:
   Check the status on each server:
   ```bash
   ./zkServer.sh status
   ```
   - One node should report as **Leader**.
   - The others should report as **Followers**.

---

### **4. Verify the Zookeeper Cluster**

1. **Connect to Zookeeper CLI**:
   On any server, connect to the CLI:
   ```bash
   ./zkCli.sh -server 192.168.1.1:2181
   ```

2. **Check Cluster Details**:
   - List the cluster members:
     ```bash
     ls /zookeeper
     ```
   - Create a test znode:
     ```bash
     create /test_znode "Cluster Test"
     ```
   - Check the znode from another server:
     ```bash
     ./zkCli.sh -server 192.168.1.2:2181
     get /test_znode
     ```

If the data is consistent across servers, the cluster is working properly.

---

### **5. Integrate Kafka with Zookeeper**

#### **Update Kafka Broker Configuration**
1. On each Kafka broker, edit the `server.properties` file:
   ```bash
   nano /opt/kafka/config/server.properties
   ```

2. Update the `zookeeper.connect` property to point to the Zookeeper cluster:
   ```properties
   zookeeper.connect=192.168.1.1:2181,192.168.1.2:2181,192.168.1.3:2181
   ```

3. Save and close the file.

---

### **6. Start Kafka with Zookeeper Cluster**

1. Start each Kafka broker:
   ```bash
   kafka-server-start.sh /opt/kafka/config/server.properties
   ```

2. Verify that Kafka is connected to Zookeeper:
   - Open the Zookeeper CLI:
     ```bash
     ./zkCli.sh -server 192.168.1.1:2181
     ```
   - Check the registered Kafka brokers:
     ```bash
     ls /brokers/ids
     ```
   - Output should show the broker IDs, e.g., `[1, 2, 3]`.

---

### **Maintenance Tips**

1. **Monitoring**:
   - Use Prometheus and Grafana for monitoring Zookeeper metrics.
   - Install a Zookeeper exporter, such as [zookeeper-exporter](https://github.com/dabealu/zookeeper-exporter).

2. **Scaling**:
   - Add new nodes by updating `zoo.cfg` and assigning a new `myid`.

3. **Backups**:
   - Regularly back up the `dataDir` directory.

4. **Logs**:
   - Monitor Zookeeper logs for errors:
     ```bash
     tail -f /opt/zookeeper/logs/zookeeper.out
     ```

---

### **Summary**

- **Cluster Setup**:
  - Configure 3+ Zookeeper nodes with unique `myid`.
  - Update `zoo.cfg` with server details.

- **Integration**:
  - Point Kafka brokers to the Zookeeper cluster using `zookeeper.connect`.

- **Verification**:
  - Use Zookeeper CLI to check cluster status and test data consistency.

Let me know if you’d like help with specific steps or advanced configurations! 😊
