# Streaming Code explaination

## **What Does This Code Do?**
1. **Receives streaming data** (real-time data) from Kafka.
2. Processes the data to create the required **features**.
3. Scales the features using a **pre-trained scaler** (to normalize data).
4. Predicts **probabilities** for each class using a **pre-trained RandomForest model**.
5. Sends the **predicted probabilities** and original data back to Kafka.

---

## **Step-by-Step Explanation**

### **1. Import Required Libraries**
```python
import faust
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
```
- **`faust`**: A library to process real-time streaming data.
- **`pandas`**: To structure the incoming data into a DataFrame (like an Excel table).
- **`mlflow`**: To load a pre-trained machine learning model and scaler for predictions.

---

### **2. Define the Incoming Data Structure**
```python
class PatientData(faust.Record, serializer='json'):
    patient_id: str
    MDC_PULS_OXIM_PULS_RATE_Result: float
    MDC_TEMP_Result: float
    MDC_ECG_HEART_RATE_Result: float
    MDC_TTHOR_RESP_RATE_Result: float
```

- **What’s Happening Here?**
   - This is a **data schema** that describes the structure of the incoming Kafka message.
   - It says that every message will have:
     - `patient_id`: a string (e.g., "patient123").
     - `MDC_PULS_OXIM_PULS_RATE_Result`: a float (e.g., 98.5).
     - `MDC_TEMP_Result`: a float (e.g., 37.5).
     - `MDC_ECG_HEART_RATE_Result`: a float (e.g., 80.0).
     - `MDC_TTHOR_RESP_RATE_Result`: a float (e.g., 20.0).

---

### **3. Set Up the Faust Streaming Application**
```python
app = faust.App(
    'real-time-ml-pipeline',
    broker='kafka://127.0.0.1:9092',
    value_serializer='json'
)
```
- **What’s Happening?**
   - A **Faust application** named `real-time-ml-pipeline` is created.
   - It connects to a **Kafka broker** running on `127.0.0.1:9092` (your local Kafka setup).
   - It processes messages serialized as JSON.

---

### **4. Define Kafka Topics**
```python
input_topic = app.topic('input-topic', value_type=PatientData)
output_topic = app.topic('output-topic', value_type=dict)
```
- **What’s Happening?**
   - **`input-topic`**: The Kafka topic where incoming messages (patient data) are streamed.
   - **`output-topic`**: The Kafka topic where predictions will be sent.

---

### **5. Load the Pre-Trained Model and Scaler**
```python
mlflow.set_tracking_uri("file:///media/muffin/F/Sepsis/mlruns")

best_run_id = '98c13481aaff40eb864fe865e72e5651'
model_url = f"runs:/{best_run_id}/RandomForest"
model = mlflow.sklearn.load_model(model_url)

scaler_id = 'd8f7faa6fb0346c28b842da7006461fe'
scaler_url = f"runs:/{scaler_id}/standard_scaler"
scaler = mlflow.sklearn.load_model(scaler_url)
```

- **What’s Happening?**
   - The **pre-trained RandomForest model** and **scaler** are loaded using MLflow.
   - `model.predict_proba` will predict the probabilities for each class.
   - `scaler.transform` will scale the input features to match what the model expects.

---

### **6. Process Incoming Messages and Predict**
```python
@app.agent(input_topic)
async def process_patient_data(stream):
    async for message in stream:
        print(f"Received data: {message}")
```
- **What’s Happening?**
   - The Faust agent listens to the `input-topic` Kafka stream.
   - For each message, it starts processing.

---

### **7. Extract Features from Incoming Data**
```python
features = pd.DataFrame([{
    'MDC_PULS_OXIM_PULS_RATE_Result_min': message.MDC_PULS_OXIM_PULS_RATE_Result,
    'MDC_TEMP_Result_mean': message.MDC_TEMP_Result,
    'MDC_PULS_OXIM_PULS_RATE_Result_mean': message.MDC_PULS_OXIM_PULS_RATE_Result,
    'HR_to_RR_Ratio': message.MDC_ECG_HEART_RATE_Result / message.MDC_TTHOR_RESP_RATE_Result
}])
```
- **What’s Happening?**
   - Incoming message data is converted into a **DataFrame** (table format).
   - Features are extracted:
     - The current pulse rate, temperature, and ratios of heart rate to respiration rate.

---

### **8. Scale Features and Predict Probabilities**
```python
scaled_features = scaler.transform(features)
probabilities = model.predict_proba(scaled_features)[0]
```
- **`scaler.transform(features)`**: Scales the features to match the model’s input requirements.
- **`model.predict_proba`**: Predicts the probabilities for each class.

