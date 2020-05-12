from moto import mock_ec2
from freezegun import freeze_time

from mce_lib_aws.services import ec2 as service

@freeze_time("2019-01-01")
@mock_ec2
def test_instance(ec2_instance, aws_session, aws_region, aws_account_id):

    arn = ec2_instance(aws_session, aws_region, aws_account_id)
    # arn:aws:ec2:us-east-1:803981987763:instance/i-5ef96e7063abde113
    instance_id = arn.split("/")[1]

    inventory = service.Instance(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1

    asset = inventory_list[0]

    # from pprint import pprint
    # pprint(inventory_list[0]._asdict())

    assert arn == asset.arn

    assert instance_id == asset.name
    assert 'm4.large' == asset.data['InstanceType']
    assert 'value1' == asset.tags['key1']

    inventory.set_tags(arn=arn, tags_dict={'key2': 'value2'})

    assert {'key1': 'value1', 'key2': 'value2'} == inventory.get_tags(arn)

    inventory.unset_tags(arn, ['key1'])

    assert {'key2': 'value2'} == inventory.get_tags(arn)

