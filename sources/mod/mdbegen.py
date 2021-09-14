'''
MANEJA TODO TIPO DE INTERACCIÓN CON LA BASE DE DATOS DEL ESTADO GENERAL
'''

import sqlite3
import sources.mod.vars as mi_vs

'''#############################################################################################################################################
    TABLA CAJAS  '''

# Actualiza la caja cuando se realiza una venta (Situación e Ingreso Diario), usando como referencia el ID de la caja
def DB_Cajas_Venta_ID(ID, Monto):
    situacion, IngDia = Dev_Datos_P_Venta("ID", ID)
    situacion += Monto
    IngDia += Monto
    sql = 'UPDATE Cajas SET Situacion = {}, IngresoDia = {} WHERE ID = {}'.format(situacion, IngDia, ID)
    Realiza_consulta(mi_vs.BASE_GENERAL_SEC, sql)

# Actualiza la caja cuando se realiza una venta (Situación e Ingreso Diario), usando como referencia el ORDEN de la caja
def DB_Cajas_Venta_Orden(Orden, Monto):
    situacion, IngDia = Dev_Datos_P_Venta("Orden", Orden)
    situacion += Monto
    IngDia += Monto
    sql = 'UPDATE Cajas SET Situacion = {}, IngresoDia = {} WHERE Orden = {}'.format(situacion, IngDia, Orden)
    Realiza_consulta(mi_vs.BASE_GENERAL_SEC, sql)

# Devuelve la cantidad de elementos de una tabla y la cantidad de activos
def DB_Cajas_Totales_Cajas(ID):
    sql = 'SELECT * FROM Totales WHERE ID = {}'.format(ID)
    Registro = Realiza_consulta(mi_vs.BASE_GENERAL_PPAL, sql)
    Total = 0
    Activos = 0
    for i in Registro:
        Total = i[2]
        Activos = i[3]
    return Total, Activos





# Actualiza datos de la tabla "Cajas" según su ID, cuando hay ingresos, ventas
def Act_Cajas_Ingresos_ID(Situacion, IngresoDia, IngresoSem, IngresoMen, IngresoAnu, IngresoTot, ID_):
    sql = 'UPDATE Cajas SET Situacion = {}, IngresoDia = {}, IngresoSem = {}, IngresoMen = {}, IngresoAnu = {}, IngresoTot = {} WHERE ID = {}'.format(Situacion, IngresoDia, IngresoSem, IngresoMen, IngresoAnu, IngresoTot, ID_)
    Realiza_consulta(mi_vs.LIST_BASE_DATOS[0] + "egen.db", sql)

# Actualiza datos de la tabla "Cajas" según su ID, cuando hay ingresos, ventas
def Act_Fondos_Ingresos_ID(Estado, IngresoDia, IngresoSem, IngresoMen, IngresoAnu, IngresoTot, ID_):
    sql = 'UPDATE Fondos SET Estado = {}, Ing_dia = {}, Ing_sem = {}, Ing_mes = {}, Ing_ano = {}, Ing_tot = {} WHERE ID = {}'.format(Estado, IngresoDia, IngresoSem, IngresoMen, IngresoAnu, IngresoTot, ID_)
    Realiza_consulta(mi_vs.LIST_BASE_DATOS[0] + "egen.db", sql)







