"""
コアスクリプト
"""

import datetime
import os
import sys
from time import sleep

from modules.Global import *
from modules.Reminder import Reminder
from modules.ReReminder import ReReminder
from modules.NotifyWindow import NotifyWindow

import httplib2
import requests

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def get_credentials():
	"""
	Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 'Google-Calendar-notifier.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		credentials = tools.run_flow(flow, store, flags)
		print('Storing credentials to ' + credential_path)
	return credentials

def wait_server_connection(self):
	"""
	http://accounts.google.com に接続できるようになるまで待機する
	"""
	while True:
		try:
			resp = requests.get("http://accounts.google.com")
			if resp.status_code == 200:
				break
		except Exception:
			self.logger.debug("Waiting server connection.")
			sleep(5)

def boot():
	"""
	起動処理
	"""
	pass

def update_reminders():
	"""
	サーバーよりリマインダを更新する
	"""
	pass
