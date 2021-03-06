#!/usr/bin/python3.7.3
'''

sources/cls/__pycache__/*.pyc
sources/mod/__pycache__/*.pyc
sources/vtn/__pycache__/*.pyc

    MODO DE TRABAJO GENERAL:
    Debido a que tenemos el código divido en diferentes módulos, éstos últimos no pueden realizar acciones de creación de instancias dentro de la ventana principal, por esto es que debemos crear y eliminar las instancias desde éste módulo. Por ejemplo, para crear un renglón de información en una venta realizada, vamos a llamar primero u una función en éste módulo que luego llama al módulo de ventas con los códigos pertinentes a su acción y una vez que establecemos que hay que crear una renglón, mediante la utilización de banderas ubicadas en la lista de datos de cada ventana, avisamos que hay que crear un renglón y esa primer función que llamamos en un principio, se encargará de hacerlo.

    (*1) Tenemos un módulo que contiene las funciones relativas a las ventas, pero desde ahí no podemos crear los renglones de la lista que muestra las ventas que se van realizando, por ende, lo que hacemos es llamar desde éste módulo a una función que también está acá, éste se encarga de llamar a las funciones pertinentes del otro módulo y luego mediante el uso de una bandera indicada en Lista_Datos[34] es que realizamos la creación de dicho renglón. [34] es una lista dentro de la ppal que en su pos[0] contiene un boolean como bandera para saber si agregamos el dato, y los demás datos son los necesarios para la acción.
'''

import sys
#import platform
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
#from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QInputDialog, QFrame
import threading
import time
#from vtn.vtn.vtn_productos import Ui_Productos
#from PyQt5.QtGui import QIcon, QPixmap, QFont
#from PyQt5.QtCore import QDir, QSize, Qt

from sources.vtn.mw_ppal import Ui_MainWindow

from sources.cls.Functions import *
#from sources.cls.productos import *
from sources.cls.ventas import *
from sources.cls.carga_fondo import *
#from sources.vtn.cla_botones import Boton

