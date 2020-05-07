from moto import mock_ec2
from freezegun import freeze_time

from mce_lib_aws.services import ec2 as service

@freeze_time("2019-01-01")
@mock_ec2
def test_instance(ec2_instance, aws_session, aws_region, aws_account_id):

    arn = ec2_instance(aws_session, aws_region, aws_account_id)
    # arn:aws:ec2:us-east-1:803981987763:instance/i-5ef96e7063abde113
    instance_id = arn.split("/")[1]

    inventory = service.Instance(aws_region, aws_account_id, aws_session)
    inventory_list = list(inventory)

    assert len(inventory_list) == 1

    asset = inventory_list[0]

    # from pprint import pprint
    # pprint(inventory_list[0]._asdict())

    assert arn == asset.arn

    assert instance_id == asset.name
    assert 'm4.large' == asset.data['InstanceType']
    assert 'value1' == asset.tags['key1']

    inventory.set_tags(arn=arn, tags_dict={'key2': 'value2'})

    assert {'key1': 'value1', 'key2': 'value2'} == inventory.get_tags(arn)

    inventory.unset_tags(arn, ['key1'])

    assert {'key2': 'value2'} == inventory.get_tags(arn)

"""
{'arn': 'arn:aws:ec2:us-east-1:803981987763:instance/i-9ed196b846d498a4d',
 'data': {'AmiLaunchIndex': 0,
          'Architecture': 'x86_64',
          'BlockDeviceMappings': [{'DeviceName': '/dev/sda1',
                                   'Ebs': {'AttachTime': datetime.datetime(2020, 5, 7, 1, 19, 10, tzinfo=tzutc()),
                                           'DeleteOnTermination': False,
                                           'Status': 'in-use',
                                           'VolumeId': 'vol-faef321e'}}],
          'ClientToken': 'ABCDE1234567890123',
          'EbsOptimized': False,
          'Hypervisor': 'xen',
          'ImageId': 'None',
          'InstanceId': 'i-9ed196b846d498a4d',
          'InstanceType': 'm4.large',
          'KernelId': 'None',
          'KeyName': 'None',
          'LaunchTime': datetime.datetime(2020, 5, 7, 1, 19, 10, tzinfo=tzutc()),
          'Monitoring': {'State': 'disabled'},
          'NetworkInterfaces': [{'Association': {'IpOwnerId': '123456789012',
                                                 'PublicIp': '54.214.100.85'},
                                 'Attachment': {'AttachTime': datetime.datetime(2015, 1, 1, 0, 0, tzinfo=tzutc()),
                                                'AttachmentId': 'eni-attach-4f3ab01d',
                                                'DeleteOnTermination': True,
                                                'DeviceIndex': 0,
                                                'Status': 'attached'},
                                 'Description': 'Primary network interface',
                                 'Groups': [],
                                 'MacAddress': '1b:2b:3c:4d:5e:6f',
                                 'NetworkInterfaceId': 'eni-e498c49a',
                                 'OwnerId': '123456789012',
                                 'PrivateIpAddress': '10.232.95.200',
                                 'PrivateIpAddresses': [{'Association': {'IpOwnerId': '123456789012',
                                                                         'PublicIp': '54.214.100.85'},
                                                         'Primary': True,
                                                         'PrivateIpAddress': '10.232.95.200'}],
                                 'SourceDestCheck': True,
                                 'Status': 'in-use',
                                 'SubnetId': 'subnet-75be6811',
                                 'VpcId': 'vpc-f29e3c31'}],
          'Placement': {'AvailabilityZone': 'us-east-1a',
                        'GroupName': '',
                        'Tenancy': 'default'},
          'PrivateDnsName': 'ip-10-232-95-200.ec2.internal',
          'PrivateIpAddress': '10.232.95.200',
          'ProductCodes': [],
          'PublicDnsName': 'ec2-54-214-100-85.compute-1.amazonaws.com',
          'PublicIpAddress': '54.214.100.85',
          'RootDeviceName': '/dev/sda1',
          'RootDeviceType': 'ebs',
          'SecurityGroups': [],
          'SourceDestCheck': True,
          'State': {'Code': 16, 'Name': 'running'},
          'StateReason': {'Code': '', 'Message': ''},
          'StateTransitionReason': '',
          'SubnetId': 'subnet-75be6811',
          'Tags': [{'Key': 'key1', 'Value': 'value1'}],
          'VirtualizationType': 'paravirtual',
          'VpcId': 'vpc-f29e3c31'},
 'name': 'i-9ed196b846d498a4d',
 'tags': {'key1': 'value1'}}
"""