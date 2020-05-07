import boto3

from moto import mock_apigateway

from mce_lib_aws.services import apigateway as service

@mock_apigateway
def test_apigateway(apigateway_restapi, aws_session, aws_region, aws_account_id):

    arn = apigateway_restapi(aws_session, aws_region)

    inventory = service.RestApi(aws_region, aws_account_id, aws_session)

    inventory_list = list(inventory)

    assert len(inventory_list) == 1

    asset = inventory_list[0]
    assert arn == asset.arn
    assert 'myapi' == asset.name
    assert 'My Test API' == asset.data['description']

