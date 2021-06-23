from PyQt5.QtWidgets import QPushButton,QToolButton,QListWidget,QDialogButtonBox,QDialog,QAbstractItemView,QTableWidget,QTextEdit,QLabel,QCompleter,QTableWidgetItem,\
QMessageBox,QApplication,QMainWindow, QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtCore import Qt, QDate,QDateTime,QSize
from PyQt5.QtGui import QIcon,QPixmap
from functools import partial
import sys

class AddQuestion(QDialog):
	def __init__(self,parent=None):
		super(AddQuestion, self).__init__(parent)
		self.title = 'Add Question'
		self.left = 230
		self.top = 90
		self.width = 900
		self.height = 480
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMaximizeButtonHint)

		self.Content()
		self.setLayout(self.mainlayout)
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())

	def Content(self):
		self.choiceList=[]
		self.choicewordwidget=[]
		self.mainlayout=QVBoxLayout()
		self.mainlayout.setSpacing(20)
		self.mainlayout.setContentsMargins(30, 20, 30, 30)
		layout=QHBoxLayout()
		self.mainlayout.addLayout(layout)
		self.addlayout=QVBoxLayout()
		uploadlayout=QVBoxLayout()

		layout.addLayout(self.addlayout,2)
		layout.addLayout(uploadlayout,1)

		questionspec=QGridLayout()
		self.addlayout.addLayout(questionspec)

		course=QComboBox()
		course.setEditable(True)
		questionspec.addWidget(course,0,1)
		course.setObjectName('questionspec')

		course_code=QComboBox()
		course_code.setEditable(True)
		questionspec.addWidget(course_code,0,2)
		course_code.setObjectName('questionspec')

		questiontype=QComboBox()
		questiontype.addItem('')
		questiontype.addItems(['Multiple choice','Filling the gap','No options'])
		questiontype.setEditable(True)
		questionspec.addWidget(questiontype,0,3)
		questiontype.setObjectName('questionspec')

		testtype=QComboBox()
		testtype.addItem('')
		testtype.addItems(['Exam','Test','Assignment'])
		testtype.setEditable(True)
		questionspec.addWidget(testtype,0,4)
		testtype.setObjectName('questionspec')

		year=QComboBox()
		year.setEditable(True)
		questionspec.addWidget(year,0,5)
		questionspec.setColumnStretch(6,6)
		year.setObjectName('questionspec')

		addquestion=QTextEdit()
		addquestion.setMaximumHeight(150)
		addquestion.setObjectName('questionspec')
		self.addlayout.addWidget(addquestion)
		self.choicelayout1=QGridLayout()
		self.choicelayout=QGridLayout()
		self.answerlayout=QGridLayout()
		self.answerlayout1=QGridLayout()

		self.addchoicebtn=QToolButton()
		self.addchoicebtn.setText(str('Add Choice'))
		self.addchoicebtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		self.addchoicebtn.setIcon(QIcon('image/add.ico'))
		self.addchoicebtn.setIconSize(QSize(80,35))
		self.addchoicebtn.setStyleSheet("border:0px solid green;")
		self.addchoicebtn.clicked.connect(self.AddChoice)

		self.addanswerbtn=QToolButton()
		self.addanswerbtn.setText(str('Add Answer'))
		self.addanswerbtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
		self.addanswerbtn.setIcon(QIcon('image/add.ico'))
		self.addanswerbtn.setIconSize(QSize(80,35))
		self.addanswerbtn.setStyleSheet("border:0px solid green;")
		self.addanswerbtn.clicked.connect(self.AddAnswer)

		self.addlayout.addLayout(self.answerlayout1)
		self.addlayout.addLayout(self.choicelayout1)
		self.addlayout.addLayout(self.choicelayout)
		self.addlayout.addLayout(self.answerlayout)
		self.addlayout.addWidget(self.addchoicebtn)
		self.addlayout.addWidget(self.addanswerbtn)

		

		self.addlayout.addStretch()
		self.answer=QComboBox()
		self.answer.insertItem(0,'')

		
	def AddChoice(self):
		self.addlayout.removeWidget(self.addchoicebtn)
		self.addchoicebtn.deleteLater()
		self.addchoicebtn= None

		self.addchoicebtn=QPushButton()
		self.addchoicebtn.setIcon(QIcon('image/add.ico'))
		self.addchoicebtn.setIconSize(QSize(80,35))
		self.addchoicebtn.setStyleSheet("border:0px solid green;")
		self.addchoicebtn.clicked.connect(self.SaveChoice)
		
		self.choice=QTextEdit()
		self.choice.setMaximumHeight(50)
		self.choice.setObjectName('questionspec')
		self.choicelayout.addWidget(self.choice,0,0)
		self.choicelayout.addWidget(self.addchoicebtn,0,1)

	def AddAnswer(self):
		self.addlayout.removeWidget(self.addanswerbtn)
		self.addanswerbtn.deleteLater()
		self.addanswerbtn= None

		
		self.answer.currentTextChanged.connect(self.SaveAnswer)
		
		self.answer.setEditable(True)
		self.answer.setObjectName('questionspec')
		self.answerlayout.addWidget(self.answer,0,0)
		self.answerlayout.addWidget(QLabel(''),0,1)	
		
	def SaveAnswer(self):
		answer=self.answer.currentText()
		if answer!='':
			self.answerlayout.removeWidget(self.answer)
			self.answer.deleteLater()
			self.answer= None

			self.editanswerbtn=QPushButton()
			self.editanswerbtn.setIcon(QIcon('image/edit.ico'))
			self.editanswerbtn.setIconSize(QSize(50,20))
			self.editanswerbtn.setStyleSheet("border:0px solid green;")
			self.editanswerbtn.clicked.connect(self.EditAnswer)
			
			self.choiceanswer=QLabel(answer)
			self.answerlayout1.addWidget(QLabel('Answer:'),0,0)
			self.answerlayout1.addWidget(self.choiceanswer,0,1)
			self.answerlayout1.addWidget(self.editanswerbtn,0,2)
			

	def SaveChoice(self):
		choice=self.choice.toPlainText()
		self.choice.setText('')
		letter=['A.','B.','C.','D.','E.','F.','G.']
		
		if choice!='' and len(self.choiceList)<=6:
			self.editchoicebtn=QPushButton()
			self.editchoicebtn.setIcon(QIcon('image/edit.ico'))
			self.editchoicebtn.setIconSize(QSize(50,20))
			self.editchoicebtn.setStyleSheet("border:0px solid green;")
			self.editchoicebtn.clicked.connect(partial(self.EditChoice,len(self.choiceList)))

			self.choicelabel=QLabel(letter[len(self.choiceList)])
			self.choiceword=QLabel(choice)
			self.choicelayout1.addWidget(self.choicelabel,len(self.choiceList),0)
			self.choicelayout1.addWidget(self.choiceword,len(self.choiceList),1)
			self.choicelayout1.addWidget(self.editchoicebtn,len(self.choiceList),2)
			self.choiceList.insert(len(self.choiceList)-1,choice)
			self.choicewordwidget.insert(len(self.choiceList)-1,self.choiceword)
			self.answer.insertItem(len(self.choiceList),letter[len(self.choiceList)-1])
	
	def EditChoice(self,row):
		self.choicelayout.removeWidget(self.choice)
		self.choice.deleteLater()
		self.choice= None

		self.choicelayout.removeWidget(self.addchoicebtn)
		self.addchoicebtn.deleteLater()
		self.addchoicebtn= None

		self.editchoicebtn=QPushButton()
		self.editchoicebtn.setIcon(QIcon('image/add.ico'))
		self.editchoicebtn.setIconSize(QSize(80,35))
		self.editchoicebtn.setStyleSheet("border:0px solid green;")
		self.editchoicebtn.clicked.connect(partial(self.SaveEditChoice,row))
		
		self.choice=QTextEdit(self.choicewordwidget[row].text())
		self.choice.setMaximumHeight(50)
		self.choice.setObjectName('questionspec')
		self.choicelayout1.addWidget(self.choice,row,1)
		self.choicelayout1.addWidget(self.editchoicebtn,row,2)

	def SaveEditChoice(self,row):
		choice=self.choice.toPlainText()
		self.choice.setText('')
		self.choicelayout1.removeWidget(self.editchoicebtn)
		self.editchoicebtn.deleteLater()
		self.editchoicebtn= None

		self.choicelayout1.removeWidget(self.choice)
		self.choice.deleteLater()
		self.choice= None
		self.choiceword=QLabel(choice)

		self.choicelayout1.removeWidget(self.choicewordwidget[row])
		self.choicewordwidget[row].deleteLater()
		self.choicewordwidget[row]= None

		self.choicelayout1.addWidget(self.choiceword,row,1)
		self.choicewordwidget.insert(row,self.choiceword)

		self.addchoicebtn=QPushButton()
		self.addchoicebtn.setIcon(QIcon('image/add.ico'))
		self.addchoicebtn.setIconSize(QSize(80,35))
		self.addchoicebtn.setStyleSheet("border:0px solid green;")
		self.addchoicebtn.clicked.connect(self.SaveChoice)
		
		self.choice=QTextEdit()
		self.choice.setMaximumHeight(50)
		self.choice.setObjectName('questionspec')
		self.choicelayout.addWidget(self.choice,0,0)
		self.choicelayout.addWidget(self.addchoicebtn,0,1)

	def EditAnswer(self,row):
		letter=['A.','B.','C.','D.','E.','F.','G.']
		answer=self.choiceanswer.text()
		self.answer=QComboBox()
		self.answer.insertItem(0,'')
		self.answer.addItems(letter[0:len(self.choiceList)-1])
		self.answer.setEditable(True)
		self.answer.addItems(letter[0:len(self.choiceList)])
		self.answer.setObjectName('questionspec')
		self.answer.setCurrentText(answer)

		
		self.answer.currentTextChanged.connect(self.SAveEditAnswer)

		self.answerlayout1.addWidget(self.answer,0,1)
		self.answerlayout1.addWidget(QLabel(''),0,2)

	def SAveEditAnswer(self):
		answer=self.answer.currentText()
		self.answerlayout1.removeWidget(self.answer)
		self.answer.deleteLater()
		self.answer= None
		self.answerlayout1.addWidget(answer,0,1)
		pass
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = AddQuestion()
	ex.show()
	sys.exit(app.exec_())
