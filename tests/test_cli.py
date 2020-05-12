from uuid import uuid4
import json
from mce_lib_aws.cli import run
from moto import mock_iam, mock_sts, mock_s3
from click.testing import CliRunner

@mock_iam
@mock_s3
def test_cli_run(tmpdir_factory, s3_bucket_with_tags, aws_session, aws_region, aws_account_id):

    arn_s3 = s3_bucket_with_tags(aws_session, aws_region)

    output_file = tmpdir_factory.mktemp("export").join("export.json")

    cmd = f"""
    -S aws.s3.bucket
    -R {aws_region} 
    -a {aws_account_id} 
    -k testing 
    -s testing 
    --output {output_file}
    """

    runner = CliRunner()
    print(" ".join(cmd.split()))
    result = runner.invoke(run, cmd.split())
    assert not result.exception
    assert result.exit_code == 0

    with open(output_file, 'r') as fp:
        data = json.load(fp)

    del data[0]['data']['CreationDate']
    assert data == [
        {
            'arn': arn_s3,
            'account_id': aws_account_id,
            'region': aws_region,
            'service': 'aws.s3.bucket',
            'name': 'mybucket0',
            'data': {
                'Name': 'mybucket0',
                #'CreationDate': '2020-05-12T14:00:53.127747'
            },
            'tags': {
                'key1': 'value1'
            }
        }
    ]