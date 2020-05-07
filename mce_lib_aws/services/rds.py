from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class DbInstance(AWSResource):
    """
    Required IAM actions:
    - rds:AddTagsToResource
    - rds:RemoveTagsFromResource
    """

    boto_service_name = 'rds'
    arn_pattern = 'arn:aws:rds:{region}:{account}:db:{elem[DBInstanceIdentifier]}'

    def _listall(self):
        paginator = self.client.get_paginator('describe_db_instances')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for elem in response['DBInstances']:
                yield elem

    def _parse_data(self, elem):
        elem['LatestRestorableTime'] = ''
        return elem

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return elem['DBInstanceIdentifier']

    def get_tags(self, arn):
        response = self.client.list_tags_for_resource(
            ResourceName=arn
        )
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
