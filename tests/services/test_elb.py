from moto import mock_elb

from mce_lib_aws.services import elb as service

@mock_elb
def test_loadbalancer(elb_load_balancer, aws_session, aws_region, aws_account_id):

    arn = elb_load_balancer(aws_session, aws_region, aws_account_id)

    inventory = service.Loadbalancer(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1
    asset = inventory_list[0]
    assert arn == asset.arn

    assert 'my-loadbalancer' == asset.name
    assert 'my-loadbalancer.us-east-1.elb.amazonaws.com' == asset.data['DNSName']
    assert 'value1' == asset.tags['key1']

    inventory.set_tags(arn=arn, tags_dict={'key2': 'value2'})

    assert {'key1': 'value1', 'key2': 'value2'} == inventory.get_tags(arn)

    inventory.unset_tags(arn, ['key1'])

    assert {'key2': 'value2'} == inventory.get_tags(arn)