def Nueva_Caja(ListaProductos, ListaStock, ListaAdicionales, SumaUnidad):
    # Devuelve 0 si se guardó correctamente, devuelve 1 si hubo algún error.

    # Debido a que nuestra intención es poder ir eliminando productos e ir reordenando la tabla por completo según el orden de los códigos, vamos a evitar el modo
    # "Autoincremental" de las tablas. Para eso debemos colocar de manera manual el valor de los ID's. En primer lugar se irán colocando según una correlatividad cargada en el
    # sistema y guardado el último valor en la tabla "Config", y cuando se desee reordenar todo, se volverán a ennumerar a gusto. Ésta es la función encargada de ver cuál es el
    # ID para el nuevo producto.

    # PARAMETROS:
        # Cada lista corresponde a las primeras 3 tablas. No pueden haber datos en la tabla Estadísticas porque es un producto nuevo, no hay estadísticas.
        # SumaUnidad, si vale cero no hace nada. De lo contrario suma una unidad en la tabla "Config", según el número que venga indica una de las siguientes cosas:
            # 1: Suma una unidad al registro de CantPrincipal
            # 2: Suma una unidad al registro de CantAyuda
            # 3: Suma una unidad al registro de CantEliminados
            # 4: Suma una unidad a los registros de CantPrincipal y CantAyuda

    Id_ = Dev_Dato_Int(mi_vs.BASE_DATOS_PPAL, "Config", "ID", 6, "Valor")
    Id_ += 1
    Cant_ = Dev_Dato_Int(mi_vs.BASE_DATOS_PPAL, "Config", "ID", 5, "Valor")
    Cant_ += 1

    try:
        # Variables de la tabla: Productos
        Codigo = ListaProductos[0]
        CodBulto = ListaProductos[1]
        CantBulto = ListaProductos[2]
        Concepto = ListaProductos[3]
        Marca = ListaProductos[4]
        Detalle = ListaProductos[5]
        UnidadMedida = ListaProductos[6]
        Reg_Add_Productos(Id_, Codigo, CodBulto, CantBulto, Concepto, Marca, Detalle, UnidadMedida)

        # Variables de la tabla: Stock
        Cant1 = ListaStock[0]
        Cant2 = ListaStock[1]
        Cant3 = ListaStock[2]
        Vto1 = ListaStock[3]
        Vto2 = ListaStock[4]
        Vto3 = ListaStock[5]
        PcioCpa1 = ListaStock[6]
        PcioCpa2 = ListaStock[7]
        PcioCpa3 = ListaStock[8]
        CantidadTotal = ListaStock[9]
        PcioVta = ListaStock[10]
        StockVerificado = ListaStock[11]
        Reg_Add_Stock(Id_, Cant1, Cant2, Cant3, Vto1, Vto2, Vto3, PcioCpa1, PcioCpa2, PcioCpa3, CantidadTotal, PcioVta, StockVerificado)

        # Variables de la tabla: Adicionales
        CajaAsoc = ListaAdicionales[0]
        Mayorista = ListaAdicionales[1]
        UltFechaVta = ListaAdicionales[2]
        Siniestro = ListaAdicionales[3]
        Sobrante = ListaAdicionales[4]
        SinCobrar = ListaAdicionales[5]
        PorcGeneral = ListaAdicionales[6]
        PathImagen = ListaAdicionales[7]
        CantPreaviso = ListaAdicionales[8]
        DiasPreaviso = ListaAdicionales[9]
        Reg_Add_Adicionales(Id_, CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, PathImagen, CantPreaviso, DiasPreaviso)

        # Variables de la tabla: Estadísticas
        GciaSemanal = 0
        GciaMensual = 0
        GciaAnual = 0
        GciaTotal = 0
        CantVendSem = 0
        CantVendMes = 0
        CantVendAnual = 0
        CantVendTotal = 0
        SiniestrosTotal = 0
        Reg_Add_Estadisticas(Id_, GciaSemanal, GciaMensual, GciaAnual, GciaTotal, CantVendSem, CantVendMes, CantVendAnual, CantVendTotal, SiniestrosTotal)

        if SumaUnidad > 0:
            if SumaUnidad == 1:
                ValorAnt = Dev_Config("CantPrincipal")
                ValorAnt += 1
                Act_Config(ValorAnt, "CantPrincipal")
            elif SumaUnidad == 2:
                ValorAnt = Dev_Config("CantAyuda")
                ValorAnt += 1
                Act_Config(ValorAnt, "CantAyuda")
            elif SumaUnidad == 3:
                ValorAnt = Dev_Config("CantEliminados")
                ValorAnt += 1
                Act_Config(ValorAnt, "CantEliminados")
            elif SumaUnidad == 4:
                ValorAnt = Dev_Config("CantPrincipal")
                ValorAnt += 1
                Act_Config(ValorAnt, "CantPrincipal")
                ValorAnt = Dev_Config("CantAyuda")
                ValorAnt += 1
                Act_Config(ValorAnt, "CantAyuda")
        Id_ = float(Id_)
        Act_Config(Id_, "Ultimo_ID")
        Cant_ = float(Cant_)
        Act_Config(Cant_, "Cant_Productos")    
        return 0
    except:
        return 1

def Reg_Add_Productos(ID, Codigo, CodBulto, CantBulto, Concepto, Marca, Detalle, UnidadMedida):
    sql = 'INSERT INTO Productos VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
    parametros = (ID, Codigo, CodBulto, CantBulto, Concepto, Marca, Detalle, UnidadMedida)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql, parametros)

