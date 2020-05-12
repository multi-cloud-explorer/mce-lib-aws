# Cloud Explorer - AWS

Librairie pour réaliser un inventaire des ressources d'une souscription AWS.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.org/multi-cloud-explorer/mce-lib-aws.svg)](https://travis-ci.org/multi-cloud-explorer/mce-lib-aws)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=multi-cloud-explorer_mce-lib-aws&metric=alert_status)](https://sonarcloud.io/dashboard?id=multi-cloud-explorer_mce-lib-aws)
[![Coverage Status](https://coveralls.io/repos/github/multi-cloud-explorer/mce-lib-aws/badge.svg?branch=master)](https://coveralls.io/github/multi-cloud-explorer/mce-lib-aws?branch=master)
[![codecov](https://codecov.io/gh/multi-cloud-explorer/mce-lib-aws/branch/master/graph/badge.svg)](https://codecov.io/gh/multi-cloud-explorer/mce-lib-aws)
[![Code Health](https://landscape.io/github/multi-cloud-explorer/mce-lib-aws/master/landscape.svg?style=flat)](https://landscape.io/github/multi-cloud-explorer/mce-lib-aws/master)
[![Requirements Status](https://requires.io/github/multi-cloud-explorer/mce-lib-aws/requirements.svg?branch=master)](https://requires.io/github/multi-cloud-explorer/mce-lib-aws/requirements/?branch=master)

[Documentation](https://multi-cloud-explorer.readthedocs.org)

## Ressources AWS implémentées

- [x] aws.acm.certificate
- [x] aws.apigateway.restapis
- [x] aws.autoscaling.autoScalingGroup
- [x] aws.cloudfront.distribution
- [x] aws.cloudsearch.domain
- [x] aws.dynamodb.table
- [x] aws.ec2.instance
- [x] aws.ecs.cluster
- [x] aws.efs.filesystem
- [x] aws.elasticache.cluster
- [x] aws.elasticbeanstalk.application
- [x] aws.elb.loadbalancer
- [x] aws.elbv2.loadbalancer
- [x] aws.es.domain
- [x] aws.lambda.function
- [x] aws.opsworks.stack
- [x] aws.rds.db
- [x] aws.redshift.cluster
- [x] aws.s3.bucket
- [x] aws.sqs.queue
- [x] aws.sns.topic

## Remarques

Sans filtre de région ou de type, cette librairie va parcourir TOUTES les régions AWS pour tous les types de services gérés par mce-lib-aws.

Tant que le parallélisme n'est pas implémenté, cette opération peut prendre de 5 à 30 mn pour réaliser un inventaire complet.

Il est donc conseillé pour le moment de selectionner les régions à filtrer pour éviter des connections inutiles et diminuer le temps d'exécution.

## Installation

```bash
pip install git+https://github.com/multi-cloud-explorer/mce-lib-aws.git
```

## Utilisation en ligne de commande

```shell 
mce-aws run --help

Usage: mce-aws run [OPTIONS]

Options:
  -S, --services [aws.acm.certificate|aws.apigateway.restapis|aws.autoscaling.autoScalingGroup|aws.cloudfront.distribution|aws.cloudsearch.domain|aws.dynamodb.table|aws.ec2.instance|aws.ecs.cluster|aws.efs.filesystem|aws.elasticache.cluster|aws.elasticbeanstalk.application|aws.elb.loadbalancer|aws.elbv2.loadbalancer|aws.es.domain|aws.lambda.function|aws.opsworks.stack|aws.rds.db|aws.redshift.cluster|aws.s3.bucket|aws.sqs.queue|aws.sns.topic]
                                  Multiple services filter
  -R, --regions TEXT              Multiple regions filter
  -a, --account-id TEXT           Subscription ID  [required]
  -k, --access-key-id TEXT        AWS Access Key ID  [required]
  -s, --secret-access-key TEXT    AWS Secret Key  [required]
  -r, --default-region TEXT       AWS Default Region  [default: eu-central-1; required]
  --output PATH                   File for output json data
  -v, --verbose                   Enables verbose mode.
  -D, --debug
  -l, --log-level [DEBUG|WARN|ERROR|INFO|CRITICAL]
                                  Logging level  [default: INFO]
  --log-file PATH                 File for output logs
  --help                          Show this message and exit.
```

```shell 
mce-aws run -S aws.s3.bucket -R us-east-1 -a 123456789001 -k testing -s testing --output /tmp/export.json
# Ou:
export AWS_ACCESS_KEY_ID=testing
export AWS_SECRET_ACCESS_KEY=testing
export AWS_DEFAULT_REGION=us-east-1
mce-aws run -S aws.s3.bucket -a 123456789001 --output /tmp/export.json

cat /tmp/export.json
```

```json
[
  {
    "arn": "arn:aws:s3:::mybucket0",
    "data": {
      "Name": "mybucket0",
      "CreationDate": "2020-05-12T14:00:53.127747"
    },
    "tags": {
      "key1": "value1"
    },
    "name": "mybucket0",
    "account_id": "123456789001",
    "region": "us-east-1",
    "service": "aws.s3.bucket"
  }
]
```

## Intégration dans votre code

```python
import boto3
from mce_lib_aws.crawler import get_all_assets
account_id = '123456789'
regions_allowed = ['eu-west-3', 'aws-global']
resources_allowed = ['aws.s3.bucket', 'aws.ec2.instance']
session = boto3.Session(aws_access_key_id="testing", aws_secret_access_key="testing", region_name="us-east-1")
for asset in get_all_assets(session, account_id, resources_allowed=resources_allowed, regions_allowed=regions_allowed):
    print(asset)
```

## TODO

- [ ] Ajouter du parallélisme avec Gevent ou concurrent.futures
- [ ] Documenter la création d'un compte et des droits AWS nécessaires à l'inventaire
- [ ] Terminer les exemples dans contrib/
- [ ] Ajouter des services AWS 
- [ ] Ajouter des tests sur les opérations sur les Tags

