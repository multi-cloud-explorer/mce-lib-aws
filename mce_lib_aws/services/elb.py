from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class Loadbalancer(AWSResource):
    """
    Required IAM actions:
    - elasticloadbalancing:AddTags
    - elasticloadbalancing:RemoveTags
    """

    boto_service_name = 'elb'
    arn_pattern = 'arn:aws:elasticloadbalancing:{region}:{account}:loadbalancer/{elem[LoadBalancerName]}'

    def _listall(self):
        paginator = self.client.get_paginator('describe_load_balancers')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for enum in response['LoadBalancerDescriptions']:
                yield enum

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return elem['LoadBalancerName']

    def get_tags(self, arn):
        loadbalancer_name = arn.split(':')[-1].split('/')[-1]
        response = self.client.describe_tags(
            LoadBalancerNames=[loadbalancer_name]
        )
        tags_dict = tags_to_dict(response['TagDescriptions'][0]['Tags'])
        return tags_dict

    def set_tags(self, arn, tags_dict):
        loadbalancer_name = arn.split(':')[-1].split('/')[-1]
        tags_list = tags_to_list(tags_dict)
        self.client.add_tags(
            LoadBalancerNames=[loadbalancer_name],
            Tags=tags_list
        )

    def unset_tags(self, arn, keys):
        loadbalancer_name = arn.split(':')[-1].split('/')[-1]
        tags_list = list(dict(Key=i) for i in keys)
        self.client.remove_tags(
            LoadBalancerNames=[loadbalancer_name],
            Tags=tags_list
        )
