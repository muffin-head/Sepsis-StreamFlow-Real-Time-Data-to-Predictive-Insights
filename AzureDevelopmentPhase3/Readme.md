### Phase 3: CI/CD Pipeline with GitHub Actions - Successful Completion


#### Objective
Automate the deployment process to streamline the model lifecycle from staging to production with minimal manual intervention.

#### Steps Accomplished

1. **Version Control**
   - All model training, preprocessing, and deployment scripts are stored and version-controlled in a GitHub repository.

2. **GitHub Actions Pipeline**
   - **Trigger**: The pipeline activates when a model reaches the Staging stage in MLflow or when code changes are pushed to the repository.
   - **Pipeline Steps**:
     - Pull the model from the MLflow Registry.
     - Containerize the model using Docker.
     - Push the Docker image to the Azure Container Registry (ACR).
     - Deploy the containerized model to Azure Kubernetes Service (AKS).

3. **CI/CD Pipeline Structure**
   - **Model Validation**: Basic tests were conducted to ensure the integrity and reliability of the model.
   - **Containerization**: The model and dependencies were packaged into a Docker container.
   - **Deployment**: The containerized model was successfully deployed to AKS.

#### Relevant Links

1. **Deploying Infrastructure as Code (IaC:acr,aks)**
   - [IaC Deployment Documentation](https://github.com/muffin-head/ACR_AKS_terraform)
  
2. **Deploying Infrastructure as Code (IaC:EventHub)**
   - [IaC Deployment Documentation](https://github.com/muffin-head/eventhub_deployment)

3. **CI/CD Model Deployment**
   - [CI/CD Pipeline Documentation](https://github.com/muffin-head/CICD_modelDeployment)

#### Note
The repository contains files for storage, including configurations and scripts. For further details on redeploying the model or infrastructure, please refer to the above reference link in the respective links.

---

