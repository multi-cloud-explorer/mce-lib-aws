from moto import mock_ecs

from mce_lib_aws.services import ecs as service

@mock_ecs
def test_cluster(ecs_cluster, aws_session, aws_region, aws_account_id):

    arn = ecs_cluster(aws_session, aws_region)

    inventory = service.Cluster(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1
    asset = inventory_list[0]
    assert arn == asset.arn

    assert 'myCluster' == asset.name
    assert 0 == asset.data['runningTasksCount']
