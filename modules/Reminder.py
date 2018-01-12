"""
リマインダクラス
"""

import threading

class Reminder:
	"""
	リマインダクラス
	"""
	def __init__(self, calendar_id, event_id, summary, trig_time):
		self.calendar_id = calendar_id
		self.event_id = event_id
		self.summary = summary
		self.trig_time = trig_time
