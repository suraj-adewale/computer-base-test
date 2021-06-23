from PyQt5.QtWidgets import QMainWindow,QToolButton,QDialog,QLineEdit,QMessageBox,QSpinBox,QComboBox,QFormLayout,QTabWidget,QTableWidget,QAbstractItemView,QApplication, QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QScrollArea,QGroupBox
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal,Qt,pyqtSlot,QDate,QSize,QRunnable,QThreadPool
from testresults import TestResults
from applicants import Applicants
from upload import UpLoad
from server.result import Result
import os, sys,time,json,random,base64
from server.server import StartServer



#print(random.randint(1,5))

class DashBoard(QMainWindow):
	
	def __init__(self, parent=None):
		super(DashBoard, self).__init__(parent)

		self.title = 'Dashboard'
		self.left = 180
		self.top = 50
		self.width = 1000
		self.height = 580
		
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		#self.setStatusTip("SmartAccount V 2.0.1 Sadel Technology")
		#self.showMaximized()
		self.Content()
		self.setCentralWidget(self.widget)
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())

		#self.ip=json.load(open("json/ipaddress.json", "r"))
		self.ip='localhost'

		
	def Content(self):
		self.userid=345678
		self.widget=QWidget()
		mainlayout=QVBoxLayout()
		mainlayout.setSpacing(0)
		mainlayout.setContentsMargins(30, 5, 30, 30)
		self.widget.setLayout(mainlayout)

		headerlayout=QVBoxLayout()# Top header for Logo and Tittle
		labellayout=QHBoxLayout()
		schoollayout=QGridLayout()
		companylayout=QGridLayout()

		headerlayout.addLayout(labellayout)
		headerlayout.addWidget(QLabel(''))
		labellayout.addLayout(schoollayout)
		labellayout.addLayout(companylayout)

		school=QLabel('Federal College of Agriculture, Akure')
		school_logo=QLabel()
		pixmap=QPixmap('image/fecalogo.png')
		school_logo.setPixmap(pixmap)
		brand_name=QLabel('Test Center<br><span style="font-size:10px;">www.testcenter.net</span>')
		school.setObjectName('brand_name')
		school_logo.setObjectName('brand_name')
		brand_name.setObjectName('brand_name')

		schoollayout.addWidget(school,0,0)
		schoollayout.addWidget(school_logo,0,1)
		schoollayout.setColumnStretch(1, 2)
		companylayout.addWidget(brand_name,0,3)

		bodylayout=QVBoxLayout()#body for all text and design
		bodylayout.setSpacing(10)
		mainlayout.addLayout(headerlayout,1)
		mainlayout.addLayout(bodylayout,18)


		scroll1=QScrollArea()
		schedule=QGroupBox()
		notification=QGroupBox()

		schedule.setStyleSheet("background-color:white;")
		notification.setStyleSheet("background-color:white;")

		dashboard=QVBoxLayout()
		dashboard.setContentsMargins(0, 0, 0, 0)
		dashboard.setSpacing(0)
		scroll1.setWidgetResizable(True)
		scrollwidget=QWidget()
		scrollwidget.setStyleSheet("background-color:white;")
		scrollwidget.setLayout(dashboard)
		scroll1.setWidget(scrollwidget)

		bodylayout.addWidget(scroll1,5)
		bodylayout.addWidget(schedule,2)
		bodylayout.addWidget(notification,1)

		self.queslabel=QLabel('<p style="color:white;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
				 stop: 0 #686e70, stop: 1 #686e70);">Dashboard[{}]</p>'.format(self.userid))
		self.queslabel.setObjectName('queslabel')
		content=QHBoxLayout()
		content.setContentsMargins(50, 30, 50, 30)
		dashboard.addWidget(self.queslabel)
		dashboard.addWidget(QLabel())
		dashboard.addLayout(content)
		dashboard.addStretch()

		schedulelayout=QVBoxLayout()
		schedulelayout.setSpacing(0)
		schedulelayout.setContentsMargins(0,0,0,0)
		schedule.setLayout(schedulelayout)

		notificationlayout=QVBoxLayout()
		notificationlayout.setSpacing(0)
		notificationlayout.setContentsMargins(0,0,0,0)
		notification.setLayout(notificationlayout)

		schedulelabel=QLabel('<p style="color:white;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
				 stop: 0 #686e70, stop: 1 #686e70);">Test Schedule</p>')
		schedulelabel.setObjectName('schedulelabel')

		notificationlabel=QLabel('<p style="color:white;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
				 stop: 0 #686e70, stop: 1 #686e70);">NOTIFICATIONS</p>')
		notificationlabel.setObjectName('schedulelabel')

		tablelayout=QVBoxLayout()
		tablelayout1=QVBoxLayout()

		schedulelayout.addWidget(schedulelabel)
		schedulelayout.addLayout(tablelayout)
		schedulelayout.addStretch()

		notificationlayout.addWidget(notificationlabel)
		notificationlayout.addLayout(tablelayout1)
		notificationlayout.addStretch()

		Header=['TEST NO','TEST[SECTIONS]','QUEs','MINs','PERIOD','']
		table =QTableWidget()
		table.setColumnCount(6)     #Set three columns
		table.setRowCount(3)

		table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		header = table.horizontalHeader()       
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(4,  1*(QtWidgets.QHeaderView.Stretch)//2)
		header.setSectionResizeMode(5,  1*(QtWidgets.QHeaderView.Stretch)//2)

		tablelayout.addWidget(table)
		table.resizeRowsToContents()
		table.setSelectionMode(QAbstractItemView.MultiSelection)
		table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		table.setShowGrid(True)
		table.setHorizontalHeaderLabels(Header)

		button=QPushButton('Open Test')
		button.setStyleSheet('background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                stop: 0 #f6f7fa, stop: 1 #f6f7fa);')
		button.setObjectName('testbtn')
		table.setCellWidget(0,5, button)


		Header1=['DATE','COMMUNICATION','MODE']
		table1 =QTableWidget()
		table1.setColumnCount(3)     #Set three columns
		table1.setRowCount(3)

		table1.setEditTriggers(QAbstractItemView.AllEditTriggers)
		table1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		header = table1.horizontalHeader()       
		header.setSectionResizeMode(0, 1*(QtWidgets.QHeaderView.Stretch)//2)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(2, 1*(QtWidgets.QHeaderView.Stretch)//2)

		tablelayout1.addWidget(table1)
		table1.resizeRowsToContents()
		table1.setSelectionMode(QAbstractItemView.MultiSelection)
		table1.setEditTriggers(QAbstractItemView.NoEditTriggers)
		
		table1.setShowGrid(True)
		table1.setHorizontalHeaderLabels(Header1)
		
		scheduleitems=['User Profile','Upload Applicants','Upload Questions','View Questions','Server','Downloads','Test Schedule',\
		'Test Results','Comments','Report Issues','Make Payment','Expiry']
		
		icons={'User Profile':'user-profile-.png','Upload Applicants':'engineering.png','View Questions':'question.png','Test Results':'exam_result.png',\
		'Server':'progress.png','Downloads':'download1.png','Test Schedule':'computing.png','Upload Questions':'upload.png'\
		,'Comments':'comment.png','Make Payment':'payment.png','Report Issues':'report.png','Expiry':'expiry.png'}

		total=len(scheduleitems)
		row=range(-(-total//6))
		counts=0
		num=0

		content1=QGridLayout()
		content.addStretch()
		content.addLayout(content1)
		content.addStretch()

		for x in row:
			lesscol=total - counts
			if lesscol <6:
				for y in range(lesscol):
					self.userbtn=QToolButton()
					self.userbtn.setText(str(scheduleitems[num]))
					self.userbtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
					img=QIcon('image/'+icons.get(scheduleitems[num],'avatar.png'))
					img.setObjectName('img')
					self.userbtn.setIcon(img)
					self.userbtn.setIconSize(QSize(80,80))
					self.userbtn.clicked.connect(self.UserAction)
					self.userbtn.setStyleSheet("margin:10px; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #dadbde, stop: 1 #f6f7fa);")

					self.userbtn.setObjectName('dashboardcontent')
					content1.addWidget(self.userbtn,x+1,y)
					num+=1	
			else:	
				for y in range(6):
					self.userbtn=QToolButton()
					self.userbtn.setText(str(scheduleitems[num]))
					self.userbtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
					self.userbtn.setIcon(QIcon('image/'+icons.get(scheduleitems[num],'avatar.png')))
					self.userbtn.setIconSize(QSize(80,80))
					self.userbtn.setStyleSheet("margin:10px; background-color: rgba(10,10,10,10);")
					self.userbtn.clicked.connect(self.UserAction)
					self.userbtn.setObjectName('dashboardcontent')
					content1.addWidget(self.userbtn,x+1,y)
					
					num+=1
			counts+=6
		
	def UserAction(self):
		widget=self.sender()
		action=widget.text()

		if action=='Server':
			self.Port()		

		if action=='Upload Questions':
			self.addques=UpLoad('questions')
			self.addques.exec_()

		if action=='Upload Applicants':
			self.addques=UpLoad('register')
			self.addques.exec_()

		if action=='Test Results':
			self.addques=TestResults(Result('SelectCategory',''))
			self.addques.exec_()

		if action=='Test Schedule':
			 self.Schedule()
			#self.Server('testschedule','result')	
	
	def Schedule(self):
		self.dialog=QDialog()
		self.dialog.setWindowTitle('Test Schedule')
		self.mainlayout=QVBoxLayout()
		self.dialog.setLayout(self.mainlayout)
		self.tabs = QTabWidget()
		self.mainlayout.addWidget(self.tabs)
		#self.tabs.currentChanged.connect(self.currentTab)

		self.widget = QWidget()
		self.layout=QFormLayout()
		self.layout.setHorizontalSpacing(150)
		self.widget.setLayout(self.layout)
		self.widget.setStatusTip("")
			
		self.tabs.addTab(self.widget,"Schedule")

		self.testtitle=QLineEdit()
		self.testtitle.setPlaceholderText("Test title")
		self.testcode=QLineEdit()
		self.testcode.setPlaceholderText("Test/Course code")
		self.category=QLineEdit()
		self.category.setPlaceholderText("Class/Level")
		self.testtype=QLineEdit()
		self.testtype.setPlaceholderText("Exam/Test...")
		#self.timetaken=QLineEdit()
		self.timetaken = QSpinBox()
		self.timetaken.setValue(30)
		#self.timetaken.setPlaceholderText("Time taken(min)")
		self.schedule=QLineEdit()
		self.schedule.setPlaceholderText("Schedule")
		self.date=QLineEdit()
		self.viewresult=QComboBox()
		self.viewresult.addItems(['','Yes','No'])
		self.date.setPlaceholderText("date")

		self.layout.addRow(QLabel("testtitle:"),self.testtitle)
		self.layout.addRow(QLabel("Exam/Test code:"),self.testcode)
		self.layout.addRow(QLabel("testtype:"),self.testtype)
		self.layout.addRow(QLabel("Category:"),self.category)
		self.layout.addRow(QLabel("Time(mins):"),self.timetaken)
		self.layout.addRow(QLabel("Schedule:"),self.schedule)
		self.layout.addRow(QLabel("Instant result:"),self.viewresult)
		self.layout.addRow(QLabel("Date:"),self.date)

		gridbutton=QGridLayout()
		self.ok=QPushButton('Save')
		self.ok.clicked.connect(self.Save)
		self.cancel=QPushButton('Cancel')
		
		self.help=QPushButton('Help')
		gridbutton.addWidget(self.ok,0,0)
		gridbutton.addWidget(self.cancel,0,1)
		gridbutton.addWidget(self.help,0,2)

		buttonlayout=QFormLayout()
		buttonlayout.setHorizontalSpacing(200)
		buttonlayout.addRow(QLabel(),gridbutton)

		self.mainlayout.addLayout(buttonlayout)
		self.dialog.exec_()
		#self.cancel.clicked.connect(self.dialog.close())

	def Save(self):
		testtitle=self.testtitle.text()
		testcode=self.testcode.text()
		timetaken=self.timetaken.text()
		testtype=self.testtype.text()
		category=self.category.text()
		timetaken=self.timetaken.text()
		schedule=self.schedule.text()
		instantresult=self.viewresult.currentText()
		date=self.date.text()
				
		postList=[]
		postList.append(testtitle)
		postList.append(testcode)
		postList.append(timetaken)
		postList.append(testtype)
		postList.append(category)
		postList.append(schedule)
		postList.append(instantresult)
		postList.append(date)
		
		if postList[0] == '' or postList[1] == '' or postList[3] == '' or postList[4] == '' or postList[5] == '':
			msg=QMessageBox()
			msg.setWindowTitle('Schedule')
			msg.setIcon(QMessageBox.Information)
			msg.setStyleSheet("QLabel{min-width:250px;margin:2px;}")
			msg.setInformativeText("<div style='font-size:15px; color:green'>Empty Fields</div>")
			msg.exec_()		
			return False

		if Result('schedule', postList) == 'success':
			msg=QMessageBox()
			msg.setWindowTitle('Success')
			msg.setIcon(QMessageBox.Information)
			msg.setStyleSheet("QLabel{min-width:250px;margin:2px;}")
			msg.setInformativeText(f"<div style='font-size:15px; color:green'>Schedule set for {testcode}</div>")
			msg.exec_()
	
	def Port(self):
		self.dialog=QDialog()
		self.title = 'Port'
		self.left = (self.x()+500)
		self.top = (self.x()+200)
		self.width =400
		self.height = 100
		self.dialog.setWindowTitle(self.title)
		#self.dialog.setGeometry(self.left, self.top, self.width, self.height)
		
		layout=QVBoxLayout()
		groupbox1 = QGroupBox('Set Port')	
		layout.addWidget(groupbox1)
		self.dialog.setLayout(layout)
		formlayout1 = QFormLayout()	
		formlayout1.setHorizontalSpacing(5)
		groupbox1.setLayout(formlayout1)

		self.ip=QLineEdit()
		self.ip.setDisabled(True)
		self.port=QLineEdit()
		self.port.setPlaceholderText('eg 8080')
		ipgrid=QGridLayout()
		ipgrid.setHorizontalSpacing(5)
		self.saveip=QPushButton('Continue')
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
			self.curr_port=json.load(open("json/port.json", "r"))
			currip.setText('Currently running on Port:{}'.format(self.curr_port))
		except Exception as e:
			currip.setText('Port: Not Set')
			#print(e)
		self.dialog.exec_()

	def SaveIp(self):
		port=self.port.text()
		if self.curr_port == port:
			return False
		if port=="":
			self.start()
			self.dialog.close()
			return False
		json.dump(port, open("json/port.json", "w"))
		self.dialog.close()
		self.start()
	
	def start(self):
		self.threadpool = QThreadPool()
		worker = Worker()
		self.threadpool.start(worker)				

class Worker(QRunnable):
    @pyqtSlot()
    def run(self):
        StartServer()
        while True:
        	time.sleep(1)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = DashBoard()
	ex.show()
	sys.exit(app.exec_())
