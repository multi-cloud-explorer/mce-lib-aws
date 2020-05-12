#!/usr/bin/env python3

import time
import logging
from pprint import pprint as pp
import sys
import json

import click
import boto3
from decouple import config

from mce_lib_aws import SERVICES
from mce_lib_aws.utils import configure_logging
from mce_lib_aws.crawler import get_selected_regions_and_services, get_asset_by_region

logger = logging.getLogger(__name__)

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default=None)
AWS_DEFAULT_REGION = config('AWS_DEFAULT_REGION', default='eu-west-3')

# TODO: delegation_role_name

opt_services = click.option(
    '--services', '-S',
    required=False,
    multiple=True,
    type=click.Choice(list(SERVICES.keys())),
    help='Multiple services filter'
)

opt_regions = click.option(
    '--regions', '-R',
    required=False,
    multiple=True,
    help='Multiple regions filter'
)

opt_account_id = click.option(
    '--account-id', '-a',
    required=True,
    help='Subscription ID'
)

opt_access_key_id = click.option(
    '--access-key-id', '-k',
    required=True,
    show_default=True,
    default=AWS_ACCESS_KEY_ID,
    help='AWS Access Key ID'
)

opt_access_secret_key = click.option(
    '--secret-access-key', '-s',
    required=True,
    show_default=True,
    default=AWS_SECRET_ACCESS_KEY,
    help='AWS Secret Key'
)

opt_default_region = click.option(
    '--default-region', '-r',
    required=True,
    show_default=True,
    default=AWS_DEFAULT_REGION,
    help='AWS Default Region'
)

opt_debug = click.option('--debug', '-D', is_flag=True)

opt_quiet = click.option('--quiet', is_flag=True)

opt_verbose = click.option('-v', '--verbose',
                           is_flag=True,
                           help='Enables verbose mode.')

opt_logger = click.option('--log-level', '-l',
                          required=False,
                          type=click.Choice(['DEBUG', 'WARN', 'ERROR', 'INFO','CRITICAL']),
                          default='INFO',
                          show_default=True,
                          help='Logging level')

opt_logger_file = click.option('--log-file',
                               type=click.Path(exists=False),
                               help='File for output logs')

opt_output_file = click.option('--output',
                               type=click.Path(exists=False),
                               help='File for output json data')

class Context(object):
    def __init__(self,
                 verbose=False,
                 log_level='ERROR', log_file=None,
                 debug=False, silent=False, pretty=False, quiet=False,
                 output=None,
                 account_id=None, default_region=None,
                 access_key_id=None, secret_access_key=None):

        self.output = output

        self.account_id = account_id
        self.default_region = default_region
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

        self.verbose = verbose
        self.debug = debug
        self.silent = silent
        self.pretty = pretty
        self.quiet = quiet

        self.log_level = log_level
        self.log_file = log_file

        if self.verbose and log_level != "DEBUG":
            self.log_level = 'INFO'

        self.logger = configure_logging(debug=self.debug,
                                        level=self.log_level)

        if self.log_file:
            self._set_log_file()

    def _set_log_file(self):
        from logging import FileHandler
        handler = FileHandler(filename=self.log_file)
        if self.logger.hasHandlers():
            handler.setFormatter(self.logger.handlers[0].formatter)
        self.logger.addHandler(handler)

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        if self.quiet:
            self.logger.info(msg)
            return
        click.echo(msg, file=sys.stderr)

    def log_error(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        if self.quiet:
            self.logger.error(msg)
            return
        click.echo(click.style(msg, fg='red'), file=sys.stderr)

    def log_ok(self, msg, *args):
        """Logs a message to stdout."""
        if args:
            msg %= args
        if self.quiet:
            self.logger.info(msg)
            return
        click.echo(click.style(msg, fg='green'), file=sys.stdout)

    def log_warn(self, msg, *args):
        """Logs a message to stdout."""
        if args:
            msg %= args
        if self.quiet:
            self.logger.warn(msg)
            return
        click.echo(click.style(msg, fg='yellow'), file=sys.stdout)

    def pretty_print(self, obj):
        pp(obj)

    def write_ouput(self, obj):
        with open(self.output, 'w') as fp:
            json.dump(obj, fp)

@click.group()
@click.version_option(prog_name="mce-aws")
def cli():
    pass

@cli.command('run')
@opt_services
@opt_regions
@opt_account_id
@opt_access_key_id
@opt_access_secret_key
@opt_default_region
@opt_output_file
@opt_verbose
@opt_debug
@opt_logger
@opt_logger_file
def run(services=None, regions=None, **kwargs):
    """"""

    ctx = Context(**kwargs)

    region_groups = get_selected_regions_and_services(
        resources_allowed=services,
        regions_allowed=regions
    )

    session = boto3.Session(
        aws_access_key_id=ctx.access_key_id,
        aws_secret_access_key=ctx.secret_access_key,
        region_name=ctx.default_region)

    results = []
    errors = []
    start = time.time()

    for region, services in region_groups.items():
        for service in services:
            # print(region, service)
            try:
                for asset in get_asset_by_region(session, ctx.account_id, region, service):
                    results.append((region, service, dict(asset._asdict())))
            except Exception as err:
                msg = f"region[{region}] - service[{service}] - error: {str(err)}"
                logger.error(msg)
                errors.append(msg)

    if ctx.output:
        with open(ctx.output, 'w') as fp:
            json.dump([r[2] for r in results], fp, indent=2)
    else:
        for region, service, asset in results:
            ctx.pretty_print(asset)

    if errors:
        print("--------------------- ERRORS ---------------------")
        for error in errors:
            print(error)
        print("--------------------------------------------------")

    duration = time.time() - start
    print("duration : %.2f seconds" % duration)

def main():
    cli()


if __name__ == "__main__":
    main()
