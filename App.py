import sys
#import platform
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
#from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QInputDialog, QFrame
#from vtn.vtn.vtn_productos import Ui_Productos
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QDir, Qt

from sources.vtn.mw_ppal import Ui_MainWindow

from sources.cls.Functions import *
#from sources.cls.productos import *
from sources.cls.ventas import *
from sources.cls.carga_fondo import *
#from sources.vtn.cla_botones import Boton
import sources.mod.vars as mi_vs
import sources.mod.func as func

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Cargamos las configuraciones de cada Page o ventana
        self.Configura_Ventas()
        self.Configura_Carga_Fondo()

        # Es el primer intento de conectar con las bases de datos, siendo necesario como mínimo la conexión con la DB local.
        Estado = func.Actualiza_Path()
        if Estado == 0:
            # Cuando no se pudo conectar ni siquiera a la base de datos local
            QMessageBox.critical(self, "ERROR", "No se ha podido establecer conexión con ninguna BASE DE DATOS, el programa no podrá funcionar. \nPuede cerrar el programa o reintentar la conexión desde la CONFIGURACIÓN.", QMessageBox.Ok)
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_configuracion)
        else:
            pass
        # Recordar que ésta función toma datos luego de haber se llamado a la función que actualiza los Path, por ende siempre debe ir dsp de ella.
        self.Configura_Configuraciones()

        self.showMaximized()

        func.Actualiza_Configuraciones(self, self.Lista_Page_Ventas)

    def Configura_Ventas(self):
        ''' Configuraciones de la ventana VENTAS (Botones, Señal-Slot, etc). '''

        # Configuramos las imagenes de la ventana
        self.ui.push_config_cierra_ses.setIcon(QtGui.QIcon("./sources/img/icon/ses.jpg"))
        

        self.Lista_Page_Ventas = []
            
        # VARIABLES QUE NO SE DEBEN MODIFICAR EN EJECUCIÓN
        # Es la cantidad de productos que vamos a dejar ver en las listas
        # Pos 0: CANT_WIDG
        self.Lista_Page_Ventas.append(0)

        # Pos 1: PRESION_ANTERIOR = 0
        self.Lista_Page_Ventas.append(0)
        # Pos 2: PRESION_ANTERIOR2 = 0. Bandera que avisa alguna evento que debe ver el KeyPressEvent.
        self.Lista_Page_Ventas.append(0)

        # Colores Normales de la ventana 1
        # Pos 3: R_v1 = 208
        # Pos 4: G_v1 = 211
        # Pos 5: B_v1 = 212
        self.Lista_Page_Ventas.append(208)
        self.Lista_Page_Ventas.append(211)
        self.Lista_Page_Ventas.append(212)
        # Colores Normales de la ventana 2
        # Pos 6: R_v2 = 0
        # Pos 7: G_v2 = 0
        # Pos 8: B_v2 = 0
        self.Lista_Page_Ventas.append(0)
        self.Lista_Page_Ventas.append(0)
        self.Lista_Page_Ventas.append(0)
        # Colores Normales de la ventana 3
        # Pos 9: R_v3 = 0
        # Pos 10: G_v3 = 0
        # Pos 11: B_v3 = 0
        self.Lista_Page_Ventas.append(0)
        self.Lista_Page_Ventas.append(0)
        self.Lista_Page_Ventas.append(0)

        # Colores de Cantidad Próxima
        # Pos 12: R_c = 0
        # Pos 13: G_c = 0
        # Pos 14: B_c = 255
        self.Lista_Page_Ventas.append(0)
        self.Lista_Page_Ventas.append(0)
        self.Lista_Page_Ventas.append(255)
        
        # Colores de Promos
        # Pos 15: R_p = 0
        # Pos 16: G_p = 255
        # Pos 17: B_p = 0
        self.Lista_Page_Ventas.append(0)
        self.Lista_Page_Ventas.append(255)
        self.Lista_Page_Ventas.append(0)

        # Colores para cuando se va a borrar algún ítem
        # Pos 18: R_b = 255
        # Pos 19: G_b = 0
        # Pos 20: B_b = 0
        self.Lista_Page_Ventas.append(255)
        self.Lista_Page_Ventas.append(0)
        self.Lista_Page_Ventas.append(0)

        self.ui.verticalScrollBar.setMinimum(0)
        self.ui.verticalScrollBar.setMaximum(0)
        self.ui.verticalScrollBar.valueChanged.connect(lambda: self.Refresca_Listas(scrol = self.ui.verticalScrollBar.value()))
        

        # VARIABLES QUE SE MODIFICAN AL LIMPIAR PANTALLA O SIMILARES
        # Lista que contiene en otras listas los datos del producto o promo para realizar los cálculos y los cobros
        # Pos 21: LISTA_VENTA_REAL = []
            # 0: ID del producto
            # 1: Concepto
            # 2: Pcio unit
            # 3: cantidad
            # 4: subtotal
            # 5: Guía - Relación directa con el valor de "Nro" que contiene la LISTA_VENTA_MOSTRADA
            # 6: Caja asociada
            # 7: Codigo Promo
        LISTA_VENTA_REAL = []
        self.Lista_Page_Ventas.append(LISTA_VENTA_REAL)
        # Lista que contiene en otras listas los datos que mostramos en los listwidgets en pantalla
        # Pos 22: LISTA_VENTA_MOSTRADA = []
            # 0: Numero
            # 1: Concepto
            # 2: Pcio Unit
            # 3: Cantidad
            # 4: Subtotal
        LISTA_VENTA_MOSTRADA = []
        self.Lista_Page_Ventas.append(LISTA_VENTA_MOSTRADA)
        # Lista con los datos del producto que estamos buscando
        # Pos 23: PROD_TEMP = []
        PROD_TEMP = []
        self.Lista_Page_Ventas.append(PROD_TEMP)


        # Es la cantidad de unidades que se van a cargar del próximo producto. Si su unidad de medida es kg o lts, la forma de cargar es distinta
        # Pos 24: Cantidad_Prox = 0
        self.Lista_Page_Ventas.append(0)
        # Relativo al vendedor activo (1 de 3)
        # Pos 25: VENDEDOR = 1
        self.Lista_Page_Ventas.append(1)
        
        # VARIABLES - OTRAS
        # Pos 26: SCROLL_BLOQUEO = False
        self.Lista_Page_Ventas.append(False)
        # Pos 27: bloqueo = False
        self.Lista_Page_Ventas.append(False)
        # Bandera que avisa al App.py que hay que abrir la ventana para crear un producto nuevo
        # Pos 28: PROD_NUEVO = ""
        self.Lista_Page_Ventas.append("")
        # Bandera para saber si estamos esperando la contestación de una promo o no
        # Pos 29: BANDERA_PROMO = False
        self.Lista_Page_Ventas.append(False)
        # A la hora de ir cargando los códigos en el tipo de promo 2, se necesitan datos que es innecesario recopilar constantemente en cada acción, por ende los cargamos acá
            # para que el Return_Line_Promo tenga datos para trabajar
            # 0: Contador. Indica cuántos productos de la promo se van cargando.
            # 1: Cantidad. Indica el total de producto que se tienen que cargar de la promo.
            # 2: lista_codigos. Es una lista con los códigos que contiene la promo.
            # 3: Sumado. Variable para ir calculando el resto que queda a la hora de sumar centavos y cargar al último ítem un valor que cumpla con el total de la promo.
            # 4: Lista_de_Promo. Es la lista con los datos de la prom.db
            # 5: Precio. Es el precio Unitario por cada producto.
            # 6: Guia. Es el valor numérico guía para relacionar la lista de venta mostrada con la real.
        # Pos 30: DATOS_PROMOS_2 = []
        # Bandera para saber si estamos esperando la contestación de una carga de Precio, Litro, etc...
            # 0: Es cuando estamos operando de manera normal. Se usa su valor para restaurar la ventana, y limpia variables tmb.
            # 1: Unidad
            # 2: Peso
            # 3: Litros
            # 4: cm3
            # 5: Precio
            # 11: Codigo
        DATOS_PROMOS_2 = []
        self.Lista_Page_Ventas.append(DATOS_PROMOS_2)

        # Pos 31: BANDERA_PRECIO = 0
        self.Lista_Page_Ventas.append(0)

        # Pos 32: TIPOS DE PRODUCTOS QUE PERMITE TRABAJAR
            # 0: Permite productos SIN stock: Desactivados / Incompletos / Completos
            # 1: Permite productos con stock: Desactivados / Incompletos / Completos
            # 2: Permite productos SIN stock: Incompletos / Completos
            # 3: Permite productos con stock: Incompletos / Completos
            # 4: Permite productos SIN stock: Completos
            # 5: Permite productos con stock: Completos
        self.Lista_Page_Ventas.append(2)

        # CONFIGURACIONES DE WIDGETS
        # GroupBox que suplantan los mensajes para evitar la pérdida del foco.
        #self.ui.page .groupBox_Ingresos.setVisible(False)
        self.ui.groupBox_Promos.setVisible(False)

        self.ui.push_Eliminar.clicked.connect(lambda: V_Ventas.Elimina_Item(self, self.ui, self.Lista_Page_Ventas))
        self.ui.push_Limpiar_Venta.clicked.connect(lambda: V_Ventas.Limpia_Ventana( self.ui, self.Lista_Page_Ventas))
        self.ui.push_Cargar.clicked.connect(self.Ventas_a_Carga_Fondo)
        self.ui.line_Codigo.textChanged.connect(lambda: V_Ventas.Change_line_Cod(self, self.ui, self.Lista_Page_Ventas))
        self.ui.line_Codigo.returnPressed.connect(lambda: V_Ventas.Return_line_Cod(self, self.ui, self.Lista_Page_Ventas))
        self.ui.line_Monto.textChanged.connect(lambda: V_Ventas.Change_line_Monto(self.ui, self.Lista_Page_Ventas))
        self.ui.line_Monto.returnPressed.connect(lambda: V_Ventas.Return_line_Monto(self.ui, self.Lista_Page_Ventas))
        self.ui.push_config_cierra_ses.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_pass))

        self.ui.line_Ingreso_Promo.returnPressed.connect(lambda: V_Ventas.Return_line_Promo(self, self.ui, self.Lista_Page_Ventas))
        self.ui.line_Ingresos.textChanged.connect(lambda: V_Ventas.Change_line_GB_Precio(self.ui))
        self.ui.line_Ingresos.returnPressed.connect(lambda: V_Ventas.Return_line_GB_Precio(self, self.ui, self.Lista_Page_Ventas))

        self.ui.push_Uno.clicked.connect(self.imprime_wid)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.line_Codigo.setFocus()

        self.lista_renglones = []
        #self.ui.groupBox_lista.setVisible(False)
        #self.Crea_renglon(10)
        '''
        color = 0
        self.ui.frame_lista.setFixedWidth(self.ui.frame_panel.width())
        alto = self.ui.frame_lista.height()
        ancho = self.ui.frame_labels.width()
        for i in range(100):
            valor = str(i)
            renglon = Lista_venta_2([valor, "Concepto                            r", "Cantidad", "Precio1", "Precio2"], valor, ancho, color, self.ui.groupBox_lista)
            if color == 0: 
                color = 1
            else:
                color = 0
            renglon.setGeometry(QtCore.QRect(0, 41 * i, ancho, 41))
            self.ui.frame_lista.setFixedSize(QtCore.QSize(ancho, 41 * (i + 1)))
        self.Imprime()
        '''

    def Crea_renglon(self, cant):
        color = 0
        self.ui.frame_lista.setFixedWidth(self.ui.frame_panel.width())
        alto = self.ui.frame_lista.height()
        ancho = self.ui.frame_labels.width()
        for i in range(cant):
            valor = str(i)
            renglon = Lista_venta([valor, "Concepto", "088,888", "088.888,88", "088.888,88"], valor, ancho, color)
            self.ui.verticalLayout_5.addWidget(renglon)
            renglon.setGeometry(0, 41 * i, ancho, 41)
            self.lista_renglones.append(renglon)
            if color == 0: 
                color = 1
            else:
                color = 0
            #renglon.setGeometry(QtCore.QRect(0, 41 * i, ancho, 41))
        self.ui.frame_lista.setFixedSize(QtCore.QSize(ancho, 41 * (i + 1)))
        self.Imprime()
    
    def Imprime(self):
        print("ancho frame labels: {}".format(self.ui.frame_labels.width()))
        print("alto frame labels: {}".format(self.ui.frame_labels.height()))
        print("ancho frame lista: {}".format(self.ui.frame_lista.width()))
        print("alto frame lista: {}".format(self.ui.frame_lista.height()))
        #print("ancho grup: {}".format(self.ui.groupBox_lista.width()))
        #print("alto grup: {}".format(self.ui.groupBox_lista.height()))
        try:
            print("ancho RENGLON 50: {}".format(self.lista_renglones[50].width()))
            print("alto RENGLON 50: {}".format(self.lista_renglones[50].height()))
        except:
            pass

    def imprime_wid(self):
        for child in self.findChildren(QLabel):
            print(child.objectName())

    def Ventas_a_Carga_Fondo(self):        
        '''Es una función de VENTAS.
        Cambia de la ventana de Ventas a Carga Fondos, y si no hay ventas para cargar deja un mensaje. '''
        if len(self.Lista_Page_Ventas[21]) > 0:
            self.Lista_Page_Carga_Fondo[8] = self.Lista_Page_Ventas[21]
            UIFunctions_Menu.Seleccion_Pages(self.ui, "Carga Fondos")
            V_Carga_Fondo.Mostrar(self.ui, self.Lista_Page_Carga_Fondo)
        else:
            self.Crea_renglon(100)
            QMessageBox.question(self,"Aviso", "No hay ventas para cargar", QMessageBox.Ok)

    def Configura_Carga_Fondo(self):
        self.Lista_Page_Carga_Fondo = []

        #self.aviso_enter = False
        #self.Tipo_Inc = 0
        # Pos 0 a 1
        self.Lista_Page_Carga_Fondo.append(False)
        self.Lista_Page_Carga_Fondo.append(0)
        
        # Variables que necesita para realizar la carga de datos
        #self.DICCIONARIO_CON_LISTA = []   ATENCIÓN! ESTE SE DEJÓ DE USAR PORQUE AHORA TENEMOS ACCESO A LA LISTA ORIGINAL
        #self.TOTAL_DEUDA = 0.0
        #self.DEUDA_PARCIAL = 0.0
        #self.LISTA_ID_FONDOS = []
        #self.LISTA_COBROS = []
        # Pos 2 a 5
        self.Lista_Page_Carga_Fondo.append(0.0)
        self.Lista_Page_Carga_Fondo.append(0.0)
        self.Lista_Page_Carga_Fondo.append([])
        self.Lista_Page_Carga_Fondo.append([])
        #self.BloqueoLista = True
        #self.Aviso_Carga = False
        # Pos 6 y 7
        self.Lista_Page_Carga_Fondo.append(True)
        self.Lista_Page_Carga_Fondo.append(False)
        # VENTA_REAL
        # Pos 8
        self.Lista_Page_Carga_Fondo.append([])

        # Elementos en pantalla
        self.ui.list_fondos_3.clicked.connect(lambda: V_Carga_Fondo.Clic_Lista_Fondos(self.ui, self.Lista_Page_Carga_Fondo))
        self.ui.list_fondos_3.itemSelectionChanged.connect(lambda: V_Carga_Fondo.Clic_Lista_Fondos(self.ui, self.Lista_Page_Carga_Fondo))
        self.ui.lineEdit_3.textChanged.connect(lambda: self.ui.lineEdit_3.setText(form.Line_Num_Coma_(self.ui.lineEdit_3.text())))
        self.ui.lineEdit_3.returnPressed.connect(lambda: V_Carga_Fondo.Return_line_Monto(self, self.ui, self.Lista_Page_Carga_Fondo))
        self.ui.push_cargar_3.clicked.connect(lambda: V_Carga_Fondo.Carga_Venta(self.Lista_Page_Carga_Fondo))

    def Configura_Configuraciones(self):
        '''Relativo a la configuración de la Page_configuraciones, que tiene datos Generales.
        Tener en cuenta de que los datos que se mostrarán y modificarán en ésta página no podrán estar en Red debido a que de lo contrario deberíamos siempre contar con red activa. Por ende todo está por el momento en la base de datos de Configuraciones (config.db).'''
        
        # Si bien se debería encargar de sólo colocar la carpeta donde están las DB, por el momento ponemos el path de la que contiene los productos y no sólo su carpeta. Una vez que se haya implementado el sistema completo de red con todos los path, aquí se deben colocar sólo sus carpetas.
        self.ui.line_conf_path_local.setText(mi_vs.BASE_DATOS_SEC)
        self.ui.line_conf_path_red.setText(mi_vs.BASE_DATOS_PPAL)

        self.ui.combo_conf_cta_usu.addItem("Crear Nuevo Usuario")
        Tabla = mdb_p.Dev_Tabla(mi_vs.BASE_CONFIG_SEC, "Usuarios")
        for reg in Tabla:
            self.ui.combo_conf_cta_usu.addItem(reg[2])

    # Recordar que esto es un rejunte de otro programa, por ende, ahora estoy intentando mezclar todos los "KeyPressEvent" en uno sólo por la cantidad de widgets que hay
    def keyPressEvent(self, event):
        '''Evento que se ejecuta siempre en la ventana. Es recomendable asignarlo luego de una actividad inusual, porque por ejemplo si yo conecto una señal con una función de 
        un line como por ej: line1.returnPressed.connect(self.line2.focus()), dicha señal genera que al presionar Enter en el line1 lleve el foco al line2, pero una vez hecho 
        ésto se ejecuta ésta función llamada keyPressEvent, donde analizamos la última tecla presionada, siendo un Enter, por ende, se va a ejecutar la función que aquí le 
        estemos asignando al presionar Enter en el widget que ahora tiene el foco, sería line2. Esto puede llevar a confusión, pero lo que termina haciendo es lo mismo que
        haber presionado Enter 2 veces en vez de una, ya que captaron el evento dos funciones distintas.'''

        # Con ésta línea podemos comparar y sólo será True cuando el evento registrado es que se haya presionado una tecla
        if event.type() == QtCore.QEvent.KeyPress:

            texto = str(event.key())
            print(texto)

            # En ésta línea como ejemplo controlamos que la tecla presionada sea "Enter"
            if event.key() == QtCore.Qt.Key_Enter:

                # VENTANA VENTAS
                # Botón Cargar de la vtn_Ventas
                if self.ui.push_Cargar.hasFocus() and self.Lista_Page_Ventas[2] == 0:
                    V_Ventas.Event_press_barra(self.ui, self.Lista_Page_Ventas)
                    print("Ventas-btn-cargar")
                    self.Ventas_a_Carga_Fondo()


                # VENTANA CARGA FONDOS
                # Botón Cargar de la vtn_Carga_Fondo
                elif self.ui.push_cargar_3.hasFocus():
                    print("Carga-fondo-btn-cargar")

                    if self.Lista_Page_Carga_Fondo[0] == True:
                        self.Lista_Page_Carga_Fondo[0] = False
                        V_Carga_Fondo.Carga_Venta(self.Lista_Page_Carga_Fondo)
                        V_Ventas.Limpia_Ventana(self.ui, self.Lista_Page_Ventas)
                        UIFunctions_Menu.Seleccion_Pages(self.ui, "Ventas")
                    else:
                        self.Lista_Page_Carga_Fondo[0] = True
                
                # Clic en botón CANCELAR
                elif self.ui.push_cancelar_3.hasFocus():
                    print("Carga-fondo-btn-cancelar")
                    UIFunctions_Menu.Seleccion_Pages(self.ui, "Ventas")
            
            if event.key() == QtCore.Qt.Key_F5:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_configuracion)
            
            # Limpiamos la acción que se haya enviado como mensaje a ésta función.
            self.Lista_Page_Ventas[2] = 0

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
            self.lista_val.append([230,230,255])        # 0
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
        lista_back = self.lista_val[tipo]
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
        
        self.setMinimumSize(QtCore.QSize(ancho_tot, 41))
        self.setMaximumSize(QtCore.QSize(16777215, 41))
        #self.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("frame_renglon_{}".format(nomb))
        self.hor_Layout = QtWidgets.QHBoxLayout(self)
        self.hor_Layout.setContentsMargins(0, 0, 0, 0)
        self.hor_Layout.setSpacing(0)
        
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
                label.setObjectName("label_Nro_{}".format(nomb))
            elif i == 1:
                #label.setMinimumSize(ancho_con, alto)
                #label.setMaximumSize(ancho_con, alto)
                label.setFixedSize(QtCore.QSize(ancho_con, alto))
                label.setObjectName("label_Con_{}".format(nomb))
                if Lista_Texto[0] == "50":
                    print(str(label.width()))
                    print(str(label.height()))
            elif i == 2:
                ancho = 130
                label.setMinimumSize(ancho, alto)
                label.setMaximumSize(ancho, alto)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setObjectName("label_Uni_{}".format(nomb))
            elif i == 3:
                ancho = 130
                label.setMinimumSize(ancho, alto)
                label.setMaximumSize(ancho, alto)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setObjectName("label_Can_{}".format(nomb))
            elif i == 4:
                ancho = 130
                label.setMinimumSize(ancho, alto)
                label.setMaximumSize(ancho, alto)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setObjectName("label_Sub_{}".format(nomb))

