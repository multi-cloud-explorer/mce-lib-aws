from moto import mock_s3

from mce_lib_aws.services import s3 as service

@mock_s3
def test_s3(s3_bucket_with_tags, aws_session, aws_region, aws_account_id):

    arn = s3_bucket_with_tags(aws_session, aws_region)

    inventory = service.Bucket(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1
    asset = inventory_list[0]
    assert arn == asset.arn

    assert 'mybucket0' == asset.name
    assert 'mybucket0' == asset.data['Name']
    assert 'value1' == asset.tags.get('key1')

    inventory.set_tags(arn=arn, tags_dict={'key2': 'value2'})

    assert {'key1': 'value1', 'key2': 'value2'} == inventory.get_tags(arn)

    inventory.unset_tags(arn, ['key1'])

    assert {'key2': 'value2'} == inventory.get_tags(arn)

    # session = boto3.Session(region_name='eu-west-1')
    # inventory = s3.Bucket('eu-west-1', aws_account_id, session)
    # inventory_list = list(inventory)
    # self.assertEqual(1, len(inventory_list))
    #
    # asset = inventory_list[0]
    # self.assertEqual(self.arn1, asset.arn)
    #
    # self.assertEqual('mybucket1', asset.name)
    # self.assertEqual('mybucket1', asset.data['Name'])
    # self.assertEqual(None, asset.tags.get('key1'))
    #
    # inventory.set_tags(arn=self.arn1, tags_dict={'key2': 'value2'})
    #
    # self.assertEqual(
    #     {'key2': 'value2'},
    #     inventory.get_tags(self.arn1)
    # )
