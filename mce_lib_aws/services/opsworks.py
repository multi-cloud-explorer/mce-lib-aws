from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class Stack(AWSResource):
    """
    Required IAM actions:
    - opsworks:ListTags
    - opsworks:TagResource
    - opsworks:UnTagResource
    """

    boto_service_name = 'opsworks'
    arn_pattern = None

    def _listall(self):
        response = self.client.describe_stacks()
        yield from response['Stacks']

    def _parse_arn(self, elem):
        return elem['Arn']

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return elem['Name']

    def get_tags(self, arn):
        response = self.client.list_tags(ResourceArn=arn)
        tags_dict = response['Tags']
        return tags_dict

    def set_tags(self, arn, tags_dict):
        self.client.tag_resource(
            ResourceArn=arn,
            Tags=tags_dict
        )

    def unset_tags(self, arn, keys):
        self.client.untag_resource(
            ResourceArn=arn,
            TagKeys=keys
        )
