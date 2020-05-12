from mce_lib_aws.utils import tags_to_dict, tags_to_list
from mce_lib_aws.common import AWSResource


class Certificate(AWSResource):
    """
    Required IAM actions:
    - acm:ListCertificates
    - acm:AddTagsToCertificate
    - acm:RemoveTagsFromCertificate
    """

    boto_service_name = 'acm'
    arn_pattern = None

    def _listall(self):
        paginator = self.client.get_paginator('list_certificates')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for enum in response['CertificateSummaryList']:
                yield enum

    def _parse_arn(self, elem):
        return elem['CertificateArn']

    def _parse_data(self, elem):
        arn = self._parse_arn(elem)
        return self.get_data(arn)

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return elem['DomainName']

    def get_data(self, arn):
        response = self.client.describe_certificate(CertificateArn=arn)
        return response['Certificate']

    def get_tags(self, arn):
        response = self.client.list_tags_for_certificate(CertificateArn=arn)
        tags_dict = tags_to_dict(response['Tags'])
        return tags_dict

    def set_tags(self, arn, tags_dict):
        tags_list = tags_to_list(tags_dict)
        self.client.add_tags_to_certificate(
            CertificateArn=arn,
            Tags=tags_list
        )

    def unset_tags(self, arn, keys):
        tags_list = list(dict(Key=i) for i in keys)
        self.client.remove_tags_from_certificate(
            CertificateArn=arn,
            Tags=tags_list
        )
