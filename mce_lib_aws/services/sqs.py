from mce_lib_aws.utils import tags_to_dict, tags_to_list
from mce_lib_aws.common import AWSResource


class Queue(AWSResource):
    """
    Required IAM actions:
    - sqs:ListQueueTags
    - sqs:TagQueue
    - sqs:UntagQueue
    """

    boto_service_name = 'sqs'
    arn_pattern = 'arn:aws:sqs:{region}:{account}:{queue_name}'

    def _listall(self):
        response = self.client.list_queues()
        for queue_url in response.get('QueueUrls', []):
            elem = {
                'QueueUrl': queue_url
            }
            yield elem

    def _parse_arn(self, elem):
        queue_url = elem['QueueUrl']
        queue_name = queue_url.split('/')[-1]
        return self.arn_pattern.format(
            region=self.region,
            account=self.account,
            queue_name=queue_name
        )

    def _parse_data(self, elem):
        arn = self._parse_arn(elem)
        return self.get_data(arn)

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return data['QueueName']

    def get_data(self, arn):
        queue_name = arn.split(':')[5]
        queue_url = 'https://sqs.{}.amazonaws.com/{}/{}'.format(
            self.region,
            self.account,
            queue_name
        )
        response = self.client.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['CreatedTimestamp',
                            'LastModifiedTimestamp',
                            'VisibilityTimeout',
                            'MaximumMessageSize',
                            'MessageRetentionPeriod',
                            'DelaySeconds',
                            'Policy',
                            'ReceiveMessageWaitTimeSeconds'])
        data = response['Attributes']
        data = {}
        data['QueueName'] = queue_name
        return data

    def get_tags(self, arn):
        queue_name = arn.split(':')[5]
        queue_url = 'https://sqs.{}.amazonaws.com/{}/{}'.format(
            self.region,
            self.account,
            queue_name
        )
        response = self.client.list_queue_tags(QueueUrl=queue_url)
        tags_dict = response.get('Tags', {})
        return tags_dict

    def set_tags(self, arn, tags_dict):
        queue_name = arn.split(':')[5]
        queue_url = 'https://sqs.{}.amazonaws.com/{}/{}'.format(
            self.region,
            self.account,
            queue_name
        )
        self.client.tag_queue(
            QueueUrl=queue_url,
            Tags=tags_dict
        )

    def unset_tags(self, arn, keys):
        queue_name = arn.split(':')[5]
        queue_url = 'https://sqs.{}.amazonaws.com/{}/{}'.format(
            self.region,
            self.account,
            queue_name
        )
        self.client.untag_queue(
            QueueUrl=queue_url,
            TagKeys=keys
        )
