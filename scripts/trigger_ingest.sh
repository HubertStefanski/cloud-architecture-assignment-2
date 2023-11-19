#!/usr/bin/bash
set -euxo pipefail

#requires $AWS_PROFILE to be set as active profile

export GEO_INGEST="s3://cloud-architecture-geo-data-ingest"
export GEO_STORAGE="s3://cloud-architecture-geo-data-storage"


# Trigger the lambda by uploading a new jp

aws s3 cp data/GeoTaggedJPG/england-london-bridge.jpg ${GEO_INGEST} --profile ${AWS_PROFILE}

# Wait for Lambda to complete
echo "Sleeping "
sleep 10

# Clean up
echo "Cleaning up"
aws s3 rm ${GEO_STORAGE} --recursive --profile ${AWS_PROFILE}
aws s3 rm ${GEO_INGEST} --recursive --profile ${AWS_PROFILE}
