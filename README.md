# Dataflow Flex Template: a pipeline with dependencies and a custom container image.

This document guides you through using gcloud commands to create, build, and run a Flex Template Dataflow job for a "Deliver Report" pipeline. This pipeline likely processes data stored in Cloud Storage (CSV format) to generate reports.


A Google Cloud Project with the Cloud Dataflow API enabled.
The gcloud command-line tool installed and configured for your project.
A Cloud Storage bucket (df-pipeline-deliver-report) containing the following files:
template/df-pipeline-deliver-report-py.json: The Flex Template spec file.
metadata.json (Optional): Metadata for the Flex Template image.
requirements.txt (Optional): Python dependencies for the pipeline.
df_deliver_report.py: The Python script for the Dataflow pipeline.
Steps:


# Data Pipeline: CSV to BigQuery

## Overview

This repository contains a data pipeline that automates the process of cleaning, filtering, and loading CSV data from Google Cloud Storage (GCS) into Google BigQuery. The pipeline is triggered by new CSV file uploads to a specified GCS bucket and utilizes Google Cloud Functions and Dataflow Flex template.

## Architecture

The pipeline consists of the following components:

1. **Google Cloud Storage (GCS)**: Used as the storage location for incoming CSV files.

2. **Cloud Functions**: An event-triggered function that listens for new CSV file uploads to GCS. Upon detection of a new file, it triggers the Dataflow Flex template.

3. **Dataflow Flex Template**: A flexible Dataflow pipeline template designed to handle data processing tasks. In this pipeline, it reads the CSV data from GCS, performs cleaning and filtering operations, and then loads the processed data into BigQuery.

4. **Google BigQuery**: A fully managed, serverless data warehouse for analytics. It serves as the destination for the cleaned and filtered data.

## Setup Instructions

### 1. Google Cloud Storage (GCS)

- Create a GCS bucket where your CSV files will be uploaded.
- Ensure that appropriate permissions are set to allow Cloud Functions to access this bucket.

### 2. Cloud Functions

- Write a Cloud Function that is triggered upon CSV file upload to your GCS bucket.
- Configure the Cloud Function to trigger the Dataflow Flex template upon detection of a new CSV file.

### 3. Dataflow Flex Template

- Develop a Dataflow Flex template that reads CSV data from GCS, cleans and filters it according to your requirements, and loads the processed data into BigQuery.
- Configure the template to receive input parameters such as GCS bucket and file paths.

### 4. Google BigQuery

- Create a dataset within BigQuery where the cleaned data will be stored.
- Ensure that the Dataflow Flex template has the necessary permissions to write data into BigQuery.

## Usage

1. Upload your CSV file to the designated GCS bucket.
2. The Cloud Function will automatically trigger the Dataflow Flex template.
3. The Dataflow Flex template will process the data, clean it, filter it, and load it into BigQuery.
4. Once completed, the cleaned data will be available for querying and analysis within BigQuery.

## Notes

- Ensure that all components are properly configured with appropriate permissions and access controls.
- Monitor pipeline performance and resource usage to optimize efficiency and cost-effectiveness.
- Customize the cleaning and filtering operations within the Dataflow Flex template according to your specific data requirements.

## Contributors

- [Ankit Utkarsh](https://github.com/ankitsrm) - Contact Information

# Prerequisites:

A Google Cloud Project with the Cloud Dataflow API enabled.
The gcloud command-line tool installed and configured for your project.
A Cloud Storage bucket `(df-pipeline-deliver-report)` containing the following files:

-`template/df-pipeline-deliver-report-py.json`: The Flex Template spec file.
-`metadata.json (Optional)`: Metadata for the Flex Template image.
-`requirements.txt (Optional)`: Python dependencies for the pipeline.
-`df_deliver_report.py`: The Python script for the Dataflow pipeline.


# Create an Artifact Repository (Optional):

```sh
    gcloud artifacts repositories create dataflowjobs-flex-template \
        --repository-format=docker --location=asia-south1
```

# Build the Flex Template Image:
```sh
    gcloud dataflow flex-template build gs://df-pipeline-deliver-report/template/df-pipeline-deliver-report-py.json \
    --image-gcr-path "asia-south1-docker.pkg.dev/bigquery-418908/dataflowjobs-flex-template/df-pipeline-deliver-report-py:latest" \
    --sdk-language "PYTHON" \
    --flex-template-base-image "PYTHON3" \
    --py-path "." \
    --metadata-file "metadata.json" \
    --env "FLEX_TEMPLATE_PYTHON_PY_FILE=df_deliver_report.py" \
    --env "FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE=requirements.txt" \
    --temp-location="gs://df-pipeline-deliver-report/temp" \
    --staging-location="gs://df-pipeline-deliver-report/staging"
```

# Run the Flex Template:
```sh
gcloud dataflow flex-template run "flex-`date +%Y%m%d-%H%M%S`" \
    --template-file-gcs-location "gs://df-pipeline-deliver-report/template/df-pipeline-deliver-report-py.json" \
    --region us-east1 \
    --parameters input=gs://testdf_bucket/sampl.csv
```
