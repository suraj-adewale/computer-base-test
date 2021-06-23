from PyQt5.QtWidgets import QPushButton,QAction,QListWidget,QToolButton,QListWidget,QDialogButtonBox,QDialog,QAbstractItemView,QTableWidget,QTextEdit,QLabel,QCompleter,QTableWidgetItem,\
QMessageBox,QApplication,QMainWindow, QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtCore import Qt, QDate,QDateTime,QSize
from PyQt5.QtGui import QIcon,QPixmap
from functools import partial
from server.result import Result
import os, sys,time,json,random,base64,math


class ViewResults(QMainWindow):
	def __init__(self,data, parent=None):
		super(ViewResults, self).__init__(parent)
		self.title = 'ViewResults'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		self.data=data['data']
		self.total={}

		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.initmenu()

		self.SupplierList()
		self.setCentralWidget(self.widget)

	def initmenu(self):
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
			 
		mainMenu = self.menuBar()
		Journal = mainMenu.addMenu('Journal')
		homeMenu = mainMenu.addMenu('Report')
		homeMenu = mainMenu.addMenu('Help')
		 
		NewEntryButton = QAction(QIcon('exit24.png'), 'New Entry', self)
		NewEntryButton.setShortcut('Ctrl+N')
		NewEntryButton.setStatusTip('New Journal')
		NewEntryButton.triggered.connect(self. AddNewSupplier)

		Editbutton = QAction(QIcon('exit24.png'), 'Edit Entry', self)
		Editbutton.setDisabled(True)
		Editbutton.setShortcut('Enter')

		Deletebutton = QAction(QIcon('exit24.png'), 'Delete Entry', self)
		Deletebutton.setDisabled(True)
		Deletebutton.setShortcut('Cltl+Delete')

		Findbutton = QAction(QIcon('exit24.png'), 'Find Entry', self)
		Findbutton.setDisabled(True)
		Findbutton.setShortcut('Cltl+F')

		Findnextbutton = QAction(QIcon('exit24.png'), 'Find Next Entry', self)
		Findnextbutton.setDisabled(True)
		Findnextbutton.setShortcut('Cltl+N')
		
		exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
		exitButton.setShortcut('Ctrl+Q')
		exitButton.setStatusTip('Exit application')
		exitButton.triggered.connect(self.close)

		self.statusBar()
		
		Journal.addAction(NewEntryButton)
		Journal.addAction(Editbutton)
		Journal.addAction(Deletebutton)
		Journal.addSeparator()
		Journal.addAction(Findbutton)
		Journal.addAction(Findnextbutton)
		Journal.addSeparator()
		Journal.addAction(exitButton)

		toolbar = self.addToolBar('Exit')
		toolbar.setObjectName('toolbar')

		self.addaccount= QAction(QIcon('image/add.ico'), 'Add Account', self)
		self.edit= QAction(QIcon('image/edit.ico'), 'Edit Account', self)
		self.delete= QAction(QIcon('image/delete.ico'), 'Delete Account', self)
		self.save= QAction(QIcon('image/save.ico'), 'Save in Excel format', self)

		toolbar.addAction(self.addaccount)
		toolbar.addAction(self.edit)
		toolbar.addAction(self.delete)
		toolbar.addSeparator()
		toolbar.addAction(self.save)
		
		self.addaccount.triggered.connect(self.AddNewSupplier)
		self.save.triggered.connect(self.Save)
		self.edit.triggered.connect(self.Edit)
		self.delete.triggered.connect(self.Delete)

		self.edit.setDisabled(True)
		self.delete.setDisabled(True)

	def Save(self):
		import xlsxwriter
		# Create a workbook and add a worksheet.
		file=self.filename.replace(' ','')
		file=file.replace('/','')

		workbook = xlsxwriter.Workbook('{}.xlsx'.format(file))
		worksheet = workbook.add_worksheet()

		bold = workbook.add_format({'bold': 1})
		cell_format = workbook.add_format({'bold': True, 'italic': True, 'color': 'red'})
		worksheet.set_column(1, 2, 15)

		JournalHeader=["Registration no.","    Subject(s)     ","  Aggregate   ","  category","   Test Type  ","Year"]
		for item in JournalHeader:
			worksheet.write(0,JournalHeader.index(item),item,bold)

		rw=1
		for row in sorted(self.data):
			worksheet.write(int(rw),0,row)
			aggr=self.total[rw-1]
			subjects=(self.data[row][0])
			subjects=str(subjects).replace('{','')
			subjects=str(subjects).replace('}','')
			
			worksheet.write(int(rw),1,subjects)
			worksheet.write(int(rw),2,str(aggr))
			worksheet.write(int(rw),3,'')
			worksheet.write(int(rw),4,self.data[row][2])
			worksheet.write(int(rw),5,self.data[row][3])
			rw+=1
		file=self.filename.replace(' ','')
		file=file.replace('/','')	
		os.system("start EXCEL.EXE {}.xlsx".format(file))	
		workbook.close()
	def Edit(self):

		self.suppl=AddSupplier({'widget':self,'data':self.del_editDic[self.delkey]})
		self.suppl.show()
		
	
	def Delete(self):
		self.dialog=QDialog(self)
		self.dialog.setWindowTitle("New Template")
		layout=QVBoxLayout()
		self.dialog.setLayout(layout)
		label=QLabel("\n Are you sure you want to delete selected Supplier {} at row {}\n\n".\
			format(self.del_editDic[self.delkey][0],self.delkey+1))
		
		layout.addWidget(label)
		buttonbox = QDialogButtonBox(QDialogButtonBox.Yes|QDialogButtonBox.No)
		layout.addWidget(buttonbox)

		buttonbox.accepted.connect(partial(self.DeleteNow,self.del_editDic[self.delkey][2]))
		buttonbox.rejected.connect(self.dialog.close)
		self.dialog.exec_()

	def DeleteNow(self,supplierid):
		self.ServerAction(supplierid)

	def AddNewSupplier(self):
		pass
		#self.AddApplicant()	

	def SupplierList(self):
		self.widget=QWidget()
		self.mainlayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)
		self.table =QTableWidget()
		self.mainlayout.addWidget(self.table)

		self.SupplierTable()
		self.SupplierData()

	def SupplierTable(self):
		JournalHeader=["Registration no.","    Subject(s)     ","  Aggregate   ","  category","   Type  ","Year"]
		self.table.setColumnCount(6)     #Set three expense
		
		self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
		header = self.table.horizontalHeader()
		
		header.setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
		
		self.table.setSelectionMode(QAbstractItemView.MultiSelection)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.table.setShowGrid(True)
		self.table.setHorizontalHeaderLabels(JournalHeader)	
		#self.table.doubleClicked.connect(self.TableAction)

	def SupplierData(self):
		
		rows=len(self.data)
		self.table.setRowCount(rows)
		self.table.resizeRowsToContents()
		rw=0

		print(self.data)
		for row in sorted(self.data):
			self.table.setItem(int(rw),0, QTableWidgetItem(row))
			aggr=self.data[row][0]['total']
			subjects=(self.data[row][0])
			subjects.pop('total')
			subjects=str(subjects).replace('{','')
			subjects=str(subjects).replace('}','')
			
			self.table.setItem(int(rw),1, QTableWidgetItem(subjects))
			self.table.setItem(int(rw),2, QTableWidgetItem(str(aggr)))
			self.table.setItem(int(rw),3, QTableWidgetItem(''))
			self.table.setItem(int(rw),4, QTableWidgetItem(self.data[row][2]))
			self.table.setItem(int(rw),5, QTableWidgetItem(self.data[row][3]))
			self.total[rw]=aggr
			rw+=1
		filename=self.data[row]
		self.filename=str((filename[1]).replace('&',''))+str(filename[2])+str(filename[3])

