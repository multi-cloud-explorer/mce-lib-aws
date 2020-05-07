from moto import mock_elbv2

from mce_lib_aws.services import elbv2 as service

@mock_elbv2
def test_load_balancer(elb_v2, aws_session, aws_region, aws_account_id):

    arn = elb_v2(aws_session, aws_region, aws_account_id)

    inventory = service.Loadbalancer(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1
    asset = inventory_list[0]
    assert arn == asset.arn

    assert 'my-loadbalancer' == asset.name
    assert 'my-loadbalancer-1.us-east-1.elb.amazonaws.com' == asset.data['DNSName']
    assert 'value1' == asset.tags['key1']

    inventory.set_tags(arn=arn, tags_dict={'key2': 'value2'})

    assert {'key1': 'value1', 'key2': 'value2'} == inventory.get_tags(arn)

    inventory.unset_tags(arn, ['key1'])

    assert {'key2': 'value2'} == inventory.get_tags(arn)
