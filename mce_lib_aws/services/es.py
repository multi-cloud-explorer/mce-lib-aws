from mce_lib_aws.utils import tags_to_dict, tags_to_list
from mce_lib_aws.common import AWSResource


class Domain(AWSResource):
    """
    Required IAM actions:
    - es:ListDomainNames
    """

    boto_service_name = 'es'
    arn_pattern = 'arn:aws:es:{region}:{account}:domain/{elem[DomainName]}'

    def _listall(self):
        response = self.client.list_domain_names()
        yield from response['DomainNames']

    def _parse_data(self, elem):
        arn = self._parse_arn(elem)
        return self.get_data(arn)

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return elem['DomainName']

    def get_data(self, arn):
        domain_name = arn.split(':')[5].split('/')[1]
        response = self.client.describe_elasticsearch_domain(
            DomainName=domain_name
        )
        return response['DomainStatus']

    def get_tags(self, arn):
        response = self.client.list_tags(ARN=arn)
        tags_dict = tags_to_dict(response['TagList'])
        return tags_dict

    def set_tags(self, arn, tags_dict):
        tags_list = tags_to_list(tags_dict)
        self.client.add_tags(
            ARN=arn,
            TagList=tags_list
        )

    def unset_tags(self, arn, keys):
        self.client.remove_tags(
            ARN=arn,
            TagKeys=keys
        )
