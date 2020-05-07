import boto3
from moto import mock_iam, mock_sts, mock_apigateway

from mce_lib_aws.crawler import get_cloud_assets

@mock_iam
@mock_sts
@mock_apigateway
def test_crawler(apigateway_restapi, aws_session, aws_region, aws_account_id, aws_delegation_role_name):

    arn = apigateway_restapi(aws_session, aws_region)

    iam_client = aws_session.client('iam', region_name=aws_region)
    iam_client.create_account_alias(AccountAlias='mock-account')

    assets_cloud = get_cloud_assets(
        account_id=aws_account_id,
        delegation_role_name=aws_delegation_role_name,
        resources_allowed=['aws.apigateway.restapis'],
        regions_allowed=[aws_region]
    )

    inventory_list = list(assets_cloud)

    assert len(inventory_list) == 1

    resource_name, region, asset = inventory_list[0]
    assert 'aws.apigateway.restapis' == resource_name
    assert 'us-east-1' == region
    assert arn == asset.arn

"""
    assets_cloud = get_cloud_assets(account_id='123456789012',
                                    delegation_role_name='LinkbynetInventoryRole',
                                    resources_allowed=['aws.acm.certificate'],
                                    regions_allowed=['us-east-1'])


    inventory_list = list(assets_cloud)
    self.assertEqual(1, len(inventory_list))

    resource_name, region, asset = inventory_list[0]
    self.assertEqual('aws.acm.certificate', resource_name)
    self.assertEqual('us-east-1', region)
    self.assertEqual(self.arn, asset.arn)

"""