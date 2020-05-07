from unittest.mock import patch
from moto import mock_rds2

from mce_lib_aws.services import rds as service

@mock_rds2
def test_dbinstance(rds_db_instance, aws_session, aws_region, aws_account_id):

    arn = rds_db_instance(aws_session, aws_region, aws_account_id)

    with patch("mce_lib_aws.services.rds.DbInstance.get_tags") as func:
        func.return_value = {"key1": "value1"}

        inventory = service.DbInstance(aws_region, aws_account_id, aws_session)
        inventory_list = list(inventory)

        assert len(inventory_list) == 1
        asset = inventory_list[0]

        # FIXME: assert arn == asset.arn

        assert 'value1' == asset.tags['key1']

