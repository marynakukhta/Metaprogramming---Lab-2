from argparse import ArgumentParser

from .analyzer import *


class CommandArgs:
    def __init__(self, args):
        if args.project_path is not None:
            self.type = "project"
            self.path = args.project_path
        elif args.file_path is not None:
            self.type = "file"
            self.path = args.file_path
        elif args.directory_path is not None:
            self.type = "directory"
            self.path = args.directory_path


def create_parser():
    parser = ArgumentParser(add_help=True)
    subparsers = parser.add_subparsers(dest='command')
    # create the parser for verify
    verify_parser = subparsers.add_parser('verify', help='verify if code conventions are satisfied')
    verify_group = verify_parser.add_mutually_exclusive_group(required=True)
    verify_group.add_argument('-p', '--project', action='store', help='path for project to verify',
                              dest='project_path')
    verify_group.add_argument('-d', '--directory', action='store', help='directory path to verify',
                              dest='directory_path')
    verify_group.add_argument('-f', '--file', action='store', help='file path to verify', dest='file_path')

    # create the parser for fix
    fix_parser = subparsers.add_parser('fix', help='fix some code conventions. Output to a new file')
    fix_group = fix_parser.add_mutually_exclusive_group(required=True)
    fix_group.add_argument('-p', '--project', action='store', help='path for project to fix',
                           dest='project_path')
    fix_group.add_argument('-d', '--directory', action='store', help='directory path to fix',
                           dest='directory_path')
    fix_group.add_argument('-f', '--file', action='store', help='file path to fix', dest='file_path')

    return parser


def process_arguments(parser):
    args = parser.parse_args()
    command_args = CommandArgs(args)
    if args.command == 'verify':
        return VerifyAnalyzer(command_args.type, command_args.path)
    elif args.command == 'fix':
        return FixAnalyzer(command_args.type, command_args.path)


def parse_command():
    parser = create_parser()
    return process_arguments(parser)
