""" 通知クラス """

from datetime import (datetime, timedelta)
from pytz import timezone

from modules.Global import logger
from modules.NotifWindow import NotifWindow

from PyQt5.QtCore import (pyqtSignal, pyqtSlot, QObject, QTimer)

class Notif(QObject):
	""" 通知クラス """

	sig_reg_re_notif = pyqtSignal(str, datetime)
	#1st arg: summary
	#2nd arg: re-notif time

	def __init__(self, summary: str, notif_time_jst: datetime, flg_re_notif: bool):
		super(Notif, self).__init__()
		self.summary = summary

		self.window = NotifWindow(summary)
		self.window.sig_done.connect(self.close_notif)
		self.window.sig_re_notif.connect(self.reg_re_notif)

		self.flg_re_notif = flg_re_notif	#再通知か?
		self.flg_triged = False	#トリガ済みか?
		self.flg_window_displaying = False	#通知ウィンドウ表示中か?

		#タイマーの準備
		self.timer = QTimer()
		self.timer.setSingleShot(True)
		self.timer.setInterval(max(0, (notif_time_jst - datetime.now(timezone('Asia/Tokyo')))/timedelta(milliseconds=1)))
		self.timer.timeout.connect(self.show)
		self.timer.start()

	def __del__(self):
		self.timer.stop()

	@pyqtSlot()
	def show(self):
		""" 通知の表示 """
		self.timer.stop()
		self.flg_triged = True
		self.window.show()
		self.flg_window_displaying = True

	@pyqtSlot()
	def close_notif(self):
		""" 通知を閉じる """
		self.window.close()
		self.flg_window_displaying = False

	@pyqtSlot(int)
	def reg_re_notif(self, minutes_after: int):
		""" 再通知登録 """
		self.sig_reg_re_notif.emit(self.summary, datetime.now(timezone('Asia/Tokyo')) + timedelta(minutes=minutes_after))
		self.close_notif()
