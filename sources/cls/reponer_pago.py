from PyQt5.QtWidgets import QMainWindow
from vtn.vtn.vtn_reponer_pago import Ui_Reponer_Pago

class V_Reponer_Pago(QMainWindow):
    def __init__(self):
        super(V_Reponer_Pago, self).__init__()
        self.ui = Ui_Reponer_Pago()
        self.ui.setupUi(self)
    
    def Mostrar(self):
        self.show()