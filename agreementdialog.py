# Dialog box for calculating agreement
from PyQt5.QtCore import QCoreApplication, QMetaObject
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QListWidget, QHBoxLayout, QFileDialog, QMessageBox
from interagreement import xmlCalc

class agreement_dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(315, 263)
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

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
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

    def add_annoxml(self,Dialog):
        filters = ['XML files(*.xml)','Any files(*)']
        choosedialog = QFileDialog(None)
        choosedialog.setFileMode(QFileDialog.ExistingFiles)
        choosedialog.setViewMode(QFileDialog.Detail)
        choosedialog.setNameFilters(filters)
        choosedialog.exec()
        filepaths = choosedialog.selectedFiles()
        for file in filepaths:
            self.listWidget.addItem(file)

    def run_calc(self):
        filepaths=[]
        for i in range(self.listWidget.count()):
            pathitem = self.listWidget.item(i)
            pathstr = pathitem.text()
            filepaths.append(pathstr)
        annoData = xmlCalc(filepaths)
        gammaval = annoData.computeGamma()
        messagebox = QMessageBox()
        messagebox.setText(f'Inter-Annotator Agreement Value: \n {gammaval:.4f}')
        messagebox.exec()
