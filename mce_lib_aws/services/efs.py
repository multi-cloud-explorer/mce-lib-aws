from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class Filesystem(AWSResource):
    """
    Required IAM actions:
    - elasticfilesystem:CreateTags
    - elasticfilesystem:DeleteTags
    """

    boto_service_name = 'efs'
    arn_pattern = 'arn:aws:elasticfilesystem:{region}:{account}:file-system-id/{elem[FileSystemId]}'

    def _listall(self):
        paginator = self.client.get_paginator('describe_file_systems')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for enum in response['FileSystems']:
                yield enum

    def _parse_data(self, elem):
        # Reset to zero the fluctuant data
        elem['SizeInBytes'] = 0
        return elem

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        tag_name = tags.get('Name')
        if tag_name:
            return tag_name
        return data['FileSystemId']

    def get_tags(self, arn):
        filesystem_id = arn.split(':')[5].split('/')[1]
        response = self.client.describe_tags(FileSystemId=filesystem_id)
        tags_dict = tags_to_dict(response['Tags'])
        return tags_dict

    def set_tags(self, arn, tags_dict):
        filesystem_id = arn.split(':')[5].split('/')[1]
        tags_list = tags_to_list(tags_dict)
        self.client.create_tags(
            FileSystemId=filesystem_id,
            Tags=tags_list
        )

    def unset_tags(self, arn, keys):
        filesystem_id = arn.split(':')[5].split('/')[1]
        self.client.delete_tags(
            FileSystemId=filesystem_id,
            TagKeys=keys
        )
