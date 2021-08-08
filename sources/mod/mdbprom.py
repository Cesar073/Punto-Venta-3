#Biblioteca para conectarse a base de datos SQLite
import sqlite3

import sources.mod.vars as mi_vars

'''
FUNCIONES PARA EL MANEJO DE LA BASE DE DATOS
    Estas funciones abarcan todo lo necesario para obtener un registro de una base de datos, varios registros, borrar, editar o agregar un registro.

FORMA DE NOMBRAR LAS FUNCIONES
    Cuando se piden datos a la base de datos, la primer palabra de la función indica por ejemplo "Reg", que va a devolver un único registro.
    "Regs" que va a devolver varios registros.
    La segunda parte indica la cantidad de parámetros que acepta la función para buscar la coincidencia y devolver el dato.

SENTENCIAS DEL LENGUAJE SQL. Las consultas están expresadas en mayúsculas y en minúsculas las variables que pueden ingresar como parámetro o un 
    formato string de Python.
    Nota: El path de la base de datos se deja establecido en la función ppal "Realiza_Consulta", pero se puede acondicionar para enviarlo mediante parametro.
    
    - Consultar un registro:
        SELECT * FROM tabla WHERE columna = dato_compara
        Ejemplo con .format:    sql = 'SELECT * FROM {} WHERE {} = {}' .format( Tabla, Columna, DatoCoincide)
        Ejemplo con parametros: sql = 'SELECT * FROM ? WHERE ? = ?'
                                Parametros( Tabla, Columna, DatoCoincide)
            Los parametros se pasan en una tupla y deben coincidir la cantidad de parametros con la cantidad de signos ?
            El asterisco indica que va a traer todas las columnas de dicho registro, pero se puede cambiar el asterisco por las columnas que uno quiere recibir.
            Además, si le agregamos al final ORDER BY / ORDER BY DESC, estamos ordenando el resultado de la búsqueda de manera ascendente o descendente respectivamente.
    
    - Insertar un dato nuevo:
        INSERT INTO tabla  VALUES (?, ?, ?) Luego se deben enviar los parametros que en este caso son 3, mediante tupla: Parametros = (Dato1, Dato2, Dato3)
        Ejemplo:
            sql = 'INSERT INTO Productos VALUES(NULL, ?, ?, ?)
            parametros = (Activo, Codigo, Concepto)
    
    - Actualizar un dato:
        "UPDATE tabla SET columna1 = ?, columna2 WHERE columnaX = datoBusqueda"
            Luego se envía el parametro mediante tupla.
'''

'''#############################################################################################################################################
                                                        FUNCIONES DE DE LA BD
#############################################################################################################################################'''

# CREA UN NUEVO REGISTRO, UNA NUEVA PROMO
def Guarda_Promo_Nueva(Codigo, Nombre, Descripcion, Tipo, Productos, Inicio, Fin, Caduca_Fecha, Caduca_Stock, Cant_vnd_ult, Cant_vnd_tot, Gcia_ult, Gcia_tot, Activacion, Monto):
    query = 'INSERT INTO Promos VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    Parametros = (Codigo, Nombre, Descripcion, Tipo, Productos, Inicio, Fin, Caduca_Fecha, Caduca_Stock, Cant_vnd_ult, Cant_vnd_tot, Gcia_ult, Gcia_tot, Activacion, Monto)
    Realiza_consulta(mi_vars.BASE_PROMOS_SEC, query, Parametros)

# BUSCA UN REGISTRO SEGÚN UN CÓDIGO. 
# DEVUELVE 2 VARIABLES:
    # VARIABLE 1:
        # 0 = Cuando no existe el código
        # 1 = Código encontrado
        # 2 = Cod encontrado pero promo desactivada
    # VARIABLE 2: Los datos
