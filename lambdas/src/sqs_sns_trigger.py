import boto3
import json
import os


def lambda_handler(event, context):
    if 'Records' in event and len(event['Records']) > 0:
        for record in event['Records']:
            body_data = json.loads(record['body'])
            device_id = body_data['detail']['DeviceId']
            geofence_id = body_data['detail']['GeofenceId']

            sns_message = f"looks like your device: {device_id} is near {geofence_id}, why not take a look?"

            sns_arn = os.getenv("AWS_SNS_TOPIC_ARN")
            sns_client = boto3.client('sns')
            sns_client.publish(
                TopicArn=sns_arn,
                Message=sns_message,
                Subject='Geofence Entry Event'
            )
