import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # For Testing in aws console
    if isinstance(event, str):
        event_json = json.loads(event)
    else:
        event_json = event
        
    # Get the s3 address from the Step Function event input
    key = event_json['s3_key']
    bucket = event_json['s3_bucket']
    
    # Download the data from s3 to /tmp/image.png
    try:
        s3.download_file(bucket, key, '/tmp/image.png')
    except Exception as e:
        print("Fail to download file")
        return {
            'statusCode': 500,
            'body': f"Error downloading the file: {e}"
        }
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

# Test Data
#{
#  "inferences": [],
#  "s3_key": "test/bicycle_s_000030.png",
#  "s3_bucket": "modeltrainwang",
#  "image_data": ""
#}