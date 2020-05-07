from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class Application(AWSResource):
    """
    Required IAM actions:
    """

    boto_service_name = 'elasticbeanstalk'
    arn_pattern = None

    def _listall(self):
        response = self.client.describe_applications()
        yield from response['Applications']

    def _parse_arn(self, elem):
        return elem['ApplicationArn']

    def _parse_data(self, elem):
        arn = self._parse_arn(elem)
        return self.get_data(arn)

    def _parse_name(self, elem, data, tags):
        return elem['ApplicationName']


class Environment(AWSResource):
    """
    Required IAM actions:
    - elasticbeanstalk:UpdateEnvironment
    - elasticbeanstalk:AddTags
    """

    boto_service_name = 'elasticbeanstalk'
    arn_pattern = None

    def _listall(self):
        response = self.client.describe_environments()
        yield from response['Environments']

    def _parse_arn(self, elem):
        return elem['EnvironmentArn']

    def _parse_data(self, elem):
        arn = self._parse_arn(elem)
        return self.get_data(arn)

    def _parse_name(self, elem, data, tags):
        return elem['EnvironmentName']