def Busca_Cod_Promo(Tabla, Columna, DatoCoincide):
    
    # Buscamos el dato de la lista de códigos principal
    Registro = Reg_Un_param_Str(Tabla, Columna, DatoCoincide)

    # He creado primero la lista row con valores de cero(0), porque no puedo capturar la excepción en caso de que haya un error al no
        # encontrar el código en la base de datos. Entonces, la línea: for posicion in Registro: no se ejecuta cuando el valor del Registro es
        # nulo. Al no ejecutarse, row no se actualiza, por ende, deduzco si se encontró o no el Registro.
    row = [ '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    for posicion in Registro:
        row = [posicion[0], posicion[1], posicion[2], posicion[3], posicion[4], posicion[5], posicion[6], posicion[7], posicion[8], posicion[9], posicion[10], posicion[11], posicion[12], posicion[13], posicion[14], posicion[15]]

    # Con éste if, determino si se han cargado los datos o no.
    # True: NO SE ENCONTRÓ EL CODIGO EN LA BD. False: Ejecución normal
    if row[2] == '0':
        return 0, row
    else:
        if row[14] == 1:
            return 1, row
        else:
            return 2, row

# ACTUALIZA UNA PROMO, NO SE PUEDE MODIFICAR UN CODIGO
def Act_Reg_Promo(Nombre, Descripcion, Tipo, Productos, Inicio, Fin, Caduca_Fecha, Caduca_Stock, Cant_vnd_ult, Cant_vnd_tot, Gcia_ult, Gcia_tot, Activacion, Monto,Codigo):
    query = 'UPDATE Promos SET Nombre = ?, Descripcion = ?, Tipo = ?, Productos = ?, Inicio = ?, Fin = ?, Caduca_Fecha = ?, Caduca_Stock = ?, Cant_vnd_ult = ?, Cant_vnd_tot = ?, Gcia_ult = ?, Gcia_tot = ?, Activacion = ?, Monto = ? WHERE Codigo = ?'
    parameters = (Nombre, Descripcion, Tipo, Productos, Inicio, Fin, Caduca_Fecha, Caduca_Stock, Cant_vnd_ult, Cant_vnd_tot, Gcia_ult, Gcia_tot, Activacion, Monto, Codigo)
    Realiza_consulta(mi_vars.BASE_PROMOS_SEC, query, parameters)

'''#############################################################################################################################################
    FUNCIONES GENERALES Y DE EJEMPLO  '''

# DEVUELVE UN REGISTRO BUSCADO SEGÚN UN DATO EN PARTICULAR ENTERO.
    # Ver explicación de la función "Reg_Un_param_Str"
def Reg_Un_param_Int( Tabla, Columna, DatoCoincide):
    sql = 'SELECT * FROM {} WHERE {} = {}' .format( Tabla, Columna, DatoCoincide)
    Resultado = Realiza_consulta(mi_vars.BASE_PROMOS_PPAL, sql)
    return Resultado

# DEVUELVE UN REGISTRO BUSCADO SEGÚN UN DATO EN PARTICULAR STRING.
    # Nota: Es una función distinta a la anterior debido a que hay que diferenciar con las comillas en el dato de búsqueda (WHERE) cuando se trata de un string ya que de lo
            # contrario, devuelve un error como "no such column" si intentamos buscar con la otra función un dato que es del tipo string.
def Reg_Un_param_Str( Tabla, Columna, DatoCoincide):
    sql = 'SELECT * FROM {} WHERE {} = "{}"' .format( Tabla, Columna, DatoCoincide)
    Resultado = Realiza_consulta(mi_vars.BASE_PROMOS_PPAL, sql)
    return Resultado

# INSERTA UN REGISTRO EN LA BASE DE DATOS
def Reg_Add( Tabla, Activo = 1, Codigo = '', Concepto = '', Marca = ''):
    sql = 'INSERT INTO Productos VALUES(NULL, ?, ?, ?, ?)'
    parametros = (Activo, Codigo, Concepto, Marca)
    Realiza_consulta(mi_vars.BASE_PROMOS_SEC, sql, parametros)

# DEVUELVE LA TABLA COMPLETA QUE SE HAYA SOLICITADO
def Dev_Tabla(Tabla, OrdenBy = ""):
    if OrdenBy == "":
        sql = 'SELECT * FROM {}' .format(Tabla)
    else:
        sql = 'SELECT * FROM {} ORDER BY {}'.format(Tabla, OrdenBy)
    Resultado = Realiza_consulta(mi_vars.BASE_PROMOS_PPAL, sql)
    return Resultado

# ACTUALIZA LA BASE DE DATOS
def Act_Reg( Tabla, ID, Activo, Codigo, Concepto, Marca, Detalle, PrecioCpa, PrecioVta, Cantidad, CodXBulto, CantXBulto, FechaVto, Clasificacion):
    query = 'UPDATE Productos SET Activo = ?, Codigo = ?, Concepto = ?, Marca = ?, Detalle = ?, PrecioCpa = ?, PrecioVta = ?, Cantidad = ?, CodXBulto = ?, CantXBulto = ?, FechaVto = ?, Clasificacion = ? WHERE ID = ?'
    parameters = (Activo, Codigo, Concepto, Marca, Detalle, PrecioCpa, PrecioVta, Cantidad, CodXBulto, CantXBulto, FechaVto, Clasificacion, ID)
    Realiza_consulta(mi_vars.BASE_PROMOS_SEC, query, parameters)


#CONECTA CON LA BD, Y RETORNA LOS DATOS SOLICITADOS
    # Los pasos para trabajar en la bd, son: Conectarse, realizar la consulta, cargarla en una variable y desconectarse
    # query será el parámetro que traiga el tipo de consuta que se desea, y en caso de haber parámetros, se utilizarán, de lo contrario, la tupla 
    # queda vacía
def Realiza_consulta(Base_De_Datos, query, parameters = ()):
    # Realizamos la conección y la almacenamos en la variable conn
    with sqlite3.connect(Base_De_Datos) as conn:
        # Cursor, es una propiedad que nos indica en qué posición estamos dentro de la base de datos, y lo almacenamos en la variable Cur
        Cur = conn.cursor()
        # Execute, es la función que realiza la consulta, y los resultados obtenidos serán almacenados en la variable resultado
        resultado = Cur.execute(query, parameters)
        conn.commit()
    return resultado




