# Dialog box for calculating agreement

import os

from PyQt5.QtCore import QCoreApplication, QMetaObject
from PyQt5.QtWidgets import (QDialog, QFileDialog, QHBoxLayout, QLabel,
                             QListWidget, QMessageBox, QPushButton,
                             QVBoxLayout)


class AgreementDialog(QDialog):
    """Popup dialog to calculate inter annotator agreement."""

    def __init__(self):
        super().__init__()

        self.setupUi()
        self.setupEvents()

    # Add annotation file to list widget
    def add_annoxml(self):
        filters = ['XML files(*.xml)', 'All files(*)']
        choosedialog = QFileDialog(None)
        choosedialog.setFileMode(QFileDialog.ExistingFiles)
        choosedialog.setViewMode(QFileDialog.Detail)
        choosedialog.setNameFilters(filters)
        choosedialog.exec()
        filepaths = choosedialog.selectedFiles()
        for file in filepaths:
            self.xmlfilepaths.append(file)
            self.listwidget_files.addItem(os.path.basename(file))

    # Remove item from list widget
    def listRemoveItem(self):
        self.xmlfilepaths.pop(self.listwidget_files.currentRow())
        self.listwidget_files.takeItem(self.listwidget_files.currentRow())

    # Function to start calculation
    def run_calc(self):
        numOfFiles = self.listwidget_files.count()
        if numOfFiles > 1:
            from interagreement import InterAgreement
            try:
                annoData = InterAgreement(self.xmlfilepaths)
                gammaval = annoData.compute_gamma()
                self.genMessage('Result', f'Inter-Annotator Agreement Value: \n {gammaval:.4f}')
            except:
                self.genMessage('Error', 'Error: Please check input files')
        else:
            self.genMessage('Error', 'Error: Please add at least 2 input files')

    # Message generator
    def genMessage(self, title='Message', content=''):
        messagebox = QMessageBox()
        messagebox.setWindowTitle(title)
        messagebox.setText(content)
        messagebox.exec()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(270, 170)

        self.v_layout = QVBoxLayout(self)
        self.listwidget_files = QListWidget()
        self.v_layout.addWidget(self.listwidget_files)
        self.infotext = QLabel()
        self.v_layout.addWidget(self.infotext)

        self.h_layout = QHBoxLayout()
        self.buttonAddFile = QPushButton()
        self.h_layout.addWidget(self.buttonAddFile)
        self.buttonCalculate = QPushButton()
        self.h_layout.addWidget(self.buttonCalculate)
        self.button_close = QPushButton()
        self.h_layout.addWidget(self.button_close)

        self.v_layout.addLayout(self.h_layout)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        self.xmlfilepaths = []

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Inter-Annotator Agreement"))
        self.buttonAddFile.setText(_translate("Dialog", "Add File"))
        self.buttonCalculate.setText(_translate("Dialog", "Calculate"))
        self.infotext.setText(_translate("Dialog", "Double-click to remove from list"))
        self.button_close.setText(_translate("Dialog", "Close"))

    def setupEvents(self):
        self.buttonAddFile.clicked.connect(self.add_annoxml)
        self.buttonCalculate.clicked.connect(self.run_calc)
        self.button_close.clicked.connect(self.reject)
        self.listwidget_files.itemDoubleClicked.connect(self.listRemoveItem)
