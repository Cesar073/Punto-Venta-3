'''
HACER:
    *** Por alguna razón, algunos productos se han guardado sin aclarar el tipo de unidad de medida, por ende generan un error.
    *** Boton de Verificado, se puede apretar y no cotrola los datos que hay en el producto actual, porende se puede verificar algo incorrecto
    *** Dsp de guardar prod nuevo, limpiar pantalla
    *** Dsp de guardar producto nuevo, no acomoda el color de fondo
    *** Ver porqué cambia la letra de la ventana
    *** Al LIMPIAR, Verificado debe actualizarse a SIN VERIFICAR
    *** Cuando realiza una búsqueda, debe rellenar todas las variables de las listas aunq sean valores vacíos
    *** Cuando se guarda un producto nuevo, no elimina el código inicial y el cursor aparece en el 2do line
    *** Ver que pasó  con los mayoristas
    ** Agreguar Cantidad máxima a l db
    *** Reparar Guardar los cambios de un prod
    *** cuando busca un producto en exixstencia no vuelve a acomodar el fondo de los line-edit
    *** la fecha buscada de un producto guardado no concuerda
    *** PRogramar el "Recorrido inicial"
    *** la función de los line, no puede recibir 2 comas juntas, da error
    *** Tiene que obligarme a crear producto nuevo al menos en el estado SIN VERIFICAR
    *** Luego de cargar producto nuevo y buscar un producto en existencia no se ajustaron llos fondos de los line


    *** Que al presionar enter en cualquier parte, haga foco donde corresponda
    *** Hay un error que colapsa todo y es:  module 'source.mod.form' has no attribute 'Trans_Fecha_Num'
    *** Se debe cambiar de foco con el Eneter
    *** Revisar el módulo de Form y cotejarlo con el básico, actualizar lo que sea necesario y nuevamente actualizar la app
    *** Limitar aún más la fecha

    *** No se actualizan las listas de STOCK ni ADICIONALES
    *** Ajustar el foco medainte tabulador desde qt designer
    *** El detalle no deja usar minúsculas
    *** Deja poner cualquier disparate de fecha
    *** Crear proveedores
    *** aGREgar las cajas
    *** Simplificar la función Colores_Contornos
    *** Igual que en la función de Colores_Contornos, también podemos simplificar las funciones de día, mes y año de cada line, en una sóla función. Ver bien los parámetros
        necesarios


    * Que al cambiar la unidad de medida en el combobox, se vuelva a ajustar el valor del line "Cantidad total" ya que queda con un valor que quizás se guarde en float cuando 
    debería ser int. Aún así no refleja lo que se espera en pantalla


EXPLICACIONES:
    Contamos con 3 listas:
        Lista_Datos[3]
        Lista_Datos[4]
        Lista_Datos[5]
        Estas listas contienen por separado los datos del producto mostrado en pantalla. Dichos datos se actualizan cada vez que hay una búsqueda de un producto nuevo, y luego
            a medida que se van editando en ventana. De ésta manera tendríamos enlistados los datos para ser comparados en caso de tener que realizarlo como por ejemplo, cuando
            hay que controlar si hubieron cambios sin guardar.
        vtn.LISTA_BD
        Esta lista contiene los datos extraídos de la base de datos. Si hubieran cambios en los datos mostrados en pantalla, antes de hacer alguna actividad importante se 
        pueden compara ésta lista con las otras 3 y así saber si hubieron cambios o no, sin necesidad de abrir la bd.

    Lista de Unidades de Medida:
        Unidad
        Peso - Kilogramos
        Litros
        cm3
        Precio
'''

'''
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
#rom vtn.vtn.vtn_productos import Ui_Productos
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QDir, Qt
'''
from main import *

import sources.mod.vars as mi_vs
import sources.mod.mdbprod as mdb
import sources.mod.mdbegen as mdb_gen
import sources.mod.mdbvari as mdb_var
import sources.mod.img
import sources.mod.nave as nv
import sources.mod.form as form
import sources.mod.mdbvari as mdb_var


'''
    HACER URGENTE:
    * Que la imagen estén en una carpeta y se maneeje cmo el de essen, no podemos tener un path para cada imagen en la db
    * Necesita que un botón del teclado numérico pueda ubicar el cursor de nuevo donde van los códigos

    * Hay una bd de estadísticas que no se crea un espacio para cada producto que se va creando
    
    * Tengo que agregar en la ventana de Productos, el espacio para "Sobrantes". Ese dato será un dato que se cargará automáticamente en función de las modificaciones de 
    stock. Cuando se modifique manualmente el stock y se coloque más stock de lo que había antes una vez ya verificado el mismo, éste se irá acumulando. Ésto estaría indicando 
    al usuario que hay un defasaje en las cantidades y que seguramente se ha cargado alguna venta de manera equivocada y es importante resolver. En los momentos en que se 
    ejecute algún algoritmo que rastree diferencias en las cajas o de stock, éste dato será importante para encontrar errores.

    * Debo agregar un algoritmo para encontrar diferencias de montos. Por ejemplo si no coincide la plata que tenemos en la caja principal o la caja chica, el algoritmo y la 
    interfaz deberían ofrecernos datos para encontrar dichas diferencias. Por ejemplo, mostrar las ventas del día, mostrar si es que se puede las ventas de otros días, mostrar 
    los productos donde figuran datos de siniestros o sobrantes, etc...

    ***** Debe marcar que hay un error y no que no se encontró el producto
    * No carga Cantidad por bulto cuando se busca un producto
    * Modifica el texto en los lineEdit
    * Cantidad total, tiene un formato con . en vez de ,
    * Que al apretar el MAS me ponga el cursor en Cantidad
    * Hace mal la suma de total de cantidad
    * Cuando limpia la pantalla tmb tiene que devolver los contornos de base y el color de fondo de la imagen
    * Permitió precio de costo incorrecto
    * Cuando reinicia las variables, no reinicia el estado de los conjuntos

    * NO ACTUALIZA EL ID CADA VEZ QUE GUARDA UN PRODUCTO NUEVO
    ******* Permite ingresar fechas erróneas
    ******* No se guardó el vencimiento
    ******* No cargó el días de preaviso
    * No busca correctamente los productos que ya están el la base de datos
    ******* Que la modificación de los datos en Cantidad, ajuste el label de cantidad total

    ******* ESTOY HACIENDO LA FUNCIÓN QUE ESTÁ AL FINAL. PREPARA TODO PARA BLOQUEAR LO QUE NO ES ÚTIL O URGENTE EN LA CARGA RÁPIDA DE PRODUCTOS 
    ******* Colocar un Estado mientras se guarda producto nuevo
    ******* Permite fechas pasadas
    ******* La cantidad total no debería ser editable

    HACER EN 2DA INSTANCIA:
    * La función "Controla_Datos_Ventana", controla que los datos estén en orden y hay algunos casos que indica que puede dejar los datos como están pero debe corregirlos si es que va a calificarlo como VERIFICADO. El problema está en que se puede cargar acá mismos como VERIFICADO pero la función ignora ésto, así que por mas que esté o no verificado va dar aviso como si no lo estuviera.
    * Permitir que se puedan cargar una lista de Proveedores a cada producto, y más de un link a web. Para que cuando tengamos la función que busca los precios sólos por
        internet, sepa qué productos buscar por cada proveedor, y cuántas y cuáles páginas posee cada proveedor.
    * Que todos los campos obligatorios tengan el color rojo si estana mal cargados

    Código a agregar si queremos recuperar la estética de la ventana
    vtn.label_Imagen_2.setStyleSheet("QLabel {background-color: white; border: 1px solid #334CFF; border-radius: 5px;}")
    vtn.push_Verificado.setStyleSheet("background-color: rgb(208, 211, 212);")

    border: 1px solid #334CFF >>> indica que el borde va a tener un grosor de 1 píxel, que el color es sólido y su color está escrito en html
    border-radius: 5px >>> indica que el borde va a ser redondeado de 5 píxeles
    NOMBRE DEL WIDGETS.setStyleSheet("background-color: rgb(237, 127, 16);")
'''

