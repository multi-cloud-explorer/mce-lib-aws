from pprint import pprint as pp
from moto import mock_iam, mock_sts, mock_apigateway

import boto3
from mce_lib_aws.crawler import get_credentials, get_asset_by_region, get_selected_regions_and_services


@mock_iam
def test_get_selected_regions_and_services():

    groups = get_selected_regions_and_services(
        regions_allowed=['eu-west-1'], resources_allowed=['aws.s3.bucket']
    )
    assert groups == {'eu-west-1': ['aws.s3.bucket']}


    groups = get_selected_regions_and_services(exclude_fips_regions=False)
    # pp(list(groups.keys()))
    assert list(groups.keys()) == [
        'af-south-1',
        'ap-east-1',
        'ap-northeast-1',
        'ap-northeast-2',
        'ap-south-1',
        'ap-southeast-1',
        'ap-southeast-2',
        'ca-central-1',
        'ca-central-1-fips',
        'eu-central-1',
        'eu-north-1',
        'eu-south-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'me-south-1',
        'sa-east-1',
        'us-east-1',
        'us-east-1-fips',
        'us-east-2',
        'us-east-2-fips',
        'us-west-1',
        'us-west-1-fips',
        'us-west-2',
        'us-west-2-fips',
        'aws-global',
        'fips-ca-central-1',
        'fips-us-east-1',
        'fips-us-east-2',
        'fips-us-west-1',
        'fips-us-west-2',
        'fips-ap-east-1',
        'fips-ap-northeast-1',
        'fips-ap-northeast-2',
        'fips-ap-south-1',
        'fips-ap-southeast-1',
        'fips-ap-southeast-2',
        'fips-eu-central-1',
        'fips-eu-north-1',
        'fips-eu-west-1',
        'fips-eu-west-2',
        'fips-eu-west-3',
        'fips-me-south-1',
        'fips-sa-east-1',
        'fips',
        'rds-fips.ca-central-1',
        'rds-fips.us-east-1',
        'rds-fips.us-east-2',
        'rds-fips.us-west-1',
        'rds-fips.us-west-2',
        's3-external-1'
    ]

    groups = get_selected_regions_and_services(exclude_fips_regions=True)
    assert list(groups.keys()) == [
        'af-south-1',
        'ap-east-1',
        'ap-northeast-1',
        'ap-northeast-2',
        'ap-south-1',
        'ap-southeast-1',
        'ap-southeast-2',
        'ca-central-1',
        'eu-central-1',
        'eu-north-1',
        'eu-south-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'me-south-1',
        'sa-east-1',
        'us-east-1',
        'us-east-2',
        'us-west-1',
        'us-west-2',
        'aws-global',
        's3-external-1'
    ]

    # exclude ap-* regions
    groups = get_selected_regions_and_services(
        exclude_fips_regions=True,
        regions_exclude=[
            'ap-east-1',
            'ap-northeast-1',
            'ap-northeast-2',
            'ap-south-1',
            'ap-southeast-1',
            'ap-southeast-2',
        ]
    )
    assert list(groups.keys()) == [
        'af-south-1',
        'ca-central-1',
        'eu-central-1',
        'eu-north-1',
        'eu-south-1',
        'eu-west-1',
        'eu-west-2',
        'eu-west-3',
        'me-south-1',
        'sa-east-1',
        'us-east-1',
        'us-east-2',
        'us-west-1',
        'us-west-2',
        'aws-global',
        's3-external-1'
    ]


@mock_iam
@mock_sts
@mock_apigateway
def test_get_asset_by_region(apigateway_restapi, aws_session, aws_region, aws_account_id):

    arn = apigateway_restapi(aws_session, aws_region)

    assets_cloud = get_asset_by_region(
        session=aws_session,
        account_id=aws_account_id,
        region=aws_region,
        service='aws.apigateway.restapis'
    )

    inventory_list = list(assets_cloud)
    assert len(inventory_list) == 1
    asset = inventory_list[0]

    assert asset.arn == arn
    assert asset.region == 'us-east-1'
    assert asset.service == 'aws.apigateway.restapis'
    assert asset.account_id == aws_account_id
    assert asset.tags == {}


@mock_iam
@mock_sts
def test_get_credentials(aws_session, aws_region, aws_account_id, aws_delegation_role_name):

    creds = get_credentials(aws_account_id, aws_delegation_role_name)
    assert not creds.get('aws_access_key_id') is None
    assert not creds.get('aws_secret_access_key') is None
    assert not creds.get('aws_session_token') is None
