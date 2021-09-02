#import platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QInputDialog, QFrame

# Clase que convierte un Label en un botón
class QlabelClickeable(QLabel):

    # "clicked" es un evento que lo nombré así sólo porque en los botones se llama así y mantengo el nombre, pero podría ponerle cualquier nombre. Cuando se presiona el label, se emite una señal a éste evento entonces cuando tengamos que conectarlo a una función, hacemos igual que los botones ej: self.label.clicked.connect(self.funcion).
    # En PyQt5 ésta misma sintaxis sería: clicked = QtCore.pyqtSignal(str)
    # El parámetro str, es un valor que puede utilizarse para reconocer el botón que se ha presionado por ejemplo.
    clicked = QtCore.pyqtSignal(str)

    flotar = QtCore.pyqtSignal(bool)
    retirar = QtCore.pyqtSignal(bool)

    def __init__(self, Texto, pos, fondo = 0, parent=None):
        super(QlabelClickeable, self).__init__(parent)

        # Una lista que contiene adentro listas de 3 números enteros (RGB) de los colores que queremos tener para cada evento.
        # Luego tiene una lista con varios valores para configurar otros atributos.
            # pos0 = Color normal
            # pos1 = Color boton apretado
            # pos2 = Color mouse hover
            # pos3 = grosor del borde normal / apretado / hover
            # pos4 = color del borde normal
            # pos5 = color del borde apretado
            # pos6 = color del borde hover
            # pos7 = width/height boton normal
            # pos8 = width/height boton expandido
            # pos9 = Texto del boton normal/apretado/hover
            # pos10 = Texto de ToolTip

        self.lista_val = []
        if fondo == 0:
            self.lista_val.append([255,255,255])        # 0
        else:
            self.lista_val.append([210,210,230])        # 0
        self.lista_val.append([200,200,200])            # 1
        self.lista_val.append([200,200,200])            # 2
        self.lista_val.append([0,0,0])                  # 3
        self.lista_val.append([85,85,85])               # 4
        self.lista_val.append([0,0,0])                  # 5
        self.lista_val.append([0,0,0])                  # 6
        self.lista_val.append([80,60])                  # 7
        self.lista_val.append([80,60])                  # 8
        self.lista_val.append([Texto,Texto,Texto])      # 9
        self.lista_val.append("")                       # 10
        
        self.setToolTip(Texto)
        
        # Bandera para indicarle a leaveEvent y enterEvent que no deben reconfigurar el botón mientras esté apretado
        self.apretado = False

        # Indicamos que el boton responde a un cambio si es que es apretado
        self.seApreta = True

        self.configuraBoton(0)

    def asigna_fondo(self, fondo):
        if fondo == 0:
            self.lista_val[0] = [255,255,255]
            self.configuraBoton(0)
        elif fondo == 1:
            self.lista_val[0] = [210,210,230]
            self.configuraBoton(0)
        elif fondo == 2:
            self.lista_val[0] = [180,180,180]
            self.configuraBoton(0)


    def leaveEvent(self, event):
        '''Evento de retirar el mouse de encima del label'''
        print("mouse out")
        #if self.apretado == False:
        #    self.configuraBoton(0)
        self.retirar.emit(True)

    # Evento cuando el mouse hace clic sobre el label
    def mousePressEvent(self, event):
        '''Evento Clic en un label'''
        print("Press")
        if self.seApreta == True:
            self.configuraBoton(1)
        self.apretado = True
        self.clicked.emit("Clic")
    
    # Evento que se ejecuta casi siempre que se ejecuta otro evento, no le encontré utilidad pero puede ser útil en algún momento.
    def mouseReleaseEvent(self, event):
        '''Evento que se ejecuta cada vez que se ejecuta otro evento'''
        print("Release")
    
    def enterEvent(self, event):
        '''Evento de pasar con el mouse por encima en un label'''
        print("Move")
        #if self.apretado == False:
        #    self.configuraBoton(2)
        self.flotar.emit(True)

    def configuraBoton(self, tipo):
        '''Configura el botón según los valores del parametro tipo(0=Normal / 1=Apretado / 2=MouseHover)'''
        
        lista_back = []
        solid = int
        lista_borde = []
        texto = str

        # Modo normal - o cuando se lo quiere llevar a ese modo luego de dejar de estar apretado el botón
        lista_back = self.lista_val[0]
        solid = self.lista_val[3][tipo]
        lista_borde = self.lista_val[4 + tipo]

        # Edita el texto que tiene el label
        #if self.text() != self.lista_val[9][tipo]:
        #    self.setText(self.lista_val[9][tipo])
        
        self.apretado = False

        self.setStyleSheet("background-color: rgb({},{},{});border: {}px solid;border-color: rgb({},{},{});".format(lista_back[0],lista_back[1],lista_back[2],solid,lista_borde[0],lista_borde[1],lista_borde[2]))

class Lista_venta(QFrame):
    def __init__(self, Lista_Texto, nomb, ancho_tot, fondo = 0, parent=None):
        super(Lista_venta, self).__init__(parent)
        
        #self.setMinimumSize(QtCore.QSize(ancho_tot, 41))
        self.setMaximumSize(QtCore.QSize(16777215, 41))
        #self.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("frame_renglon_{}".format(nomb))
        self.hor_Layout = QtWidgets.QHBoxLayout(self)
        self.hor_Layout.setContentsMargins(0, 0, 0, 0)
        self.hor_Layout.setSpacing(0)
        self.Lista_Labels = []
        
        ancho = 0
        alto = 41
        font = QtGui.QFont()
        font.setPointSize(18)
        for i in range(5):
            label = QlabelClickeable(Lista_Texto[i],0, fondo, self)
            self.hor_Layout.addWidget(label)
            self.hor_Layout.setObjectName("hor_Layout_{}".format(nomb))
            label.setText(Lista_Texto[i])
            label.setFont(font)
            
            ancho_con = ancho_tot - 460
            # Tamaño según su pos. 0 no se edita el tamaño porque es para el concepto, que se ajusta a la pantalla.
            if i == 0:
                label.setMinimumSize(70, alto)
                label.setMaximumSize(70, alto)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setObjectName("label_Nro")
                self.Lista_Labels.append(label)
            elif i == 1:
                #label.setMinimumSize(ancho_con, alto)
                #label.setMaximumSize(ancho_con, alto)
                label.setFixedSize(QtCore.QSize(ancho_con, alto))
                label.setObjectName("label_Con")
                self.Lista_Labels.append(label)
                if Lista_Texto[0] == "50":
                    print(str(label.width()))
                    print(str(label.height()))
            elif i == 2:
                ancho = 130
                label.setMinimumSize(ancho, alto)
                label.setMaximumSize(ancho, alto)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setObjectName("label_Uni")
                self.Lista_Labels.append(label)
            elif i == 3:
                ancho = 130
                label.setMinimumSize(ancho, alto)
                label.setMaximumSize(ancho, alto)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setObjectName("label_Can")
                self.Lista_Labels.append(label)
            elif i == 4:
                ancho = 130
                label.setMinimumSize(ancho, alto)
                label.setMaximumSize(ancho, alto)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setObjectName("label_Sub")
                self.Lista_Labels.append(label)
    

    def __del__(self):
        print("Renglón eliminado")

    def resizeEvent(self, event):
        '''Desde el exterior se llama a ésta función al momento en que se redimencionan los renglones, pero es necesario reubicar los labels.'''