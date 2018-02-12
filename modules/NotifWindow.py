""" 通知ウィンドウクラス """

import math
import threading
import time

from modules.Global import logger

from PyQt5.QtCore import (pyqtSignal, QPoint, Qt)
from PyQt5.QtGui import (QCursor, QGuiApplication)
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton, QSpinBox, QVBoxLayout, QWidget)

class NotifWindow(QWidget):
	""" 通知ウィンドウクラス """

	sig_done = pyqtSignal()
	sig_re_notif = pyqtSignal(int)	#arg: minutes after

	def __init__(self, summary: str):
		super(NotifWindow, self).__init__()
		label = QLabel(summary)
		label.setStyleSheet("font-size: 14pt; font-weight: bold")

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
		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)	#常に最前面表示

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
		screens = QGuiApplication.screens()
		screen = screens[QApplication.desktop().screenNumber(QCursor.pos())]	#マウスカーソルが居るデスクトップ
		X = screen.geometry().bottomRight().x() - self.frameSize().width()	#通知ウィンドウの左端座標
		Y = screen.geometry().bottomRight().y() - self.frameSize().height()	#通知ウィンドウ上端初期y座標
		DURATION = 1.0	#エフェクト時間[sec]
		DIV = 120	#エフェクト時間分割数
		for t in range(-DIV>>1, DIV>>1):
			self.move(X, Y/(1.0+math.exp(5.0*t/(0.5*DIV))))	#シグモイド関数で動かす
			time.sleep(DURATION/DIV)
			self.move(X, 0)	#仕上げ
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
