'''
RESUMEN:
    Este módulo realiza la búsqueda de archivos en red y mantiene las bases de datos actualizadas según la App ppal. Siempre trabajará en 2do plano sin iterferir en la actividad principal del programa en ejecución, que en la mayoría de los casos serían PCs de punto de venta.

MODO DE TRABAJO:
    Existen dos tipos de equipos, los puntos de venta y las PC principales. Los puntos de venta siempre intentarán utilizar la base de datos ppal para realizar todas las interacciones con las bases de datos y así evitamos el uso de la tarjeta SD del raspberry al máximo. Al mismo tiempo se podrán configurar para que no se realice de ésta manera en el caso de que contemos con una única PC o bien no estemos trabajando con RPi. Cuando no contemos con conexión a las DBs, vamos a usar la local, por ende, siempre que se encuentre algún tipo de actualización en la red, será aplicada.
    
    En cada PC hay que registrar cuáles son las otras PC y sus Path de DBs.
    Cuando haya alguna actualización por ejemplo de un precio, lo que se realizará es que en la PC que se origina el cambio se deja una db con el nombre de la PC y un código único por PC, que no es más que un número incremental que va a identificar la actualización del resto que tienen las demás. Dicho código estará compuesto por sus 6 primeros caracteres que indican la fecha y luego un identificatorio por día, así entonces si hubiesen millones de actualizaciones en 10 años el nombre no sería tan afectado (ej: PC1210914_1.db). Adicionalmente contará con una db que contendrá el nombre de cada actualización, la fecha y hora en que se generó, y una columna para cada PC, para que pueda informar el estado.
    Entonces, al generarse el cambio en una PC, en su carpeta pública se mostrarán esos datos, las demás PCs lo veerán y realizarán los siguientes pasos:
        - Observar periódicamente la carpeta de cada PC en la red.
        - Observar en la db si hay alguna actualización que no se haya incorporado, eso lo sabremos porque encontraremos en la columna que pertenece a cada PC un msj que dirá "Nueva actualización", y el mismo corresponderá al registro que indica el nombre de la actualización a implementar.
        - Luego, las demás PCs de la red, copian la db con los cambios, pero al momento de actualizarlos compara la fecha y hora de la nueva actualización, con la fecha y hora de la última actualización que tuvo cada producto, evitando así el caso de que hubieran más de una computadora cargando actualizaciones, y que las PCs mezclen los valores y sólo se permitirá el más reciente.
        - Terminada la actualización se sobreescribe en la db de la PC origen, en el campo que decía "Nueva actualización", con msjs como "Actualizado" o "Parcialmente Actualizado", el cuál éste último estaría indicando que uno o más productos ya estaban con actualizaciones más recientes y que no todos fueron actualizados con esa db.
    
    Se agrega también que una columna se encargará de indicar el tipo de actividad a realizar, por ejemplo, actualizar los datos de un producto, de otras db, o bien, reemplazar completamente una nueva db.
    Al mismo tiempo contaremos con una copia local que se intentará manter siempre actualizada, para casos de desconexión con las bases de datos en red.

    Este módulo contiene una lista (lista_scan) que se debe rellenar desde la app ppal con los path de las PCs autorizadas a realizar actualizaciones. Luego sólo se necesita llamar a una función de éste mismo módulo que se encargará de recorrer todo, informar si hubieron actualizaciones, el estado de las conexiones y si hay datos para actualizar los devuelve, si hay que reemplazar completamente una DB envía los datos necesarios como ser el Path de la misma.
'''
import sqlite3
from datetime import datetime as dt

# Esta lista debe contener los path unicamente de las PCs que se van a utlizar para cargar actualizaciones, que pueden ser hasta 5 PCs.
# Se carga con el inicio del programa y puede actualizarse en la ventana de CONFIGURACIÓN.
lista_scan = []

