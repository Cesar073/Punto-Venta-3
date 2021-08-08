from PyQt5.QtWidgets import QMainWindow
from vtn.vtn.vtn_buscar_prod import Ui_Buscar_Prod

class V_Buscar_Prod(QMainWindow):
    def __init__(self):
        super(V_Buscar_Prod, self).__init__()
        self.ui = Ui_Buscar_Prod()
        self.ui.setupUi(self)

    def Mostrar(self):
        self.show()
    