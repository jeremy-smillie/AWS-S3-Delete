# AWS-S3-Delete
This README covers the setup, usage, and detailed explanations of the script's functionality.

# S3 Bucket Delete Script

This Python script efficiently deletes objects and object versions in an S3 bucket. It uses parallel processing to maximize deletion speed, making it ideal for large-scale deletions.

## Features

- **Parallel Processing**: Uses multiple threads to delete files concurrently, speeding up the deletion process.
- **Batch Deletion**: Deletes up to 1000 objects at a time, in accordance with AWS S3 limits.
- **Handles Object Versions**: Supports deletion of versioned objects and delete markers, which is essential for versioned buckets.
- **Configurable**: Allows setting a specific folder (prefix) within the bucket to delete, or clears the entire bucket if no prefix is specified.

## Prerequisites

- **Python 3.8 or later**
- **AWS CLI** configured with access permissions for S3.
- **boto3 and botocore** libraries (these will be installed in the setup steps).

## Setup Instructions for macOS

### 1. Install Python

If you don't already have Python 3.8+ installed, use [Homebrew](https://brew.sh/):

```bash
brew install python
```

### 2. Set Up a Virtual Environment

It's recommended to create a virtual environment to manage dependencies:

```
# Navigate to your project directory
cd path/to/your/project

# Create a virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate
```

### 3. Install Required Packages

Inside the virtual environment, install the necessary packages:

```
pip install boto3 botocore
```

### 4. Configure AWS CLI (if not already configured)

Ensure the AWS CLI has the right permissions to access the S3 bucket. Run:

```
aws configure
```

Provide your AWS Access Key ID, Secret Access Key, region, and output format when prompted.

### 5. Set Up the Script

Open the script and update the following variables:

bucket_name: Set this to your S3 bucket name.
folder_prefix: Set this to the folder prefix within the bucket you want to delete. Leave it blank to delete everything in the bucket.

Example:
```
bucket_name = 'my-s3-bucket-name'
folder_prefix = 'my-folder/'  # Optional: specify a folder prefix to delete only a specific directory
```

# How to Run the Script

With the virtual environment activated, run the script with:

```
python delete_s3_folder_parallel.py
```

# The script will:

List all objects (including versions and delete markers) under the specified folder_prefix.
Delete objects in batches of 1000 for efficiency.
Print progress after each batch and total files deleted at the end.

# Script Explanation
## Key Components
Parallel Processing with ThreadPoolExecutor:

Uses up to 30 concurrent threads for parallel deletion, controlled by max_workers=30. Adjust this based on your system and network capability.
Batch Deletion:

Deletes up to 1000 objects per request, as recommended by AWS. If there are more than 1000 objects, the script continues listing and deleting in batches.
Handles Object Versions and Delete Markers:

Essential for versioned buckets. It deletes all versions of each object as well as any delete markers.

# Code Walkthrough

Delete Batch Function (delete_batch):

Takes a batch of up to 1000 keys (objects) and deletes them using s3.delete_objects.
Updates the global count of deleted files and prints progress.
Main Deletion Loop (delete_s3_folder_parallel):

Uses pagination to list all versions and delete markers within the specified bucket and prefix.
Adds each object version and delete marker to a batch until it reaches 1000, then submits the batch for deletion.
Continues this process until all objects are deleted.

### Example Output
```
Deleted 1000 files... Total deleted so far: 1000
Deleted 1000 files... Total deleted so far: 2000
No more files to delete.
All objects in my-s3-bucket-name/my-folder/ have been deleted. Total files deleted: 2000
```

# Customization

Adjust max_workers: Increase or decrease the number of threads by setting max_workers in ThreadPoolExecutor.
Change folder_prefix: Specify a different folder prefix to target a specific directory within the bucket.
Run on an EC2 Instance: For faster performance, consider running the script on an EC2 instance in the same region as the S3 bucket.

# Troubleshooting

## Common Issues

Permissions Error:

Ensure your AWS CLI credentials have s3:ListBucket, s3:GetObjectVersion, and s3:DeleteObjectVersion permissions.
Connection Timeout or Slow Performance:

Increase max_workers if your network can handle more concurrent requests.
Run the script on an EC2 instance closer to the bucket region to reduce latency.

## Logging and Error Handling

The script includes error handling in the delete_batch function, which catches and logs errors. If an error occurs during deletion, it will print an error message but continue with the next batch.

# License

This project is licensed under the MIT License.
