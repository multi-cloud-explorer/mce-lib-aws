#!/usr/bin/env python3

import urllib3
urllib3.disable_warnings()

import boto3
from mce_lib_aws.pytest import fixtures

endpoint_url = 'https://localhost:4566'
region = 'us-east-1'
subscription_id = "123456789"

session = boto3.session.Session(
    aws_access_key_id='testing',
    aws_secret_access_key='testing',
    aws_session_token='testing',
    region_name=region
)
#sqs_client = session_us.client('sqs', endpoint_url=endpoint_url_us, region_name='us-east-1')

# ok avec: endpoint_url = 'https://localhost:4566' & moto_server -H localhost -p 45660 -s acm
# FIXME: acm_certificate = fixtures.acm_certificate(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False)
# botocore.exceptions.ClientError: An error occurred (404) when calling the RequestCertificate operation

networking = fixtures.setup_networking(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False)
# aws ec2 describe-vpcs

apigateway_restapi = fixtures.apigateway_restapi(session=session, region=region, endpoint_url=endpoint_url, verify=False)

# FIXME: auto_scaling_group = fixtures.auto_scaling_group(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False, networking=networking)
# botocore.exceptions.ClientError: An error occurred (502) when calling the CreateLaunchConfiguration operation (reached max retries: 4): Bad Gateway

cloud_formation_stack = fixtures.cloud_formation_stack(session=session, region=region, endpoint_url=endpoint_url, verify=False)

dynamodb_table = fixtures.dynamodb_table(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False)

ec2_instance = fixtures.ec2_instance(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False)

# FIXME: ecs_cluster = fixtures.ecs_cluster(session=session, region=region, endpoint_url=endpoint_url, verify=False)
# botocore.exceptions.ClientError: An error occurred (502) when calling the CreateCluster operation (reached max retries: 4): Bad Gateway

# FIXME: elb_load_balancer = fixtures.elb_load_balancer(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False)
# botocore.parsers.ResponseParserError: Unable to parse response (not well-formed (invalid token): line 1, column 0), invalid XML received. Further retries may succeed: b'{"status": "running"}'

# FIXME: elbv2_load_balancer = fixtures.elbv2_load_balancer(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False)
# botocore.parsers.ResponseParserError: Unable to parse response (not well-formed (invalid token): line 1, column 0), invalid XML received. Further retries may succeed: b'{"status": "running"}'

# FIXME: opsworks_stack = fixtures.opsworks_stack(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False)
# botocore.exceptions.ClientError: An error occurred (404) when calling the CreateStack operation:

# FIXME: rds_db_instance = fixtures.rds_db_instance(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False)
# botocore.exceptions.ClientError: An error occurred (502) when calling the CreateDBInstance operation (reached max retries: 4): Bad Gateway

redshift_cluster = fixtures.redshift_cluster(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False)

s3_bucket_with_tags = fixtures.s3_bucket_with_tags(session=session, region=region, endpoint_url=endpoint_url, verify=False)
# aws s3 ls

sns_topic = fixtures.sns_topic(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False)

sqs_queue = fixtures.sqs_queue(session=session, region=region, account_id=subscription_id, endpoint_url=endpoint_url, verify=False)