def Reg_Add_Stock(ID, Cant1, Cant2, Cant3, Vto1, Vto2, Vto3, PcioCpa1, PcioCpa2, PcioCpa3, CantTotal, PcioVta, StockVerificado):
    sql = 'INSERT INTO Stock VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    parametros = (ID, Cant1, Cant2, Cant3, Vto1, Vto2, Vto3, PcioCpa1, PcioCpa2, PcioCpa3, CantTotal, PcioVta, StockVerificado)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql, parametros)

def Reg_Add_Adicionales(ID, CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, PathImagen, CantPreaviso, DiasPreaviso):
    sql = 'INSERT INTO Adicionales VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    parametros = (ID, CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, PathImagen, CantPreaviso, DiasPreaviso)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql, parametros)

def Reg_Add_Estadisticas(ID, GciaSemanal, GciaMensual, GciaAnual, GciaTotal, CantVendSem, CantVendMes, CantVendAnual, CantVendTotal, SiniestrosTotal):
    sql = 'INSERT INTO Estadisticas VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    parametros = (ID, GciaSemanal, GciaMensual, GciaAnual, GciaTotal, CantVendSem, CantVendMes, CantVendAnual, CantVendTotal, SiniestrosTotal)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql, parametros)

'''#############################################################################################################################################
    ACTUALIZA PRODUCTO  '''

# ESTE BLOQUE DE CÓDIGO ESTÁ PREPARADO PERO NO TERMINADO HASTA QUE AL MENOS TENGAMOS LAS INTERFACES ASÍ SABEMOS SI CON ÉSTAS FUNCIONES ALCANZAN O SI SE NECESITAN MÁS.

# Genera que una actualización que viene preparada en una lista, se pueda hacer dividida en variables para la función que está debajo
def Act_Productos_Segun_ID_Por_Lista(Lista):
    Codigo = Lista[1]
    CodBulto = Lista[2]
    CantBulto = Lista[3]
    Concepto = Lista[4]
    Marca = Lista[5]
    Detalle = Lista[6]
    UnidadMedida = Lista[7]
    ID_ = Lista[0]
    Act_Productos_Segun_ID(Codigo, CodBulto, CantBulto, Concepto, Marca, Detalle, UnidadMedida, ID_)
# Actualiza datos de la tabla "Productos" según su ID
def Act_Productos_Segun_ID(Codigo, CodBulto, CantBulto, Concepto, Marca, Detalle, UnidadMedida, ID_):
    sql = 'UPDATE Productos SET Codigo = {}, CodBulto = {}, CantBulto = {}, Concepto = {}, Marca = {}, Detalle = {}, UnidadMedida = {} WHERE ID = {}' .format(Codigo, CodBulto, CantBulto, Concepto, Marca, Detalle, UnidadMedida, ID_)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql)

# Actualiza datos de la tabla "Productos" según su Código
def Act_Productos_Segun_Codigo(CodBulto, CantBulto, Concepto, Marca, Detalle, UnidadMedida, Codigo_):
    sql = 'UPDATE Productos SET CodBulto = {}, CantBulto = {}, Concepto = {}, Marca = {}, Detalle = {}, UnidadMedida = {} WHERE Codigo = {}' .format(CodBulto, CantBulto, Concepto, Marca, Detalle, UnidadMedida, Codigo_)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql)

# Genera que una actualización que viene preparada en una lista, se pueda hacer dividida en variables para la función que está debajo
def Act_Stock_Segun_ID_Por_Lista(Lista):
    Cant1 = Lista[1]
    Cant2 = Lista[2]
    Cant3 = Lista[3]
    Vto1 = Lista[4]
    Vto2 = Lista[5]
    Vto3 = Lista[6]
    PcioCpa1 = Lista[7]
    PcioCpa2 = Lista[8]
    PcioCpa3 = Lista[9]
    CantTotal = Lista[10]
    PcioVta = Lista[11]
    StockVerificado = Lista[12]
    ID_ = Lista[0]
    Act_Stock_Segun_ID(Cant1, Cant2, Cant3, Vto1, Vto2, Vto3, PcioCpa1, PcioCpa2, PcioCpa3, CantTotal, PcioVta, StockVerificado, ID_)
