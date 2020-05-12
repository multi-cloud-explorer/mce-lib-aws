import boto3

DEFAULT_ACCOUNT_ID = "123456789001"

def setup_networking(session=None, region=None, account_id=None, **kwargs):

    if session:
        resource = session.resource('ec2', region_name=region, **kwargs)
    else:
        resource = boto3.resource('ec2', region_name=region, **kwargs)

    vpc = resource.create_vpc(CidrBlock="10.11.0.0/16")

    subnet1 = resource.create_subnet(
        VpcId=vpc.id, CidrBlock="10.11.1.0/24", AvailabilityZone="us-east-1a"
    )
    subnet2 = resource.create_subnet(
        VpcId=vpc.id, CidrBlock="10.11.2.0/24", AvailabilityZone="us-east-1b"
    )
    return {"vpc": vpc.id, "subnet1": subnet1.id, "subnet2": subnet2.id}


def acm_certificate(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('acm', region_name=region, **kwargs)
    else:
        client = boto3.client('acm', region_name=region, **kwargs)

    response = client.request_certificate(
        DomainName='example.com',
        SubjectAlternativeNames=[
            'www.example.com'
        ]
    )

    client.add_tags_to_certificate(
        CertificateArn=response['CertificateArn'],
        Tags=[
            {
                'Key': 'key1',
                'Value': 'value1'
            }
        ]
    )

    return response['CertificateArn']


def apigateway_restapi(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('apigateway', region_name=region, **kwargs)
    else:
        client = boto3.client('apigateway', region_name=region, **kwargs)

    response = client.create_rest_api(
        name='myapi',
        description='My Test API'
    )

    restapi_id = response['id']

    return 'arn:aws:apigateway:{}::/restapis/{}'.format(region, restapi_id)


def auto_scaling_group(session=None, region=None, account_id=DEFAULT_ACCOUNT_ID, endpoint_url=None, networking=None, **kwargs):

    if not networking:
        networking = setup_networking(session=session, region=region, endpoint_url=endpoint_url)

    if session:
        client = session.client('autoscaling', region_name=region, endpoint_url=endpoint_url, **kwargs)
    else:
        client = boto3.client('autoscaling', region_name=region, endpoint_url=endpoint_url, **kwargs)

    response = client.create_launch_configuration(
        IamInstanceProfile='my-iam-role',
        ImageId='ami-12345678',
        InstanceType='m3.medium',
        LaunchConfigurationName='my-launch-config',
        SecurityGroups=[
            'sg-eb2af88e'
        ]
    )

    response = client.create_auto_scaling_group(
        AutoScalingGroupName='my-auto-scaling-group',
        LaunchConfigurationName='my-launch-config',
        MaxSize=3,
        MinSize=1,
        VPCZoneIdentifier=networking["subnet1"],
    )

    client.create_or_update_tags(
        Tags=[
            {
                'ResourceId': 'my-auto-scaling-group',
                'ResourceType': 'auto-scaling-group',
                'Key': 'key1',
                'Value': 'value1',
                'PropagateAtLaunch': False
            }
        ]
    )

    return f'arn:aws:autoscaling:{region}:{account_id}:autoScalingGroup:ca861182-c8f9-4ca7-b1eb-cd35505f5ebb:autoScalingGroupName/my-auto-scaling-group'


def cloud_formation_stack(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('cloudformation', region_name=region, **kwargs)
    else:
        client = boto3.client('cloudformation', region_name=region, **kwargs)

    response = client.create_stack(
        StackName='my-stack',
        TemplateBody='{"Resources": {}}',
        NotificationARNs=['arn:aws:sns:region:account-id:topicname'],
        Parameters=[
            {
                'ParameterKey': 'testKey',
                'ParameterValue': 'testValue'
            }
        ],
        Tags=[
            {
                'Key': 'key1',
                'Value': 'value1'
            }
        ]
    )

    return response['StackId']


def dynamodb_table(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('dynamodb', region_name=region, **kwargs)
    else:
        client = boto3.client('dynamodb', region_name=region, **kwargs)

    response = client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'my-key',
                'AttributeType': 'S'
            }
        ],
        TableName='my-table',
        KeySchema=[
            {
                'AttributeName': 'my-key',
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    arn = f'arn:aws:dynamodb:{region}:{account_id}:table/my-table'

    client.tag_resource(
        ResourceArn=arn,
        Tags=[
            {
                'Key': 'key1',
                'Value': 'value1'
            }
        ]
    )

    return arn


def ec2_instance(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('ec2', region_name=region, **kwargs)
    else:
        client = boto3.client('ec2', region_name=region, **kwargs)

    response = client.run_instances(
        MinCount=1,
        MaxCount=1,
        InstanceType='m4.large'
    )

    instance_id = response['Instances'][0]['InstanceId']

    arn = f'arn:aws:ec2:{region}:{account_id}:instance/{instance_id}'

    client.create_tags(
        Resources=[
            instance_id,
        ],
        Tags=[
            {
                'Key': 'key1',
                'Value': 'value1'
            }
        ]
    )
    return arn


def ecs_cluster(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('ecs', region_name=region, **kwargs)
    else:
        client = boto3.client('ecs', region_name=region, **kwargs)

    response = client.create_cluster(
        clusterName='myCluster',
        tags=[
            {
                'key': 'key1',
                'value': 'value1'
            }
        ]
    )

    return response['cluster']['clusterArn']


def elb_load_balancer(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('elb', region_name=region, **kwargs)
    else:
        client = boto3.client('elb', region_name=region, **kwargs)

    response = client.create_load_balancer(
        LoadBalancerName='my-loadbalancer',
        Listeners=[
            {
                'Protocol': 'HTTP',
                'LoadBalancerPort': 80,
                'InstanceProtocol': 'HTTP',
                'InstancePort': 80
            },
        ],
        Tags=[
            {
                'Key': 'key1',
                'Value': 'value1'
            }
        ]
    )

    return f"arn:aws:elasticloadbalancing:{region}:{account_id}:loadbalancer/my-loadbalancer"


def elbv2_load_balancer(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('elbv2', region_name=region, **kwargs)
        ec2_client = session.client('ec2', region_name=region, **kwargs)
    else:
        client = boto3.client('elbv2', region_name=region, **kwargs)
        ec2_client = boto3.client('ec2', region_name=region, **kwargs)

    response = ec2_client.describe_subnets()
    subnet_id = response['Subnets'][0]['SubnetId']

    response = client.create_load_balancer(
        Name='my-loadbalancer',
        Subnets=[
            subnet_id
        ],
        Scheme='internal',
        Tags=[
            {
                'Key': 'key1',
                'Value': 'value1'
            }
        ]
    )

    return response['LoadBalancers'][0]['LoadBalancerArn']


def opsworks_stack(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('opsworks', region_name=region, **kwargs)
    else:
        client = boto3.client('opsworks', region_name=region, **kwargs)

    response = client.create_stack(
        Name='my-stack',
        Region=region,
        ServiceRoleArn=f'arn:aws:iam::{account_id}:role/aws-opsworks-service-role',
        DefaultInstanceProfileArn=f'arn:aws:iam::{account_id}:instance-profile/aws-opsworks-ec2-role',
    )

    stack_id = response['StackId']

    return f'arn:aws:opsworks:{region}:{account_id}:stack/{stack_id}'


def rds_db_instance(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('rds', region_name=region, **kwargs)
    else:
        client = boto3.client('rds', region_name=region, **kwargs)

    response = client.create_db_instance(
        AllocatedStorage=5,
        DBName='mydb',
        DBInstanceIdentifier='mydbinstance',
        DBInstanceClass='db.t2.micro',
        Engine='mysql',
        MasterUserPassword='MyPassword',
        MasterUsername='MyUser',
        Tags=[
            {
                'Key': 'key1',
                'Value': 'value1'
            }
        ]
    )

    return f'arn:aws:rds:{region}:{account_id}:instance:mydbinstance'


def redshift_cluster(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('redshift', region_name=region, **kwargs)
    else:
        client = boto3.client('redshift', region_name=region, **kwargs)

    response = client.create_cluster(
        ClusterIdentifier='mycluster',
        NodeType='ds2.xlarge',
        MasterUsername='myuser',
        MasterUserPassword='mypass',
        DBName='mycluster',
        Tags=[
            {
                'Key': 'key1',
                'Value': 'value1'
            }
        ]
    )

    return f'arn:aws:redshift:{region}:{account_id}:cluster:mycluster'


def s3_bucket_with_tags(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('s3', region_name=region, **kwargs)
    else:
        client = boto3.client('s3', region_name=region, **kwargs)

    client.create_bucket(
        ACL='public-read',
        Bucket='mybucket0',
    )

    client.put_bucket_tagging(
        Bucket='mybucket0',
        Tagging={
            'TagSet': [
                {
                    'Key': 'key1',
                    'Value': 'value1'
                }
            ]
        }
    )

    # client = boto3.client('s3', region_name='eu-west-1')
    # client.create_bucket(
    #     ACL='public-read',
    #     Bucket='mybucket1',
    #     CreateBucketConfiguration={
    #         'LocationConstraint': 'EU'
    #     }
    # )

    #self.arn0 = 'arn:aws:s3:::mybucket0'
    #self.arn1 = 'arn:aws:s3:::mybucket1'
    return 'arn:aws:s3:::mybucket0'


def sns_topic(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('sns', region_name=region, **kwargs)
    else:
        client = boto3.client('sns', region_name=region, **kwargs)

    response = client.create_topic(
        Name='mytopic'
    )

    return response['TopicArn']


def sqs_queue(session=None, region=None, account_id=None, **kwargs):

    if session:
        client = session.client('sqs', region_name=region, **kwargs)
    else:
        client = boto3.client('sqs', region_name=region, **kwargs)

    client.create_queue(
        QueueName='myqueue',
        Attributes={
            'string': 'string'
        }
    )

    client.tag_queue(
        QueueUrl=f'https://sqs.us-east-1.amazonaws.com/{account_id}/myqueue',
        Tags={
            'key1': 'value1'
        }
    )

    return f'arn:aws:sqs:{region}:{account_id}:myqueue'