class V_Productos(QMainWindow):


    '''#############################################################################################################################################
                                                                FUNCIONES DE VENTANA  '''

    def Mostrar(vtn, Lista_Datos):
        if Lista_Datos[8] != "":
            vtn.line_Codigo_2.setText(Lista_Datos[8])
            Lista_Datos[8] = ""
            V_Productos.Carga_Info_Ventana(vtn, Lista_Datos, Aviso_New=False)
            vtn.push_Eliminar_2.setVisible(False)
            vtn.push_Reco_Inicial.setVisible(False)
            vtn.push_Menu.setText("Volver")
        else:
            vtn.push_Eliminar_2.setVisible(True)
            vtn.push_Reco_Inicial.setVisible(True)
            vtn.push_Menu.setText("Menu")
        V_Productos.Config_Unidad_de_Medida(vtn)
        vtn.stackedWidget.setCurrentWidget(vtn.page_Cargar_Productos)
        vtn.line_Codigo_2.setFocus()

    # Al apretar Enter en el line del Código, se cargan todos sus datos. También cuando se viene con un código desde la ventana de buscar.
    # Devuelve una lista para mostrar un mensaje
    def Carga_Info_Ventana(matriz, vtn, Lista_Datos, Aviso_New = True):
        Lista_msjs = [False]

        Lista_Datos[3][1] = vtn.line_Codigo_2.text()
        
        # True: si hay algo escrito en el line, se busca ese código. False: se limpia la ventana
        if Lista_Datos[3][1] != "":

            # Controlamos si el producto existe o no
            Encontrado, Lista_Datos[6] = mdb.Dev_Info_Producto(Lista_Datos[3][1], Todos = True)

            if Encontrado:
                Lista_Datos[0] = True
                Lista_Datos[1] = False
                V_Productos.Limpia_Ventana(matriz, vtn, Lista_Datos)
                V_Productos.Copia_BD_Listas(vtn, Lista_Datos, Lista_Datos[6])
                
                # GrupBox: Detalles del Producto
                vtn.line_Codigo_2.setText(Lista_Datos[6][1])
                vtn.line_Cod_Bulto.setText(Lista_Datos[6][2])
                # Ver unidades de medida (en Explicaciones)
                if Lista_Datos[6][2] != "":
                    if Lista_Datos[6][7] == 1 or Lista_Datos[6][7] == 3:
                        vtn.line_Cant_Bulto.setText(form.Formato_Unidades(Lista_Datos[6][3], 0))
                    else:
                        vtn.line_Cant_Bulto.setText(form.Formato_Unidades(Lista_Datos[6][3], 3))
                vtn.line_Concepto.setText(Lista_Datos[6][4])
                vtn.line_Marca.setText(Lista_Datos[6][5])
                vtn.combo_Uni_Medida.setCurrentIndex(Lista_Datos[6][7])
                vtn.line_Detalle.setText(Lista_Datos[6][6])
                vtn.label_Imagen_2.clear()
                if Lista_Datos[6][27] != "":
                    try:
                        pixmapImagen = QPixmap(Lista_Datos[6][27]).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        vtn.label_Imagen_2.setPixmap(pixmapImagen)
                    except:
                        vtn.label_Imagen_2.setText("Imagen")
                
                # GroupBox: Stock
                V_Productos.Estado_Verificado(vtn, Lista_Datos[6][19])
                vtn.line_Pcio_Venta.setText(form.Formato_ValorF_Line(Lista_Datos[6][18]))
                # No es necesario cargar el total porque lo hacen los eventos "Change" de los line de Cantidad
                if Lista_Datos[6][7] == 1 or Lista_Datos[6][7] == 3:
                    vtn.label_Cant_Total.setText(form.Formato_ValorF_Line(Lista_Datos[6][17]))
                else:
                    vtn.label_Cant_Total.setText(form.Formato_ValorF_Line(Lista_Datos[6][17]))
                
                # Se envía la lista de datos a una función que se encarga de habilitar y rellenar los campos que sean necesarios de los conjuntos de stock (cant, vto, pcio)
                V_Productos.Ajusta_Valores_Conjuntos(vtn, Lista = Lista_Datos[6])

                # GroupBox: Detalles Adicionales
                vtn.combo_Caja.setCurrentIndex(Lista_Datos[6][20])
                vtn.combo_Mayorista.setCurrentIndex(Lista_Datos[6][21])
                if Lista_Datos[6][22] > 0:
                    vtn.label_Ult_Fecha_Vta.setText(form.Trans_Num_Fecha(Lista_Datos[6][22]))
                else:
                    vtn.label_Ult_Fecha_Vta.setText("-")
                #vtn.line_Siniestro.setText(form.Formato_ValorF_Line(Lista_Datos[6][23]))
                #vtn.line_Sin_Cobrar.setText(form.Formato_ValorF_Line(Lista_Datos[6][25]))
                vtn.line_Incremento.setText(form.Formato_ValorF_Line(Lista_Datos[6][26]))
                vtn.line_Cant_Preav.setText(form.Formato_ValorF_Line(Lista_Datos[6][28]))
                vtn.line_Cant_Max.setText(form.Formato_ValorF_Line(Lista_Datos[6][29]))
                vtn.line_Dias_Preav.setText(form.Formato_ValorF_Line(Lista_Datos[6][30]))
                Lista_Datos[0] = False
            else:
                # Consultamos si quiere guardar un producto
                Rta = QMessageBox.No
                if Aviso_New == True:
                    Rta = QMessageBox.question(matriz, "Guardar Producto", "El producto buscado NO EXISTE.\n ¿Desea crear un PRODUCTO NUEVO?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                else:
                    Rta = QMessageBox.Yes
                if Rta == QMessageBox.Yes:
                    V_Productos.Reinicia_Variables_Datos(vtn, Lista_Datos)
                    Lista_Datos[3][1] = vtn.line_Codigo_2.text()
                    Lista_Datos[4][11] = 1
                    V_Productos.Estado_Verificado(vtn, 1)
                    V_Productos.Limpia_Ventana(vtn, Lista_Datos, True)
                    Lista_Datos[1] = True
                    vtn.label_Imagen_2.clear()
                    vtn.label_Imagen_2.setText("PRODUCTO\nNUEVO")
                    vtn.label_Imagen_2.setStyleSheet("background: rgb(255,50,50);")
                    vtn.line_Cod_Bulto.setFocus()
                else:
                    vtn.line_Codigo_2.setText("")
        else:
            V_Productos.Limpia_Ventana(vtn, Lista_Datos)

    # Los CONJUNTOS son datos relacionados entre sí relativos a stock. Hay 3 conjuntos y ésta función se encarga de ajustar la ventana a tal fin. Sólo habilita o deshabilita
    # los groupbox para tal fin, a menos que venga la lista de datos.
    # También, si viene alguna Lista entiende que se realizó una búsqueda en la base de datos y cargará los conjuntos que el producto tenga
        # Parámetros:
        # En "Lista" lo que viene es la lista de todos los datos cargados por alguna búsqueda realizada, así que desde allí se toman todos los datos
        # Conjuntos: Pueden ser 1, 2 o 3, y hacen referencia a la cantidad de conjuntos habilitados. Si por ejemplo viene un 2, entonces intenta limpiar los datos del conjunto
            # 3, luego lo deshabilita y se asegura que estén habilitados los conjuntos 1 y 2.
    def Ajusta_Valores_Conjuntos(vtn, Conjunto = 1, Lista = 0):
        if Lista == 0:
            if Conjunto == 3:
                vtn.groupBox_4.setEnabled(True)
                vtn.groupBox_5.setEnabled(True)
            elif Conjunto == 2:
                vtn.groupBox_4.setEnabled(True)
                try:
                    vtn.line_Cant_3.setText("")
                    vtn.line_Vto_3_D.setText("")
                    vtn.line_Vto_3_M.setText("")
                    vtn.line_Vto_3_A.setText("")
                    vtn.line_Pcio_Costo_3.setText("")
                    vtn.groupBox_5.setEnabled(False)
                except:
                    pass
            else:
                try:
                    vtn.line_Cant_2.setText("")
                    vtn.line_Vto_2_D.setText("")
                    vtn.line_Vto_2_M.setText("")
                    vtn.line_Vto_2_A.setText("")
                    vtn.line_Pcio_Costo_2.setText("")
                    vtn.groupBox_4.setEnabled(False)
                    vtn.line_Cant_3.setText("")
                    vtn.line_Vto_3_D.setText("")
                    vtn.line_Vto_3_M.setText("")
                    vtn.line_Vto_3_A.setText("")
                    vtn.line_Pcio_Costo_3.setText("")
                    vtn.groupBox_5.setEnabled(False)
                except:
                    pass
        else:
            vtn.line_Cant_1.setText(form.Formato_ValorF_Line(Lista[8]))
            if Lista[11] > 0:
                fechaAux = form.Trans_Num_Fecha(Lista[11])
                vtn.line_Vto_1_D.setText(form.Extrae_Fecha(fechaAux,1))
                vtn.line_Vto_1_M.setText(form.Extrae_Fecha(fechaAux,2))
                vtn.line_Vto_1_A.setText(form.Extrae_Fecha(fechaAux,3))
            else:
                vtn.line_Vto_1_D.setText("")
                vtn.line_Vto_1_M.setText("")
                vtn.line_Vto_1_A.setText("")
            vtn.line_Pcio_Costo_1.setText(form.Formato_ValorF_Line(Lista[14]))

            if Lista[9] > 0:
                vtn.groupBox_4.setEnabled(True)
                vtn.line_Cant_2.setText(form.Formato_ValorF_Line(Lista[9]))
                if Lista[12] > 0:
                    fechaAux = form.Trans_Num_Fecha(Lista[12])
                    vtn.line_Vto_2_D.setText(form.Extrae_Fecha(fechaAux,1))
                    vtn.line_Vto_2_M.setText(form.Extrae_Fecha(fechaAux,2))
                    vtn.line_Vto_2_A.setText(form.Extrae_Fecha(fechaAux,3))
                else:
                    vtn.line_Vto_2_D.setText("")
                    vtn.line_Vto_2_M.setText("")
                    vtn.line_Vto_2_A.setText("")
                vtn.line_Pcio_Costo_2.setText(form.Formato_ValorF_Line(Lista[15]))
                if Lista[10] > 0:
                    vtn.groupBox_5.setEnabled(True)
                    vtn.line_Cant_3.setText(form.Formato_ValorF_Line(Lista[10]))
                    if Lista[13] > 0:
                        fechaAux = form.Trans_Num_Fecha(Lista[13])
                        vtn.line_Vto_3_D.setText(form.Extrae_Fecha(fechaAux,1))
                        vtn.line_Vto_3_M.setText(form.Extrae_Fecha(fechaAux,2))
                        vtn.line_Vto_3_A.setText(form.Extrae_Fecha(fechaAux,3))
                    else:
                        vtn.line_Vto_3_D.setText("")
                        vtn.line_Vto_3_M.setText("")
                        vtn.line_Vto_3_A.setText("")
                    vtn.line_Pcio_Costo_3.setText(form.Formato_ValorF_Line(Lista[16]))
                else:
                    V_Productos.Ajusta_Valores_Conjuntos(vtn, Conjunto = 2)
            else:
                V_Productos.Ajusta_Valores_Conjuntos(vtn, Conjunto = 1)

    def Reinicia_Ventana(vtn, Lista_Datos):
        vtn.push_Verificado.setStyleSheet("background-color: rgb(237, 127, 16);")
        vtn.push_Verificado.setText("Sin Estado")
        V_Productos.Carga_Imagen(vtn, Lista_Datos)

    '''
    # Cuando se pulsa una tecla en la ventana
    def keyPressEvent(vtn, event):
        # Capturamos la tecla presionada en formato str
        Valor = event.text()

        # Le permitimos sólo valores indicados para números decimales
        Texto = form.Devuelve_Entero_Signo(Valor)

        # LINE: Cantidad por bulto
        if (vtn.line_Cant_Bulto.hasFocus()):
            # Se ejecuta cuando se apreta para borrar
            if event.key() == Qt.Key_Backspace:
                vtn.LINEVALOR1, AuxString = vtn.Ayuda_Event_Backspace(vtn.LINEVALOR1)
                vtn.line_Cant_Bulto.setText(AuxString)
            elif Texto != 'F':
                vtn.LINEVALOR1 += Texto
                vtn.LINEVALOR1, AuxString = vtn.Ayuda_Event_Ingresan_Valores(vtn.LINEVALOR1)
                vtn.line_Cant_Bulto.setText(AuxString)
    '''
    '''#############################################################################################################################################
    FUNCIONES DE BOTONES  '''

    # Genera la búsqueda de una imagen y luego manda la ruta a otra función que la carga en el label
    def F_Btn_Buscar_Imagen(vtn, Lista_Datos):
        # Abrimos la ventana para que el usuario cargue en el sistema la imagen buscada
        Ruta = ""
        Ruta, _ = QFileDialog.getOpenFileName(vtn, 'Buscar Archivo', QDir.homePath(), "All Files (*.jpg);;All Files (*.png);;All Files (*)")
        V_Productos.Carga_Imagen(vtn, Lista_Datos, Ruta)

    # Cambia del Estado 0 o 1 a 2. Si se puede o no verificar un producto dependerá del momento en que será guardado donde se controlarán todos los datos
    def Btn_Verificado(vtn, Lista_Datos):
        if Lista_Datos[4][11] == 2 and Lista_Datos[1] == False:
            QMessageBox.question(vtn, "Aviso", "No puede modificarse el estado de un producto que ya está VERIFICADO", QMessageBox.Ok)
        else:
            if Lista_Datos[4][11] == 0 or Lista_Datos[4][11] == 1:
                Lista_Datos[4][11] = 2
            else:
                Lista_Datos[4][11] = 1
            V_Productos.Estado_Verificado(vtn, Lista_Datos[4][11])

    # Controla si el grupo de stock anterior contiene una cantidad mayor a cero y un precio, si no se cumplen esas reglas no permite agregar y da aviso
    def Btn_Adiciona_Conjunto(vtn, Lista_Datos):
        aux2 = False
        aux3 = False
        if Lista_Datos[12] == 1:
            # Si hay algún producto en el stock y a la vez tiene al menos un precio de compra, entonces está habilitado a cargar un segundo grupo, de lo contrario es innesesar.
            if Lista_Datos[4][0] > 0 and Lista_Datos[4][6] > 0.0:
                aux2 = True
            else:
                QMessageBox.question(vtn, "Aviso", "No puede agregar un nuevo grupo de Stock si no tiene el 1er grupo con los datos mínimos, su CANTIDAD y PRECIO DE COMPRA.", QMessageBox.Ok)
        if Lista_Datos[12] == 2:
            # Si hay algún producto en el stock y a la vez tiene al menos un precio de compra, entonces está habilitado a cargar un segundo grupo, de lo contrario es innesesar.
            if Lista_Datos[4][0] > 0 and Lista_Datos[4][6] > 0.0:
                if Lista_Datos[4][1] > 0 and Lista_Datos[4][7] > 0.0:
                    aux3 = True
                else:
                    QMessageBox.question(vtn, "Aviso", "No puede agregar un nuevo grupo de Stock si no tiene el 2do grupo con los datos mínimos, su CANTIDAD y PRECIO DE COMPRA.", QMessageBox.Ok)
            else:
                QMessageBox.question(vtn, "Aviso", "No puede agregar un nuevo grupo de Stock si no tiene el 1er y 2do grupo con los datos mínimos, su CANTIDAD y PRECIO DE COMPRA.", QMessageBox.Ok)
        if aux2 == True:
            vtn.groupBox_4.setEnabled(True)
        if aux3 == True:
            vtn.groupBox_5.setEnabled(True)
    
    # Controla si se va a guardar o crear uno nuevo, luego controla si los datos mínimos están correctos y luego guarda
    def Btn_Guardar(vtn, Lista_Datos):
        #True: Hay algún código escrito. False: El line está vacío
        if Lista_Datos[3][1] != "":

            # Existencia es un V_F sobre si existe o no dicho código. Lista, es todos los datos del producto en caso de existir
            Existencia, Lista = mdb.Dev_Info_Producto(Lista_Datos[3][1])

            # Concatenamos las listas de la ventana para su control y comparación
            NuevaL = Lista_Datos[3] + Lista_Datos[4] + Lista_Datos[5]

            # True: Cuando el producto que se está queriendo guardar ya existe en la bd. False: Si es un producto nuevo
            if Existencia == 1:

                if V_Productos.Compara_Listas(vtn, Lista, NuevaL):
                    QMessageBox.question(vtn, "Aviso", "No hay cambios que guardar.", QMessageBox.Ok)
                else:

                    # Consultamos si está seguro de guardar los cambios
                    Rta = QMessageBox.question(vtn, "Guardar Cambios", "¿Desea guardar los CAMBIOS?", QMessageBox.Yes | QMessageBox.No)
                    if Rta == QMessageBox.Yes:
                        V_Productos.Compara_Y_Actualiza(vtn, NuevaL, Lista)
                        V_Productos.Estado_Verificado(vtn)
                        V_Productos.Limpia_Ventana(vtn, Lista_Datos, Inicia_P_Nuevo = False, Mantiene_Cod = False)
            else:
                if Existencia == 2:
                    QMessageBox.question(vtn, "Error", "El código es un CODIGO POR BULTO, que pertenece a un producto.", QMessageBox.Ok)
                else:
                    # Consultamos si está seguro de guardar un producto nuevo
                    Rta = QMessageBox.question(vtn, "Guardar Producto", "¿Desea guardar un PRODUCTO NUEVO?", QMessageBox.Yes | QMessageBox.No)
                    if Rta == QMessageBox.Yes:
                        if vtn.Controla_Datos_Ventana(vtn, Lista_Datos, NuevaL):
                            mdb.Nuevo_Producto(Lista_Datos[3][1:], Lista_Datos[4], Lista_Datos[5], 4)
                            V_Productos.Estado_Verificado(vtn)
                            V_Productos.Limpia_Ventana(vtn, Lista_Datos, Inicia_P_Nuevo = False, Mantiene_Cod = False)
                    else:
                        V_Productos.Limpia_Ventana(vtn, Lista_Datos)
                        V_Productos.Colores_Contornos(vtn)
        else:
            QMessageBox.question(vtn, "Aviso", "No se puede Guardar o Crear Nuevo Producto sin un código.", QMessageBox.Ok)

    # SIN CODIGO, DEBE ELIMINAR EL PRODUCTO QUE SE ESTÁ TRATANDO
    def Btn_Eliminar(vtn):
        V_Productos.Colores_Contornos(vtn)

    # Recorre todos los productos y va cargando en pantalla los que no están verificados
    def Btn_Recorrido_Inicial(vtn, Lista_Datos):
        Cantidad = mdb.Dev_Config("CantPrincipal")
        if Cantidad > 0:
            if Cantidad < vtn.CONT_VER:
                vtn.CONT_VER = 1
            while vtn.CONT_VER <= Cantidad:
                verificado = mdb.Dev_Dato_Int(mi_vs.BASE_DATOS_PPAL, "Stock", "ID", vtn.CONT_VER, "StockVerificado")
                if verificado == 1:
                    codigo = mdb.Dev_Dato_Int(mi_vs.BASE_DATOS_PPAL, "Productos", "ID", vtn.CONT_VER, "Codigo")
                    V_Productos.Limpia_Ventana(vtn, Lista_Datos)
                    vtn.line_Codigo_2.setText(codigo)
                    V_Productos.Carga_Info_Ventana(vtn, Lista_Datos)
                vtn.CONT_VER += 1
        else:
            QMessageBox.question(vtn, "Error", "No hay productos en la base de datos, no se puede realizar el recorrido inicial.", QMessageBox.Ok)

    '''#############################################################################################################################################
    FUNCIONES DE LINEEDIT Y COMBOBOX ORDENADAS SEGÚN LAS ENCONTRAMOS EN LA VENTANA '''
    
    # GROUPBOX PRODUCTO
    # El line de Código ya está incluído en otra función para cuando existe un returnPressed
    
    def F_Line_Codigo_Bulto(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[3][2] = vtn.line_Cod_Bulto.text()
    
    def F_Line_Cantidad_Bulto(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[3][3] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Cant_Bulto)
            Lista_Datos[0] = False
    
    def F_Line_Concepto(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            texto = vtn.line_Concepto.text()
            texto = texto.upper()
            vtn.line_Concepto.setText(texto)
            Lista_Datos[3][4] = texto
            if Lista_Datos[1] == True:
                if Lista_Datos[3][4] != "":
                    V_Productos.Colores_Contornos(vtn, Color = 2, Widget_ = 4)
                else:
                    V_Productos.Colores_Contornos(vtn, Color = 1, Widget_ = 4)
            Lista_Datos[0] = False
    
    def F_Line_Marca(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            texto = vtn.line_Marca.text()
            texto = texto.upper()
            vtn.line_Marca.setText(texto)
            Lista_Datos[3][5] = texto
            if Lista_Datos[1] == True:
                if Lista_Datos[3][5] != "":
                    V_Productos.Colores_Contornos(vtn, Color = 2, Widget_ = 5)
                else:
                    V_Productos.Colores_Contornos(vtn, Color = 1, Widget_ = 5)
            Lista_Datos[0] = False
    
    def F_Combo_Medida(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[3][7] = vtn.combo_Uni_Medida.currentIndex()
            if Lista_Datos[1] == True:
                if Lista_Datos[3][7] > 0:
                    V_Productos.Colores_Contornos(vtn, Color = 2, Widget_ = 6)
                else:
                    V_Productos.Colores_Contornos(vtn, Color = 1, Widget_ = 6)
    
    def F_Line_Detalle(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            texto = vtn.line_Detalle.text()
            #texto = texto.upper()
            #vtn.line_Detalle.setText(texto)
            Lista_Datos[3][6] = texto
            if Lista_Datos[1] == True:
                if Lista_Datos[3][6] != "":
                    V_Productos.Colores_Contornos(vtn, Color = 2, Widget_ = 7)
                else:
                    V_Productos.Colores_Contornos(vtn, Color = 1, Widget_ = 7)
            Lista_Datos[0] = False
    
    # GROUPBOX STOCK
    def Line_Precio_Venta(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[4][10] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Pcio_Venta)
            if Lista_Datos[1] == True:
                if Lista_Datos[4][10] > 0.0:
                    V_Productos.Colores_Contornos(vtn, Color = 2, Widget_ = 10)
                else:
                    V_Productos.Colores_Contornos(vtn, Color = 1, Widget_ = 10)
            Lista_Datos[0] = False

    def Line_Cantidad_1(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[4][0] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Cant_1)
            if Lista_Datos[4][0] == 0.0:
                Lista_Datos[9][1] = False
            else:
                Lista_Datos[9][1] = True
            V_Productos.Suma_Cantidades(vtn, Lista_Datos)
            if Lista_Datos[1] == True:
                if vtn.line_Cant_1.text() != "":
                    V_Productos.Colores_Contornos(vtn, Color = 2, Widget_ = 11)
                else:
                    V_Productos.Colores_Contornos(vtn, Color = 1, Widget_ = 11)
            Lista_Datos[0] = False
    
    def Line_Fecha_Dia_1(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            aux = form.Line_Solo_Num(vtn.line_Vto_1_D.text())
            if len(aux) > 2:
                aux = aux[0:2]
            if len(aux) > 0:
                if int(aux) < 32:
                    vtn.line_Vto_1_D.setText(aux)
                else:
                    QMessageBox.question(vtn, "Error numérico", "No se puede ingresar un día superior a 31", QMessageBox.Ok)
                    vtn.line_Vto_1_D.setText(aux[0])
            else:
                vtn.line_Vto_1_D.setText("")
            V_Productos.Autoriza_Guardar_Fecha(vtn, Lista_Datos, 1)
            Lista_Datos[0] = False
    
    def Line_Fecha_Mes_1(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            aux = form.Line_Solo_Num(vtn.line_Vto_1_M.text())
            if len(aux) > 2:
                aux = aux[0:2]
            if len(aux) > 0:
                if int(aux) < 13:
                    vtn.line_Vto_1_M.setText(aux)
                else:
                    QMessageBox.question(vtn, "Error numérico", "No se puede ingresar un mes superior a 12", QMessageBox.Ok)
                    vtn.line_Vto_1_M.setText(aux[0])
            else:
                vtn.line_Vto_1_M.setText("")
            V_Productos.Autoriza_Guardar_Fecha(vtn, Lista_Datos, 1)
            Lista_Datos[0] = False
    
    def Line_Fecha_Ano_1(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            aux = form.Line_Solo_Num(vtn.line_Vto_1_A.text())
            if len(aux) > 2:
                aux = aux[0:2]
            vtn.line_Vto_1_A.setText(aux)
            V_Productos.Autoriza_Guardar_Fecha(vtn, Lista_Datos, 1)
            Lista_Datos[0] = False
    
    def Line_Precio_Costo_1(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[4][6] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Pcio_Costo_1)
            if Lista_Datos[4][6] == 0.0:
                Lista_Datos[9][3] = False
            else:
                Lista_Datos[9][3] = True
            if Lista_Datos[1] == True:
                if Lista_Datos[4][6] > 0.0:
                    V_Productos.Colores_Contornos(vtn, Color = 2, Widget_ = 15)
                else:
                    V_Productos.Colores_Contornos(vtn, Color = 1, Widget_ = 15)
            Lista_Datos[0] = False   


    def Line_Cantidad_2(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[4][1] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Cant_2)
            if Lista_Datos[4][1] == 0.0:
                Lista_Datos[10][1] = False
            else:
                Lista_Datos[10][1] = True
            V_Productos.Suma_Cantidades(vtn, Lista_Datos)
            Lista_Datos[0] = False
    
    def Line_Fecha_Dia_2(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            aux = form.Line_Solo_Num(vtn.line_Vto_2_D.text())
            if len(aux) > 2:
                aux = aux[0:2]
            if len(aux) > 0:
                if int(aux) < 32:
                    vtn.line_Vto_2_D.setText(aux)
                else:
                    QMessageBox.question(vtn, "Error numérico", "No se puede ingresar un día superior a 31", QMessageBox.Ok)
                    vtn.line_Vto_2_D.setText(aux[0])
            else:
                vtn.line_Vto_2_D.setText("")
            V_Productos.Autoriza_Guardar_Fecha(vtn, Lista_Datos, 2)
            Lista_Datos[0] = False
    
    def Line_Fecha_Mes_2(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            aux = form.Line_Solo_Num(vtn.line_Vto_2_M.text())
            if len(aux) > 2:
                aux = aux[0:2]
            if len(aux) > 0:
                if int(aux) < 13:
                    vtn.line_Vto_2_M.setText(aux)
                else:
                    QMessageBox.question(vtn, "Error numérico", "No se puede ingresar un mes superior a 12", QMessageBox.Ok)
                    vtn.line_Vto_2_M.setText(aux[0])
            else:
                vtn.line_Vto_2_M.setText("")
            V_Productos.Autoriza_Guardar_Fecha(vtn, Lista_Datos, 2)
            Lista_Datos[0] = False
    
    def Line_Fecha_Ano_2(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            aux = form.Line_Solo_Num(vtn.line_Vto_2_A.text())
            if len(aux) > 2:
                aux = aux[0:2]
            vtn.line_Vto_2_A.setText(aux)
            V_Productos.Autoriza_Guardar_Fecha(vtn, Lista_Datos, 2)
            Lista_Datos[0] = False
    
    def Line_Precio_Costo_2(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[4][7] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Pcio_Costo_2)
            if Lista_Datos[4][7] == 0.0:
                Lista_Datos[10][3] = False
            else:
                Lista_Datos[10][3] = True
            Lista_Datos[0] = False   


    def Line_Cantidad_3(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[4][2] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Cant_3)
            if Lista_Datos[4][2] == 0.0:
                Lista_Datos[11][1] = False
            else:
                Lista_Datos[11][1] = True
            V_Productos.Suma_Cantidades(vtn, Lista_Datos)
            Lista_Datos[0] = False
    
    def Line_Fecha_Dia_3(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            aux = form.Line_Solo_Num(vtn.line_Vto_3_D.text())
            if len(aux) > 2:
                aux = aux[0:2]
            if len(aux) > 0:
                if int(aux) < 32:
                    vtn.line_Vto_3_D.setText(aux)
                else:
                    QMessageBox.question(vtn, "Error numérico", "No se puede ingresar un día superior a 31", QMessageBox.Ok)
                    vtn.line_Vto_3_D.setText(aux[0])
            else:
                vtn.line_Vto_3_D.setText("")
            V_Productos.Autoriza_Guardar_Fecha(vtn, Lista_Datos, 3)
            Lista_Datos[0] = False
    
    def Line_Fecha_Mes_3(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            aux = form.Line_Solo_Num(vtn.line_Vto_3_M.text())
            if len(aux) > 2:
                aux = aux[0:2]
            if len(aux) > 0:
                if int(aux) < 13:
                    vtn.line_Vto_3_M.setText(aux)
                else:
                    QMessageBox.question(vtn, "Error numérico", "No se puede ingresar un mes superior a 12", QMessageBox.Ok)
                    vtn.line_Vto_3_M.setText(aux[0])
            else:
                vtn.line_Vto_3_M.setText("")
            V_Productos.Autoriza_Guardar_Fecha(vtn, Lista_Datos, 3)
            Lista_Datos[0] = False
    
    def Line_Fecha_Ano_3(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            aux = form.Line_Solo_Num(vtn.line_Vto_3_A.text())
            if len(aux) > 2:
                aux = aux[0:2]
            vtn.line_Vto_3_A.setText(aux)
            V_Productos.Autoriza_Guardar_Fecha(vtn, Lista_Datos, 3)
            Lista_Datos[0] = False
    
    def Line_Precio_Costo_3(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[4][8] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Pcio_Costo_3)
            if Lista_Datos[4][8] == 0.0:
                Lista_Datos[11][3] = False
            else:
                Lista_Datos[11][3] = True
            Lista_Datos[0] = False   

    # FUNCIONES ADICIONALES AL PANEL DE CONJUNTOS DE CANTIDADES
    # Suma las cantidades y coloca el total tanto en la lista para la db como en el label
    def Suma_Cantidades(vtn, Lista_Datos):
        Lista_Datos[4][9] = Lista_Datos[4][0] + Lista_Datos[4][1] + Lista_Datos[4][2]
        if Lista_Datos[3][7] == 1 or Lista_Datos[3][7] == 3:
            vtn.label_Cant_Total.setText(form.Formato_Unidades(Lista_Datos[4][9], 0))
        else:
            vtn.label_Cant_Total.setText(form.Formato_Unidades(Lista_Datos[4][9], 3))
    # Funciones que se encargar de revisar si los conjuntos que están activos, se pueden o no guardar, Y LOS GUARDA
    def Autoriza_Guardar_Fecha(vtn, Lista_Datos, Conjunto):
        PX = 1
        R = 0
        G = 0
        B = 0
        if Conjunto == 1:
            Dia = vtn.line_Vto_1_D.text()
            Mes = vtn.line_Vto_1_M.text()
            Ano = vtn.line_Vto_1_A.text()
            if Dia != "":
                Dia = int(Dia)
            else:
                Dia = 0
            if Mes != "":
                Mes = int(Mes)
            else:
                Mes = 0
            if Ano != "":
                Ano = int(Ano) + 2000
            else:
                Ano = 0
            if form.Autoriza_Guardar_Fecha_Aux(Dia, Mes, Ano):
                Lista_Datos[9][2] = True
                if Dia > 0:
                    Lista_Datos[4][3] = form.Trans_Fecha_Num(Dia, Mes, Ano)
            else:
                Lista_Datos[9][2] = False
                Lista_Datos[4][3] = 0
                R = 255
                PX = 3
        elif Conjunto == 2:
            Dia = vtn.line_Vto_2_D.text()
            Mes = vtn.line_Vto_2_M.text()
            Ano = vtn.line_Vto_2_A.text()
            if Dia != "":
                Dia = int(Dia)
            else:
                Dia = 0
            if Mes != "":
                Mes = int(Mes)
            else:
                Mes = 0
            if Ano != "":
                Ano = int(Ano) + 2000
            else:
                Ano = 0
            if form.Autoriza_Guardar_Fecha_Aux(Dia, Mes, Ano):
                Lista_Datos[10][2] = True
                if Dia > 0:
                    Lista_Datos[4][4] = form.Trans_Fecha_Num(Dia, Mes, Ano)
            else:
                Lista_Datos[10][2] = False
                Lista_Datos[4][4] = 0
                R = 255
                PX = 3
        elif Conjunto == 3:
            Dia = vtn.line_Vto_3_D.text()
            Mes = vtn.line_Vto_3_M.text()
            Ano = vtn.line_Vto_3_A.text()
            if Dia != "":
                Dia = int(Dia)
            else:
                Dia = 0
            if Mes != "":
                Mes = int(Mes)
            else:
                Mes = 0
            if Ano != "":
                Ano = int(Ano) + 2000
            else:
                Ano = 0
            if form.Autoriza_Guardar_Fecha_Aux(Dia, Mes, Ano):
                Lista_Datos[11][2] = True
                if Dia > 0:
                    Lista_Datos[4][5] = form.Trans_Fecha_Num(Dia, Mes, Ano)
            else:
                Lista_Datos[11][2] = False
                Lista_Datos[4][5] = 0
                R = 255
                PX = 3

        # Le damos el color al borde
        if Conjunto == 1:
            vtn.line_Vto_1_D.setStyleSheet(u"border: {}px solid rgb({},{},{});".format(PX, R,G,B))
            vtn.line_Vto_1_M.setStyleSheet(u"border: {}px solid rgb({},{},{});".format(PX, R,G,B))
            vtn.line_Vto_1_A.setStyleSheet(u"border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        elif Conjunto == 2:
            vtn.line_Vto_2_D.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
            vtn.line_Vto_2_M.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
            vtn.line_Vto_2_A.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        elif Conjunto == 3:
            vtn.line_Vto_3_D.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
            vtn.line_Vto_3_M.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
            vtn.line_Vto_3_A.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))


    # Botón para restar Conjuntos
    def Boton_Restar_Cj(vtn, Lista_Datos):
        if Lista_Datos[11][0] == True:
            cont = 0
            while cont < 4:
                Lista_Datos[11][cont] = False
                cont += 1
            vtn.line_Cant_3.clear()
            vtn.line_Vto_3_D.clear()
            vtn.line_Vto_3_M.clear()
            vtn.line_Vto_3_A.clear()
            vtn.line_Pcio_Costo_3.clear()
            vtn.groupBox_5.setEnabled(False)
            vtn.push_Agregar_Conjunto.setEnabled(True)
        else:
            cont = 0
            while cont < 4:
                Lista_Datos[10][cont] = False
                cont += 1
            vtn.line_Cant_2.clear()
            vtn.line_Vto_2_D.clear()
            vtn.line_Vto_2_M.clear()
            vtn.line_Vto_2_A.clear()
            vtn.line_Pcio_Costo_2.clear()
            vtn.groupBox_4.setEnabled(False)
            vtn.push_Quitar_Conjunto.setEnabled(False)

    # Botón para sumar conjuntos
    def Boton_Sumar_Cj(vtn, Lista_Datos):
        if Lista_Datos[10][0] == True:
            vtn.groupBox_5.setEnabled(True)
            Lista_Datos[11][0] = True
            vtn.push_Agregar_Conjunto.setEnabled(False)
        else:
            vtn.groupBox_4.setEnabled(True)
            Lista_Datos[10][0] = True
            vtn.push_Quitar_Conjunto.setEnabled(True)



    # GROUPBOX ADICIONALES
    def Combo_Caja_Asociada(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[5][0] = vtn.combo_Caja.currentIndex()
            if Lista_Datos[1] == True:
                if Lista_Datos[5][0] > 0:
                    V_Productos.Colores_Contornos(vtn, Color = 2, Widget_ = 26)
                else:
                    V_Productos.Colores_Contornos(vtn, Color = 1, Widget_ = 26)
            Lista_Datos[0] = False
    
    def ComboBox_Mayorista(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[5][1] = vtn.combo_Mayorista.currentIndex()

    def LineEdit_Siniestro(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            #Lista_Datos[5][3] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Siniestro)
            Lista_Datos[0] = False
    
    def LineEdit_Sin_Cobrar(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            #Lista_Datos[5][5] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Sin_Cobrar)
            Lista_Datos[0] = False
    
    def Line_Porc_Incremento(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[5][6] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Incremento)
            Lista_Datos[0] = False
    
    def Line_Cant_Preaviso(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[5][8] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Cant_Preav)
            Lista_Datos[0] = False
    
    def Line_Cant_Maxima(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[5][9] = V_Productos.Form_Line_Num_Dec(vtn, vtn.line_Cant_Max)
            Lista_Datos[0] = False
    
    def Line_Dias_Preaviso(vtn, Lista_Datos):
        if Lista_Datos[0] == False:
            Lista_Datos[0] = True
            Lista_Datos[5][10] = V_Productos.Form_Line_Num_Int(vtn, vtn.line_Dias_Preav)
            Lista_Datos[0] = False
    
    # Formato para line que sólo permite una coma. Recibe el line como "objeto" y devuelve el valor en tipo Float para ser ingresado en la lista para la BD
    def Form_Line_Num_Dec(vtn, objeto):
        # Obtenemos el texto del line
        aux = form.Line_Num_Coma_(objeto.text())
        # Luego de editarlo, lo sobreescribimos
        objeto.setText(aux)
        # Si el line quedó vacío devolvemos un valor de 0.0 para la BD
        if aux == "":
            return 0.0
        # Si se escribió sólo una coma, devolvemos 0.0 pero escribimos en el objeto "0,"
        elif  aux == ",":
            objeto.setText("0,")
            return 0.0
        else:
            # En caso de ser un número completo, lo transformamos al tipo Float que necesita la BD para ser ingresado donde corresponda
            return form.Str_Float(aux)
    
    # Formato para line que no permite decimales. Recibe el line como "objeto" y devuelve el valor en tipo Int para ser ingresado en la lista para la BD
    def Form_Line_Num_Int(vtn, objeto):
        # Obtenemos el texto del line
        aux = form.Line_Solo_Num(objeto.text())
        # Luego de editarlo, lo sobreescribimos
        objeto.setText(aux)
        # Si el line quedó vacío devolvemos un valor de 0.0 para la BD
        if aux == "":
            return 0.0
        else:
            # En caso de ser un número completo, lo transformamos al tipo Float que necesita la BD para ser ingresado donde corresponda
            return form.Str_Float(aux)

    # Funciones que trabajan sobre la apariencia de la ventana
    def Config_Unidad_de_Medida(vtn, Uni_Medida = 1):
        R = 0
        G = 0
        B = 0
        if Uni_Medida == 1:
            R = 255
            G = 255
            B = 255
        elif Uni_Medida == 2:
            R = 200
            G = 230
            B = 230
        vtn.line_Cant_Bulto.setStyleSheet("background: rgb({}, {}, {});".format(R,G,B))
        vtn.line_Detalle.setStyleSheet("background: rgb({}, {}, {});".format(R,G,B))
        vtn.label_Cant_Total.setStyleSheet("background: rgb({}, {}, {});".format(R,G,B))
        vtn.line_Cant_1.setStyleSheet("background: rgb({}, {}, {});".format(R,G,B))
        vtn.line_Cant_2.setStyleSheet("background: rgb({}, {}, {});".format(R,G,B))
        vtn.line_Cant_3.setStyleSheet("background: rgb({}, {}, {});".format(R,G,B))
        #vtn.line_Siniestro.setStyleSheet("background: rgb({}, {}, {});".format(R,G,B))
        #vtn.line_Sin_Cobrar.setStyleSheet("background: rgb({}, {}, {});".format(R,G,B))
        vtn.line_Cant_Preav.setStyleSheet("background: rgb({}, {}, {});".format(R,G,B))

    '''#############################################################################################################################################
    FUNCIONES AUXILIARES  '''

    # Copia lo que vino en la base de datos a las listas de datos que tiene la clase de la ventana
    def Copia_BD_Listas(vtn, Lista_Datos, Lista):
        cont = 0
        while cont < 8:
            Lista_Datos[3][cont] = Lista[cont]
            cont += 1

        while cont < 20:
            Lista_Datos[4][cont - 8] = Lista[cont]
            cont += 1
        
        while cont < 30:
            Lista_Datos[5][cont - 20] = Lista[cont]
            cont += 1

    # Carga la imagen que viene por parámetro. Pero si no viene nada o tiene algún error entonces deja en blanco el labels
    def Carga_Imagen(vtn, Lista_Datos, Ruta = ""):
        if Ruta != "":
            if nv.Dev_Existe_File(Ruta):
                try:
                    imagen = QPixmap(Ruta).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    vtn.label_Imagen_2.setPixmap(imagen)
                    Lista_Datos[5][7] = Ruta
                    return
                except:
                    pass
        vtn.label_Imagen_2.clear()
        vtn.label_Imagen_2.setText("Imagen")

    # Coloca el botón de VERIFICADO en el estado que corresponde
    def Estado_Verificado(vtn, Nro = 0):
        if Nro == 0:
            vtn.push_Verificado.setStyleSheet("background-color: rgb(208, 211, 212);")
            vtn.push_Verificado.setText("Sin Estado")
        elif Nro == 1:
            vtn.push_Verificado.setStyleSheet("background-color: rgb(255, 51, 51);")
            vtn.push_Verificado.setText("Sin Verificar")
        elif Nro == 2:
            vtn.push_Verificado.setStyleSheet("background-color: rgb(0, 153, 0);")
            vtn.push_Verificado.setText("Verificado")
        font = QFont()
        font.setPointSize(16)
        vtn.push_Verificado.setFont(font)

    
    # Muestra o bloquea los conjuntos de cantidades que hay en el stock. Si hay que bloquear un conjunto, primero lo limpia y dsp lo bloquea
    def Estado_Conjuntos(vtn, Lista_Datos):
        if Lista_Datos[12] < 3:
            try:
                vtn.line_Cant_3.clear()
                vtn.line_Vto_3_D.clear()
                vtn.line_Vto_3_M.clear()
                vtn.line_Vto_3_A.clear()
                vtn.line_Pcio_Costo_3.clear()
                vtn.groupBox_5.setEnabled(False)
            except:
                pass
        else:
            vtn.groupBox_5.setEnabled(True)
        if Lista_Datos[12] < 2:
            try:
                vtn.line_Cant_2.clear()
                vtn.line_Vto_2_D.clear()
                vtn.line_Vto_2_M.clear()
                vtn.line_Vto_2_A.clear()
                vtn.line_Pcio_Costo_2.clear()
                vtn.groupBox_4.setEnabled(False)
            except:
                pass
        else:
            vtn.groupBox_4.setEnabled(True)

    # Compara 2 listas de datos, si son iguales devuelve True, de lo contrario False
    def Compara_Listas(vtn, Lista1, Lista2):
        largo = len(Lista1)
        if len(Lista2) != largo:
            return False
        cont = 0
        while cont < largo:
            if Lista1[cont] != Lista2[cont]:
                return False
            cont += 1
        return True

    # Actualiza un producto
        # Llegan 2 listas, la lista que tiene los datos de la ventana y la lista con los datos de la base de datos. Compara cada sección y sólo actualiza la parte que tiene datos
        # nuevos, ya que la base de datos está dividida en 3 partes que se pueden actualizar desde ésta ventana y quizás sea un único dato el que hay que actualizar como por
        # ejemplo el precio de un producto. En ese caso no vamos a actualizar los 30 datos que tenemos del producto sino únicamente la sección que le corresponde.
    def Compara_Y_Actualiza(vtn, Lista_Ventana, Lista_BD):
        if Lista_Ventana[0:8] != Lista_BD[0:8]:
            mdb.Act_Productos_Segun_ID_Por_Lista(Lista_Ventana[0:8])

        if Lista_Ventana[8:20] != Lista_BD[8:20]:
            ListaAux = []
            ListaAux.append(Lista_Ventana[0])
            ListaAux.extend(Lista_Ventana[8:20])
            mdb.Act_Stock_Segun_ID_Por_Lista(ListaAux)

        if Lista_Ventana[20:] != Lista_BD[20:]:
            ListaAux = []
            ListaAux.append(Lista_Ventana[0])
            ListaAux.extend(Lista_Ventana[20:])
            mdb.Act_Adicionales_Segun_ID_Por_Lista(ListaAux)

    # Le llega la lista que contiene todos los datos de la ventana para un producto nuevo, si el mismo tiene todo lo mínimo devuelve true, si falta algún dato importante False.
    def Controla_Datos_Ventana(vtn, Lista_Datos, Lista):
        Control = True
        Guardado_Esp = False
        cant = 0
        Lista_Mensajes = []

        # TABLA PRODUCTOS
        # ID
        if Lista[0] != 0:
            Lista_Mensajes.append("Hay un conflicto con el ID, si es un producto nuevo no debería tener un ID. Su ID es: {}".format(str(Lista[0])))
            Control = False
        # Codigo
        if Lista[1] == "":
            Lista_Mensajes.append("Debe cargar el código del producto.")
            Control = False
        # Codigo por Bulto y Cantidad por Bulto
        if (Lista[2] != "" and Lista[3] == 0.0) or (Lista[2] == "" and Lista[3] != 0.0):
            Lista_Mensajes.append("Falta algún dato. Si no desea cargar el CODIGO de un BULTO y la CANTIDAD que le corresponde, deje ambas casillas en blanco.")
            Control = False
        # Concepto
        if Lista[4] == "":
            Lista_Mensajes.append("Debe cargar el Concepto del producto.")
            Control = False
        # Marca, Unidad de Medida y Detalle
        if Lista[5] == "" or Lista[6] == "" or Lista[7] == 0:
            Lista_Mensajes.append("Advertencia:\n\nSi bien se puede cargar el producto, recuerde que para ser considerado como VERIFICADO debe contener su MARCA, UNIDAD DE MEDIDA y su DETALLE.")

        # TABLA ADICIONALES
        # Caja Asociada
        if Lista[20] == 0:
            cant += 1
            Lista_Mensajes.append("Debe asociar el producto a una Caja.")
            Control = False

        # TABLA STOCK
        # Cantidad 1
        if Lista[8] == "":
            Lista_Mensajes.append("Debe cargar una Cantidad para el producto, sino en stock coloque 0 (cero).")
            if Control == True:
                Guardado_Esp = True
                Control = False
                Lista_Datos[4][0] = 0
        # Precio de Cpa 1
        if Lista[14] == 0.0:
            Lista_Mensajes.append("Debe cargar un Precio de Compra para el producto, no es obligación que sea exacto hasta que no lo convierta a VERIFICADO.")
            if Control == True:
                Guardado_Esp = True
                Control = False
        # Precio de Venta
        if Lista[18] == 0.0:
            Lista_Mensajes.append("Debe cargar su Precio de Venta.")
            if Control == True:
                Guardado_Esp = True
                Control = False
        # Stock Verificado
        if Lista[19] == 0:
            Lista_Datos[4][11] = 1

        if Control == False:
            if Guardado_Esp == True:
                Rta = QMessageBox.question(vtn, "Error", "Al producto le faltan datos importantes para poder utilizarse. Haga clic en SI, para cargarlo de todas maneras, o haga clic en NO para poder editarlo y volver a guardarlo luego.\n\nNota: Haciendo clic en SI, se creará el producto pero no se podrá utilizar al menos hasta que lo guarde con los datos necesarios.", QMessageBox.Yes | QMessageBox.No)
                if Rta == QMessageBox.Yes:
                    Lista_Datos[4][11] = 0
                    Control = True
            else:
                cont = 0
                largo = len(Lista_Mensajes)
                for i in Lista_Mensajes:
                    cont += 1
                    QMessageBox.question(vtn, "Error {} de {}".format(cont, largo), "{}".format(i), QMessageBox.Ok)

        return Control

    # Reincia toda la ventana a cero
    # Inicia_P_Nuevo: parámetro para indicar que estamos limpiando la ventana pero para crear un prod nuevo
    def Limpia_Ventana(matriz, vtn, Lista_Datos, Inicia_P_Nuevo = False, Mantiene_Cod = True):
        # True: Cuando limpiamos para colocar un producto nuevo. False: Cuando limpiamos todo
        if Inicia_P_Nuevo == False:
            # Reiniciamos la bandera que indica que se está creando un producto nuevo
            Lista_Datos[1] = False
            V_Productos.Estado_Verificado(vtn)
            V_Productos.Colores_Contornos(vtn)
            vtn.line_Codigo_2.setFocus()
        else:
            # No es necesario colocar la variable de PNUEVO porque ya se hizo antes
            # Recuperamos los contornos de todos los widgets
            V_Productos.Colores_Contornos(vtn, True, True)
            vtn.line_Cod_Bulto.setFocus()
        # Limpiamos los line edit pero antes obtenemos el código que estaba escrito para volver a escribirlo luego
        auxS = vtn.line_Codigo_2.text()
        for line in matriz.findChildren(QtWidgets.QLineEdit):
            line.clear()
        # Mantenemos el código que estaba escrito
        if Mantiene_Cod == True:
            vtn.line_Codigo_2.setText(auxS)
        # Reiniciamos los comboBox
        vtn.combo_Uni_Medida.setCurrentIndex(0)
        vtn.combo_Caja.setCurrentIndex(0)
        vtn.combo_Mayorista.setCurrentIndex(0)

    # Hay 3 listas donde se cargan los datos de ésta ventana, que corresponden a las 3 tablas principales de la base de datos para los productos (productos, stock y Adicionales)
    # , las listas se reincian con los valores básicos cuando se limpia la ventana o mismo cuando se incia la ventana.
    def Reinicia_Variables_Datos(vtn, Lista_Datos):
        # Variables que contienen los datos del producto en cargado en pantalla, ya sea para uno nuevo que se está creando o para uno que fue buscado
            # Sus valores que cargamos ahora mismo por defecto, dependen del tipo de variable que debe ser cada posición, así en tonces si uno quiere controlar un Path cuyo tipo
            # es de string, realiza la siguiente comparación: if Lista_Datos[3][1] == "":   - Pero en cambio si desea comprobar si el usuario colocó un valor en la
            # cantidad la comparación debe ser de la siguiente manera: if Lista_Datos[4][0] >= 0:    - De ésta manera permitimos que se pueda comprobar los datos cargados
            # según su tipo de variable.
        # Nota: Lista_Datos[3][0] == ID del producto. Luego ninguna lista repite el ID
        # 8 posiciones, la 0 = ID
        Lista_Datos[3] = [0,"","",0.0,"","","",0]
        # 12 posiciones sin ID
        Lista_Datos[4] = [ 0.0, 0.0, 0.0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0]
        # 10 posiciones sin ID
        Lista_Datos[5] = [ 0, 0, 0, 0.0, 0.0, 0.0, 0.0, "", 0.0, 0.0, 0]
        Lista_Datos[12] = 1

    # Remarca o reestablece el contorno de los widgets en pantalla.
    # En caso de que no se especifiquen parámetros, devuelve toda la ventana a lo original
    def Colores_Contornos(vtn, Nuevo_Basico_V_F = False, Color = 0, Widget_ = 0, Reestablece = False):
        
        # Creamos una lista, donde cada posición representa con un boleano cada widget, y con True o False indicamos si vamos a trabajar en él o no 
        cont = 0
        Estados = []
        while cont < 33:
            Estados.append(False)
            cont += 1
        
        # Dependiendo del parámetro que viene en "Color", lo configuramos acá.
        # Adicionalmente configuramos el ancho en pixeles que va a tener dicho contorno, quedando normal en 1px cuando es negro, y 3 cuando tiene otro color
        # NEGRO
        PX = 3
        if Color == 0:
            R = 255
            G = 255
            B = 255
            PX = 1
        # ROJO
        elif Color == 1:
            R = 255
            G = 0
            B = 0
        # VERDE
        elif Color == 2:
            R = 0
            G = 255
            B = 0
            
        # Configuración especial para cuando se crea un producto nuevo, donde marcamos lo que debe rellenarse sí o sí
        if Nuevo_Basico_V_F == True:
            Estados[4] = True
            Estados[5] = True
            Estados[6] = True
            Estados[7] = True
            Estados[10] = True
            Estados[11] = True
            Estados[15] = True
            Estados[26] = True
            PX = 3
        
        # Por si se trabaja sobre un Widget en especial
        if Widget_ > 0:
            Estados[Widget_] = True

        # Sin importar otros parámetros, dejamos la configuración por defecto
        if Reestablece == True:
            cont = 0
            while cont < 33:
                Estados[cont] = True
                cont += 1
            R = 255
            G = 255
            B = 255
            PX = 1

        if Estados[1] == True:
            vtn.line_Codigo_2.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[2] == True:
            vtn.line_Cod_Bulto.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[3] == True:
            vtn.line_Cant_Bulto.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[4] == True:
            vtn.line_Concepto.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[5] == True:
            vtn.line_Marca.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        # COMBOBOX UNIDAD DE MEDIDA
        if Estados[6] == True:
            vtn.combo_Uni_Medida.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[7] == True:
            vtn.line_Detalle.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        # BOTÓN BUSCAR IMAGEN
        if Estados[8] == True:
            vtn.push_Buscar_Imagen.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))

        # BOTÓN VERIFICADO
        if Estados[9] == True:
            vtn.push_Verificado.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[10] == True:
            vtn.line_Pcio_Venta.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[11] == True:
            vtn.line_Cant_1.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[12] == True:
            vtn.line_Vto_1_D.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[13] == True:
            vtn.line_Vto_1_M.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[14] == True:
            vtn.line_Vto_1_A.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[15] == True:
            vtn.line_Pcio_Costo_1.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[16] == True:
            vtn.line_Cant_2.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[17] == True:
            vtn.line_Vto_2_D.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[18] == True:
            vtn.line_Vto_2_M.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[19] == True:
            vtn.line_Vto_2_A.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[20] == True:
            vtn.line_Pcio_Costo_2.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[21] == True:
            vtn.line_Cant_3.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[22] == True:
            vtn.line_Vto_3_D.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[23] == True:
            vtn.line_Vto_3_M.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[24] == True:
            vtn.line_Vto_3_A.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[25] == True:
            vtn.line_Pcio_Costo_3.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))

        # COMBOBOX CAJA ASOCIADA
        if Estados[26] == True:
            vtn.combo_Caja.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        # COMBOBOX PROVEEDOR
        if Estados[27] == True:
            vtn.combo_Mayorista.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        #if Estados[28] == True:
            #vtn.line_Siniestro.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        #if Estados[29] == True:
            #vtn.line_Sin_Cobrar.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[30] == True:
            vtn.line_Incremento.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[31] == True:
            vtn.line_Cant_Preav.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))
        if Estados[32] == True:
            vtn.line_Dias_Preav.setStyleSheet("border: {}px solid rgb({},{},{});".format(PX, R,G,B))






