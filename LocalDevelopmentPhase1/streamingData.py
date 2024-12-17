import faust
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn

# ------------------------------
# Faust Record for Input Data
# ------------------------------
class PatientData(faust.Record, serializer='json'):
    patient_id: str
    MDC_PULS_OXIM_PULS_RATE_Result: float
    MDC_TEMP_Result: float
    MDC_ECG_HEART_RATE_Result: float
    MDC_TTHOR_RESP_RATE_Result: float

# ------------------------------
# Faust App Setup
# ------------------------------
app = faust.App(
    'real-time-ml-pipeline',
    broker='kafka://127.0.0.1:9092',
    value_serializer='json'  # JSON deserialization
)

# Topics
input_topic = app.topic('input-topic', value_type=PatientData)
output_topic = app.topic('output-topic', value_type=dict)

# ------------------------------
# Load Scaler and Model from MLflow
# ------------------------------
mlflow.set_tracking_uri("file:///media/muffin/F/Sepsis/mlruns")

# Load Best Model
best_run_id = '98c13481aaff40eb864fe865e72e5651'
model_url = f"runs:/{best_run_id}/RandomForest"
model = mlflow.sklearn.load_model(model_url)

# Load Scaler
scaler_id = 'd8f7faa6fb0346c28b842da7006461fe'
scaler_url = f"runs:/{scaler_id}/standard_scaler"
scaler = mlflow.sklearn.load_model(scaler_url)

# ------------------------------
# Faust Agent for Processing
# ------------------------------
@app.agent(input_topic)
async def process_patient_data(stream):
    async for message in stream:
        print(f"Received data: {message}")

        try:
            # Convert incoming data into a DataFrame-like structure
            features = pd.DataFrame([{
                'MDC_PULS_OXIM_PULS_RATE_Result_min': message.MDC_PULS_OXIM_PULS_RATE_Result,
                'MDC_TEMP_Result_mean': message.MDC_TEMP_Result,
                'MDC_PULS_OXIM_PULS_RATE_Result_mean': message.MDC_PULS_OXIM_PULS_RATE_Result,
                'HR_to_RR_Ratio': message.MDC_ECG_HEART_RATE_Result / message.MDC_TTHOR_RESP_RATE_Result
            }])

            print("Extracted Features:")
            print(features)

            # Scale features
            scaled_features = scaler.transform(features)
            print("Scaled Features:", scaled_features)

            # Get prediction probabilities
            probabilities = model.predict_proba(scaled_features)[0]  # Probabilities for each class

            print(f"Prediction Probabilities: {probabilities}")

            # Prepare and send result
            result = {
                'patient_id': message.patient_id,
                'prediction_probabilities': [float(prob) for prob in probabilities],  # Convert to standard floats
                'original_data': message.asdict()
            }

            print("Sending prediction probabilities to Kafka...")
            await output_topic.send(value=result)
            print(f"Prediction probabilities sent: {result}")

        except Exception as e:
            print(f"Error during prediction: {e}")

# ------------------------------
# Run Faust Worker:
# faust -A streamingData worker --loglevel=info
# ------------------------------
