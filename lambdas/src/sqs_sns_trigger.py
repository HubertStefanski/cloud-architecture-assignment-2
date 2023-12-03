import json
import os

import boto3


def lambda_handler(event, context):
    if 'Records' in event and len(event['Records']) > 0:
        print(event['Records'])

        sqs_message = json.loads(event[0]['body'])['detail']['GeofenceId']

        device_id = sqs_message['DeviceId']
        landmark = sqs_message['GeofenceId']

        sns_message = f"looks like your device: {device_id} is near {landmark}, why not take a look?"

        sns_arn = os.getenv("AWS_SNS_TOPIC_ARN")
        sns_client = boto3.client('sns')
        sns_client.publish(
            TopicArn=sns_arn,
            Message=sns_message,
            Subject='Geofence Entry Event'
        )