class TestResults(QDialog):
	def __init__(self,data,parent=None):
		super(TestResults, self).__init__(parent)
		self.title = 'Results'
		self.left = 450
		self.top = 90
		self.width = 500
		self.height = 480
		self.data=data['cat']
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMaximizeButtonHint)

		self.Content()
		self.setLayout(self.mainlayout)
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())

		#self.ip=json.load(open("json/ipaddress.json", "r"))
		self.ip='localhost'

	def Content(self):
		self.mainlayout=QVBoxLayout()
		self.mainlayout.setSpacing(20)
		self.mainlayout.setContentsMargins(10, 10, 10, 10)
		button=QPushButton('UTME')
		self.mainlayout.addWidget(button)
		#button.setObjectName('viewresultbutton')

		self.setLayout(self.mainlayout)
		self.listwidget = QListWidget()
		self.mainlayout.addWidget(self.listwidget)

		
		for row in self.data:
			self.listwidget.insertItem(int(row), self.data[row][0]+'  '+self.data[row][1]+'			'+self.data[row][2])
			
		self.listwidget.clicked.connect(self.CheckResult)
		

	def CheckResult(self):
		row= self.listwidget.currentRow()
		self.postdata=self.data[row]
		self.results=ViewResults(Result('CheckResult', self.postdata))
		self.results.show()

	def Server(self,action,postDic,url):
		data = QtCore.QByteArray()
		data.append("action={}&".format(action))
		data.append("data={}".format(postDic.decode("utf-8")))
		url = "http://{}:5000/{}".format(self.ip,url)
		req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
		req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 
		    "application/x-www-form-urlencoded")
		self.nam = QtNetwork.QNetworkAccessManager()
		self.nam.finished.connect(self.handleResponse)
		self.nam.post(req, data)

	def handleResponse(self, reply):
		er = reply.error()
		if er == QtNetwork.QNetworkReply.NoError:
		    bytes_string = reply.readAll()
		    json_ar = json.loads(str(bytes_string, 'utf-8'))
		    
		    self.close()
		else:
		    #QMessageBox.critical(self, 'Databese Connection  ', "\n {}	 \n".format(reply.errorString())) 
		    print(reply.errorString())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = TestResults({})
	ex.show()
	sys.exit(app.exec_())		