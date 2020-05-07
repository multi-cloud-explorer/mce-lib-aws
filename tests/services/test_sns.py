from moto import mock_sns

from mce_lib_aws.services import sns as service

@mock_sns
def test_sns(sns_topic, aws_session, aws_region, aws_account_id):

    arn = sns_topic(aws_session, aws_region, aws_account_id)

    inventory = service.Topic(aws_region, aws_account_id, aws_session)

    inventory_list = list(inventory)

    assert len(inventory_list) == 1
    asset = inventory_list[0]
    assert arn == asset.arn

    assert 'mytopic' == asset.name
