from PyQt5.QtWidgets import QMainWindow,QFrame,QDialogButtonBox,QTextEdit,QDesktopWidget,QSplashScreen,QApplication,QDialog, QPushButton,QLabel,QSpinBox,QMessageBox,QRadioButton,\
 QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QGroupBox,QFormLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal,Qt,pyqtSlot,QDate,QSize,QTimer,QRunnable,QThreadPool
QThreadPool
import os, sys,time,json,random,base64,math
from functools import partial
from PyQt5 import QtWebEngineWidgets 
from calculator import Calculator
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QDir, QUrl


class QHLine(QFrame):
	def __init__(self):
		super(QHLine, self).__init__()
		self.setFrameShape(QFrame.HLine)
		self.setFrameShadow(QFrame.Sunken)

class QVLine(QFrame):
	def __init__(self):
		super(QVLINE, self).__init__()
		self.setFrameShape(QFrame.VLine)
		self.setFrameShadow(QFrame.Sunken)

	

class Main(QMainWindow):
	
	def __init__(self,authorid,regno,name,testtype,year,tittle,course_code,timeallowed,const,quesdic,ansDic, parent=None):
		super(Main, self).__init__(parent)

		self.ipaddress=json.load(open("json/ipaddress.json", "r"))
		#self.ip='localhost'
		print
		self.timerDic={}
		self.title = 'Computer Based Test'
		self.left = 180
		self.top = 50
		self.width = 1000
		self.height = 580
		self.const=const
		self.quesDic=quesdic

		self.authorid=authorid
		self.regno=regno
		self.othername = name
		self.year=year
		self.course_code=course_code
		self.timeallowed=timeallowed
		self.testtype=testtype
		self.title=tittle
		self.timetaken=timeallowed

		self.timerDic['regno']=self.regno
		self.timerDic['course_code']=self.course_code
		self.timerDic['authorid']=self.authorid
		self.timerDic['testtype']=self.testtype
		self.timerDic['year']=self.year
		self.postDic={'regno':self.regno,'year':self.year,'course_code':self.course_code,'testtype':self.testtype,'authorid':self.authorid}
		
		self.answeredDix=ansDic
		postDic=json.dumps(self.postDic)
		##self.Server('checkanswers',base64.b64encode(postDic.encode()),'choice')
		
		
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		#self.setStatusTip("SmartAccount V 2.0.1 Sadel Technology")
		self.showMaximized()
		self.Content()
		self.setCentralWidget(self.widget)
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())

		
	def Content(self):
		self.widget=QWidget()
		mainlayout=QVBoxLayout()
		mainlayout.setSpacing(0)
		mainlayout.setContentsMargins(30, 5, 30, 30)
		self.widget.setLayout(mainlayout)
		self.saving_answer=''
		self.sectionList=list(sorted(self.quesDic))# or ([*self.quesDic])

		self.quesno=1
		self.currsection=self.sectionList[0]
		self.currQuestionData={self.currsection:self.quesno}
		self.total={self.currsection:len(self.quesDic[self.currsection])}
		self.totalques=self.total[self.currsection]

		self.answeredList=self.answeredDix.get(self.currsection,{})

		random.seed(self.const)
		self.randomNumber = [i+1 for i in range(len(self.quesDic[self.currsection]))]
		random.shuffle(self.randomNumber)
		
		self.notansweredDix={}
		for section in self.quesDic:
			self.notansweredList=[]
			for quesno in [i+1 for i in range(len(self.quesDic[section]))]:
				if str(quesno) in self.answeredDix.get(section,[]):
					self.notansweredList.append(quesno)		
			self.notansweredDix[section]=self.notansweredList
		
		if self.notansweredList==[]:
			self.notansweredList.append(1)

		self.btnList=[]
		self.radiobtnList=[]
		self.labelList=[]
		#print(self.notansweredDix)
		#print(self.answeredList)
	
		try:
			self.passport=('image/avatar.png')
		except Exception as e:
			self.passport=('image/avatar.png')
		
		headerlayout=QVBoxLayout()# Top header for Logo and Tittle
		labellayout=QHBoxLayout()
		schoollayout=QGridLayout()
		companylayout=QGridLayout()

		headerlayout.addLayout(labellayout)
		#headerlayout.addWidget(QLabel())
		labellayout.addLayout(schoollayout)
		labellayout.addLayout(companylayout)

		bodylayout=QVBoxLayout()#body for all text and design
		mainlayout.addLayout(headerlayout,1)
		mainlayout.addLayout(bodylayout,18)

		header=QWidget()#header inside body
		content=QHBoxLayout()
		bodylayout.addWidget(header)
		bodylayout.addLayout(content)

		questionlayout=QVBoxLayout()
		panellayout=QVBoxLayout()
		content.addLayout(questionlayout,4)
		content.addLayout(panellayout,1)

		section=QGroupBox('Sections')
		scroll1=QScrollArea()
		self.control=QGroupBox()

		questionarea=QVBoxLayout()
		questionarea.setContentsMargins(0, 0, 0, 0)
		questionarea.setSpacing(0)
		scroll1.setWidgetResizable(True)
		scrollwidget=QWidget()
		scrollwidget.setStyleSheet("background-color:white;")
		scrollwidget.setLayout(questionarea)
		scroll1.setWidget(scrollwidget)

		idlayout=QGridLayout()
		scroll2=QScrollArea()
		submitlayout=QGroupBox()

		self.numlayout=QVBoxLayout()
		scroll2.setWidgetResizable(True)
		scrollwidget2=QWidget()
		scrollwidget2.setLayout(self.numlayout)
		scroll2.setWidget(scrollwidget2)

		questionlayout.addWidget(section,1)
		questionlayout.addWidget(scroll1,11)
		questionlayout.addWidget(self.control,1)

		panellayout.addLayout(idlayout,2)
		panellayout.addWidget(scroll2,10)
		panellayout.addWidget(submitlayout,1)


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
		
		self.titlelabel=QLabel(self.title)
		self.titlelabel.setObjectName('titlelabel')
		headerlayout.addWidget(self.titlelabel)

		self.sectionlayout=QGridLayout()
		self.sectionlayout.setContentsMargins(0,0,5,0)
		section.setLayout(self.sectionlayout)

		self.queslabel=QLabel('<p style="color:red;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);">Question 1</p>')
		self.queslabel.setObjectName('queslabel')
		self.question=QVBoxLayout()
		self.question.setContentsMargins(20,0,40,0)
		questionarea.addWidget(self.queslabel,1)
		questionarea.addStretch()
		questionarea.addLayout(self.question,15)
		self.browser= QWebEngineView()
	
		self.browser.setUrl(QtCore.QUrl('http://'+self.ipaddress))
		#self.browser.load(QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r'\html\cbt.html'))
		self.browser.loadFinished.connect(self.onLoadFinished)
		
		#self.browser= QLabel()
		self.optionlayout=QGridLayout()
		self.optionlayout.setSpacing(10)
		self.browser.setObjectName('currquestion')
		self.question.addWidget(self.browser)
		#self.question.addWidget(QHLine())
		#self.question.addStretch(1)
		#self.question.addLayout(self.optionlayout,1)
		
		self.question.addStretch(1)

		controllayout=QHBoxLayout()
		controllayout.setSpacing(0)
		self.nextbtn=QPushButton()
		self.nextbtn.setIcon(QIcon('image/arrow-right.png'))
		self.nextbtn.setIconSize(QSize(80,35))
		self.nextbtn.setStyleSheet("border:0px solid green;")
		self.nextbtn.clicked.connect(partial(self.btnstate,self.nextbtn,'next'))
		self.nextbtn.setObjectName('nextbtn')
		self.prevbtn=QPushButton()
		self.prevbtn.setIcon(QIcon('image/arrow-left.png'))
		self.prevbtn.setIconSize(QSize(80,35))
		self.prevbtn.setStyleSheet("border:0px solid green;")
		self.prevbtn.clicked.connect(partial(self.btnstate,self.prevbtn,'prev'))
		self.prevbtn.setObjectName('prevbtn')
		self.control.setLayout(controllayout)
		controllayout.addWidget(self.prevbtn)
		controllayout.addWidget(self.nextbtn)
		controllayout.addStretch()
		self.prevbtn.setDisabled(True)

		passport=QLabel(self)
		pixmap=QPixmap(self.passport)
		passport.setPixmap(pixmap)

		self.timerwidget=QLabel('<p style="font-size:14px;"><b>Time Left<span style="color:green;">:\
		 {}</span><br><span style="font-size:10px;">Reg no: {}</span></b></p>'.format('Time Allowed','Reg No'))
		idlayout.addWidget(passport,0,0)
		idlayout.addWidget(self.timerwidget,0,1)
		idlayout.addWidget(QLabel(),1,0)

		statlayout=QGridLayout()
		self.numlayout.setContentsMargins(0, 0, 0, 0)
		self.numlayout.setSpacing(0)
		controllayout2=QVBoxLayout()
		self.numlayout.addLayout(statlayout,1)
		self.numlayout.addLayout(controllayout2,4)

		self.answeredbtn=QPushButton('0')
		self.answeredbtn.setObjectName('answeredbtn')
		self.notansweredbtn=QPushButton('1')
		self.notansweredbtn.setObjectName('notansweredbtn')
		self.notvisitedbtn=QPushButton(str(self.totalques-1))
		self.notvisitedbtn.setObjectName('notvisitedbtn')
		self.subject=QLabel(str(self.course_code))
		self.subject.setObjectName('subject')

		statlayout.addWidget(self.answeredbtn,0,0)
		statlayout.addWidget(QLabel('Answered'),0,1)

		statlayout.addWidget(self.notansweredbtn,0,2)
		statlayout.addWidget(QLabel('Not answered'),0,3)
		statlayout.addWidget(self.notvisitedbtn,1,0)
		statlayout.addWidget(QLabel('Not visited'),1,1)
		statlayout.addWidget(self.subject,2,0,1,4)

		controlheader=QLabel('Choose a Question')
		controlheader.setObjectName('questionlabel')
		
		controllabel=QVBoxLayout()
		self.controlcontent=QGridLayout()
		stretch=QVBoxLayout()

		controllayout2.addLayout(controllabel)
		controllayout2.addLayout(self.controlcontent)
		controllayout2.addLayout(stretch)
		controllabel.addWidget(controlheader)
		stretch.addStretch()

		self.SectionButton()		

		submit=QHBoxLayout()
		submitbtn=QPushButton('Submit')
		submitbtn.clicked.connect(self.SubmitNow)
		submitbtn.setObjectName('submitbtn')
		submitlayout.setLayout(submit)
		submit.addStretch()
		submit.addWidget(submitbtn)
		submit.addStretch()
 		

		self.ChooseNumber(self.totalques)
		
		self.timer1 = QTimer()
		self.timer1.setInterval(1000)
		self.timer1.timeout.connect(self.CountDown)
		self.timer1.start()
		#print(len(self.notansweredList),len(self.answeredDix.get(self.currsection,[])))
		self.answeredbtn.setText(str(len(self.answeredDix.get(self.currsection,[]))))
		self.notansweredbtn.setText(str(len(self.notansweredList)-len(self.answeredDix.get(self.currsection,[]))))
		self.notvisitedbtn.setText(str(self.totalques-len(self.notansweredList)))
		self.queslabel.setText('<p style="color:green;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);">Question '+str(self.quesno)+'</p>' if str(self.quesno )in self.answeredList \
									else '<p style="color:red;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);">Question '+str(self.quesno)+'</p>')
		
		for index in self.answeredList:
			(self.btnList[int(index)-1]).setStyleSheet("background-color:green;border-top-right-radius: 12px;\
				border-top-left-radius: 12px; border-bottom-right-radius: 6px;border-bottom-left-radius: 6px;")
		
		self.channel=QWebChannel()
		self.channel.registerObject('backend', self)
		self.browser.page().setWebChannel(self.channel)

	
	def onLoadFinished(self):
		self.PrintQuestions()
	def recurring_timer(self):
		self.CheckTimer('timer')    
					
	def  PrintQuestions(self):
		self.quesno=self.currQuestionData.get(self.currsection,1)
		currquestiondata=self.quesDic[self.currsection][str(self.randomNumber[(self.quesno-1)])]
		self.currqchoicetype=currquestiondata[1]
		currquestion=currquestiondata[2]
		#print(str(self.randomNumber[(self.quesno-1)]))
		#print(self.quesDic[self.currsection])		

		#pageSource+="<p>If $ax^2+bx+c=0$ with $a≠0$, then: $x={-b±√{b^2-4ac}}/{2a}$  $u = &int;↙{-&infin;}↖{&infin;}(awesome)dx;$</p>"
		
		if self.currqchoicetype=='mc':
			labelChoices=['A','B','C','D','E','F','G']
			# choices from the qusetion
			options=currquestiondata[3:]
			# random choices from the qusetion
			randomOptions=currquestiondata[3:]
			random.seed(self.const)
			# ramdomized choices 
			random.shuffle(randomOptions)
			radioHtml=""	
			#print(self.randomNumber[self.quesno-1],self.quesno)
			self.postDic['quesno']=self.randomNumber[self.quesno-1]
			self.postDic['quesno_']=str(self.quesno)
			self.postDic['choice']=""
			self.postDic['choicetype']=self.currqchoicetype
			self.postDic['section']=self.currsection
			postDic=json.dumps(self.postDic)
			
			for quetChoices in randomOptions:
				checked=""
				choice=labelChoices[options.index(quetChoices)]
				if str(self.quesno) in self.answeredList:
					answerChoice=self.answeredList[str(self.quesno)]
					if answerChoice==choice:
						checked="checked"

				radioHtml+="<input type='radio' class='radioHtml' name='option' id="+choice+" value="+choice+" onclick='return save(this.value,"+postDic+")' "+checked+">"+quetChoices+"<br>"

			page = self.browser.page()
			page.runJavaScript('DisplayQuestion({});'.format([currquestion,radioHtml]))
			
		if self.currqchoicetype=='FillingTheGap':
			self.textanswer=QTextEdit()
			
			if str(self.quesno) in self.answeredList:
				answer=self.answeredList[str(self.quesno)]
				self.textanswer.setText(str(answer))

			textInput='<p></p>'
	
	@pyqtSlot(str)
	def Submitted(self,arg):
		self.timer1.stop()
		QMessageBox.about(self, 'Submitted', "<p> 	\n{} {} has been taken by you	\n</p>".format(self.course_code, self.testtype)) 
		if (QMessageBox.Ok)==1024:
			self.close()
	@pyqtSlot(str)
	def JoinRoom(self,arg):
		self.view = self.browser.page()
		self.view.runJavaScript('JoinRoom({});'.format({'id':self.regno, 'room':self.course_code,\
		'course_code':self.course_code,'testtype':self.testtype, 'year':self.year, 'authorid':self.authorid,}))

		
	@pyqtSlot(str,int)	
	def RadioButtonToggled(self,answer,test):
		
		self.answeredList[str(self.quesno)]=answer
		self.answeredDix[self.currsection]=self.answeredList
		
		self.answeredbtn.setText(str(len(self.answeredDix[self.currsection])))
		self.notansweredbtn.setText(str(len(self.notansweredList)-len(self.answeredDix[self.currsection])))
		self.notvisitedbtn.setText(str(self.totalques-len(self.notansweredList)))
		(self.btnList[self.quesno-1]).setStyleSheet("background-color:green;border-top-right-radius: 12px;\
			border-top-left-radius: 12px; border-bottom-right-radius: 6px;border-bottom-left-radius: 6px;")
		
		self.queslabel.setText('<p style="color:green;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);">Question '+str(self.quesno)+'</p>' if str(self.quesno) in self.answeredList \
									else '<p style="color:red;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);">Question '+str(self.quesno)+'</p>')	
	
		if self.quesno is not self.totalques:	
			self.btnstate('widget','next')	
		
	def SectionButton(self):
		self.sectionbtnDic={}
		col=0
		for section in self.sectionList:
			self.sectionbtn=QPushButton(section)
			self.sectionbtn.clicked.connect(self.Sections)
			self.sectionbtn.setObjectName('sectionbtn')
			self.sectionlayout.addWidget(self.sectionbtn,0,col)
			self.sectionbtnDic[section]=self.sectionbtn
			if col==0:
				self.sectionbtn.setStyleSheet('background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
				 stop: 0 #f6f7fa, stop: 1 #00c6ff);')
			col+=1
		self.sectionlayout.setColumnStretch(col, col+1)

		calc=QPushButton()
		calc.setStyleSheet('border:none;')
		calc.setIcon(QIcon('image/calculator.png'))
		calc.setIconSize(QtCore.QSize(40,30))

		calc.clicked.connect(self.Calculate)
		self.sectionlayout.addWidget(calc,0,col+1)

	def Calculate(self):
		Calculator(self).exec_()
		
	def ChooseNumber(self,totalques):
		row=range(-(-totalques//5))
		counts=0
		num=1

		for btn in self.btnList:
			self.controlcontent.removeWidget(btn)
			btn.deleteLater()
			btn = None
		self.btnList=[]

		for x in row:
			lesscol=totalques - counts
			if lesscol <5:
				for y in range(lesscol):
					self.quesnobtn=QPushButton(str(num))
					self.quesnobtn.clicked.connect(self.btnstate1)
					self.quesnobtn.setObjectName('quesnobtn')
					self.controlcontent.addWidget(self.quesnobtn,x+1,y)
					self.btnList.append(self.quesnobtn)
					num+=1
			elif totalques <5:
				for y in range(totalques):
					self.quesnobtn=QPushButton(str(num))
					self.quesnobtn.clicked.connect(self.btnstate1)
					self.quesnobtn.setObjectName('quesnobtn')
					self.controlcontent.addWidget(self.quesnobtn,x+1,y)
					self.btnList.append(self.quesnobtn)
					num+=1		
			else:	
				for y in range(5):
					self.quesnobtn=QPushButton(str(num))
					self.quesnobtn.clicked.connect(self.btnstate1)
					self.quesnobtn.setObjectName('quesnobtn')
					self.controlcontent.addWidget(self.quesnobtn,x+1,y)
					self.btnList.append(self.quesnobtn)
					num+=1
			counts+=5
		self.notansweredList=self.notansweredDix.get(self.currsection,[1])	
		for index in self.notansweredList:
			(self.btnList[index-1]).setStyleSheet("background-color:red;border-bottom-right-radius:12px;\
			 border-bottom-left-radius: 0px;")

	def Sections(self):
		self.currsection=self.sender().text()
		self.notansweredList=self.notansweredDix.get(self.currsection)
		if self.notansweredList==[]:
			self.notansweredList.append(1)

		self.answeredList=self.answeredDix.get(self.currsection,{})
		self.quesno=self.currQuestionData.get(self.currsection,1)

		if self.currsection not in self.total:
			self.total={self.currsection:len(self.quesDic[self.currsection])}
		self.totalques=self.total[self.currsection]

		random.seed(self.const)
		self.randomNumber = [i+1 for i in range(len(self.quesDic[self.currsection]))]
		random.shuffle(self.randomNumber)

		self.ChooseNumber(self.totalques)

		self.answeredbtn.setText(str(len(self.answeredDix.get(self.currsection,[]))))
		self.notansweredbtn.setText(str(len(self.notansweredList)-len(self.answeredDix.get(self.currsection,[]))))
		self.notvisitedbtn.setText(str(self.totalques-len(self.notansweredList)))
		self.queslabel.setText('<p style="color:green;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);">Question '+str(self.quesno)+'</p>' if str(self.quesno) in self.answeredList \
									else '<p style="color:red;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);">Question '+str(self.quesno)+'</p>')
		
		for index in self.answeredList:
			(self.btnList[int(index)-1]).setStyleSheet("background-color:green;border-top-right-radius: 12px;\
				border-top-left-radius: 12px; border-bottom-right-radius: 6px;border-bottom-left-radius: 6px;")

		for section in self.sectionbtnDic:
			if section==self.currsection:
				(self.sectionbtnDic[section]).setStyleSheet('background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
				 stop: 0 #f6f7fa, stop: 1 #00c6ff);')
				continue
			(self.sectionbtnDic[section]).setStyleSheet(' background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
				 stop: 0 #9da49d, stop: 1 #9da49d);')
		
		self.PrintQuestions()

		if self.quesno==1:
			self.prevbtn.setDisabled(True)
		else:
			self.prevbtn.setEnabled(True)

		if self.quesno==self.totalques:
			self.nextbtn.setDisabled(True)
		else:
			self.nextbtn.setEnabled(True)
		
	def btnstate1(self):
		if self.currqchoicetype=='FillingTheGap' and self.textanswer.toPlainText()!='':
			self.answeredList[str(self.quesno)]=self.textanswer.toPlainText()
			(self.btnList[self.quesno-1]).setStyleSheet("background-color:green;border-top-right-radius: 12px;\
				border-top-left-radius: 12px; border-bottom-right-radius: 6px;border-bottom-left-radius: 6px;")
			self.SaveAnswer(self.textanswer.toPlainText())	

		self.quesno=int(self.sender().text())
		if self.quesno==1:
			self.prevbtn.setDisabled(True)
		else:
			self.prevbtn.setEnabled(True)

		if self.quesno==self.totalques:
			self.nextbtn.setDisabled(True)
		else:
			self.nextbtn.setEnabled(True)

		if self.quesno not in self.notansweredList:
			self.notansweredList.append(self.quesno)
			self.notansweredDix[self.currsection]=self.notansweredList
		self.answeredbtn.setText(str(len(self.answeredDix.get(self.currsection,[]))))
		
		self.notansweredbtn.setText(str(len(self.notansweredList)-len(self.answeredDix.get(self.currsection,[]))))
		
		self.notvisitedbtn.setText(str(self.totalques-len(self.notansweredList)))
		self.queslabel.setText('<p style="color:green;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);">Question '+str(self.quesno)+'</p>' if str(self.quesno) in self.answeredList \
									else '<p style="color:red;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);">Question '+str(self.quesno)+'</p>')

		self.currQuestionData[self.currsection]=self.quesno

		self.PrintQuestions()
		if str(self.quesno) in self.answeredList:
			if self.currqchoicetype=='FillingTheGap':
				self.textanswer.setText(self.answeredList[str(self.quesno)])
			
		else:	
			(self.btnList[self.quesno-1]).setStyleSheet("background-color:red;border-bottom-right-radius: 12px;\
			 border-bottom-left-radius: 0px;")

	def btnstate(self,widget,control):
		if self.currqchoicetype=='FillingTheGap' and self.textanswer.toPlainText()!='':
			self.answeredList[str(self.quesno)]=self.textanswer.toPlainText()
			(self.btnList[self.quesno-1]).setStyleSheet("background-color:green;border-top-right-radius: 12px;\
				border-top-left-radius: 12px; border-bottom-right-radius: 6px;border-bottom-left-radius: 6px;")
			self.SaveAnswer(self.textanswer.toPlainText())
		
		if control=='prev':
			self.quesno=self.quesno-1

		if control=='next':
			self.quesno=self.quesno+1	
		
		if self.quesno==1:
			self.prevbtn.setDisabled(True)
		else:
			self.prevbtn.setEnabled(True)

		if self.quesno==self.totalques:
			self.nextbtn.setDisabled(True)
		else:
			self.nextbtn.setEnabled(True)		
		
		if self.quesno not in self.notansweredList:
			self.notansweredList.append(self.quesno)
			self.notansweredDix[self.currsection]=self.notansweredList
		self.answeredbtn.setText(str(len(self.answeredDix.get(self.currsection,[]))))
		self.notansweredbtn.setText(str(len(self.notansweredList)-len(self.answeredDix.get(self.currsection,[]))))
		self.notvisitedbtn.setText(str(self.totalques-len(self.notansweredList)))
		self.queslabel.setText('<p style="color:green;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);">Question '+str(self.quesno)+'</p>' if str(self.quesno) in self.answeredList \
									else '<p style="color:red;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);">Question '+str(self.quesno)+'</p>')
		
		self.currQuestionData[self.currsection]=self.quesno

		
		self.PrintQuestions()
		if str(self.quesno) in self.answeredList:
			if self.currqchoicetype=='FillingTheGap':
				self.textanswer.setText(self.answeredList[str(self.quesno)])
			
		else:	
			(self.btnList[self.quesno-1]).setStyleSheet("background-color:red;border-bottom-right-radius: 12px;\
			 border-bottom-left-radius: 0px;")

	def SaveAnswer(self,answer):
		self.postDic['quesno']=self.randomNumber[self.quesno-1]
		if self.currqchoicetype=='mc':
			self.postDic['quesno_']=(str(self.quesno)+self.answeredList[str(self.quesno)])
		if self.currqchoicetype=='FillingTheGap':
			self.postDic['quesno_']=(str(self.quesno))	
		self.postDic['choice']=answer
		self.postDic['choicetype']=self.currqchoicetype
		self.postDic['section']=self.currsection
		
		postDic=json.dumps(self.postDic)
		postDic=base64.b64encode(postDic.encode())
		self.saving_answer='saving_answer'
		#self.Server('postanswer',postDic,'choice')
		

	def CheckTimer(self,action):
		if self.saving_answer=='saving_answer':
			time.sleep(1)
		self.timerDic['timer']=self.timeallowed
		postDic=json.dumps(self.timerDic)
		postDic=base64.b64encode(postDic.encode())
		#self.Server(action,postDic,'timer')		    

	def CountDown(self):
		self.timeallowed=int(self.timeallowed)
		secs=(math.floor(self.timeallowed%60))
		mins=(math.floor(self.timeallowed%(60*60)/60))
		hr=(math.floor(self.timeallowed/(60*60)))
		secs = secs -1;

		if secs < 0:
			secs += 60
			mins = mins - 1

		if  mins < 0:
			mins += 60
			hr = hr -1
		self.timeallowed-=1

		timeleft=(('0'+str(hr) if len(str(hr))<2 else str(hr))+':'+('0'+str(mins) if len(str(mins))<2 else str(mins)) +':'\
				 +('0'+str(secs) if len(str(secs))<2 else str(secs)))

		if hr<=0 and mins < 5:
			self.timerwidget.setText('<p style="margin:1px;font-size:12px;">\
				<span style="font-size:12px;">{}<br> ({})</span><br><br>\
				<b>Time Left:<span style="color:red;">\
				{}</span></p>'.format(self.othername,self.regno, timeleft))
		else: 		
			self.timerwidget.setText('<p style="margin:1px;font-size:12px;">\
				<span style="font-size:12px;">{}<br> ({})</span><br><br>\
				<b>Time Left:<span style="color:green;">\
				{}</span></p>'.format(self.othername,self.regno, timeleft))
		
		if hr<=0 and mins<=0 and secs<=0 or self.timeallowed<=0:
			self.CheckTimer('timeup') 
			self.timer1.stop()

			self.view = self.browser.page()
			self.view.runJavaScript('LeaveRoom({});'.format({'id':self.regno, 'room':self.course_code,\
			'course_code':self.course_code,'testtype':self.testtype, 'year':self.year, 'authorid':self.authorid}))

			QMessageBox.about(self, 'Submit', "\n{} has been successfully submitted  \n".format(self.course_code)) 
			if (QMessageBox.Ok)==1024:
				self.close()
		
	def SubmitNow(self):
		self.msg=QMessageBox()
		self.msg.setIcon(QMessageBox.Information)
		self.msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		self.msg.button(QMessageBox.Yes).setText("Yes, Submit Now!")
		self.msg.button(QMessageBox.Yes).setStyleSheet("border-radius:3px;background-color: green;padding:1px;color: white;min-width: 110px;height:20px;")
		self.msg.button(QMessageBox.No).setStyleSheet("border-radius:3px;background-color: red;padding:1px;color: white;min-width: 80px;height:20px;")
		self.msg.setWindowTitle('Submit')
		self.msg.setInformativeText("<p style='font-size:15px; color:green'>Are you sure you want to submit now</p>")
		self.msg.buttonClicked.connect(self.MsgBtn)
		retrieval =self.msg.exec_()

	def MsgBtn(self,item):
		action=item.text()
		if action=='&No':
			self.msg.close()
		if action=='Yes, Submit Now!':
			if self.currqchoicetype=='FillingTheGap':
				self.SaveAnswer(self.textanswer.toPlainText())
			self.view = self.browser.page()
			self.timer1.stop()
			self.msg.close()
			self.close()

			self.view = self.browser.page()
			self.view.runJavaScript('LeaveRoom({});'.format({'id':self.regno, 'room':self.course_code,\
			'course_code':self.course_code,'testtype':self.testtype, 'year':self.year, 'authorid':self.authorid,}))
			QMessageBox.about(self, 'Submit', "\n{} has been successfully submitted  \n".format(self.course_code)) 
		
	


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Main('106AA','Test','2019','MTH222',100,ques)
	ex.show()
	sys.exit(app.exec_())		