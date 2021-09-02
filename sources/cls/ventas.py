'''Contiene todo lo relativo a la ventana de Ventas.'''

# (*1) = Para que un producto esté en condiciones de ser vendido, debe cumplir 3 requisitos:
    # Ser un producto que se vende por unidad.
    # Luego de conocer su estado (Desactivado - Incompleto - Completo), controlamos la configuración del programa para ver si coincide con la config del prod.
    # Y luego de controlar su stock, verificar si el programa permite su venta cuando no tiene.

from sources.mod.mdbegen import DB_Cajas_Totales_Cajas
import threading
from App_Caja import *
import time
#from sources.cls.Functions import *

import sources.mod.mdbprod as mdb_p
import sources.mod.mdbprom as mdbprom
import sources.mod.form as form
import sources.mod.vars as mi_vars
import sources.mod.func as mi_func
from sources.mod.renglones import *

'''
    HACER URGENTE:
    * Controlar el funcionamiento normal de la venta completa (promos - productos especiales)
    * Controlar la eliminación de promos y productos especiales
    * Controlar el efecto en las db.
    * Revisar todas las interacciones con las bases de datos enfocado en el nuevo método de control
    * Configurar el funcionamiento por red
    * Controlar el ajuste de la ventana cuando se crean y eliminan productos
    * Inicio de sesión para modificación de precios (vincular con activdad en red)


    * Controlar las funciones actuales que quedaron sin ver, las que están expandidas o tienen comentarios verdes


    CORREGIR
    Se achicharran los renglones cuando está minimizado
    Al cargar promo compleja, aparecieron los dos groupbox y no tenían foco
    Se cerró cuando cargué el útlimo producto
    

    SIN URGENCIA
    La redimensión de la ventana cuando ya contiene renglones
    Forma de brindar los datos de cantidades y precio unitario




    FORMA DE TRABAJO
    
        PRODUCTOS QUE PUEDEN VENDERSE (*1)
            Si vemos los datos que representa la variable de la pos [32] podemos ver que en el programa se puede seleccionar con qué tipo deproductos se pueden trabajar, por 
            ejemplo, se pueden usar productos que estén DESACTIVADOS. La idea ppal es que yo pueda ir incorporando desde casa todos los productos que pueda pero indicar que 
            están desactivados y probar el programa a pesar de que quizás no tenga productos que estén a la venta en el local realmente. Luego antes de entregarlo se cambia la 
            configuración y se evitan los productos desactivados. De esta manera incorporo a la lista productos que quizás no esté trabajando actualmente el vendedor pero si 
            lo incorpora a futuro puede resultarle útil. Para ello una función se encargará de analizar los datos y confirmar si se pueden o no vender dichos productos.

    Si un usuario carga un código que no existe, no está funcionando la posibilidad de crearlo. buscar línea: Lista_Datos[28] = texto


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
    
    # Lista que contiene 2 datos por cada producto que se carga, primero la guía en formato texto y luego el objeto del renglón.
    lista_renglones = []
    '''#############################################################################################################################################
                                                            FUNCIONES DE VENTANA
    #############################################################################################################################################'''

    def Mostrar(vtn_w):
        '''Muestra la Page correspondiente y por ahora sólo hace foco en el line_cod'''
        vtn_w.stackedWidget.setCurrentWidget(vtn_w.page_Ventas)
        vtn_w.line_Codigo.setFocus()

    def Limpia_Ventana(vtn_w, Lista_Datos):
        '''Limpia todos los datos de una venta, incluyendo variables y widgets.'''
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

        # Limpiamos las variables
        V_Ventas.lista_renglones = []
        Lista_Datos[0] = 0
        Lista_Datos[1] = 0
        Lista_Datos[21] = []
        Lista_Datos[22] = []
        Lista_Datos[23] = []
        Lista_Datos[24] = 0
        Lista_Datos[28] = ""
        Lista_Datos[29] = False
        Lista_Datos[30] = []
        Lista_Datos[31] = 0
        Lista_Datos[36] = 0
        V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
        vtn_w.line_Codigo.setFocus()

    def Config_Mensaje(vtn_w, Lista_Datos, Mensajes = 0):
        print("INICIO: Config_Mensaje 154")

        '''Configura la casilla de mensajes inferior con el texto y color de fondo, con 3 parámetros donde el último >>> "Mensajes = 0" indica que se restaura la ventana y los demás mensajes contienen su texto en ésta función.'''

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

        print("FIN: COnfig msj 203")

    def Config_Ingreso_Precio(vtn_w, Lista_Datos, Tipo = 0):
        '''Configura y muestra el groupbox que simula ser ventana de ingreso de datos (Precio, Litros, Kg, etc). Tener en cuenta que con sólo llamar a la función indicando lo 
        que se va a hacer, ella se encarga de configurar todo lo relativo a las cargas de datos.'''
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
            vtn_w.stackedWidget.setCurrentWidget(vtn_w.page_Ventas)
            V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)

    def Config_Ingreso_Promo(vtn_w, Lista_Datos, Coloca = True):
        '''Configura y muestra la pagina para cargar los productos de una promo.'''
        # Parametros:
            # Coloca= True: Por defecto, configura la pantalla para colocar el mensaje.
            # Coloca= False: Devuelve el estado de la pantalla a la normalidad.
        if Coloca == True:
            vtn_w.groupBox_Promos.setVisible(True)
            vtn_w.groupBox_Ingresos.setEnabled(False)
            Lista_Datos[29] = True
            vtn_w.stackedWidget.setCurrentWidget(vtn_w.page_msjs)
            vtn_w.groupBox_Promos.setTitle("Ingrese Promo: {} de {}".format(str(Lista_Datos[30][0]), str(int(Lista_Datos[30][1]))))
            vtn_w.line_Ingreso_Promo.setFocus()
        else:
            vtn_w.line_Ingreso_Promo.clear()
            vtn_w.groupBox_Promos.setVisible(False)
            vtn_w.groupBox_Ingresos.setEnabled(True)
            Lista_Datos[29] = False
            vtn_w.stackedWidget.setCurrentWidget(vtn_w.page_Ventas)
            V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)

    def Mensaje_De_Conexion(vtn_w, msj):
        '''Configura el mensaje superior referido a la conexión. msj = int (0, 1, 2 o 3)'''
        # ROJO
        r = 255
        g = 0
        b = 0
        if msj == 0:
            vtn_w.label.setText("DESCONECTADO")
        elif msj == 1:
            vtn_w.label.setText("Trabajando en: LOCAL")
            r = 255
            g = 170
            b = 127
        elif msj == 2:
            vtn_w.label.setText("Conectado")
            r = 35
            g = 200
            b = 35
        elif msj == 3:
            vtn_w.label.setText("Esperando actividad...")
            r = 150
            g = 150
            b = 150
        vtn_w.frame.setStyleSheet("background-color: rgb({},{},{});".format(r,g,b))

    '''#############################################################################################################################################
                                                        COMANDOS ESPECIALES DE VENTANA
    #############################################################################################################################################'''

    def Comandos_Especiales_1(vtn_w, Lista_Datos, texto):
        '''Se llama siempre que hay un sólo caracter en el line_cod.'''
        if texto == "-":
            V_Ventas.Config_Mensaje(vtn_w, Lista_Datos, Mensajes = 3)

    def Comandos_especiales_2(vtn, vtn_w, Lista_Datos, texto):
        '''Se llama siempre que hay dos caracteres en el line_cod.'''
        # Elimina el último ítem
        if texto == "--":
            V_Ventas.Elimina_Item(vtn, vtn_w, Lista_Datos)

    def Comandos_Especiales_Enter(vtn, vtn_w, Lista_Datos, texto):
        '''Analiza si el texto que se ingresó en el line_cod es un comando especial, y de ser así lo ejecuta. Tener en cuenta que los comando especiales de 1 y 2 caracteres 
        son trabajados en Comandos_Especiales_1 y Comandos_especiales_2 respectivamente.'''
        # INFO SOBRE LOS CÓDIGOS:
            # Hay casos donde 2 códigos distintos hacen la misma tarea, por ejemplo responder con "SI" a preguntas como si quieren aceptar la promo se puede contestar con 
            # "CODSI" o con "+51+". El motivo es porque para usar el lector de códigos utilizo combinaciones de letras para evitar que en algún momento un código inventado por 
            # mí se cruce con un código de productos ya que esos son exclusivamente números. Por otro lado necesito crear un código a la par que haga lo mismo pero sin el 
            # lector, con el teclado numérico, porque si por ejemplo se arruina la hoja de códigos o por algún motivo el lector no puede leerlo, tienen que tener una 
            # alternativa reproducible con un poco de facilidad en el teclado numérico (+51+).
            # La razón por la cuál no genero un código para el lector igual al otro (+51+), es porque los códigos de barra que genero con CODE39, no se leen de igual forma en 
            # Windows y Linux, siendo que el único símbolo que entienden por igual ambos sistemas operativos es el signo $, el cuál no contiene ningún teclado numérico. Es 
            # decir, que si genero un código de barras que signifique "+51+", serviría sólo en Windows pero no en Linux. La única combinación que me sirve en ambos es $51$ 
            # pero es un código que no se puede reproducir en el teclado, y por ello es que tengo que hacer sí o sí 2 códigos para un mismo fin. Y ya que hago 2 códigos para 
            # lo mismo, hago algo simple para el teclado y algo más complejo pero práctico para le lector.
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
                            # Controlamos que haya un código normal de producto pero al mismo tiempo que no contenga uno de una promo.
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

                    elif aux == "-" or texto == "CODBO":
                        ''' Llama a eliminar productos. Recordar que exiten 2 formas.
                        1) Borrar el útlimo cargado, útil para cuando sólo queríamos saber el precio de algo. (-- / CODBO / presionando "Eliminar" sin selección)
                        2) Borrar uno en particular. (ejemplo: -3 borra la posición 3 en pantalla / seleccionando y luego presionar "Eliminar")
                        '''
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
                                        V_Ventas.Acepta_Promo_Simple(vtn, vtn_w, Lista_Datos, lista_Auxiliar)
                                    elif Tipo_Prom == 2:
                                        existe, lista_Auxiliar = mdbprom.Busca_Cod_Promo("Promos", "Codigo", ID_Promo)
                                        V_Ventas.Acepta_Promo_Compleja(vtn_w, Lista_Datos, lista_Auxiliar, Lista_Datos[23][1])

                                # Cuando el usuario indica NO
                                elif texto == "+80+" or texto == "CODNO":
                                    Lista_Datos[29] = False
                                    V_Ventas.Carga_Prod(vtn, vtn_w, Lista_Datos, Lista_Datos[23])

                        V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
                        return True
        except:
            QMessageBox.question(vtn, "ERROR", "Anote el PRODUCTO para tener registro del error.", QMessageBox.Ok)
        return False

    def Event_press_barra(vtn_w, Lista_Datos):
        '''Al precionar la / que está tanto en el teclado como por código, lo que vamos a hacer es limpiar el line_cod, dirigirle el foco y poner a cero cant_proxima.
        Esto va a ser que la /, sea un recurso casi en todo momento para limpiar esos requechos de datos que no se pueden cancelar y poder dirigir al line_cod el foco del
        programa en cualquier momento.'''
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
    
    def Carga_Prod(vtn, vtn_w, Lista_Datos, Lista):
        '''El primer paso para crear un nuevo renglón o actualizar datos existentes como cuando sumamos unidades a un producto ya cargado.'''
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
            # Actualizamos ambos datos pero en pantalla
            for i in V_Ventas.lista_renglones:
                if i[0] == Lista_Datos[22][pos2][0]:
                    i[1].Lista_Labels[3].setText(Cantidad_s)
                    i[1].Lista_Labels[4].setText(Subtotal_s)
                    break

            # Llamamos a la función que suma los subtotales
            V_Ventas.Suma_Venta(vtn_w, Lista_Datos)
            V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
        else:
            # CUANDO SE VA A CARGAR UN PRODUCTO NUEVO
            # Actualizamos el numero de guía
            Lista_Datos[36] += 1

            Pcio_unit_f = Lista[18]
            Cantidad_i = 1
            Subtotal_f = Lista[18]

            # Numero_s es la guía, que coincide el nombre del renglón, el renglón que se muestra en pantalla (Lista_Datos[22]) y la lista real de prod.(Lista_Datos[21])
            Numero_s = str(Lista_Datos[36])
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

            # Agregamos un renglón
            # Redimencionamos el frame que lo contiene y ajustamos el scroll si es necesario
            #threading.Thread(target=V_Ventas.Ajusta_Frame_Scroll, args=(vtn_w, Lista_Datos,)).start()
            threading.Thread(target=V_Ventas.Espera_renglon, args=(vtn, vtn_w, Lista_Datos, Lista_Datos[36], True,)).start()
            #V_Ventas.Ajusta_Frame_Scroll(vtn_w, Lista_Datos)
            V_Ventas.Crea_renglon(vtn, vtn_w, Lista_Datos)
            
            V_Ventas.Suma_Venta(vtn_w, Lista_Datos)
            V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
    
    def Carga_Prod_Promo1(vtn, vtn_w, Lista_Datos, Cod_Promo, Nomb_Promo, Costo_Total, Lista_Cod, Lista_Cant, Lista_Precio):
        '''A ésta función se le entregan los datos de la promo y carga la promo completa tanto en la lista en pantalla como en las listas para las ventas.'''
        # Número de Guía
        Lista_Datos[36] += 1
        Numero_s = str(Lista_Datos[36])

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
                aux = form.Redondear_float(Costo_Total - sumado,2)
            else:
                aux = form.Redondear_float(Lista_Precio[i] * Lista_Cant[i],2)
                sumado += aux
            Lista_Datos[21].append([Lista_Datos_bd[0], Concepto_s, Lista_Precio[i], Lista_Cant[i], aux, Numero_s, Lista_Datos[20], Cod_Promo])

        # Guardamos los valores de la lista en ventana
        suma = 0
        for i in Lista_Cant:
            suma += i
        Lista_Datos[22].append([Numero_s, Nomb_Promo, form.Formato_Decimal(Costo_Total,2), str(suma),form.Formato_Decimal(Costo_Total,2)])
        
        # Cargamos en los listW el producto
        # Redimencionamos el frame que lo contiene y ajustamos el scroll si es necesario
        #V_Ventas.Espera_renglon(vtn, vtn_w, Lista_Datos, Numero_s, True)
        V_Ventas.Ajusta_Frame_Scroll(vtn_w, Lista_Datos)
        V_Ventas.Crea_renglon(vtn, vtn_w, Lista_Datos)

        # Desactiva el sistema de promo
        Lista_Datos[29] = False

        # Llamamos a la función que suma los subtotales
        V_Ventas.Suma_Venta(vtn_w, Lista_Datos)
        V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
    
    def Crea_renglon(vtn, vtn_w, Lista_Datos):
        '''Función que crea un renglón en la lista de productos, sólo necesita ser llamada porque toma todos los valores de las variables existentes. Tener en cuenta que para 
        cuando es llamada la función, la Lista_Datos tanto en la pos [21] como en [22] ya deben estar actualizadas. Saber también que se encarga de asignar a cada label del 
        renglón un evento clic, haciendo parecer que es un botón entero.'''

        # Obtenemos el nombre que va a ser el número de guía ya que sin importar los cambios que hayan en pantalla, no van a repetirse en una misma venta los números de guía.
        nombre = str(Lista_Datos[36])
        # El color es para que cada renglón tenga distinto fondo de manera intercalada, se indica con 0 o 1
        color = 1
        largo = len(Lista_Datos[22])
        if largo % 2 == 0:
            color = 0
        # El ancho debe conocerlo la clase del renglón, así calcula el ancho de la columna "Concepto" en función al espacio que dejan libre las otras columnas.
        ancho = vtn_w.frame_labels.width()
        # Creamos el renglón
        Nro = str(len(Lista_Datos[22]))
        renglon = Lista_venta([Nro, Lista_Datos[22][-1][1], Lista_Datos[22][-1][2], Lista_Datos[22][-1][3], Lista_Datos[22][-1][4]], nombre, ancho, color)
        # Lo colocamos dentro del layout
        vtn_w.verticalLayout_5.addWidget(renglon, 0, QtCore.Qt.AlignTop)
        # Lo ubicamos y redimencionamos 
        renglon.setGeometry(0,Lista_Datos[34][1] * (largo - 1), ancho, Lista_Datos[34][1])
        # Lo colocamos dentro de una lista para su fácil uso
        V_Ventas.lista_renglones.append([nombre, renglon])

        # INTENTANDO CONFIGURAR EL SIGNAL
        V_Ventas.lista_renglones[-1][1].Lista_Labels[0].clicked.connect(lambda: V_Ventas.Color_seleccion(nombre, Lista_Datos))
        V_Ventas.lista_renglones[-1][1].Lista_Labels[1].clicked.connect(lambda: V_Ventas.Color_seleccion(nombre, Lista_Datos))
        V_Ventas.lista_renglones[-1][1].Lista_Labels[2].clicked.connect(lambda: V_Ventas.Color_seleccion(nombre, Lista_Datos))
        V_Ventas.lista_renglones[-1][1].Lista_Labels[3].clicked.connect(lambda: V_Ventas.Color_seleccion(nombre, Lista_Datos))
        V_Ventas.lista_renglones[-1][1].Lista_Labels[4].clicked.connect(lambda: V_Ventas.Color_seleccion(nombre, Lista_Datos))
    
    def Espera_renglon(vtn, vtn_w, Lista_Datos, guia, Aparicion):
        '''Espera que aparezca o desaparezca algún objeto(renglon) y luego actualiza las dimensiones y el valor del scrollBar. Explicación: sucede que al colocar de manera 
        dinámica objetos en un layout, el objeto no aparece hasta que no termina toda la función que lo crea, por ende, los intentos de redimencionar los frames o dar un nuevo 
        valor al ScrollBar para que siempre muestre el último elemento no funcionan.
        Por ello es que llamamos a ésta función con un hilo de ejecución a parte del ppal, para que así el hilo ppal termine correctamente, y éste hilo espera a que eso suceda 
        para luego sí realizar las acciones necesarias para ajustar los widgets.
        El parametro guia, indica el objeto que esperamos que cambie su estado.
        El parametro Aparicion en True, es porque esperamos a que aparezca el objeto indicado, de lo contrario, es que estamos esperando a que desaparezca.'''
        
        print("\nINICIO: Espera_renglon 625")

        # Nombre del renglón que esperamos
        nombre = "frame_renglon_{}".format(guia)
        
        bucle = True
        encontrado = False
        while bucle:
            for child in vtn.findChildren(Lista_venta):
                if child.objectName() == nombre:
                    encontrado = True
            if Aparicion == True:
                if encontrado == True:
                    bucle = False
            else:
                if encontrado == False:
                    bucle = False
        V_Ventas.Ajusta_Frame_Scroll(vtn_w, Lista_Datos)
        print("\nFIN: Espera_renglon 643")

    '''#############################################################################################################################################
                                                        FUNCIONES DEDICADAS A LAS PROMOS
    #############################################################################################################################################'''

    def Detecta_Promo(vtn, vtn_w, Lista_Datos, encontrado, Codigo):
        '''Controla si el código cargado o el producto y cantidades cargadas pertenecen o no a una promo.'''

        # ATENCIÓN: Cuando se carga el código de una promo se sobreentiende que es lo que quieren y entonces directamente vamos a cargar la promo.
            # Pero cuando detectamos que un producto forma parte de una promo, el cliente puede o no querer la promo, por ello es que vamos a consultar antes de cargarla.

        # Cuando el producto no existe, entonces puede ser un código de promo
        if encontrado == 0:
            existe, lista = mdbprom.Busca_Cod_Promo("Promos", "Codigo", Codigo)
            # True: Existe la promo
            if existe == 1:
                
                # Cuando la promo es simple, un producto con diversas cantidades
                if lista[4] == 1:
                    V_Ventas.Acepta_Promo_Simple(vtn, vtn_w, Lista_Datos, lista)

                # Cuando la promo es compleja
                elif lista[4] == 2:
                    V_Ventas.Acepta_Promo_Compleja(vtn_w, Lista_Datos, lista)

                return True
        
        elif encontrado == 1:
            # El producto es normal así que vamos a ver si se puede vender
            estado, msj = V_Ventas.Analiza_Producto(Lista_Datos)
            if estado == True:
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
            else:
                QMessageBox.question(vtn, "Error", msj, QMessageBox.Ok)
        return False

    def Acepta_Promo_Simple(vtn, vtn_w, Lista_Datos, Lista_Promo):
        '''Se ejecuta cuando sabemos que el cliente quiere comprar la promo, porque por ej pudo haber comprado un producto pero no quiere llevarse los 3 que componen la promo,
        en este caso preparamos los datos necesarios para cargar dicha promo, y luego llamamos a la función que carga la promo.'''

        Prod_de_Promo = Lista_Promo[5]
        nomb = "PROMO: " + Lista_Promo[2]
        costo = Lista_Promo[15]

        # En la db hay un campo de texto con el producto, precio y cantidad, vamos a extraer de ahí esos datos
            # Nos llegan 3 listas cuyo nombre nos indica por producto sus datos
        lista_Codi, lista_Cant, lista_Pcio = mi_func.Dev_Info_Promo_1(Prod_de_Promo)

        # Cargamos la promo en las ventas(lista[15]: Monto total de la promo. lista_promo[1]: Cod de la promo)
        V_Ventas.Carga_Prod_Promo1(vtn, vtn_w, Lista_Datos, Lista_Promo[1], nomb, costo, lista_Codi, lista_Cant, lista_Pcio)

    def Acepta_Promo_Compleja(vtn_w, Lista_Datos, Lista_de_Promo, Codigo = "0"):
        '''Su función es cargar los códigos de los productos que componen la promo, una vez que sabemos que el cliente va a adquirir la promo, y actualizar los datos en 
        ventana.
        El parametro Codigo, viene con el codigo del primer producto que se haya pasado por el scaner.'''
        
        # Obtenemos la cantidad de productos que tiene que tener la promo, los códigos y sus precios dentro de la promo
        cant = 0
        precio = 0.0
        lista_codigos = []
        cant, precio, lista_codigos = mi_func.Dev_Info_Promo_2_Codigos(Lista_de_Promo[5])

        # Datos para los ListWidgets
        Lista_Datos[36] += 1
        Guia_s = str(Lista_Datos[36])
        Concepto_s = "PROMO >>> " + Lista_de_Promo[2]
        P_Unitario_s = form.Formato_Decimal(precio, 2)
        Cantidad_s = form.Formato_Unidades(cant, 3)
        Subtotal_s = form.Formato_Decimal(Lista_de_Promo[15], 2)
        # Agregamos a la lista que contiene las ventas el ID, Nro(en los listwidget), Pcio Costo de la promo float, Cant, costo de nuevo, T_F, Pcio de compra.
        # No hay problema si se cancela la promo en algún momento, xq se llama a la función de Eliminar, que se encarga de eliminar el último ítem de la ventana mostrada y 
        # luego busca en la lista_venta-real el nro de guía, si no hay ninguno no pasa nada, si hay los elimina.
        Lista_Datos[22].append([Guia_s, Concepto_s, P_Unitario_s, Cantidad_s, Subtotal_s])

        if Codigo != "0":
            listilla = []
            encontrado, listilla, conexion = mdb_p.Dev_Info_Producto(Codigo)
            # Luego de hacer un llamado a las bases de datos, informamos cómo resultó la conexión con el mensaje superior en ventana
            V_Ventas.Mensaje_De_Conexion(vtn_w, conexion)
            Concepto_s = "PROMO >>> {} {} {}".format(listilla[4], listilla[5], listilla[6])
            Lista_Datos[21].append([listilla[0], Concepto_s, precio, 1, precio, Guia_s, listilla[20], Lista_de_Promo[1]])

            # Cargamos la lista necesaria para la continuación de la promo
            Lista_Datos[30] = []
            Lista_Datos[30].append(1)
            Lista_Datos[30].append(cant)
            Lista_Datos[30].append(lista_codigos)
            Lista_Datos[30].append(precio)
            Lista_Datos[30].append(Lista_de_Promo)
            Lista_Datos[30].append(precio)
            Lista_Datos[30].append(Guia_s)
        else:
            # Cargamos la lista necesaria para la continuación de la promo
            Lista_Datos[30] = []
            Lista_Datos[30].append(0)
            Lista_Datos[30].append(cant)
            Lista_Datos[30].append(lista_codigos)
            Lista_Datos[30].append(0.0)
            Lista_Datos[30].append(Lista_de_Promo)
            Lista_Datos[30].append(precio)
            Lista_Datos[30].append(Guia_s)

        V_Ventas.Config_Ingreso_Promo(vtn_w, Lista_Datos)

    '''#############################################################################################################################################
                                                            FUNCIONES DE WIDGETS
    #############################################################################################################################################'''

    def Return_line_Cod(vtn, vtn_w, Lista_Datos):
        '''Evento Return del line_cod. En la función explicamos los pasos más detalladamente.'''
        # Pasos:
        # Controlamos que haya algo escrito en el line
        # Ejecutamos los comandos especiales
        # Controlamos si es o no una promo
        # Cargamos los datos del producto
        # Ofrecemos crear un producto nuevo

        # Se realizan múltiples acciones en las diferentes funciones, por ende, necesitamos asegurarnos que ninguna nos cierre el programa.
        try:
            # Si el Enter que llama a ésta función fue el que se ejecuta después de haber cargado el signo pesos con el lector, entonces ignoramos
            if Lista_Datos[1] == 1:
                Lista_Datos[1] = 0
                V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
                return

            # Si no hay nada escrito, llevamos el foco al line para ingresar el monto con el que paga el cliente
            if vtn_w.line_Codigo.text() == "":
                # La acción de apretar Enter con el Line vacío cuando se está esperando una promo, equivale a: +80+
                if Lista_Datos[29] == True:
                    V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
                    Lista_Datos[29] = False                          
                    V_Ventas.Carga_Prod(vtn, vtn_w, Lista_Datos, Lista_Datos[23])
                    V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
                else:
                    vtn_w.line_Monto.setFocus()
                return

            # Capturamos el texto escrito en el line
            texto = vtn_w.line_Codigo.text()

            # Si son comandos especiales, salimos de la función
            if V_Ventas.Comandos_Especiales_Enter(vtn, vtn_w, Lista_Datos, texto) == True:
                return

            # La función nos devuelve en la primer variable (0= no existe; 1= Existe y es código normal; 2= Es codXbulto; 3= Producto Desactivado), de ser > 0, entonces en la 
                # lista están todos sus datos. En conexión nos llega información desde cuál base de datos pudo obtener la información, así podemos informar si estamos 
                # conectado por wifi a la db ppal o si estamos trabajando de manera local.
            encontrado, Lista_Datos[23], conexion = mdb_p.Dev_Info_Producto(texto)
            # Luego de hacer un llamado a las bases de datos, informamos cómo resultó la conexión con el mensaje superior en ventana
            V_Ventas.Mensaje_De_Conexion(vtn_w, conexion)

            # Si es una Promo, salimos de la función
            if V_Ventas.Detecta_Promo(vtn, vtn_w, Lista_Datos, encontrado, texto) == True:
                return

            # Cuando el producto no existe
            if encontrado == 0:
                Rta = QMessageBox.question(vtn, "Desconocido", "El código no existe.", QMessageBox.Ok)
                V_Ventas.Limpia_Foco_Cod(vtn_w,Lista_Datos)
            else:
                if encontrado == 2:
                    Lista_Datos[24] = Lista_Datos[23][3]

                estado, msj = V_Ventas.Analiza_Producto(Lista_Datos)

                if estado == False:
                    QMessageBox.question(vtn, "ERROR CON EL PRODUCTO", msj, QMessageBox.Ok)
                else:
                    # Venta por unidad
                    if Lista_Datos[23][7] == 1:
                        V_Ventas.Carga_Prod(vtn, vtn_w, Lista_Datos, Lista_Datos[23])
                        return
                    # Venta por cantidad o peso
                    else:
                        V_Ventas.Config_Ingreso_Precio(vtn_w, Lista_Datos, Lista_Datos[23][7])

            # Cant_Proxima = 0
            Lista_Datos[24] = 0
            V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
            if vtn_w.stackedWidget.currentWidget() != vtn_w.page_msjs:
                V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
        except:
            QMessageBox.question(vtn, "ERROR", "Anote el PRODUCTO para tener registro del error.", QMessageBox.Ok)
            V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)

    def Change_ScrollBar(vtn_w, Lista_Datos):
        '''Si el scroll está habilitado, entonces movemos el frame_lista con los valores del mismo para mostrar lo que no entra en el frame_content_lista.'''
        # No es necesario controlar si el frame puede moverse o el rango, ya que el evento sólo se va a ejecutar si es posible y dentro de los valores correctos.
        if Lista_Datos[26] == False:
            valor = vtn_w.verticalScrollBar.value()
            ancho = vtn_w.frame_lista.width()
            alto = vtn_w.frame_lista.height()
            vtn_w.frame_lista.setGeometry(0, 0 - valor, ancho, alto)

    def Change_line_Cod(vtn, vtn_w, Lista_Datos):
        '''Evento Change del line. Permite todo tipo de letras, números y signos, y cuando hay 1 o 2 caracteres analiza si es un comando especial.'''
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

    def Change_line_GB_Precio(vtn_w):
        '''Evento Change del line que se encuentra en las opciones del GroupBox de precios. Permite números y (, y .) pero los traduce a una única coma.'''
        vtn_w.line_Ingresos.setText(form.Line_Num_Coma_(vtn_w.line_Ingresos.text()))

    def Return_line_GB_Precio(vtn, vtn_w, Lista_Datos):
        '''Evento Enter en el line que está dentro del groupBox que carga precios, litros, etc...'''

        # La posición [31] hace referencia al tipo de valor que vamos a cargar, ver la función def Config_Ingreso_Precio
        texto = vtn_w.line_Ingresos.text()
        # Cuando [31] = 0, es que se debe volver o se canceló. Vale 6 cuando se quiere editar el precio de un producto, y las demás opciones es para cargar precio, peso, lts...
        if Lista_Datos[31] != 6:
            if len(texto) > 0:
                # Capturamos el texto escrito en el line
                Lista_Datos[24] = form.Str_Float(texto)
                V_Ventas.Carga_Prod(vtn, vtn_w, Lista_Datos, Lista_Datos[23])
                V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
                V_Ventas.Config_Ingreso_Precio(vtn_w, Lista_Datos)
                V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
            else:
                V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
                V_Ventas.Config_Ingreso_Precio(vtn_w, Lista_Datos)
        else:
            if len(texto) > 0:
                threading.Thread(target=V_Ventas.Espera_renglon, args=(vtn, vtn_w, Lista_Datos,Lista_Datos[36], True,)).start()
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

    def Return_line_Promo(vtn, vtn_w, Lista_Datos):
        '''Evento Enter en el line dentro del groupBox de Promos.'''

        texto = vtn_w.line_Ingreso_Promo.text()

        if len(texto) > 0:

            # Si es un código de la promo que se está cargando
            if texto in Lista_Datos[30][2]:

                # True: Último producto de la promo. False: Lo contrario.
                if Lista_Datos[30][0] == Lista_Datos[30][1] - 1:

                    # Si es el último producto, guardamos en la variable de Precio, el monto de lo que debe valer el último producto cargado.
                    Lista_Datos[30][5] = float(form.Ajusta_A_2_Dec(Lista_Datos[30][4][15] - Lista_Datos[30][3]))

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
                    # Actualizamos la LISTA MOSTRADA
                    #Lista_Datos[22].append([Lista_Datos[30][6], Lista_Datos[30][4][2], Lista_Datos[30][5], Lista_Datos[30][1], Lista_Datos[30][4][15]])
                    # Cargamos en los listW el producto
                    V_Ventas.Crea_renglon(vtn, vtn_w, Lista_Datos)
                    # Volvemos a la ventana normal
                    V_Ventas.Config_Ingreso_Promo(vtn_w, Lista_Datos, False)
                    V_Ventas.Suma_Venta(vtn_w, Lista_Datos)
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
            V_Ventas.Cancela_Promo_2(vtn, vtn_w, Lista_Datos)

    def Change_line_Monto(vtn_w, Lista_Datos):
        '''Evento change del line_monto que calcula lo que debe devolverse en caso de pagar con efectivo, y si se presiona algún símbolo aceptado (/*+$) se limpia y dirige el foco hacia el line_cod.'''
        texto = vtn_w.line_Monto.text()

        if "/" in texto or mi_vars.BTN_IGUAL in texto or "*" in texto or "+" in texto or "$" in texto:
            vtn_w.line_Monto.setText("")
            V_Ventas.Event_press_barra(vtn_w, Lista_Datos)
            return
        
        texto = form.Line_Num_Coma_(texto)
        vtn_w.line_Monto.setText(texto)
        if texto != "":
            vtn_w.label_Vuelto.setText(form.Formato_Decimal(form.Str_Float(vtn_w.line_Monto.text()) - V_Ventas.Aux_Suma_Venta(vtn_w, Lista_Datos), 2))

    def Return_line_Monto(vtn_w, Lista_Datos):
        '''Dirige el foco al botón de cargar, pero también utiliza la posición [2] para funcionar como bandera del evento keyPressEvent en el módulo ppal, donde ahí se explica 
        mejor su motivo.'''
        Lista_Datos[2] = 1
        vtn_w.push_Cargar.setFocus()

    '''#############################################################################################################################################
                                                            FUNCIONES PARA WIDGETS
    #############################################################################################################################################'''

    def Elimina_Item(vtn, vtn_w, Lista_Datos, ubi = 0):
        print("INICIO: Elimina_Item")

        '''Elimina algún renglón de la lista siguiendo las siguientes prioridades: Primero controla el parámetro ubi, luego si existe alguna selección en Lista_Datos[0], de lo contrario elije el último renglón para borrar. Nota: el primer renglón será 1 y no 0.'''
        largo = len(Lista_Datos[22])
        if largo > 0:
            pos = 0
            # True: Cuando viene con una ubicación indicada. False: Sin ubicación
            if ubi > 0:
                if ubi <= largo:
                    pos = ubi
                else:
                    QMessageBox.question(vtn, "Error", "Error al indicar ubicación del PRODUCTO que desea ELIMINAR.", QMessageBox.Ok)
                    return
            else:
                if Lista_Datos[0] > 0:
                    pos = Lista_Datos[0]
                else:
                    pos = largo
            
            # Eliminamos el renglón
            V_Ventas.lista_renglones[pos - 1][1].deleteLater()
            # Debemos eliminar su referencia para que no hayan más datos
            V_Ventas.lista_renglones.pop(pos - 1)
            # Obtenemos el número de Guía antes de eliminar todo registro de la lista 22
            texto = Lista_Datos[22][pos-1][0]
            # Eliminamos de la lista de productos en pantalla
            Lista_Datos[22].pop(pos-1)
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

            # Quitamos la selección que haya y restauramos los colores como si no hubiera selección
            if pos != largo or Lista_Datos[0] > 0:
                V_Ventas.Colores_de_renglones()
                Lista_Datos[0] = 0

            threading.Thread(target=V_Ventas.Espera_renglon, args=(vtn, vtn_w, Lista_Datos, texto, False,)).start()
            V_Ventas.Config_Mensaje(vtn_w, Lista_Datos)
            V_Ventas.Suma_Venta(vtn_w, Lista_Datos)
            V_Ventas.Limpia_Foco_Cod(vtn_w, Lista_Datos)
        else:
            QMessageBox.question(vtn, "Aviso", "No hay productos cargados para ELIMINAR.", QMessageBox.Ok)
        print("FIN: Elimina_Item")

    def Cancela_Promo_2(vtn, vtn_w, Lista_Datos):
        '''Función que reestablece lo que se haya cargado en el caso de que se haya cancelado una promo del tipo 2 en medio de la carga.'''
        V_Ventas.Elimina_Item(vtn, vtn_w, Lista_Datos)
        V_Ventas.Config_Ingreso_Promo(vtn_w, Lista_Datos, False)

    def Color_seleccion(guia, Lista_Datos):
        '''Le llega como parámetro la guía que nos indica qué renglón se ha presionado. A ésta función la llaman los 5 labels que componen al renglón.
        Esta función se encarga de marcar como seleccionado el renglón entero pintándolo y además cargando su valor en la Lista_Datos[0]'''
        # color es el parametro que va a indicar que paleta de colores utilizar (ver modulo renglones.py)
        color = 2
        # Si hay renglones, continuamos
        if len(V_Ventas.lista_renglones) > 0:
            # Si había alguna selección, quitamos su color
            if Lista_Datos[0] > 0:
                V_Ventas.Colores_de_renglones()
            # Recorremos los renglones que tenemos en la listsa_renglones, cuando encontramos el que buscamos, guardamos su valor en la variable y lo pintamos de color
            for i in V_Ventas.lista_renglones:
                if i[1].objectName() == "frame_renglon_{}".format(guia):
                    Lista_Datos[0] = int(guia)
                    i[1].Lista_Labels[0].asigna_fondo(color)
                    i[1].Lista_Labels[1].asigna_fondo(color)
                    i[1].Lista_Labels[2].asigna_fondo(color)
                    i[1].Lista_Labels[3].asigna_fondo(color)
                    i[1].Lista_Labels[4].asigna_fondo(color)
                    return

    def Colores_de_renglones():
        '''Recorre todos los renglones y le asigna de nuevo un color de fondo y renumera el valor de Nro de la lista.'''
        largo = len(V_Ventas.lista_renglones)
        cont = 0
        for pos in range(largo):
            cont += 1
            color = 1
            if (pos + 1) % 2 == 0:
                color = 0
            V_Ventas.lista_renglones[pos][1].Lista_Labels[0].setText(str(cont))
            V_Ventas.lista_renglones[pos][1].Lista_Labels[0].asigna_fondo(color)
            V_Ventas.lista_renglones[pos][1].Lista_Labels[1].asigna_fondo(color)
            V_Ventas.lista_renglones[pos][1].Lista_Labels[2].asigna_fondo(color)
            V_Ventas.lista_renglones[pos][1].Lista_Labels[3].asigna_fondo(color)
            V_Ventas.lista_renglones[pos][1].Lista_Labels[4].asigna_fondo(color)

    def Ajusta_Frame_Scroll(vtn_w, Lista_Datos):
        print("INICIO: Ajusta_Frame_Scroll 1096")

        '''Rajusta los valores del scrollbar en función a los datos actuales de la aplicación, es decir, que ya deben haberse realizado los cambios necesarios. Adicionalmente coloca la lista mostrando el último producto de la misma al final.'''
        # Nota: el valor mínimo del scroll es siempre 0.
        
        # Desactivamos el evento change
        Lista_Datos[26] = True
        # Obtenemos los valores necesarios
        cant_renglones = len(Lista_Datos[22])
        alto_renglones = (cant_renglones * Lista_Datos[34][1]) + cant_renglones
        alto_panel = vtn_w.frame_panel_lista.height() - vtn_w.frame_labels.height()
        ancho = vtn_w.frame_labels.width()
        # Redimencionamos este frame, que sólo es necesario redimencionar cuando se modifica el tamaño de la ventana
        #vtn_w.frame_content_lista.setFixedSize(QtCore.QSize(ancho, alto_panel))
        if alto_panel < alto_renglones:
            max = alto_renglones - alto_panel
            vtn_w.verticalScrollBar.setMaximum(max)
            vtn_w.frame_lista.setGeometry(0, 0 - max, ancho, alto_renglones)
            cont = 0
            for i in V_Ventas.lista_renglones:
                i[1].setGeometry(0, 41 * cont, ancho, 41)
                cont += 1
            vtn_w.verticalScrollBar.setValue(max)
        else:
            vtn_w.verticalScrollBar.setMaximum(0)
            vtn_w.verticalScrollBar.setValue(0)
            vtn_w.frame_lista.setGeometry(0, 0, ancho, alto_renglones)
        Lista_Datos[26] = False
        V_Ventas.Imprime(vtn_w)
        print("FIN: Ajusta_Frame_Scroll 1100")

    def Evento_Rezise(vtn_w, Lista_Datos):
        '''Cuando se redimenciona la ventana, algunos layout no se ajustan automáticamente al tamaño que esperamos, así que lo realizamos manualmente.'''
        
        # El frame_panel_lista es la guía, porque es el panel que se ajusta correctamente al máximo que necesitamos y dentro de él se acomodan los demás.
        # El frame_panel, contiene otros incluyendo el título de las columnas, a éste lo ajustamos restando el espacio que el título usa.
        # El frame_labels, es el título de las columna, un frame que permanece fijo.
        # El frame_content_lista, es el que debe reajustarse al espacio que queda dentro del frame_panel luego de restar el título. Funciona como ventana para ver los prod.
        # El frame_lista, es quién contiene las listas, debe ajustarse manualmente ya que si no tiene el tamaño que los renglones usan se comporta con error, por ejemplo, si
            # su tamaño es mayor, los renglones de muestran dispersos, si su tamaño es menor, los renglones se empiezan a encimar, y en el caso de que la lista de productos es
            # superior a lo que puede mostrarse en pantalla, éste frame debe tener ese valor también superior ya que eso va a hacer que los renglones se sigan viendo correctam-
            # mente porque el frame_content_lista funciona como ventana mostrando los que puedan verse. En ese momento se activa el scrollBar para poder observar los que no
            # llegan a aparecer en pantalla.

        # AJUSTAMOS frame_panel
        alto_panel = vtn_w.frame_panel_lista.height()
        ancho = vtn_w.frame_labels.width()
        vtn_w.frame_panel.setMinimumSize(QtCore.QSize(ancho, alto_panel))
        
        # AJUSTAMOS frame_content_lista
        alto = alto_panel - vtn_w.frame_labels.height()        
        vtn_w.frame_content_lista.setMinimumSize(QtCore.QSize(ancho, alto))

        # AJUSTAMOS frame_lista
        cant_renglones = len(Lista_Datos[22])
        alto_renglones = (cant_renglones * Lista_Datos[34][1]) + cant_renglones
        vtn_w.frame_lista.setMinimumSize(QtCore.QSize(ancho, alto_renglones))

        # Ajustamos el ancho de los renglones.
        # Explcación: Cuando se modifica el tamaño queremos que todas las columnas se mantengan igual, pero redimencionamos la de los conceptos. Debido a que ésta no contiene
            # un layout distinto para que se comporte de tal modo, lo tengo que redimencionar de manera manual, por ende, recorremos todos los renglones y lo cambiamos.
            # IMPORTANTE: El ancho actual que las demás columnas ocupan es 460, un valor que se utiliza aquí y también en la clase que crea los renglones. Adaptar ésto a una
                # función me tomará más tiempo así que por el momento será así, pero el renglón debería incluír la función que redimencione sus renglones, debiendo ser invoca-
                # da desde fuera, ya que el evento resizeEvent no se ejecuta en el renglón cuándo se redimenciona la ventana, xq justamente sólo se redimenciona la ventana pero
                # no el renglón.
        # Además, tenemos que ajustar el frame del título del concepto porque a pesar de que en el QtDesigner es comporta correctamente, en la App no.
        
        # Ancho renglon sin el scrollBar 40
        ancho_ren = vtn_w.frame_panel_lista.width() - 40
        ancho_con = ancho_ren - 460
        vtn_w.frame_concepto.setFixedWidth(ancho_con)
        vtn_w.frame_panel.setFixedWidth(ancho_ren)
        vtn_w.frame_labels.setFixedWidth(ancho_ren)
        vtn_w.frame_content_lista.setFixedWidth(ancho_ren)
        vtn_w.frame_lista.setFixedWidth(ancho_ren)

        if len(V_Ventas.lista_renglones) > 0:
            for i in V_Ventas.lista_renglones:
                i[1].setFixedWidth(ancho_con)
            print("Ancho del CONCEPTO: {}".format(i[1].width()))

    '''#############################################################################################################################################
                                                            FUNCIONES GENERALES
    #############################################################################################################################################'''

    def Suma_Venta(vtn_w, Lista_Datos):
        print("INICIO: suma_venta 1153")

        '''Suma los subtotales y coloca el total en el label. Al mismo tiempo devuelve el valor total en formato float si es que lo requieren.
        Nota: Debido a que a ésta función se la llama cada vez que hay un cambio en los datos en pantalla, le he incorporado que controle y actualice el valor del monto a devolver a un cliente que se ha calculado al pagar con efectivo. La causa es que a veces se termina de realizar una venta, se calcula lo que le debemos devolver al cliente pero si se elimina o agrega un producto, el monto queda sin actualizar así que pueden cobrar mal, esto lo soluciona.'''
        aux = V_Ventas.Aux_Suma_Venta(vtn_w, Lista_Datos)
        if len(Lista_Datos[21]) > 0:
            vtn_w.label_Total.setText(form.Formato_Decimal(aux, 2))
        else:
            vtn_w.label_Total.setText("0,00")
        if vtn_w.line_Monto.text() != "":
            V_Ventas.Change_line_Monto(vtn_w, Lista_Datos)
        print("FIN: suma_venta 1164")
        return aux

    def Aux_Suma_Venta(vtn_w, Lista_Datos):
        '''Calcula la suma de la venta devolviendo un resultado del tipo float. '''
        aux = 0.0
        if len(Lista_Datos[21]) > 0:
            for pos in Lista_Datos[21]:
                aux += pos[4]
        return aux

    def Limpia_Foco_Cod(vtn_w, Lista_Datos):
        print("INICIO: Limpia_Foco_Cod 1175")

        ''''Trabaja sobre el line_codigo, limpiándolo y luego llevando el foco sobre él. '''
        Lista_Datos[27] = True
        vtn_w.line_Codigo.setText("")
        vtn_w.line_Codigo.setFocus()
        Lista_Datos[27] = False

        print("FIN: Limpia_Foco_Cod 1184")

    def Analiza_Producto(Lista_Datos):
        
        ''' (*1) Función que controla si el producto que está por cargarse (pos[23]) se puede vender en función a la configuración actual del sistema (pos[32]). Devuelve un 
        V/F indicando si se puede vender, y en caso de que no se pueda regresa el mensaje indicando la cuasa.'''

        estado = Lista_Datos[23][19]
        stock = Lista_Datos[23][8] + Lista_Datos[23][8] + Lista_Datos[23][8]
        config = Lista_Datos[32]
        cant = 1
        if Lista_Datos[24] > 0:
            cant = Lista_Datos[24]
        
        # True: Permite sin stock. False: Sólo con stock disponible.
        if config < 3:
            if config == 0:
                return True, ""
            elif config == 1:
                if estado == 0:
                    return False, "El producto está DESACTIVADO. El programa se encuentra configurado de manera tal que no permite éste tipo de ventas."
                else:
                    return True, ""
            elif config == 2:
                if estado == 0:
                    return False, "El producto está DESACTIVADO. El programa se encuentra configurado de manera tal que no permite éste tipo de ventas."
                elif estado == 1:
                    return False, "El producto está INCOMPLETO. El programa se encuentra configurado de manera tal que no permite éste tipo de ventas."
                elif estado == 2:
                    return True, ""
        else:
            if stock >= cant:
                if config == 3:
                    return True, ""
                elif config == 4:
                    if estado == 0:
                        return False, "El producto está DESACTIVADO. El programa se encuentra configurado de manera tal que no permite éste tipo de ventas."
                    else:
                        return True, ""
                elif config == 5:
                    if estado == 2:
                        return True, ""
                    else:
                        if estado == 1:
                            return False, "El producto está INCOMPLETO. El programa se encuentra configurado de manera tal que no permite éste tipo de ventas."
                        elif estado == 0:
                            return False, "El producto está DESACTIVADO. El programa se encuentra configurado de manera tal que no permite éste tipo de ventas."
            else:
                return False, "El producto NO TIENE STOCK suficiente. El programa se encuentra configurado de manera tal que no permite éste tipo de ventas."

    def Imprime(vtn_w):
        print("IMPRIME 1:")
        print("ancho frame panel lista: {}".format(vtn_w.frame_panel_lista.width()))
        print("alto frame panel lista: {} \n".format(vtn_w.frame_panel_lista.height()))
        print("ancho frame panel: {}".format(vtn_w.frame_panel.width()))
        print("alto frame panel: {}\n".format(vtn_w.frame_panel.height()))
        print("ancho frame labels: {}".format(vtn_w.frame_labels.width()))
        print("alto frame labels: {}\n".format(vtn_w.frame_labels.height()))
        print("ancho frame content lista: {}".format(vtn_w.frame_content_lista.width()))
        print("alto frame content lista: {}".format(vtn_w.frame_content_lista.height()))
        print("ancho frame lista: {}".format(vtn_w.frame_lista.width()))
        print("alto frame lista: {}".format(vtn_w.frame_lista.height()))
        try:
            print("ancho RENGLON 50: {}".format(V_Ventas.lista_renglones[50].width()))
            print("alto RENGLON 50: {}".format(V_Ventas.lista_renglones[50].height()))
        except:
            pass


