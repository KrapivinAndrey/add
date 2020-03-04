import argparse
import sys

from .platform import main as platform_main


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_argument("product", choices=["platform"])
    args = parser.parse_args(sys.argv[1:2])
    del sys.argv[1]
    if args.product == "platform":
        platform_main()
