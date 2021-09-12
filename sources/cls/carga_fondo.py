'''
SE UTILIZA PARA CULMINAR LA CARGA DE UNA VENTA INDICANDO A DÓNDE VA A IR LA PLATA

    Lista_Datos[8] es una copia del diccionario que se usó para rellenar las listas en la ventana de Ventas, ya que ahí está toda la info q necesitamos. El valor 
    que tenga cada producto en dicha lista es lo que hay que cargar, es decir, que si algo tiene o no descuento no nos importa, porque ése valor ya viene correcto desde la 
    lista.
        # Su Clave es el ID del producto. Luego contiene una lista con los datos del ítem dentro de las listas:
        # 0: Nro
        # 1: Concepto
        # 2: Pcio unit
        # 3: cantidad
        # 4: subtotal
        # 5: V-F si es o no es una promoción
        # 6: Caja asociada
'''

#from PyQt5 import QtWidgets, QtCore
#from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog
#from vtn.vtn.vtn_carga_fondos import Ui_Vta_Fondos
from App_Caja import *

import sources.mod.form as form
import sources.mod.mdbprod as mdbprod
import sources.mod.mdbegen as mdbegen
import sources.mod.vars as mi_vars

class V_Carga_Fondo(QMainWindow):

    # Cuando se hace clic en un FONDO desde su lista
    def Clic_Lista_Fondos(vtn_w, Lista_Datos):
        if Lista_Datos[6] == True:
            if Lista_Datos[3] == 0.0:
                #texto = form.Formato_Decimal(Lista_Datos[2], 2)
                vtn_w.lineEdit_3.setText(str(Lista_Datos[2]))
                Lista_Datos[1] = mi_vars.INCREMENTOS[vtn_w.list_fondos_3.currentRow()]
            else:
                vtn_w.lineEdit_3.setText(str(Lista_Datos[2] - Lista_Datos[3]))
                Lista_Datos[1] = mi_vars.INCREMENTOS[vtn_w.list_fondos_3.currentRow()]
                #texto = form.Formato_Decimal(Lista_Datos[2] - Lista_Datos[3], 2)
            #vtn_w.lineEdit_3.setText(texto)
            V_Carga_Fondo.Foco(vtn_w, 2)

    # Cuando se muestra la ventana, se actualizan todos los valores en función de la venta actual
    def Mostrar(vtn_w, Lista_Datos):
        # Deshabilitamos el botón de CARGAR para que sólo esté activo cuando se puede usar nada más
        vtn_w.push_cargar_3.setEnabled(False)
        # Limpiamos las listas
        vtn_w.list_fondos_3.clear()
        vtn_w.list_resumen_3.clear()
        # Actualizamos la lista de FONDOS, ya que si no lo hacemos ahora, deberían reiniciar el programa cuando le agregan un nuevo FONDO
        # También generamos una lista que contiene los ID de las listas de fondos, ya que es útil luego para identificarlas al hacer clic en dicha lista
        Lista_Datos[4] = []
        tabla = mdbegen.Dev_Tabla(mi_vars.BASE_GENERAL_PPAL, "Fondos", "Orden")
        cont = 0
        for reg in tabla:
            if reg[2] > 0:
                cont += 1
                vtn_w.list_fondos_3.addItem(str(cont) + ") " + reg[3])
                Lista_Datos[4].append(reg[0])
        # Reiniciamos la variable que contiene la deuda total del cliente
        Lista_Datos[2] = 0.0
        # Reiniciamos la variable que contiene la suma de los fondos de donde el cliente nos paga
        Lista_Datos[3] = 0.0
        # Reiniciamos la lista que acumula los fondos y montos
        Lista_Datos[5] = []
        # Calculamos el total de la deuda, que si bien podría venir indicado, lo calculamos porque es una tarea simple y tenemos todos los datos cargados en el diccionario
            # tiene que venir sí o sí desde la ventana de Ventas
        for valores in Lista_Datos[8]:
            Lista_Datos[2] += valores[4]
        # Mostramos el total de la deuda
        vtn_w.label_total_venta_3.setText(form.Formato_Decimal(Lista_Datos[2], 2))
        # Limpiamos el line donde se carga los totales de los fondos que está pagando el cliente
        vtn_w.label_total_fondos_3.setText("0,00")
        V_Carga_Fondo.Foco(vtn_w, 1)

    # Return del Line_Monto
    def Return_line_Monto(vtn, vtn_w, Lista_Datos):
        aux = form.Str_Float(vtn_w.lineEdit_3.text())
        if aux > 0.0:
            if Lista_Datos[1] > 0:
                Msj = ""
                if Lista_Datos[1] == 1:
                    Msj = "%:"
                elif Lista_Datos[1] == 2:
                    Msj = '% de descuento:'
                elif Lista_Datos[1] == 3:
                    Msj = "Incremento:"
                elif Lista_Datos[1] == 4:
                    Msj = "Descuento:"
                
                # Bucle para solicitar un valor correcto hasta que lo coloquen bien, sino pueden cancelar o dejar vacío el cuadro de texto
                bucle = True
                while bucle == True:
                    texto, ok = QInputDialog.getText(vtn, "", "Ingrese " + Msj)
                    if texto != "" and ok:
                        if form.Es_Numero(texto, coma = True):
                            nuevo_valor = float(form.Ajusta_A_2_Dec(form.Str_Float_Punto(texto)))
                            if Lista_Datos[1] < 3:
                                nuevo_valor = float(form.Ajusta_A_2_Dec((nuevo_valor * aux) / 100))

                            # Actualizamos la variable con el valor de la deuda total. Tener en cuenta que éste valor no afecta a la carga de la venta en la base de datos, 
                                # porque esos datos se toman del diccionario, y como nunca lo modificamos en las bases de datos seguimos cargando la ganancia generada por la 
                                # venta habitual
                            Lista_Datos[2] += nuevo_valor
                            # Actualizamos el valor del monto total en el label
                            vtn_w.label_total_venta_3.setText(form.Formato_Decimal(Lista_Datos[2], 2))

                            Lista_Datos[3] += (aux + nuevo_valor)
                            V_Carga_Fondo.Agrega_registro(vtn_w, Lista_Datos, aux, nuevo_valor)
                            if V_Carga_Fondo.Calcula_Resultado(vtn_w, Lista_Datos) == False:
                                vtn_w.lineEdit_3.setText("0,00")
                                Lista_Datos[6] = False
                                V_Carga_Fondo.Foco(vtn_w, 1)
                                Lista_Datos[6] = True
                            else:
                                Lista_Datos[7] = True
                            bucle = False
                        else:
                            QMessageBox.question(vtn, "Error", "El valor ingresado contiene letras, símbolos o algún caracter inválido.", QMessageBox.Ok)
                    else:
                        bucle = False
            else:
                Lista_Datos[3] += aux
                V_Carga_Fondo.Agrega_registro(vtn_w, Lista_Datos, aux)
                if V_Carga_Fondo.Calcula_Resultado(vtn_w, Lista_Datos) == False:
                    vtn_w.lineEdit_3.setText("0,00")
                    Lista_Datos[6] = False
                    V_Carga_Fondo.Foco(vtn_w, 1)
                    Lista_Datos[6] = True
                else:
                    Lista_Datos[7] = True
        else:
            QMessageBox.question(vtn, "Error", "El valor ingresado no puede ser igual a 0.", QMessageBox.Ok)

    # Agrega a la lista los datos de la venta, fondo y monto que se está pagando, y actualiza el label total_fondos
    def Agrega_registro(vtn_w, Lista_Datos, valor_line, modificacion = 0.0):
        # Agregamos a la lista donde guardamos los fondos, el id correspondiente
        Lista_Datos[5].append(Lista_Datos[4][vtn_w.list_fondos_3.currentRow()])
        # Agregamos a la misma lista, el monto que debe incorporarse a ese fondo
        Lista_Datos[5].append(valor_line)
        # Preparamos el texto a mostrar
        # Obtenemos el texto que dice en la lista de fondos para luego traspasarlo en la lista de resumen
        texto = vtn_w.list_fondos_3.currentItem().text()
        if modificacion == 0.0:
            texto = "  >>>  " + texto[3:]
        else:
            if Lista_Datos[1] < 3:
                texto = "  >>>  (" + form.Formato_Decimal(valor_line, 2) + "  +  " + form.Formato_Decimal(modificacion, 2) + ") - " + texto[3:]
        # Sumamos el dato a la lista resumen
        vtn_w.list_resumen_3.addItem(form.Formato_Decimal((valor_line + modificacion), 2) + texto)
        # Dejamos asentado el total de la lista de resumen
        vtn_w.label_total_fondos_3.setText(form.Formato_Decimal(Lista_Datos[3], 2))
    
    # Función que controla si coinciden el monto del fondo con la dueda, y habilita o no el botón de cargar
    def Calcula_Resultado(vtn_w, Lista_Datos):
        if Lista_Datos[3] == Lista_Datos[2]:
            vtn_w.push_cargar_3.setEnabled(True)
            V_Carga_Fondo.Foco(vtn_w, 5)
            return True
        else:
            vtn_w.push_cargar_3.setEnabled(False)
            return False

    # Para ayudar al usuario, cada vez que un elemento tiene el foco le remarcamos el fondo. Creamos una función que le da fondo al elemento según un parámetro
    def Foco(vtn_w, elemento):
        # Restauramos el color de todos los groupbox
        vtn_w.groupBox_31.setStyleSheet("background-color: rgb(208, 211, 212);")
        vtn_w.groupBox_32.setStyleSheet("background-color: rgb(208, 211, 212);")
        vtn_w.groupBox_33.setStyleSheet("background-color: rgb(208, 211, 212);")
        vtn_w.groupBox_34.setStyleSheet("background-color: rgb(208, 211, 212);")
        vtn_w.groupBox_35.setStyleSheet("background-color: rgb(208, 211, 212);")
        # Colocamos en ROJO el fondo de lo que va a obtener el FOCUS
        if elemento == 1:
            vtn_w.groupBox_31.setStyleSheet("background-color: rgb(200,0,0);")
            # Deseleccionamos el ítem que se haya seleccionado con anterioridad
            vtn_w.list_fondos_3.setCurrentRow(-1)
            vtn_w.list_fondos_3.setFocus()
        elif elemento == 2:
            vtn_w.groupBox_32.setStyleSheet("background-color: rgb(200,0,0);")
            # Hacemos que aparezca el line seleccionado para poder cambiar su valor
            vtn_w.lineEdit_3.selectAll()
            vtn_w.lineEdit_3.setFocus()
        elif elemento == 3:
            vtn_w.groupBox_33.setStyleSheet("background-color: rgb(200,0,0);")
            # Deseleccionamos el ítem que se haya seleccionado con anterioridad
            vtn_w.list_resumen_3.setCurrentRow(-1)
            vtn_w.list_resumen_3.setFocus()
        elif elemento == 4:
            vtn_w.groupBox_34.setStyleSheet("background-color: rgb(200,0,0);")
            vtn_w.push_cancelar_3.setFocus()
        elif elemento == 5:
            vtn_w.groupBox_35.setStyleSheet("background-color: rgb(200,0,0);")
            vtn_w.push_cargar_3.setFocus()

    # Cuando está todo correcto, se carga la venta
    def Carga_Venta(Lista_Datos):

        # EJECUTAMOS UN BUCLE PARA RECORRER EL DICCIONARIO Y ASÍ IR ACTUALIZANDO LOS DATOS UNO POR UNO
        for valor in Lista_Datos[8]:
            ID_ = valor[0]
            # Precio total de venta
            Pcio_vta_Cant = 0.0
            # Acumulamos la suma de los precios de costo que hubieron en todos los tipos de producto, para luego calcular ganancias
            Pcio_cto_acum = 0.0
            # Guardamos la ganancia que generó la venta de éste producto
            Ganancia = 0.0

            # TABLA STOCK
            # Obtenemos el stock, le restamos y reajustamos los valores según los conjuntos de mercaderías
            # Lista ajustada a lo que necesita la función de la base de datos para actualizar los registros
            Lista_Stock = []
            Lista_Stock.append(ID_)
            # Agregamos 3 espacios para las 3 cantidades que prosiguen
            Lista_Stock.append(0.0)
            Lista_Stock.append(0.0)
            Lista_Stock.append(0.0)
            # Agregamos 3 espacios para las 3 fechas de vencimiento
            Lista_Stock.append(0)
            Lista_Stock.append(0)
            Lista_Stock.append(0)
            # Agregamos 3 espacios para los 3 precios de compra
            Lista_Stock.append(0.0)
            Lista_Stock.append(0.0)
            Lista_Stock.append(0.0)
            # Obtenemos los valores reales de la db
            reg = mdbprod.Reg_Un_param(mi_vars.BASE_DATOS_PPAL, "Stock", "ID", ID_)
            # aux va a ser la cantidad a restar al stock
            aux = valor[3]
            for i in reg:

                # True: Cuando las unidades vendidas superan el conjunto 3 de stock
                if aux > i[3]:
                    Pcio_cto_acum = i[3] * i[9]
                    aux -= i[3]
                    # En éste caso deberíamos poner la lista en 0, pero como ya se hizo así dicha lista, no es necesario volver a cargarle 0
                    pass

                    # True: Cuando las unidades vendidas superan el conjunto 2 de stock
                    if aux > i[2]:
                        Pcio_cto_acum += (i[2] * i[8])
                        aux -= i[2]
                        pass
                        
                        # Acá llegamos al conjunto de stock 1. Si la cantidad de éste conjunto es suficiente o no, es irrelevante para calcular el precio de costo ya que vamos
                            # a utilizar de todas formas su valor de Pcio_costo para calcular los costos totales. Si bien nunca se debería vender más cantidades de las que 
                            # quedan en el conjunto 1, ésto puede darse igual cuando hay errores de control de stock y lo que hacemos es seguir calculando con esos valores.
                        Pcio_cto_acum += (aux * i[7])

                        # NO SE BORRA EL ÚLTIMO PRECIO DE COSTO POR ESO CON ÉSTA LÍNEA LO MANTENEMOS:
                            # La causa es que si por alguna razón se controlaron mal las cantidades y tenemos en existencia mercadería que no figura en stock, 
                            # debemos tomar de algún lado un precio de costo porque sino su venta generará un 100% de ganancia y eso es claramente un error.
                        Lista_Stock[7] = i[7]

                        # Cuando las unidades vendidas superan al conjunto 1 de stock
                        if aux > i[1]:
                            Lista_Stock[1] = i[1] - aux

                        else:
                            # False: Cuando las unidades vendidas bastan con el conjunto 1 de stock
                            if aux == i[1]:
                                pass
                            else:
                                Lista_Stock[1] = i[1] - aux
                                Lista_Stock[4] = i[4]

                    else:
                        # False: Cuando las unidades vendidas bastan con las que tenemos en el conjunto 2
                        Pcio_cto_acum += (aux * i[8])
                        if aux == i[2]:
                            Lista_Stock[1] = i[1]
                            Lista_Stock[4] = i[4]
                            Lista_Stock[7] = i[7]
                        else:
                            Lista_Stock[1] = i[1]
                            Lista_Stock[4] = i[4]
                            Lista_Stock[7] = i[7]

                            Lista_Stock[2] = i[2] - aux
                            Lista_Stock[5] = i[5]
                            Lista_Stock[8] = i[8]

                else:
                    # False: Cuando las unidades vendidas bastan con las cargadas en el conjunto 3
                    Pcio_cto_acum = aux * i[9]
                    if aux == i[3]:
                        Lista_Stock[1] = i[1]
                        Lista_Stock[4] = i[4]
                        Lista_Stock[7] = i[7]

                        Lista_Stock[2] = i[2]
                        Lista_Stock[5] = i[5]
                        Lista_Stock[8] = i[8]
                    else:
                        Lista_Stock[1] = i[1]
                        Lista_Stock[4] = i[4]
                        Lista_Stock[7] = i[7]

                        Lista_Stock[2] = i[2]
                        Lista_Stock[5] = i[5]
                        Lista_Stock[8] = i[8]

                        Lista_Stock[3] = i[3] - aux
                        Lista_Stock[6] = i[6]
                        Lista_Stock[9] = i[9]

                # Calculamos la cantidad total
                Lista_Stock.append(Lista_Stock[1] + Lista_Stock[2] + Lista_Stock[3])
                # Mantenemos el mismo precio de venta
                Lista_Stock.append(i[11])
                # Mantenemos el stock verificado
                Lista_Stock.append(i[12])
                # Se actualiza la base de datos, tabla de STOCK
                mdbprod.Act_Stock_Segun_ID_Por_Lista(Lista_Stock)
            
            Pcio_vta_Cant = valor[4]

            # TABLA ESTADISTICAS
            # Lista ajustada a lo que necesita la función de la base de datos para actualizar los registros
            Lista_Estadistica = []
            Lista_Estadistica.append(ID_)
            # Agregamos 4 espacios para las ganancias semanales, mensuales, anuales y totales
            Lista_Estadistica.append(0.0)
            Lista_Estadistica.append(0.0)
            Lista_Estadistica.append(0.0)
            Lista_Estadistica.append(0.0)
            # Agregamos 4 espacios para las cantidades vendidas semanales, mensuales, anuales y totales
            Lista_Estadistica.append(0.0)
            Lista_Estadistica.append(0.0)
            Lista_Estadistica.append(0.0)
            Lista_Estadistica.append(0.0)
            # Aquí van la cantidad de siniestros, así que mantenemos el valor que venía por defecto
            Lista_Estadistica.append(0.0)
            # Obtenemos los valores reales de la db
            reg = mdbprod.Reg_Un_param(mi_vars.BASE_DATOS_PPAL, "Estadistica", "ID", ID_)
            Ganancia = float(form.Ajusta_A_2_Dec(valor[4] - Pcio_cto_acum))
            for i in reg:
                # Preparamos las ganancias
                Lista_Estadistica[1] += i[1] + Ganancia
                Lista_Estadistica[2] += i[2] + Ganancia
                Lista_Estadistica[3] += i[3] + Ganancia
                Lista_Estadistica[4] += i[4] + Ganancia
                # Preparamos las cantidades vendidas
                Lista_Estadistica[5] += i[5] + valor[3]
                Lista_Estadistica[6] += i[6] + valor[3]
                Lista_Estadistica[7] += i[7] + valor[3]
                Lista_Estadistica[8] += i[8] + valor[3]
                # Valor del siniestro se mantiene igual
                Lista_Estadistica[9] = i[9]
            mdbprod.Act_Estadisticas_Segun_ID_Por_Lista(Lista_Estadistica)

            # Se ajustan los valores de las cajas
            reg = mdbprod.Reg_Un_param(mi_vars.BASE_GENERAL_PPAL, "Cajas", "ID", valor[6])
            situacion = 0.0
            ingresoDia = 0.0
            ingresoSem = 0.0
            ingresoMen = 0.0
            ingresoAnu = 0.0
            ingresoTot = 0.0
            for i in reg:
                situacion = i[3] + Pcio_vta_Cant
                ingresoDia = i[4] + Pcio_vta_Cant
                ingresoSem = i[5] + Pcio_vta_Cant
                ingresoMen = i[6] + Pcio_vta_Cant
                ingresoAnu = i[7] + Pcio_vta_Cant
                ingresoTot = i[8] + Pcio_vta_Cant
            # Por las dudas que no haya algún error y sobreescribamos algún dato incorrecto, vamos a realizar un control
            if Pcio_vta_Cant > 0.0:
                mdbegen.Act_Cajas_Ingresos_ID(situacion, ingresoDia, ingresoSem, ingresoMen, ingresoAnu, ingresoTot, valor[6])
            
        # Se ajustan los valores de los FONDOS
        # Recorremos la lista que indica a qué fondo ingresar la venta y el monto
        tope = len(Lista_Datos[5])
        for i in range(tope):
            cargar = False
            if i == 0:
                cargar = True
                reg = mdbprod.Reg_Un_param(mi_vars.BASE_GENERAL_PPAL, "Fondos", "ID", Lista_Datos[5][0])
                for n in reg:
                    situacion = n[4] + Lista_Datos[5][1]
                    ingresoDia = n[5] + Lista_Datos[5][1]
                    ingresoSem = n[6] + Lista_Datos[5][1]
                    ingresoMen = n[7] + Lista_Datos[5][1]
                    ingresoAnu = n[8] + Lista_Datos[5][1]
                    ingresoTot = n[9] + Lista_Datos[5][1]
            elif (i / 2) == (i // 2):
                cargar = True
                reg = mdbprod.Reg_Un_param(mi_vars.BASE_GENERAL_PPAL, "Fondos", "ID", Lista_Datos[5][i])
                for n in reg:
                    situacion = n[4] + Lista_Datos[5][i + 1]
                    ingresoDia = n[5] + Lista_Datos[5][i + 1]
                    ingresoSem = n[6] + Lista_Datos[5][i + 1]
                    ingresoMen = n[7] + Lista_Datos[5][i + 1]
                    ingresoAnu = n[8] + Lista_Datos[5][i + 1]
                    ingresoTot = n[9] + Lista_Datos[5][i + 1]
            else:
                cargar = False
            if cargar == True:
                mdbegen.Act_Fondos_Ingresos_ID(situacion, ingresoDia, ingresoSem, ingresoMen, ingresoAnu, ingresoTot, Lista_Datos[5][i])







