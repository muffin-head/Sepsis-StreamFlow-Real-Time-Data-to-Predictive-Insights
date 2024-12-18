# IAC ADLS deployment with data
To deploy Infrastructure as Code (IaC) for Azure Data Lake Storage using Terraform via GitHub, kindly refer to the repository [Azure-Terraform-Storage-IaC](https://github.com/muffin-head/ADLS_terraform).

# Wiki for Training a Machine Learning Model on Databricks Using MLflow

This guide walks you through the steps of using Databricks to preprocess data, train machine learning models, and log results to MLflow.

---

### **1. Initialize and Load Data**

1. **Initialize SparkSession**
   - SparkSession is required for managing Spark operations.
   ```python
   from pyspark.sql import SparkSession
   spark = SparkSession.builder.appName("ModelPreparation").getOrCreate()
   ```

2. **Load Silver Layer Data**
   - Load data from the Silver layer in the Azure Data Lake.
   ```python
   silver_path = "/mnt/silver/silver_data.parquet"
   silver_df = spark.read.parquet(silver_path)
   ```

3. **Convert to Pandas**
   - For processing, convert the Spark DataFrame to Pandas.
   ```python
   silver_pd_df = silver_df.toPandas()
   ```

---

### **2. Preprocess Data**

1. **Select Features and Label**
   - Define features and the target label for the model.
   ```python
   features = [
       "MDC_PULS_OXIM_PULS_RATE_Result_min",
       "MDC_TEMP_Result_mean",
       "MDC_PULS_OXIM_PULS_RATE_Result_mean",
       "HR_to_RR_Ratio"
   ]
   X = silver_pd_df[features]
   y = silver_pd_df["Label"]
   ```

2. **Handle Missing and Infinite Values**
   - Replace `inf` and `-inf` with `NaN` and fill missing values with 0.
   ```python
   X.replace([np.inf, -np.inf], np.nan, inplace=True)
   X.fillna(0, inplace=True)
   ```

3. **Split Data**
   - Split the data into training and testing sets.
   ```python
   from sklearn.model_selection import train_test_split
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
   ```

4. **Standard Scaling**
   - Standardize features by removing the mean and scaling to unit variance.
   ```python
   from sklearn.preprocessing import StandardScaler
   scaler = StandardScaler()
   X_train_scaled = scaler.fit_transform(X_train)
   X_test_scaled = scaler.transform(X_test)
   ```

---

### **3. Log Scaler with MLflow**

1. **Set Up MLflow Experiment**
   - Define an MLflow experiment for logging.
   ```python
   import mlflow
   mlflow.set_tracking_uri("databricks")
   experiment_name = "/Users/<your-email>/silver_layer_scaler_experiment1"
   mlflow.set_experiment(experiment_name)
   ```

2. **Log Scaler**
   - Save the scaler for use in future real-time applications.
   ```python
   with mlflow.start_run(run_name="scaler_silver_layer"):
       mlflow.sklearn.log_model(scaler, artifact_path="standard_scaler")
       print("Scaler saved to MLflow successfully!")
   ```

---

### **4. Train Models with Hyperparameter Tuning**

1. **Define Model Training Function**
   - Train and log models with metrics.
   ```python
   from sklearn.metrics import f1_score
   from sklearn.model_selection import RandomizedSearchCV

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

2. **Train Multiple Models**
   - Define and train multiple models using a dictionary.
   ```python
   from sklearn.ensemble import RandomForestClassifier
   from xgboost import XGBClassifier
   from lightgbm import LGBMClassifier

   models = {
       "RandomForest": (RandomForestClassifier(), {"n_estimators": [50, 100, 200], "max_depth": [3, 5, 10]}),
       "XGBoost": (XGBClassifier(use_label_encoder=False, eval_metric='logloss'), {"n_estimators": [50, 100], "learning_rate": [0.01, 0.1], "max_depth": [3, 5]}),
       "LightGBM": (LGBMClassifier(), {"n_estimators": [50, 100], "learning_rate": [0.01, 0.1], "max_depth": [-1, 5]})
   }

   for model_name, (model, params) in models.items():
       train_and_log_model(model, params, model_name)
   ```

---

### **5. Monitor MLflow Dashboard**

- To view experiment details:
  - Open the Databricks MLflow UI by navigating to the **MLflow Experiment** page:
    ```plaintext
    https://<databricks-workspace-url>/ml/experiments/<experiment_id>
    ```
- Inspect logged models, metrics, and parameters.

---

### **6. Summary**

This notebook demonstrates:
- Loading data from Azure Data Lake.
- Preprocessing data.
- Training multiple models with hyperparameter tuning.
- Logging models and metrics using MLflow for reproducibility and comparison.

This setup ensures scalability and effective model tracking in Databricks.
