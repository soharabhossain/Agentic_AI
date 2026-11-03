# Deploy your Agent on GCP using CloudRun

---

## Environment setup on Google Cloud Platform

i. Sign-in to the Google Cloud Console

ii. Create a New Project or reuse an existing one.

iii. Note the project ID.

iv. Enable Billing.

## Start Cloud Shell

---

[optional] Navigate to Cloud Shell Editor if you wish to use the GUI editor to create the files.
e.g.
cloudshell edit requirements.txt

---

You may use the CloudShell CLI to run the following commands.

### List GCP projects

gcloud projects list | awk '/PROJECT_ID/{print $2}'

### Set project

gcloud config set project [YOUR-PROJECT-ID]

---

## Setup your Environment - Enable APIs and set environment variables and all necessary services:

You may use the CloudShell CLI to run the commands.

gcloud services enable  run.googleapis.com  artifactregistry.googleapis.com  cloudbuild.googleapis.com  aiplatform.googleapis.com

---

## Set Environment variables for your current project ID, project number and also create a dedicated service account for your project.

export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
export SA_NAME=agentic-ai-course-service
export SERVICE_ACCOUNT="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

---

gcloud iam service-accounts create ${SA_NAME} \
 --display-name="Service Account for Agentic AI Course "

---

## Grant Vertex AI User role so it can talk to Gemini models

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
 --role="roles/aiplatform.user"

# [optional] Verification: Run the following command to check that the service account is successfully bound to the role

gcloud projects get-iam-policy ${PROJECT_ID} \
    --flatten="bindings[].members" \
    --filter="bindings.members:${SERVICE_ACCOUNT}"

---

## Create the project directory.

This command creates project root folder 'coder' for the agent's source code.

cd && mkdir coder && cd coder

Create all the files inside this folder.

> requirements.txt
> .env
> **init**.py
> agent.py

+++++++++++++++++++++++++++++++++++++++

## Run the Deployment Command from CloudShell CLI

uvx --from google-adk==1.14.0 \
adk deploy cloud_run \
 --project=$PROJECT_ID \
  --region=asia-south2 \
  --service_name=agentic-ai-course-service \
  --with_ui \
  . \
  -- \
  --labels=deployment-tutorial=agentic-ai-course \
  --service-account=$SERVICE_ACCOUNT

Give permissionsL

Do you want to continue (Y/n)? Y

Allow unauthenticated invocations to [agentic-ai-course-service] (y/N)? y

Note down the public service URL of the CloudRun app after the successful deployment.

It will be similarr to the following:
Service URL: https://agentic-ai-course-service-879665146982.asia-south2.run.app

Open it in a browser.

---

## Clean up Environment - Delete the Cloud Run service itself, the temporary files in /tmp, and the Artifact Registry container repository, etc.

### Delete the Service

gcloud run services delete agentic-ai-course-service --region=asia-south2 --quiet

### Delete the Artifact Registry

gcloud artifacts repositories delete cloud-run-source-deploy --location=asia-south2 --quiet

### Delete the Service Account

gcloud iam service-accounts delete agentic-ai-course-service@${SERVICE_ACCOUNT}.iam.gserviceaccount.com
--quiet
