from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox,QGroupBox,QFormLayout, QPushButton,QLabel, QVBoxLayout, QGridLayout,QLineEdit
from PyQt5 import QtNetwork,QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json, sqlite3


class Settings(QDialog):
	def __init__(self, parent=None):
		super(Settings, self).__init__(parent)
		self.title = 'Settings'
		self.left = (self.x()+500)
		self.top = (self.x()+200)
		self.width =400
		self.height = 100
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		layout=QVBoxLayout()
		groupbox1 = QGroupBox('Set IP Address')	
		layout.addWidget(groupbox1)
		self.setLayout(layout)
		formlayout1 = QFormLayout()	
		formlayout1.setHorizontalSpacing(5)
		groupbox1.setLayout(formlayout1)

		self.ip=QLineEdit()
		self.port=QLineEdit("Port:e.g 8080")
		self.port.setDisabled(True)

		ipgrid=QGridLayout()
		ipgrid.setHorizontalSpacing(5)
		self.saveip=QPushButton('Save')
		currip=QLabel()
		ipgrid.addWidget(self.port,0,0,1,2)
		ipgrid.addWidget(self.saveip,0,2)

		self.saveip.clicked.connect(self.SaveIp)

		self.ip.setPlaceholderText("Set IP Address e.g 192.168.173.1 ")
		self.port.setMaximumWidth(100)
		self.ip.setMinimumWidth(200)
		formlayout1.addRow(currip,QLabel())
		formlayout1.addRow(self.ip,ipgrid)

		try:
			ip=json.load(open("json/ipaddress.json", "r"))
			currip.setText('Current IP Address:{}'.format(ip))
		except Exception as e:
			currip.setText('Current IP Address: Not Set')
		
	def SaveIp(self):
		ip=self.ip.text()
		if ip=="":
			return False
		json.dump(ip, open("json/ipaddress.json", "w"))
		#QMessageBox.about(self, 'Ip Address ', "IP Address Changed to {}	\n\n  ".format(ip))
		self.close()
	
	



if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Settings()
	ex.show()
	sys.exit(app.exec_())
