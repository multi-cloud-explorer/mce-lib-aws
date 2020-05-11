from moto import mock_iam, mock_sts, mock_apigateway

import boto3
from mce_lib_aws.crawler import get_cloud_assets, get_credentials

@mock_iam
@mock_sts
@mock_apigateway
def test_crawler(apigateway_restapi, aws_session, aws_region, aws_account_id):

    arn = apigateway_restapi(aws_session, aws_region)

    #iam_client = aws_session.client('iam', region_name=aws_region)
    #iam_client.create_account_alias(AccountAlias='mock-account')

    assets_cloud = get_cloud_assets(
        session=aws_session,
        account_id=aws_account_id,
        resources_allowed=['aws.apigateway.restapis'],
        regions_allowed=[aws_region]
    )

    inventory_list = list(assets_cloud)

    assert len(inventory_list) == 1

    resource_name, region, asset = inventory_list[0]
    assert 'aws.apigateway.restapis' == resource_name
    assert 'us-east-1' == region
    assert arn == asset.arn

@mock_iam
@mock_sts
@mock_apigateway
def test_crawler_with_role_delegation(apigateway_restapi, aws_session, aws_region, aws_account_id, aws_delegation_role_name):

    arn = apigateway_restapi(aws_session, aws_region)

    creds = get_credentials(aws_account_id, aws_delegation_role_name)
    session = boto3.Session(region_name=aws_region, **creds)

    assets_cloud = get_cloud_assets(
        session=session,
        account_id=aws_account_id,
        resources_allowed=['aws.apigateway.restapis'],
        regions_allowed=[aws_region]
    )

    inventory_list = list(assets_cloud)

    assert len(inventory_list) == 1

    resource_name, region, asset = inventory_list[0]
    assert 'aws.apigateway.restapis' == resource_name
    assert 'us-east-1' == region
    assert arn == asset.arn
