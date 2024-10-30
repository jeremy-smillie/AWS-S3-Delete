import boto3
import os
from concurrent.futures import ThreadPoolExecutor  # Import ThreadPoolExecutor
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from boto3.s3.transfer import TransferConfig

# Initialize the S3 client with retry configuration
s3 = boto3.client('s3', config=Config(retries={'max_attempts': 10, 'mode': 'standard'}))

# Specify the S3 bucket name
bucket_name = '{enter bucket name here}'
folder_prefix = '{enter folder or directory here or leave blank to delte all}'

deleted_files_count = 0  # Counter for deleted files

# Function to delete a batch of objects
def delete_batch(delete_keys):
    global deleted_files_count
    if delete_keys['Objects']:
        response = s3.delete_objects(Bucket=bucket_name, Delete=delete_keys)
        batch_count = len(delete_keys['Objects'])
        deleted_files_count += batch_count
        print(f"Deleted {batch_count} files... Total deleted so far: {deleted_files_count}")

# Main function to list and delete objects in parallel
def delete_s3_folder_parallel():
    global deleted_files_count
    with ThreadPoolExecutor(max_workers=30) as executor:  # Adjust max_workers based on your available resources
        while True:
            response = s3.list_object_versions(Bucket=bucket_name, Prefix=folder_prefix)
            
            if 'Versions' not in response and 'DeleteMarkers' not in response:
                print("No more files to delete.")
                break

            # Prepare delete requests in batches of 1000
            delete_keys = {'Objects': []}
            futures = []

            # Handle object versions
            for version in response.get('Versions', []):
                delete_keys['Objects'].append({'Key': version['Key'], 'VersionId': version['VersionId']})
                if len(delete_keys['Objects']) >= 1000:
                    # Submit delete task to executor
                    futures.append(executor.submit(delete_batch, delete_keys))
                    delete_keys = {'Objects': []}

            # Handle delete markers
            for marker in response.get('DeleteMarkers', []):
                delete_keys['Objects'].append({'Key': marker['Key'], 'VersionId': marker['VersionId']})
                if len(delete_keys['Objects']) >= 1000:
                    # Submit delete task to executor
                    futures.append(executor.submit(delete_batch, delete_keys))
                    delete_keys = {'Objects': []}

            # Delete any remaining objects in the batch
            if delete_keys['Objects']:
                futures.append(executor.submit(delete_batch, delete_keys))

            # Wait for all delete tasks to complete before checking for more files
            for future in futures:
                future.result()

            # Check if more objects are available
            if not response.get('IsTruncated'):
                break

    print(f"All objects in {bucket_name}/{folder_prefix} have been deleted. Total files deleted: {deleted_files_count}")

# Run the delete function
delete_s3_folder_parallel()
