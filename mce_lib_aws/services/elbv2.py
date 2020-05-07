from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class Loadbalancer(AWSResource):
    """
    Required IAM actions:
    - elasticloadbalancing:AddTags
    - elasticloadbalancing:RemoveTags
    """

    boto_service_name = 'elbv2'
    arn_pattern = None

    def _listall(self):
        paginator = self.client.get_paginator('describe_load_balancers')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for enum in response['LoadBalancers']:
                yield enum

    def _parse_arn(self, elem):
        return elem['LoadBalancerArn']

    def _parse_data(self, elem):
        arn = self._parse_arn(elem)
        return self.get_data(arn)

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return elem['LoadBalancerName']

    def get_data(self, arn):
        response = self.client.describe_listeners(
            LoadBalancerArn=arn,
        )
        data = {
            'Listeners': response['Listeners']
        }
        return data

    def get_tags(self, arn):
        response = self.client.describe_tags(
            ResourceArns=[arn],
        )
        tags_dict = tags_to_dict(response['TagDescriptions'][0]['Tags'])
        return tags_dict

    def set_tags(self, arn, tags_dict):
        tags_list = tags_to_list(tags_dict)
        self.client.add_tags(
            ResourceArns=[arn],
            Tags=tags_list
        )

    def unset_tags(self, arn, keys):
        self.client.remove_tags(
            ResourceArns=[arn],
            TagKeys=keys
        )
