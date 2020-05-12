import logging
import logging.config
import sys
from datetime import date, datetime
from decimal import Decimal


def clean(value):
    """DynamoDB does not support empty string, Float.
    And Datetime is not JSON serializable.
    This recursive function cleans the data."""
    if isinstance(value, dict):
        return dict((k, clean(v)) for k, v in value.items())
    elif isinstance(value, list):
        return list(clean(v) for v in value)
    elif isinstance(value, tuple):
        return tuple(list(clean(v) for v in value))
    elif isinstance(value, str) and value == '':
        return None
    elif isinstance(value, (datetime, date)):
        return value.isoformat()
    elif isinstance(value, float):
        return Decimal(str(value))
    return value

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



def configure_logging(debug=False, stdout_enable=True, level="INFO"):

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'debug': {
                'format': 'line:%(lineno)d - %(asctime)s %(name)s: [%(levelname)s] - [%(process)d] - [%(module)s] - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'simple': {
                'format': '[%(process)d] - %(asctime)s %(name)s: [%(levelname)s] - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'null': {
                'level': level,
                'class': 'logging.NullHandler',
            },
            'console':{
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'stream': sys.stdout
            },
        },
        'loggers': {
            '': {
                'handlers': [],
                'level': level,
                'propagate': False,
            },
            'botocore': {'level': 'WARN'},
            'boto3': {'level': 'WARN'},
            'urllib3': {'level': 'WARN'},
            'adal-python': {'level': 'WARN'},
        },
    }

    if stdout_enable:
        if 'console' not in LOGGING['loggers']['']['handlers']:
            LOGGING['loggers']['']['handlers'].append('console')

    '''if handlers is empty'''
    if not LOGGING['loggers']['']['handlers']:
        LOGGING['loggers']['']['handlers'] = ['console']

    if debug:
        LOGGING['loggers']['']['level'] = 'DEBUG'
        for handler in LOGGING['handlers'].keys():
            if handler != 'null':
                LOGGING['handlers'][handler]['formatter'] = 'debug'
                LOGGING['handlers'][handler]['level'] = 'DEBUG'

    logging.config.dictConfig(LOGGING)
    return logging.getLogger()
