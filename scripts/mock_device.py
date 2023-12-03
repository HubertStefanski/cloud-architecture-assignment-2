#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone

import boto3

if __name__ == "__main__":
    # Replace these values with your own
    tracker_name = "AppGeoDemoTracker"
    device_id = 'my_mock_device'

    # Tower Bridge Coordinates
    latitude = 51.5055
    longitude = -0.075406

    # Create a Location client
    location_client = boto3.client('location', region_name="eu-west-1")

    # Update the tracker with the device's location
    response = location_client.batch_update_device_position(
        TrackerName=tracker_name,
        Updates=[
            {
                'SampleTime': datetime.now(timezone.utc) - timedelta(minutes=1),
                'DeviceId': device_id,
                'Position': [-1.075406, latitude],
            },
        ],
    )

    print(response)

    response = location_client.batch_update_device_position(
        TrackerName=tracker_name,
        Updates=[
            {
                'SampleTime': datetime.now(timezone.utc) - timedelta(minutes=1),
                'DeviceId': device_id,
                'Position': [longitude, latitude],
            },
        ],
    )

    print(response)
