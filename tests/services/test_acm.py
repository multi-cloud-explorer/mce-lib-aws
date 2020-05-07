from moto import mock_acm

from mce_lib_aws.services import acm as service

@mock_acm
def test_acm(acm_certificate, aws_session, aws_region, aws_account_id):

    arn = acm_certificate(aws_session, aws_region)
    inventory = service.Certificate(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1
    asset = inventory_list[0]
    assert arn == asset.arn

    assert 'example.com' == asset.name
    subject_alternative_names = asset.data['SubjectAlternativeNames']
    subject_alternative_names.sort()
    assert ['example.com', 'www.example.com'] == subject_alternative_names
    assert 'value1' == asset.tags['key1']

    inventory.set_tags(arn=arn, tags_dict={'key2': 'value2'})

    assert {'key1': 'value1', 'key2': 'value2'} == inventory.get_tags(arn)

    inventory.unset_tags(arn, ['key1'])

    assert {'key2': 'value2'} == inventory.get_tags(arn)