# Actualiza datos de la tabla "Stock" según su ID
def Act_Stock_Segun_ID(Cant1, Cant2, Cant3, Vto1, Vto2, Vto3, PcioCpa1, PcioCpa2, PcioCpa3, CantTotal, PcioVta, StockVerificado, ID_):
    sql = 'UPDATE Stock SET Cant1 = {}, Cant2 = {}, Cant3 = {}, Vto1 = {}, Vto2 = {}, Vto3 = {}, PcioCpa1 = {}, PcioCpa2 = {}, PcioCpa3 = {}, CantTotal = {}, PcioVta = {}, StockVerificado = {} WHERE ID = {}' .format(Cant1, Cant2, Cant3, Vto1, Vto2, Vto3, PcioCpa1, PcioCpa2, PcioCpa3, CantTotal, PcioVta, StockVerificado, ID_)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql)

# Genera que una actualización que viene preparada en una lista, se pueda hacer dividida en variables para la función que está debajo
def Act_Adicionales_Segun_ID_Por_Lista(Lista):
    CajaAsoc = Lista[1]
    Mayorista = Lista[2]
    UltFechaVta = Lista[3]
    Siniestro = Lista[4]
    Sobrante = Lista[5]
    SinCobrar = Lista[6]
    PorcGeneral = Lista[7]
    PathImagen = Lista[8]
    CantPreaviso = Lista[9]
    DiasPreaviso = Lista[10]
    ID_ = Lista[0]
    Act_Adicionales_Segun_ID(CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, PathImagen, CantPreaviso, DiasPreaviso, ID_)
# Actualiza datos de la tabla "Adicionales" según su ID
def Act_Adicionales_Segun_ID(CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, PathImagen, CantPreaviso, DiasPreaviso, ID_):
    sql = 'UPDATE Adicionales SET CajaAsoc = {}, Mayorista = {}, UltFechaVta = {}, Siniestro = {}, Sobrante = {}, SinCobrar = {}, PorcGeneral = {}, PathImagen = {}, CantPreaviso = {}, DiasPreaviso = {} WHERE ID = {}' .format(CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, PathImagen, CantPreaviso, DiasPreaviso, ID_)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql)

# Actualiza datos de la tabla "Estadisticas" según su ID
def Act_Estadisticas_Segun_ID(GciaSemanal, GciaMensual, GciaAnual, GciaTotal, CantVendSem, CantVendMes, CantVendAnual, CantVendTotal, SiniestrosTotal, ID_):
    sql = 'UPDATE Adicionales SET GciaSemanal = {}, GciaMensual = {}, GciaAnual = {}, GciaTotal = {}, CantVendSem = {}, CantVendMes = {}, CantVendAnual = {}, CantVendTotal = {}, SiniestrosTotal = {} WHERE ID = {}' .format(GciaSemanal, GciaMensual, GciaAnual, GciaTotal, CantVendSem, CantVendMes, CantVendAnual, CantVendTotal, SiniestrosTotal, ID_)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql)

'''#############################################################################################################################################
    BUSCA INFORMACIÓN DEL PRODUCTO  '''

# Busca un código, si lo encuentra devuelve una variable con V-F, y otra con la lista de lo que hay en todas las tablas
    # Variables que devuelve:
    # Encontrado = True o False, si se pudo ejecutar todo sin novedad o no.
    # Lista_Datos:    pos0 = ID
                    # pos1 = Codigo
                    # pos2 = Codigo del bulto
                    # pos3 = Cant por bulto
                    # pos4 = Concepto
                    # pos5 = Marca
                    # pos6 = Detalle
                    # pos7 = Unidad de Medida

                    # pos8 = Cant1
                    # pos9 = Cant2
                    # pos10 = Cant3
                    # pos11 = Vto1
                    # pos12 = Vto2
                    # pos13 = Vto3
                    # pos14 = PcioCpa1
                    # pos15 = PcioCpa2
                    # pos16 = PcioCpa3
                    # pos17 = CantTotal
                    # pos18 = PcioVta
                    # pos19 = StockVerificado

                    # pos20 = Caja Asociada
                    # pos21 = Mayorista
                    # pos22 = Ultima Fecha de Venta
                    # pos23 = Siniestro
                    # pos24 = Sobrante
                    # pos25 = Sin Cobrar
                    # pos26 = Porcentaje General (Incremento)
                    # pos27 = Path Imagen
                    # pos28 = Cantidad de stock de Preaviso
                    # pos29 = Días de Preaviso