For example, probabilities might look like this for a binary classification problem:
```python
[0.85, 0.15]
```
This means:
- Class 0: 85% probability.
- Class 1: 15% probability.

---

### **9. Send Predictions to Kafka**
```python
result = {
    'patient_id': message.patient_id,
    'prediction_probabilities': [float(prob) for prob in probabilities],
    'original_data': message.asdict()
}

await output_topic.send(value=result)
print(f"Prediction probabilities sent: {result}")
```
- **What’s Happening?**
   - A dictionary containing the patient ID, predicted probabilities, and original data is created.
   - This dictionary is sent to the **output-topic** in Kafka.

---

### **10. Running the Faust Worker**
At the bottom, you see:
```bash
faust -A streamingData worker --loglevel=info
```
- This starts the **Faust application worker**.
- It connects to Kafka, listens to the `input-topic`, processes messages, and sends results to `output-topic`.

---

## **Why is This Code Useful?**

1. **Real-Time Processing**:
   - It processes patient data as soon as it arrives in Kafka.

2. **Feature Engineering**:
   - It extracts features (like ratios) from incoming data for use in the model.

3. **Machine Learning Predictions**:
   - It uses a pre-trained model to predict probabilities in real-time.

4. **Integration with Kafka**:
   - Results are sent to a Kafka topic (`output-topic`), which can be consumed by other systems (e.g., dashboards, alerts).

5. **Scalable**:
   - You can add more Kafka topics or scale Faust workers to handle more data.

---

# Kafka producer code explaination

Here is an updated version of your **Kafka Producer** script with explanations added step by step and the logic clearly separated. I will keep the functionality intact while cleaning it up for clarity.

---

## **Revised Kafka Producer Code**

### Key Features:
1. Streams patient data row-by-row from a CSV file to Kafka.
2. Ensures required columns exist in the CSV file.
3. Sends each row as a **JSON-encoded message** to the Kafka topic **`input-topic`**.
4. Simulates **real-time streaming** with a delay of 1 second per loop.

---

### Code:
```python
from kafka import KafkaProducer
import pandas as pd
import json
import time

# ------------------------------
# Kafka Producer Setup
# ------------------------------
producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',  # Kafka broker address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize messages to JSON
)

# ------------------------------
# Load and Validate Patient Data
# ------------------------------
# Load CSV file
csv_file = 'patient3.csv'  # Update this path if needed
df = pd.read_csv(csv_file)

# Rename columns to standardize names (if needed)
df.rename(columns={
    'Patient ID': 'patient_id',
    'MDC_PULS_OXIM_PULS_RATE_Result': 'MDC_PULS_OXIM_PULS_RATE_Result',
    'MDC_TEMP_Result': 'MDC_TEMP_Result',
    'MDC_ECG_HEART_RATE_Result': 'MDC_ECG_HEART_RATE_Result',
    'MDC_TTHOR_RESP_RATE_Result': 'MDC_TTHOR_RESP_RATE_Result'
}, inplace=True)

# Validate required columns
required_columns = ["patient_id", "MDC_PULS_OXIM_PULS_RATE_Result", 
                    "MDC_TEMP_Result", "MDC_ECG_HEART_RATE_Result", 
                    "MDC_TTHOR_RESP_RATE_Result"]

if not all(col in df.columns for col in required_columns):
    raise ValueError(f"CSV file must contain these columns: {required_columns}")

print("Patient data loaded and validated successfully.")
print(f"Streaming {len(df)} records to Kafka topic 'input-topic'...")

# ------------------------------
# Stream Data Row by Row to Kafka
# ------------------------------
try:
    while True:  # Infinite loop for continuous streaming
        for _, row in df.iterrows():
            # Prepare the message as a JSON-compatible dictionary
            data = {
                "patient_id": str(row["patient_id"]),  # Convert to string for consistency
                "MDC_PULS_OXIM_PULS_RATE_Result": float(row["MDC_PULS_OXIM_PULS_RATE_Result"]),
                "MDC_TEMP_Result": float(row["MDC_TEMP_Result"]),
                "MDC_ECG_HEART_RATE_Result": float(row["MDC_ECG_HEART_RATE_Result"]),
                "MDC_TTHOR_RESP_RATE_Result": float(row["MDC_TTHOR_RESP_RATE_Result"])
            }
            
            # Send the message to the Kafka topic
            producer.send('input-topic', data)
            print(f"Sent: {data}")
        
        # Simulate real-time streaming delay
        time.sleep(1)

except KeyboardInterrupt:
    print("Kafka producer stopped by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    producer.close()
    print("Kafka producer closed.")
```

