### Wiki for Creating an Event Hub Namespace with Capture and Storage Setup in Azure Portal

1. **Create an Event Hub Namespace**
   - Go to the **Azure Portal** and search for **Event Hubs**.
   - Click **+ Create** to start creating a namespace.
   - Fill in the required fields:
     - **Namespace Name**: Enter a unique name (e.g., `streamingdatasepsis`).
     - **Pricing Tier**: Choose **Standard** (required for Capture).
     - **Region**: Select the region closest to your application.
   - Click **Review + Create** and then **Create**.

2. **Create a Storage Account for Capture**
   - In the Azure Portal, search for **Storage Accounts** and click **+ Create**.
   - Fill in the required fields:
     - **Name**: Enter a unique name for the storage account.
     - **Performance/Redundancy**: Choose based on your needs (default settings are usually fine).
   - Once created, go to the **Storage Account**, navigate to **Containers**, and create a new container for storing Event Hub data (e.g., `eventhubcapture`).

3. **Enable Capture on the Event Hub**
   - Go to your Event Hub namespace and click on **Event Hubs**.
   - Create a new Event Hub:
     - Enter a name (e.g., `streamingeventhub`).
     - Set **Message Retention** and **Partition Count** as required.
   - After creation, click on the Event Hub and go to the **Capture** tab.
   - Enable **Capture**, and set:
     - **Capture Provider**: Azure Storage.
     - **Storage Account**: Select the storage account you created.
     - **Container**: Select the container you created earlier.
   - Save the configuration.

---

### Wiki for the Python Script to Send Data to Event Hub

1. **Install Required Libraries**
   - Run the following command to install the Azure Event Hub SDK:
     ```bash
     pip install azure-eventhub
     ```

2. **Purpose of the Script**
   - The script sends JSON data from a file (`test.json`) to the Azure Event Hub.

3. **Steps in the Script**
   - Import required libraries.
   - Create an **EventHubProducerClient** using the connection string and WebSocket transport type.
   - Open the `test.json` file, read its content, and create an **EventData** batch.
   - Add the JSON data to the batch and send it to the Event Hub.
   - Close the producer connection.

4. **Running the Script**
   - Save the script as `send_to_eventhub.py`.
   - Ensure the file `test.json` is in the same folder as the script.
   - Run the script:
     ```bash
     python send_to_eventhub.py
     ```

5. **Sample JSON Data**
   - Ensure `test.json` has valid JSON data, e.g.:
     ```json
     {"idDrink": "11002", "strDrink": "Cocktail", "dateModified": "2015-08-18 15:12:07"}
     ```
