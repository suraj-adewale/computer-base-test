import sys
from PyQt5.QtWidgets import QApplication, QDialog,QGridLayout,QPushButton, QLineEdit, QFileDialog,QMessageBox
import pandas as pd
import sqlite3
class UpLoad(QDialog):

    def __init__(self,table_name):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 500
        self.top = 150
        self.width = 400
        self.height = 90

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Upload')

        layout=QGridLayout()
        self.setLayout(layout)
        self.textbox = QLineEdit()
        self.btn1=QPushButton('Browse')
        self.btn=QPushButton('Save')
        self.btn.clicked.connect(self.Save)
        self.btn1.clicked.connect(self.Browse)
        
        layout.addWidget(self.textbox,0,0,1,4)
        layout.addWidget(self.btn1,0,3)
        layout.addWidget(self.btn,0,4)

        self.table_name = table_name


    def Save(self):
        try:
            conn = sqlite3.connect('server/database/cbt.db')
            df = pd.read_excel(f'{self.file}')
            df.to_sql(name=self.table_name, con=conn,if_exists='append', index=False)

            msg=QMessageBox()
            msg.setWindowTitle('Success')
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet("QLabel{min-width:250px;margin:2px;}")
            msg.setInformativeText("<div style='font-size:15px; color:green'>SQL insert process finished</div>")
            self.close()
            msg.exec_()
            self.close()
        except Exception as e:
            msg=QMessageBox()
            msg.setWindowTitle('Error')
            msg.setIcon(QMessageBox.Critical)
            msg.setStyleSheet("QLabel{min-width:250px;margin:2px;}")
            msg.setInformativeText(f"<div style='font-size:15px; color:red'>{e}</div>")
            self.close()
            msg.exec_()

    
    def Browse(self):
        fileName = QFileDialog.getOpenFileName(self, 'OpenFile')
        self.file = fileName[0]
        self.textbox.setText(self.file)
   
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UpLoad('register')
    ex.show()
    sys.exit(app.exec_())