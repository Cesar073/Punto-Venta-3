from PyQt5.QtWidgets import QDialog
from vtn.vtn.vtn_peso_pcio import Ui_Dialog
import source.mod.form as form

class V_Carga_Valores(QDialog):
    def __init__(self):
        super(V_Carga_Valores, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowModality(2)
        self.ui.lineEdit.textChanged.connect(lambda: self.ui.lineEdit.setText(form.Line_Num_Coma_(self.ui.lineEdit.text())))

        self.Valor_Cargado = 0.0
        self.Titulo = ""
        self.Msj = ""
        self.Msj2 = "PRECIO:"

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def mostrar(self):
        self.setWindowTitle(self.Titulo)
        self.ui.label.setText(self.Msj)
        self.ui.label_2.setText(self.Msj2)
        self.show()
