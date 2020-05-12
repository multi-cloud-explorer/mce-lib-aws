import pytest
from pprint import pprint
from moto import mock_autoscaling, mock_ec2

from mce_lib_aws.services import autoscaling as service

# @mock_ec2
# @mock_autoscaling
@pytest.mark.mce_known_bug
def test_auto_scaling_group(auto_scaling_group, aws_session, aws_region, aws_account_id):

    arn = auto_scaling_group(aws_session, aws_region)
    # print('!!! arn : ', arn)

    inventory = service.AutoScalingGroup(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1

    asset = inventory_list[0]

    # print('!!! asset.arn : ', asset.arn)
    # pprint(dict(asset._asdict()))

    assert arn == asset.arn
    assert 'my-auto-scaling-group' == asset.name
    assert 'my-launch-config' == asset.data['LaunchConfigurationName']
    # self.assertEqual(mocked_networking["subnet1"], asset.data['VPCZoneIdentifier'])
    assert 'value1' == asset.tags['key1']


    # inventory.set_tags(arn=self.arn, tags_dict={'key2': 'value2'})

    # self.assertEqual(
    #     {'key1': 'value1', 'key2': 'value2'},
    #     inventory.get_tags(self.arn)
    # )

    # inventory.unset_tags(self.arn, ['key1'])

    # self.assertEqual(
    #     {'key2': 'value2'},
    #     certs.get_tags(self.arn)
    # )
