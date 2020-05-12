from typing import List, Dict
import logging

import boto3
from boto3.session import Session as BotoSession

from . import SERVICES
from .common import Asset
from .utils import clean

logger = logging.getLogger(__name__)

__all__ = [
    'get_credentials',
    'get_selected_regions_and_services',
    'get_asset_by_region',
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


# def get_cloud_assets(
#         session: BotoSession,
#         account_id: str,
#         resources_allowed: List = None, resources_exclude: List = None,
#         regions_allowed: List = None, regions_exclude: List = None,
#         endpoint_url: str = None) -> (str, str, Dict):
#     """Get all assets in an AWS Account
#
#     # example:
#     >>> import boto3
#     >>> from mce_lib_aws.crawler import get_cloud_assets
#     >>> account_id = '123456789'
#     >>> regions_allowed = ['eu-west-3', 'aws-global']
#     >>> resources_allowed = ['aws.s3.bucket', 'aws.ec2.instance']
#     >>> session = boto3.Session(aws_access_key_id="xxx", aws_secret_access_key="xxx", region_name="eu-west-3")
#     >>> for resource_type, region, asset in get_cloud_assets(session, account_id, resources_allowed=resources_allowed, regions_allowed=regions_allowed):
#     >>>     print(resource_type, region, dict(asset._asdict()))
#
#     # With role delegation:
#     # Connect with AWS-CLI or set env variables before this:
#     >>> import boto3
#     >>> from mce_lib_aws.crawler import get_cloud_assets
#     >>> account_id = '123456789'
#     >>> regions_allowed = ['eu-west-3', 'aws-global']
#     >>> resources_allowed = ['aws.s3.bucket', 'aws.ec2.instance']
#     >>> aws_creds = get_credentials(account_id, delegation_role_name)
#     >>> session = boto3.Session(**aws_creds)
#     >>> for resource_type, region, asset in get_cloud_assets(session, account_id, resources_allowed=resources_allowed, regions_allowed=regions_allowed):
#     >>>     print(resource_type, region, dict(asset._asdict()))
#     """
#
#     for resource_type, klass in SERVICES.items():
#
#         if resources_allowed and resource_type not in resources_allowed:
#             continue
#         if resources_exclude and resource_type in resources_exclude:
#             continue
#
#         regions_available = session.get_available_regions(
#             service_name=klass.boto_service_name,
#             allow_non_regional=True
#         )
#
#         for region in regions_available:
#
#             if regions_allowed and region not in regions_allowed:
#                 continue
#             if regions_exclude and region in regions_exclude:
#                 continue
#
#             # Skip sgipecial regions
#             if region == 'local' or region.endswith('fips'):
#                 continue
#
#             for asset in klass(
#                     region=region,
#                     account=account_id,
#                     session=session,
#                     endpoint_url=endpoint_url):
#
#                 asset_tags = clean(asset.tags)
#                 asset_data = clean(asset.data)
#                 asset_data['Tags'] = None
#
#                 asset = Asset(arn=asset.arn,
#                               data=asset_data,
#                               tags=asset_tags,
#                               name=asset.name)
#
#                 if resource_type == 'aws.ec2.instance' and asset.tags.get('aws:autoscaling:groupName'):
#                     continue
#
#                 yield resource_type, region, asset
#
def get_selected_regions_and_services(
        resources_allowed: List = None, resources_exclude: List = None,
        regions_allowed: List = None, regions_exclude: List = None,
        exclude_fips_regions=True) -> Dict:
    """Get selected region and resource type grouped by region"""

    session = boto3.Session()

    groups = {}

    for resource_type, klass in SERVICES.items():

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
                logger.info(f"exclude region [{region}]")
                continue
            if regions_exclude and region in regions_exclude:
                logger.info(f"exclude region [{region}]")
                continue

            # Skip special regions
            if region == 'local':
                logger.info(f"exclude region [{region}]")
                continue

            if exclude_fips_regions and "fips" in region:
                logger.info(f"exclude region [{region}]")
                continue

            if not region in groups:
                groups[region] = []
            if not resource_type in groups[region]:
                groups[region].append(resource_type)

    return groups


def get_asset_by_region(
        session: BotoSession,
        account_id: str,
        region: str,
        service: str,
        endpoint_url: str = None):
    """

    >>> import boto3
    >>> from mce_lib_aws.crawler import get_selected_regions_and_services, get_asset_by_region
    >>> account_id = '123456789'
    >>> regions_allowed = ['eu-west-3', 'aws-global']
    >>> resources_allowed = ['aws.s3.bucket', 'aws.ec2.instance']
    >>> session = boto3.Session(aws_access_key_id="xxx", aws_secret_access_key="xxx", region_name="eu-west-3")
    >>> region_groups = get_selected_regions_and_services(resources_allowed=resources_allowed, regions_allowed=regions_allowed)
    >>> for region, services in region_groups.items():
    >>>     for service in services:
    >>>         assets = list(get_asset_by_region(session, account_id, region, service))
    """

    klass = SERVICES[service]

    for asset in klass(region=region, account=account_id, session=session, endpoint_url=endpoint_url):
        asset_tags = clean(asset.tags)
        asset_data = clean(asset.data)

        if 'Tags' in asset_data:
            del asset_data['Tags']

        _asset = Asset(
            arn=asset.arn,
            data=asset_data,
            tags=asset_tags,
            name=asset.name,
            account_id=account_id,
            region=region,
            service=service)

        if service == 'aws.ec2.instance' and _asset.tags.get('aws:autoscaling:groupName'):
            continue

        yield _asset

def get_all_assets(
        session: BotoSession,
        account_id: str,
        resources_allowed: List = None, resources_exclude: List = None,
        regions_allowed: List = None, regions_exclude: List = None,
        exclude_fips_regions=True,
        endpoint_url: str = None):
    """Get all assets in an AWS Account

    # example:
    >>> import boto3
    >>> from mce_lib_aws.crawler import get_all_assets
    >>> account_id = '123456789'
    >>> regions_allowed = ['eu-west-3', 'aws-global']
    >>> resources_allowed = ['aws.s3.bucket', 'aws.ec2.instance']
    >>> session = boto3.Session(aws_access_key_id="xxx", aws_secret_access_key="xxx", region_name="eu-west-3")
    >>> for asset in get_all_assets(session, account_id, resources_allowed=resources_allowed, regions_allowed=regions_allowed):
    >>>     print(asset)

    # With role delegation:
    # Connect with AWS-CLI or set env variables before this:
    >>> import boto3
    >>> from mce_lib_aws.crawler import get_all_assets
    >>> account_id = '123456789'
    >>> regions_allowed = ['eu-west-3', 'aws-global']
    >>> resources_allowed = ['aws.s3.bucket', 'aws.ec2.instance']
    >>> aws_creds = get_credentials(account_id, delegation_role_name)
    >>> session = boto3.Session(**aws_creds)
    >>> for asset in get_all_assets(session, account_id, resources_allowed=resources_allowed, regions_allowed=regions_allowed):
    >>>     print(asset)
    """

    services_by_regions = get_selected_regions_and_services(
        resources_allowed=resources_allowed,
        resources_exclude=resources_exclude,
        regions_allowed=regions_allowed,
        regions_exclude=regions_exclude,
        exclude_fips_regions=exclude_fips_regions
    )

    for region, services in services_by_regions.items():
        for service in services:
            try:
                for asset in get_asset_by_region(
                        session=session,
                        account_id=account_id,
                        region=region,
                        service=service,
                        endpoint_url=endpoint_url):
                    yield dict(asset._asdict())
            except Exception as err:
                msg = f"region[{region}] - service[{service}] - error: {str(err)}"
                logger.error(msg)

