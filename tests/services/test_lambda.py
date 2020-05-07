from moto import mock_lambda

from mce_lib_aws.services import lambda_ as service

import pytest

@pytest.mark.mce_todo
@mock_lambda
def test_lambda(aws_session, aws_region, aws_account_id):
    raise  NotImplementedError()
