#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google-Calendar-notifier

Google Calendar から直近の予定を取得し、通知時刻になったらデスクトップに通知を表示する。
"""

import logging

import modules.Core

from PyQt5.QtWidgets import (QApplication, QWidget)

#logging の設定
logger = logging.getLogger(__name__); logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler(); streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s: %(message)s'))
logger.addHandler(streamHandler)

def main():
	"""
	main function
	"""
	#app = QApplication(sys.argv)
	#w = QWidget()
	#w.show()

	quit()

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

	#sys.exit(app.exec_())

if __name__ == '__main__':
    main()
