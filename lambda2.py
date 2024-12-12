import json
import base64
import boto3

# Define the SageMaker runtime client using boto3
sagemaker_runtime = boto3.client('sagemaker-runtime')

ENDPOINT = "image-classification-2024-12-12-13-34-25-137"

def lambda_handler(event, context):

    # For Testing in AWS Console (parse event depending on structure)
    if isinstance(event, str):
        event_json = json.loads(event['body'])
    else:
        event_json = event['body']
    
    image_data = base64.b64decode(event_json['image_data'])
    
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        ContentType='application/x-image',
        Body=image_data
    )
    
    inferences = response['Body'].read().decode('utf-8')
    
    event["inferences"] = inferences
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

# Test Data
#{
#  "statusCode": 200,
#  "body": {
#    "image_data": #"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",
#    "s3_bucket": "modeltrainwang",
#    "s3_key": "test/bicycle_s_000030.png",
#    "inferences": []
#  }
#}