# Función decoradora
def conexion_db(sql):
    '''
    FUNCIÓN DECORADORA DE CONEXIÓN CON DB SQLITE3.
    Debe ser llamada desde una función que proporcione 3 parámetros, el path de la db, la consulta (query), y los parámetros si es que se usan.

    Intenta conectarse con las bases de datos indicada por parámetro y devuelve 2 valores:
    1: True/False si pudo o no conectarse.
    2: Resultado de la consulta.
    En el caso de que no se haya podido conectar con ninguna base de datos, devolverá False, el total de DBs recorridas y un string vacío.'''
    def conexion(*args):
        db, query, parameters = sql(*args)
        try:
            with sqlite3.connect(db) as conn:
                Cur = conn.cursor()
                result = Cur.execute(query, parameters)
                conn.commit()
            return True, result
        except:
            return False, ""
    return conexion

@conexion_db
def tableActualizaciones(db):
    '''Busca en orden según jerarquías, las carpetas que deberían tener archivos destinados a éste punto de venta, ya que en los mismos se deberían encontrar archivos con un identificador para cada punto.'''
    sql = "SELECT * FROM Actualizaciones"
    return db, sql, ()

@conexion_db
def updatePrice(db):
    '''Devuelve la tabla con los datos para actualizar los precios.'''
    sql = "SELECT * FROM upd_price"
    return db, sql, ()

@conexion_db
def setUpdate(name_PC, name_Upd, state, db):
    '''Indica en la DB que registra todas las actualizaciones que la PC que llama a ésta función ha realizado la misma.'''
    sql = "UPDATE Actualizaciones SET {} = {} WHERE db = {}".format(name_PC, state, name_Upd)
    return db, sql, ()

def scanActualizaciones(pc):
    '''Escanea la red para ver si hay actualizaciones en las DBs. Si encuentra alguna o varias devuelve las siguientes listas:
    NOTA: Tener en cuenta que por cada posición en las listas que devuelve, se hace referencia a los resultados de cada uno de los path que tenemos en la lista_scan, siendo que habrán tantas posiciones como actualizaciones pendientes, por ejemplo: si tenemos 2 PCs registradas y hay en PC1 3 actualizaciones tendríamos 4 resultados, donde los 3 primeros responden a las 3 actualizaciones que hay que hacer tomando los datos de la PC1 y el 4to dato es el aviso de la PC2 que quizás no pudo conectarse porque está apagada o bien no tiene actualizaciones pendientes.
    1: [] True/False si se pudo realizar la búsqueda.
    2: [] Path controlado según ubicación en la lista_scan.
    3: [] Acción a realizar.
    4: [] Nombre de la base de datos a trabajar.
    5: [] Acción a realizar, como una actualización, reemplazar una db, etc...
    6: [] Fecha y hora de la creación de dicha actualización.
    
    El parámetro pc debe ser el nombre de la terminal que está realizando la consulta pudiendo ser PC1 a PC5, o bien desde la CAJA1 a CAJA5.'''
    
    # Listas que se devolverán en el return, donde están relacionadas entre sí correspondiendo cada posición de la misma a los resultados de las búsquedas realizadas con los path indicados en lista_scan
    scan_ = []
    path_ = []
    update_ = []
    db_name_ = []
    action_ = []
    date_ = []

    # Determinamos la columna que le corresponde a la PC que está realizando la consulta
    col = 0
    if pc[0:2] == "PC":
        col = 3 + int(pc[2])
    else:
        col = 8 + int(pc[4])

    # Realizamos la consulta en cada uno de los path dentro de la lista
    for db in lista_scan:
        base = db + "\config.db"
        ok, tabla = tableActualizaciones(base)

        # Si pudo hacerse la consulta, controlamos si hay actualizaciones
        if ok:

            # Bandera para dar aviso que se han revisado pero no se han encontrado actualizaciones
            find_ = False

            # Recorremos la tabla para ver si tenemos que realizar alguna acción, de ser así retornamos los datos necesarios para tal fin
            for i in tabla:
                if i[col] == "No actualizado":
                    scan_.append(True)
                    path_.append(db)
                    update_.append(True)
                    db_name_.append(i[1])
                    action_.append(i[3])
                    date_.append(i[2])
                    find_ = True
            
            # Cuando no hay actualizaciones pendientes
            if find_ == False:
                scan_.append(True)
                path_.append(db)
                update_.append(False)
                db_name_.append("")
                action_.append("")
                date_.append("")

        else:
            # Si no se pudo realizar la consulta lo retornamos
            scan_.append(False)
            path_.append(db)
            update_.append(False)
            db_name_.append("")
            action_.append("")
            date_.append("")
    
    return scan_, path_, update_, db_name_, action_, date_

