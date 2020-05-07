from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class AutoScalingGroup(AWSResource):
    """
    Required IAM actions:
    - autoscaling:CreateOrUpdateTags
    - autoscaling:DeleteTags
    """

    boto_service_name = 'autoscaling'
    arn_pattern = None

    def _listall(self):
        paginator = self.client.get_paginator('describe_auto_scaling_groups')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for enum in response['AutoScalingGroups']:
                yield enum

    def _parse_arn(self, elem):
        return elem['AutoScalingGroupARN']

    def _parse_data(self, elem):
        # Reorder lists to avoid false change detection
        elem['EnabledMetrics'].sort(key=lambda item: item['Metric'])
        elem['SuspendedProcesses'].sort(key=str)
        return elem

    def _parse_name(self, elem, data, tags):
        return elem['AutoScalingGroupName']

    def get_tags(self, arn):
        group_name = arn.split(':')[-1].split('/')[-1]
        response = self.client.describe_tags(
            Filters=[
                {
                    'Name': 'auto-scaling-group',
                    'Values': [group_name]
                }
            ]
        )
        tags_dict = tags_to_dict(response['Tags'])
        return tags_dict

    def set_tags(self, arn, tags_dict):
        asg_name = arn.split(':')[7].split('/')[1]
        addon = dict(ResourceId=asg_name,
                     ResourceType='auto-scaling-group',
                     PropagateAtLaunch=False)
        tags_list = tags_to_list(tags_dict, addon=addon)
        self.client.create_or_update_tags(Tags=tags_list)

    def unset_tags(self, arn, keys):
        asg_name = arn.split(':')[7].split('/')[1]
        addon = dict(ResourceId=asg_name,
                     ResourceType='auto-scaling-group',
                     PropagateAtLaunch=False)
        tags_list = [dict(Key=k, **addon) for k in keys]
        self.client.delete_tags(Tags=tags_list)
