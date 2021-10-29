import os

from interagreement import InterAgreement
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

        self.xmlfilepaths = []

    # Add annotation file to list widget
    def button_add_file_clicked(self):
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

    # Start agreement calculation on files
    def button_calculate_clicked(self):
        numOfFiles = self.listwidget_files.count()
        if numOfFiles > 1:
            try:
                gammaval = InterAgreement.compute_gamma(self.xmlfilepaths)
                self.show_message('Result', f'Inter-Annotator Agreement Value: \n {gammaval:.4f}')
            except:
                self.show_message('Error', 'Error: Please check input files')
        else:
            self.show_message('Error', 'Error: Please add at least 2 input files')

    # Remove item from list widget
    def list_doubleclicked(self):
        self.xmlfilepaths.pop(self.listwidget_files.currentRow())
        self.listwidget_files.takeItem(self.listwidget_files.currentRow())

    # Message generator
    def show_message(self, title='Message', content=''):
        messagebox = QMessageBox()
        messagebox.setWindowTitle(title)
        messagebox.setText(content)
        messagebox.exec()

    def setupUi(self):
        self.resize(270, 170)

        self.v_layout = QVBoxLayout(self)
        self.listwidget_files = QListWidget()
        self.v_layout.addWidget(self.listwidget_files)
        self.infotext = QLabel()
        self.v_layout.addWidget(self.infotext)

        self.h_layout = QHBoxLayout()
        self.button_add_file = QPushButton()
        self.h_layout.addWidget(self.button_add_file)
        self.button_calculate = QPushButton()
        self.h_layout.addWidget(self.button_calculate)
        self.button_close = QPushButton()
        self.h_layout.addWidget(self.button_close)

        self.v_layout.addLayout(self.h_layout)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Inter-Annotator Agreement"))
        self.button_add_file.setText(_translate("Dialog", "Add File"))
        self.button_calculate.setText(_translate("Dialog", "Calculate"))
        self.infotext.setText(_translate("Dialog", "Double-click file name to remove.\nCalculation may take some time."))
        self.button_close.setText(_translate("Dialog", "Close"))

    def setupEvents(self):
        self.button_add_file.clicked.connect(self.button_add_file_clicked)
        self.button_calculate.clicked.connect(self.button_calculate_clicked)
        self.button_close.clicked.connect(self.close)
        self.listwidget_files.itemDoubleClicked.connect(self.list_doubleclicked)
