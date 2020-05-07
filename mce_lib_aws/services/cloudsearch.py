from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class Domain(AWSResource):
    """
    Required IAM actions:
    - cloudsearch:AddTags
    - cloudsearch:RemoveTags
    """

    boto_service_name = 'cloudsearch'
    arn_pattern = None

    def _listall(self):
        response = self.client.describe_domains()
        for enum in response['DomainStatusList']:
            yield enum

    def _parse_arn(self, elem):
        return elem['ARN']

    def _parse_name(self, elem, data, tags):
        return elem['DomainName']
