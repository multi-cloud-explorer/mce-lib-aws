from mce_lib_aws.utils import tags_to_dict, tags_to_list
from mce_lib_aws.common import AWSResource


class Distribution(AWSResource):
    """
    Required IAM actions:
    - cloudfront:TagResource
    - cloudfront:UntagResource
    """

    boto_service_name = 'cloudfront'
    arn_pattern = None

    def _listall(self):
        paginator = self.client.get_paginator('list_distributions')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for enum in response['DistributionList']['Items']:
                yield enum

    def _parse_arn(self, elem):
        return elem['ARN']

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return elem['Id']

    def get_tags(self, arn):
        response = self.client.list_tags_for_resource(Resource=arn)
        tags_dict = tags_to_dict(response['Tags']['Items'])
        return tags_dict

    def set_tags(self, arn, tags_dict):
        tags_list = tags_to_list(tags_dict)
        self.client.tag_resource(
            Resource=arn,
            Tags={
                'Items': tags_list
            }
        )

    def unset_tags(self, arn, keys):
        self.client.untag_resource(
            Resource=arn,
            TagKeys={
                'Items': keys
            }
        )
