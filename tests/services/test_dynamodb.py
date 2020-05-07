from moto import mock_dynamodb

from mce_lib_aws.services import dynamodb as service

@mock_dynamodb
def test_table(dynamodb_table, aws_session, aws_region, aws_account_id):

    arn = dynamodb_table(aws_session, aws_region, aws_account_id)

    inventory = service.Table(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1

    asset = inventory_list[0]
    assert arn == asset.arn

    assert 'my-table' == asset.name

    assert 5 == asset.data['ProvisionedThroughput']['ReadCapacityUnits']
    assert 'value1' == asset.tags['key1']

    inventory.set_tags(arn=arn, tags_dict={'key2': 'value2'})

    assert {'key1': 'value1', 'key2': 'value2'} == inventory.get_tags(arn)

    inventory.unset_tags(arn, ['key1'])

    assert {'key2': 'value2'} == inventory.get_tags(arn)