import sources.mod.vars as mi_vs
import sources.mod.func as func
import sources.mod.mdbprod as mdb_p
import sources.mod.act as act
from sources.mod.renglones import *
import sources.mod.nave as nv

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Es el primer intento de conectar con las bases de datos, siendo necesario como mínimo la conexión con la DB local.
        Estado = func.Actualiza_Path()
        if Estado == 0:
            # Cuando no se pudo conectar ni siquiera a la base de datos local
            QMessageBox.critical(self, "ERROR", "No se ha podido establecer conexión con ninguna BASE DE DATOS, el programa no podrá funcionar. \nPuede cerrar el programa o reintentar la conexión desde la CONFIGURACIÓN.", QMessageBox.Ok)
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_configuracion)
        else:
            # Una vez que realizamos la actualización de DBs que necesita el programa, vamos a actualizar los path donde deben buscarse las actualizaciones
            for pos in range(len(mi_vs.LIST_BASE_DATOS)):
                if pos > 0:
                    act.lista_scan.append(mi_vs.LIST_BASE_DATOS[pos])
        
        # Recordar que ésta función toma datos luego de haber se llamado a la función que actualiza los Path, por ende siempre debe ir dsp de ella.
        self.Configura_Configuraciones()
        # Cargamos las configuraciones de cada Page o ventana
        self.Configura_Ventas()

        self.Configura_Carga_Fondo()

        self.showMaximized()
        V_Ventas.Resize_Window(self.ui, self.Lista_Page_Ventas, Ventana=True)

        V_Ventas.Limpia_Foco_Cod(self.ui, self.Lista_Page_Ventas)

        func.Actualiza_Configuraciones(self, self.Lista_Page_Ventas)

        # Iniciamos el bucle encargado de mantener las DBs actualizadas.
        self.bucle = True
        self.T1 = threading.Thread(target=self.bucleDeActualizacion)
        self.T1.start()
    
    def closeEvent(self, event):
        # Cerramos el bucle de esta manera, ya que en los foros he encontrado que a veces da error intentar eliminar un hilo, y no se tiene un buen control del mismo. Por ende, al quitar la validación del bucle vamos a hacer que se elimine sólo.
        self.bucle = False

    ############################################################## VENTAS ##############################################################
    ####################################################################################################################################
    def Configura_Ventas(self):
        ''' Configuraciones de la ventana VENTAS (Botones, Señal-Slot, etc). '''

        self.ui.verticalLayout_5 = QtWidgets.QVBoxLayout(self.ui.frame_lista)
        self.ui.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.ui.verticalLayout_5.setSpacing(0)
        self.ui.verticalLayout_5.setObjectName("verticalLayout_5")

        # Configuramos las imagenes de la ventana
        self.ui.push_config_cierra_ses.setIcon(QtGui.QIcon("./sources/img/icon/ses.jpg"))

        self.Lista_Page_Ventas = []
        
        # VARIABLES QUE NO SE DEBEN MODIFICAR EN EJECUCIÓN
        # Esta variable del tipo int, indica el producto que se encuentra seleccionado de la lista. Si está seleccionado el primer producto de la lista, ésta variable vale 1 y 
        # no 0.
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

        # VARIABLES QUE SE MODIFICAN AL LIMPIAR PANTALLA O SIMILARES
        # Lista que contiene en otras listas los datos del producto o promo para realizar los cálculos y los cobros
        # Pos 21: LISTA_VENTA_REAL = []
            # 0: ID del producto
            # 1: Concepto
            # 2: Pcio unit
            # 3: cantidad
            # 4: subtotal
            # 5: Guía
            # 6: Caja asociada
            # 7: Codigo Promo
        LISTA_VENTA_REAL = []
        self.Lista_Page_Ventas.append(LISTA_VENTA_REAL)
        # Lista que contiene en otras listas los datos que mostramos en los listwidgets en pantalla
        # Pos 22: LISTA_VENTA_MOSTRADA = []
            # 0: Numero de GUÍA
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
        self.Lista_Page_Ventas.append([])

        # Pos 31: BANDERA_PRECIO = 0
        self.Lista_Page_Ventas.append(0)

        # Pos 32: TIPOS DE PRODUCTOS QUE PERMITE TRABAJAR
            # 0: Permite productos SIN stock: Desactivados / Incompletos / Completos
            # 1: Permite productos SIN stock: Incompletos / Completos
            # 2: Permite productos SIN stock: Completos
            # 3: Permite productos con stock: Desactivados / Incompletos / Completos
            # 4: Permite productos con stock: Incompletos / Completos
            # 5: Permite productos con stock: Completos
        estado, Registro = mdb_p.Reg_Un_param("config.db", "Generales", "Nombre", "Vta_Prod_Desact")
        for Dato in Registro:
            self.Lista_Page_Ventas.append(Dato[4])
        
        # Pos 33: Color del renglón que hay que colocar cada vez que se crea uno nuevo
        self.Lista_Page_Ventas.append(False)

        ''' Pos 34: Lista con los datos necesarios para crear un nuevo renglón. (*1)
            0: T/F bandera que no se utiliza aquí.
            1: alto del renglón, por el momento es 41 píxeles.
        '''
        self.Lista_Page_Ventas.append([False, 41])

        # Pos 35: Avisa si hay que actualizar el valor de algún renglón
            # 0: T-F
            # 1: Pos de la lista
            # 2: Nuevo valor para Nro
            # 3: Nuevo valor para Concepto
            # 4: Nuevo valor para Pcio Unit
            # 5: Nuevo valor para Cantidad
            # 6: Nuevo valor para Subtotal
        self.Lista_Page_Ventas.append([False, 0, "", "", "", "", ""])

        # Pos 36: Valor de referencia para cada producto de venta. Por cada producto que se carga, se le asigna un valor de referencia, que no es más que un número entero que se va incrementando desde 1. El valor es la guía que comparten las lista [21] y [22]. Si no se borran ítems, también coincidiría con el número visto en pantalla, pero, no siempre va a ser así, ya que si un elemento de pantalla se borra, su guía permanecerá intacta y los próximos productos se mantienen en aumento, perdiendo la concordancia con los números mostrados en la lista por pantalla.
        self.Lista_Page_Ventas.append(0)

        # ATENCIÓN!: LA POS 37 ES CARGADA POR LA FUNCIÓN QUE SE LLAMA AL BUSCAR ACTUALIZACIONES: bucleDeActualizacion

        # CONFIGURACIONES DE WIDGETS
        self.ui.verticalScrollBar.setMinimum(0)
        self.ui.verticalScrollBar.setMaximum(0)
        self.ui.verticalScrollBar.valueChanged.connect(lambda: V_Ventas.Change_ScrollBar(self.ui, self.Lista_Page_Ventas))

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
        
        self.ui.push_Uno.clicked.connect(self.Imprime)
        self.ui.push_Dos.clicked.connect(self.imprime_wid)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.line_Codigo.setFocus()

    def Imprime(self):
        print("IMPRIME 1:")
        print("ancho frame panel lista: {}".format(self.ui.frame_panel_lista.width()))
        print("alto frame panel lista: {} \n".format(self.ui.frame_panel_lista.height()))
        print("ancho frame panel: {}".format(self.ui.frame_panel.width()))
        print("alto frame panel: {}\n".format(self.ui.frame_panel.height()))
        print("ancho frame labels: {}".format(self.ui.frame_labels.width()))
        print("alto frame labels: {}\n".format(self.ui.frame_labels.height()))
        print("ancho frame content lista: {}".format(self.ui.frame_content_lista.width()))
        print("alto frame content lista: {}".format(self.ui.frame_content_lista.height()))
        print("ancho frame lista: {}".format(self.ui.frame_lista.width()))
        print("alto frame lista: {}".format(self.ui.frame_lista.height()))
        try:
            print("ancho RENGLON 50: {}".format(self.lista_renglones[50].width()))
            print("alto RENGLON 50: {}".format(self.lista_renglones[50].height()))
        except:
            pass

    def imprime_wid(self):
        print("IMPRIME 2:")
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
            QMessageBox.question(self,"Aviso", "No hay ventas para cargar", QMessageBox.Ok)
            V_Ventas.Limpia_Foco_Cod(self.ui, self.Lista_Page_Ventas)

    ############################################################ CARGA FONDO ###########################################################
    ####################################################################################################################################
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
        self.ui.line_conf_path_local.setText(mi_vs.LIST_BASE_DATOS[0])
        self.ui.line_conf_path_red.setText(mi_vs.LIST_BASE_DATOS[1])

        self.ui.combo_conf_cta_usu.addItem("Crear Nuevo Usuario")
        intento = False
        Tabla = ""
        for pos in range(len(mi_vs.LIST_BASE_DATOS)):
            if pos > 0:
                try:
                    if nv.os.path.isdir(mi_vs.LIST_BASE_DATOS[pos]):
                        Tabla = mdb_p.Dev_Tabla(mi_vs.LIST_BASE_DATOS[pos] + "config.db", "Usuarios")
                        intento = True
                except:
                    intento = False
        if intento == False:
            try:
                if nv.os.path.isdir(mi_vs.LIST_BASE_DATOS[0]):
                    Tabla = mdb_p.Dev_Tabla_inicio(mi_vs.LIST_BASE_DATOS[0] + "config.db", "Usuarios")
            except:
                pass
        for reg in Tabla:
            self.ui.combo_conf_cta_usu.addItem(reg[2])
        
        # Ahora guardamos el nombre de la PC o terminal
        estado, Registro = mdb_p.Reg_Un_param("config.db", "Generales", "Nombre", "Name_terminal")
        for i in Registro:
            mi_vs.MY_NAME = i[5]
        print("MY_NAME: {}".format(mi_vs.MY_NAME))

    ####################################################### ACTUALIZACIÓN DE DB ########################################################
    ####################################################################################################################################
    def bucleDeActualizacion(self):
        '''Bucle que se encarga de ver en qué momento debe realizarse una actualización, ya que es quién llama periódicamente a la función para tal fin. A ésta función se la 
            llama desde un hilo a parte para que no interfiera en las actividades de las cajas.
            En principio se ejecuta en cada inicio del programa y luego va a estar monitoreando cada 30 minutos la red en busca de actualizaciones con la lectura de las DBs en la red. Cuando encuentre una actualización el tiempo se reducirá de 30 a 5 minutos durante 30 minutos (lo que indica que se ejecutará al menos 6 veces cada 5 minutos hasta volver a la normalidad), ya que entendemos que estamos en una situación donde por lo general son periodos de cambios de precios donde esperamos varias actualizaciones y lo importante es que estén actualizados en las cajas. Esos valores se podrán configurar a futuro.
            También contará con un botón para que el usuario pueda llamar a la función. Cuando el usuario haga ésto, el sistema entenderá que es importante una nueva actualización y por ende, estará atento a la búsqueda de la misma, sabrá que hay una actualización y debe encontrarla, por ello, la frecuencia se aumentará a 30 segundos hasta que pueda tener conexión con alguna DB con actualizaciones.
            En el trabajo se tiene en cuenta que las conexiones vía WiFi de las Rpi son intermitentes, por ende, nos preparamos para trabajar con y sin conexión. Por ello contamos con una copia local que es la que estamos actualizando para trabajar con ella cada vez que nos desconectamos.
            Al mismo tiempo, puede darse un caso remoto de que estemos conectados, descarguemos una nueva actualización y la misma se demore lo suficiente como para generar algún problema a la hora de que la caja consulte la misma DB para seguir cargando ventas. Para evitar dicho problema, contaremos con 2 DB locales, así la caja trabaja con la DB1 mientras se esté realizando la actualización en la DB2. Al finalizar la actualización inmediatamente se cambian los path para que el programa siga trabajando con la DB2 y comience a actualizarse la DB1.
            Todos los procesos deben ser informados por pantalla para que el usuario sepa la fecha, la hora de la última y el nombre de la actualización.
            Y por último, nos manejaremos con banderas en una lista que vamos a incorporar en la posición self.Lista_Page_Ventas[37]
            Nota: El botón manual dispara la actualización y en caso de no resultar exitosa, deja el MODO del bucle en 3, intentando cada 30 segundos.
        '''

        # Agregamos a la lista_Ventas las banderas que utilizaremos en el bucle
            # 0: Indica si se está realizando una actualización
            # 1: Es un ESTADO con distintos valores que significan:
                # 0: DETENIDO. Actualizaciones detenidas por motivos de desconexión con todas las DB.
                # 1: NORMAL. Se ejecutan intentos de actualización cada 30 minutos.
                # 2: ATENTO. Es cuando se ha realizado una actualización y estamos a la espera cada 5 minutos de nuevas actualizaciones.
                # 3: MANUAL. Cuando el usuario hizo clic en actualizar y no pudo ejecutarse la misma, éste valor genera intentos de actualizarse cada 10 segundos.
                # Indica si está en modo de MAXIMA ATENCIÓN que es cuando el usuario hizo clic para buscar actualizaciones, que entendemos q sólo sucede cuando es importante.
            # 2: Name_Last_Upd. Es el nombre de la última actualización que tuvimos, porque debemos saber siempre aunq se haya apagado la PC por ej.
        self.Lista_Page_Ventas.append([False, 1, ""])
        # Facilitamos el código dando un nombre a la lista completa
        lista = self.Lista_Page_Ventas[37]

        # Realizamos la primer búsqueda con el inicio del programa
        lista[1] = 4
        self.buscaActualizaciones()

        # VARIABLES. Configurando las mismas controlamos el comportamiento del bucle
        # Es el tiempo para de frecuencia del time.sleep() que va a determinar las repeticiones del bucle completo.
        time_bucle = 10
        # Tiempo total y contador para la frecuencia de la ejecución del MODO NORMAL. (norm_tot * time_bucle = frecuencia con la que se buscarán actualizaciones)
        norm_total = 180
        norm_count = 0
        # Idem anterior pero en modo ATENTO.
        aten_total = 30
        aten_count = 0

        # El bucle va a chequear cada 10 segundos el estado de las variables para saber qué debe realizar, y si el usuario hace clic para buscar actualizaciones de manera manual, se deja avisado aquí para que el bucle no vuelva a generar lo mismo.
        # La variable es puesta en True en el Init.
        while self.bucle:

            time.sleep(time_bucle)

            # Bandera que se va a configurar durante todo el bucle para indicar si hay que buscar o no actualizaciones.
            act = False

            # Puede que casualmente se esté actualizando indicado desde fuera del bucle mediante el botón de usuario, por ende, vamos a controlar eso primero
            if lista[0] == False:
                
                # En caso de estar en modo NORMAL, trabajamos cada 30 minutos
                if lista[1] == 1:
                    norm_count += 1
                    if norm_count == norm_total:
                        act = True
                        norm_count = 0
                
                # En caso de estar en modo ATENTO, trabajamos cada 5 minutos
                elif lista[1] == 2:
                    aten_count += 1
                    if aten_count == aten_total:
                        act = True
                        aten_count = 0

                # Controlamos si no estamos esperando conexión para una act impulsada por el usuario que debe ejecutarse cada 10 segundos. Tener en cuenta que si un usuario busca una actualización y se ejecuta, lista[1] nunca va a ser 3, ya que la actualización se ha ejecutado con éxito. Ahora bien, si se intentó actualizar y no se pudo conectar, entonces sí va a valer 3 generando que cada 10 segundos busquemos actualizaciones.
                elif lista[1] == 3:
                    act = True

            # Función ppal que busca actualizaciones nuevas
            if act == True:
                lista[0] = True
                lista[1] = 4
                self.buscaActualizaciones()

    def buscaActualizaciones(self):
        '''Es la función encargada de buscar actualizaciones de las DBs y de econtrarse las aplica. También se ecarga de informar el estado por el panel de mensajes superior.'''
        self.Lista_Page_Ventas[37][0] = True
        V_Ventas.Mensaje_De_Actualizacion(self.ui, 4, self.Lista_Page_Ventas)
        list_result = act.consultaActualizaciones(mi_vs.MY_NAME)
        # Bandera por si hay que dar aviso de una actualización realizada
        name_act = ""
        # Bandera que indica que al menos se ha conectado a una DB
        conectado = False
        # Vamos a dar aviso en el programa que se buscaron actualizaciones, y si se conectó pero no encontró se avisará, y si se con
        for pos in list_result:
            if pos[0] == True:
                conectado = True
                if pos[1] == "upd_price":
                    self.updatePrice(pos[2], pos[3], pos[4])
                    name_act = pos[5]
                elif pos[1] == "replace_prod":
                    self.replaceDbProd(pos[2][0], pos[2][1])
                    name_act = pos[3]
        # TimeSleep para que el usuario alcance a ver que se está ejecutando una búsqueda, ya que si no hay conexiones disponibles disponibles ésto se ejecutaría el usuario no alcanzaría a verlo.
        time.sleep(10)
        self.Lista_Page_Ventas[37][0] = False
        if name_act != "":
            self.Lista_Page_Ventas[37][2] = name_act
        else:
            if conectado == False:
                self.Lista_Page_Ventas[37][1] = 0
        
        V_Ventas.Mensaje_De_Actualizacion(self.ui, self.Lista_Page_Ventas[37][1], self.Lista_Page_Ventas)


    def updatePrice(self, Lista, Date, nameUpdate):
        '''Ejecuta la actualización de precios. Para confirmar el cambio de precio de un producto, vamos a comparar la fecha y hora de la última actualización con respecto a la actualización que vamos a implementar producto por producto. En el caso de que se implementen todas las actualizaciones de una base de datos, vamos a colocar en su registro: "Hecho", de lo contrario, si en algunos productos no se ha realizado la actualización ya que hay una más reciente, vamos a colocar "Parcial" sin más detalles. Esto es suficiente para saber de que hubo alguna otra actualización en la red donde hemos actualizado con anterioridad y no vamos a sobreescribir un precio nuevo con uno viejo.'''
        # Lo que llega en la lista son las actualizaciones de cada producto conformada por otras listas de 2 posiciones: Codigo y Precio nuevo.
        # Usamos el valor pasado por parámetro Date para asegurarnos que debemos realizar la actualización.

        try:
            cont = 0
            for prod in Lista:
                dateCurrent, id_ = mdb_p.dateUpdate(prod[0])
                if self.comparaFechas(Date, dateCurrent):
                    mdb_p.Update_Price_Act(id_, Lista[1], nameUpdate, Date)
                else:
                    cont += 1
                largo = len(Lista)
                self.ui.label_upd.setText("[{}][{}/{}]".format(nameUpdate, cont, largo))
        except:
            self.ui.label_upd.setText("[{}][False]".format(nameUpdate))

    def comparaFechas(self, Date1, Date2):
        '''Las fechas que llegan deben tener el siguiente formato: AAAA-MM-DD HH:MM:SS. Como los valores están ordenados de mayor a menor, se realizan comparaciones de los mismos de izq a der, y una vez encontrado alguna diferencia devolvemos:
        True: Cuando Date1 > Date2.
        False: Cuando Date1 < Date2.
        En el caso de ser iguales, que debería ser muchísima coincidencia, devolvemos True.
        Y si alguna fecha no tiene un largo superior a 10 se considera que no es fecha. El número es elegido al azar, ya que debería venir una fecha correcta o una cadena vacía.'''

        # Si una cadena es menor a 10 caracteres entonces estamos en presencia de un producto que todavía no tiene fecha cargada. Y entendiendo que Date1 es la fecha de una actualización, por ende es correcta, directamente no la controlamos para evitar más cálculos.
        if len(Date2) < 10:
            return True

        # AÑO
        # Primero comparamos si existen diferencias entre los años, ya que es poco frecuente ésta situación, luego sí vamos a comparar su valor.
        if Date1[0:4] != Date2[0:4]:
            year1 = int(Date1[0:4])
            year2 = int(Date2[0:4])
            if year1 < year2:
                return False
            else:
                return True

        # MES
        month1 = int(Date1[5:7])
        month2 = int(Date2[5:7])
        if month1 > month2:
            return True
        else:
            if month1 < month2:
                return True
        
        # DÍA
        day1 = int(Date1[8:10])
        day2 = int(Date2[8:10])
        if day1 > day2:
            return True
        else:
            if day1 < day2:
                return True
        
        # HORA
        day1 = int(Date1[11:13])
        day2 = int(Date2[11:13])
        if day1 > day2:
            return True
        else:
            if day1 < day2:
                return True
        
        # MINUTO
        day1 = int(Date1[14:16])
        day2 = int(Date2[14:16])
        if day1 > day2:
            return True
        else:
            if day1 < day2:
                return True
        
        # SEGUNDO
        day1 = int(Date1[17:18])
        day2 = int(Date2[17:18])
        if day1 > day2:
            return True
        else:
            if day1 < day2:
                return True
        
        # IGUALDAD. Si llegamos a esta instacia es porque ambos valores son iguales, devolvemos True
        return True

    def replaceDbProd(self, Path, nameUp):
        '''Reemplaza una base de datos según el Path que viene por parámetro. IMPORTANTE: El Path sólo debe ser la carpeta, no requerimos el nombre de la db.'''
        nv.Copiar(Path + "/prod.db", "./sources/db/prod.db")
        mdb_p.Update_State_Value(Path + "/config.db", mi_vs.MY_NAME, "Hecho", nameUp)

    ############################################################ SOBRE LA APP ##########################################################
    ####################################################################################################################################
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
                # Botón Cargar de la vtn_Ventas. Debido a que al presionar Enter en el line_Monto genera que éste botón tenga el foco, necesitamos una bandera (pos [2]) que nos
                    # avise que el foco fue producido por otra acción para evitar que se ejecute el código.
                if self.ui.push_Cargar.hasFocus() and self.Lista_Page_Ventas[2] == 0:
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

    def resizeEvent(self, event):
        V_Ventas.Resize_Window(self.ui, self.Lista_Page_Ventas, Ventana=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())