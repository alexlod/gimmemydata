#!/usr/bin/env python3

from .config import Config
from datetime import datetime
import asyncio
import time
import argparse
import re
import logging
import shutil, os
import sys
from .datasources.obsidian.analyzevault import AnalyzeVault

def enableDebugMode():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.debug("Debug mode enabled.")

def runObsidianAnalyze():
    
    vault_dir = Config().get_param('OBSIDIAN_VAULT_DIR')

    av = AnalyzeVault(vault_dir)
    av.analyze_to_db()


def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    exclusive_group = parser.add_mutually_exclusive_group(required=False)
    exclusive_group.add_argument('--configure', action='store_true', help="Configure the CLI and create or update config yaml file.")
    parser.add_argument('--obsidian', action="store_true", help="Analyze Obsidian vault & return data.")
    parser.add_argument('--debug', action="store_true", help="Enable debug mode.")
    args = parser.parse_args().__dict__

    if args.get('debug'):
        enableDebugMode()

    if args.get('configure'):
        Config().configure()
        sys.exit(1)
    else:
        Config().get_config()

    if args.get('obsidian'):
        runObsidianAnalyze()
    else:
        parser.print_help()


