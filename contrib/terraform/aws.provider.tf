provider "aws" {

  version                     = "~> 2.60"

  region                      = var.region

  #profile                    = var.credentials_profile
  #shared_credentials_file    = var.credentials_file
  access_key                  = var.credentials_access_key
  secret_key                  = var.credentials_secret_key

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_force_path_style         = true

  #assume_role {
  #  role_arn = "arn of the role"
  #}

  #DynamoDB Streams at http://localhost:4570
  #EventBridge (CloudWatch Events) at http://localhost:4587
  #KMS at http://localhost:4599

  endpoints {
    acm            = var.localstack_global_url
    apigateway     = var.localstack_global_url
    cloudformation = var.localstack_global_url
    cloudwatch     = var.localstack_global_url
    dynamodb       = var.localstack_global_url
    ec2            = var.localstack_global_url
    es             = var.localstack_global_url
    firehose       = var.localstack_global_url
    iam            = var.localstack_global_url
    kinesis        = var.localstack_global_url
    lambda         = var.localstack_global_url
    route53        = var.localstack_global_url
    redshift       = var.localstack_global_url
    s3             = var.localstack_global_url
    s3control      = var.localstack_global_url
    secretsmanager = var.localstack_global_url
    ses            = var.localstack_global_url
    sns            = var.localstack_global_url
    sqs            = var.localstack_global_url
    ssm            = var.localstack_global_url
    stepfunctions  = var.localstack_global_url
    sts            = var.localstack_global_url
  }

}	

