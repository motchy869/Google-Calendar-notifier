"""
マネージャクラス
"""
import argparse
import datetime
import os
import sys
from time import sleep

from modules.Global import (logger, APPLICATION_NAME)
from modules.Notif import Notif

import httplib2
import requests

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

class Manager:
	"""
	マネージャクラス
	"""

	def __init__(self):
		self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
		self.CLIENT_SECRET_FILE = 'client_secret.json'
		self.notifs = []	#Notif インスタンスのリスト

		#認証情報を取得
		self.wait_server_connection()
		self.credentials = self.get_credentials()

	def get_credentials(self):
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
			flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
			flow.user_agent = APPLICATION_NAME
			credentials = tools.run_flow(flow, store, flags)
			print('Storing credentials to ' + credential_path)
		return credentials

	@staticmethod
	def wait_server_connection():
		"""
		http://accounts.google.com に接続できるようになるまで待機する
		"""
		while True:
			try:
				resp = requests.get("http://accounts.google.com")
				if resp.status_code == 200:
					break
			except Exception:
				logger.debug("Waiting server connection.")
				sleep(5)

	def update_notifs(self):
		"""
		サーバーより通知を更新する
		"""
		pass
