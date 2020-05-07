from moto import mock_ec2

from mce_lib_aws.services import ec2

@mock_ec2
def test_instance(ec2_instance, aws_session, aws_region, aws_account_id):

    arn = ec2_instance(aws_session, aws_region, aws_account_id)
    instance_id = arn.split("/")[:1]

    inventory = ec2.Instance(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1

    asset = inventory_list[0]
    assert arn == asset.arn

    assert 'my-table' == asset.name

    assert instance_id == asset.name
    assert 'm4.large' == asset.data['InstanceType']
    assert 'value1' == asset.tags['key1']

    inventory.set_tags(arn=arn, tags_dict={'key2': 'value2'})

    assert {'key1': 'value1', 'key2': 'value2'} == inventory.get_tags(arn)

    inventory.unset_tags(arn, ['key1'])

    assert {'key2': 'value2'} == inventory.get_tags(arn)

