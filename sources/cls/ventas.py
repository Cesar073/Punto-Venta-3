
from sources.mod.mdbegen import DB_Cajas_Totales_Cajas
from typing import List
from App import *
#from sources.cls.Functions import *

import sources.mod.mdbprod as mdb_p
import sources.mod.mdbprom as mdbprom
import sources.mod.form as form
import sources.mod.vars as mi_vars
import sources.mod.func as mi_func

'''
    CAMBIOS REALIZADOS PARA INFORMAR QUE SE HICIERON EN ÉSTA VERSIÓN:


    CAMBIOS QUE ESTOY REALIZANDO AHORA Y QUE NO DEBO ABANDONAR HASTA Q LOS TERMINE.
    INCORPORÉ UN NÚMERO DE GUÍA EN LA LISTA DE VENTA REAL, PARA QUE TENGA RELACIÓN DIRECTA CON LA Lista_Datos[22] Y ASÍ, UTILIZANDO ESOS VALORES PUEDO ELIMINAR Y/O ENCONTRAR
        CUALQUIER VALOR EN AMBAS SIN PROBLEMAS. POR EJ, SI EL 4TO PRODUCTO QUE SE PASA ES UNA PROMO, EN PANTALLA VAMOS A MOSTRAR EL  VALOR 4 Y EL NOMBRE DE LA PROMO, Y EN LA LISTA
        DE VENTA REAL, VAMOS A CARGAR TODOS LOS PRODUCTOS DE UNO EN UNO PERO CON SU NÚMERO DE GUÍA 4, ENTONCES SI POR EJ SE ELIMINA LA PROMO EN LA POSICIÓN 4, EL PRGM SABE QUE 
        TIENE QUE ELIMINAR TODOS LOS PRODUCTOS CON GUIA 4.
        TAMBIÉN NOS SIRVE PARA MOSTRAR SI SE NECESITA SABER QUE PRODUCTOS TENÍA LA PROMO, PODEMOS PONER UN MSJ EN PANTALLA PARA TAL FIN.
    TAMBIÉN VAMOS A CARGAR COMO VALOR DE PROMO, EL PRECIO FINAL Y AJUSTAR LOS MISMOS PARA TAL FIN.
    Y AL FINAL LE AGREGO UN ESPACIO PARA COLOCAR EL CODIGO DE LA PROMO (STRING), ESTANDO VACÍO EN EL CASO DE UN PRODUCTO NORMAL O CONTENIENDO EL CODIGO DE LA PROMO EN FORMATO TEXT.

    INCORPORAR VENTANAS TRUCHAS PARA EVITAR LA PÉRDIDA DEL FOCO.

    HACER PROXIMO:
        * Reparar bugs al eliminar promo.
        * Controlar el Foco, para que funcione mejor, en todo momento se dirija al lugar donde corresponde, y q sepa cuando tiene que limpiar variables.
        * Que se puedan desactivar y activar promos.
        * IMPORTANTE: QUE SOLUCIONE EL TEMA DE PROMOCIONES QUE AL ACTUALIZAR NO SE ACTUALIZAN LOS PRECIOS INDIVIDUALES

    HACER FUTURO:
        * Preparar un plan de Emergencia para cortes de luz, que se rompa una u otra PC, etc...
        * Hacer que funcione bien el aviso con el label_Msj, las cantidades que está por cargar (rojo)
        * Hacer que funcione bien el aviso con el label_Msj, la carga de promos (axzul)
        * Generar registro de ventas.
        * Que se puedan eliminar productos leyendo el código del mismo. Por ej, cargué 5 aceites y devuelvo 1, mediante la lectura de su cod deberían quedarme 4.

        * Que un mismo producto pueda pertenecer a más de una promo.
        * Mejorar el sistema de red para que ambas PC trabajen con una única base de datos y la puedan editar.
        * Hay que configurar la variable mi_vars.btn_igual, es el botón extra que tenemos en el pad numérico.
        * qUE PUEDA alternar entre ventas, entre pantallas. VER COMANDOS ESPECIALES
        * Ver si la ejecución de Mostrar, no es que termina llamando siempre a showEvent, quizás deba quitarla
        * Revisar y hacer que funcionen todos los comandos especiales
        * Cargar una venta, pero que diferencie las promos y que registre hora de carga
        * Cuenta que pueda modificar los precios tipo admin.
        * Que al hacer clic en una promo que ya esté cargada en pantalla, se pueda ver los productos que la componen.

    CAMBIOS REALIZADOS V 1.0:
        + El actualizador debe colocar en los códigos de las promos de la tabla Adicionales, un guión o un signo + para indicar el tipo de promo.
        + Incorporación del sistema de Red.
        + Promociones reducidas a un sólo renglón.
        + Reparaciones de los métodos de borrado de productos.
        + Incorporación del botón de Limpiar Pantalla.
        + Ventanas sustitutas para no perder el foco.
        + Métodos abreviados para cuando se pierde el foco y dirigirlo hacia el line_codigo. En line_monto se puede casi con cualquier símbolo y no sólo con la barra.
            - La barra en cualquier parte del programa nos lleva al foco del line_cod.
        + Adecuar pgm a las pantallas cuadradas.
        + Incorporación de botón pre-seleccionado cuando aparece un mensaje en pantalla.
'''