def Dev_Info_Producto(Codigo):
    Encontrado = False
    Lista_Datos = []
    try:
        # Tabla: Productos
        Reg = Reg_Un_param(mi_vs.BASE_DATOS_PPAL, "Productos", "Codigo", Codigo)
        for i in Reg:
            Lista_Datos.append(i[0])
            Lista_Datos.append(i[1])
            Lista_Datos.append(i[2])
            Lista_Datos.append(i[3])
            Lista_Datos.append(i[4])
            Lista_Datos.append(i[5])
            Lista_Datos.append(i[6])
            Lista_Datos.append(i[7])
        Id_ = Lista_Datos[0]
        
        # Tabla: Stock
        Reg = Reg_Un_param(mi_vs.BASE_DATOS_PPAL, "Stock", "ID", Id_)
        for i in Reg:
            Lista_Datos.append(i[1])
            Lista_Datos.append(i[2])
            Lista_Datos.append(i[3])
            Lista_Datos.append(i[4])
            Lista_Datos.append(i[5])
            Lista_Datos.append(i[6])
            Lista_Datos.append(i[7])
            Lista_Datos.append(i[8])
            Lista_Datos.append(i[9])
            Lista_Datos.append(i[10])
            Lista_Datos.append(i[11])
            Lista_Datos.append(i[12])
        
        # Tabla: Adicionales
        Reg = Reg_Un_param(mi_vs.BASE_DATOS_PPAL, "Adicionales", "ID", Id_)
        for i in Reg:
            Lista_Datos.append(i[1])
            Lista_Datos.append(i[2])
            Lista_Datos.append(i[3])
            Lista_Datos.append(i[4])
            Lista_Datos.append(i[5])
            Lista_Datos.append(i[6])
            Lista_Datos.append(i[7])
            Lista_Datos.append(i[8])
            Lista_Datos.append(i[9])
            Lista_Datos.append(i[10])

        Encontrado = True
    except:
        pass
    return Encontrado, Lista_Datos


'''#############################################################################################################################################
    ELIMINA PRODUCTO  '''

'''#############################################################################################################################################
    FUNCIONES AUXILIARES  '''

# Devuelve el Valor solicitado del registro indicado en "DatoTexto", donde "Valor" es una columna del tipo float y "Nombre" es un texto en la tabla.
def Dev_Config(DatoTexto):
    sql = "SELECT Valor FROM Config WHERE Nombre = '{}'" .format(DatoTexto)
    Resultado = Realiza_consulta("./source/db/prod.db",sql)
    aux = 0
    for res in Resultado:
        aux = res[0] 
    return float(aux)

# Actualiza cualquier valor de la tabla "Config"
def Act_Config(Valor, Nombre):
    sql = "UPDATE Config SET Valor = {} WHERE Nombre = '{}'" .format(Valor, Nombre)
    Realiza_consulta("./source/db/prod.db", sql)

'''#############################################################################################################################################
    EJECUCIÓN  '''
# FUNCIÓN BASE DE ACTUALIZACIÓN CUANDO LA COMPARACIÓN ES NUMÉRICA
def Act_Valor_Num(Tabla, Col_Actualiza, Valor_Actualiza, Col_Compara, Valor_Compara):
    sql = 'UPDATE {} SET {} = {} WHERE {} = {}'.format(Tabla, Col_Actualiza, Valor_Actualiza, Col_Compara, Valor_Compara)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql)

# FUNCIÓN BASE DE ACTUALIZACIÓN CUANDO LA COMPARACIÓN ES TEXTO
def Act_Valor_Texto(Tabla, Col_Actualiza, Valor_Actualiza, Col_Compara, Texto_Compara):
    sql = "UPDATE {} SET {} = {} WHERE {} = '{}'".format(Tabla, Col_Actualiza, Valor_Actualiza, Col_Compara, Texto_Compara)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql)

#CONECTA CON LA BD, REALIZA LA CONSULTA Y GUARDA LOS CAMBIOS
    # Los pasos para trabajar en la bd, son: Conectarse, realizar la consulta, cargarla en una variable y desconectarse
    # query será el parámetro que traiga el tipo de consuta que se desea, y en caso de haber parámetros, se utilizarán, de lo contrario, la tupla queda vacía
def Realiza_consulta( BaseDeDatos, query, parameters = ()):
    db_nombre = BaseDeDatos
    # Realizamos la conección y la almacenamos en la variable conn
    with sqlite3.connect(db_nombre) as conn:
        # Cursor, es una propiedad que nos indica en qué posición estamos dentro de la base de datos, y lo almacenamos en la variable Cur
        Cur = conn.cursor()
        # Execute, es la función que realiza la consulta, y los resultados obtenidos serán almacenados en la variable resultado
        resultado = Cur.execute(query, parameters)
        conn.commit()
    return resultado

