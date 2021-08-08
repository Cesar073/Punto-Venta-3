'''
Clase para botones de menúes de inicio
'''
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QAbstractAnimation
from PyQt5.QtWidgets import QPushButton, QSizePolicy

class Boton(QPushButton):
    def __init__(self, parent = None):
        QPushButton.__init__(self, parent)

        # Activamos el seguimiento del cursor cuando está sobre el boton
        self.setMouseTracking(True)

        # VARIABLES DEL BOTON CON UN VALOR POR DEFECTO, PERO QUE PUEDEN CAMBIARSE CON LAS FUNCIONES
        # Texto que tendrá el botón cuando se expande
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.Texto = "X"
        self.Texto_tam = 12
        self.Posx = 0
        self.Posy = 0
        self.Width = 60
        self.Height = 60
        self.setMaximumWidth = 200
        self.color_back = [85,85,85]
        self.color_hover = [35,35,35]
        self.setStyleSheet("border: 0px solid;")
        self.fuente = self.font()
        self.configura_boton(0,self.Texto, self.Texto_tam, self.Posx, self.Posy, self.Width, self.Height, True)


    def configura_boton(self, grosor_borde=(-1), texto =(-1), tam_texto=(-1), posx=(-1), posy=(-1), ancho=(-1), alto=(-1), config_color=False):
        if grosor_borde != (-1):
            self.setStyleSheet("border: {}px solid;".format(str(grosor_borde)))
        if texto != (-1):
            self.setText(texto)
            self.Texto = texto
        if tam_texto != (-1):
            self.fuente.setPointSize(tam_texto)
            self.Texto_tam = tam_texto
        pos1 = self.Posx
        pos2 = self.Posy
        tam1 = self.Width
        tam2 = self.Height
        cambiar = False
        if posx != (-1):
            cambiar = True
            pos1 = posx
            self.Posx = posx
        if posy != (-1):
            cambiar = True
            pos2 = posy
            self.Posy = posy
        if ancho != (-1):
            cambiar = True
            tam1 = ancho
            self.Whidth = ancho
        if alto != (-1):
            cambiar = True
            tam2 = alto
            self.Height = alto
        if cambiar == True:
            self.setGeometry(pos1, pos2, tam1, tam2)
        if config_color == True:
            self.setStyleSheet("background-color: rgb({},{},{});".format(str(self.color_back[0]),str(self.color_back[1]),str(self.color_back[2])))

    # Evento que se ejecuta cuando el cursor está encima del boton
    def enterEvent(self, event):
        self.setStyleSheet("background-color: rgb({},{},{});".format(self.color_hover[0], self.color_hover[1], self.color_hover[2]))

    # Evento que se ejecuta cuando el cursor deja de estar encima del boton
    def leaveEvent(self, event):
        self.setStyleSheet("background-color: rgb({},{},{});".format(self.color_back[0], self.color_back[1], self.color_back[2]))
        self.setStyleSheet("border: 0px solid;")



