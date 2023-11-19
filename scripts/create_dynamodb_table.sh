#!/usr/bin/bash
set -euxo pipefail

aws dynamodb create-table \
    --table-name AppGeoData \
    --attribute-definitions \
        AttributeName=geolocation_lat,AttributeType=S \
        AttributeName=geolocation_lng,AttributeType=S \
    --key-schema \
        AttributeName=geolocation_lat,KeyType=HASH \
        AttributeName=geolocation_lng,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --region ${AWS_REGION}
