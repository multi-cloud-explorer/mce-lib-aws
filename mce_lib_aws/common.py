import logging
from collections import namedtuple

from boto3.session import Session as BotoSession
from botocore.client import BaseClient

from .utils import tags_to_dict, tags_to_list

logger = logging.getLogger(__name__)

Asset = namedtuple('Asset', ('arn', 'data', 'tags', 'name', 'account_id', 'region', 'service'))

class AWSResource:

    boto_service_name = None
    arn_pattern = None

    def __init__(self, region: str, account: str, session: BotoSession, client: BaseClient = None, endpoint_url: str = None):
        self.region = region
        self.account = account
        self.client = client

        if not self.client:
            self.client = session.client(
                self.boto_service_name,
                region_name=region,
                endpoint_url=endpoint_url
            )

    def __iter__(self):
        for elem in self._listall():
            arn = self._parse_arn(elem)
            data = self._parse_data(elem)
            tags = self._parse_tags(elem, data)
            name = self._parse_name(elem, data, tags)

            # TODO: ???
            if isinstance(elem, (str, list)):
                elem = {}

            if not isinstance(data, dict):
                logger.error('data should be a dict, not a %s.', type(data))
                data = {}

            data = dict(elem, **data)

            yield Asset(
                arn=arn,
                data=data,
                tags=tags,
                name=name,
                account_id=self.account,
                region=self.region,
                service=None)


    def _listall(self):
        """Enumerates all assets with a one API call, an returns a list"""
        return []

    def _parse_arn(self, elem):
        """Returns the ARN (string) from the given values in the dict `elem`"""
        if self.arn_pattern:
            return self.arn_pattern.format(
                region=self.region,
                account=self.account,
                elem=elem
            )
        return ''

    def _parse_data(self, elem):
        """Returns the asset data, this could require additionnal API calls."""
        return elem

    def _parse_tags(self, elem, data):
        """Returns the asset tags, this could require additionnal API calls."""
        tags_dict = tags_to_dict(elem.get('Tags', []))
        return tags_dict

    def _parse_name(self, elem, data, tags):
        return '<Undefined>'

    def get_data(self, arn):
        return {}

    def get_tags(self, arn):
        return {}

    def set_tags(self, arn, tags_dict):
        return None

    def unset_tags(self, arn, keys):
        return None
