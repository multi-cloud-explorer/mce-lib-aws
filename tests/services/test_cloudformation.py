from moto import mock_cloudformation

from mce_lib_aws.services import cloudformation as service

@mock_cloudformation
def test_cloudformation(cloud_formation_stack, aws_session, aws_region, aws_account_id):

    arn = cloud_formation_stack(aws_session, aws_region)

    inventory = service.Stack(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1

    asset = inventory_list[0]
    assert arn == asset.arn

    assert 'my-stack' == asset.name
    assert asset.data['DisableRollback'] is False
    assert ['arn:aws:sns:region:account-id:topicname'] == asset.data['NotificationARNs']

    assert 'value1' == asset.tags['key1']

    assert {'key1': 'value1'} == inventory.get_tags(arn)