def consultaActualizaciones(name_PC):
    '''Es la función que deben llamar desde fuera que se encarga de realizar toda la actividad.
    name_PC: Nombre de la PC que llama a la función pudiendo ser por ejemplo: CAJA1.
    Devuelve una lista, con listas dentro que cada una representa tanto una conexión como también una actualización. (ver función)
    '''

    # Es la lista que devolvemos con todos los datos necesarios para actualizaciones.
    list_update = []

    # Obtenemos los datos de la DB que da aviso de las actualizaciones
    scan_, path_, update_, db_name_, action_, date_ = scanActualizaciones(name_PC)

    # Preparamos y ejecutamos el bucle que prepara la información a entregar según las actualizaciones que hayan que realizar
    largo = len(scan_)
    for i in range(largo):

        # Primero controlamos si pudieron realizarse escaneos correctamente para dar aviso de los mismos
        if scan_[i] == True:

            # Cuando tenemos una actualización
            if update_[i] == True:

                # Creamos una lista que va a contener desde 2 datos hasta 4 dependiendo el caso, luego se adiciona a la lista que se retorna en la función:
                    # 0: T/F. Indica si el scan se hizo sin problemas. False sería cuándo no se pudo dar con la PC por desconexión o similar.
                    # 1: Acción: Indicamos por medio de un str que hay que hacer siendo opciones como: no_change, upd_price, replace, etc.
                    # 2: Datos: En caso de que haya una acción que requiera datos, se envían aquí como los precios y códigos de una act. o los path para reemplazar una db.
                    # 3: Date: En el caso de la actualización de precios que debemos contar con la variable de su fecha, lo agregamos.
                    # 4: Url: Url de la db.
                    # 5: NameDb: Es el nombre de la base de datos que usamos para actualizar.
                list_aux = []

                # Cuando se actualiza un precio
                if action_[i] == "upd_price":
                    Url = path_[i] + "/" + db_name_[i] + ".db"
                    ok, table = updatePrice(Url)
                    if ok:
                        list_aux.append(True)
                        list_aux.append("upd_price")
                        list_aux2 = []
                        cont = 0
                        for reg in table:
                            cont += 1
                            # El registro contiene: ID - Codigo - Concepto - Precio de Venta. Sólo guardamos el Código y el PCio Vta desde la db, pero agregamos el date_
                            list_aux2.append([reg[1], reg[3]])
                        list_aux.append(list_aux2)
                        list_aux.append(return_value(date_[i],3))
                        list_aux.append(Url)
                        list_aux.append(db_name_[i])

                        if cont > 99:
                            list_update.append(list_aux)
                            return list_update
                    else:
                        list_aux.append(True)
                        list_aux.append("no_change")
                        list_update.append(list_aux)
                
                # Cuando se debe reemplazar la prod.db
                if action_[i] == "replace_prod":
                    list_aux.append(True)
                    list_aux.append("replace_prod")
                    list_aux.append([return_value(path_[i], 3), return_value(db_name_[i], 3)])
                    list_aux.append(db_name_[i])
                    list_update.append(list_aux)
            else:
                list_update.append([True, "no_change"])
        else:
            # En caso de que no se haya podido escanear, se devuelve esta info pero como dato adicional avisamos cuál es el path con esa desconexión
            list_update.append([False, "no_connect", return_value(path_[i],3)])
    return list_update

def return_value(valor, tipo):
    '''Debido a que no puedo encontrar la manera en que Python trabaje dentro de un bucle y su iterador se comporte como uno de otro lenguaje, la manera de solucionarlo es cuando mando los datos a una nueva función y me retorna el valor, lo que genera algo así como un pasaje por valor y no por referencia solucionando el problema.
    Debe llegar el valor a procesar y si además tenemos que cambiar su estado como por ejemplo devolver en formato str a un int, ya lo realizamos.'''
    if tipo == 1:
        return int(valor)
    elif tipo == 2:
        return float(valor)
    elif tipo == 3:
        return str(valor)


def prueba_caja():
    for i in range(2,6):
        print(i)
#prueba_caja()
print(dt.now())
