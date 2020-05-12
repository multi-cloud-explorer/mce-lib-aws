from mce_lib_aws.utils import tags_to_dict, tags_to_list
from mce_lib_aws.common import AWSResource


class Cluster(AWSResource):
    """
    Required IAM actions:
    - ecs:TagResource
    - ecs:UntagResource
    """

    boto_service_name = 'ecs'
    arn_pattern= None

    def _listall(self):
        paginator = self.client.get_paginator('list_clusters')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for enum in response['clusterArns']:
                yield enum

    def _parse_arn(self, elem):
        return elem

    def _parse_data(self, elem):
        arn = self._parse_arn(elem)
        return self.get_data(arn)

    def _parse_tags(self, elem, data):
        tags_list = data.get('tags', [])
        return tags_to_dict(tags_list)

    def _parse_name(self, elem, data, tags):
        return data['clusterName']

    def get_data(self, arn):
        response = self.client.describe_clusters(clusters=[arn])
        return response['clusters'][0]
