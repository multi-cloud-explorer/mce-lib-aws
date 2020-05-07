from moto import mock_redshift

from mce_lib_aws.services import redshift as service

@mock_redshift
def test_redshift(redshift_cluster, aws_session, aws_region, aws_account_id):

    arn = redshift_cluster(aws_session, aws_region, aws_account_id)

    inventory = service.Cluster(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1
    asset = inventory_list[0]
    assert arn == asset.arn

    assert 'mycluster' == asset.name
    assert 'ds2.xlarge' == asset.data['NodeType']
    assert 'value1' == asset.tags['key1']

    inventory.set_tags(arn=arn, tags_dict={'key2': 'value2'})

    assert {'key1': 'value1', 'key2': 'value2'} == inventory.get_tags(arn)

    inventory.unset_tags(arn, ['key1'])

    assert {'key2': 'value2'} == inventory.get_tags(arn)
