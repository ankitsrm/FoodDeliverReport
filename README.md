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
