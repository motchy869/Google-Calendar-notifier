"""
グローバル変数
"""

import argparse
import logging

from oauth2client import tools

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar notifier'

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

#logging の設定
logger = logging.getLogger(__name__); logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler(); streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s: %(message)s'))
logger.addHandler(streamHandler)