---

## **Key Changes and Improvements**
1. **Error Handling**:
   - Added a `try-except` block to handle interruptions or unexpected errors gracefully.
   - The `finally` block ensures the Kafka producer is properly closed.

2. **Column Validation**:
   - Ensures all required columns exist in the CSV file before starting streaming.

3. **Data Type Standardization**:
   - Ensures all values sent to Kafka are **JSON-compatible**:
     - `patient_id` → `str` (string)
     - Other values → `float`

4. **Clear Output**:
   - Logs each message being sent to Kafka.

5. **Graceful Exit**:
   - Allows stopping the producer with `Ctrl+C` (KeyboardInterrupt).

---

## **What Does This Script Do?**

1. **Loads Data**:
   - Reads a CSV file containing patient data.

2. **Validates Data**:
   - Ensures the required columns are present in the CSV file.

3. **Streams Data**:
   - Sends each row of data, serialized as a JSON message, to the Kafka topic `input-topic`.

4. **Simulates Real-Time Streaming**:
   - Adds a delay (`time.sleep(1)`) after each full pass through the data to mimic real-time data streaming.

5. **Handles Interruptions**:
   - Allows you to stop the producer safely using `Ctrl+C`.

---

## **Example Output**
When you run the script, you should see output like this in your terminal:
```
Patient data loaded and validated successfully.
Streaming 100 records to Kafka topic 'input-topic'...
Sent: {'patient_id': '123', 'MDC_PULS_OXIM_PULS_RATE_Result': 85.0, 'MDC_TEMP_Result': 37.5, 'MDC_ECG_HEART_RATE_Result': 120.0, 'MDC_TTHOR_RESP_RATE_Result': 18.0}
Sent: {'patient_id': '124', 'MDC_PULS_OXIM_PULS_RATE_Result': 90.0, 'MDC_TEMP_Result': 38.2, 'MDC_ECG_HEART_RATE_Result': 110.0, 'MDC_TTHOR_RESP_RATE_Result': 20.0}
...
```

---

## **How to Run**

1. Make sure your **Kafka broker** is running:
   ```bash
   zookeeper-server-start.sh config/zookeeper.properties
   kafka-server-start.sh config/server.properties
   ```

2. Create the topic `input-topic` (if it doesn’t exist):
   ```bash
   kafka-topics.sh --create --topic input-topic --bootstrap-server 127.0.0.1:9092 --partitions 1 --replication-factor 1
   ```

3. Run the producer script:
   ```bash
   python kafkaProducer.py
   ```

4. Use a **Kafka consumer** to verify the messages:
   ```bash
   kafka-console-consumer.sh --topic input-topic --from-beginning --bootstrap-server 127.0.0.1:9092
   ```

# ML flow Local model development after feature importance is been done



## **Overview**
This script demonstrates **local model development** using the **MLflow tracking system**. It covers the following stages of machine learning workflow:

1. **Data Loading and Preparation**
2. **Feature Engineering**
3. **Data Preprocessing (Scaling)**
4. **Model Training and Hyperparameter Tuning** using `RandomizedSearchCV`.
5. **MLflow Integration** to:
   - Log experiments, parameters, metrics, and models.
   - Store preprocessing components (like scalers).
6. **Model Comparison** to identify the best performing model.

---

## **Step-by-Step Breakdown**

### **1. Data Loading and Preparation**

- The script loads and combines two datasets, `patient1.csv` and `patient2.csv`.
- `pandas` is used for data handling.

```python
df1 = pd.read_csv('patient1.csv')
df2 = pd.read_csv('patient2.csv')
combined_df = pd.concat([df1, df2], axis=0, ignore_index=True)
```

- **Why?**
   - Combining datasets provides a larger sample size, which improves model generalization.

---

### **2. Feature Engineering**

The script generates **4 derived features** using rolling windows and ratios:

```python
combined_df['MDC_PULS_OXIM_PULS_RATE_Result_min'] = combined_df['MDC_PULS_OXIM_PULS_RATE_Result'].rolling(window=2).min()
combined_df['MDC_TEMP_Result_mean'] = combined_df['MDC_TEMP_Result'].rolling(window=2).mean()
combined_df['MDC_PULS_OXIM_PULS_RATE_Result_mean'] = combined_df['MDC_PULS_OXIM_PULS_RATE_Result'].rolling(window=2).mean()
combined_df['HR_to_RR_Ratio'] = combined_df['MDC_ECG_HEART_RATE_Result'] / combined_df['MDC_TTHOR_RESP_RATE_Result']
```

