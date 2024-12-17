from kafka import KafkaProducer
import pandas as pd
import json
import time

# Kafka Producer Setup
producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON serializer
)

# Load Patient Data from CSV
csv_file = 'patient3.csv'
df = pd.read_csv(csv_file)

# Rename the columns to match required names
df.rename(columns={
    'Patient ID': 'patient_id',
    'MDC_PULS_OXIM_PULS_RATE_Result': 'MDC_PULS_OXIM_PULS_RATE_Result',
    'MDC_TEMP_Result': 'MDC_TEMP_Result',
    'MDC_ECG_HEART_RATE_Result': 'MDC_ECG_HEART_RATE_Result',
    'MDC_TTHOR_RESP_RATE_Result': 'MDC_TTHOR_RESP_RATE_Result'
}, inplace=True)

# Ensure only required columns exist
required_columns = ["patient_id", "MDC_PULS_OXIM_PULS_RATE_Result", "MDC_TEMP_Result",
                    "MDC_ECG_HEART_RATE_Result", "MDC_TTHOR_RESP_RATE_Result"]

if not all(col in df.columns for col in required_columns):
    raise ValueError(f"CSV file must contain these columns: {required_columns}")

print("Starting Kafka producer...")

# Stream data row by row
while True:
    for _, row in df.iterrows():
        data = {
            "patient_id": row["patient_id"],
            "MDC_PULS_OXIM_PULS_RATE_Result": row["MDC_PULS_OXIM_PULS_RATE_Result"],
            "MDC_TEMP_Result": row["MDC_TEMP_Result"],
            "MDC_ECG_HEART_RATE_Result": row["MDC_ECG_HEART_RATE_Result"],
            "MDC_TTHOR_RESP_RATE_Result": row["MDC_TTHOR_RESP_RATE_Result"]
        }
        producer.send('input-topic', data)  # Send data to Kafka
        print(f"Sent: {data}")
    time.sleep(1)  # Simulate real-time streaming
