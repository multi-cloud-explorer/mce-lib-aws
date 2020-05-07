import boto3
import pytest

from moto import mock_iam, mock_sts, mock_apigateway, mock_s3

from . import fixtures

@pytest.fixture(scope='function', autouse=True)
def aws_credentials(monkeypatch):
    """Mocked AWS Credentials for moto."""
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'testing')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'testing')
    monkeypatch.setenv('AWS_SECURITY_TOKEN', 'testing')
    monkeypatch.setenv('AWS_SESSION_TOKEN', 'testing')

@pytest.fixture(scope='function')
def aws_account_id():
    return fixtures.DEFAULT_ACCOUNT_ID

@pytest.fixture(scope='function')
def aws_delegation_role_name():
    return "TestingRole"

@pytest.fixture(scope='function')
def aws_region():
    return "us-east-1"

@pytest.fixture(scope='function')
@mock_iam
@mock_sts
def aws_session(aws_region):
    return boto3.session.Session(region_name=aws_region)

# TODO: assume role: https://github.com/spulec/moto/blob/d0c60ecaac93f9712220030924d85a2cd6ac4f8f/tests/test_sts/test_sts.py#L56

@pytest.fixture
def acm_certificate():
    return fixtures.acm_certificate

@pytest.fixture
def apigateway_restapi():
    return fixtures.apigateway_restapi

@pytest.fixture
def auto_scaling_group():
    return fixtures.auto_scaling_group

@pytest.fixture
def cloud_formation_stack():
    return fixtures.cloud_formation_stack

@pytest.fixture
def dynamodb_table():
    return fixtures.dynamodb_table

@pytest.fixture
def ec2_instance():
    return fixtures.ec2_instance

@pytest.fixture
def ecs_cluster():
    return fixtures.ecs_cluster

@pytest.fixture
def elb_load_balancer():
    return fixtures.elb_load_balancer

@pytest.fixture
def elbv2_load_balancer():
    return fixtures.elbv2_load_balancer

@pytest.fixture
def opsworks_stack():
    return fixtures.opsworks_stack

@pytest.fixture
def rds_db_instance():
    return fixtures.rds_db_instance

@pytest.fixture
def redshift_cluster():
    return fixtures.redshift_cluster

@pytest.fixture
def s3_bucket_with_tags():
    return fixtures.s3_bucket_with_tags

@pytest.fixture
def sns_topic():
    return fixtures.sns_topic

@pytest.fixture
def sqs_queue():
    return fixtures.sqs_queue