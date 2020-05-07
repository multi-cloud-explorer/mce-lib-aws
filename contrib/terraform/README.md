## AWS Tests with Terraform and LocalStack

En cours de mise au point...

**Requis:**
- [Terraform](https://www.terraform.io/)
- [Docker](https://www.docker.com/)
- [Python 3](https://python.org/)

**Installation de terraform:**

```shell
curl -L -O https://releases.hashicorp.com/terraform/0.12.24/terraform_0.12.24_linux_amd64.zip
unzip terraform_0.12.24_linux_amd64.zip -d .
rm -f terraform_0.12.24_linux_amd64.zip
sudo mv terraform /usr/local/bin
terraform --version
```

**Exécution de localstack:**

> Remplacez `-v /var/run/docker.sock` par `-e DOCKER_HOST=tcp://localhost:2375` si vous utilisez un serveur Docker situé sur une autre machine.


```shell
docker run -d --name localstack-us-east-1 \
    --hostname localstack-us-east-1 \
    -e HOSTNAME=localstack-us-east-1 \
    -e HOSTNAME_EXTERNAL=localstack-us-east-1 \ # Pour l'url vers une queue comme SQS
    -e DEBUG=1 \
    -e USE_SSL=true \
    -e START_WEB=0 \
    -e DEFAULT_REGION="us-east-1" \
    -e AWS_XRAY_SDK_ENABLED=true \
    -e LAMBDA_EXECUTOR=docker \
    -e LAMBDA_REMOTE_DOCKER=false \
    -e EDGE_PORT=4566 \
    -e DATA_DIR="/tmp/localstack/data" \       # Pour rendre persistent
    -v "/tmp/localstack-us-east-1:/tmp/localstack/data" \      
    -v "/var/run/docker.sock:/var/run/docker.sock" localstack/localstack
    -p 4566:4566 localstack/localstack
```

**Définition d'alias:**

```shell
alias awslocal='docker exec -it -e PYTHONWARNINGS="ignore:Unverified HTTPS request" localstack-us-east-1 awslocal'

awslocal s3 ls
```

**Déploiement de l'infrastructure avec Terraform:**

```shell
terraform init
terraform plan
terraform apply
```

**Destruction de l'infrastructure:**

```shell
terraform destroy
```
