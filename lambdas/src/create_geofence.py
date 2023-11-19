import json

import boto3
from botocore.exceptions import ClientError


def create_circle_geofence(client, collection_name, geofence_name, center, radius_meters):
    # Create a geofence collection

    try:
        response = client.describe_geofence_collection(
            CollectionName=collection_name
        )
    except ClientError as e:
        print(f"{e.response['Error']['Code']}")

    try:
        response = client.create_geofence_collection(
            CollectionName=collection_name,
            PricingPlan='RequestBasedUsage'
        )
    except ClientError as e:
        # Expect a resource conflict, continue regardless, laziness mostly
        print(f"{e.response['Error']['Code']}")

    geofence = {
        'Geometry': {
            'Circle': {
                'Center': center,  # [longitude, latitude]
                'Radius': radius_meters
            }
        },
        'GeofenceId': geofence_name,
    }

    client.batch_put_geofence(
        CollectionName=collection_name,
        Entries=[geofence]
    )


def lambda_handler(event, context):
    print(f"Event {json.dumps(event, indent=2)}")
    location = boto3.client('location')
    arn = ""
    print(event['Records'])
    if 'Records' in event and len(event['Records']) > 0:
        for record in event['Records']:
            if 'eventName' in record and record['eventName'] == 'INSERT':
                item = record['dynamodb']['NewImage']
                create_circle_geofence(location, "appGeoData", item['s3_key']['S'].removesuffix(".jpg"),
                                       [float(item['geolocation_lng']['S']),
                                        float(item['geolocation_lat']['S'])], 300)
    print(f"Geofence Collection ARN: {arn}")
