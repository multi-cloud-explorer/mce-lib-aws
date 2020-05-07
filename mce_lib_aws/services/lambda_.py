from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class Function(AWSResource):
    """
    Required IAM actions:
    - lambda:TagResource
    - lambda:UntagResource*
    """

    boto_service_name = 'lambda'
    arn_pattern = None

    def _listall(self):
        paginator = self.client.get_paginator('list_functions')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for elem in response['Functions']:
                yield elem

    def _parse_arn(self, elem):
        return elem['FunctionArn']

    def _parse_data(self, elem):
        arn = self._parse_arn(elem)
        return self.get_data(arn)

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return elem['FunctionName']

    def get_data(self, arn):
        data = {
            'EventSources': []
        }
        function_name = arn.split(':')[6]
        response = self.client.list_event_source_mappings(FunctionName=function_name)
        for esm in response['EventSourceMappings']:
            data['EventSources'].append(esm['EventSourceArn'])
        return data

    def get_tags(self, arn):
        response = self.client.list_tags(Resource=arn)
        tags_dict = response['Tags']
        return tags_dict

    def set_tags(self, arn, tags_dict):
        self.client.tag_resource(
            Resource=arn,
            Tags=tags_dict
        )

    def unset_tags(self, arn, keys):
        self.client.untag_resource(
            Resource=arn,
            TagKeys=keys
        )
