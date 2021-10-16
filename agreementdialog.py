# Dialog box for calculating agreement
from PyQt5.QtCore import QCoreApplication, QMetaObject
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QListWidget, QHBoxLayout, QFileDialog, QMessageBox

class agreement_dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 150)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QListWidget(Dialog)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.buttonAddFile = QPushButton(Dialog)
        self.buttonAddFile.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.buttonAddFile)

        self.buttonCalculate = QPushButton(Dialog)
        self.buttonCalculate.setObjectName("buttonCalculate")
        self.horizontalLayout_2.addWidget(self.buttonCalculate)

        self.buttonCancel = QPushButton(Dialog)
        self.buttonCancel.setObjectName("buttonCancel")
        self.horizontalLayout_2.addWidget(self.buttonCancel)
        
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)
        self.xmlfilepaths = []

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Inter-Annotator Agreement"))
        self.buttonAddFile.setText(_translate("Dialog", "Add File"))
        self.buttonCalculate.setText(_translate("Dialog", "Calculate"))
        self.buttonCancel.setText(_translate("Dialog", "Cancel"))

    def sig_slot_link(self, Dialog):
        self.buttonAddFile.clicked.connect(self.add_annoxml)
        self.buttonCalculate.clicked.connect(self.run_calc)
        self.buttonCancel.clicked.connect(Dialog.reject)
        self.listWidget.itemDoubleClicked.connect(self.listRemoveItem)

    def listRemoveItem(self):
        self.listWidget.takeItem(self.listWidget.currentRow())

    def add_annoxml(self):
        filters = ['XML files(*.xml)','All files(*)']
        choosedialog = QFileDialog(None)
        choosedialog.setFileMode(QFileDialog.ExistingFiles)
        choosedialog.setViewMode(QFileDialog.Detail)
        choosedialog.setNameFilters(filters)
        choosedialog.exec()
        filepaths = choosedialog.selectedFiles()
        for file in filepaths:
            self.xmlfilepaths.append(file)
            self.listWidget.addItem(self.getFileName(file))

    def genMessage(self, title = 'Message', content = ''):
        messagebox = QMessageBox()
        messagebox.setWindowTitle(title)
        messagebox.setText(content)
        messagebox.exec()

    def getFileName(self,path):
        i=-1
        while True:
            if path[i]!='/':
                i-=1
            else:
                return path[i+1:]

    def run_calc(self):
        numOfFiles = self.listWidget.count()
        if numOfFiles > 1:
            import interagreement
            '''filepaths=[]
            for i in range(self.listWidget.count()):
                pathitem = self.listWidget.item(i)
                pathstr = pathitem.text()
                filepaths.append(pathstr)'''
            try:
                annoData = interagreement.xmlCalc(self.xmlfilepaths)
                gammaval = annoData.computeGamma()
                self.genMessage('Result', f'Inter-Annotator Agreement Value: \n {gammaval:.4f}')
            except:
                self.genMessage('Error', 'Error: Please check input files')
        else:
            self.genMessage('Error', 'Error: Please add at least 2 input files')
