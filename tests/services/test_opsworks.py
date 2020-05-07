from moto import mock_opsworks

from mce_lib_aws.services import opsworks as service

@mock_opsworks
def test_stack(opsworks_stack, aws_session, aws_region, aws_account_id):

    arn = opsworks_stack(aws_session, aws_region, aws_account_id)

    inventory = service.Stack(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1
    asset = inventory_list[0]
    assert arn == asset.arn


    # FIXME: NotImplementedError: The list_tags action has not been implemented
