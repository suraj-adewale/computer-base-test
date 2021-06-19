from PyQt5.QtWidgets import QMainWindow,QDesktopWidget,QSplashScreen,QApplication,QDialog, QPushButton,QLabel,QSpinBox,QMessageBox,QRadioButton,\
 QWidget,QVBoxLayout,QHBoxLayout, QGridLayout,QGroupBox,QFormLayout,QComboBox,QLineEdit,QScrollArea,QDateEdit,QButtonGroup
from PyQt5.QtGui import QIcon,QPixmap,QImage,QPalette,QBrush
from PyQt5.QtCore import Qt, pyqtSignal,Qt,pyqtSlot,QDate,QSize
from PyQt5 import QtCore, QtNetwork,QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal,Qt,pyqtSlot,QDate,QSize,QTimer,QRunnable,QThreadPool
from settings import Settings
from dashboard import DashBoard
import PyQt5.sip
import os, sys,time,json,random,base64
#from server.routing import StartServer


class App(QMainWindow):
	resized = pyqtSignal()
	def __init__(self):
		super().__init__()	
		
		self.title = 'Login'
		self.left_ = 350
		self.top_ = 70
		self.width_ = 600
		self.height_ = 600
		sizeobject=QDesktopWidget().screenGeometry(-1)

		self.setWindowTitle(self.title)
		self.setGeometry(self.left_, self.top_, self.width_, self.height_)
		self.setStyleSheet(open("qss/mainstyle.qss", "r").read())
		self.resized.connect(self.reSizedFunction)
		ran=random.randint(1,7)
		
		self.scroll=QScrollArea()
		self.scrollwidget=QWidget(self.scroll)
		self.scroll.setWidgetResizable(True)
		#self.showMaximized()
		oImage = QImage("image/bg{}.jpg".format(ran))
		sImage = oImage.scaled(QSize(sizeobject.width(),sizeobject.height())) 
		    
		self.palette = QPalette()
		self.palette.setBrush(10, QBrush(sImage)) 
		self.scroll.setPalette(self.palette)

		self.LoginContent()
		self.setCentralWidget(self.widget)
		self.Connection("",'test_conn')
	def resizeEvent(self, event):
		self.resized.emit()
		return super(App, self).resizeEvent(event)

	def LoginContent(self):	
		self.widget=QWidget()

		self.mainlayout=QVBoxLayout()
		self.widget.setLayout(self.mainlayout)
		self.mainlayout.setSpacing(0)
		self.mainlayout.setContentsMargins(0, 0, 0, 0)
		self.mainlayout.addWidget(self.scroll)
		
		self.scrollwidget.setStyleSheet("background-color: rgba(10, 10, 10, 100);position:20px;border-radius: 6px;")
		#self.scrollwidget.setFixedSize(250, 180)
		self.scrollwidget.resize(350, 200)
		
		self.LoginForm()
		self.scrollwidget.setLayout(self.formlayout)		
	
	def reSizedFunction(self):
		hpos = (self.width()-250) / 2
		self.scrollwidget.move(hpos,100)
		
	def LoginForm(self):
		self.formlayout =QGridLayout()
		#setColumnStretch(3, 1)#setColumnStretch(0, 1)#addStretch(1)
		self.formlayout.setVerticalSpacing(20)
		self.admin=ClickableLabel()
		self.admin.clicked.connect(self.SetIpAddress)
		self.admin.setText('<a href="/none/" style="color:green;">admin</a>')
		self.admin.setStyleSheet("background-color: none; margin-left:190px;")
		self.admin.setObjectName('admin')
		self.username=QLineEdit()
		self.Password=QLineEdit()
		self.submit=QPushButton()
		self.submit.setText('No connection')
		self.submit.setEnabled(False)
		self.Password.setEchoMode(QLineEdit.Password)
		self.username.setPlaceholderText('Reg no.')
		self.Password.setPlaceholderText('********')
		self.formlayout.addWidget(self.admin,0,0,1,2)
		self.formlayout.addWidget(self.username,1,0,1,2)
		self.formlayout.addWidget(self.Password, 2,0,1,2)

		self.formlayout.addWidget(self.submit, 3,0,1,2)
		self.username.setStyleSheet("font-size:15px;color:#00c6ff;background-color: white;")
		self.username.setObjectName('signlineedit')
		self.Password.setObjectName('signlineedit')
		self.Password.setStyleSheet("font-size:15px;color:#00c6ff;background-color: white;")
		self.submit.setObjectName('signinbutton')
		self.submit.setStyleSheet("padding:2px;font-size:18px;background-color:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                      stop: 0 #f6f7fa, stop: 1 #00c6ff);")
		#self.username.setMaximumWidth(300)
		#self.Password.setMaximumWidth(300)
		#self.submit.setMaximumWidth(50)
		
		self.submit.clicked.connect(self.SignIn)

	def SetIpAddress(self):
		self.ipdialog=Settings(self)
		self.ipdialog.exec_()
		self.Connection("",'test_conn')

	def SignIn(self):
		
		postDic={}
		usern=self.username.text()
		passw=self.Password.text()
		if usern=='' and passw=='':
			QMessageBox.about(self, 'Login', "   \nPlease enter your user name and password\n   ")
			return False
		if  passw=='':
			QMessageBox.about(self, 'Password ', "\nPlease enter your password\n   ")
			return False
		if usern=='':
			QMessageBox.about(self, 'User name ', "\nPlease enter your user name\n   ")
			return False
		
		postDic['regno']=usern
		postDic['password']=passw
		postDic=json.dumps(postDic)
		postDic=base64.b64encode(postDic.encode())
		#postDic=postDic.decode("utf-8")
		self.Connection(postDic, 'login')

	def Connection(self, postDic,path):
		self.ip=json.load(open("json/ipaddress.json", "r"))
		data = QtCore.QByteArray()
		data.append("action=login&")
		if postDic!="":
			data.append("data={}".format(postDic.decode("utf-8")))
		url = "http://{}/{}".format(self.ip, path)
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

	        if json_ar['login'] == 'connected':
	        	self.submit.setEnabled(True)
	        	self.submit.setText('Login')
	        if json_ar['login']==1:
	        	self.dashboard=DashBoard(json_ar['data'])
        		self.dashboard.show()
        	if json_ar['login']==22:
        		QMessageBox.critical(self, 'Login Error', "\n{}		".format(json_ar['reason']))	
	    else:
	        QMessageBox.critical(self, 'Databese Connection  ', "\n {}		\n".format(reply.errorString()))		

			
			
class Worker(QRunnable):
    @pyqtSlot()
    def run(self):

        StartServer()
        while True:
        	time.sleep(1)	

class ClickableLabel(QLabel):
	clicked=pyqtSignal()
	def mousePressEvent(self,event):
		if event.button()==Qt.LeftButton: self.clicked.emit()


if __name__ == '__main__':
	sys.argv.append('--disable-web-security') 
	app = QApplication(sys.argv)
	ex = App()
	ex.show()
	sys.exit(app.exec_())

