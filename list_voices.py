#!/usr/bin/env python3
"""
List available AWS Polly voices for a specific engine.
"""

import boto3
from botocore.exceptions import BotoCoreError, ClientError
import argparse
import sys


def list_voices(engine, aws_profile=None):
    """
    List available Polly voices for the given engine.

    Args:
        engine (str): Engine type - 'neural', 'standard', or 'generative'
        aws_profile (str): AWS profile name to use (default: None)
    """
    try:
        if aws_profile:
            session = boto3.Session(profile_name=aws_profile)
            polly_client = session.client('polly')
        else:
            polly_client = boto3.client('polly')

        voices = []
        paginator = polly_client.get_paginator('describe_voices')
        for page in paginator.paginate(Engine=engine):
            voices.extend(page['Voices'])

        if not voices:
            print(f"No voices found for engine '{engine}'.")
            return

        print(f"Available voices for engine '{engine}':\n")
        print(f"{'ID':<20} {'Name':<20} {'Gender':<10} {'Language':<10} {'Language Name'}")
        print("-" * 80)
        for v in sorted(voices, key=lambda x: x['Id']):
            print(f"{v['Id']:<20} {v['Name']:<20} {v['Gender']:<10} {v['LanguageCode']:<10} {v['LanguageName']}")

    except (BotoCoreError, ClientError) as error:
        print(f"✗ Error occurred: {error}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='List available AWS Polly voices for a specific engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python list_voices.py --engine neural
  python list_voices.py --engine standard
  python list_voices.py --engine generative
  python list_voices.py -e neural --profile myprofile
        """
    )

    parser.add_argument('--engine', '-e', choices=['neural', 'standard', 'generative'], required=True,
                        help='Engine type: neural, standard, or generative')
    parser.add_argument('--profile', '-p', help='AWS profile name to use')

    args = parser.parse_args()
    list_voices(engine=args.engine, aws_profile=args.profile)


if __name__ == "__main__":
    main()