- **What’s Happening?**
   - **Rolling Window**: Computes statistics (e.g., min, mean) over two consecutive rows.
   - **Ratios**: Calculate `HR_to_RR_Ratio` as the heart rate divided by respiration rate.

- **Purpose**:
   - These new features capture trends and relationships in the data, improving model performance.

---

### **3. Handling Missing and Infinite Values**

Rolling window operations can create **NaN values**. The script removes or replaces them:

```python
combined_df = combined_df.dropna().reset_index(drop=True)
X.replace([np.inf, -np.inf], np.nan, inplace=True)
X = X.fillna(0)  # Replace NaN with 0
```

---

### **4. Splitting the Data**

The data is split into training and test sets:

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

- **Why?**
   - Splitting ensures the model is evaluated on unseen data to avoid overfitting.

---

### **5. Feature Scaling**

The script uses `StandardScaler` to standardize the data:

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

- **Why Scaling?**
   - Scaling ensures all features are on a similar scale, improving model convergence.

---

### **6. Model Training and Hyperparameter Tuning**

The script defines a `train_and_log_model` function to:
- Perform hyperparameter tuning using **RandomizedSearchCV**.
- Log results and models using MLflow.

```python
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import f1_score

def train_and_log_model(model, param, model_name):
    with mlflow.start_run(run_name=model_name):
        mlflow.log_params(param)
        gridSearch = RandomizedSearchCV(model, param, cv=3, scoring='f1', random_state=42)
        gridSearch.fit(X_train_scaled, y_train)
        best_model = gridSearch.best_estimator_
        y_pred = best_model.predict(X_test_scaled)
        f1 = f1_score(y_test, y_pred)
        print(f'{model_name} F1 score is : {f1}')
        mlflow.log_metric('f1', f1)
        mlflow.sklearn.log_model(best_model, model_name)
```

- **What’s Happening?**
   1. **Hyperparameter Tuning**: `RandomizedSearchCV` explores combinations of hyperparameters.
   2. **Model Training**: The best model is selected and evaluated using **F1 score**.
   3. **MLflow Logging**:
      - **Parameters**: Logged with `mlflow.log_params`.
      - **Metrics**: F1 score is logged with `mlflow.log_metric`.
      - **Model**: Best model is logged using `mlflow.sklearn.log_model`.

---

### **7. Model Training Loop**

The script trains and evaluates models for multiple algorithms:

```python
from lightgbm import LGBMClassifier

models = {
    "LightGBM": (LGBMClassifier(), {"n_estimators": [50, 100], "learning_rate": [0.01, 0.1], "max_depth": [-1, 5]})
}

mlflow.set_experiment("sepsis_observation_sample_experiment")

for model_name, (model, params) in models.items():
    train_and_log_model(model, params, model_name)
```

- **Why?**
   - Iterates through different models and hyperparameter spaces.
   - Logs everything to MLflow for easy comparison.

---

### **8. Logging the Scaler**

The **scaler** is also logged to MLflow for later use:

```python
with mlflow.start_run():
    mlflow.sklearn.log_model(scaler, 'standard_scaler')
```

- **Why?**
   - Logging the scaler ensures the same preprocessing is applied during inference.

---

## **Summary of MLflow Logging**

MLflow logs the following:
1. **Experiment Name**: `sepsis_observation_sample_experiment`.
2. **Parameters**: Hyperparameter grid used for tuning.
3. **Metrics**: F1 score for model evaluation.
4. **Artifacts**: The trained model and scaler.

---

## **How to Run This Code**

1. **Install Dependencies**:
   Ensure required libraries are installed:
   ```bash
   pip install pandas numpy mlflow scikit-learn lightgbm
   ```

2. **Run MLflow Tracking Server**:
   Start the MLflow UI to view experiments:
   ```bash
   mlflow ui
   ```

   Open `http://localhost:5000` in a browser to view experiments.

3. **Run the Code**:
   Execute the script to train models and log everything to MLflow:
   ```bash
   python train_model.py
   ```

---

## **What This Script Achieves**
- Combines data and extracts meaningful features.
- Scales the data and ensures consistency for modeling.
- Performs hyperparameter tuning and model comparison.
- Logs experiments, metrics, and artifacts to **MLflow** for reproducibility.
- Enables easy comparison of models using MLflow's UI.

---

## **Why Use MLflow?**
1. **Experiment Tracking**:
   - Easily compare model runs, parameters, and metrics.
2. **Reproducibility**:
   - Log models and scalers to ensure consistent results.
3. **Scalability**:
   - Extend this workflow to other models or large datasets.

