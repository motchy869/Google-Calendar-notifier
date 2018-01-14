"""
マネージャクラス
"""

import argparse
from datetime import (datetime, timedelta)
import os
import sys
import threading
import time

from modules.Global import (logger, APPLICATION_NAME)
from modules.Notif import Notif

from dateutil import parser
import httplib2
from pytz import timezone
import requests

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

class Manager(threading.Thread):
	"""
	マネージャクラス
	"""

	def __init__(self):
		super(Manager, self).__init__()
		self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
		self.CLIENT_SECRET_FILE = 'client_secret.json'
		self.credentials = None
		self.service = None
		self.notifs = []	#Notif インスタンスのリスト

	def run(self):
		logger.debug("Manager started.")

		#認証情報, APIサービスを取得
		self.wait_server_connection()
		self.credentials = self.get_credentials()
		http = self.credentials.authorize(httplib2.Http())
		self.service = discovery.build('calendar', 'v3', http=http)

		#10分おきに通知を更新
		while True:
			self.update_notifs()
			time.sleep(600)

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
		http://accounts.google.com に接続できるまで待機する
		"""
		while True:
			try:
				resp = requests.get("http://accounts.google.com")
				if resp.status_code == 200:
					break
			except Exception:
				logger.debug("Waiting server connection. Retrying in 5 seconds.")
				time.sleep(5)

	def update_notifs(self):
		"""
		サーバーより通知を更新する
		"""
		logger.debug("update_notifs")
		self.wait_server_connection()

		#カレンダーリストを取得(「Contacts, 日本の祝日」を除く最大3)
		try:
			calendars = self.service.calendarList().list(#pylint: disable=E1101
				maxResults=3+2, minAccessRole='reader', showHidden='true'
			).execute().get('items', [])
		except Exception:
			return

		#各カレンダーから直近最大3個の通知を取得
		notifs_latest = []	#[('summary', notif_time_jst), ...]
		now_jst = datetime.now(timezone('Asia/Tokyo'))
		for calendar in calendars:
			if calendar['summary'] == '日本の祝日' or calendar['summary'] == 'Contacts':
				continue
			try:
				events = self.service.events().list(#pylint: disable=E1101
					calendarId=calendar['id'], timeMin=now_jst.isoformat(),
					maxResults=3, singleEvents=True, orderBy='startTime', showHiddenInvitations=True
				).execute().get('items', [])
			except Exception:
				return
			for event in events:
				start_time_jst = parser.parse(event['start'].get('dateTime')).astimezone(timezone('Asia/Tokyo'))
				if event['reminders']['useDefault'] is True:
					rems = calendar['defaultReminders']
				else:
					rems = event['reminders']['overrides']
				for rem in rems:
					notif_time_jst = start_time_jst - timedelta(minutes=rem['minutes'])
					if (notif_time_jst - now_jst)/timedelta(minutes=1) > 11:
						continue
					notifs_latest.append((event['summary'], notif_time_jst))

		#noitfs を更新
		for notif in self.notifs:	#発動していない通知を除去
			pass
		for notif_new in notifs_latest:	#新しい通知を追加
			pass
