from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class Stack(AWSResource):
    """
    Required IAM actions:
    - cloudformation:UpdateStack
    """

    boto_service_name = 'cloudformation'
    arn_pattern = None

    def _listall(self):
        paginator = self.client.get_paginator('describe_stacks')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for enum in response['Stacks']:
                yield enum

    def _parse_arn(self, elem):
        return elem['StackId']

    def _parse_data(self, elem):
        arn = self._parse_arn(elem)
        return self.get_data(arn)

    def _parse_name(self, elem, data, tags):
        return elem['StackName']

    def get_data(self, arn):
        stack_name = arn.split(':')[5].split('/')[1]
        response = self.client.describe_stack_resources(
            StackName=stack_name
        )
        data = {
            'Resources': [dict(id=item.get('PhysicalResourceId', item.get('LogicalResourceId')),
                               type=item.get('ResourceType')) 
                          for item in response['StackResources']
            ]
        }
        return data

    def get_tags(self, arn):
        stack_name = arn.split(':')[5].split('/')[1]
        response = self.client.describe_stacks(StackName=stack_name)
        tags_dict = tags_to_dict(response['Stacks'][0]['Tags'])
        return tags_dict
