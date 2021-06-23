from PyQt5.QtWidgets import QMainWindow,QFormLayout,QTextEdit,QTabWidget,QListWidget,QAction,QTableWidget,QDialogButtonBox,QDialog,QAbstractItemView, QApplication,QPushButton,QLabel,QMessageBox,\
 QWidget,QVBoxLayout,QGridLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QColor
from PyQt5.QtCore import Qt, QDate,QDateTime
import sys,json,base64
from functools import partial
#from addsupplier import AddSupplier
	

class ViewApplicants(QMainWindow):
	def __init__(self,data, parent=None):
		super(ViewApplicants, self).__init__(parent)
		self.title = 'ViewApplicants'
		self.left = (self.x()+250)
		self.top = (self.x()+80)
		self.width = 950
		self.height = 600
		self.data=data
		self.keys={}

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
		 
		NewEntryButton = QAction(QIcon('exit24.png'), 'New Entry                    ', self)
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

		toolbar.addAction(self.addaccount)
		toolbar.addAction(self.edit)
		toolbar.addAction(self.delete)
		toolbar.addSeparator()
		
		self.addaccount.triggered.connect(self.AddNewSupplier)
		self.edit.triggered.connect(self.Edit)
		self.delete.triggered.connect(self.Delete)

		self.edit.setDisabled(True)
		self.delete.setDisabled(True)

	
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
		self.AddApplicant()	

	def SupplierList(self):
		self.widget=QWidget()
		self.mainlayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)
		self.table =QTableWidget()
		self.mainlayout.addWidget(self.table)

		self.SupplierTable()
		self.SupplierData()

	def SupplierTable(self):
		JournalHeader=["Surname","         Other        ","     Regno          ","   Password  ","   Phone  ","   Email"]
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
		self.table.doubleClicked.connect(self.TableAction)

	def SupplierData(self):
		
		rows=len(self.data)
		self.table.setRowCount(rows)
		self.table.resizeRowsToContents()
		rw=0
		for row in sorted(self.data):
			self.table.setItem(int(rw),0, QTableWidgetItem(self.data[row][0]))
			self.table.setItem(int(rw),1, QTableWidgetItem(self.data[row][1]))
			self.table.setItem(int(rw),2, QTableWidgetItem(self.data[row][2]))
			self.table.setItem(int(rw),3, QTableWidgetItem(self.data[row][3]))
			self.table.setItem(int(rw),4, QTableWidgetItem(self.data[row][4]))
			self.table.setItem(int(rw),5, QTableWidgetItem(self.data[row][5]))
			self.keys[rw]=row
			rw+=1
	
	def TableAction(self,item):
		
		row=item.row()
		self.delkey=row
		self.del_editDic={}
		
		if self.data.get(str(self.keys[row]), '') is not '':
			self.del_editDic[row]=self.data[self.keys[row]]		
		self.edit.setEnabled(True)
		self.delete.setEnabled(True)
		#print(self.requireddata[str(row)])	
	
	def AddApplicant(self):
		self.supplier_action='addsupplier'
		self.supplierid=''
	
		self.widget=QDialog()
		self.mainlayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)
		self.tabs = QTabWidget()
		self.mainlayout.addWidget(self.tabs)
		#self.tabs.currentChanged.connect(self.currentTab)

		self.supplier = QWidget()
		self.layout=QFormLayout()
		self.layout.setHorizontalSpacing(150)
		self.supplier.setLayout(self.layout)
		self.supplier.setStatusTip("Enter supplier information")
			
		self.tabs.addTab(self.supplier,"Applicant")

		self.surname=QLineEdit()
		self.surname.setPlaceholderText("Surname")
		self.othername=QLineEdit()
		self.othername.setPlaceholderText("Others")
		self.regno=QLineEdit()
		self.regno.setPlaceholderText("Registration number")
		self.password=QLineEdit()
		self.password.setPlaceholderText("password")
		self.category=QLineEdit()
		self.category.setPlaceholderText("category")
		self.phone=QLineEdit()
		self.phone.setPlaceholderText("+2347 055 224 987")
		self.email=QLineEdit()
		self.email.setPlaceholderText("ade.temi@sadetec.com")

		self.layout.addRow(QLabel("Surname:"),self.surname)
		self.layout.addRow(QLabel("Other name:"),self.othername)
		self.layout.addRow(QLabel("Reg No.:"),self.regno)
		self.layout.addRow(QLabel("Password:"),self.password)
		self.layout.addRow(QLabel("Category:"),self.category)
		self.layout.addRow(QLabel("Phone (primary):"),self.phone)
		self.layout.addRow(QLabel("Email:"),self.email)

		gridbutton=QGridLayout()
		self.ok=QPushButton('Save')
		self.ok.clicked.connect(self.Save)
		self.cancel=QPushButton('Cancel')
		self.cancel.clicked.connect(self.close)
		self.help=QPushButton('Help')
		gridbutton.addWidget(self.ok,0,0)
		gridbutton.addWidget(self.cancel,0,1)
		gridbutton.addWidget(self.help,0,2)

		buttonlayout=QFormLayout()
		buttonlayout.setHorizontalSpacing(200)
		buttonlayout.addRow(QLabel(),gridbutton)

		self.mainlayout.addLayout(buttonlayout)
		self.widget.exec_()



	def Save(self):
		surname=self.surname.text()
		othername=self.othername.text()
		regno=self.regno.text()
		password=self.password.text()
		category=self.category.text()
		phone=self.phone.text()
		email=self.email.text()
				
		postList=[]
		postList.append(surname)
		postList.append(othername)
		postList.append(regno)
		postList.append(password)
		postList.append(category)
		postList.append(phone)
		postList.append(email)

		postList=json.dumps(postList)
		postList=base64.b64encode(postList.encode())

		
		self.Server('addapplicant',postList,'applicants')

	def Server(self,action,postDic,url):
		
		self.ip=json.load(open("json/ipaddress.json", "r"))
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
		    if json_ar['result']=='addpplicants':
		    	print(1234567)
		    if json_ar['result']=='viewapplicants':
		    	self.applic=ViewApplicants(json_ar['data'])
		    	self.applic.show()
		    	self.close()	
		else:
		    #QMessageBox.critical(self, 'Databese Connection  ', "\n {}	 \n".format(reply.errorString())) 
		    print(reply.errorString())

