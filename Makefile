.phony: build/push

login:
	aws ecr get-login-password --region eu-west-1 --profile ${AWS_PROFILE} | podman login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com

build:
	podman build -t lambda lambdas

tag:
	podman tag lambdas:latest ${ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/lambdas:latest

push:
	podman push ${ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/lambdas:latest

build/push: login build tag push

trigger/ingest:
	./scripts/trigger_ingest.sh

table:
	./scripts/create_dynamodb_table.sh