'''
HACIENDO:
ÚLTIMO BUG QUE NO PUDE SOLUCIONAR NOMBRADO EN UN COMMIT PERO EN ESE COMMIT YO TODAVÍA NO HABÍA ESCRITO ÉSTE TEXTO:
    - Luego de haber seleccionado una promo, cuando uno quiere crear un producto nuevo no le quita el checked a los radiobuttons. El problema es que después el usuario puede
        que coincida su decisión con el radiobutton que haya quedado seleccionado y puede que crea que está hecho, pero en la variable no hay un valor establecido, así que
        sin explicarle el xq, el programa le avisa que le faltan datos. Lo ideal sería que al limpiar la ventana se pueda quitar el check de ambos radiobuttons.


DEBO CONVERTIR LOS VALORES DE CANTIDAD DE FLOAT A INT, EN EL CASO DE QUE QUIERA INCORPORAR UNA PROMO CON DECIMALES COMO SER ALGO QUE TENGA QUE VER CON KILOGRAMOS  O LITROS O ALGO ASÍ, DEBERÍA SER UNA NUEVA PROMO. EL TEMA ES QUE HAY CONTADORES QUE ESTÁN DENTRO DE BUCLES IMPORTANTES, DONDE NO PUEDE RECORRERSE SI EL VALOR ES FLOAT EN VEZ DE INT. Al momento la línea con problema es 499: Tope2 es float y no int.
SI UNA PROMO SE DESACTIVA, QUITAR SU VALOR DEL DATO DE CADA PRODUCTO, Y VICEVERSA.
EL PROGRAMA NO PERMITE MODIFICAR WIDGETS CUANDO LA VARIABLE DE CONTROL NO ESTÁ COMPLETA, CUESTIÓN QUE ESO DIFICULTA LA ACTIVIDAD DE RELLENO DE VENTANA
LLAMAR A LA FUNCÍÓN Control_Datos_En_Pantalla TANTAS VEQCES SEA NECESARIA, CADA VEZ QE CAMBIA EL VALOR DE SU VARIABLE
TENGO QUE CREAR UNA FUNCIÓN QUE CALCULE LOS VALORES EN PANTALLA, PARA IR ACTUALIZANDO CADA VEZ QUE SE CAMBIAN DATOS COMO PRECIO, PRODUCTOS, CANT, ETC. Y LUEGO REALIZAR EL LLAMADO A LA FUNCIÓN TANTAS VECES COMO SEA NECEASRIO

INCORPORANDO:
    * Cambiò el formato que guarda los detalles de una promo, donde el $ indica la cantidad total necesaria de productos ya que ahora el tipo 1 de promo acepta varios produc.
    * Incorporando el código del producto en vez de los IDs
    * Adaptación a la nueva estructura, donde el código de la promo es de tipo texto. Si bien lo vamos a dejar numérica por el momento, la idea es agregarle quizás la letra P
        delante para ir dejando sólo códigos numéricos a los productos, ya que si se incorpora esas balanzas con ticket, seguro tengamos que adaptarnos a los ticket que la
        balanza genera por su cuenta y son sólo numéricos.
    * No corresponde acá, pero anoto igual para no olvidarme. Incorporar de prueba un beep en la carga de ventas cada vez que se lee un código, para no tener la necesidad de
        tener que estar mirando la pantalla y controlar si el producto pasó o no.
    * Adaptación al cambio en cada producto ya que ahora le indicamos en el mismo a qué promo pertenecen. Además, cuando se elimina una promo o se desactiva hay que borrar
        la promo del producto ya que si un producto tiene algo escrito en su casilla, entonces es porque tiene promo activa.
    * Incorporar un 3er tipo de promo como lo es de ejemplo la promo 3 cocas y un fernet.
    * Que se puedan activar y desactivar las promos.
    * Que se pueda limpiar pantalla.
    * QUe se pueda eliminar una promo.
    * Que se pueda agregar y/o quitar un producto de una promo.
    * Que en la lista de promos se vea si un producto está activado y/o desactivado.
    * Ajustar la lista de promos xq nos excedemos de su capacidad, alcanza para 18 productos.
    * No borrar nada de todo esto así lo podemos ajustar en la aplicación de actualización.
    * Ajustar el foco con tarjetas de crédito.
    * Registro de ventas.
    * Incorporar el scrollbar, el sistema para manipular muchos items en las listas.
'''

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog
from vtn.vtn.vtn_promociones import Ui_Promociones

import source.mod.mdbprom as mdbprom
import source.mod.mdbprod as mdbprod
import source.mod.func as mi_func
import source.mod.form as form