class Applicants(QDialog):
	def __init__(self,data,parent=None):
		super(Applicants, self).__init__(parent)
		self.title = 'Results'
		self.left = 450
		self.top = 90
		self.width = 500
		self.height = 480
		self.data=data
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMaximizeButtonHint)

		self.Content()
		self.setLayout(self.mainlayout)
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())

		#self.ip=json.load(open("json/ipaddress.json", "r"))
		
	def Content(self):
		self.mainlayout=QVBoxLayout()
		self.mainlayout.setSpacing(20)
		self.mainlayout.setContentsMargins(10, 10, 10, 10)
		button=QPushButton('Add')
		button.clicked.connect(self.AddApplicant)
		self.mainlayout.addWidget(button)
		#button.setObjectName('viewresultbutton')

		self.setLayout(self.mainlayout)
		self.listwidget = QListWidget()
		self.mainlayout.addWidget(self.listwidget)
		#print(self.data)
		for row in self.data:
			self.listwidget.insertItem(int(row), self.data[row][0]+'  '+self.data[row][1])
			
		self.listwidget.clicked.connect(self.CheckResult)
		
	def AddApplicant(self):
		addapplicant=ViewApplicants({})
		addapplicant.AddApplicant()
		

	def CheckResult(self):
		row = self.listwidget.currentRow()
		self.postdata=self.data[str(row)]
		postDic=json.dumps(self.postdata)
		postDic=base64.b64encode(postDic.encode())
		self.Server('viewapplicants',postDic,'applicants')

	def Server(self,action,postDic,url):
		
		self.ip=json.load(open("json/ipaddress.json", "r"))
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
		    if json_ar['result']=='viewapplicants':
		    	self.applic=ViewApplicants(json_ar['data'])
		    	self.applic.show()
		    	self.close()	
		else:
		    #QMessageBox.critical(self, 'Databese Connection  ', "\n {}	 \n".format(reply.errorString())) 
		    print(reply.errorString())


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Applicants('')
	ex.show()
	sys.exit(app.exec_())
