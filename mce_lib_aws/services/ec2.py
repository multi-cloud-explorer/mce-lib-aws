from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class Instance(AWSResource):
    """
    Required IAM actions:
    - ec2:CreateTags
    - ec2:DeleteTags
    """

    boto_service_name = 'ec2'
    arn_pattern = 'arn:aws:ec2:{region}:{account}:instance/{elem[InstanceId]}'

    def _listall(self):
        response = self.client.describe_instances()
        for reservations in response['Reservations']:
            yield from reservations['Instances']

    def _parse_name(self, elem, data, tags):
        tag_name = tags.get('Name')
        if tag_name:
            return tag_name
        return data['InstanceId']

    def get_tags(self, arn):
        resource_id = arn.split(':')[-1].split('/')[-1]
        response = self.client.describe_tags(
            Filters=[
                {
                    'Name': 'resource-id',
                    'Values': [resource_id]
                },
                {
                    'Name': 'resource-type',
                    'Values': ['instance']
                }
            ],
        )
        tags_dict = tags_to_dict(response['Tags'])
        return tags_dict

    def set_tags(self, arn, tags_dict):
        tags_list = tags_to_list(tags_dict)
        resource_id = arn.split('/')[-1].split('/')[-1]
        self.client.create_tags(
            Resources=[resource_id],
            Tags=tags_list
        )

    def unset_tags(self, arn, keys):
        tags_list = list(dict(Key=i) for i in keys)
        resource_id = arn.split(':')[-1].split('/')[-1]
        self.client.delete_tags(
            Resources=[resource_id],
            Tags=tags_list
        )
