"""
通知クラス
"""

from modules.NotifWindow import NotifWindow

class Notif:
	"""
	通知クラス
	"""
	def __init__(self, summary, trig_time):
		self.summary = summary
		self.trig_time = trig_time
		self.flg_re_notif = False	#再通知か?
		self.flg_triged = False	#トリガ済みか?
		self.flg_window_displaying = False	#通知ウィンドウ表示中か?
