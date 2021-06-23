import sys
import os
# import site
# site.addsitedir('/usr/local/lib/python2.7/site-packages')
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

app = QtWidgets.QApplication(sys.argv)
view = QtWebEngineWidgets.QWebEngineView()


port=json.load(open("json/port.json", "r"))
view.setUrl(QtCore.QUrl(f"http://127.0.0.1:{port}/admin"))

view.show()
sys.exit(app.exec_())