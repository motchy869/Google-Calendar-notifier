#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google-Calendar-notifier

Google Calendar から直近の予定を取得し、通知時刻になったらデスクトップに通知を表示する。
"""

import argparse
import datetime
import os

import modules.Reminder
import modules.ReReminder

import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

def main():
	"""
	main function
	"""
	print('hello')

if __name__ == '__main__':
    main()
