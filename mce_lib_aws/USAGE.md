# AWS Abstract

An abstract module for AWS resource management in a consistent way.

## How it works

This module will open a session on a remote given `account_id` over STS with its `delegation_role_name`.

All the founded resources matching `resources_allowed` and `regions_allowed` are returned.

## Interactive test

Run the following code interactively or in a script.

```python
from mce_lib_aws.crawler import get_cloud_assets

cloud_assets = get_cloud_assets(account_id='0000000000',
                                delegation_role_name='YourRole',
                                resources_allowed=['aws.acm.certificate'],
                                regions_allowed=['aws-global', 'eu-west-1'])


for resource_name, region, asset in cloud_assets:
    print(resource_name, region)
    print(asset)
```

## Unit test

```bash
pip install -e .[tests]
pytest 
```
