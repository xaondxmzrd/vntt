import os
import sys
import argparse
import gui
import extract

__version__ = "0.0.1"
__program__ = "vntt"


def is_file_or_dir(path):
    if os.path.isfile(path) or os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"No such file or directory: {path}")


def startup_parser():
    parser = argparse.ArgumentParser(description="simple visual novel translation tool")
    parser.add_argument("-v", "--version", action="store_true")
    startup_subparsers(parser)

    return parser


def process_args(args):
    if args.version:
        print(__program__, "version", __version__)

    if hasattr(args, "func"):
        args.func(args)


class startup_subparsers:
    def __init__(self, parser):
        self.subparsers = parser.add_subparsers(
            title="subcommands", description="choose one of the commands"
        )
        self.add_extract_parser()
        self.add_embed_parser()
        self.add_gui_parser()

    def add_extract_parser(self):
        def process_args(args):
            path = args.file
            extract.extract(path)

        parser = self.subparsers.add_parser("extract", help="extract game")
        parser.add_argument("file", help="game file or directory", type=is_file_or_dir)
        parser.set_defaults(func=process_args)

    def add_embed_parser(self):
        def process_args(args):
            pass

        parser = self.subparsers.add_parser("embed", help="embed game")

    def add_gui_parser(self):
        def process_args(args):
            app = gui.App(sys.argv)
            app.exec()

        parser = self.subparsers.add_parser("gui", help="startup gui")
        parser.set_defaults(func=process_args)


def main():
    parser = startup_parser()

    args = parser.parse_args(["extract", ""])

    process_args(args)


if __name__ == "__main__":
    main()
