""" 通知ウィンドウクラス """

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSpinBox, QVBoxLayout, QWidget)

class NotifWindow(QWidget):
	""" 通知ウィンドウクラス """

	sig_done = pyqtSignal()
	sig_re_notif = pyqtSignal(int)

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

	def button_done_clicked(self):
		""" 完了ボタンがクリックされた """
		self.sig_done.emit()

	def button_re_notif_clicked(self):
		""" 再通知ボタンがクリックされた """
		self.sig_re_notif.emit(self.spinBox.value())
