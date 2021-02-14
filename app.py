import json

# import requests

import os
def lambda_handler(event, context):
 
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": os.environ.get("DYNAMODB_LOCAL_PATH"),
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
