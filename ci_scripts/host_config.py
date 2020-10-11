#!/usr/bin/env python

import argparse
import os
from textwrap import dedent


def get_args():
    parser = argparse.ArgumentParser(description='Build ssh config file.')
    parser.add_argument('deploy_host',
                        help='Hostname or IP of deploy host')
    parser.add_argument('--user',
                        default='ubuntu',
                        help='User on deploy host')
    parser.add_argument('--dest',
                        default='~/.ssh/config',
                        help='Default destination')

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    config = os.path.expanduser(args.dest)
    dest_dir = os.path.dirname(config)

    os.makedirs(os.path.expanduser(dest_dir), exist_ok=True)
    with open(config, 'w') as fp:
        fp.write(dedent(f"""
        Host *
            StrictHostKeyChecking no
            
        Host deploy_host
            Hostname {args.deploy_host}
            User {args.user}
            StrictHostKeyChecking no
            ConnectTimeout 5
            ConnectionAttempts 20

        """))


if __name__ == "__main__":
    main()
