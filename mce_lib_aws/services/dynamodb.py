from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class Table(AWSResource):
    """
    Required IAM actions:
    - dynamodb:TagResource
    - dynamodb:UntagResource
    """

    boto_service_name = 'dynamodb'
    arn_pattern = 'arn:aws:dynamodb:{region}:{account}:table/{elem}'

    def _listall(self):
        paginator = self.client.get_paginator('list_tables')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for enum in response['TableNames']:
                yield enum

    def _parse_data(self, elem):
        arn = self._parse_arn(elem)
        return self.get_data(arn)

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return elem

    def get_data(self, arn):
        table_name = arn.split(':')[5].split('/')[1]
        response = self.client.describe_table(TableName=table_name)
        return response['Table']

    def get_tags(self, arn):
        response = self.client.list_tags_of_resource(ResourceArn=arn)
        tags_dict = tags_to_dict(response['Tags'])
        return tags_dict

    def set_tags(self, arn, tags_dict):
        tags_list = tags_to_list(tags_dict)
        self.client.tag_resource(
            ResourceArn=arn,
            Tags=tags_list
        )

    def unset_tags(self, arn, keys):
        self.client.untag_resource(
            ResourceArn=arn,
            TagKeys=keys
        )
