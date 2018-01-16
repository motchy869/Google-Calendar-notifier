""" 通知クラス """

from datetime import datetime

from modules.NotifWindow import NotifWindow

from PyQt5.QtCore import (pyqtSignal, pyqtSlot, QObject)

class Notif(QObject):
	""" 通知クラス """

	sig_reg_re_notif = pyqtSignal(str, datetime)

	def __init__(self, summary: str, notif_time: datetime, flg_re_notif: bool):
		super(Notif, self).__init__()
		self.summary = summary
		self.notif_time = notif_time
		self.window = NotifWindow(summary)
		self.window.sig_done.connect(self.close_notif)
		self.window.sig_re_notif.connect(self.reg_re_notif)
		self.flg_re_notif = flg_re_notif	#再通知か?
		self.flg_triged = False	#トリガ済みか?
		self.flg_window_displaying = False	#通知ウィンドウ表示中か?

		self.timer = None	#single shot QTimer

	def show(self):
		""" 通知の表示 """
		pass

	@pyqtSlot()
	def close_notif(self):
		""" 通知を閉じる """

	@pyqtSlot(int)
	def reg_re_notif(self, minutes_after: int):
		""" 再通知登録 """
