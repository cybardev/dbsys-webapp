#!/usr/bin/env python3
# -*- coding: utf8 -*-

import argparse
from getpass import getpass

from .app import app_factory


def main(args: argparse.Namespace) -> None:
    password = (
        args.PASSWORD
        if args.PASSWORD is not None
        else getpass("Enter MySQL password: ")
    )
    app = app_factory(args.HOST, args.USER, password, args.DATABASE)
    app.run(debug=True, host="0.0.0.0", port=args.PORT)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Group project for CSCI-3461, made by Group 13",
        allow_abbrev=False,
    )
    parser.add_argument(
        "-s",
        "--server",
        dest="HOST",
        type=str,
        default="localhost",
        help="server to host webapp on",
    )
    parser.add_argument(
        "-n",
        "--port",
        dest="PORT",
        type=int,
        default=42818,
        help="port to serve webapp on",
    )
    parser.add_argument(
        "-d",
        "--database",
        dest="DATABASE",
        type=str,
        help="database to use for webapp",
        required=True,
    )
    parser.add_argument(
        "-u",
        "--user",
        dest="USER",
        type=str,
        help="database to use for webapp",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--password",
        dest="PASSWORD",
        type=str,
        help="database to use for webapp",
        default=None,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    main(args)
