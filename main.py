import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from PySide2 import QtWidgets
from PySide2.QtWidgets import QMainWindow, QMessageBox, QFileDialog
#rom vtn.vtn.vtn_productos import Ui_Productos
from PySide2.QtGui import QIcon, QPixmap, QFont
from PySide2.QtCore import QDir, Qt

from sources.vtn.mw_ppal import Ui_MainWindow

from sources.cls.Functions import *
from sources.cls.productos import *
from sources.cls.ventas import *
from sources.vtn.cla_botones import Boton
import sources.mod.vars as mi_vs
import sources.mod.func as func

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        func.Actualiza_Path()



        contraer = True

        # VARIABLES
        if contraer == True:
            # Expancion: indica cuál de todos los botones tiene el foco del 2do menu
            self.ex_productos = 0
            # Color de fondo del menu
            self.color_back_m = [185,185,185]
            # Color hover del menu
            self.color_hover_m = [125,125,125]
            # Color de fondo de los botones
            self.color_back_b = self.color_back_m
            # Color hover de los botones
            self.color_hover_b = self.color_hover_m
            # Height boton. Se coloca una altura mayor porque se ajusta a todas las pantallas separándose lo más posible según su altura.
            hb = 100
            # Widht boton
            wb = 60
            # Espacio para separar a los botones
            espacio = 0
            # Se usa ahora sólo para ir ubicando los botones que se vayan creando en un eje Y
            PosY = 0
            # Grosor del borde
            grosor = 0

        # CONFIGURACIONES
        if contraer == True:
            # MENUES
            #self.ui.frame_1.setStyleSheet("background-color: rgb({},{},{});".format(str(self.color_back_m[0]),str(self.color_back_m[1]),str(self.color_back_m[2])))
            self.ui.frame_1.setMinimumWidth(60)
            self.ui.frame_1.setMaximumWidth(60)
            self.ui.frame_menu1_btns.setMinimumWidth(60)
            self.ui.frame_menu1_btns.setMaximumWidth(450)

        # LISTAS UTILES DE LOS WIDGETS
        if contraer == True:
            self.lista_botones1 = [self.ui.push_1,self.ui.push_2,self.ui.push_3,self.ui.push_4,self.ui.push_5,self.ui.push_6,self.ui.push_7,self.ui.push_8,self.ui.push_9,self.ui.push_10]
            self.lista_btns1_texto = ["Expandir/Contraer","Ventas","Fijar","Fijar","Productos","Registros","Estadísticas","Contabilidad","Varios","Configuración"]
            self.lista_botones2 = [self.ui.push_11,self.ui.push_12,self.ui.push_13,self.ui.push_14,self.ui.push_15,self.ui.push_16,self.ui.push_17,self.ui.push_18,self.ui.push_19,self.ui.push_20]
            # Productos
            self.lista_btns5_texto = ["Cargar Productos","Reponer Stock","Promociones"]
            # Registros
            self.lista_btns6_texto = ["Reg. de Ventas"]
            # Estadísticas
            self.lista_btns7_texto = ["Por Periodos"]
            # Contabilidad
            self.lista_btns8_texto = ["Estado General", "Pasivos", "Activos", "Pagos", "Transferencias"]
            # Varios
            self.lista_btns9_texto = ["Usuarios"]
            # Configuración
            self.lista_btns10_texto = ["Cajas"]

        '''
                                                                                PAGINA VENTAS
        '''

        # ASIGNAMOS LA LISTA DE DATOS
        if contraer == True:

            self.Lista_Page_Ventas = []
            
            # VARIABLES QUE NO SE DEBEN MODIFICAR EN EJECUCIÓN
            # Es la cantidad de productos que vamos a dejar ver en las listas
            # Pos 0: CANT_WIDG
            self.Lista_Page_Ventas.append(13)

            # Pos 1: PRESION_ANTERIOR = 0
            self.Lista_Page_Ventas.append(0)
            # Pos 2: PRESION_ANTERIOR2 = ""
            self.Lista_Page_Ventas.append("")

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
            # Pos 8: .B_v2 = 0
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

        # CONFIGURACIONES DE WIDGETS
        if contraer == True:
            # Reacomodo los GroupBox que suplantan los mensajes para evitar la pérdida del foco.
            self.ui.groupBox_Ingresos.setGeometry( 485, 270, 361, 131)
            self.ui.groupBox_Promos.setGeometry( 485, 270, 361, 161)
            self.ui.groupBox_Ingresos.setVisible(False)
            self.ui.groupBox_Promos.setVisible(False)

            self.ui.push_Eliminar.clicked.connect(lambda: V_Ventas.Elimina_Item(self, self.ui, self.Lista_Page_Ventas))
            self.ui.push_Limpiar_Venta.clicked.connect(lambda: V_Ventas.Limpia_Ventana( self.ui, self.Lista_Page_Ventas))
            self.ui.push_Cargar.clicked.connect(self.Ventas_a_Carga_Fondo)
            self.ui.line_Codigo.textChanged.connect(lambda: V_Ventas.Change_line_Cod(self, self.ui, self.Lista_Page_Ventas))
            self.ui.line_Codigo.returnPressed.connect(lambda: V_Ventas.Return_line_Cod(self, self.ui, self.Lista_Page_Ventas))
            self.ui.line_Monto.textChanged.connect(lambda: V_Ventas.Change_line_Monto(self.ui, self.Lista_Page_Ventas))
            self.ui.listWidget_1.clicked.connect(lambda: V_Ventas.Seleccion_Listas(self.ui, 1))
            self.ui.listWidget_2.clicked.connect(lambda: V_Ventas.Seleccion_Listas(self.ui, 2))
            self.ui.listWidget_3.clicked.connect(lambda: V_Ventas.Seleccion_Listas(self.ui, 3))
            self.ui.listWidget_4.clicked.connect(lambda: V_Ventas.Seleccion_Listas(self.ui, 4))
            self.ui.listWidget_5.clicked.connect(lambda: V_Ventas.Seleccion_Listas(self.ui, 5))

            self.ui.line_Ingreso_Promo.returnPressed.connect(lambda: V_Ventas.Return_line_Promo(self, self.ui, self.Lista_Page_Ventas))
            self.ui.line_Ingresos.textChanged.connect(lambda: V_Ventas.Change_line_GB_Precio(self.ui))
            self.ui.line_Ingresos.returnPressed.connect(lambda: V_Ventas.Return_line_GB_Precio( self.ui, self.Lista_Page_Ventas))

            #self.Config_Mensaje(self.ui)

            self.ui.line_Codigo.setFocus()
            

        # ASIGNAMOS LOS EVENTOS DE LA VENTANA: VENTAS
        if contraer == True:
            pass


        '''
                                                                                PAGINA PRODUCTOS
        '''
        if contraer == True:
            # Pos 0  >>> BLOQUEO
            # Pos 1  >>> PNUEVO
            # Pos 2  >>> LISTA_FLOAT
            # Pos 3  >>> LISTA_PRODUCTO
            # Pos 4  >>> LISTA_STOCK
            # Pos 5  >>> LISTA_ADICIONALES
            # Pos 6  >>> LISTA_BD
            # Pos 7  >>> CONT_VER
            # Pos 8  >>> COD_EXTERNO
            # Pos 9  >>> CONJ_STOCK1
            # Pos 10 >>> CONJ_STOCK2
            # Pos 11 >>> CONJ_STOCK3
            # Pos 12 >>> CANT_CONJ
            self.Lista_Page_Productos = []
            # Pos 0 >>> BLOQUEO
            self.Lista_Page_Productos.append(False)
            # Variable que indica que se está creando un producto nuevo, sino la ventana tendrá un comportamiento erróneo en algunos casos
            # La única función que modifca su valor, es la que se ejecuta al intentar buscar un producto en la base de datos y cuando se limpia la pantalla
            #Pos 1 >>> PNUEVO
            self.Lista_Page_Productos.append(False)
            #: Lista que contiene todos los valores tipeados por el usuario
            # Pos 2 >>> LISTA_FLOAT
            self.LISTA_FLOAT = []
            self.Lista_Page_Productos.append(self.LISTA_FLOAT)
            # IMPORTANTE: Si se editan los tipos de datos de las listas, hay que corregir la función "Reinicia_Variables_Datos"
            # Pos 3 >>> LISTA_PRODUCTO
            self.LISTA_PRODUCTO = [0,"","",0.0,"","","",0]
            # Pos 4 >>> 
            self.LISTA_STOCK = [ 0.0, 0.0, 0.0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0]
            # Pos 5 >>> 
            self.LISTA_ADICIONALES = [ 0, 0, 0, 0.0, 0.0, 0.0, 0.0, "", 0.0, 0.0, 0]
            # Pos 6 >>> 
            self.LISTA_BD = []
            self.Lista_Page_Productos.append(self.LISTA_PRODUCTO)
            self.Lista_Page_Productos.append(self.LISTA_STOCK)
            self.Lista_Page_Productos.append(self.LISTA_ADICIONALES)
            self.Lista_Page_Productos.append(self.LISTA_BD)
            # Pos 7 >>> CONT_VER
            self.Lista_Page_Productos.append(0)
            # Cuando se viene desde otro lado con un código previo
            # Pos 8 >>> COD_EXTERNO
            self.Lista_Page_Productos.append("")
            # Listas que indican los estado de los conjuntos de stock. Hay una posición para Cantidad, Fecha y Precio de Costo.
            # Valores:
                # pos 0: Indica si ese conjunto se va a trabajar
                # pos 1: Indica si la cantidad ingresada es correcta
                # pos 2: Indica si la fecha es correcta
                # pos 3: Indica si el precio de costo es correcto
            self.CONJ_STOCK1 = [True, False, False, False]
            self.CONJ_STOCK2 = [False, False, False, False]
            self.CONJ_STOCK3 = [False, False, False, False]
            # Pos 9
            self.Lista_Page_Productos.append(self.CONJ_STOCK1)
            # Pos 10
            self.Lista_Page_Productos.append(self.CONJ_STOCK2)
            # Pos 11
            self.Lista_Page_Productos.append(self.CONJ_STOCK3)
            # Pos 12 >>> CANT_CONJ
            self.Lista_Page_Productos.append(1)
            # Pos 13 >>> BOTON_PRESIONADO
            # Valor que identifica el botón del Menú 1 que se presionó, pero sólo los que extienden la barra, de lo contrario vale 0
            self.Lista_Page_Productos.append(0)

        # RETURN PRESSED
        if contraer == True:
            # Hacemos que al presionar Enter, el foco vaya tmb moviéndose al igual que el tabulador
            self.ui.line_Cod_Bulto.returnPressed.connect(lambda: self.ui.line_Cant_Bulto.setFocus())
            self.ui.line_Cant_Bulto.returnPressed.connect(lambda: self.ui.line_Concepto.setFocus())
            self.ui.line_Concepto.returnPressed.connect(lambda: self.ui.line_Marca.setFocus())
            self.ui.line_Marca.returnPressed.connect(lambda: self.ui.line_Detalle.setFocus())
            self.ui.line_Detalle.returnPressed.connect(lambda: self.ui.combo_Uni_Medida.setFocus())
            #self.ui.combo_Uni_Medida.returnPressed.connect(lambda: self.ui.push_Buscar_Imagen.setFocus())
            #self.ui.push_Buscar_Imagen.returnPressed.connect(lambda: self.ui.push_Verificado.setFocus())
            self.ui.line_Pcio_Venta.returnPressed.connect(lambda: self.ui.line_Cant_1.setFocus())

            self.ui.line_Cant_1.returnPressed.connect(lambda: self.ui.line_Vto_1_D.setFocus())
            self.ui.line_Vto_1_D.returnPressed.connect(lambda: self.ui.line_Vto_1_M.setFocus())
            self.ui.line_Vto_1_M.returnPressed.connect(lambda: self.ui.line_Vto_1_A.setFocus())
            self.ui.line_Vto_1_A.returnPressed.connect(lambda: self.ui.line_Pcio_Costo_1.setFocus())
            self.ui.line_Pcio_Costo_1.returnPressed.connect(lambda: self.ui.line_Cant_2.setFocus())

            self.ui.line_Cant_2.returnPressed.connect(lambda: self.ui.line_Vto_2_D.setFocus())
            self.ui.line_Vto_2_D.returnPressed.connect(lambda: self.ui.line_Vto_2_M.setFocus())
            self.ui.line_Vto_2_M.returnPressed.connect(lambda: self.ui.line_Vto_2_A.setFocus())
            self.ui.line_Vto_2_A.returnPressed.connect(lambda: self.ui.line_Pcio_Costo_2.setFocus())
            self.ui.line_Pcio_Costo_2.returnPressed.connect(lambda: self.ui.line_Cant_3.setFocus())

            self.ui.line_Cant_3.returnPressed.connect(lambda: self.ui.line_Vto_1_D.setFocus())
            self.ui.line_Vto_3_D.returnPressed.connect(lambda: self.ui.line_Vto_1_M.setFocus())
            self.ui.line_Vto_3_M.returnPressed.connect(lambda: self.ui.line_Vto_1_A.setFocus())
            self.ui.line_Vto_3_A.returnPressed.connect(lambda: self.ui.line_Pcio_Costo_1.setFocus())
            self.ui.line_Pcio_Costo_3.returnPressed.connect(lambda: self.ui.push_Quitar_Conjunto.setFocus())

            #self.ui.line_Siniestro.returnPressed.connect(lambda: self.ui.line_Sin_Cobrar.setFocus())
            #self.ui.line_Sin_Cobrar.returnPressed.connect(lambda: self.ui.line_Incremento.setFocus())
            self.ui.line_Incremento.returnPressed.connect(lambda: self.ui.line_Cant_Preav.setFocus())
            self.ui.line_Cant_Preav.returnPressed.connect(lambda: self.ui.line_Cant_Max.setFocus())
            self.ui.line_Cant_Max.returnPressed.connect(lambda: self.ui.line_Dias_Preav.setFocus())
            self.ui.line_Dias_Preav.returnPressed.connect(lambda: self.ui.push_Guardar.setFocus())

        # GroupBox Productos
        if contraer == True:
            self.ui.line_Codigo_2.returnPressed.connect(lambda: V_Productos.Carga_Info_Ventana(self, self.ui, self.Lista_Page_Productos))
            self.ui.line_Cod_Bulto.textChanged.connect(lambda: V_Productos.F_Line_Codigo_Bulto(self.ui, self.Lista_Page_Productos))
            self.ui.line_Cant_Bulto.textChanged.connect(lambda: V_Productos.F_Line_Cantidad_Bulto(self.ui, self.Lista_Page_Productos))
            self.ui.line_Concepto.textChanged.connect(lambda: V_Productos.F_Line_Concepto(self.ui, self.Lista_Page_Productos))
            self.ui.line_Marca.textChanged.connect(lambda: V_Productos.F_Line_Marca(self.ui, self.Lista_Page_Productos))
            self.ui.combo_Uni_Medida.currentIndexChanged.connect(lambda: V_Productos.F_Combo_Medida(self.ui, self.Lista_Page_Productos))
            self.ui.line_Detalle.textChanged.connect(lambda: V_Productos.F_Line_Detalle(self.ui, self.Lista_Page_Productos))
            self.ui.push_Buscar_Imagen.clicked.connect(V_Productos.F_Btn_Buscar_Imagen)

        # GroupBox Stock
        if contraer == True:
            self.ui.push_Verificado.clicked.connect(V_Productos.Btn_Verificado)
            self.ui.line_Pcio_Venta.textChanged.connect(lambda: V_Productos.Line_Precio_Venta(self.ui, self.Lista_Page_Productos))
            
            self.ui.line_Cant_1.textChanged.connect(lambda: V_Productos.Line_Cantidad_1(self.ui, self.Lista_Page_Productos))
            self.ui.line_Vto_1_D.textChanged.connect(lambda: V_Productos.Line_Fecha_Dia_1(self.ui, self.Lista_Page_Productos))
            self.ui.line_Vto_1_M.textChanged.connect(lambda: V_Productos.Line_Fecha_Mes_1(self.ui, self.Lista_Page_Productos))
            self.ui.line_Vto_1_A.textChanged.connect(lambda: V_Productos.Line_Fecha_Ano_1(self.ui, self.Lista_Page_Productos))
            self.ui.line_Pcio_Costo_1.textChanged.connect(lambda: V_Productos.Line_Precio_Costo_1(self.ui, self.Lista_Page_Productos))
            
            self.ui.line_Cant_2.textChanged.connect(lambda: V_Productos.Line_Cantidad_2(self.ui, self.Lista_Page_Productos))
            self.ui.line_Vto_2_D.textChanged.connect(lambda: V_Productos.Line_Fecha_Dia_2(self.ui, self.Lista_Page_Productos))
            self.ui.line_Vto_2_M.textChanged.connect(lambda: V_Productos.Line_Fecha_Mes_2(self.ui, self.Lista_Page_Productos))
            self.ui.line_Vto_2_A.textChanged.connect(lambda: V_Productos.Line_Fecha_Ano_2(self.ui, self.Lista_Page_Productos))
            self.ui.line_Pcio_Costo_2.textChanged.connect(lambda: V_Productos.Line_Precio_Costo_2(self.ui, self.Lista_Page_Productos))

            self.ui.line_Cant_3.textChanged.connect(lambda: V_Productos.Line_Cantidad_3(self.ui, self.Lista_Page_Productos))
            self.ui.line_Vto_3_D.textChanged.connect(lambda: V_Productos.Line_Fecha_Dia_3(self.ui, self.Lista_Page_Productos))
            self.ui.line_Vto_3_M.textChanged.connect(lambda: V_Productos.Line_Fecha_Mes_3(self.ui, self.Lista_Page_Productos))
            self.ui.line_Vto_3_A.textChanged.connect(lambda: V_Productos.Line_Fecha_Ano_3(self.ui, self.Lista_Page_Productos))
            self.ui.line_Pcio_Costo_3.textChanged.connect(lambda: V_Productos.Line_Precio_Costo_3(self.ui, self.Lista_Page_Productos))

            self.ui.push_Quitar_Conjunto.clicked.connect(V_Productos.Boton_Restar_Cj)
            self.ui.push_Agregar_Conjunto.clicked.connect(V_Productos.Boton_Sumar_Cj)

        # GroupBox Detalles Adicionales
        if contraer == True:
            self.ui.combo_Caja.currentIndexChanged.connect(lambda: V_Productos.Combo_Caja_Asociada(self.ui, self.Lista_Page_Productos))
            self.ui.combo_Mayorista.currentIndexChanged.connect(lambda: V_Productos.ComboBox_Mayorista(self.ui, self.Lista_Page_Productos))
            #self.ui.line_Siniestro.textChanged.connect(self.LineEdit_Siniestro)
            #self.ui.line_Sin_Cobrar.textChanged.connect(self.LineEdit_Sin_Cobrar)
            self.ui.line_Incremento.textChanged.connect(lambda: V_Productos.Line_Porc_Incremento(self.ui, self.Lista_Page_Productos))
            self.ui.line_Cant_Preav.textChanged.connect(lambda: V_Productos.Line_Cant_Preaviso(self.ui, self.Lista_Page_Productos))
            self.ui.line_Cant_Max.textChanged.connect(lambda: V_Productos.Line_Cant_Maxima(self.ui, self.Lista_Page_Productos))
            self.ui.line_Dias_Preav.textChanged.connect(lambda: V_Productos.Line_Dias_Preaviso(self.ui, self.Lista_Page_Productos))

            # BOTONES GUARDAR, ELIMINAR, LIMPIAR Y RECORRIDO INICIAL
            self.ui.push_Guardar.clicked.connect(V_Productos.Btn_Guardar)
            self.ui.push_Eliminar.clicked.connect(V_Productos.Btn_Eliminar)
            self.ui.push_Reco_Inicial.clicked.connect(V_Productos.Btn_Recorrido_Inicial)
            self.ui.push_Limpiar.clicked.connect(lambda: V_Productos.Limpia_Ventana(Inicia_P_Nuevo=False, Mantiene_Cod=False))

        # CARGA DE LOS COMBO BOX
        if contraer == True:
            # Combo Unidad de Medida
            # Debido a que la unidad de medición siempre va a estar dada por 3 valores únicamente, los cargamos ahora. Agrego cm3 para prevenir únicamente
            self.ui.combo_Uni_Medida.addItem("Seleccione Medida")
            self.ui.combo_Uni_Medida.addItem("Unidad")
            self.ui.combo_Uni_Medida.addItem("Peso - Kilogramos")
            self.ui.combo_Uni_Medida.addItem("Litros")
            self.ui.combo_Uni_Medida.addItem("cm3")
            self.ui.combo_Uni_Medida.addItem("Precio")

            # Combo Cajas
            self.ui.combo_Caja.addItem("Seleccione Caja")
            tabla = mdb_gen.Dev_Tabla(mi_vs.BASE_GENERAL_PPAL, "Cajas", OrdenBy = "Orden")
            for i in tabla:
                if i[1] > 0:
                    self.ui.combo_Caja.addItem(i[2])

            # Combo Proveedores
            Mayo = 0
            tabla = mdb_gen.Dev_Tabla(mi_vs.BASE_VARIOS_PPAL, "Proveedores", OrdenBy = "Orden")
            for i in tabla:
                if i[1] > 0:
                    Mayo += 1
                    if Mayo == 1:
                        self.ui.combo_Mayorista.addItem("Selecc. Proveedor")
                    self.ui.combo_Mayorista.addItem(i[2])
            if Mayo == 0:
                self.ui.combo_Mayorista.addItem("No hay datos")

        #self.ui.push_Buscar.clearFocus()
        #self.ui.line_Codigo.setFocus()

        # ASIGNAMOS LAS FUNCIONES A LOS BOTONES
        if contraer == True:
            self.ui.push_1.clicked.connect(lambda: UIFunctions_Menu.Boton_1(self.ui, 60, 280, self.lista_botones1, self.lista_btns1_texto))
            self.ui.push_2.clicked.connect(lambda: self.Boton_presionado(2))
            self.ui.push_3.clicked.connect(lambda: UIFunctions_Menu.Boton_Op1(self.ui))
            self.ui.push_4.clicked.connect(lambda: UIFunctions_Menu.Boton_Op2(self.ui))
            self.ui.push_5.clicked.connect(lambda: self.Boton_presionado(5))
            self.ui.push_6.clicked.connect(lambda: self.Boton_presionado(6))
            self.ui.push_7.clicked.connect(lambda: self.Boton_presionado(7))
            self.ui.push_8.clicked.connect(lambda: self.Boton_presionado(8))
            self.ui.push_9.clicked.connect(lambda: self.Boton_presionado(9))
            self.ui.push_10.clicked.connect(lambda: self.Boton_presionado(10))

        # ASIGNAMOS LAS FUNCIONES DE LOS BOTONES DEL MENU 2
        if contraer == True:
            self.ui.push_11.clicked.connect(lambda: UIFunctions_Menu.Seleccion_Pages(self.ui, self.ui.push_11.text()))
            self.ui.push_12.clicked.connect(lambda: UIFunctions_Menu.Seleccion_Pages(self.ui, self.ui.push_12.text()))
            self.ui.push_13.clicked.connect(lambda: UIFunctions_Menu.Seleccion_Pages(self.ui, self.ui.push_13.text()))
            self.ui.push_14.clicked.connect(lambda: UIFunctions_Menu.Seleccion_Pages(self.ui, self.ui.push_14.text()))
            self.ui.push_15.clicked.connect(lambda: UIFunctions_Menu.Seleccion_Pages(self.ui, self.ui.push_15.text()))
            self.ui.push_16.clicked.connect(lambda: UIFunctions_Menu.Seleccion_Pages(self.ui, self.ui.push_16.text()))
            self.ui.push_17.clicked.connect(lambda: UIFunctions_Menu.Seleccion_Pages(self.ui, self.ui.push_17.text()))
            self.ui.push_18.clicked.connect(lambda: UIFunctions_Menu.Seleccion_Pages(self.ui, self.ui.push_18.text()))
            self.ui.push_19.clicked.connect(lambda: UIFunctions_Menu.Seleccion_Pages(self.ui, self.ui.push_19.text()))
            self.ui.push_20.clicked.connect(lambda: UIFunctions_Menu.Seleccion_Pages(self.ui, self.ui.push_20.text()))

        #self.Imprimir()

        #    Configuramos la pantalla
        self.Config(wb, hb)
        self.show()
    
    # Configuración de los botones del 1er menú y el alto del Menu 2
    def Config(self, ancho, alto):
        # Btn Expandir Menú
        self.ui.push_1.setText("")
        self.ui.push_1.setIcon(QtGui.QIcon(r"./sources\img\men.png"))
        self.ui.push_1.setIconSize(QtCore.QSize(ancho,alto))
        # Btn Ventas
        self.ui.push_2.setText("")
        self.ui.push_2.setIcon(QtGui.QIcon(r"./sources\img\vts.png"))
        self.ui.push_2.setIconSize(QtCore.QSize(ancho,alto))
        # Btn Clip 1
        self.ui.push_3.setText("")
        self.ui.push_3.setIcon(QtGui.QIcon(r"./sources\img\clp.png"))
        self.ui.push_3.setIconSize(QtCore.QSize(ancho,alto))
        # Btn Clip 2
        self.ui.push_4.setText("")
        self.ui.push_4.setIcon(QtGui.QIcon(r"./sources\img\clp.png"))
        self.ui.push_4.setIconSize(QtCore.QSize(ancho,alto))
        # Btn Productos
        self.ui.push_5.setText("")
        self.ui.push_5.setIcon(QtGui.QIcon(r"./sources\img\pro.png"))
        self.ui.push_5.setIconSize(QtCore.QSize(ancho,alto))
        # Btn Registros
        self.ui.push_6.setText("")
        self.ui.push_6.setIcon(QtGui.QIcon(r"./sources\img\reg.png"))
        self.ui.push_6.setIconSize(QtCore.QSize(ancho,alto))
        # Btn Registros
        self.ui.push_7.setText("")
        self.ui.push_7.setIcon(QtGui.QIcon(r"./sources\img\est.png"))
        self.ui.push_7.setIconSize(QtCore.QSize(ancho,alto))
        # Btn Estadísticas
        self.ui.push_8.setText("")
        self.ui.push_8.setIcon(QtGui.QIcon(r"./sources\img\gen.png"))
        self.ui.push_8.setIconSize(QtCore.QSize(ancho,alto))
        # Btn Estado General
        self.ui.push_9.setText("")
        self.ui.push_9.setIcon(QtGui.QIcon(r"./sources\img\mas.png"))
        self.ui.push_9.setIconSize(QtCore.QSize(ancho,alto))
        # Btn Configuración
        self.ui.push_10.setText("")
        self.ui.push_10.setIcon(QtGui.QIcon(r"./sources\img\cnf.png"))
        self.ui.push_10.setIconSize(QtCore.QSize(ancho,alto))
        
        self.ui.frame_2.setFixedSize(0,600)

    # Función llamada cuando se presiona algún botón del 1er menú
    def Boton_presionado(self, Id):
        lista_Aux = []
        if Id == 2:
            ancho1 = self.ui.frame_menu1_btns.width()
            ancho2 = self.ui.frame_menu2_btns.width()
            if ancho1 > 60:
                UIFunctions_Menu.Boton_1(self.ui, 60, 280, self.lista_botones1, self.lista_btns1_texto)
            if ancho2 > 0:
                UIFunctions_Menu.Boton_Extiende_Menu2(self.ui, 250, 0, 0, [], [])
            self.Lista_Page_Productos[13] = 0
            V_Ventas.Mostrar(self.ui)
            return
        if Id == 5:
            lista_Aux = self.lista_btns5_texto
        if Id == 6:
            lista_Aux = self.lista_btns6_texto
        if Id == 7:
            lista_Aux = self.lista_btns7_texto
        if Id == 8:
            lista_Aux = self.lista_btns8_texto
        if Id == 9:
            lista_Aux = self.lista_btns9_texto
        if Id == 10:
            lista_Aux = self.lista_btns10_texto
        self.Lista_Page_Productos[13] = UIFunctions_Menu.Boton_Extiende_Menu2(self.ui, 250, self.Lista_Page_Productos[13], Id, self.lista_botones2, lista_Aux)

    '''
                                                                                BOTONES DE NAVEGACIÓN
    '''

    # Desde la ventana de Ventas, a la ventana de finalización de una venta donde se cargan los fondos
    def Ventas_a_Carga_Fondo(self):        
        ''' Cambia de la ventana de Ventas a Carga Fondos. '''

        if len(self.Lista_Page_Ventas[21]) > 0:
            '''
            self.Ventana_Carga_Fondos.DICCIONARIO_CON_LISTA = self.Ventana_Ventas.LISTA_VENTA_REAL
            self.Ventana_Carga_Fondos.Mostrar()
            '''
            UIFunctions_Menu.Seleccion_Pages(self.ui, "Carga Fondos")
        else:
            QMessageBox.question(self,"Aviso", "No hay ventas para cargar", QMessageBox.Ok)

    # Función auxiliar que utilicé para arreglar las animaciones
    def Imprimir(self):
        # Asignamos funciones a los botones de paginas
        #self.ui.push_sub2_1_reponer.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        print("\nSTACKED:")
        print("width: {}".format(str(self.ui.stackedWidget.width())))
        print("height: {}".format(str(self.ui.stackedWidget.height())))
        print("X: {}".format(str(self.ui.stackedWidget.pos().x())))
        print("Y: {}".format(str(self.ui.stackedWidget.pos().y())))
        print("\nFRAME1:")
        print("width: {}".format(str(self.ui.frame_menu1_btns.width())))
        print("height: {}".format(str(self.ui.frame_menu1_btns.height())))
        print("X: {}".format(str(self.ui.frame_menu1_btns.pos().x())))
        print("Y: {}".format(str(self.ui.frame_menu1_btns.pos().y())))
        print("\nFRAME2:")
        print("width: {}".format(str(self.ui.frame_2.width())))
        print("height: {}".format(str(self.ui.frame_2.height())))
        print("X: {}".format(str(self.ui.frame_2.pos().x())))
        print("Y: {}".format(str(self.ui.frame_2.pos().y())))
        print("\nFRAME2:")
        print("width: {}".format(str(self.ui.frame_menu2_btns.width())))
        print("height: {}".format(str(self.ui.frame_menu2_btns.height())))
        print("X: {}".format(str(self.ui.frame_menu2_btns.pos().x())))
        print("Y: {}".format(str(self.ui.frame_menu2_btns.pos().y())))
        print("\nBTN:")
        print("width: {}".format(str(self.ui.push_1.width())))
        print("height: {}".format(str(self.ui.push_1.height())))
        print("X: {}".format(str(self.ui.push_1.pos().x())))
        print("Y: {}".format(str(self.ui.push_1.pos().y())))
        print("\nBTN:")
        print("width: {}".format(str(self.ui.push_12.width())))
        print("height: {}".format(str(self.ui.push_12.height())))
        print("X: {}".format(str(self.ui.push_12.pos().x())))
        print("Y: {}".format(str(self.ui.push_12.pos().y())))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())