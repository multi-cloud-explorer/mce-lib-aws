import logging
from collections import namedtuple

from boto3.session import Session as BotoSession
from botocore.client import BaseClient

logger = logging.getLogger(__name__)

Asset = namedtuple('Asset', ('arn', 'data', 'tags', 'name'))


def tags_to_dict(tags_list, nk='Key', nv='Value'):
    """
    Maps a list of dicts to a flat dict.
    From :
        [
          {'Key': 'tag1', 'Value': 'value1'},
          {'Key': 'tag2', 'Value': 'value2'},
          ...
        ]
    To :
        {
            'tag1': 'value1',
            'tag2': 'value2',
            ...
        }

    If defined, addon is an additionnal dict to extend each items
    """

    tags_dict = dict((i[nk], i[nv]) for i in tags_list)
    return tags_dict


def tags_to_list(tags_dict, nk='Key', nv='Value', addon=None):
    """
    Maps a flat dict to a list of dicts.
    From :
        {
            'tag1': 'value1',
            'tag2': 'value2',
            ...
        }
    To :
        [
          {'Key': 'tag1', 'Value': 'value1'},
          {'Key': 'tag2', 'Value': 'value2'},
          ...
        ]

    If defined, addon is an additionnal dict to extend each items
    """

    if addon:
        tags_list = list(dict(**{nk: k, nv: v}, **addon)
                         for k, v in tags_dict.items())
    else:
        tags_list = list(dict(**{nk: k, nv: v}) for k, v in tags_dict.items())
    return tags_list


class AWSResource:

    boto_service_name = None
    arn_pattern = None

    def __init__(self, region: str, account: str, session: BotoSession, client: BaseClient = None, endpoint_url: str = None):
        self.region = region
        self.account = account
        self.client = client

        if not self.client:
            self.client = session.client(
                self.boto_service_name, region_name=region, endpoint_url=endpoint_url
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

            yield Asset(arn, data, tags, name)

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