class V_Promociones(QMainWindow):
    def __init__(self):
        super(V_Promociones, self).__init__()
        self.ui = Ui_Promociones()
        self.ui.setupUi(self)

        self.ui.groupBox_4.setEnabled(False)
        
        # Variable de control para creación o Edición de una promo. Su numeración va avanzando a medida que van cumpliendo los pasos
        self.CONTROL_GRAL = 0
        # Por el momento tenemos 2 tipos de promos, la que tiene uno o varios productos fijos, y la que tiene combinaciones de productos. Esta variable indica ese dato
            # de la promo que estemos observando actualmente. 
            # Al mismo tiempo la estoy usando como bandera para asegurarme que se haya elegido alguna promo y esté cargada en ventana, cuando vale 0 es xq no hay nada seleccio.
        self.TIPO_ACTUAL = 0
        # 0: Desactivado - 1: Activado - 2: Sin Valor
        self.ACTIVACION = 2
        # Agendamos en el orden que se crea la lista de promociones, la listas de ID de las mismas obtenidas de la tabla de Promos
        self.lista_id_promos =  []
        # Las listas en pantalla con muchos elementos no coordinan correctamente, por ende vamos a mostrar en pantalla las que se pueden ver bien y el resto lo actualizamos
        # con funciones sobre la barra lateral. A este límite lo manejamos con una variable para poder ser adaptado en otras pantallas con facilidad.
        self.LIMITE_LISTA = 500

        self.LISTA_COD_PROMO1 = []
        self.LISTA_CAN_PROMO1 = []
        # Es el concepto del producto
        self.LISTA_CON_PROMO1 = []
        # Precio calculado en proporción a lo que cuesta y el valor de la promo. Su valor equivale a su precio * la cantidad de productos.
        self.LISTA_PRE_PROMO1 = []
        # Precio de costo del producto, lo que llamo en las variables "PrecioIndividual", sin importar la cantidad de productos que tenga.
        self.LISTA_PRE_COSTO1 = []
        self.PRE_TOTAL1 = 0.0

        self.LISTA_COD_PROMO2 = []
        self.LISTA_CON_PROMO2 = []
        self.LISTA_PRE_PROMO2 = []
        self.LISTA_PRE_COSTO2 = []
        self.CANT_PROMO2 = 0
        self.PRE_TOTAL2 = 0.0

        # Colores predeterminados para los botones de: activado, desactivado, seleccionado y cuando están en gris
        self.Ra = 0
        self.Ga = 255
        self.Ba = 0
        self.Rd = 255
        self.Gd = 0
        self.Bd = 0
        self.Rs = 0
        self.Gs = 0
        self.Bs = 255
        self.Rg = 180
        self.Gg = 180
        self.Bg = 180

        # Variable que bloquea o habilita el uso de los radiobuttons
        self.RADIO = True
        # Variable para los Line
        self.LINE = True

        # Actualizamos las listas de Promociones
        self.Actualiza_lista_Promo()

        '''
        self.ui.verticalScrollBar.setMinimum(0)
        self.ui.verticalScrollBar.setMaximum(0)
        self.ui.verticalScrollBar.valueChanged.connect(lambda: self.Refresca_Listas(scrol = self.ui.verticalScrollBar.value()))
        
        # VARIABLES
        self.SCROLL_BLOQUEO = False
        '''

        self.ui.line_Codigo.textChanged.connect(self.Line_Change_Codigo)
        self.ui.line_Nombre.textChanged.connect(self.Line_Change_Nombre)
        self.ui.line_cant.textChanged.connect(self.Line_Cant_Change)
        self.ui.line_precio.textChanged.connect(self.Line_Precio_Change)

        self.ui.push_guardar.clicked.connect(self.Clic_Btn_Guarda_Promo)
        self.ui.push_agregar.clicked.connect(self.Carga_Prod_Tipo)
        self.ui.list_nombre.clicked.connect(self.Clic_Listas)
        self.ui.push_limpiar.clicked.connect(lambda: self.Limpia_Ventana(True))
        self.ui.push_activar.clicked.connect(self.Activar)
        self.ui.push_desactivar.clicked.connect(self.Desactivar)
        self.ui.radio_Fijos.clicked.connect(self.Clic_Fijos)
        self.ui.radio_Combinacion.clicked.connect(self.Clic_Combinacion)

    '''#############################################################################################################################################
                                                            FUNCIONES DE SCROL
    #############################################################################################################################################'''

    # Limpia y refresca los datos de todas las listas en pantalla y refresca el índice que mostramos en el listWidget1, ya que si por ej se ha borrado un item estos cambian.
    def Refresca_Listas(self, scrol = 0):

        # Esta variable es True sólo cuando se asigna por primera vez el valor del scrollbar, pero llama a ésta función y no debe ejecutarse xq luego se vuelve a llamar a ésta
            # misma función pero con un nuevo valor
        if self.SCROLL_BLOQUEO == False:

            # Limpiamos todas las listas
            self.ui.list_nombre.clear()
            self.ui.list_activacion.clear()

            largo = len(self.LISTA_VENTA_MOSTRADA)
            # ReEnumeramos los valores de índice que se cargan en la primer lista
            for i in range(largo):
                self.LISTA_VENTA_MOSTRADA[i][0] = str(i + 1)

            # Si los ítems entran en pantalla, los cargamos de manera normal, de lo contrario, cargamos los últimos ítems
            if largo > self.CANT_WIDG:

                # Ahora miramos si el valor máximo de la scrollbar es correcto, porque si se han eliminado productos, el largo debe ajustarse
                largoLW = self.ui.verticalScrollBar.maximum()
                if (largoLW - 1) > (largo - self.CANT_WIDG):
                    if self.ui.verticalScrollBar.value() == largoLW:
                        self.SCROLL_BLOQUEO = True
                        maximo = largo - self.CANT_WIDG + 1
                        self.ui.verticalScrollBar.setValue(maximo)
                        self.ui.verticalScrollBar.setMaximum(maximo)
                        scrol = maximo
                        self.SCROLL_BLOQUEO = False                        

                if scrol == 0:
                    for i in range(self.CANT_WIDG):
                        self.ui.listWidget_1.addItem(self.LISTA_VENTA_MOSTRADA[-(self.CANT_WIDG - i)][0])
                        self.ui.listWidget_2.addItem(self.LISTA_VENTA_MOSTRADA[-(self.CANT_WIDG - i)][1])
                        self.ui.listWidget_3.addItem(self.LISTA_VENTA_MOSTRADA[-(self.CANT_WIDG - i)][2])
                        self.ui.listWidget_4.addItem(self.LISTA_VENTA_MOSTRADA[-(self.CANT_WIDG - i)][3])
                        self.ui.listWidget_5.addItem(self.LISTA_VENTA_MOSTRADA[-(self.CANT_WIDG - i)][4])
                else:
                    for i in range((scrol - 1), (scrol + self.CANT_WIDG - 1)):
                        self.ui.listWidget_1.addItem(self.LISTA_VENTA_MOSTRADA[i][0])
                        self.ui.listWidget_2.addItem(self.LISTA_VENTA_MOSTRADA[i][1])
                        self.ui.listWidget_3.addItem(self.LISTA_VENTA_MOSTRADA[i][2])
                        self.ui.listWidget_4.addItem(self.LISTA_VENTA_MOSTRADA[i][3])
                        self.ui.listWidget_5.addItem(self.LISTA_VENTA_MOSTRADA[i][4])
            else:
                # Si está habilitada la barra hay que deshabilitarla
                if self.ui.verticalScrollBar.value() > 0:
                    self.SCROLL_BLOQUEO = True
                    self.ui.verticalScrollBar.setMinimum(0)
                    self.ui.verticalScrollBar.setValue(0)
                    self.ui.verticalScrollBar.setMaximum(0)
                for sub in self.LISTA_VENTA_MOSTRADA:
                    self.ui.listWidget_1.addItem(sub[0])
                    self.ui.listWidget_2.addItem(sub[1])
                    self.ui.listWidget_3.addItem(sub[2])
                    self.ui.listWidget_4.addItem(sub[3])
                    self.ui.listWidget_5.addItem(sub[4])
            self.Reinicio_Vtn_Parcial()
    
    '''#############################################################################################################################################
                                                            FUNCIONES DE VENTANA
    #############################################################################################################################################'''

    # Función que muestra la ventana
    def Mostrar(self):
        self.show()

    # Limpia la pantalla sin limpiar las listas y la variable (lista_id_promos), pero deja las listas de promos sin selección
    def Limpia_Ventana(self, Limpia_Cod = True):

        self.LINE = False
        self.RADIO = False
        
        self.CONTROL_GRAL = 0
        self.TIPO_ACTUAL = 0
        self.ACTIVACION = 2

        self.LISTA_COD_PROMO1 = []
        self.LISTA_CAN_PROMO1 = []
        self.LISTA_CON_PROMO1 = []
        self.LISTA_PRE_PROMO1 = []
        self.LISTA_PRE_COSTO1 = []
        self.PRE_TOTAL1 = 0.0

        self.LISTA_COD_PROMO2 = []
        self.LISTA_CON_PROMO2 = []
        self.LISTA_PRE_PROMO2 = []
        self.LISTA_PRE_COSTO2 = []
        self.CANT_PROMO2 = 0
        self.PRE_TOTAL2 = 0.0

        self.ui.list_nombre.setCurrentRow(-1)
        self.ui.list_activacion.setCurrentRow(-1)

        if Limpia_Cod == True: self.ui.line_Codigo.clear()
        self.ui.line_Nombre.clear()

        self.ui.radio_Fijos.setChecked(False)
        self.ui.radio_Combinacion.setChecked(False)

        self.ui.line_cant.clear()
        self.ui.line_precio.clear()
        self.ui.list_Productos.clear()

        '''
        self.ui.check_Fin_Stock_Tot.setChecked(False)
        self.ui.check_Fin_Stock_Asig.setChecked(False)
        self.ui.check_Fin_Fecha.setChecked(False)
        self.ui.label_fecha_ini.setText("-")
        self.ui.label_fecha_fin.setText("-")
        '''

        self.Estado_Activacion(2)
        self.LINE = True
        self.RADIO = True

        self.ui.line_Codigo.setFocus()

    # Actualiza únicamente los datos de la lista que contiene las promociones (o sea los 2 listwidgets)
    def Actualiza_lista_Promo(self):
        # Limpiamos las variables asociadas a los listwidgets y los listwidgets
        self.lista_id_promos = []
        self.ui.list_nombre.clear()
        self.ui.list_activacion.clear()
        # Limpiamos los demás widgets
        self.Limpia_Ventana()
        # Obtenemos los datos y rellenamos las listas
        Tabla = mdbprom.Dev_Tabla("Promos", "Codigo")
        # Debido a que ponemos en orden todos los producto dejando al final los desactivados, guardamos los datos necesarios de aquellos que estén desactivados para agregarlos
            # después de cargar los que están activados
        lista_Ceros = []
        lista_id_aux = []
        lista_activado = []
        # Cargamos los datos que corresponden y guardamos a parte aquellos que corresponden a Promos que están desactivadas para ser cargadas en otro bucle luego de éste
        for reg in Tabla:
            Nombre = "(" + reg[1] + ") - " + reg[2]
            activa = "ACTIVADO"
            if reg[14] == 0:
                activa = "Desactivado"
                lista_Ceros.append(Nombre)
                lista_id_aux.append(reg[0])
                lista_activado.append(activa)
            else:
                if len(self.ui.list_nombre) <= self.LIMITE_LISTA:
                    self.ui.list_nombre.addItem(Nombre)
                    self.ui.list_activacion.addItem(activa)
                self.lista_id_promos.append(reg[0])
        # Cargamos las promos desactivadas
        cont = 0
        tope = len(lista_activado)
        while cont < tope:
            if len(self.ui.list_nombre) <= self.LIMITE_LISTA:
                self.ui.list_nombre.addItem(lista_Ceros[cont])
                self.ui.list_activacion.addItem(lista_activado[cont])
            self.lista_id_promos.append(lista_id_aux[cont])
            cont += 1

    '''#############################################################################################################################################
                                                            FUNCIONES DE WIDGETS
    #############################################################################################################################################'''

    def Line_Change_Codigo(self):
        if self.LINE == True:
            texto = self.ui.line_Codigo.text()
            largo = len(texto)
            if largo < 2: self.Control_Datos_En_Pantalla()
            if largo > 0:
                existe, Lista = mdbprom.Busca_Cod_Promo("Promos", "Codigo", texto)
                if existe > 0:
                    self.Carga_Datos_en_Ventana(Lista[0])
                else:
                    self.Limpia_Ventana(False)

    def Line_Change_Nombre(self):
        if self.LINE == True:
            # Se ejecuta tanto cuando se borra todo (len=0) o cuando tiene al menos un caracter (len=1). Porque en las demás opciones no es necesario
            if len(self.ui.line_Nombre.text()) < 2: self.Control_Datos_En_Pantalla()

    def Line_Cant_Change(self):
        if self.LINE == True:
            if self.CONTROL_GRAL < 3:
                QMessageBox.question(self, "Atención", "Debe configurar los datos en orden para continuar (Codigo, Nombre, Tipo de promo).", QMessageBox.Ok)
                self.LINE = False
                self.ui.line_cant.clear()
                self.LINE = True
                self.ui.line_Codigo.setFocus()
            else:
                self.LINE = False
                self.ui.line_cant.setText(form.Line_Solo_Num(self.ui.line_cant.text()))
                self.LINE = True
                texto = self.ui.line_cant.text()
                if texto != "":
                    valor = int(texto)
                    if self.TIPO_ACTUAL == 2:
                        if valor > 0:
                            self.CANT_PROMO2 = valor
                        else:
                            self.CANT_PROMO2 = 0
                        self.Actualiza_Lista_Productos()
                    else:
                        QMessageBox.question(self, "Error", "No se puede determinar el error, pero tenga en cuenta que la cantidad sólo se carga en las promociones del primer tipo (FIJAS).", QMessageBox.Ok)
                        self.LINE = False
                        self.ui.line_cant.clear()
                        self.LINE = True
                        self.ui.line_Codigo.setFocus()
                else:
                    if self.TIPO_ACTUAL == 2:
                        self.CANT_PROMO2 = 0
                        self.Actualiza_Lista_Productos()
                    else:
                        QMessageBox.question(self, "Error", "No se puede determinar el error, pero tenga en cuenta que la cantidad sólo se carga en las promociones del primer tipo (FIJAS).", QMessageBox.Ok)
                        self.LINE = False
                        self.ui.line_cant.clear()
                        self.LINE = True
                        self.ui.line_Codigo.setFocus()
                if len(texto) < 2: self.Control_Datos_En_Pantalla()
                if len(self.LISTA_COD_PROMO2) > 0 and self.CONTROL_GRAL > 5:
                    self.Actualiza_Lista_Productos()

    def Line_Precio_Change(self):
        if self.LINE == True:
            if self.CONTROL_GRAL < 4:
                mensaje = ""
                if self.TIPO_ACTUAL == 2:
                    mensaje = "Debe configurar los datos en orden para continuar (Codigo, Nombre, Tipo de promo, Cantidad de productos)."
                else:
                    mensaje = "Debe configurar los datos en orden para continuar (Codigo, Nombre, Tipo de promo)."
                QMessageBox.question(self, "Atención", mensaje, QMessageBox.Ok)
                self.LINE = False
                self.ui.line_precio.clear()
                self.LINE = True
                self.ui.line_Codigo.setFocus()
            else:
                self.LINE = False
                self.ui.line_precio.setText(form.Line_Num_Coma_(self.ui.line_precio.text()))
                self.LINE = True
                texto = self.ui.line_precio.text()
                if texto != "":
                    valor = form.Str_Float(texto)
                    if self.TIPO_ACTUAL == 1:
                        self.PRE_TOTAL1 = valor
                        self.Calcula_Precios_Promo1()
                    else:
                        self.PRE_TOTAL2 = valor
                        self.Calcula_Precios_Promo2()
                else:
                    if self.TIPO_ACTUAL == 1:
                        self.PRE_TOTAL1 = 0.0
                        self.Calcula_Precios_Promo1()
                    else:
                        self.PRE_TOTAL2 = 0.0
                        self.Calcula_Precios_Promo2()
                if len(texto) < 2: self.Control_Datos_En_Pantalla()
                self.Actualiza_Lista_Productos()

    def Clic_Fijos(self):
        if self.RADIO == True:
            if self.CONTROL_GRAL < 2:
                QMessageBox.question(self, "Error", "Debe cargar primero un CÓDIGO y un NOMBRE antes de continuar.", QMessageBox.Ok)
                self.RADIO = False
                self.ui.radio_Fijos.setChecked(False)
                self.ui.radio_Combinacion.setChecked(False)
                self.RADIO = True
            else:
                if len(self.LISTA_COD_PROMO2) > 0:
                    Rta = QMessageBox.question(self, "Atención", "Si cambia el tipo de Promoción se eliminarán los productos que tiene configurado actualmente.\n¿Desea cambiar el tipo de Promoción de todos modos?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if Rta == QMessageBox.No:
                        self.RADIO = False
                        self.ui.radio_Fijos.setChecked(False)
                        self.ui.radio_Combinacion.setChecked(True)
                        self.RADIO = True
                        return
                
                self.LISTA_COD_PROMO2 = []
                self.LISTA_CON_PROMO2 = []
                self.LISTA_PRE_PROMO2 = []
                self.LISTA_PRE_COSTO2 = []
                self.CANT_PROMO2 = 0
                self.PRE_TOTAL2 = 0.0
                self.Config_Tipos(1)
                self.Control_Datos_En_Pantalla()
                self.ui.line_precio.setFocus()

    def Clic_Combinacion(self):
        if self.RADIO == True:
            if self.CONTROL_GRAL < 2:
                QMessageBox.question(self, "Error", "Debe cargar primero un CÓDIGO y un NOMBRE antes de continuar.", QMessageBox.Ok)
                self.RADIO = False
                self.ui.radio_Fijos.setChecked(False)
                self.ui.radio_Combinacion.setChecked(False)
                self.RADIO = True
            else:
                if len(self.LISTA_COD_PROMO1) > 0:
                    Rta = QMessageBox.question(self, "Atención", "Si cambia el tipo de Promoción se eliminarán los productos que tiene configurado actualmente.\n¿Desea cambiar el tipo de Promoción de todos modos?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if Rta == QMessageBox.No:
                        self.RADIO = False
                        self.ui.radio_Fijos.setChecked(True)
                        self.ui.radio_Combinacion.setChecked(False)
                        self.RADIO = True
                        return
                
                self.LISTA_COD_PROMO1 = []
                self.LISTA_CAN_PROMO1 = []
                self.LISTA_CON_PROMO1 = []
                self.LISTA_PRE_PROMO1 = []
                self.LISTA_PRE_COSTO1 = []
                self.PRE_TOTAL1 = 0.0
                self.Config_Tipos(2)
                self.Control_Datos_En_Pantalla()
                self.ui.line_cant.setFocus()

    def Activar(self):
        if self.TIPO_ACTUAL > 0:
            self.Estado_Activacion(1)

    def Desactivar(self):
        if self.TIPO_ACTUAL > 0:
            self.Estado_Activacion(0)

    # Clic en la lista del nombre
    def Clic_Listas(self):
        pos = self.ui.list_nombre.currentRow()
        self.Carga_Datos_en_Ventana(self.lista_id_promos[pos])

    def Clic_Btn_Guarda_Promo(self):
        if self.CONTROL_GRAL < 7:
            QMessageBox.question(self, "INCOMPLETO", "No se puede Guardar los cambios porque falta información:\n- Activación de la Promo\n- Código\n- Nombre\n- Tipo de Promo\n- Cantidad de productos (Sólo si es promo Combinada)\n- Precio Total\n- Al menos un producto", QMessageBox.Ok)
        else:
            # Controlamos que cada dato que se necesita esté cargado, como codigo, cantidad, precio, productos, etc...
            if self.Controla_Datos():
                # Si está todo OK, entonces guardamos la promo
                self.Guarda_Promo()

    # Clic en agregar productos a la promo
    def Carga_Prod_Tipo(self):

        if self.CONTROL_GRAL < 5:
            QMessageBox.question(self, "Error", "No se pueden agregar productos hasta que no rellene los valores anteriores.", QMessageBox.Ok)
            return

        if self.TIPO_ACTUAL == 1:

            texto1, ok = QInputDialog.getText(self, "Cargar", "Ingrese el CÓDIGO del producto:")
            if ok and texto1 != "":
                
                existe, Lista = mdbprod.Dev_Info_Producto(texto1)
                if existe == 1:

                    texto2, ok = QInputDialog.getInt(self, "Cargar", "Ingrese la CANTIDAD del producto:")
                    if ok and texto2 != "":
                        texto2 = int(texto2)
                        if texto2 > 0:
                            concepto = Lista[4]
                            detalle = Lista[6]
                            marca = Lista[5]
                            self.LISTA_COD_PROMO1.append(texto1)
                            self.LISTA_CAN_PROMO1.append(texto2)
                            self.LISTA_CON_PROMO1.append(concepto + " " + detalle + " " + marca)
                            self.LISTA_PRE_COSTO1.append(Lista[18])
                            self.LISTA_PRE_PROMO1.append(0.0)
                            self.Actualiza_Lista_Productos()
                        else:
                            QMessageBox.question(self, "Error", "Debe cargar un valor superior a cero.", QMessageBox.Ok)
                elif existe == 0:
                    QMessageBox.question(self, "Error", "No existe el producto que se desea cargar.", QMessageBox.Ok)
                elif existe == 2:
                    QMessageBox.question(self, "Error", "Por el momento no se pueden usar los códigos de los bultos para las promociones.", QMessageBox.Ok)
                elif existe == 3:
                    QMessageBox.question(self, "Error", "El producto que desea utilizar no se encuentra activado, debe controlar y cargar los datos exactos del producto y luego podrá utilizarlos en las promociones.", QMessageBox.Ok)

        elif self.TIPO_ACTUAL == 2:
            bucle = True
            while bucle == True:
                texto, ok = QInputDialog.getText(self, "Cargar", "Ingrese el CÓDIGO del producto a agregar:")
                if ok and texto != "":
                    existe, Lista = mdbprod.Dev_Info_Producto(texto)
                    if existe == 1:
                        concepto = Lista[4]
                        detalle = Lista[6]
                        marca = Lista[5]
                        self.LISTA_COD_PROMO2.append(texto)
                        self.LISTA_CON_PROMO2.append(concepto + " " + detalle + " " + marca)
                        self.LISTA_PRE_COSTO2.append(Lista[18])
                        self.LISTA_PRE_PROMO2.append(0.0)
                        self.Actualiza_Lista_Productos()
                    else:
                        QMessageBox.question(self, "Error de Código", "El código ingresado no puede utilizarse ya sea porque no está registrado, es un código para los bultos o es el producto está DESACTIVADO.", QMessageBox.Ok)
                else:
                    bucle = False
        self.Control_Datos_En_Pantalla()

    '''#############################################################################################################################################
                                                            FUNCIONES GENERALES
    #############################################################################################################################################'''

    # Tomando los datos de las variables globales, se encarga de actualizar el precio de la lista que contiene los precios de cada prod. en la promo
    def Calcula_Precios_Promo1(self):
        if self.PRE_TOTAL1 > 0.0:
            lista_Auxiliar = []
            Tope = len(self.LISTA_CAN_PROMO1)
            for i in range(Tope):
                Tope2 = int(self.LISTA_CAN_PROMO1[i])
                for n in range(Tope2):
                    lista_Auxiliar.append(float(self.LISTA_PRE_COSTO1[i]))
            precios = mi_func.Dev_Texto_Precios(self.PRE_TOTAL1, lista_Auxiliar)
            Tope = len(self.LISTA_COD_PROMO1)
            pos = -1
            for i in range(Tope):
                pos += int(self.LISTA_CAN_PROMO1[i])
                self.LISTA_PRE_PROMO1[i] = precios[pos] * self.LISTA_CAN_PROMO1[i]
        else:
            Tope = len(self.LISTA_COD_PROMO1)
            for i in range(Tope):
                self.LISTA_PRE_PROMO1[i] = 0.0

    # Idem anterior, pero más fácil
    def Calcula_Precios_Promo2(self):
        valor = 0.0
        if self.PRE_TOTAL2 > 0.0 and self.CANT_PROMO2 > 0.0:
            valor = form.Redondear_float(self.PRE_TOTAL2 / self.CANT_PROMO2, 2)
        Tope = len(self.LISTA_PRE_PROMO2)
        for i in range(Tope):
            self.LISTA_PRE_PROMO2[i] = valor

    # Función que controla el progreso de la edición o creación de una promo. A medida que va controlando cada ítem va dandole valor a la variable
    # ATENCIÓN! A ESTA FUNCIÓN SE DEBE LLAMAR CADA VEZ QUE HAY MODIFICACIONES EN VENTANA Y NO CUANDO HAY QUE HACER UN CONTROL
    def Control_Datos_En_Pantalla(self):
        # Reinciamos el contador
        self.CONTROL_GRAL = 0

        # Si hay un código de promo escrito aumentamos su valor a 1
        texto = self.ui.line_Codigo.text()
        if texto == "":
            return
        self.CONTROL_GRAL += 1

        # Dependiendo su estado, actualizamos la leyenda del botón de "Guardar"
        existe, Lista = mdbprom.Busca_Cod_Promo("Promos", "Codigo", texto)
        Lista = []
        if existe == 0:
            self.ui.push_guardar.setText("NUEVA PROMO")
        elif existe > 0:
            self.ui.push_guardar.setText("Actualizar")
        
        # Controlamos el nombre de la promo - 2
        if self.ui.line_Nombre.text() != "":
            self.CONTROL_GRAL += 1
        else:
            return

        # Controlamos que haya un tipo de promo seleccionada - 3
        if self.TIPO_ACTUAL > 0:
            self.CONTROL_GRAL += 1
        else:
            self.RADIO = False
            self.ui.radio_Fijos.setChecked(False)
            self.ui.radio_Combinacion.setChecked(False)
            self.RADIO = True
            return
        
        # Controlamos que haya una cantidad asignada - 4
        if self.TIPO_ACTUAL == 2:
            if self.CANT_PROMO2 == 0:
                return
        self.CONTROL_GRAL += 1

        # Controlamos el Precio Final de la Promo - 5
        if self.TIPO_ACTUAL == 1:
            if self.PRE_TOTAL1 > 0.0:
                self.CONTROL_GRAL += 1
            else:
                return
        elif self.TIPO_ACTUAL == 2:
            if self.PRE_TOTAL2 > 0.0:
                self.CONTROL_GRAL += 1
            else:
                return
        else:
            return
        
        # Controlamos que hayan productos seleccionados - 6
        if len(self.LISTA_COD_PROMO1) > 0 or len(self.LISTA_COD_PROMO2) > 0:
            self.CONTROL_GRAL += 1
        else:
            return
        
        # Controlamos que se haya establecido que tiene seleccionado la activación - 7
        if self.ACTIVACION != 2:
            self.CONTROL_GRAL += 1

    # Actualiza los datos que mostramos en la pantalla en base a las listas que contienen los datos.
        # Esta función limpia la lista y se encarga de determinar que tipo de promo se está observando y luego si están todos los datos que necesita la rellena completamente de 
        # lo contrario carga los datos que puede.
    def Actualiza_Lista_Productos(self):

        self.ui.list_Productos.clear()
        
        if self.TIPO_ACTUAL == 1:
            self.Calcula_Precios_Promo1()
            Tope = len(self.LISTA_COD_PROMO1)
            for i in range(Tope):
                texto = "[{}] [{}] - Cant: {} - {} ".format(form.Ajusta_A_2_Dec(self.LISTA_PRE_COSTO1[i] * self.LISTA_CAN_PROMO1[i]), form.Ajusta_A_2_Dec(self.LISTA_PRE_PROMO1[i]), str(self.LISTA_CAN_PROMO1[i]), self.LISTA_CON_PROMO1[i])
                self.ui.list_Productos.addItem(texto)

        elif self.TIPO_ACTUAL == 2:
            self.Calcula_Precios_Promo2()
            Tope = len(self.LISTA_COD_PROMO2)
            for i in range(Tope):
                texto = "[{}] [{}] - Cant: {} - {} ".format(form.Ajusta_A_2_Dec(self.LISTA_PRE_COSTO2[i]), form.Ajusta_A_2_Dec(self.LISTA_PRE_PROMO2[i]), "1", self.LISTA_CON_PROMO2[i])
                self.ui.list_Productos.addItem(texto)

    # Función que configura los colores de los botones de Activar y Desactivar.
        # Estado: 0 > Desactivado / 1: Activado / 2: Sin Valor
        # Seleccion: 
            # True: Significa que se ha seleccionado una promo y vamos a marcar con Azul el estado de la misma, es decir, si está activada o no.
            # False: Cuando estamos cambiando el valor de una promo, no vamos a marcar con azul las opciones, sino con verde y rojo, para que se sepa que ese dato aún no fue
                # guardado.
    def Estado_Activacion(self, Estado = 0, Seleccion = False):
        self.ACTIVACION = Estado
        R_btn_D = 0
        G_btn_D = 0
        B_btn_D = 0
        R_btn_A = 0
        G_btn_A = 0
        B_btn_A = 0
        if Estado == 0:
            if Seleccion == False:
                R_btn_D = self.Rd
                G_btn_D = self.Gd
                B_btn_D = self.Bd
            else:
                R_btn_D = self.Rs
                G_btn_D = self.Gs
                B_btn_D = self.Bs
            R_btn_A = self.Rg
            G_btn_A = self.Gg
            B_btn_A = self.Bg
        elif Estado == 1:
            R_btn_D = self.Rg
            G_btn_D = self.Gg
            B_btn_D = self.Bg
            if Seleccion == False:
                R_btn_A = self.Ra
                G_btn_A = self.Ga
                B_btn_A = self.Ba
            else:
                R_btn_A = self.Rs
                G_btn_A = self.Gs
                B_btn_A = self.Bs
        elif Estado == 2:
            R_btn_D = self.Rg
            G_btn_D = self.Gg
            B_btn_D = self.Bg
            R_btn_A = self.Rg
            G_btn_A = self.Gg
            B_btn_A = self.Bg

        self.ui.push_activar.setStyleSheet("background-color: rgb({}, {}, {});".format(R_btn_A, G_btn_A, B_btn_A))
        self.ui.push_desactivar.setStyleSheet("background-color: rgb({}, {}, {});".format(R_btn_D, G_btn_D, B_btn_D))
        if Seleccion == False: self.Control_Datos_En_Pantalla()

    # Función que cambia el valor de Enabled de los grupos de datos para los 2 tipos de promos que tenemos. Dando la posibilidad incluso de deshabilitar a ambos.
        # Parámetro: Tipo: 
            # 0: Se anulan ambos
            # 1: Se deja habilitado el tipo "Productos Fijos"
            # 2: Se deja habilitado el tipo "Combinación de productos"
    def Config_Tipos(self, tipo):
        self.LINE = False
        self.TIPO_ACTUAL = tipo
        self.ui.line_cant.clear()
        self.ui.line_precio.clear()
        self.ui.list_Productos.clear()
        if tipo == 1:
            self.ui.line_cant.setEnabled(False)
        elif tipo == 2:
            self.ui.line_cant.setEnabled(True)
        else:
            self.ui.line_cant.setEnabled(True)
        self.LINE = True

    # Pone en pantalla la configuración de la Promo que haya que cargar
    def Carga_Datos_en_Ventana(self, id_):
        self.Limpia_Ventana()
        reg = mdbprom.Reg_Un_param_Int("Promos", "ID", id_)
        Lista_Aux = []
        for pos in reg:
            for i in range(16):
                Lista_Aux.append(pos[i])

        # 1: Producto simple. 2: Combinación de productos
        if Lista_Aux[4] == 1:
            # Configuramos pantalla
            self.Config_Tipos(1)

            # Obtenemos los datos de la promo
            self.LISTA_COD_PROMO1, self.LISTA_CAN_PROMO1, self.LISTA_PRE_PROMO1 = mi_func.Dev_Info_Promo_1(Lista_Aux[5])
            # Rellenamos las listas que contienen todos los datos
            Tope = len(self.LISTA_COD_PROMO1)
            for i in range(Tope):
                existe, lista = mdbprod.Dev_Info_Producto(self.LISTA_COD_PROMO1[i])
                self.LISTA_PRE_COSTO1.append(lista[18])
                concepto = lista[4]
                marca = lista[5]
                detalle = lista[6]
                self.LISTA_CON_PROMO1.append(concepto + " " + detalle + " " + marca)
            self.PRE_TOTAL1 = Lista_Aux[15]

            # Una vez obtenido los datos los colocamos en pantalla
            # Datos generales
            self.LINE = False
            self.ui.line_Codigo.setText(Lista_Aux[1])
            self.ui.line_Nombre.setText(Lista_Aux[2])
            self.LINE = True
            # RadioButtons
            self.RADIO = False
            self.ui.radio_Fijos.setChecked(True)
            self.ui.radio_Combinacion.setChecked(False)
            self.RADIO = True
            # Cargamos el precio de la promo
            self.LINE = False
            self.ui.line_precio.setText(form.Ajusta_A_2_Dec(self.PRE_TOTAL1))
            self.LINE = True
            # Rellenamos la lista de productos
            self.Actualiza_Lista_Productos()
            # Configuramos los botones de Activación
            self.Estado_Activacion(Lista_Aux[14], True)
        else:
            # Configuramos pantalla
            self.Config_Tipos(2)
            # Obtenemos los datos para mostrar el precio del combo, la cantidad y rellenar la lista con los productos
            self.CANT_PROMO2, Valor, self.LISTA_COD_PROMO2 = mi_func.Dev_Info_Promo_2(Lista_Aux[5])
            self.LINE = False
            self.ui.line_cant.setText(str(self.CANT_PROMO2))
            self.LINE = True
            self.PRE_TOTAL2 = Lista_Aux[15]
            for Codigos in self.LISTA_COD_PROMO2:
                existe, lista = mdbprod.Dev_Info_Producto(Codigos)
                self.LISTA_PRE_COSTO2.append(lista[18])
                concepto = lista[4]
                marca = lista[5]
                detalle = lista[6]
                self.LISTA_CON_PROMO2.append(concepto + " " + detalle + " " + marca)
                self.LISTA_PRE_PROMO2.append(Valor)

            # Una vez obtenido los datos los colocamos en pantalla
            # Datos generales
            self.LINE = False
            self.ui.line_Codigo.setText(Lista_Aux[1])
            self.ui.line_Nombre.setText(Lista_Aux[2])
            self.LINE = True
            # RadioButtons
            self.RADIO = False
            self.ui.radio_Fijos.setChecked(False)
            self.ui.radio_Combinacion.setChecked(True)
            self.RADIO = True
            # Cargamos el precio de la promo
            self.LINE = False
            self.ui.line_precio.setText(form.Ajusta_A_2_Dec(self.PRE_TOTAL2))
            self.LINE = True
            # Rellenamos la lista de productos
            self.Actualiza_Lista_Productos()
            # Configuramos los botones de Activación
            self.Estado_Activacion(Lista_Aux[14], True)
        self.Control_Datos_En_Pantalla()

    # Controla que las opciones que deben tener algún valor, las tengan
    # Nota: No controlamos el Line del Código xq se hace en la función que llama a ésta función
    def Controla_Datos(self):
        # Controlamos que haya un código para la promo
        Texto = self.ui.line_Codigo.text()
        if Texto == "":
            QMessageBox.question(self, "Atención!", "Debe colocar un CODIGO para la Promo.", QMessageBox.Ok)
            return False
        # Controlamos que hayan colocado el nombre de la promo
        if self.ui.line_Nombre.text() == "":
            QMessageBox.question(self, "Atención", "Debe ingresar un nombre para la Promo", QMessageBox.Ok)
            return False
        # Controlamos que hayan colocado el monto total de la promo
        if self.ui.line_precio.text() == "":
            QMessageBox.question(self, "Atención", "Debe ingresar el monto total de la promo", QMessageBox.Ok)
            return False
        # Controlamos que hayan colocado el tipo de promo (1 o 2)
        if self.TIPO_ACTUAL == 0:
            QMessageBox.question(self, "Atención", "Debe seleccionar el tipo de promo que está guardando, con PRODUCTOS FIJOS o promo con COMBINACIÓN DE PRODUCTOS.", QMessageBox.Ok)
            return False
        # Controlamos según el tipo de Promo, que tenga cargado al menos algún producto
        if self.TIPO_ACTUAL == 1:
            if len(self.LISTA_COD_PROMO1) == 0:
                QMessageBox.question(self, "Atención", "No hay productos cargados.", QMessageBox.Ok)
                return False
        if self.TIPO_ACTUAL == 2:
            if self.ui.line_cant.text() == "":
                QMessageBox.question(self, "Atención", "Debe colocar la cantidad de productos que contiene la Promo", QMessageBox.Ok)
                return False
            if len(self.LISTA_COD_PROMO2) == 0:
                QMessageBox.question(self, "Atención", "No hay productos cargados.", QMessageBox.Ok)
                return False
        # Controlamos que se haya seleccionado si se quiere activada o Desactivada
        if self.ACTIVACION == 2:
            QMessageBox.question(self, "Atención!", "Falta especificar si se crea la Promo ACTIVADA o DESACTIVADA.", QMessageBox.Ok)
            return False
        return True

    # Guarda una nueva Promo tomando los datos en pantalla
    def Guarda_Promo(self):

        Codigo = self.ui.line_Codigo.text()

        # Controlamos si el código ya existe
        estado, lista = mdbprom.Busca_Cod_Promo("Promos", "Codigo", Codigo)
        lista = []

        Nombre = self.ui.line_Nombre.text()
        # Si bien eliminé la descripción de la ventana, no se ha eliminado el campo de la db y tampoco voy a eliminarlo porque hasta puedo reutilizarlo.
        Descripcion = ""
        Activacion = self.ACTIVACION
        Tipo = self.TIPO_ACTUAL
        Productos = ""
        Inicio = 0
        Fin = 0
        Caduca_Fecha = 0
        Caduca_Stock = 0
        Cant_vnd_ult = 0
        Cant_vnd_tot = 0
        Gcia_ult = 0.0
        Gcia_tot = 0.0
        Monto = 0.0

        # Promo con productos Fijos y diversas cantidades
        if Tipo == 1:
            Monto = self.PRE_TOTAL1
            # En este momento se debe convertir los detalles de los productos a un sólo texto
            Tope = len(self.LISTA_COD_PROMO1)
            for i in range(Tope):
                Productos += str(self.LISTA_COD_PROMO1[i]) + "/" + str(self.LISTA_CAN_PROMO1[i]) + "*" + str(form.Redondear_float(self.LISTA_PRE_PROMO1[i]/self.LISTA_CAN_PROMO1[i], 2)) + "$"
        elif Tipo == 2:
            Monto = self.PRE_TOTAL2
            Productos = str(self.CANT_PROMO2) + "*" + str(self.LISTA_PRE_PROMO2[0]) + "$"
            for i in range(len(self.LISTA_COD_PROMO2)):
                Productos += str(self.LISTA_COD_PROMO2[i]) + "/"

        # Promo nueva
        if estado == 0:
            mdbprom.Guarda_Promo_Nueva(Codigo, Nombre, Descripcion, Tipo, Productos, Inicio, Fin, Caduca_Fecha, Caduca_Stock, Cant_vnd_ult, Cant_vnd_tot, Gcia_ult, Gcia_tot, Activacion, Monto)
        # Editando
        else:
            mdbprom.Act_Reg_Promo(Nombre, Descripcion, Tipo, Productos, Inicio, Fin, Caduca_Fecha, Caduca_Stock, Cant_vnd_ult, Cant_vnd_tot, Gcia_ult, Gcia_tot, Activacion, Monto, Codigo)

        # Debido a la complicación que tenemos con el sistema de Promos incorporado a cada producto, lo que hacemos es siempre quitarle a todos los productos de la promo actual,
            # el valor que tienen en su columna "Promo". Luego se lo volvemos a cargar.
            # Esto es así xq cuando un usuario elimina un producto yo no puedo actualizar dicho producto quitándole su promo porque luego puede que el usuario se arrepienta y no 
            # guarde los cambios, entonces si ya lo hice le he quitado la promo, y como el usuario no guarda los cambios no se recupera.
            # Entonces, si siempre limpiamos la promo de todos los productos y las volvemos a cargar, entonces nos aseguramos una correcta actualización.
        mi_func.Quita_Producto_Promo(Codigo)

        # Sin importar la actividad que se esté haciendo, es necesario actualizar el estado de los productos, sus promos siempre.
        if self.TIPO_ACTUAL == 1:
            if Activacion == 1:
                Codigo += "-"
                for i in self.LISTA_COD_PROMO1:
                    mdbprod.Act_Promo_S_Cod(i, Codigo)

        elif self.TIPO_ACTUAL == 2:
            if Activacion == 1:
                Codigo += "+"
                for i in self.LISTA_COD_PROMO2:
                    mdbprod.Act_Promo_S_Cod(i, Codigo)

        self.Limpia_Ventana()
        self.Actualiza_lista_Promo()








