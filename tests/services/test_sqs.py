from moto import mock_sqs

from mce_lib_aws.services import sqs as service

@mock_sqs
def test_sqs(sqs_queue, aws_session, aws_region, aws_account_id):

    arn = sqs_queue(aws_session, aws_region, aws_account_id)

    inventory = service.Queue(aws_region, aws_account_id, aws_session)

    inventory_list = list(inventory)

    assert len(inventory_list) == 1
    asset = inventory_list[0]
    assert arn == asset.arn

    assert 'myqueue' == asset.name
    assert 'myqueue' == asset.data['QueueName']
    assert 'value1' == asset.tags['key1']

    inventory.set_tags(arn=arn, tags_dict={'key2': 'value2'})

    assert {'key1': 'value1', 'key2': 'value2'} == inventory.get_tags(arn)

    inventory.unset_tags(arn, ['key1'])

    assert {'key2': 'value2'} == inventory.get_tags(arn)
