# Form implementation generated from reading ui file 'cad-lte.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1060, 560)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_cid_mod = QtWidgets.QFrame(self.centralwidget)
        self.frame_cid_mod.setGeometry(QtCore.QRect(10, 60, 1041, 81))
        self.frame_cid_mod.setStyleSheet("background-color: rgb(171, 196, 223);")
        self.frame_cid_mod.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_cid_mod.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_cid_mod.setObjectName("frame_cid_mod")
        self.btn_salvar_mod = QtWidgets.QPushButton(self.frame_cid_mod)
        self.btn_salvar_mod.setGeometry(QtCore.QRect(820, 30, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_salvar_mod.setFont(font)
        self.btn_salvar_mod.setObjectName("btn_salvar_mod")
        self.label_cidade_2 = QtWidgets.QLabel(self.frame_cid_mod)
        self.label_cidade_2.setEnabled(True)
        self.label_cidade_2.setGeometry(QtCore.QRect(90, 10, 58, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_cidade_2.setFont(font)
        self.label_cidade_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_cidade_2.setObjectName("label_cidade_2")
        self.label_12 = QtWidgets.QLabel(self.frame_cid_mod)
        self.label_12.setGeometry(QtCore.QRect(550, 10, 78, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.cbo_cidade = QtWidgets.QComboBox(self.frame_cid_mod)
        self.cbo_cidade.setGeometry(QtCore.QRect(90, 30, 251, 31))
        self.cbo_cidade.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cbo_cidade.setEditable(True)
        self.cbo_cidade.setObjectName("cbo_cidade")
        self.cbo_cidade.addItem("")
        self.cbo_cidade.setItemText(0, "")
        self.cbo_cidade.addItem("")
        self.cbo_cidade.addItem("")
        self.cbo_modulo = QtWidgets.QComboBox(self.frame_cid_mod)
        self.cbo_modulo.setGeometry(QtCore.QRect(550, 30, 210, 31))
        self.cbo_modulo.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cbo_modulo.setEditable(True)
        self.cbo_modulo.setObjectName("cbo_modulo")
        self.cbo_modulo.addItem("")
        self.cbo_modulo.setItemText(0, "")
        self.cbo_modulo.addItem("")
        self.cbo_modulo.addItem("")
        self.cbo_modulo.addItem("")
        self.cbo_modulo.addItem("")
        self.frame_desc = QtWidgets.QFrame(self.centralwidget)
        self.frame_desc.setGeometry(QtCore.QRect(9, 10, 1041, 48))
        self.frame_desc.setStyleSheet("background-color: rgb(76, 121, 183);")
        self.frame_desc.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_desc.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_desc.setObjectName("frame_desc")
        self.text_top = QtWidgets.QLabel(self.frame_desc)
        self.text_top.setGeometry(QtCore.QRect(0, 10, 1041, 28))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(False)
        self.text_top.setFont(font)
        self.text_top.setStyleSheet("color: rgb(255, 255, 255);")
        self.text_top.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.text_top.setScaledContents(False)
        self.text_top.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_top.setObjectName("text_top")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setGeometry(QtCore.QRect(10, 150, 1041, 401))
        self.toolBox.setObjectName("toolBox")
        self.frequencia = QtWidgets.QWidget()
        self.frequencia.setGeometry(QtCore.QRect(0, 0, 1041, 347))
        self.frequencia.setObjectName("frequencia")
        self.table = QtWidgets.QTableWidget(self.frequencia)
        self.table.setGeometry(QtCore.QRect(0, 230, 931, 121))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.table.setFont(font)
        self.table.setStyleSheet("background-color: rgb(171, 196, 223);")
        self.table.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
        self.table.setWordWrap(True)
        self.table.setRowCount(0)
        self.table.setObjectName("table")
        self.table.setColumnCount(13)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(12, item)
        self.frame_3 = QtWidgets.QFrame(self.frequencia)
        self.frame_3.setGeometry(QtCore.QRect(940, 230, 101, 121))
        self.frame_3.setStyleSheet("background-color: rgb(171, 196, 223);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_4.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.frame_freq = QtWidgets.QFrame(self.frequencia)
        self.frame_freq.setEnabled(False)
        self.frame_freq.setGeometry(QtCore.QRect(0, 0, 1041, 221))
        self.frame_freq.setStyleSheet("background-color: rgb(171, 196, 223);")
        self.frame_freq.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_freq.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_freq.setObjectName("frame_freq")
        self.label_SIB3CELLID = QtWidgets.QLabel(self.frame_freq)
        self.label_SIB3CELLID.setGeometry(QtCore.QRect(816, 115, 65, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_SIB3CELLID.setFont(font)
        self.label_SIB3CELLID.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_SIB3CELLID.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";\n"
"\n"
"color: rgb(0, 0, 0);")
        self.label_SIB3CELLID.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_SIB3CELLID.setObjectName("label_SIB3CELLID")
        self.label_fcn = QtWidgets.QLabel(self.frame_freq)
        self.label_fcn.setGeometry(QtCore.QRect(10, 120, 23, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_fcn.setFont(font)
        self.label_fcn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_fcn.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";\n"
"\n"
"color: rgb(0, 0, 0);")
        self.label_fcn.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_fcn.setObjectName("label_fcn")
        self.label_8 = QtWidgets.QLabel(self.frame_freq)
        self.label_8.setGeometry(QtCore.QRect(614, 115, 18, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_8.setFont(font)
        self.label_8.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_8.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";\n"
"\n"
"color: rgb(0, 0, 0);")
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.label_mcc = QtWidgets.QLabel(self.frame_freq)
        self.label_mcc.setGeometry(QtCore.QRect(210, 120, 26, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_mcc.setFont(font)
        self.label_mcc.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_mcc.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";\n"
"\n"
"color: rgb(0, 0, 0);")
        self.label_mcc.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_mcc.setObjectName("label_mcc")
        self.label_freq = QtWidgets.QLabel(self.frame_freq)
        self.label_freq.setEnabled(False)
        self.label_freq.setGeometry(QtCore.QRect(-2, 10, 1041, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_freq.setFont(font)
        self.label_freq.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_freq.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_freq.setObjectName("label_freq")
        self.label_mnc = QtWidgets.QLabel(self.frame_freq)
        self.label_mnc.setGeometry(QtCore.QRect(413, 120, 26, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_mnc.setFont(font)
        self.label_mnc.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_mnc.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";\n"
"\n"
"color: rgb(0, 0, 0);")
        self.label_mnc.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_mnc.setObjectName("label_mnc")
        self.btn_inserir = QtWidgets.QPushButton(self.frame_freq)
        self.btn_inserir.setEnabled(False)
        self.btn_inserir.setGeometry(QtCore.QRect(700, 181, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_inserir.setFont(font)
        self.btn_inserir.setStyleSheet("color: rgb(0, 0, 0);")
        self.btn_inserir.setObjectName("btn_inserir")
        self.btn_salvar_freq = QtWidgets.QPushButton(self.frame_freq)
        self.btn_salvar_freq.setGeometry(QtCore.QRect(816, 181, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_salvar_freq.setFont(font)
        self.btn_salvar_freq.setStyleSheet("color: rgb(0, 0, 0);")
        self.btn_salvar_freq.setObjectName("btn_salvar_freq")
        self.cbo_cidade_2 = QtWidgets.QComboBox(self.frame_freq)
        self.cbo_cidade_2.setEnabled(False)
        self.cbo_cidade_2.setGeometry(QtCore.QRect(10, 70, 241, 28))
        self.cbo_cidade_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cbo_cidade_2.setEditable(True)
        self.cbo_cidade_2.setObjectName("cbo_cidade_2")
        self.cbo_cidade_2.addItem("")
        self.cbo_cidade_2.setItemText(0, "")
        self.cbo_cidade_2.addItem("")
        self.cbo_cidade_2.addItem("")
        self.cbo_cidade_2.addItem("")
        self.cbo_cidade_2.addItem("")
        self.label_cidade = QtWidgets.QLabel(self.frame_freq)
        self.label_cidade.setEnabled(False)
        self.label_cidade.setGeometry(QtCore.QRect(10, 50, 39, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_cidade.setFont(font)
        self.label_cidade.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_cidade.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_cidade.setObjectName("label_cidade")
        self.splitter_2 = QtWidgets.QSplitter(self.frame_freq)
        self.splitter_2.setGeometry(QtCore.QRect(10, 144, 1001, 28))
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.lineEdit_fcn = QtWidgets.QLineEdit(self.splitter_2)
        self.lineEdit_fcn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_fcn.setObjectName("lineEdit_fcn")
        self.lineEdit_mcc = QtWidgets.QLineEdit(self.splitter_2)
        self.lineEdit_mcc.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_mcc.setObjectName("lineEdit_mcc")
        self.lineEdit_mnc = QtWidgets.QLineEdit(self.splitter_2)
        self.lineEdit_mnc.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_mnc.setObjectName("lineEdit_mnc")
        self.lineEdit_lai = QtWidgets.QLineEdit(self.splitter_2)
        self.lineEdit_lai.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_lai.setObjectName("lineEdit_lai")
        self.lineEdit_SIB3CELLID = QtWidgets.QLineEdit(self.splitter_2)
        self.lineEdit_SIB3CELLID.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_SIB3CELLID.setObjectName("lineEdit_SIB3CELLID")
        self.toolBox.addItem(self.frequencia, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 1041, 347))
        self.page_4.setObjectName("page_4")
        self.toolBox.addItem(self.page_4, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_salvar_mod.setText(_translate("MainWindow", "Salvar"))
        self.label_cidade_2.setText(_translate("MainWindow", "Cidade"))
        self.label_12.setText(_translate("MainWindow", "Módulo"))
        self.cbo_cidade.setItemText(1, _translate("MainWindow", "São Paulo"))
        self.cbo_cidade.setItemText(2, _translate("MainWindow", "Campinas"))
        self.cbo_modulo.setItemText(1, _translate("MainWindow", "Módulo B1"))
        self.cbo_modulo.setItemText(2, _translate("MainWindow", "Módulo B3"))
        self.cbo_modulo.setItemText(3, _translate("MainWindow", "Módulo B7"))
        self.cbo_modulo.setItemText(4, _translate("MainWindow", "Módulo B28"))
        self.text_top.setText(_translate("MainWindow", "Cadastro XML - LTE"))
        self.table.setSortingEnabled(False)
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Id Operadora"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Nome da operadora"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "id"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "arfcn"))
        item = self.table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "mcc"))
        item = self.table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "mnc"))
        item = self.table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "lai"))
        item = self.table.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "sib3CellId"))
        item = self.table.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "bsic "))
        item = self.table.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "cro"))
        item = self.table.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", "rxLevAccMin"))
        item = self.table.horizontalHeaderItem(11)
        item.setText(_translate("MainWindow", "reselctHyst"))
        item = self.table.horizontalHeaderItem(12)
        item.setText(_translate("MainWindow", "nbFreq"))
        self.pushButton_3.setText(_translate("MainWindow", "Editar"))
        self.label_SIB3CELLID.setText(_translate("MainWindow", "SIB3CELLID"))
        self.label_fcn.setText(_translate("MainWindow", "FCN"))
        self.label_8.setText(_translate("MainWindow", "LAI"))
        self.label_mcc.setText(_translate("MainWindow", "MCC"))
        self.label_freq.setText(_translate("MainWindow", "Frequencia da Operadora"))
        self.label_mnc.setText(_translate("MainWindow", "MNC"))
        self.btn_inserir.setText(_translate("MainWindow", "Inserir"))
        self.btn_salvar_freq.setText(_translate("MainWindow", "Salvar"))
        self.cbo_cidade_2.setItemText(1, _translate("MainWindow", "Oi"))
        self.cbo_cidade_2.setItemText(2, _translate("MainWindow", "Claro"))
        self.cbo_cidade_2.setItemText(3, _translate("MainWindow", "Vivo"))
        self.cbo_cidade_2.setItemText(4, _translate("MainWindow", "Tim"))
        self.label_cidade.setText(_translate("MainWindow", "Cidade"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.frequencia), _translate("MainWindow", "Frequencia"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("MainWindow", "Page 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
