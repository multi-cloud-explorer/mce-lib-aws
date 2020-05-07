from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class RestApi(AWSResource):
    """
    Required IAM actions:
    """

    boto_service_name = 'apigateway'
    arn_pattern = 'arn:aws:apigateway:{region}::/restapis/{elem[id]}'

    def _listall(self):
        paginator = self.client.get_paginator('get_rest_apis')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for enum in response['items']:
                yield enum
    
    def _parse_name(self, elem, data, tags):
        return elem['name']
