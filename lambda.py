#serializeImageData
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event["s3_key"]
    bucket = event["s3_bucket"]
    
    # Download the data from s3 to /tmp/image.png
    boto3.resource('s3').Bucket(bucket).download_file(key, "/tmp/image.png")
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function

    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": [0,1]
        }
    }

#imageClassifier - Lambda Function 2

import os
import io
import boto3
import json
import base64

# setting the  environment variables
ENDPOINT_NAME = 'image-classification-2021-12-07-13-31-39-062'
# I used  AWS's lightweight runtime solution to invoke an endpoint, as the one mentioned in the Jupyter notebook just did not work out for me.
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    
    # Decode the image data
    image = base64.b64decode(event["image_data"])
    
    # Make a prediction:
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='image/png',
                                       Body=image)
    
    # We return the data back to the Step Function    
    event["inferences"] = json.loads(response['Body'].read().decode('utf-8'))
    return {
        'statusCode': 200,
        'body': event
    }

#InferenceConfidenceFilter - Lambda Function 3

import json


THRESHOLD = .93

def lambda_handler(event, context):
    # Get the inferences from the event
    inferences = event["inferences"]
    
    # Check if any values in any inferences are above THRESHOLD
    meets_threshold = (max(inferences) > THRESHOLD)
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': event
    }