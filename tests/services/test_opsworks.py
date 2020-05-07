from unittest.mock import patch
from moto import mock_opsworks

from mce_lib_aws.services import opsworks as service

@mock_opsworks
def test_opsworks_stack(opsworks_stack, aws_session, aws_region, aws_account_id):

    arn = opsworks_stack(aws_session, aws_region, aws_account_id)

    with patch("mce_lib_aws.services.opsworks.Stack.get_tags") as func:
        func.return_value = {"key1": "value1"}

        inventory = service.Stack(region=aws_region, account=aws_account_id, session=aws_session)
        inventory_list = list(inventory)

        assert len(inventory_list) == 1
        asset = inventory_list[0]

        # FIXME: assert arn == asset.arn

        assert 'value1' == asset.tags['key1']

"""
{'arn': 'arn:aws:opsworks:us-east-1:123456789012:stack/33951734-4737-47c6-b121-21b39c880539',
 'data': {'Arn': 'arn:aws:opsworks:us-east-1:123456789012:stack/33951734-4737-47c6-b121-21b39c880539',
          'Attributes': {'Color': None},
          'ChefConfiguration': {},
          'ConfigurationManager': {'Name': 'Chef', 'Version': '11.4'},
          'CreatedAt': '2020-05-07T02:21:27.014880',
          'CustomCookbooksSource': {},
          'DefaultInstanceProfileArn': 'arn:aws:iam::803981987763:instance-profile/aws-opsworks-ec2-role',
          'DefaultSubnetId': 'arn:aws:iam::803981987763:instance-profile/aws-opsworks-ec2-role',
          'Name': 'my-stack',
          'Region': 'us-east-1',
          'ServiceRoleArn': 'arn:aws:iam::803981987763:role/aws-opsworks-service-role',
          'StackId': '33951734-4737-47c6-b121-21b39c880539'},
 'name': 'my-stack',
 'tags': {'key1': 'value1'}}
"""