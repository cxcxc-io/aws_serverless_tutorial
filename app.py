import json

# import requests

import boto3
import os
import time


import os
def lambda_handler(event, context):
    print(os.environ.get("DYNAMODB_LOCAL_PATH"))
    dynamodb_client = boto3.resource('dynamodb', endpoint_url=os.environ.get("DYNAMODB_LOCAL_PATH"))
    table = dynamodb_client.Table('Movies')
    
    try:
        table_info_does_exist = table.archival_summary()
        print(table_info_does_exist)
    except:
        dynamodb_client.create_table(
            TableName="Movies",
            KeySchema=[
                {
                    'AttributeName': 'year',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'title',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'year',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                },
    
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    
    ####
    response = table.put_item(
       Item={
            'year': 2021,
            'title': "新年快樂",
            'info': {
                'plot': "其他欄位隨意塞",
                'rating': 20
            }
        }
    )

    print(f'上傳結果 {response}')
    
    ####
    get_response = table.get_item(Key={'year': 2021, 'title': "新年快樂"})
    
    print(f'讀取結果 {get_response.get("Item")}')
 
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": os.environ.get("DYNAMODB_LOCAL_PATH")
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
