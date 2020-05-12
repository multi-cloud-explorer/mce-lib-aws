from mce_lib_aws.utils import tags_to_dict, tags_to_list
from mce_lib_aws.common import AWSResource


class Cluster(AWSResource):
    """
    Required IAM actions:
    - elasticache:DescribeCacheClusters
    """

    boto_service_name = 'elasticache'
    arn_pattern = None

    def _listall(self):
        paginator = self.client.get_paginator('describe_cache_clusters')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for enum in response['CacheClusters']:
                yield enum

    def _parse_arn(self, elem):
        cluster_id = elem['CacheClusterId']
        return 'arn:aws:elasticache:{}:{}:cluster:{}'.format(
            self.region,
            self.account,
            cluster_id
        )

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return elem['CacheClusterId']

    def get_tags(self, arn):
        response = self.client.list_tags_for_resource(ResourceName=arn)
        tags_dict = tags_to_dict(response['TagList'])
        return tags_dict

    def set_tags(self, arn, tags_dict):
        tags_list = tags_to_list(tags_dict)
        self.client.add_tags_to_resource(
            ResourceName=arn,
            Tags=tags_list
        )

    def unset_tags(self, arn, keys):
        self.client.remove_tags_from_resource(
            ResourceName=arn,
            TagKeys=keys
        )
