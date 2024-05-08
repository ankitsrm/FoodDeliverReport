import functions_framework 
from functions_framework import CloudEvent 
from googleapiclient.discovery import build
import re

@functions_framework.cloud_event
def dataflow_trigger(cloud_event: CloudEvent) -> None:
    # Print received event ID and data
    print(f"Received event with ID: {cloud_event['id']} and data: {cloud_event.data}")
    
    # Extract necessary data from the event
    data = cloud_event.data
    bucket = data['bucket']
    file_name = data['name']
    file_path = f'gs://{bucket}/{file_name}'  # Corrected file_path format
    
    print(f'Dataflow input filepath: {file_path}')
    
    # Define project ID
    project_id = 'bigquery-418908'
    
    # Generate job name based on the timeCreated field
    job_name = generate_job_name(data, project_id)
    print(f"Job name: {job_name}")
    
    # Define environment variables for Dataflow job
    environment = {
        "temp_location": "gs://data_flow_temp_75229",  # Temp location for Dataflow
        "service_account_email": "biqg-75229@bigquery-418908.iam.gserviceaccount.com",  # Service account email
        "staging_location": "gs://data_flow_temp_75229/staging"  # Staging location for Dataflow
    }
    
    print(f"Environment variables: {environment}")
    
    # Define Dataflow template location
    df_temp_location = 'gs://your-bucket/getting_started_py.json'  # Replace 'your-bucket' with actual bucket name
    
    print(f"Dataflow template location: {df_temp_location}")
    
    # Define parameters for the Dataflow job
    parameters = {"input": file_path}  # Input parameter for the Dataflow job
    
    # Build Dataflow service
    dataflow_service = build('dataflow', 'v1b3', cache_discovery=False)
    
    # Launch Dataflow job using Flex Templates
    request = dataflow_service.projects().locations().flexTemplates().launch(
        projectId=project_id,
        location='us-central1',
        body={
            "launch_parameter": {
                "job_name": job_name,
                "parameters": parameters,
                "container_spec_gcs_path": df_temp_location,
                "environment": environment,
            }
        }
    )

    # Execute the request to launch the Dataflow job
    response = request.execute()
    print(f"Dataflow job launched with ID: {response['job']['id']}")

# Function to generate a job name based on the timeCreated field
def generate_job_name(data, project_id) -> str:
    year = data['timeCreated'][:4]
    month = data['timeCreated'][5:7]
    day = data['timeCreated'][8:10]

    # Generate a job name compliant with the naming conventions
    job_name = f"{project_id}-{year}-{month}-{day}"
    job_name = re.sub('[^a-zA-Z0-9-]', '-', job_name)  # Replace non-compliant characters with '-'
    job_name = re.sub('-+', '-', job_name)  # Replace consecutive '-' with single '-'
    job_name = job_name.strip('-')  # Remove leading/trailing '-'

    return job_name
