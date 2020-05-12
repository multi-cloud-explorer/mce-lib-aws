from mce_lib_aws.utils import tags_to_dict, tags_to_list
from mce_lib_aws.common import AWSResource


class Topic(AWSResource):
    """
    Required IAM actions:
    - SNS:ListTopics
    """

    boto_service_name = 'sns'
    arn_pattern = None

    def _listall(self):
        paginator = self.client.get_paginator('list_topics')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for elem in response['Topics']:
                yield elem

    def _parse_arn(self, elem):
        return elem['TopicArn']

    def _parse_data(self, elem):
        arn = self._parse_arn(elem)
        return self.get_data(arn)

    def _parse_name(self, elem, data, tags):
        # Attribute DisplayName is not relevant, set Id as name instead
        topic_id = elem['TopicArn'].split(':', 5)[5]
        return topic_id

    def get_data(self, arn):
        response = self.client.get_topic_attributes(TopicArn=arn)
        return response['Attributes']
