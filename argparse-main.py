import sys
import json
import re
import argparse
import datetime
from common.Instance import Instance
from models.Issue import Issue
from models.Comment import Comment
from common.BaseCommand import BaseCommand
from common.ResultAndData import ResultAndData, Error, Success
from common.utils import enable_vt_support
from argparse import Namespace


class SampleCommand(BaseCommand):
    def add_parser(self, subparsers):
        sample = subparsers.add_parser("sample", description="The sample command")
        return sample

    def do_command_with_args(self, instance, args):
        # type: (Instance, Namespace) -> ResultAndData
        print("You've run the sample command!")
        return Success()


class OtherSampleCommand(BaseCommand):
    def add_parser(self, subparsers):
        sample = subparsers.add_parser("other", description="The other sample command")
        return sample

    def do_command_with_args(self, instance, args):
        # type: (Instance, Namespace) -> ResultAndData
        print("You've run the other command!")
        return Success()


def build_arg_parser():

    common_parser = argparse.ArgumentParser(add_help=True)
    common_parser.add_argument("-l", "--log", default=None)
    common_parser.add_argument("-v", "--verbose", default=None)

    subparsers = common_parser.add_subparsers(
        dest="command",
        title="commands",
        description="Application commands",
        help="Commands for working with this application",
    )
    sample_cmd = SampleCommand(subparsers)
    other_cmd = OtherSampleCommand(subparsers)
    return common_parser


def main(argv):

    enable_vt_support()

    parser = build_arg_parser()
    args = parser.parse_args()
    if args.command == None:
        # print('no cmd')
        # print(parser.usage)
        parser.print_help()
    elif args.func:
        instance = Instance()
        result = args.func(instance, args)
        if result is not None:
            if result.success:
                sys.exit(0)
            else:
                if result.data:
                    print("\x1b[31m")
                    print(result.data)
                    print("\x1b[m")
                sys.exit(-1)
        else:
            sys.exit(-1)

    else:
        print(
            "Programming error - The command you entered didnt supply a implementation"
        )
        print("Go add a `set_defaults(func=DO_THE_THING)` to {}".format(args.command))
    return


if __name__ == "__main__":
    main(sys.argv)
