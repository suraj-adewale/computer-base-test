from PyQt5.QtWidgets import QMainWindow,QToolButton,QTableWidget,QTableWidgetItem,QAbstractItemView,QTextEdit,QDesktopWidget,QSplashScreen,QApplication,QDialog, QPushButton,QLabel,QSpinBox,QMessageBox,QRadioButton,\
 QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QGroupBox,QFormLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal,Qt,pyqtSlot,QDate,QSize
import os, sys,time,json,random,base64,math
from functools import partial
from question import Main

#print(random.randint(1,5))


class DashBoard(QMainWindow):
	
	def __init__(self,dataDic, parent=None):
		super(DashBoard, self).__init__(parent)			

		self.title = 'Dashboard'
		self.left = 180
		self.top = 50
		self.width = 1000
		self.height = 580

		self.regno=dataDic['profile']['regno']
		self.surname=dataDic['profile']['surname']
		self.othername=dataDic['profile']['othername']
		self.phone=dataDic['profile']['phone']
		self.email=dataDic['profile']['email']
		self.category=dataDic['profile']['category']
		self.schedule=dataDic['schedule']
		
		
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		#self.setStatusTip("SmartAccount V 2.0.1 Sadel Technology")
		#self.showMaximized()
		self.Content()
		self.setCentralWidget(self.widget)
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())

		
	def Content(self):
		self.widget=QWidget()
		mainlayout=QVBoxLayout()
		mainlayout.setSpacing(0)
		mainlayout.setContentsMargins(30, 5, 30, 30)
		self.widget.setLayout(mainlayout)

		headerlayout=QVBoxLayout()#Top header for Logo and Tittle
		labellayout=QHBoxLayout()
		schoollayout=QGridLayout()
		companylayout=QGridLayout()

		headerlayout.addLayout(labellayout)
		headerlayout.addWidget(QLabel(''))
		labellayout.addLayout(schoollayout)
		labellayout.addLayout(companylayout)

		schoollayout.addWidget(QLabel('Institution'),0,0)
		schoollayout.addWidget(QLabel('Logo....<br>'),0,1)
		companylayout.addWidget(QLabel('DigitalTesting'),0,1)

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
				 stop: 0 #686e70, stop: 1 #686e70);">Dashboard[{}]</p>'.format(self.regno))
		self.queslabel.setObjectName('queslabel')
		content=QHBoxLayout()
		content.setSpacing(10)
		content.setContentsMargins(30, 30, 30, 30)
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

		Header=['TEST NO','TEST[SECTIONS]','QUEs','DURATION','SCHEDULE','']
		table =QTableWidget()
		table.setColumnCount(6)     #Set three columns
		table.setRowCount(len(self.schedule)+2)

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

		
		row=0
		for date in sorted(self.schedule):
			timetaken=self.schedule[date]['timeallowed']
			secs=str(math.floor(int(timetaken)%60))
			mins=str(math.floor(int(timetaken)%(60*60)/60))
			hr=str(math.floor(int(timetaken)/(60*60)))
			timetaken=(('0'+str(hr) if len(str(hr))<2 else str(hr))+':'+('0'+str(mins) if len(str(mins))<2 else str(mins)) +':'\
	       		 +('0'+str(secs) if len(str(secs))<2 else str(secs)))

			Id=QLabel(str(self.schedule[date]['id']))
			tittle=QLabel(str(self.schedule[date]['tittle']+'('+self.schedule[date]['coursecode'] +')'+' '+self.schedule[date]['type']))
			no=QLabel(str(self.schedule[date]['totalques']))
			time=QLabel(str(timetaken+'hr'))
			schedule=QLabel(str(date+' '+self.schedule[date]['scheduletime']))

			Id.setObjectName('schedule')
			tittle.setObjectName('schedule')
			no.setObjectName('schedule')
			time.setObjectName('schedule')
			schedule.setObjectName('schedule')

			table.setCellWidget(row,0, Id)
			table.setCellWidget(row,1, tittle)
			table.setCellWidget(row,2, no)
			table.setCellWidget(row,3, time)
			table.setCellWidget(row,4, schedule)
			table.setCellWidget(row,5, button)
			button.clicked.connect(partial(self.OpenTest,date))
			#table.setItem(row,, QTableWidgetItem(date))
			row+=1
		
		

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
		
		scheduleitems=['My Profile']
		self.passport='image/avatar.png'
		imglayout=QVBoxLayout()
		prolayout=QVBoxLayout()

		self.imgbtn=QPushButton()
		form=QGridLayout()

		imglayout.addWidget(self.imgbtn)
		imglayout.addStretch()
		prolayout.addLayout(form)
		
		self.imgbtn.setIcon(QIcon(self.passport))
		self.imgbtn.setIconSize(QSize(100,100))
		self.imgbtn.setStyleSheet(" border-radius: 4px;;border:1px solid #00c6ff; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                          stop: 0 #dadbde, stop: 1 #f6f7fa);")
		content.addLayout(imglayout)
		content.addLayout(prolayout)
		
		reglabel=QLabel('Reg No:  ')
		reglabel.setObjectName('profile')
		regno=QLabel(self.regno)
		regno.setObjectName('profile')

		surnamelabel=QLabel('Surname:  ')
		surnamelabel.setObjectName('profile')
		surname=QLabel(self.surname)
		surname.setObjectName('profile')

		othernamelabel=QLabel('Others:  ')
		othernamelabel.setObjectName('profile')
		othername=QLabel(self.othername)
		othername.setObjectName('profile')

		phonelabel=QLabel('Phone:  ')
		phonelabel.setObjectName('profile')
		phone=QLabel(self.phone)
		phone.setObjectName('profile')

		emaillabel=QLabel('Email:  ')
		emaillabel.setObjectName('profile')
		email=QLabel(self.email)
		email.setObjectName('profile')
		
		form.addWidget(reglabel,0,1)
		form.addWidget(regno,0,2)

		form.addWidget(surnamelabel,1,1)
		form.addWidget(surname,1,2)

		form.addWidget(othernamelabel,2,1)
		form.addWidget(othername,2,2)

		form.addWidget(phonelabel,3,1)
		form.addWidget(phone,3,2)

		form.addWidget(emaillabel,4,1)
		form.addWidget(email,4,2)
					
		content.addStretch()

	def OpenTest(self,date):
   		self.constant=self.schedule[date]['constant']
   		self.coursecode=self.schedule[date]['coursecode']
   		self.year=self.schedule[date]['date']
   		self.testtype=self.schedule[date]['type']
   		self.tittle=self.schedule[date]['tittle']
   		self.authorid=self.schedule[date]['authorid']
   		self.timeallowed=self.schedule[date]['timeallowed']
   		self.questions=self.schedule[date]['questions']
   		self.answers=self.schedule[date]['answers']
   		self.question=Main(self.authorid,self.regno,self.testtype,self.year,self.tittle,self.coursecode,self.timeallowed,self.constant,self.questions,self.answers)
   		self.question.show()
   		self.close()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ques={'section A':{1:['mc','What is 10 divided by 2','2','4','5','8'],
					   2:['mc','What is 10 - 2','2','4','5','8'],
					   3:['mc','What is 100 * 2','20A','4B','5C','8D'],
					   4:['mc','What is 10 * 2','20','4','5','8'],
					   5:['fg','What is 10 * 2']
					  },

		  'section B':{1:['mc','What is 10 divided by 2','2','4','5','8'],
					   2:['mc','What is 10 - 2','2','4','5','8'],
					   3:['mc','What is 10 * 2','20','4','5','8'],
					   4:['mc','What is 10 * 2','20','4','5','8']
					   
					 }  		   	
		}

	ex = DashBoard(ques)
	ex.show()
	sys.exit(app.exec_())