class Lista_venta_2():
    def __init__(self, Lista_Texto, nomb, ancho_tot, fondo = 0, parent=None):
        #super(Lista_venta, self).__init__(parent)
        
        ancho = 0
        alto = 41
        for i in range(5):
            label = QlabelClickeable(Lista_Texto[i],0, fondo)
            label.setText(Lista_Texto[i])
            
            ancho_con = ancho_tot - 460
            # Tamaño según su pos. 0 no se edita el tamaño porque es para el concepto, que se ajusta a la pantalla.
            texto = str(i)
            if i == 0:
                label.setMinimumSize(70, alto)
                label.setMaximumSize(70, alto)
                label.setObjectName("label_Nro_{}".format(texto))
            elif i == 1:
                #label.setMinimumSize(ancho_con, alto)
                #label.setMaximumSize(ancho_con, alto)
                label.setFixedSize(QtCore.QSize(ancho_con, alto))
                label.setObjectName("label_Con_{}".format(texto))
                print(ancho_con)
            elif i == 2:
                ancho = 130
                label.setMinimumSize(ancho, alto)
                label.setMaximumSize(ancho, alto)
                label.setObjectName("label_Uni_{}".format(texto))
            elif i == 3:
                ancho = 130
                label.setMinimumSize(ancho, alto)
                label.setMaximumSize(ancho, alto)
                label.setObjectName("label_Can_{}".format(texto))
            elif i == 4:
                ancho = 130
                label.setMinimumSize(ancho, alto)
                label.setMaximumSize(ancho, alto)
                label.setObjectName("label_Sub_{}".format(texto))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())