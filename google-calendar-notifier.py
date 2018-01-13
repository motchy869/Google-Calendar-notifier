#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google-Calendar-notifier

Google Calendar から直近の予定を取得し、通知時刻になったらデスクトップに通知を表示する。
"""
import sys

from modules.Global import APPLICATION_NAME
from modules.Manager import Manager

import setproctitle

from PyQt5.QtWidgets import (QApplication, QWidget)

def main():
	"""
	main function
	"""
	setproctitle.setproctitle(APPLICATION_NAME)
	app = QApplication(sys.argv)
	w = QWidget()
	w.show()

	#マネージャを起動
	manager = Manager()
	manager.setDaemon(True)
	manager.setName('Manager')
	manager.start()

	sys.exit(app.exec_())
	"""
	try:
		credentials = get_credentials()
	except Exception as e:
		#print(e)
		pass

	try:
		http = credentials.authorize(httplib2.Http())
		service = discovery.build('calendar', 'v3', http=http)
	except Exception as e:
		#print(e)
		pass

	print("hoge")
	"""

if __name__ == '__main__':
    main()
