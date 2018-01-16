"""
マネージャクラス
"""

import argparse
from datetime import (datetime, timedelta)
import os
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

from PyQt5.QtCore import (pyqtSignal, pyqtSlot, QObject, QThread, QTimer)

credentials = None
service = None

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

def wait_server_connection():
	""" http://accounts.google.com に接続できるまで待機する """
	while True:
		try:
			resp = requests.get("http://accounts.google.com")
			if resp.status_code == 200:
				break
		except Exception:
			logger.debug("Waiting server connection. Retrying in 5 seconds.")
			time.sleep(5)

class Thread_startup(QThread):
	""" 認証情報の取得, APIサービスオブジェクトの構築 """
	def __init__(self):
		super(Thread_startup, self).__init__()
		self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
		self.CLIENT_SECRET_FILE = 'client_secret.json'

	def run(self):
		""" run """
		logger.debug('Getting credentials.')
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir, 'Google-Calendar-notifier.json')

		wait_server_connection()

		store = Storage(credential_path)
		global credentials
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
			flow.user_agent = APPLICATION_NAME
			credentials = tools.run_flow(flow, store, flags)
			print('Storing credentials to ' + credential_path)

		logger.debug('Getting service.')
		http = credentials.authorize(httplib2.Http())
		global service
		service = discovery.build('calendar', 'v3', http=http)

class Thread_fetch_notif_updates(QThread):
	""" サーバーより通知を更新 """
	sig_fetch_done = pyqtSignal(bool, list)
	#1st arg: True,False=succeed,fail
	#2nd arg: [{'summary': 'summary', 'notif_time': notif_time_jst}, ...]

	def __init__(self):	#pylint: disable=W0235
		super(Thread_fetch_notif_updates, self).__init__()

	def run(self):
		""" run """
		logger.debug('Fetching latest notifs.')
		wait_server_connection()

		#カレンダーリストを取得(「Contacts, 日本の祝日」を除く最大3)
		try:
			calendars = service.calendarList().list(	#pylint: disable=E1101
				maxResults=3+2, minAccessRole='reader', showHidden='true'
			).execute().get('items', [])
		except Exception:
			self.sig_fetch_done.emit(False, [])
			return

		#各カレンダーから直近最大3個の通知を取得
		notifs_latest = []	#[{'summary': summary', 'notif_time': notif_time_jst}, ...]
		now_jst = datetime.now(timezone('Asia/Tokyo'))
		for calendar in calendars:
			if calendar['summary'] == '日本の祝日' or calendar['summary'] == 'Contacts':
				continue
			try:
				events = service.events().list(#pylint: disable=E1101
					calendarId=calendar['id'], timeMin=now_jst.isoformat(),
					maxResults=3, singleEvents=True, orderBy='startTime', showHiddenInvitations=True
				).execute().get('items', [])
			except Exception:
				self.sig_fetch_done.emit(False, [])
				return
			for event in events:
				start_time_jst = parser.parse(event['start'].get('dateTime')).astimezone(timezone('Asia/Tokyo'))
				if event['reminders']['useDefault'] is True:
					rems = calendar['defaultReminders']
				else:
					rems = event['reminders']['overrides']
				for rem in rems:
					notif_time_jst = start_time_jst - timedelta(minutes=rem['minutes'])
					if (notif_time_jst - now_jst)/timedelta(minutes=1) <= 0 or (notif_time_jst - now_jst)/timedelta(minutes=1) > 11:
						continue	#通知時刻を過ぎたものや、11分超過後のものは除外(次の更新で取り入れられる。1分は安全マージン)。
					notifs_latest.append({'summary': event['summary'], 'notif_time': notif_time_jst})
		self.sig_fetch_done.emit(True, notifs_latest)

class Manager(QObject):
	""" マネージャクラス """

	def __init__(self):
		super(Manager, self).__init__()
		self.notifs = []	#Notif インスタンスのリスト

		#認証情報の取得, APIサービスの構築
		self.th = Thread_startup()
		self.th.finished.connect(self.fetch_notif_updates)	#最初の更新
		self.th.start()

	@pyqtSlot()
	def fetch_notif_updates(self):
		""" サーバより最新の通知を取得 """
		self.th = Thread_fetch_notif_updates()
		self.th.sig_fetch_done.connect(self.update_notifs)
		self.th.start()

	@pyqtSlot(bool, list)
	def update_notifs(self, isSucceeded: bool, notifs_latest: list):
		""" 通知を更新 """

		if isSucceeded:
			#notifs 内の表示中,未トリガ再通知以外を削除
			for i, notif in enumerate(self.notifs):
				if notif.flg_window_displaying:
					continue
				if (not notif.flg_triged) and notif.flg_re_notif:
					continue
				del self.notifs[i]

			#新しい通知を追加
			for notif in notifs_latest:
				new_notif = Notif(notif['summary'], notif['notif_time'], False)
				new_notif.sig_reg_re_notif.connect(self.register_re_notif)
				self.notifs.append(new_notif)

			#テスト通知
			new_notif = Notif('test notif', datetime.now(timezone('Asia/Tokyo')) + timedelta(seconds=1), False)
			new_notif.sig_reg_re_notif.connect(self.register_re_notif)
			self.notifs.append(new_notif)

		QTimer.singleShot(1000*60*10, self.fetch_notif_updates)	#次回のスケジュール

	@pyqtSlot(str, datetime)
	def register_re_notif(self, summary: str, notif_time_jst: datetime):
		""" 再通知の登録 """
		re_notif = Notif(summary, notif_time_jst, True)
		re_notif.sig_reg_re_notif.connect(self.register_re_notif)
		self.notifs.append(re_notif)
