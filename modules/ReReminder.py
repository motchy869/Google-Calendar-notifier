"""
再通知リマインダクラス
"""

import threading

class ReReminder:
	"""
	再通知リマインダクラス
	"""
	def __init__(self, summary, trig_time):
		self.summary = summary
		self.trig_time = trig_time
