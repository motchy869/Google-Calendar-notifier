#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google-Calendar-notifier

Google Calendar から直近の予定を取得し、通知時刻になったらデスクトップに通知を表示する。
"""

import argparse
import datetime
import logging
import os
import sys

import modules.Reminder
import modules.ReReminder
import modules.RemindWindow

from PyQt5.QtWidgets import (QApplication, QWidget)

import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

#logging の設定
logger = logging.getLogger(__name__); logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler(); streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s: %(message)s'))
logger.addHandler(streamHandler)

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar notifier'

def get_credentials():
	"""
	Gets valid user credentials from storage.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		credentials = tools.run_flow(flow, store, flags)
		print('Storing credentials to ' + credential_path)
	return credentials

def main():
	"""
	main function
	"""
	app = QApplication(sys.argv)
	w = QWidget()
	w.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
    main()
