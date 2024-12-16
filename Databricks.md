

### Wiki for Using Databricks to Read from Event Hub

1. **Set Up Databricks Cluster**
   - In Databricks, create a new **Cluster**:
     - Click on **Clusters** and then **+ Create Cluster**.
     - Enter a name, select a runtime version, and click **Create**.

2. **Install the Event Hub Library**
   - After the cluster is created, go to the **Libraries** tab.
   - Click **Install New** and choose **Maven**.
   - Enter the following Maven coordinate:
     ```
     com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.18
     ```
   - Install and restart the cluster if needed.

3. **Connect to Event Hub**
   - Use the following code to connect Databricks to your Event Hub:
     ```python
     from pyspark.sql.types import *
     import pyspark.sql.functions as F

     connectionString = "Endpoint=sb://streamingdatasepsis.servicebus.windows.net/;SharedAccessKeyName=eventhub;SharedAccessKey=g7fCnBi4CfJOKCpxjLrFY7nVdAUa8DUmM+AEhBcv+4M=;EntityPath=streamingeventhub"

     ehConf = {}
     ehConf["eventhubs.connectionString"] = sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connectionString)
     ehConf["eventhubs.consumerGroup"] = "$Default"
     ```

4. **Define the JSON Schema**
   - Define the schema for the JSON data:
     ```python
     json_schema = StructType([
         StructField("idDrink", StringType(), True),
         StructField("strDrink", StringType(), True),
         StructField("dateModified", StringType(), True),
     ])
     ```

5. **Read Data from Event Hub**
   - Stream data from the Event Hub:
     ```python
     df = spark.readStream.format("eventhubs").options(**ehConf).load()

     json_df = df.withColumn("body", F.from_json(df.body.cast("string"), json_schema))

     df3 = json_df.select(
         F.col("body.idDrink"), F.col("body.strDrink"), F.col("body.dateModified")
     )
     ```

6. **Write Data to Storage**
   - Write the processed data to Azure Blob Storage or ADLS:
     ```python
     df3.writeStream.format("json").outputMode("append").option(
         "checkpointLocation", "/mnt/..../..../checkpointapievents"
     ).start("/mnt/..../...")
     ```

7. **Run the Notebook**
   - Attach the notebook to the cluster and click **Run All** to start streaming.



To see the data written to Azure Blob Storage or Azure Data Lake Storage (ADLS), follow these steps:

---

### **1. Check Your Storage Path**

The data is written to the path you specify in the `.start()` method, which is:
```python
"/mnt/..../..."
```

In this path:
- `/mnt` refers to Databricks' **mount point** for Azure storage.
- Replace `..../...` with your actual directory path in Azure storage.

If you don't know the path:
1. Check the **mount configuration** in your Databricks environment.
2. Verify the storage account/container where you expect the data to be written.

---

### **2. Locate Data in Azure Storage**
To view the data:
1. **Azure Portal**:
   - Go to the **Storage Account** linked to your Databricks mount.
   - Navigate to the **Container** where the data is written.
   - Browse through the folder structure to find your JSON files.

2. **Databricks Notebook**:
   - Use the `dbutils` command to inspect the storage path directly:
     ```python
     dbutils.fs.ls("/mnt/..../...")
     ```
   - This will list all files in the specified path. You can also view the file contents:
     ```python
     display(spark.read.json("/mnt/..../..."))
     ```

---

### **3. Verify Checkpoint Location**
- The checkpoint location (`checkpointLocation`) ensures fault tolerance and keeps track of streaming progress.
- The checkpoint files are stored in the path:
  ```python
  "/mnt/..../..../checkpointapievents"
  ```
- You won't typically need to inspect these files unless debugging.

---

### **4. View Data in Azure Storage Explorer**
   - Download and install [Azure Storage Explorer](https://azure.microsoft.com/en-us/products/storage/storage-explorer/).
   - Connect it to your Azure account and navigate to the container and directory where the data is stored.
   - Open the JSON files to inspect the processed data.

---

### **5. Example Path in Azure**
For example:
- **Blob Storage Container**: `data-container`
- **Directory**: `processed-data/`
- **Databricks Mount**: `/mnt/blobmount`

The data might be accessible in **Azure Portal** under:
```
Storage Account > Containers > data-container > processed-data
```

Replace your `/mnt/...` path with its corresponding Azure storage container and directory. If you're still unsure about the path or storage account, review the storage mounting configuration in Databricks.
