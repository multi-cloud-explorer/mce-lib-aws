from moto import mock_elasticbeanstalk

from mce_lib_aws.services import elasticbeanstalk as service

@mock_elasticbeanstalk
def test_elastic_beanstalk(aws_session, aws_region, aws_account_id):
    raise  NotImplementedError()