'''#############################################################################################################################################
    AYUDAS  '''

# Devuelve los valores de la situación actual y el ingreso diario de la Caja indicada por parámetro
def Dev_Datos_P_Venta(Parametro, ID):
    sql = 'SELECT * FROM Cajas WHERE {} = {}'.format(Parametro, ID)
    Registro = Realiza_consulta(mi_vs.BASE_GENERAL_PPAL, sql)
    situacion = 0
    ingDia = 0
    for i in Registro:
        situacion = i[3]
        ingDia = i[4]
    return situacion, ingDia

# DEVUELVE LA TABLA COMPLETA QUE SE HAYA SOLICITADO
def Dev_Tabla(BaseDeDatos, Tabla, OrdenBy = ""):
    if OrdenBy == "":
        sql = 'SELECT * FROM {}' .format(Tabla)
    else:
        sql = 'SELECT * FROM {} ORDER BY {}'.format(Tabla, OrdenBy)
    Resultado = Realiza_consulta(BaseDeDatos, sql)
    return Resultado

# DEVUELVE EN FORMA DE LISTA UNA COLUMNA DE UNA TABLA
    # La columna se debe indicar con un número entero siendo 0 el primero
def Dev_Columna_Lista(Tabla, Colum_Int):
    Tabla = Dev_Tabla(mi_vs.BASE_GENERAL_SEC, Tabla)
    Lista = []
    for reg in Tabla:
        Lista.append(reg[Colum_Int])
    return Lista

# DEVUELVE UN REGISTRO BUSCADO SEGÚN UN DATO EN PARTICULAR
def Reg_Un_param(BaseDeDatos, Tabla, Columna, DatoCoincide):
    sql = "SELECT * FROM {} WHERE {} = '{}'" .format( Tabla, Columna, DatoCoincide)
    Resultado = Realiza_consulta(BaseDeDatos,sql)
    return Resultado










# Devuelve la tabla solicitada de la base de datos de clientes
def Dev_Tabla_Clie(Tabla):
    return Dev_Tabla("./db\\clie.db", Tabla)

# Devuelve el total de registros de la tabla solicitada de la base de datos de clientes
def Dev_Total_Tabla_Clie(Tabla):
    reg = Reg_Un_param("./db\\clie.db", "sqlite_sequence", "name", Tabla)
    valor = 0
    for i in reg:
        valor = i[1]
    return valor

def Dev_ID_ClienteTexto(Tabla, ColumnaCompara, DatoTexto):
    sql = "SELECT ID FROM {} WHERE {} = '{}'" .format(Tabla, ColumnaCompara, DatoTexto)
    Resultado = Realiza_consulta("./db\\clie.db",sql)
    aux = 0
    for res in Resultado:
        aux = res[0] 
    return int(aux)

# Devuelve un dato solicitado cuando el valor de comparación es un entero
def Dev_Dato_Int(BaseDeDatos, Tabla, ColumnaCompara, DatoCompara, ColumnaDevuelve):
    sql = 'SELECT {} FROM {} WHERE {} = {}'.format(ColumnaDevuelve, Tabla, ColumnaCompara, DatoCompara)
    Result = Realiza_consulta(BaseDeDatos, sql)
    return Result

# INSERTA UN REGISTRO EN LA BASE DE DATOS
def Reg_Add2(BaseDeDatos, Activo, Codigo, Linea, Tipo, Interior, Repuesto, ConceptoBazar, ConceptoAyVta, PedidosEsp, Otros,Tamanio, Litros, PcioCosto, Costo10, PSPV, PcioLista, Puntos, PuntosMG, Comentarios, Imagen, Actualizado):
    sql = 'INSERT INTO Productos VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    parametros = (Activo, Codigo, Linea, Tipo, Interior, Repuesto, ConceptoBazar, ConceptoAyVta, PedidosEsp, Otros,Tamanio, Litros, PcioCosto, Costo10, PSPV, PcioLista, Puntos, PuntosMG, Comentarios, Imagen, Actualizado)
    Realiza_consulta(BaseDeDatos, sql, parametros)

# Actualiza la tabla "Config", sirve para actualizar todos los totales de "Registros" que hay en cada una de las tablas
def Act_Reg_Cant(BaseDeDatos, Cantidad, NomTabla):
    query = 'UPDATE Config SET Registros = ? WHERE Tabla = ?'
    parameters = (Cantidad, NomTabla)
    Realiza_consulta(BaseDeDatos, query, parameters)


