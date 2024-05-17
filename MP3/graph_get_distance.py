import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = dynamodb.Table('locations')


def lambda_handler(event, context):
    print(f"event {event}")

    slots = event['sessionState']['intent']['slots']

    source = slots['Source']['value']['originalValue']
    destination = slots['Destination']['value']['originalValue']

    print(f"Reading from DynamoDB {source}:{destination}")
    response = table_name.get_item(
        Key={
            'sd_pair': f"{source}-{destination}"
        }
    )
    print(f"response from dyanmoDB {response}")
    distance = response['Item']['distance']

    response = {
        "sessionState": {
            "dialogAction": {
                "type": "ConfirmIntent"
            },
            "intent": {
                "name": "getDistance",
                "slots": {
                    "Source": {
                        "value": {
                            "originalValue": source,
                            "resolvedValues": [
                                source
                            ],
                            "interpretedValue": source
                        }
                    },
                    "Destination": {
                        "value": {
                            "originalValue": destination,
                            "resolvedValues": [
                                destination
                            ],
                            "interpretedValue": destination
                        }
                    }
                }
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": distance
            }
        ]
    }

    print(f"response before returning ---> {response}")
    return response