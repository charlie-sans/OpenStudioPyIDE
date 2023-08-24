###########
# Imports #
###########
import os
import sys
import time
import json
import random
import logging
import argparse
import datetime
import gzip
import configparser
import pyqt6
# setup argparse

def print_version():
    print('OpenStudioPyIDE v0.1.0')
    print('Created by: OpenStudioPyIDE Team')

def print_status(func):
    def wrapper(*args, **kwargs):
        print('Running {func}...'.format(func=func.__name__))
        func(*args, **kwargs)
        print('Finished {func}...'.format(func=func.__name__))
    return wrapper
parser = argparse.ArgumentParser(description='help for OpenStudioPyIDE')
parser.add_argument('-p', '--project', help='project name, use only if running from external script')
parser.add_argument('-s', '--script', help='script name to run, use only if running from external script')
parser.add_argument('-d', '--debug', help='debug mode, use only if something went woops', action='store_true')
parser.add_argument('-v', '--version', help='prints the version', action='store_true')


args = parser.parse_args()

# setup logging
if args.log:
    logging.basicConfig(filename="OpenIDE.crsh", level=logging.DEBUG)
else:
    print('No log file specified, using default log file name')

# setup config file
try:
    
    config_file = 'config.ini'
    configparser = configparser.ConfigParser()
    configparser.read(config_file)
    background = configparser['DEFAULT']['project']
    color = configparser['DEFAULT']['project']
    theme = configparser['DEFAULT']['project']
    font = configparser['DEFAULT']['project']
    font_size = configparser['DEFAULT']['project']

except Exception as e:
    logging.error('Error: {e}'.format(e))
    print('Error: {e}'.format(e))
    sys.exit(1)
# setup project