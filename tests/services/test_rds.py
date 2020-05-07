from moto import mock_rds

from mce_lib_aws.services import rds as service

@mock_rds
def test_dbinstance(rds_db_instance, aws_session, aws_region, aws_account_id):

    arn = rds_db_instance(aws_session, aws_region, aws_account_id)

    inventory = service.DbInstance(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1
    asset = inventory_list[0]
    assert arn == asset.arn

    # FIXME: NotImplementedError: The list_tags_for_resource action has not been implemented