class V_Ventas(QMainWindow):    

    '''#############################################################################################################################################
                                                            FUNCIONES DE VENTANA
    #############################################################################################################################################'''

    # Lo que queremos que se ejecute al mostrar la página
    def Mostrar(vtn_w):
        vtn_w.stackedWidget.setCurrentWidget(vtn_w.page_Ventas)
        vtn_w.line_Codigo.setFocus()

    # Sirve para limpiar toda la ventana, o para limpiar los datos luego de haberse cargado un producto a la lista
    def Limpia_Ventana(vtn_w, Lista_Datos):
        for i in reversed(range(vtn_w.verticalLayout_5.count())): 
            widgetToRemove = vtn_w.verticalLayout_5.itemAt(i).widget()
            # remove it from the layout list
            vtn_w.verticalLayout_5.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)
        # Limpiamos los widgets
        vtn_w.line_Codigo.clear()
        vtn_w.label_Imagen.clear()
        vtn_w.line_Monto.clear()
        vtn_w.label_Vuelto.setText("0,00")
        vtn_w.label_Total.setText("0,00")
        '''
        vtn_w.listWidget_2.clear()
        vtn_w.listWidget_3.clear()
        vtn_w.listWidget_4.clear()
        vtn_w.listWidget_5.clear()
        vtn_w.listWidget_6.clear()
        '''
        # Limpiamos las variables
        Lista_Datos[24] = 0
        Lista_Datos[21] = []
        Lista_Datos[22] = []
        Lista_Datos[23] = []
        Lista_Datos[28] = ""
        Lista_Datos[31] = 0
        Lista_Datos[29] = False
        V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)

        vtn_w.line_Codigo.setFocus()

    # Coloca los colores en la ventana según el formato que desee
    def Config_Mensaje(vtn_w, Lista_Datos, Mensajes = 0):
        R = 0
        G = 0
        B = 0

        # Restauramos el label de los msjs
        if Mensajes == 0:
            Lista_Datos[24] = 0
            vtn_w.label_Msj.setText("")
            if Lista_Datos[25] == 1:
                R = Lista_Datos[3]
                G = Lista_Datos[4]
                B = Lista_Datos[5]
            elif Lista_Datos[25] == 2:
                R = Lista_Datos[6]
                G = Lista_Datos[7]
                B = Lista_Datos[8]
            elif Lista_Datos[25] == 3:
                R = Lista_Datos[9]
                G = Lista_Datos[10]
                B = Lista_Datos[11]

        # Cantidad próxima
        elif Mensajes == 1:
            R = Lista_Datos[12]
            G = Lista_Datos[13]
            B = Lista_Datos[14]
            vtn_w.label_Msj.setText("CANTIDAD: {}".format(str(Lista_Datos[24])))

        # Promociones
        elif Mensajes == 2:
            R = Lista_Datos[15]
            G = Lista_Datos[16]
            B = Lista_Datos[17]
            vtn_w.label_Msj.setText("SI - NO    >>> Cargar la sgte. PROMO: {}".format(""))
        
        # Se borrará algún producto
        elif Mensajes == 3:
            R = Lista_Datos[18]
            G = Lista_Datos[19]
            B = Lista_Datos[20]
            vtn_w.label_Msj.setText("Indique el índice o elimine el último producto con 2 guiones (--).")

        # Le asignamos el color seleccionado al fondo del label de mensajes
        vtn_w.label_Msj.setStyleSheet("background-color: rgb({}, {}, {});".format(R, G, B))

    # Configura y muestra el groupbox que simula ser ventana de ingreso de datos (Precio, Litros, Kg, etc). Tener en cuenta que con sólo llamar a la función indicando lo que
        # se va a hacer, ella se encarga de configurar todo lo relativo a las cargas de datos.
    def Config_Ingreso_Precio(vtn_w, Lista_Datos, Tipo = 0):
        # Parametros:
            # Tipo= 0: Es para restaurar la ventana, y limpia variables tmb.
            # Tipo= 1: Unidad - 2: Peso - 3: Litros - 4: cm3 - 5: Precio
        if Tipo > 0:
            vtn_w.groupBox_Ingresos.setVisible(True)
            Titulo = ""
            if Tipo == 1:
                Titulo = "Ingrese cantidad"
            elif Tipo == 2:
                Titulo = "Ingrese Peso (Kg)"
            elif Tipo == 3:
                Titulo = "Ingrese Litros"
            elif Tipo == 4:
                Titulo = "Ingrese cm3"
            elif Tipo == 5:
                Titulo = "Ingrese Precio"
            elif Tipo == 6:
                Titulo = "Pcio: {}".format(Lista_Datos[22][-1][1])
            elif Tipo == 11:
                Titulo = "Ingrese Código"
            
            vtn_w.stackedWidget.setCurrentWidget(vtn_w.page_msjs)
            vtn_w.groupBox_Ingresos.setVisible(True)
            vtn_w.groupBox_Ingresos.setTitle(Titulo)
            vtn_w.groupBox_Promos.setVisible(False)

            Lista_Datos[31] = Tipo
            vtn_w.line_Ingresos.clear()
            vtn_w.line_Ingresos.setFocus()
        else:
            Lista_Datos[31] = 0
            V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
            vtn_w.stackedWidget.setCurrentWidget(vtn_w.page_Ventas)

    # Configura y muestra el groupbox que simula ser ventana de ingreso Productos para promociones
    def Config_Ingreso_Promo(vtn_w, Lista_Datos, Coloca = True):
        # Parametros:
            # Coloca= True: Por defecto, configura la pantalla para colocar el mensaje.
            # Coloca= False: Devuelve el estado de la pantalla a la normalidad.
        if Coloca == True:
            vtn_w.groupBox_Promos.setVisible(True)
            vtn_w.groupBox_Datos.setEnabled(False)
            vtn_w.listWidget_2.setEnabled(False)
            vtn_w.listWidget_3.setEnabled(False)
            vtn_w.listWidget_4.setEnabled(False)
            vtn_w.listWidget_5.setEnabled(False)
            vtn_w.listWidget_6.setEnabled(False)
            vtn_w.push_Eliminar.setEnabled(False)
            vtn_w.push_Limpiar_Venta.setEnabled(False)
            vtn_w.push_Uno.setEnabled(False)
            vtn_w.push_Dos.setEnabled(False)
            vtn_w.push_Tres.setEnabled(False)
            #vtn_w.groupBox_Productos.setEnabled(False)
            #vtn_w.push_Menu.setEnabled(False)
            Lista_Datos[29] = True
            vtn_w.groupBox_Promos.setTitle("Ingrese Promo: {} de {}".format(str(Lista_Datos[30][0]), str(int(Lista_Datos[30][1]))))
            vtn_w.line_Ingreso_Promo.setFocus()
        else:
            vtn_w.line_Ingreso_Promo.clear()
            vtn_w.groupBox_Promos.setVisible(False)
            vtn_w.groupBox_Datos.setEnabled(True)
            vtn_w.listWidget_2.setEnabled(True)
            vtn_w.listWidget_3.setEnabled(True)
            vtn_w.listWidget_4.setEnabled(True)
            vtn_w.listWidget_5.setEnabled(True)
            vtn_w.listWidget_6.setEnabled(True)
            vtn_w.push_Eliminar.setEnabled(True)
            vtn_w.push_Limpiar_Venta.setEnabled(True)
            vtn_w.push_Uno.setEnabled(True)
            vtn_w.push_Dos.setEnabled(True)
            vtn_w.push_Tres.setEnabled(True)
            #vtn_w.groupBox_Productos.setEnabled(True)
            #vtn_w.push_Menu.setEnabled(True)
            Lista_Datos[29] = False
            V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)

    # Configura el mensaje superior referido a la conexión
    def Mensaje_De_Conexion(vtn_w, msj):
        # ROJO
        r = 255
        g = 0
        b = 0
        if msj == 0:
            vtn_w.label.setText("DESCONECTADO")
        elif msj == 1:
            vtn_w.label.setText("Reconectando")
            r = 255
            g = 170
            b = 127
        elif msj == 2:
            vtn_w.label.setText("Conectado")
            r = 35
            g = 200
            b = 35
        vtn_w.frame.setStyleSheet("background-color: rgb({},{},{});".format(r,g,b))

    '''#############################################################################################################################################
                                                        COMANDOS ESPECIALES DE VENTANA
    #############################################################################################################################################'''

    # LINE_COD 1 caracter
    def Comandos_Especiales_1(vtn_w, Lista_Datos, texto):
        if texto == "-":
            V_Ventas.Config_Mensaje(vtn_w, Lista_Datos, Mensajes = 3)

    # LINE_COD 2 caracteres
    def Comandos_especiales_2(vtn, vtn_w, Lista_Datos, texto):

        # Elimina el último ítem
        if texto == "--":
            V_Ventas.Elimina_Item(vtn, vtn_w, Lista_Datos)
            V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
            V_Ventas.Reinicio_Vtn_Parcial(vtn_w, Lista_Datos)

    # Analiza si el texto que se ingresó en el line_cod es un comando especial, y de ser así lo ejecuta
    # INFO SOBRE LOS CÓDIGOS:
        # Hay casos donde 2 códigos distintos hacen la misma tarea, por ejemplo responder con "SI" a preguntas como si quieren aceptar la promo se puede contestar con "CODSI" 
        # o con "+51+". El motivo es porque para usar el lector de códigos utilizo combinaciones de letras para evitar que en algún momento un código inventado por mí se cruce
        # con un código de productos ya que esos son exclusivamente números. Por otro lado necesito crear un código a la par que haga lo mismo pero sin el lector, con el 
        # teclado numérico, porque si por ejemplo se arruina la hoja de códigos o por algún motivo el lector no puede leerlo, tienen que tener una alternativa reproducible con 
        # un poco de facilidad en el teclado numérico (+51+).
        # La razón por la cuál no genero un código para el lector igual al otro (+51+), es porque los códigos de barra que genero con CODE39, no se leen de igual forma en 
        # Windows y Linux, siendo que el único símbolo que entienden por igual ambos sistemas operativos es el signo $, el cuál no contiene ningún teclado numérico. Es decir, 
        # que si genero un código de barras que signifique "+51+", serviría sólo en Windows pero no en Linux. La única combinación que me sirve en ambos es $51$ pero es un 
        # código que no se puede reproducir en el teclado, y por ello es que tengo que hacer sí o sí 2 códigos para un mismo fin. Y ya que hago 2 códigos para lo mismo, hago 
        # algo simple para el teclado y algo más complejo pero práctico para le lector.
    def Comandos_Especiales_Enter(vtn, vtn_w, Lista_Datos, texto):
        try:
            # Primero controlamos si es que es un comando, de lo contrario devolvemos el control del flujo
            aux = texto[0]
            
            # Los comandos comienzan con un signo, así que controlamos eso y dsp seguimos
            if aux == "C" or aux == "+" or aux == "-" or aux == "*" or aux == "/" or aux == mi_vars.BTN_IGUAL:

                # Indica si estamos en una promo o no
                if Lista_Datos[29] == False:

                    # Cambia de precio unitario con el botón del teclado que parece ser un "=", pero no es el mismo en todas las PCs. Tener en cuenta que sólo se trabaja sobre
                    # el útlimo producto cargado.
                    if aux == mi_vars.BTN_IGUAL or texto == "CODPR":
                        # Ya sabemos que se ingresó el código para modificar un precio, ahora vamos a hacer los controles pertinentes
                        # Controlamos que haya algún producto cargado
                        if len(Lista_Datos[21]) > 0:
                            # Teniendo en cuenta que los códigos internos sobretodo de promos tienen menos de 5 caracteres, usamos dicho valor para distinguir un producto de
                                # un código interno
                            if Lista_Datos[21][-1][0] > 0 and Lista_Datos[21][-1][7] == "":
                                V_Ventas.Config_Ingreso_Precio(vtn_w, Lista_Datos, 6)
                        else:
                            QMessageBox.information(vtn, "Atención!", "No hay productos cargados para actualizar.", QMessageBox.Ok)
                        return True
                    
                    # Configuramos la Cantidad_Próxima
                    # Un asterisco seguido de un número es la cantidad a sumar para el próximo producto a cargar.
                    elif aux == "*":

                        largo = len(texto)

                        if largo > 1:
                            if form.Es_Numero_Int(texto[1:]):
                                Lista_Datos[24] = int(texto[1:])
                                V_Ventas.Config_Mensaje(vtn_w, Lista_Datos, 1)
                            else:
                                QMessageBox.question(vtn, "Error", "Recuerde que para cargar una cantidad va un asterisco y la cantidad en números enteros, ejemplo:\n*5", QMessageBox.Ok)
                                Lista_Datos[24] = 0
                                V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
                        else:
                            QMessageBox.question(vtn, "Error", "Recuerde que para cargar una cantidad va un asterisco y la cantidad en números enteros, ejemplo:\n*5", QMessageBox.Ok)
                            Lista_Datos[24] = 0
                            V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)

                        V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
                        return True

                    # Elimina el último producto. En realidad se controla con el primer caracter si es que es un comando, y luego con 2 "--" recién se elimina
                    elif aux == "-" or texto == "CODBO":

                        # Cuando colocan el signo "-" y presionan Enter
                        if len(texto) == 1 or texto == "CODBO":
                            V_Ventas.Elimina_Item(vtn, vtn_w, Lista_Datos)
                        else:
                            try:
                                pos = int(texto[1:])
                                V_Ventas.Elimina_Item(vtn, vtn_w, Lista_Datos, ubi = pos)
                            except:
                                pass
                        V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
                        V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
                        return True
                else:
                    # Alterna entre pantallas de ventas:
                        # 1: +1
                        # 2: +2
                        # 3: +3
                    if aux == "+" or aux == "C":

                        largo = len(texto)
                        if largo == 4 or largo == 5:
                            if texto[3] == "+" or texto[0:3] == "COD":

                                V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)

                                # Cuando el usuario indica: SI
                                if texto == "+51+" or texto == "CODSI":
                                    
                                    # Vemos que tipo de promo es (Fija - Combinada)
                                    aux = ""
                                    ID_Promo = ""
                                    Tipo_Prom = 0
                                    for i in Lista_Datos[23][27]:
                                        if i == "-":
                                            ID_Promo = aux
                                            Tipo_Prom = 1
                                            aux = ""
                                        elif i == "+":
                                            ID_Promo = aux
                                            Tipo_Prom = 2
                                            aux = ""
                                        else:
                                            aux += i
                                    
                                    # Promo simple
                                    if Tipo_Prom == 1:
                                        existe, lista_Auxiliar = mdbprom.Busca_Cod_Promo("Promos", "Codigo", ID_Promo)
                                        V_Ventas.Acepta_Promo_Simple(vtn_w, Lista_Datos, lista_Auxiliar)
                                    elif Tipo_Prom == 2:
                                        existe, lista_Auxiliar = mdbprom.Busca_Cod_Promo("Promos", "Codigo", ID_Promo)
                                        V_Ventas.Acepta_Promo_Compleja(vtn_w, Lista_Datos, lista_Auxiliar, Lista_Datos[23][1])

                                # Cuando el usuario indica NO
                                elif texto == "+80+" or texto == "CODNO":
                                    Lista_Datos[29] = False
                                    V_Ventas.Carga_Prod(vtn_w, Lista_Datos, Lista_Datos[23])

                        V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
                        return True
        except:
            QMessageBox.question(vtn, "ERROR", "Anote el PRODUCTO para tener registro del error.", QMessageBox.Ok)
        return False

    # Al precionar la / que está tanto en el teclado como por código, lo que vamos a hacer es limpiar el line_cod, dirigirle el foco y poner a cero cant_proxima
        # Esto va a ser que la /, sea un recurso casi en todo momento para limpiar esos requechos de datos que no se pueden cancelar, etc...
    def Event_press_barra(vtn_w, Lista_Datos):
        Lista_Datos[27] = True
        vtn_w.line_Codigo.setText("")
        Lista_Datos[27] = False
        Lista_Datos[24] = 0
        Lista_Datos[29] = False
        V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
        vtn_w.line_Codigo.setFocus()

    '''#############################################################################################################################################
                                                        FUNCIONES DE CARGA DE PRODUCTOS
    #############################################################################################################################################'''
    
    # Le debe llegar una lista con todos los datos de un producto, controla con la Lista_Datos[21] si ya había dicho producto, si está actualiza su cantidad, y sino lo 
        # agrega a la lista y a los listwidget
    def Carga_Prod(vtn_w, Lista_Datos, Lista):
        pos = -1

        # El código va a buscar en las listas a ver si no existe con anterioridad para únicamente sumar las unidades y subtotales, pero vamos a evitar las promos para que 
            # aparezcan tantos renglones como promos cargadas, y también vamos a evitar todos los productos que no se cargan por unidad como ser la carnicería que es por precio.
            # La posición 7 de la lista representa la Unidad de Medida.
        if Lista[7] == 1:

            # Vamos a buscar en la lista a ver si el producto no existe con anterioridad. Recordar ignorar los que son promos
            cont = 0
            for i in Lista_Datos[21]:
                if Lista[0] == i[0] and i[7] == "":
                    pos = cont
                    break
                cont += 1
        
        # Pos es >= 0 cuando se encontró cargado con anterioridad
        if pos >= 0:
            # Se editan los valores de las listas de datos y luego se refresca la lista

            # Necesitamos tener la posición del mismo producto pero ahora en la lista-venta-mostrada
            pos2 = 0
            cont = 0
            for i in Lista_Datos[22]:
                if i[0] == Lista_Datos[21][pos][5]:
                    pos2 = cont
                    break
                cont += 1

            Cantidad_i = 0
            Cantidad_s = ""
            Subtotal_f = 0.0
            Subtotal_s = ""

            if Lista_Datos[24] == 0:
                Lista_Datos[24] = 1

            # Actualización de las cantidades nuevas
            Cantidad_i = Lista_Datos[24] + Lista_Datos[21][pos][3]
            Cantidad_s = form.Formato_Unidades(Cantidad_i, 3)
            Lista_Datos[24] = 0
            V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
            Lista_Datos[21][pos][3] = Cantidad_i
            Lista_Datos[22][pos2][3] = Cantidad_s
            # Actualización de los subtotales
            Subtotal_f = Lista[18] * Cantidad_i
            Subtotal_s = form.Formato_Decimal(Subtotal_f, 2)
            Lista_Datos[21][pos][4] = Subtotal_f
            Lista_Datos[22][pos2][4] = Subtotal_s

            # Limpiamos y refrescamos las listas
            V_Ventas.Refresca_Listas(vtn_w, Lista_Datos)
            Lista_Datos[26] = True
            largo = len(Lista_Datos[22])
            maximo = largo - Lista_Datos[0] + 1
            vtn_w.verticalScrollBar.setValue(maximo)
            Lista_Datos[26] = False

            # Llamamos a la función que suma los subtotales
            V_Ventas.Suma_Venta(vtn_w, Lista_Datos)
            V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
        else:
            # CUANDO SE VA A CARGAR UN PRODUCTO NUEVO
            Pcio_unit_f = Lista[18]
            Cantidad_i = 1
            Subtotal_f = Lista[18]

            Numero_s = str(len(Lista_Datos[22]) + 1)
            Concepto_s = Lista[4] + " " + Lista[5] + " " + Lista[6]
            Pcio_unit_s = form.Formato_Unidades(Pcio_unit_f, 3)
            Cantidad_s = "1"
            Subtotal_s = ""

            if Lista_Datos[24] > 0:
                Cantidad_s = form.Formato_Unidades(Lista_Datos[24], 3)
                Cantidad_i = Lista_Datos[24]
                Lista_Datos[24] = 0
                V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)

                Subtotal_f = Subtotal_f * Cantidad_i
                Subtotal_s = form.Formato_Decimal(Subtotal_f, 2)
            else:
                Subtotal_s = form.Formato_Decimal(Subtotal_f,2)
            
            # Agregamos los datos en las listas
            Lista_Datos[21].append([Lista[0], Concepto_s, Pcio_unit_f, Cantidad_i, Subtotal_f, Numero_s, Lista[20], ""])
            Lista_Datos[22].append([Numero_s, Concepto_s, Pcio_unit_s, Cantidad_s, Subtotal_s])

            # Cargamos en los listW el producto
            V_Ventas.Actualiza_Ultimo_ListW(vtn_w, Lista_Datos)

            # Llamamos a la función que suma los subtotales
            V_Ventas.Suma_Venta(vtn_w, Lista_Datos)
            V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
    
    # A ésta función se le entregan los datos de la promo y carga la promo completa tanto en la lista en pantalla como en las listas para las ventas
    def Carga_Prod_Promo1(vtn_w, Lista_Datos, Cod_Promo, Nomb_Promo, Costo_Total, Lista_Cod, Lista_Cant, Lista_Precio):
        # Datos para los ListWidgets
        Numero_s = str(len(Lista_Datos[22]) + 1)

        # Guardamos cada uno de los productos por separado en la lista de Venta Real
        Tope = len(Lista_Cod)
        sumado = 0.0
        aux = 0.0
        for i in range(Tope):
            existe, Lista_Datos_bd, conexion = mdb_p.Dev_Info_Producto(Lista_Cod[i])
            # Luego de hacer un llamado a las bases de datos, informamos cómo resultó la conexión con el mensaje superior en ventana
            V_Ventas.Mensaje_De_Conexion(vtn_w, conexion)
            
            Concepto_s = "PROMO: " + Lista_Datos_bd[4] + " " + Lista_Datos_bd[5] + " " + Lista_Datos_bd[6]
            if i == Tope - 1:
                aux = Costo_Total - sumado
            else:
                aux = form.Redondear_float(Lista_Precio[i] * Lista_Cant[i],2)
            Lista_Datos[21].append([Lista_Datos[0], Concepto_s, Lista_Precio[i], Lista_Cant[i], aux, Numero_s, Lista_Datos[20], Cod_Promo])

        # Guardamos los valores de la lista en ventana
        suma = 0
        for i in Lista_Cant:
            suma += i
        Lista_Datos[22].append([Numero_s, Nomb_Promo, form.Formato_Decimal(Costo_Total,2), str(suma),form.Formato_Decimal(Costo_Total,2)])
        
        # Cargamos en los listW el producto
        V_Ventas.Actualiza_Ultimo_ListW(vtn_w, Lista_Datos)

        # Siempre el último paso de las promos, son los que desactivan el sistema de promo
        Lista_Datos[29] = False

        # Llamamos a la función que suma los subtotales
        V_Ventas.Suma_Venta(vtn_w, Lista_Datos)
        V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
    
    '''#############################################################################################################################################
                                                        FUNCIONES DEDICADAS A LAS PROMOS
    #############################################################################################################################################'''

    # Controla si el código cargado o el producto y cantidades cargadas pertenecen o no a una promo
    def Detecta_Promo(vtn_w, Lista_Datos, encontrado, Codigo):

        # ATENCIÓN: Cuando se carga el código de una promo se sobreentiende que es lo que quieren y entonces directamente vamos a cargar la promo.
            # Pero cuando detectamos que un producto forma parte de una promo, el cliente puede o no querer la promo, por ello es que vamos a consultar antes de cargarla.

        # Cuando el producto no existe, entonces puede ser un código de promo
        if encontrado == 0:
            existe, lista = mdbprom.Busca_Cod_Promo("Promos", "Codigo", Codigo)
            # True: Existe la promo
            if existe == 1:
                
                # Cuando la promo es simple, un producto con diversas cantidades
                if lista[4] == 1:
                    V_Ventas.Acepta_Promo_Simple(vtn_w, Lista_Datos, lista)

                # Cuando la promo es compleja
                elif lista[4] == 2:
                    V_Ventas.Acepta_Promo_Compleja(vtn_w, Lista_Datos, lista)

                return True
        
        elif encontrado == 1:
            # Es cuando un Producto forma parte de una promo indicado en su columna en la DB
            if Lista_Datos[23][27] != "":
                largo = len(Lista_Datos[23][27])
                cod = Lista_Datos[23][27][0:(largo - 1)]
                existe, lista = mdbprom.Busca_Cod_Promo("Promos", "Codigo", cod)
                vtn_w.label_Msj.setText("DESEA CARGAR LA PROMO: {}?".format(lista[2]))
                vtn_w.label_Msj.setStyleSheet('background-color: rgb({},{},{});'.format(Lista_Datos[15], Lista_Datos[16], Lista_Datos[17]))
                Lista_Datos[29] = True
                V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
                return True
        
        return False

    # Se ejecuta cuando sabemos que el cliente quiere comprar la promo, porque por ej pudo haber comprado un producto pero no quiere llevarse los 3 que componen la promo,
        # en este caso preparamos los datos necesarios para cargar dicha promo, y luego llamamos a la función que carga la promo.
    def Acepta_Promo_Simple(vtn_w, Lista_Datos, Lista_Promo):
        Prod_de_Promo = Lista_Promo[5]
        nomb = "PROMO: " + Lista_Promo[2]
        costo = Lista_Promo[15]

        # En la db hay un campo de texto con el producto, precio y cantidad, vamos a extraer de ahí esos datos
            # Nos llegan 3 listas cuyo nombre nos indica por producto sus datos
        lista_Codi, lista_Cant, lista_Pcio = mi_func.Dev_Info_Promo_1(Prod_de_Promo)

        # Cargamos la promo en las ventas(lista[15]: Monto total de la promo. lista_promo[1]: Cod de la promo)
        V_Ventas.Carga_Prod_Promo1(vtn_w, Lista_Datos, Lista_Promo[1], nomb, costo, lista_Codi, lista_Cant, lista_Pcio)

    # Su función es cargar los códigos de los productos que componen la promo, una vez que sabemos que el cliente va a adquirir la promo, y actualizar los datos de los listw.
    # El parametro Codigo, viene con el codigo del primer producto que se haya pasado por el scaner.
    def Acepta_Promo_Compleja(vtn_w, Lista_Datos, Lista_de_Promo, Codigo = "0"):
        # Obtenemos la cantidad de productos que tiene que tener la promo, los códigos y sus precios dentro de la promo
        cant = 0
        precio = 0.0
        lista_codigos = []
        cant, precio, lista_codigos = mi_func.Dev_Info_Promo_2_Codigos(Lista_de_Promo[5])

        # Datos para los ListWidgets
        Numero_s = str(len(Lista_Datos[22]) + 1)
        Concepto_s = "PROMO >>> " + Lista_de_Promo[2]
        P_Unitario_s = form.Formato_Decimal(precio, 2)
        Cantidad_s = form.Formato_Unidades(cant, 3)
        Subtotal_s = form.Formato_Decimal(Lista_de_Promo[15], 2)
        # Agregamos a la lista que contiene las ventas el ID, Nro(en los listwidget), Pcio Costo de la promo float, Cant, costo de nuevo, T_F, Pcio de compra.
        # No hay problema si se cancela la promo en algún momento, xq se llama a la función de Eliminar, que se encarga de eliminar el último ítem de la ventana mostrada y 
        # luego busca en la lista_venta-real el nro de guía, si no hay ninguno no pasa nada, si hay los elimina.
        Lista_Datos[22].append([Numero_s, Concepto_s, P_Unitario_s, Cantidad_s, Subtotal_s])

        if Codigo != "0":
            listilla = []
            encontrado, listilla, conexion = mdb_p.Dev_Info_Producto(Codigo)
            # Luego de hacer un llamado a las bases de datos, informamos cómo resultó la conexión con el mensaje superior en ventana
            V_Ventas.Mensaje_De_Conexion(vtn_w, conexion)
            Concepto_s = "PROMO >>> {} {} {}".format(listilla[4], listilla[5], listilla[6])
            Lista_Datos[21].append([listilla[0], Concepto_s, precio, 1, precio, Numero_s, listilla[20], Lista_de_Promo[1]])

            # Cargamos la lista necesaria para la continuación de la promo
            Lista_Datos[30] = []
            Lista_Datos[30].append(1)
            Lista_Datos[30].append(cant)
            Lista_Datos[30].append(lista_codigos)
            Lista_Datos[30].append(precio)
            Lista_Datos[30].append(Lista_de_Promo)
            Lista_Datos[30].append(precio)
            Lista_Datos[30].append(Numero_s)
        else:
            # Cargamos la lista necesaria para la continuación de la promo
            Lista_Datos[30] = []
            Lista_Datos[30].append(0)
            Lista_Datos[30].append(cant)
            Lista_Datos[30].append(lista_codigos)
            Lista_Datos[30].append(0.0)
            Lista_Datos[30].append(Lista_de_Promo)
            Lista_Datos[30].append(precio)
            Lista_Datos[30].append(Numero_s)

        V_Ventas.Config_Ingreso_Promo(vtn_w, Lista_Datos)

    '''#############################################################################################################################################
                                                            FUNCIONES DE WIDGETS
    #############################################################################################################################################'''

    # ScrollBar
    def Change_ScrollBar(vtn_w, Lista_Datos):
        largo = len(Lista_Datos[22])
        if largo > Lista_Datos[0]:
            valor = vtn_w.verticalScrollBar.value()

    # Hace que al hacer clic en una posición de una lista, se seleccionen las demás simulando que todas forman parte de un mismo renglón. Así tmb si se llama a ésta función
        # sin valor del parámetro Origen, se termina deseleccionando las listas
    def Seleccion_Listas(vtn_w, Origen = 0):
        pos = -1
        if Origen == 1:
            pos = vtn_w.listWidget_2.currentRow()
        elif Origen == 2:
            pos = vtn_w.listWidget_3.currentRow()
        elif Origen == 3:
            pos = vtn_w.listWidget_4.currentRow()
        elif Origen == 4:
            pos = vtn_w.listWidget_5.currentRow()
        elif Origen == 5:
            pos = vtn_w.listWidget_6.currentRow()
        
        vtn_w.listWidget_2.setCurrentRow(pos)
        vtn_w.listWidget_3.setCurrentRow(pos)
        vtn_w.listWidget_4.setCurrentRow(pos)
        vtn_w.listWidget_5.setCurrentRow(pos)
        vtn_w.listWidget_6.setCurrentRow(pos)

    # Evento Change del line. Permite todo tipo de letras, números y signos, y cuando hay 1 o 2 caracteres analiza si es un comando especial.
    def Change_line_Cod(vtn, vtn_w, Lista_Datos):
        if Lista_Datos[27] == False:
            texto1 = vtn_w.line_Codigo.text()
            if "/" in texto1 or "$" in texto1:
                V_Ventas.Event_press_barra(vtn_w, Lista_Datos)
                return

            largo = len(texto1)
            if largo == 1:
                V_Ventas.Comandos_Especiales_1(vtn_w, Lista_Datos, texto1)
            elif largo == 2:
                V_Ventas.Comandos_especiales_2(vtn, vtn_w, Lista_Datos, texto1)

    # Se ejecuta con Enter dentro del line de Buscar Códigos
        # Pasos:
        # Controlamos que haya algo escrito en el line
        # Ejecutamos los comandos especiales
        # Controlamos si es o no una promo
        # Cargamos los datos del producto
        # Ofrecemos crear un producto nuevo
    def Return_line_Cod(vtn, vtn_w, Lista_Datos):

        # Estamos teniendo problemas con productos que cierran el programa, por esto es que tanto ésta función como las que están dentro, van a contener éste try
        try:
            # Si el Enter que llama a ésta función fue el que se ejecuta después de haber cargado el signo pesos con el lector, entonces ignoramos
            if Lista_Datos[1] == 1:
                Lista_Datos[1] = 0
                return

            # Si no hay nada escrito, llevamos el foco al line para ingresar el monto con el que paga el cliente
            if vtn_w.line_Codigo.text() == "":
                # La acción de apretar Enter con el Line vacío cuando se está esperando una promo, equivale a: +80+
                if Lista_Datos[29] == True:
                    V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
                    Lista_Datos[29] = False                          
                    V_Ventas.Carga_Prod(vtn_w, Lista_Datos, Lista_Datos[23])
                vtn_w.line_Monto.setFocus()
                return

            # Capturamos el texto escrito en el line
            texto = vtn_w.line_Codigo.text()

            # Si son comandos especiales, salimos de la función
            if V_Ventas.Comandos_Especiales_Enter(vtn, vtn_w, Lista_Datos, texto) == True:
                return

            # La función nos devuelve en la primer variable (0= no existe; 1= Existe y es código normal; 2= Es codXbulto; 3= Producto Desactivado), de ser > 0, entonces en la lista están todos sus datos
            encontrado, Lista_Datos[23], conexion = mdb_p.Dev_Info_Producto(texto)
            # Luego de hacer un llamado a las bases de datos, informamos cómo resultó la conexión con el mensaje superior en ventana
            V_Ventas.Mensaje_De_Conexion(vtn_w, conexion)

            # Si el producto está desactivado no hacemos nada
            if encontrado == 3:
                QMessageBox.question(vtn, "Error", "Producto DESACTIVADO.", QMessageBox.Ok)
                V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
                return
            
            # Si es una Promo, salimos de la función
            if V_Ventas.Detecta_Promo(vtn_w, Lista_Datos, encontrado, texto) == True:
                return

            # Cuando el producto no existe
            if encontrado == 0:
                Rta = QMessageBox.question(vtn, "Desconocido", "El código no existe, ¿desea crear un PRODUCTO NUEVO?", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
                if Rta == QMessageBox.Ok:
                    Lista_Datos[28] = texto
                else:
                    V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)

            # El producto existe y tiene valores normales
            elif encontrado == 1:

                # Ahora controlamos en el modo en que se vende, por ejemplo, cuando se vende por Kg, mostramos una pantalla para que el usuario cargue el kg luego del código.
                # Venta por unidad
                if Lista_Datos[23][7] == 1:
                    V_Ventas.Carga_Prod(vtn_w, Lista_Datos, Lista_Datos[23])
                    return
                else:
                    V_Ventas.Config_Ingreso_Precio(vtn_w, Lista_Datos, Lista_Datos[23][7])

            # El producto exise pero el código es un cod x bulto
            elif encontrado == 2:
                Lista_Datos[24] = Lista_Datos[23][3]
                V_Ventas.Carga_Prod(vtn_w, Lista_Datos, Lista_Datos[23])

            Lista_Datos[24] = 0
            V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)

        except:
            QMessageBox.question(vtn, "ERROR", "Anote el PRODUCTO para tener registro del error.", QMessageBox.Ok)
            V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)

    # Evento Change del line que se encuentra en las opciones del GroupBox de precios. Permite números y (, y .) pero los traduce a una única coma.
    def Change_line_GB_Precio(vtn_w):
        vtn_w.line_Ingresos.setText(form.Line_Num_Coma_(vtn_w.line_Ingresos.text()))

    # Evento Enter en el line que está dentro del groupBox que carga precios, litros, etc...
    def Return_line_GB_Precio(vtn, vtn_w, Lista_Datos):
        
        texto = vtn_w.line_Ingresos.text()
        if Lista_Datos[31] != 6:
            if len(texto) > 0:
                # Capturamos el texto escrito en el line
                Lista_Datos[24] = form.Str_Float(texto)
                V_Ventas.Carga_Prod(vtn_w, Lista_Datos, Lista_Datos[23])
                V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
                V_Ventas.Config_Ingreso_Precio(vtn_w, Lista_Datos)
                V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
            else:
                V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
                V_Ventas.Config_Ingreso_Precio(vtn_w, Lista_Datos)
                V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
        else:
            if len(texto) > 0:
                V_Ventas.Elimina_Item(vtn, vtn_w, Lista_Datos)
                try:
                    mdb_p.Act_Valor_Num(mi_vars.BASE_DATOS_PPAL, "Stock", "PcioVta", form.Str_Float(texto), "ID", Lista_Datos[23][0])
                    vtn_w.line_Codigo.setText(Lista_Datos[23][1])
                    V_Ventas.Return_line_Cod(vtn, vtn_w, Lista_Datos)
                    V_Ventas.Mensaje_De_Conexion(vtn_w, 2)
                except:
                    try:
                        mdb_p.Act_Valor_Num(mi_vars.BASE_DATOS_SEC, "Stock", "PcioVta", form.Str_Float(texto), "ID", Lista_Datos[23][0])
                        vtn_w.line_Codigo.setText(Lista_Datos[23][1])
                        V_Ventas.Return_line_Cod(vtn, vtn_w, Lista_Datos)
                        V_Ventas.Mensaje_De_Conexion(vtn_w, 1)
                        
                    except:
                        V_Ventas.Mensaje_De_Conexion(vtn_w, 0)
                V_Ventas.Config_Ingreso_Precio(vtn_w, Lista_Datos)
                V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
            else:
                Lista_Datos[31]= 0
                V_Ventas.Config_Ingreso_Precio(vtn_w, Lista_Datos)
                V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)

    # Evento Enter en el line dentro del groupBox de Promos
    def Return_line_Promo(vtn, vtn_w, Lista_Datos):
        texto = vtn_w.line_Ingreso_Promo.text()

        if len(texto) > 0:

            # Si es un código de la promo que se está cargando
            if texto in Lista_Datos[30][2]:

                # True: Último producto de la promo. False: Lo contrario.
                if Lista_Datos[30][0] == Lista_Datos[30][1] - 1:

                    # Si es el último producto, guardamos en la variable de Precio, el monto de lo que debe valer el último producto cargado.
                    Lista_Datos[30][5] = Lista_Datos[30][4][15] - Lista_Datos[30][3]

                else:
                    # Acumulamos la suma de lo que se viene cargando
                    Lista_Datos[30][3] += Lista_Datos[30][5]

                listilla = []
                encontrado, listilla, conexion = mdb_p.Dev_Info_Producto(texto)
                # Luego de hacer un llamado a las bases de datos, informamos cómo resultó la conexión con el mensaje superior en ventana
                V_Ventas.Mensaje_De_Conexion(vtn_w, conexion)
                Concepto_s = "PROMO >>> {} {} {}".format(listilla[4], listilla[5], listilla[6])
                Lista_Datos[21].append([listilla[0], Concepto_s, Lista_Datos[30][5], 1, Lista_Datos[30][5], Lista_Datos[30][6], listilla[20], Lista_Datos[30][4][1]])
                Lista_Datos[30][0] += 1

                # Control: Si se cargó el último de la promo tenemos que devolver la pantalla.
                if Lista_Datos[30][0] == Lista_Datos[30][1]:
                    V_Ventas.Config_Ingreso_Promo(vtn_w, Lista_Datos, False)
                    # Cargamos en los listW el producto
                    V_Ventas.Actualiza_Ultimo_ListW(vtn_w, Lista_Datos)
                    # Llamamos a la función que suma los subtotales
                    V_Ventas.Refresca_Listas(vtn_w, Lista_Datos)
                    V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
                else:
                    vtn_w.groupBox_Promos.setTitle("Ingrese Promo: {} de {}".format(str(Lista_Datos[30][0]), str(int(Lista_Datos[30][1]))))
                    vtn_w.line_Ingreso_Promo.clear()
                    vtn_w.line_Ingreso_Promo.setFocus()
            else:
                QMessageBox.question(vtn, "ERROR", "El código cargado no pertenece a ésta promo.", QMessageBox.Ok)
                vtn_w.line_Ingreso_Promo.clear()
                vtn_w.line_Ingreso_Promo.setFocus()
        else:
            V_Ventas.Cancela_Promo(vtn, vtn_w, Lista_Datos)

    # Change Line Monto
    def Change_line_Monto(vtn_w, Lista_Datos):
        texto = vtn_w.line_Monto.text()

        if "/" in texto or mi_vars.BTN_IGUAL in texto or "*" in texto or "+" in texto or "$" in texto:
            vtn_w.line_Monto.setText("")
            V_Ventas.Event_press_barra(vtn_w, Lista_Datos)
            return
        
        texto = form.Line_Num_Coma_(texto)
        vtn_w.line_Monto.setText(texto)
        if texto != "":
            vtn_w.label_Vuelto.setText(form.Formato_Decimal(form.Str_Float(vtn_w.line_Monto.text()) - V_Ventas.Aux_Suma_Venta(vtn_w, Lista_Datos), 2))

    # Al presionar Enter
    def Return_line_Monto(vtn_w, Lista_Datos):
        Lista_Datos[2] = 1
        vtn_w.push_Cargar.setFocus()

    '''#############################################################################################################################################
                                                            FUNCIONES PARA WIDGETS
    #############################################################################################################################################'''

    # Elimina un item de las listas. Si hay algún producto seleccionado lo elimina y quita toda selección, de lo contrario elimina al último ítem. Si viene por parámetro la 
        # ubicación de un ítem lo borra.
        # Nota: el valor de ubi será 1 para la primer posición de la lista y no 0, y tmb recordar que si la lista supera lo mostrado en pantalla, las posiciones no son las
            # mismas en pantalla con la Lista_Datos[22], ya que en pantalla se muestra lo que se puede ver y no todos los productos totales.
    def Elimina_Item(vtn, vtn_w, Lista_Datos, ubi = 0):
        largo = len(Lista_Datos[22])
        if largo > 0:
            # Dejamos por defecto que no se debe quitar selección ya que sólo sucede en 1 de cada 3 tipos de casos en que se llama a ésta función
            quita_sel = False
            # True: Cuando viene con una ubicación indicada. False: Sin ubicación
            if ubi > 0:
                if ubi <= largo:
                    pos = ubi
                else:
                    QMessageBox.question(vtn, "Error", "Error al indicar ubicación del PRODUCTO que desea ELIMINAR.", QMessageBox.Ok)
                    return
            else:
                try:
                    valor = "a"
                    valor = vtn_w.listWidget_2.selectedItems()[0].text()
                    pos = int(valor)
                    quita_sel = True
                except:
                    pos = largo
            
            # Eliminamos
            Lista_Datos[22].pop(pos-1)
            texto = str(pos)
            bucle = True
            cont = 0
            while bucle:
                if cont == len(Lista_Datos[21]):
                    bucle = False
                else:
                    if Lista_Datos[21][cont][5] == texto:
                        Lista_Datos[21].pop(cont)
                        cont = 0
                    else:
                        cont += 1

            # Si se eliminó un producto que estaba seleccionado en pantalla, se quita dicha selección previo a la eliminación, para que no quede algo seleccionado luego
            if quita_sel == True:
                V_Ventas.Seleccion_Listas(vtn_w)
            
            # Se limpian y se refrescan todas las listas
            V_Ventas.Refresca_Listas(vtn_w, Lista_Datos)
            Lista_Datos[26] = True
            maximo = largo - Lista_Datos[0] + 1
            if maximo > 1:
                vtn_w.verticalScrollBar.setValue(maximo)
            else:
                vtn_w.verticalScrollBar.setMinimum(0)
                vtn_w.verticalScrollBar.setValue(0)
                vtn_w.verticalScrollBar.setMaximum(0)
            Lista_Datos[26] = False

    # Cuando se agrega algún producto nuevo ésta función lo agrega los listwidget en pantalla según los datos que están en la Lista_Datos[22]
    # No modifica valores importantes, sino variables del scrollbar
    def Actualiza_Ultimo_ListW(vtn_w, Lista_Datos):

        largo = len(Lista_Datos[22])

        if largo == 0:
            return

        if largo > Lista_Datos[0]:
            Lista_Datos[26] = True
            valor = vtn_w.verticalScrollBar.value()
            if valor == 0:
                vtn_w.verticalScrollBar.setMinimum(1)
            maximo = largo - Lista_Datos[0] + 1
            vtn_w.verticalScrollBar.setMaximum(maximo)
            # Al asignar éste valor a la barra, se llama automáticamente a la función que actualiza las listas
            Lista_Datos[26] = False
            vtn_w.verticalScrollBar.setValue(maximo)

        else:
            vtn_w.listWidget_2.addItem(Lista_Datos[22][-1][0])
            vtn_w.listWidget_3.addItem(Lista_Datos[22][-1][1])
            vtn_w.listWidget_4.addItem(Lista_Datos[22][-1][2])
            vtn_w.listWidget_5.addItem(Lista_Datos[22][-1][3])
            vtn_w.listWidget_6.addItem(Lista_Datos[22][-1][4])

    # Limpia y refresca los datos de todas las listas en pantalla y refresca el índice que mostramos en el listWidget1, ya que si por ej se ha borrado un item estos cambian.
    def Refresca_Listas(vtn_w, Lista_Datos, scrol = 0):

        # Esta variable es True sólo cuando se asigna por primera vez el valor del scrollbar, pero llama a ésta función y no debe ejecutarse xq luego se vuelve a llamar a ésta
            # misma función pero con un nuevo valor
        if Lista_Datos[26] == False:

            # Limpiamos todas las listas
            vtn_w.listWidget_2.clear()
            vtn_w.listWidget_3.clear()
            vtn_w.listWidget_4.clear()
            vtn_w.listWidget_5.clear()
            vtn_w.listWidget_6.clear()

            largo = len(Lista_Datos[22])
            # ReEnumeramos los valores de índice que se cargan en la primer lista, tener en cuenta que debe permanecer en concordancia con la Guía en la lista de venta real.
            for i in range(largo):
                Nro_Nuevo = str(i + 1)
                Nro_Viejo = Lista_Datos[22][i][0]
                for n in Lista_Datos[21]:
                    if n[5] == Nro_Viejo:
                        n[5] = Nro_Nuevo
                Lista_Datos[22][i][0] = Nro_Nuevo

            # Si los ítems entran en pantalla, los cargamos de manera normal, de lo contrario, cargamos los últimos ítems
            if largo > Lista_Datos[0]:

                # Ahora miramos si el valor máximo de la scrollbar es correcto, porque si se han eliminado productos, el largo debe ajustarse
                largoLW = vtn_w.verticalScrollBar.maximum()
                if (largoLW - 1) > (largo - Lista_Datos[0]):
                    if vtn_w.verticalScrollBar.value() == largoLW:
                        Lista_Datos[26] = True
                        maximo = largo - Lista_Datos[0] + 1
                        vtn_w.verticalScrollBar.setValue(maximo)
                        vtn_w.verticalScrollBar.setMaximum(maximo)
                        scrol = maximo
                        Lista_Datos[26] = False                        

                if scrol == 0:
                    for i in range(Lista_Datos[0]):
                        vtn_w.listWidget_2.addItem(Lista_Datos[22][-(Lista_Datos[0] - i)][0])
                        vtn_w.listWidget_3.addItem(Lista_Datos[22][-(Lista_Datos[0] - i)][1])
                        vtn_w.listWidget_4.addItem(Lista_Datos[22][-(Lista_Datos[0] - i)][2])
                        vtn_w.listWidget_5.addItem(Lista_Datos[22][-(Lista_Datos[0] - i)][3])
                        vtn_w.listWidget_6.addItem(Lista_Datos[22][-(Lista_Datos[0] - i)][4])
                else:
                    for i in range((scrol - 1), (scrol + Lista_Datos[0] - 1)):
                        vtn_w.listWidget_2.addItem(Lista_Datos[22][i][0])
                        vtn_w.listWidget_3.addItem(Lista_Datos[22][i][1])
                        vtn_w.listWidget_4.addItem(Lista_Datos[22][i][2])
                        vtn_w.listWidget_5.addItem(Lista_Datos[22][i][3])
                        vtn_w.listWidget_6.addItem(Lista_Datos[22][i][4])
            else:
                # Si está habilitada la barra hay que deshabilitarla
                if vtn_w.verticalScrollBar.value() > 0:
                    Lista_Datos[26] = True
                    vtn_w.verticalScrollBar.setMinimum(0)
                    vtn_w.verticalScrollBar.setValue(0)
                    vtn_w.verticalScrollBar.setMaximum(0)
                    Lista_Datos[26] = False
                for sub in Lista_Datos[22]:
                    vtn_w.listWidget_2.addItem(sub[0])
                    vtn_w.listWidget_3.addItem(sub[1])
                    vtn_w.listWidget_4.addItem(sub[2])
                    vtn_w.listWidget_5.addItem(sub[3])
                    vtn_w.listWidget_6.addItem(sub[4])
            V_Ventas.Reinicio_Vtn_Parcial(vtn_w, Lista_Datos)

    # Función que reestablece lo que se haya cargado en el caso de que se haya cancelado una promo del tipo 2 en medio de la carga.
    def Cancela_Promo(vtn, vtn_w, Lista_Datos):
        V_Ventas.Elimina_Item(vtn, vtn_w, Lista_Datos)
        V_Ventas.Config_Ingreso_Promo(vtn_w, Lista_Datos, False)

    '''#############################################################################################################################################
                                                            FUNCIONES GENERALES
    #############################################################################################################################################'''

    # Suma los subtotales y coloca el total en el label. Al mismo tiempo devuelve el valor total en formato float si es que lo requieren
    def Suma_Venta(vtn_w, Lista_Datos):
        aux = V_Ventas.Aux_Suma_Venta(vtn_w, Lista_Datos)
        if len(Lista_Datos[21]) > 0:
            vtn_w.label_Total.setText(form.Formato_Decimal(aux, 2))
        else:
            vtn_w.label_Total.setText("0,00")
        return aux

    # Calcula el total y devuelve un float
    def Aux_Suma_Venta(vtn_w, Lista_Datos):
        aux = 0.0
        if len(Lista_Datos[21]) > 0:
            for pos in Lista_Datos[21]:
                aux += pos[4]
        return aux

    # Cuando se desea resetear toda la ventana pero sin modificar los datos de la lista
        # Refresco: Es por si le agregamos o no el refresco de la lista de datos
    def Reinicio_Vtn_Parcial(vtn_w, Lista_Datos, Refresco=False):
        if Refresco == True:
            V_Ventas.Refresca_Listas(vtn_w, Lista_Datos)
        else:
            V_Ventas.Suma_Venta(vtn_w, Lista_Datos)
        vtn_w.line_Codigo.setText("")
        vtn_w.line_Codigo.setFocus()

    # Trabaja sobre el line_codigo, limpiándolo y luego llevando el foco sobre él. Coloqué éstas 4 líneas en una función porque se ejecuta muchísimas veces en el programa.
    def Limpia_Foco_Cod(vtn_w, Lista_Datos):
        Lista_Datos[27] = True
        vtn_w.line_Codigo.setText("")
        vtn_w.line_Codigo.setFocus()
        Lista_Datos[27] = False
