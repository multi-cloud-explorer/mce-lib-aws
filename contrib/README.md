# Quelques exemples pour utiliser mce-lib-aws

En cours de mise au point...

## Localstack

```shell
docker run -d --name localstack-us-east-1 \
    --hostname localstack-us-east-1 \
    -e DEBUG=1 \
    -e USE_SSL=true \
    -e START_WEB=0 \
    -e DEFAULT_REGION="us-east-1" \
    -e AWS_XRAY_SDK_ENABLED=true \
    -e LAMBDA_EXECUTOR=docker \
    -e LAMBDA_REMOTE_DOCKER=false \
    -e DOCKER_HOST=tcp://localhost:2375 \
    -e EDGE_PORT=4566 \
    -p 4566:4566 localstack/localstack

docker run --rm -it -e SERVICES=sqs,sts,ec2,iam,secretsmanager,acm -p 45660:4566 localstack/localstack

```



  