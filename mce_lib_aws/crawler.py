from typing import List, Dict
import logging
from datetime import date, datetime
from decimal import Decimal

import boto3
from boto3.session import Session as BotoSession

from . import _AVAILABLES_RESOURCES
from .common import Asset

logger = logging.getLogger(__name__)

__all__ = [
    'get_cloud_assets'
]


def get_credentials(account_id, delegation_role_name, session=None):
    # Get credential of the delegated role over STS

    role_arn = f'arn:aws:iam::{account_id}:role/{delegation_role_name}'

    if session:
        sts_client = session.client('sts')
    else:
        sts_client = boto3.client('sts')

    assumed_role_object = sts_client.assume_role(
        DurationSeconds=900,
        RoleArn=role_arn,
        RoleSessionName='AssumeRoleSession1'
    )

    credentials = assumed_role_object['Credentials']

    return dict(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )


def clean(value):
    """DynamoDB does not support empty string, Float.
    And Datetime is not JSON serializable.
    This recursive function cleans the data."""
    if isinstance(value, dict):
        return dict((k, clean(v)) for k, v in value.items())
    elif isinstance(value, list):
        return list(clean(v) for v in value)
    elif isinstance(value, tuple):
        return tuple(list(clean(v) for v in value))
    elif isinstance(value, str) and value == '':
        return None
    elif isinstance(value, (datetime, date)):
        return value.isoformat()
    elif isinstance(value, float):
        return Decimal(str(value))
    return value

def get_cloud_assets(
        session: BotoSession,
        account_id: str,
        resources_allowed: List = None, resources_exclude: List = None,
        regions_allowed: List = None, regions_exclude: List = None,
        endpoint_url: str = None) -> (str, str, Dict):
    """Get all assets in an AWS Account

    # example:
    >>> import boto3
    >>> from mce_lib_aws.crawler import get_cloud_assets
    >>> account_id = '123456789'
    >>> regions_allowed = ['eu-west-3', 'aws-global']
    >>> resources_allowed = ['aws.s3.bucket', 'aws.ec2.instance']
    >>> session = boto3.Session(aws_access_key_id="xxx", aws_secret_access_key="xxx", region_name="eu-west-3")
    >>> for resource_type, region, asset in get_cloud_assets(session, account_id, resources_allowed=resources_allowed, regions_allowed=regions_allowed):
    >>>     print(resource_type, region, dict(asset._asdict()))

    # With role delegation:
    # Connect with AWS-CLI or set env variables before this:
    >>> import boto3
    >>> from mce_lib_aws.crawler import get_cloud_assets
    >>> account_id = '123456789'
    >>> regions_allowed = ['eu-west-3', 'aws-global']
    >>> resources_allowed = ['aws.s3.bucket', 'aws.ec2.instance']
    >>> aws_creds = get_credentials(account_id, delegation_role_name)
    >>> session = boto3.Session(**aws_creds)
    >>> for resource_type, region, asset in get_cloud_assets(session, account_id, resources_allowed=resources_allowed, regions_allowed=regions_allowed):
    >>>     print(resource_type, region, dict(asset._asdict()))
    """

    for resource_type, klass in _AVAILABLES_RESOURCES.items():

        if resources_allowed and resource_type not in resources_allowed:
            continue
        if resources_exclude and resource_type in resources_exclude:
            continue

        regions_available = session.get_available_regions(
            service_name=klass.boto_service_name,
            allow_non_regional=True
        )

        for region in regions_available:

            if regions_allowed and region not in regions_allowed:
                continue
            if regions_exclude and region in regions_exclude:
                continue

            # Skip special regions
            if region == 'local' or region[:4] == 'fips':
                continue

            for asset in klass(
                    region=region,
                    account=account_id,
                    session=session,
                    endpoint_url=endpoint_url):

                asset_tags = clean(asset.tags)
                asset_data = clean(asset.data)
                asset_data['Tags'] = None

                asset = Asset(arn=asset.arn,
                              data=asset_data,
                              tags=asset_tags,
                              name=asset.name)

                yield resource_type, region, asset


