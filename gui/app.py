from PyQt6 import uic, QtWidgets

def chama_tela():
    cad.show()

app = QtWidgets.QApplication([])
cadModulo = uic.loadUi("cadModulo.ui")
cad = uic.loadUi("cad.ui")
cadModulo.pushButton.clicked.connect(chama_tela)

cadModulo.show()
app.exec()
