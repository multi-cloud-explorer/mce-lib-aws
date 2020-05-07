import logging
from datetime import date, datetime
from decimal import Decimal

import boto3

from . import _AVAILABLES_RESOURCES
from .common import Asset

logger = logging.getLogger(__name__)

__all__ = ('get_cloud_assets', 'set_asset_tags')


def get_credentials(account_id, delegation_role_name):
    # Get credential of the delagated role over STS
    role_arn = 'arn:aws:iam::{}:role/{}'.format(
        account_id, delegation_role_name)
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


def get_cloud_assets(account_id, delegation_role_name, resources_allowed, regions_allowed):
    """Get all assets in an AWS Account"""

    aws_creds = get_credentials(account_id, delegation_role_name)

    # Open a session to get Account Alias, then later available regions
    session = boto3.session.Session(**aws_creds)
    client = session.client('iam')
    account_alias = client.list_account_aliases()['AccountAliases'][0]

    logger.info('Gather resources on AWS Account', extra=dict(data=dict(
        account_alias=account_alias,
        account_id=account_id
    )))

    for resource_name, generator in _AVAILABLES_RESOURCES.items():
        # Skip not allowed resources
        if resources_allowed and resource_name not in resources_allowed:
            continue

        # Botocore knows for each resources which regions are available
        # KB: https://github.com/boto/botocore/blob/master/botocore/data/endpoints.json
        regions_available = session.get_available_regions(
            service_name=generator.boto_service_name,
            allow_non_regional=True
        )

        for region in regions_available:
            # Skip not allowed regions
            if regions_allowed and region not in regions_allowed:
                continue
            # Skip special regions
            if region == 'local' or region[:4] == 'fips':
                continue

            for asset in generator(region=region, account=account_id, session=session):

                # Remove unsupported types in DynamoDB
                asset_tags = clean(asset.tags)
                asset_data = clean(asset.data)
                asset_data['Tags'] = None

                # A namedtuple is readonly, reset its values with a new one
                asset = Asset(arn=asset.arn,
                              data=asset_data,
                              tags=asset_tags,
                              name=asset.name)

                # Dot not inventory instances in AutoScaling
                if resource_name == 'aws.ec2.instance' and asset.tags.get('aws:autoscaling:groupName'):
                    continue

                yield resource_name, region, asset


def set_asset_tags(account_id, delegation_role_name, region, resource_name, asset_id, tags):
    aws_creds = get_credentials(account_id, delegation_role_name)
    session = boto3.session.Session(**aws_creds)

    resource_cls = _AVAILABLES_RESOURCES[resource_name]
    asset = resource_cls(region=region,
                         account=account_id,
                         session=session)
    asset.set_tags(arn=asset_id, tags_dict=tags)


def unset_asset_tags(account_id, delegation_role_name, region, resource_name, asset_id, tag_keys):
    aws_creds = get_credentials(account_id, delegation_role_name)
    session = boto3.session.Session(**aws_creds)

    resource_cls = _AVAILABLES_RESOURCES[resource_name]
    asset = resource_cls(region=region,
                         account=account_id,
                         session=session)
    asset.unset_tags(arn=asset_id, keys=tag_keys)
