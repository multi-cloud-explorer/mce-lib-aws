import json
import datetime
import boto3
from decouple import config
from mce_lib_aws.crawler import get_all_assets

# account_id = '123456789'
# regions_allowed = ['eu-west-3', 'aws-global']
# resources_allowed = ['aws.s3.bucket', 'aws.ec2.instance']
# session = boto3.Session(aws_access_key_id="testing", aws_secret_access_key="testing", region_name="us-east-1")
# for asset in get_all_assets(session, account_id, resources_allowed=resources_allowed, regions_allowed=regions_allowed):
#     print(asset)
#
# def endpoint(event, context):
#     current_time = datetime.datetime.now().time()
#     body = {
#         "message": "Hello, the current time is " + str(current_time)
#     }
#
#     response = {
#         "statusCode": 200,
#         "body": json.dumps(body)
#     }
#
#     return response