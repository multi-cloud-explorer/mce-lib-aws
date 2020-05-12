from mce_lib_aws.utils import tags_to_dict, tags_to_list
from mce_lib_aws.common import AWSResource


class Cluster(AWSResource):
    """
    Required IAM actions:
    - redshift:DescribeClusters
    - redshift:CreateTags
    - redshift:DeleteTags
    """

    boto_service_name = 'redshift'
    arn_pattern = 'arn:aws:redshift:{region}:{account}:cluster:{elem[ClusterIdentifier]}'

    def _listall(self):
        paginator = self.client.get_paginator('describe_clusters')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for elem in response['Clusters']:
                yield elem

    def _parse_name(self, elem, data, tags):
        return elem['ClusterIdentifier']

    def get_tags(self, arn):
        response = self.client.describe_tags(
            ResourceName=arn)
        tags_list = list(i['Tag'] for i in response['TaggedResources'])
        tags_dict = tags_to_dict(tags_list)
        return tags_dict

    def set_tags(self, arn, tags_dict):
        tags_list = tags_to_list(tags_dict)
        self.client.create_tags(
            ResourceName=arn,
            Tags=tags_list
        )

    def unset_tags(self, arn, keys):
        self.client.delete_tags(
            ResourceName=arn,
            TagKeys=keys
        )
