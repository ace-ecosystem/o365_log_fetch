from uuid import uuid4
import argparse

import logging
import os

from o365_api.argparsing import add_arg_parser_args
from o365_api.handler import O365ManagementApi
from o365_api.logger import setup_logger
from o365_api.wrappers import ParserWrapper


if __name__ == '__main__':

    run_id = uuid4()
    try:
        # Get configuration
        config_file = os.environ.get('O365_MANAGEMENT_API_CONFIG')
        setup_logger()
        config_parser = ParserWrapper(config_file)

        # Interact with arguments
        arg_parser = argparse.ArgumentParser()
        add_arg_parser_args(arg_parser)
        args = arg_parser.parse_args()

        if args.start_time and args.end_time:
            start = args.start_time
            end = args.end_time
        else:
            start = None
            end = None

        api = O365ManagementApi(config_parser, start, end, run_id)

        for content_type in api.content_types:
            print("Getting {}".format(content_type))
            api.retrieve_logs(content_type=content_type)
            
    except Exception as e:
        # If an exception gets up here, it's serious. Log it and then
        # let it bubble up like normal.
        logging.exception("JobId={0} {1}".format(run_id, e))
        raise

    exit()