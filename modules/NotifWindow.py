""" 通知ウィンドウクラス """

import threading
import time

from modules.Global import logger

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSpinBox, QVBoxLayout, QWidget)

class NotifWindow(QWidget):
	""" 通知ウィンドウクラス """

	sig_done = pyqtSignal()
	sig_re_notif = pyqtSignal(int)	#arg: minutes after

	def __init__(self, summary: str):
		super(NotifWindow, self).__init__()
		label = QLabel(summary)

		button_re_notif = QPushButton('再通知')
		button_re_notif.clicked.connect(self.button_re_notif_clicked)

		self.spinBox = QSpinBox()
		self.spinBox.setRange(1, 5)
		self.spinBox.setValue(5)

		button_done = QPushButton('完了')
		button_done.clicked.connect(self.button_done_clicked)

		hLayout = QHBoxLayout()
		hLayout.addWidget(button_re_notif)
		hLayout.addWidget(self.spinBox)
		hLayout.addWidget(QLabel('分'))

		vLayout = QVBoxLayout()
		vLayout.addWidget(label)
		vLayout.addLayout(hLayout)
		vLayout.addWidget(button_done)

		self.setLayout(vLayout)
		self.setWindowTitle('Google Calendar の通知')

		self.flg_can_close = False	#ウィンドウを閉じても良いか?

	def showEvent(self, se):
		"""
		ウィンドウの表示
		基底クラスの showEvent をオーバーライドしている。

		マウスカーソルが居るデスクトップの右下から出現して右上へスライドする。
		"""
		super(NotifWindow, self).showEvent(se)
		th = threading.Thread(target=self.slide)
		th.start()

	def slide(self):
		""" ウィンドウをスライドする """
		self.setEnabled(False)	#移動中は入力を無効化
		time.sleep(3)
		self.setEnabled(True)

	def button_done_clicked(self):
		""" 完了ボタンがクリックされた """
		self.flg_can_close = True
		self.sig_done.emit()

	def button_re_notif_clicked(self):
		""" 再通知ボタンがクリックされた """
		self.flg_can_close = True
		self.sig_re_notif.emit(self.spinBox.value())

	def closeEvent(self, ce):
		""" タイトルバーの x ボタンが押された """
		if self.flg_can_close:
			super(NotifWindow, self).closeEvent(ce)
		else:
			ce.ignore()
