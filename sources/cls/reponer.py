from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog
from vtn.vtn.vtn_reponer import Ui_Reponer

from vtn.cla.productos import V_Productos

import source.mod.mdbprod as mdb_p
import source.mod.vars as mi_vars
import source.mod.form as form
import source.mod.Clase_Listas as tabla
import copy
'''
HACER PARA PROXIMA VERSIÓN:
    - Cuando se carga un producto que ya estaba cargado (en la lista de la derecha) y tiene alguna diferencia de cantidad, se le suma la cantidad al producto anterior. Pero si hay otras diferencias como ser el precio de costo, se crea un ítem nuevo. Pero al mismo tiempo, si volvemos a cargar nuevamente el mismo código (por tercera vez), sólo es comparado con el primero, y quizás coincida con el 2do codigo cargado, debería tmb sumar la cantidad en ese caso, xq lo que hace actualmente es crear directamente un nuevo ítem.

CONTROLAR:
    - A ver si se puede crear un producto nuevo cuando no está previamente cargado.
    - Controlar que se mantenga actualizada la lista de codigos con cada eliminación

'''




class V_Reponer(QMainWindow):
    def __init__(self):
        super(V_Reponer, self).__init__()
        self.ui = Ui_Reponer()
        self.ui.setupUi(self)

        # Creamos y configuramos la tabla de info
        self.Tabla = tabla.Tabla_Propia(self.ui.groupBox)
        self.Tabla.setGeometry(10, 45, 940, 490)
        Lista = [8, 50, 14, 14, 14]
        self.Tabla.Setea(940, 490, Lista, 18, True)

        # VARIABLES
        # Cuando se cargan los productos, puede ser que se utilice la función de Listas del lector de barras, para ello debemos activar primero ésta variable
        self.FUNCION_LISTA = False
        # Es la lista del producto que se está tratando
        self.LISTA_AUXILIAR = []
        # Lista que con tiene dentro una lista por cada producto que están siendo cargados
        self.LISTA_PRODUCTOS = []
            # Datos de la lista:
            # 0:  text  - Codigo del producto
            # 1:  float - Cant a comprar
            # 2:  float - Pcio Costo Anterior
            # 3:  float - Pcio Vta Anterior
            # 4:  text  - Concepto completo (concepto, marca, detalle)
            # 5:  float - Pcio Costo
            # 6:  float - Pcio Vta
            # 7:  bool  - V/F si tiene un incremento establecido o no
            # 8:  float - Porcentaje de incremento
            # 9:  float - Descuento en porcentaje
            # 10: float - Descuento en pesos
            # 11: float - Precio de venta sugerido
            # 12: float - Precio de Costo con el Descuento Aplicado
            # 13: float - Total de costo del producto * cantidad
            # 14: str   - Identificador

            # Nota: El valor del incremento será el que contenga el producto, bien el generalizado. La pos[7] es quién nos indica de donde sale dicho valor

        # Idem lista anterior, pero con los datos que necesita en formato str para poder ser cargada en la tabla
        #self.LISTA_PRODUCTOS_STR = []

        # Se crea una lista con los códigos de cada prod, por el simple hecho de que es más simple su tratamiento xq ya sabemos q su dato está cargado en la list anterior.
        self.LISTA_CODIGOS = []
        # Guardamos el porcentaje que se incrementa a los productos que no tienen su propio porcentaje
        self.PORCENTAJE = 0.0
        # Hay interacción entre el los line que determinan el descuento, así que entre sí pueden bloquearse la función de Change con ésta variable.
        self.LINE_BLOQUEO = False
        # Contador que hace de ID. Se necesita un identificador único, y que no vaya cambiando a medida que se agregan y eliminan ítems, así que usaré un contador que será
            # convertido a str a medida que se va utilizando y se reinicia a 0 cada vez que se limpia la ventana
        self.CONT_ID = 0

        self.ui.push_Sumar.clicked.connect(self.Clic_Btn_Sumar)
        self.ui.push_Restar.clicked.connect(self.Clic_Btn_Restar)
        self.ui.push_ModoLista.clicked.connect(self.Btn_Modo_Lista)
        self.ui.push_Incremento.clicked.connect(self.Clic_Incremento)
        self.ui.push_Cargar.clicked.connect(self.Carga_Prod_Lista)
        self.ui.push_Eliminar.clicked.connect(self.Elimina_Item)
        self.ui.push_Eliminar_2.clicked.connect(self.Limpia_Pantalla)

        self.ui.line_Codigo.returnPressed.connect(self.Return_line_Cod)

        self.ui.line_Cantidad.textChanged.connect(self.Change_line_Cantidad)
        self.ui.line_Pcio_Unit_Act.textChanged.connect(self.Change_line_Pcio_Unit_Actual)
        self.ui.line_Desc_Porc.textChanged.connect(self.Change_line_Desc_Porc)
        self.ui.line_Desc_Valor.textChanged.connect(self.Change_line_Desc_Valor)

        self.Limpia_Datos_Actuales()

    '''#############################################################################################################################################
    FUNCIONES DE VENTANA  '''

    # Función que se ejecuta cada vez que se tiene que cargar la ventana
    def Mostrar(self):
        # Cada vez que se abre, se actualiza el monto del porcentaje a incrementar
        self.PORCENTAJE = 1 + (mdb_p.Dev_Config("Porcentaje") / 100)
        self.show()

    # Muestra en pantalla los datos que correspondan al producto actual. IMPORTANTE!: la LISTA_AUXILIAR debe estar actualizada
    def Muestra_Datos(self):
        # Rellenamos los widgets con los datos que ya tenemos actualizados en la LISTA_AUXILIAR
        if len(self.LISTA_AUXILIAR) > 0:
            self.LINE_BLOQUEO = True
            # Separados por GroupBox
            self.ui.label_Concepto.setText(self.LISTA_AUXILIAR[4])
            #
            self.ui.line_Cantidad.setText(form.Formato_Unidades(self.LISTA_AUXILIAR[1], 3))
            #
            self.ui.label_Pcio_Cpa_Ant.setText(form.Formato_Decimal(self.LISTA_AUXILIAR[2], 2))
            self.ui.label_Pcio_Vta_Ant.setText(form.Formato_Decimal(self.LISTA_AUXILIAR[3], 2))
            #
            self.ui.line_Pcio_Unit_Act.setText(form.Formato_Decimal_S_Punto_Mil(self.LISTA_AUXILIAR[5], 2))
            self.ui.line_Desc_Porc.setText(form.Formato_Decimal_S_Punto_Mil(self.LISTA_AUXILIAR[9], 2))
            self.ui.line_Desc_Valor.setText(form.Formato_Decimal_S_Punto_Mil(self.LISTA_AUXILIAR[10], 2))
            self.ui.label_Unit_Final.setText(form.Formato_Decimal(self.LISTA_AUXILIAR[12], 2))
            #
            self.ui.label_Pcio_Vta_Sug.setText(form.Formato_Decimal(self.LISTA_AUXILIAR[11], 2))
            if self.LISTA_AUXILIAR[7] == True:
                self.ui.label_20.setText("% Inc. del Producto:")
            else:
                self.ui.label_20.setText("% Inc. GENÉRICO:")
            self.ui.push_Incremento.setText(form.Formato_Decimal(self.LISTA_AUXILIAR[8], 2))
            self.ui.line_Pcio_Vta.setText(form.Formato_Decimal_S_Punto_Mil(self.LISTA_AUXILIAR[6], 2))
            #
            self.ui.label_Subtotal.setText(form.Formato_Decimal(self.LISTA_AUXILIAR[13], 2))
            #
            #self.Calcula_Subtotales()
            self.ui.line_Cantidad.setFocus()
            self.ui.line_Cantidad.selectAll()
            self.LINE_BLOQUEO = False

    # Actualiza lista de productos
    def Actualiza_Listas(self):

        self.Actualiza_Tabla_Str()
        self.Tabla.Refresca_Lista()
        '''
        self.ui.listWidget_1.clear()
        self.ui.listWidget_2.clear()
        self.ui.listWidget_3.clear()
        self.ui.listWidget_4.clear()
        self.ui.listWidget_5.clear()

        for i in range(len(self.LISTA_PRODUCTOS)):
            self.ui.listWidget_1.addItem(str(i + 1))
            self.ui.listWidget_2.addItem(self.LISTA_PRODUCTOS[i][4])
            self.ui.listWidget_3.addItem(form.Formato_Decimal(self.LISTA_PRODUCTOS[i][12], 2))
            self.ui.listWidget_4.addItem(form.Formato_Decimal(self.LISTA_PRODUCTOS[i][1], 2))
            self.ui.listWidget_5.addItem(form.Formato_Decimal(self.LISTA_PRODUCTOS[i][13], 2))
        '''
    
    # En varias ocaciones sólo agregamos al listwidgets el producto que se encuentra en la lista_auxiliar, donde no es necesario limpiar todo y volver a cargar
    def Agrega_Auxiliar(self):
        Lista = []
        Lista.append(str(self.CONT_ID))
        Lista.append(str(len(self.LISTA_PRODUCTOS)))
        Lista.append(self.LISTA_AUXILIAR[4])
        Lista.append(form.Formato_Decimal(self.LISTA_AUXILIAR[12], 2))
        Lista.append(form.Formato_Decimal(self.LISTA_AUXILIAR[1], 3))
        Lista.append(form.Formato_Decimal(self.LISTA_AUXILIAR[13], 2))
        self.CONT_ID += 1
        self.Tabla.Agrega_Item_Final(Lista)

    def Actualiza_Tabla_Str(self):
        self.Tabla.LISTA_GENERAL = []
        for i in range(len(self.LISTA_PRODUCTOS)):
            list_Aux = []
            list_Aux.append(self.LISTA_PRODUCTOS[i][14])
            list_Aux.append(str(i + 1))
            list_Aux.append(self.LISTA_PRODUCTOS[i][4])
            list_Aux.append(form.Formato_Decimal(self.LISTA_PRODUCTOS[i][12], 2))
            list_Aux.append(form.Formato_Decimal(self.LISTA_PRODUCTOS[i][1], 2))
            list_Aux.append(form.Formato_Decimal(self.LISTA_PRODUCTOS[i][13], 2))
            self.Tabla.LISTA_GENERAL.append(list_Aux)
    
    # Limpia la parte de la izquierda de la ventana
    def Limpia_Datos_Actuales(self):
        self.ui.line_Codigo.clear()
        self.ui.label_Concepto.setText("")
        self.ui.line_Cantidad.clear()
        self.ui.label_Pcio_Cpa_Ant.setText("0,00")
        self.ui.label_Pcio_Vta_Ant.setText("0,00")
        self.ui.line_Pcio_Unit_Act.clear()
        self.ui.line_Desc_Porc.clear()
        self.ui.line_Desc_Valor.clear()
        self.ui.label_Unit_Final.setText("0,00")
        self.ui.label_Pcio_Vta_Sug.setText("0,00")
        self.ui.push_Incremento.setText(form.Formato_Decimal((self.PORCENTAJE - 1)*100,2))
        self.ui.line_Pcio_Vta.clear()
        self.ui.label_Subtotal.setText("0,00")
        self.ui.line_Codigo.setFocus()

    '''#############################################################################################################################################
    FUNCIONES DE BOTONES  '''

    # Clic Btn Sumar una unidad
    def Clic_Btn_Sumar(self):
        self.LISTA_AUXILIAR[1] += 1.0
        self.LINE_BLOQUEO = True
        self.ui.line_Cantidad.setText(form.Formato_Decimal_S_Punto_Mil(self.LISTA_AUXILIAR[1], 2))
        self.Calcula_Subtotales()
        self.LINE_BLOQUEO = False
    
    # Clic Btn Restar una unidad
    def Clic_Btn_Restar(self):
        if self.LISTA_AUXILIAR[1] >= 1.0:
            self.LISTA_AUXILIAR[1] -= 1.0
        else:
            self.LISTA_AUXILIAR[1] = 0.0
        self.LINE_BLOQUEO = True
        self.ui.line_Cantidad.setText(form.Formato_Decimal_S_Punto_Mil(self.LISTA_AUXILIAR[1], 2))
        self.Calcula_Subtotales()
        self.LINE_BLOQUEO = False

    # Al precionarse puede modificarse o asignarse un valor de incremento al producto en pantalla, pero NO permite actualizar el porcentaje genérico del programa
    def Clic_Incremento(self):

        # Nos fijamos si hay un producto en pantalla
        if len(self.LISTA_AUXILIAR) > 0:

            # True: Cuando el producto tiene un porcentaje de incremento establecido. False: Cuando el producto no tiene incremento.
            if self.LISTA_AUXILIAR[7] == True:

                # Consultamos si quiere modificar el % de incremento del producto
                Rta = QMessageBox.question(self, "Modificar Incremento", "El incremento aplicado es del PRODUCTO. \n\n¿Desea modificar el Porcentaje de Incremento de éste PRODUCTO?\nNota: El porcentaje del PRODUCTO se actualizará cuando confirme el PAGO de la factura, al final del proceso de carga.", QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
                if Rta == QMessageBox.Yes:
                    Valor, ok = QInputDialog.getDouble(self, "Modificar Incremento", r"Ingrese Porcentaje:", (1 - self.PORCENTAJE) * 100, 0.0,10000.0,2)
                    print(str(Valor))
                    if ok and form.Es_Numero(Valor):
                        self.LISTA_AUXILIAR[8] = Valor
                        self.LINE_BLOQUEO = True
                        self.ui.push_Incremento.setText(form.Formato_Decimal(Valor, 2))
                        self.LINE_BLOQUEO = False
                        self.Calcula_Subtotales()
            
            else:
                # Consultamos si quiere modificar el % de incremento Genérico
                Rta = QMessageBox.question(self, "Modificar Incremento", "El incremento aplicado actualmente es GENÉRICO. \n\n¿Desea cargar un nuevo Porcentaje de Incremento para éste PRODUCTO?\nNota: El porcentaje del PRODUCTO se actualizará cuando confirme el PAGO de la factura, al final del proceso de carga.", QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
                if Rta == QMessageBox.Yes:
                    Valor, ok = QInputDialog.getDouble(self, "Modificar Incremento", r"Ingrese un PORCENTAJE.\nEjemplo: 30. Indicaría que se incrementa un 30% al costo de cada producto para calcular el valor sugerido de venta.", (self.PORCENTAJE - 1) * 100, 0.0,10000.0,2)
                    print(str(Valor))
                    if ok and form.Es_Numero(Valor):
                        self.LISTA_AUXILIAR[7] = True
                        self.LISTA_AUXILIAR[8] = Valor
                        self.LINE_BLOQUEO = True
                        self.ui.push_Incremento.setText(form.Formato_Decimal(Valor, 2))
                        self.LINE_BLOQUEO = False
                        self.Calcula_Subtotales()

    # No sólo es llamada por el botón. Intercambia el estado entre normal y Modo Lista
    def Btn_Modo_Lista(self):
        QMessageBox.question(self, "Atención!", "Proceso sin terminar", QMessageBox.Ok)
        '''
        if self.FUNCION_LISTA == False:
            self.FUNCION_LISTA = True
            self.ui.push_ModoLista.setText("Desactivar\nModo Lista")
            self.push_ModoLista.setStyleSheet("background-color: rgb(50, 255, 50);")
        else:
            self.FUNCION_LISTA = False
            self.ui.push_ModoLista.setText("Desactivar\nModo Lista")
            self.push_ModoLista.setStyleSheet("background-color: rgb(208, 211, 212);")
        '''

    # Elimina todo lo que se ve en la lista de la derecha
    def Limpia_Pantalla(self):
        Rta, ok = QMessageBox.question(self, "ATENCIÓN!", "¿Desea limpiar toda la lista?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if Rta == QMessageBox.Yes:
            self.LISTA_PRODUCTOS = []
            self.LISTA_CODIGOS = []
            self.Tabla.Elimina_Lista(True)

    # Elimina un ítem de la lista que ya creamos
    def Elimina_Item(self):
        id = self.Tabla.Elimina_Item()
        # id es False sólo si no se ha eliminado nada, de lo contrario vale el id (string) que se ha eliminado
        if id != False:
            cont = 0
            largo = len(self.LISTA_PRODUCTOS)
            while cont < largo:
                if self.LISTA_PRODUCTOS[cont][14] == id:
                    self.LISTA_PRODUCTOS.pop(cont)
                    cont = 0
                    largo = len(self.LISTA_PRODUCTOS)
                else:
                    cont += 1
            self.Suma_Compra_Completa()

    '''#############################################################################################################################################
    FUNCIONES DE LINE_EDIT  '''
    
    '''
    # Evento Change del line. Por el momento permite números y unos signos (+-*/), y cuando hay 2 caracteres analiza si es un comando especial.
    def Change_line_Cod(self):
        if self.LINE_BLOQUEO == False and self.FUNCION_LISTA == False:
            texto1 = self.ui.line_Codigo.text()
            texto2 = form.Line_Numero_Signos(texto1)
            if texto1 != texto2:
                self.LINE_BLOQUEO = True
                self.ui.line_Codigo.setText(texto2)
                self.LINE_BLOQUEO = False
            if len(texto2) == 2:
                self.LINE_BLOQUEO = True
                self.Comandos_especiales(texto2, False)
                self.LINE_BLOQUEO = False
    '''

    # Evento Change del line Cantidad
    def Change_line_Cantidad(self):
        if self.LINE_BLOQUEO == False:
            texto = form.Line_Num_Coma_(self.ui.line_Cantidad.text())
            self.ui.line_Cantidad.setText(texto)
            if texto != "":
                self.LISTA_AUXILIAR[1] = form.Str_Float(texto)
            else:
                self.LISTA_AUXILIAR[1] = 0.0
            self.Calcula_Subtotales()

    # Evento Change del line de Precio Unitario Actual (Previo a la compra)
    def Change_line_Pcio_Unit_Actual(self):
        if self.LINE_BLOQUEO == False:
            texto = form.Line_Num_Coma_(self.ui.line_Pcio_Unit_Act.text())
            self.ui.line_Pcio_Unit_Act.setText(texto)
            if texto != "":
                self.LISTA_AUXILIAR[5] = form.Str_Float(texto)
            else:
                self.LISTA_AUXILIAR[5] = 0.0
            self.Calcula_Subtotales()

    # Evento Change del line de Descuentos por porcentajes.
    # IMPORTANTE: El valor de Descuento se saca siempre del line_Desc_Valor. Cuando éste line se modifica, actualiza el valor del otro line. Pero cuando se modifica manualmente
        # el line de Desc_Valor, entonces éste queda vacío.
    def Change_line_Desc_Porc(self):
        if self.LINE_BLOQUEO == False:
            self.LINE_BLOQUEO = True
            texto = form.Line_Num_Coma_(self.ui.line_Desc_Porc.text())
            self.ui.line_Desc_Porc.setText(texto)
            if texto != "":
                self.LISTA_AUXILIAR[9] = form.Str_Float(texto)
                aux = self.LISTA_AUXILIAR[9] / 100
                self.LISTA_AUXILIAR[10] = self.LISTA_AUXILIAR[5] * (aux)
            else:
                self.LISTA_AUXILIAR[10] = 0.0
                self.LISTA_AUXILIAR[9] = 0.0
            self.ui.line_Desc_Valor.setText(form.Formato_Decimal(self.LISTA_AUXILIAR[10], 2))
            self.Calcula_Subtotales()
            self.LINE_BLOQUEO = False
    
    # Evento Change del line Descuentos por Valor.
    # Importante: El valor de Descuento se saca siempre del line_Desc_Valor. Cuando éste line se modifica, se actualiza la variable que indica el monto a descontar.
    # Pero cuando se modifica el porcentaje, entonces éste se actualiza en función a ese porcentaje.
    def Change_line_Desc_Valor(self):
        if self.LINE_BLOQUEO == False:
            self.LINE_BLOQUEO = True
            self.ui.line_Desc_Porc.clear()
            self.LISTA_AUXILIAR[9] = 0.0
            texto = form.Line_Num_Coma_(self.ui.line_Desc_Valor.text())
            self.ui.line_Desc_Valor.setText(texto)
            if texto != "":
                self.LISTA_AUXILIAR[10] = form.Str_Float(texto)
            else:
                self.LISTA_AUXILIAR[10] = 0.0
            self.Calcula_Subtotales()
            self.LINE_BLOQUEO = False

    # Busca los datos del código en cuestión y los carga en la LISTA_AUXILIAR
    def Return_line_Cod(self):

        # Capturamos el texto escrito en el line
        texto = self.ui.line_Codigo.text()

        # Cuando estamos en el Modo Lista, evitamos cualquier tarea extra al procesador para que no se pierda ningún dato, así que lo que hacemos es crear una lista con todos
            # los códigos y una vez terminada la carga, los analizamos.
        if self.FUNCION_LISTA == True:

            # Todavía no está definido xq no vamos a programar ésto, pero hay que incorporar en ésta parte, cuando damos aviso que se terminó la lista, o que se borra lo últ.
            if texto == "999":
                self.Carga_Modo_Lista()
            else:
                self.LISTA_AUXILIAR.append(texto)
        else:   

            # La función nos devuelve en la primer variable (0= no existe; 1= Existe y es código normal; 2= Es codXbulto), y la lista son todos sus datos.
            encontrado, Lista = mdb_p.Dev_Info_Producto(texto)

            # Cuando el producto no existe
            if encontrado == 0:
                Rta = QMessageBox.question(self, "NO EXISTE", "El producto NO EXISTE, para continuar cargando la compra, deberá crear el producto con sus datos.\n¿Desea cargar el producto ahora?", QMessageBox.Ok | QMessageBox.Cancel)
                if Rta == QMessageBox.Ok:
                    self.Ventana_Productos2 = V_Productos(texto)
                    self.Ventana_Productos2.ui.push_Menu.setVisible(False)
                    self.Ventana_Productos2.ui.push_Eliminar.setVisible(False)
                    self.Ventana_Productos2.ui.push_Reco_Inicial.setVisible(False)
                    self.Ventana_Productos2.show()

            # RECORDAR DE INCORPORAR LA CANTIDAD_PROX Y CONTROLAR SI EL PRODUCTO NO PERTENECE A UNA PROMO

            # El producto existe y tiene valores normales
            elif encontrado == 1:
                self.Carga_Prod_Datos(Lista)
                
            # El producto exise pero el código es un cod x bulto
            elif encontrado == 2:
                self.Carga_Prod_Datos(Lista, True)

    '''#############################################################################################################################################
    FUNCIONES RELATIVAS AL CONJUNTO DE LISTAS DE LA DERECHA  '''

    # Carga el PRODUCTO que se está trabajando self.LISTA_AUXILIAR en las lista de la derecha. A ésta función se la llama desde el botón CARGAR o cuando se usó el MODO LISTA.
        # Cuando se carga un producto que ya está cargado pero todos los datos coinciden salvo la cantidad a comprar, entonces actualizamos ese valor, que es la cantidad.
        # Pero en cambio si tiene otro precio de compra porque puede tener por ej un descuento, entonces se crea un nuevo concepto. Al mismo tiempo se carga en la base de datos
        # en una nueva posición entonces por ejemplo el dueño del negocio puede crear una promo hasta agotar el stock que consiguió a un precio más barato y luego se desactiva.
    def Carga_Prod_Lista(self):

        # Generamos una copia para poder ir ingresando los datos en la LISTA_PRODUCTOS
        Lista_prod = self.LISTA_AUXILIAR.copy()

        # Controlamos los datos mínimos
        if len(Lista_prod) > 0:
            if Lista_prod[1] > 0.0 and Lista_prod[6] > 0.0:

                # Ahora hay que saber si se está cargando un producto nuevo o si se está actualizando los datos de uno preexistente
                if Lista_prod[0] in self.LISTA_CODIGOS:
                    
                    # Si hay que actualizar, ahora hay que saber qué vamos a actualizar
                    pos = self.LISTA_CODIGOS.index(Lista_prod[0])
                    Lista = self.Compara_Nueva_Carga(pos, Lista_prod)
                    if Lista[0] == True:
                        QMessageBox.question(self,"Error", "Error interno, de aviso del mismo código: 55446", QMessageBox.Ok)
                        return
                    
                    if Lista[2] == True:
                        QMessageBox.question(self, "Atención", "El PRECIO DE VENTA que está cargando difiere del precio de venta cargado anteriormente. Como sólo se puede cargar un PRECIO DE VENTA por producto, quedará el último que configure.", QMessageBox.Ok)
                    
                    # Si hay un precio de costo distinto creamos un nuevo grupo de stock
                    if Lista[6] == True:
                        QMessageBox.question(self, "Atención", "El precio de costo del producto difiere de lo cargado anteriormente, se creará un nuevo ítem y se pueden cargar en la Boleta ambos por separado quedando como grupos distintos de stock.", QMessageBox.Ok)
                        # Rellenamos la LISTA_PRODUCTOS y luego los listwidgets
                        self.LISTA_CODIGOS.append(Lista_prod[0])
                        self.LISTA_PRODUCTOS.append(Lista_prod)
                        self.Agrega_Auxiliar()
                    else:
                        # Si no hubieron cambios en ese valor, sumamos la cantidad
                        self.LISTA_PRODUCTOS[pos][1] = self.LISTA_PRODUCTOS[pos][1] + Lista_prod[1]
                        self.LISTA_PRODUCTOS[pos][13] = self.LISTA_PRODUCTOS[pos][13] + Lista_prod[13]
                        self.Actualiza_Listas()
                    self.Limpia_Datos_Actuales()
                else:
                    # Rellenamos la LISTA_PRODUCTOS y luego los listwidgets
                    self.LISTA_CODIGOS.append(Lista_prod[0])
                    self.LISTA_PRODUCTOS.append(Lista_prod)
                    self.Agrega_Auxiliar()
                    self.Limpia_Datos_Actuales()
                self.Suma_Compra_Completa()
            else:
                QMessageBox.question(self, "Atención", "Para cargar un producto debe contener una CANTIDAD a comprar y el PRECIO DE VENTA.", QMessageBox.Ok)
                self.ui.line_Codigo.setFocus()
        else:
            QMessageBox.question(self, "Aviso", "No hay producto para cargar", QMessageBox.Ok)
            self.ui.line_Codigo.setFocus()

    # Anexo de la función de arriba. Se llama a ésta función cuando se está por cargar una lista de datos de un producto que ya se encuentre cargado con anterioridad.
        # Informa mediante una lista a la función que la llama, los cambios importantes que pueda tener el nuevo producto respecto a lo cargado anteriormente.
        # Lista:
        # 0: Si el código es igual al que estamos analizando, para evitar errores internos ppalmente.
        # 1: Pcio de costo.
        # 2: Pcio de Vta.
        # 3: Incremento.
        # 4: Descuento en %.
        # 5: Desc. en pesos.
        # 6: Precio de costo con el descuento aplicado.
        
        # Nota: En caso de no coincidir los códigos, no es necesario mandar los demás datos xq no se va a realizar ninguna carga.
    def Compara_Nueva_Carga(self, pos, Lista_N):
        Lista = []
        # A pesar de que tiene que venir la posición correcta vamos a controlar igual el código
        if self.LISTA_PRODUCTOS[pos][0] == Lista_N[0]:

            # Si no hay diferencia en el código
            Lista.append(False)

            # Pcio de Costo
            if Lista_N[5] != self.LISTA_PRODUCTOS[pos][5]:
                Lista.append(True)
            else:
                Lista.append(False)
            
            # Pcio Vta
            if Lista_N[6] != self.LISTA_PRODUCTOS[pos][6]:
                Lista.append(True)
            else:
                Lista.append(False)

            # Incremento
            if Lista_N[8] != self.LISTA_PRODUCTOS[pos][8]:
                Lista.append(True)
            else:
                Lista.append(False)

            # Dto en porcentaje
            if Lista_N[9] != self.LISTA_PRODUCTOS[pos][9]:
                Lista.append(True)
            else:
                Lista.append(False)

            # Dto en pesos
            if Lista_N[10] != self.LISTA_PRODUCTOS[pos][10]:
                Lista.append(True)
            else:
                Lista.append(False)
            
            # Precio de Costo con el descuento aplicado
            if Lista_N[12] != self.LISTA_PRODUCTOS[pos][12]:
                Lista.append(True)
            else:
                Lista.append(False)

        else:
            # Cuando el código es distinto al que se quiere trabajar
            Lista.append(True)
        
        return Lista

    '''#############################################################################################################################################
    FUNCIONES DEL MODO LISTA  '''

    # Analiza la lista de códigos generada en el MODO LISTA y luego los carga
    def Carga_Modo_Lista(self):
        for i in self.LISTA_AUXILIAR:
            try:
                auxS = i[0:-1]
                auxI = int(auxS)
                if auxI > 998:
                    self.Carga_Prod(i)
                elif auxI == 999:
                    self.Cantidad_Prox = 0.0
                else:
                    auxI -= 100
                    self.Cantidad_Prox += float(auxI)
            except:
                pass

    '''#############################################################################################################################################
    FUNCIONES VARIAS  '''

    # Analiza si el texto que llegó corresponde a algún comando adicional.
        # Nota: tener en cuenta que el texto nunca llega vacío por eso no se controla
    def Comandos_especiales(self, texto, Btn_Enter = True):
        
        if Btn_Enter == True:

            # Primero controlamos si es que es un comando, de lo contrario devolvemos el control del flujo
            aux = texto[0]
            
            # Cambia de precio unitario en el momento y en la base de datos
            if aux == "/":

                self.LINE_BLOQUEO = True
                self.ui.line_Codigo.setText("")
                self.ui.line_Codigo.setFocus()
                self.LINE_BLOQUEO = False
                return True
            
            # Agenda la cantidad a ingresar para el nuevo producto que se agregue
            elif aux == "*":
                if len(texto) > 1:
                    if form.Es_Numero_Int(texto[1:]):
                        self.Cantidad_Prox = int(texto[1:])
                    else:
                        QMessageBox.question(self, "Error", "Recuerde que para cargar una cantidad va un asterisco y la cantidad en números enteros, ejemplo:\n*5", QMessageBox.Ok)
                        self.Cantidad_Prox = 0
                self.LINE_BLOQUEO = True
                self.ui.line_Codigo.setText("")
                self.ui.line_Codigo.setFocus()
                self.LINE_BLOQUEO = False
                return True
            
            # Alterna entre pantallas de ventas
            elif aux == "+":

                self.LINE_BLOQUEO = True
                self.ui.line_Codigo.setText("")
                self.ui.line_Codigo.setFocus()
                self.LINE_BLOQUEO = False
                return True
            
            # Elimina el último producto. En realidad se controla con el primer caracter si es que es un comando, y luego con 2 "--" recién se elimina
            elif aux == "-":
                # Cuando colocan el signo "-" y presionan Enter
                if len(texto) == 1:
                    self.Elimina_Item()
                # Cuando presionan 2 veces el signo "-"
                elif texto == "--":
                    self.Quita_Seleccion()
                    self.Elimina_Item()
                else:
                    pos = int(texto[1:])
                    self.ui.listWidget_1.setCurrentIndex(int(pos))
                    self.Elimina_Item()
                self.LINE_BLOQUEO = True
                self.ui.line_Codigo.setText("")
                self.ui.line_Codigo.setFocus()
                self.LINE_BLOQUEO = False
                return True
            
            # Cuando no es un comando
            else:
                # Si en el primer caracter no hay un símbolo, entonces no puede ser un comando
                if "-" in texto or "+" in texto or "/" in texto or "*" in texto:
                    self.ui.line_Codigo.setText("")
                    return True
                return False
        else:
            if texto == "--":
                pass

    # Le debe llegar una lista con todos los datos de un producto, suma a un producto si ya se repite, tener en cuenta que si un producto tiene un descuento en la mitad de sus
        # cantidades, tal vez sea más simple sólamente cargar el Descuento por monto y no por porcentaje.
    def Carga_Prod_Datos(self, Lista, Bulto = False):
        # Parámetro: Lista, son los datos del producto a agregar
        # Bulto: es en el caso de que se haya leído un cód x bulto

        # True: El producto ya está cargado. False: un producto nuevo se suma a la lista
        if Lista[0] in self.LISTA_CODIGOS:

            # Obtenemos la posición de los datos del producto, dentro de la lista con todos los datos
            pos = self.LISTA_CODIGOS.index(Lista[0])

            # Actualizamos la LISTA_AUXILIAR donde quedarán los datos del producto actual
            self.Completa_Auxiliar_Prod(pos)
        else:
            # Actualizamos la LISTA_AUXILIAR donde quedarán los datos del producto actual
            self.Completa_Auxiliar_BD(Lista, Bulto = Bulto)

        # Rellenamos los widgets con los datos que ya tenemos actualizados en la LISTA_AUXILIAR
        self.Muestra_Datos()

    # Carga los datos de la LISTA_AUXILIAR, desde los datos de un producto, o sea, cuando se ingresa por primera vez un producto (Lista = Base de datos)
    def Completa_Auxiliar_BD(self, Lista, Bulto = False):
        # Mediante el parametro Bulto, podemos saber si el usuario cargó un cód x bulto o no, en caso de serlo se agrega la cantidad que trae el bulto sino 0
        self.LISTA_AUXILIAR = []

        self.LISTA_AUXILIAR.append(Lista[1])
        if Bulto == False:
            self.LISTA_AUXILIAR.append(0.0)
        else:
            self.LISTA_AUXILIAR.append(Lista[3])
        self.LISTA_AUXILIAR.append(Lista[14])
        self.LISTA_AUXILIAR.append(Lista[18])
        self.LISTA_AUXILIAR.append("{} {} {}".format(Lista[4],Lista[5],Lista[6]))
        self.LISTA_AUXILIAR.append(Lista[14])
        self.LISTA_AUXILIAR.append(Lista[18])
        if Lista[26] > 0.0:
            self.LISTA_AUXILIAR.append(True)
            self.LISTA_AUXILIAR.append(Lista[26])
        else:
            self.LISTA_AUXILIAR.append(False)
            self.LISTA_AUXILIAR.append((self.PORCENTAJE - 1) * 100)
        self.LISTA_AUXILIAR.append(0.0)
        self.LISTA_AUXILIAR.append(0.0)
        self.LISTA_AUXILIAR.append(Lista[18])
        self.LISTA_AUXILIAR.append(Lista[14])
        self.LISTA_AUXILIAR.append(Lista[14] * self.LISTA_AUXILIAR[1])
        self.LISTA_AUXILIAR.append(str(self.CONT_ID))
        self.CONT_ID += 1
        # Una vez creado todos los espacios correctamente, actualizamos el precio de venta y el sugerido en función al incremento que deberían tener
        self.LISTA_AUXILIAR[6] = self.LISTA_AUXILIAR[12] * (1 + (self.LISTA_AUXILIAR[8] / 100))
        self.LISTA_AUXILIAR[11] = self.LISTA_AUXILIAR[6]

    # # Carga los datos de la LISTA_AUXILIAR, desde los datos pre-cargados en la LISTA_PRODUCTOS
    def Completa_Auxiliar_Prod(self, Pos):
        self.LISTA_AUXILIAR = []

        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][0])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][1])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][2])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][3])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][4])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][5])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][6])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][7])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][8])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][9])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][10])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][11])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][12])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][13])
        self.LISTA_AUXILIAR.append(self.LISTA_PRODUCTOS[Pos][14])

    # Usando los valores de la LISTA_AUXILIAR calcula los subtotales y actualiza los labels (Unitario_Final - Pcio_Vta_Sugerido - line_Pcio_Vta_Nuevo - SUBTOTAL)
    # Tener en cuenta que ya se tiene el precio de costo del producto (AUXILIAR[5]) con los descuentos incluídos y que actualiza las posiciones 6,10,11,12,13 de AUXILIAR.
    def Calcula_Subtotales(self):
        self.LINE_BLOQUEO = True
        # En el caso de que se haya cargado un porcentaje de descuento, al modificarse el Pcio Costo Actual, se debe actualizar el Descuento en pesos tmb.
        if self.LISTA_AUXILIAR[9] > 0.0:
            aux = self.LISTA_AUXILIAR[9] / 100
            self.LISTA_AUXILIAR[10] = self.LISTA_AUXILIAR[5] * (aux)

        # Precio Unitario Final con descuento incluído
        self.LISTA_AUXILIAR[12] = self.LISTA_AUXILIAR[5] - self.LISTA_AUXILIAR[10]
        self.ui.label_Unit_Final.setText(form.Formato_Decimal(self.LISTA_AUXILIAR[12], 2))

        # Precio de Venta Sugerido
        self.LISTA_AUXILIAR[11] = self.LISTA_AUXILIAR[12] * (1 + (self.LISTA_AUXILIAR[8] / 100))
        self.ui.label_Pcio_Vta_Sug.setText(form.Formato_Decimal_S_Punto_Mil(self.LISTA_AUXILIAR[11], 2))

        # Nuevo Precio de Venta
        self.ui.line_Pcio_Vta.setText(form.Formato_Decimal_S_Punto_Mil(self.LISTA_AUXILIAR[11], 2))
        self.LISTA_AUXILIAR[6] = self.LISTA_AUXILIAR[11]

        # Subtotal, precio de costo * cantidad
        self.LISTA_AUXILIAR[13] = form.Redondear_float(self.LISTA_AUXILIAR[1] * self.LISTA_AUXILIAR[12], 2)
        self.ui.label_Subtotal.setText(form.Formato_Decimal(self.LISTA_AUXILIAR[13], 2))
        self.LINE_BLOQUEO = False

    # Suma los subtotales y coloca el total en el label. Al mismo tiempo devuelve el valor total en formato float si es que lo requieren
    def Suma_Compra_Completa(self):
        aux = 0.0
        if len(self.LISTA_PRODUCTOS) > 0:
            for sub in self.LISTA_PRODUCTOS:
                aux += sub[13]
            self.ui.label_Total.setText(form.Formato_Decimal(aux, 2))
        else:
            self.ui.label_Total.setText("0,00")
        return aux












