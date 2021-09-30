'''
POSIBLES ERRORES DE SQLITE 3
    "No such column". A veces cuando tratamos de introducir un valor o actualizar con .format, es necesario que las columnas que sean de tipo texto, tengan sus corchetes de 
    parámetros entre otras comillas.

MANEJA TODO TIPO DE INTERACCIÓN CON LA BASE DE DATOS DE LOS PRODCUTOS.

    El programa cuenta con 3 bases de datos destinadas a los productos. La primera contiene un apoyo para el inicio del sistema en un negocio, donde obtenemos los datos de 
    todos los productos y se los facilitamos al dueño para la carga incial de datos explicada más adelante. Luego la base de datos normal de uso cotidiano, y por último la base 
    de datos de eliminados, que es un respaldo de los productos que se dejaron de vender.
    ayuda.db - prod.db - elim.db

    Debido a que dichas base de datos es compleja, dedicamos un módulo exclusivo a su manejo.
    Posee 4 tablas separadas de la siguiente manera:
    
    Tabla: Productos:
    Datos exclusivos de cada producto que nunca varían.
        ID.
        Codigo. Integer
        CodBulto: Es el código que contiene los paquetes cerrados que suelen venir desde el mayorista.
        CantBulto: Es la cantidad que poseen esos paquetes cerrados.
        Concepto.
        Marca.
        Detalle.
        UnidadMedida: Se indica con un Integer, si es un producto que se vende por cantidad, peso, litro o cm3
    
    Tabla: Stock:
    Ésta tabla permite hast 3 diferencias entre un mismo producto en sus datos de compra. Por ej, se pueden tener 5 unidades de una mayonesa que fueron adquiridas a un precio
    de compra, mientras que también podemos tener otras 15 nuevas unidades a otro precio, por ende la venta de las mismas generan diferentes ganancias. Al mismo tiempo puede
    que esas 5 unidades mas viejas contengan una fecha de de vto mientras que las otras 15 tener otra fecha. Por cualquiera de las 2 diferencias se genera un nuevo stock 
    permitiendo hasta 3 por producto.
    Debemo entender que las unidades se van restando por cada venta en función a la fecha de vto, es decir, que el programa no sabe qué producto se vendió pero se resta siempre
    el que vence más pronto.
    Y por último con respecto a los 3 registros de stock, la cantidad1 (Cant1) corresponde a la misma fecha de vencimiento (Vto1) y al precio de compra (PcioCpa1) y así con los
    demás datos.
        ID.
        Cant1.
        Cant2.
        Cant3.
        Vto1.
        Vto2.
        Vto3.
        PcioCpa1.
        PcioCpa2.
        PcioCpa3.
        CantTotal.
        PcioVta.
        StockVerificado: Éste ítem debería ser True o False, pero no me funciona correctamente en la db por eso uso enteros siendo 1 y 2 sus valores. Me reservo el valor de 0
                            debido a que en la programación lo utilizo para indicar cuando no hay estado que colocar al botón, como por ejemplo cuando se limpia toda la vtn.
                            0 = Nada - 1 = NO VERIFICADO - 2 = VERIFICADOS

        Explicación del uso del ítem "StockVerificado":
        Cuando un negocio incorpora por primera vez el programa, debería realizar una carga completa de todos los datos existentes, ya sea de productos, cantidad en stock como de
        precios de cada uno. Éste programa no funcionaría correctamente hasta que se hayan cargado todos los datos de todos los productos lo cuál es una tarea muy exigente en cuanto a tiempo y uso de personal, cuya actividad debería ser ejecutada completamente durante un momento cerrado del negocio. Puesto que si no se terminan de cargar todos los stock de cada producto y el programa comienza a ejecutarse no contará con todos los productos cargados y puede llegar a tener problemas al vender porque no le arrojaría los datos de algún producto, y si no se utiliza el programa y luego abre el negocio los datos que se hallan cargado de stock van a estar erróneos a medida que se vaya vendiendo la mercadería porque se irían modificando sus cantidades pero en el programa no estarían actualizados.

        Al mismo tiempo al momento de cargar los datos de los productos por primera vez, se deben colocar los valores de costo y precio de venta, importantes para el inicio del sistema. Lo que vamos a evitar es que el dueño o encargado deba buscar todos los datos de las facturas si es que cuenta con ellas, para cargar el precio de costo de la mercadería que tiene. Entonces por el momento puede ir inventando o cargando según lo que crea que cuestan para calcular un estimativo de todas las estadísticas. Luego, una vez que reponga la mercadería y tenga una factura con sus precios de costos actualizados, puede llenar el valor exacto de costo, al igual que el stock y ahí sí dar por hecho que el producto está VERIFICADO.

        Por ello existe éste ítem (SockVerificado), donde todos los productos incian en el negocio con una cantidad exagerada (1.000) y el valor de StockVerificado es de 0. Cuando dicho stock es controlado por el dueño y cargado correctamente su precio de costo, puede configurarlo como VERIFICADO y a partir de ése momento se pueda controlar el stock existente y contar con un dato de ganancias y estadísticas exactos. Hasta que dicho producto no sea considerado como VERIFICADO, no se puede contar con toda la información que le compete.

        IMPORTANTE: UNA VEZ INDICADO COMO VERIFICADO (1), NO PUEDE VOLVERSE MÁS PARA ATRÁS
        
        De éste modo lo que debe realizar con urgencia el Dueño antes de iniciar el uso de la aplicación son:
            * Carga de los Mayoristas para facilitar luego la carga de los productos.
            * La carga de códigos y detalles de los productos existentes debido a que no todos los productos van a estar en la db.
            * Carga de sus precios de venta.
            * Carga de sus precios de compra. Éste dato no debe ser necesariamente exacto, pero afecta de manera directa en la ganancia y otras estadísticas.

    Tabla: Adicionales:
    Datos para estadísticas y de ayuda para la configuración y ejecución del programa.
        ID.
        CajaAsoc: Es la caja de donde se retiran fondos para la compra del producto, al mismo tiempo que de éste producto sus ganancias van a esa misma caja.
        Mayorista: Índice de la tabla de Mayoristas. Si su valor igual o mayor que 1, indica el índice del mayorista en su tabla, pero si es 0, es porque el producto no está
            ligado directamente a un mayorista sino que es un producto que se puede conseguir en varios lugares y se lo compra donde esté más barato.
        UltFechaVta: Indica la fecha en que se vendió por útlima vez el producto.
        Siniestro: Si sufrimos robos o pérdidas ya sea por vencimientos o roturas, se cargan acá para ser discriminados.
        Sobrante: No debería ocurrir, pero si tenemos más stock de lo que deberíamos, algún error ocurrió y se deja asentado en éste ítem la cantidad de sobrantes que acumula.
        SinCobrar: Productos fiados.
        PorcGeneral: Si el valor es 0.0, quiere decir que cada vez que se realiza el recargo al precio de costo para calcular el precio de venta, nos manejamos con un valor   
            general de todo el negocio que podría ser por ejemplo 40%, siendo que si un producto contiene un valor distinto por algún motivo, se agenda aquí. Entonces, si éste 
            valor es 0 es porque usa el valor general indicado en la tabla config, de lo contrario aquí se carga el valor individual.
        Promo: 0 o 1: Indican si pertenece o no a una o más promociones
        CantPreaviso.
        CantMaxima: Cuando uno tiene promociones de un producto que vende normalmente, no quiere mezclar la mercadería que tenía con la nueva, por ende, con cantidad máxima
            no nos excedemos.
        DiasPreaviso.

    Tabla: Config:
        Datos generales y de configuración del sistema.
            ID.
            Nombre.
            Valor.
        Su info:
            CantPrincipal: Es la cantidad de productos en la base principal.
            CantAyuda: Idem en Ayuda.
            CantEliminados: Idem Eliminados.
            Porcentaje: Es el porcentaje general de cálculo de precio de venta de los productos indicados en la tabla "Adicionales".
            Cantidad_Productos: Es la cantidad total de productos incluyendo los eliminados
            Ultimo_ID: Es una guía para saber cuál es el último entero de ID que se guardó, a pesar de que está cargado como float en la db

    BASE DE DATOS: elim.db:
    Cuando se elimina un producto, en realidad lo quitamos de la base de datos general para que no interfiera en las búsquedas, pero realizamos una copia en una base de datos llamada "elim.db". La idea principal es mantener sus datos estadísticos si es que hubieron, y además permitir que vuelvan a estar presentes a futuro.

    Cuando se inicia por primera vez el programa se deben cargar los productos, stock y precios. Para ayudar al proceso, se contará con una base de datos con los productos que se conocen y así el encargado de la tarea no tendrá que cargar todos los detalles y códigos de cada producto. Desde la ventana de carga se irán mostrando y pasando todos los productos de la base de datos de ayuda para que se puedan ir controlando uno a uno.
    Lo más probable es que dentro de la lista de productos hayan unos que el negocio vende y otros que no vende. Para los productos que vende, sólo debe ir actualizando los valores sin más problemas. Pero cuando se ecuentra con uno que no vende debe eliminarlo, que no va a ser más que ignorarlo y continuar con el proceso.

    Pero si una vez que el negocio está en marcha trabajando con el programa, se decide dejar de vender algún producto por alguna razón, éste al eliminarse genera una copia en la base de datos de eliminados que no es más que una copia exacta de la base de datos original, lo cuál permite que su copiado se realice con el mismo código para la base de datos principal.
    De ésta manera, si un día queremos ver los datos estadísticos de un producto ya eliminado, podemos consultarlo sin más problemas porque su info estará en la correspondiente base de datos.
    En el caso de que en un futuro se desee volver a cargar un producto eliminado que contiene estadística, se lo puede volver a recuperar conservando todos sus datos o ignorándolos según lo desee el encargado.

    Cabe aclarar también que a medida que se vayan creando productos nuevos, lo que se hace es generar un nuevo registro también en la base de datos de ayuda para ir actualizándola constantemente.
'''

import sqlite3
import sources.mod.vars as mi_vs

LISTA_PATH = []

# Función decoradora
def conexion_db(sql):
    '''
    FUNCIÓN DECORADORA DE CONEXIÓN CON DB SQLITE3.
    Debe ser llamada desde una función que proporcione 3 parámetros, el nombre de la db, la consulta (query), y los parámetros si es que se usan.
    La búsqueda en las bases de datos será en orden según lo trabajado en la lista que hay en mi_vs, dejando la pos[0] para el final ya que es la local, y armando el path según el string que llegue en el parámetro db.

    Intenta conectarse con las bases de datos indicada por parámetro y devuelve 2 valores:
    1: valores:
        -1 = No pudo conectarse a ninguna base de datos
        0  = Se conectó a la db local
        1  = Se conectó a la que está en la pos 1 de la lista de path que tenemos en mi_vs.LIST_BASE_DATOS
        n  = Continúa con la lógica del valor anterior hasta llegar a 4, que es la 5ta posición de path.
    2: Resultado de la consulta.
    En el caso de que no se haya podido conectar con ninguna base de datos, devolverá False y un string vacío.'''
    def wrapper(*args):
        db, query, parameters = sql(*args)
        largo = len(mi_vs.LIST_BASE_DATOS)
        for pos in range(largo):
            if parameters == "LOCAL":
                path = mi_vs.LIST_BASE_DATOS[0] + db
                aux = 0
            else:
                if pos == largo - 1:
                    path = mi_vs.LIST_BASE_DATOS[0] + db
                    aux = 0
                else:
                    path = mi_vs.LIST_BASE_DATOS[pos + 1] + db
                    aux = pos + 1
            try:
                with sqlite3.connect(path) as conn:
                    Cur = conn.cursor()
                    result = Cur.execute(query, parameters)
                    conn.commit()
                return aux, result
            except:
                if parameters == "LOCAL":
                    return -1, ""
        return -1, ""
    return wrapper

'''#############################################################################################################################################
    CREA PRODUCTO  '''

def Nuevo_Producto(ListaProductos, ListaStock, ListaAdicionales, SumaUnidad):
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
        Promo = ListaAdicionales[7]
        CantPreaviso = ListaAdicionales[8]
        CantMaxima = ListaAdicionales[9]
        DiasPreaviso = ListaAdicionales[10]
        Reg_Add_Adicionales(Id_, CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, Promo, CantPreaviso, CantMaxima, DiasPreaviso)

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
        Reg_Add_Estadistica(Id_, GciaSemanal, GciaMensual, GciaAnual, GciaTotal, CantVendSem, CantVendMes, CantVendAnual, CantVendTotal, SiniestrosTotal)

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

def Reg_Add_Adicionales(ID, CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, Promo, CantPreaviso, CantMaxima, DiasPreaviso):
    sql = 'INSERT INTO Adicionales VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    parametros = (ID, CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, Promo, CantPreaviso, CantMaxima, DiasPreaviso)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql, parametros)

def Reg_Add_Estadistica(ID, GciaSemanal, GciaMensual, GciaAnual, GciaTotal, CantVendSem, CantVendMes, CantVendAnual, CantVendTotal, SiniestrosTotal):
    sql = 'INSERT INTO Estadistica VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
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
    sql = 'UPDATE Productos SET Codigo = "{}", CodBulto = "{}", CantBulto = {}, Concepto = "{}", Marca = "{}", Detalle = "{}", UnidadMedida = {} WHERE ID = {}' .format(Codigo, CodBulto, CantBulto, Concepto, Marca, Detalle, UnidadMedida, ID_)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql)

# Actualiza datos de la tabla "Productos" según su Código
def Act_Productos_Segun_Codigo(CodBulto, CantBulto, Concepto, Marca, Detalle, UnidadMedida, Codigo_):
    sql = 'UPDATE Productos SET CodBulto = "{}", CantBulto = "{}", Concepto = "{}", Marca = "{}", Detalle = "{}", UnidadMedida = {} WHERE Codigo = {}' .format(CodBulto, CantBulto, Concepto, Marca, Detalle, UnidadMedida, Codigo_)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql)

def Act_Stock_Segun_ID_Por_Lista(Lista):
    '''Genera que una actualización que viene preparada en una lista, se pueda hacer dividida en variables para la función que está debajo.'''
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
    estado, Datos = Act_Stock_Segun_ID(Cant1, Cant2, Cant3, Vto1, Vto2, Vto3, PcioCpa1, PcioCpa2, PcioCpa3, CantTotal, PcioVta, StockVerificado, ID_)
    return estado, Datos
@conexion_db
def Act_Stock_Segun_ID(Cant1, Cant2, Cant3, Vto1, Vto2, Vto3, PcioCpa1, PcioCpa2, PcioCpa3, CantTotal, PcioVta, StockVerificado, ID_):
    '''# Actualiza datos de la tabla "Stock" según su ID'''
    sql = 'UPDATE Stock SET Cant1 = {}, Cant2 = {}, Cant3 = {}, Vto1 = {}, Vto2 = {}, Vto3 = {}, PcioCpa1 = {}, PcioCpa2 = {}, PcioCpa3 = {}, CantTotal = {}, PcioVta = {}, StockVerificado = {} WHERE ID = {}'.format(Cant1, Cant2, Cant3, Vto1, Vto2, Vto3, PcioCpa1, PcioCpa2, PcioCpa3, CantTotal, PcioVta, StockVerificado, ID_)
    return "prod.db", sql, ()

# Genera que una actualización que viene preparada en una lista, se pueda hacer dividida en variables para la función que está debajo
def Act_Adicionales_Segun_ID_Por_Lista(Lista):
    CajaAsoc = Lista[1]
    Mayorista = Lista[2]
    UltFechaVta = Lista[3]
    Siniestro = Lista[4]
    Sobrante = Lista[5]
    SinCobrar = Lista[6]
    PorcGeneral = Lista[7]
    Promo = Lista[8]
    CantPreaviso = Lista[9]
    CantMaxima = Lista[10]
    DiasPreaviso = Lista[11]
    ID_ = Lista[0]
    Act_Adicionales_Segun_ID(CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, Promo, CantPreaviso, CantMaxima, DiasPreaviso, ID_)
# Actualiza datos de la tabla "Adicionales" según su ID
def Act_Adicionales_Segun_ID(CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, Promo, CantPreaviso, CantMaxima, DiasPreaviso, ID_):
    #if Promo == "": Promo = "Sin_Imagen"
    sql = 'UPDATE Adicionales SET CajaAsoc = {}, Mayorista = {}, UltFechaVta = {}, Siniestro = {}, Sobrante = {}, SinCobrar = {}, PorcGeneral = {}, Promo = "{}", CantPreaviso = {}, CantMaxima = {}, DiasPreaviso = {} WHERE ID = {}'.format(CajaAsoc, Mayorista, UltFechaVta, Siniestro, Sobrante, SinCobrar, PorcGeneral, Promo, CantPreaviso, CantMaxima, DiasPreaviso, ID_)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql)

def Act_Estadisticas_Segun_ID_Por_Lista(Lista):
    '''Genera que una actualización que viene preparada en una lista, se pueda hacer dividida en variables para la función que está debajo.'''
    GciaSemanal = Lista[1]
    GciaMensual = Lista[2]
    GciaAnual = Lista[3]
    GciaTotal = Lista[4]
    CantVendSem = Lista[5]
    CantVendMes = Lista[6]
    CantVendAnual = Lista[7]
    CantVendTotal = Lista[8]
    SiniestrosTotal = Lista[9]
    ID_ = Lista[0]
    estado, Datos = Act_Estadisticas_Segun_ID(GciaSemanal, GciaMensual, GciaAnual, GciaTotal, CantVendSem, CantVendMes, CantVendAnual, CantVendTotal, SiniestrosTotal, ID_)
    return estado, Datos
@conexion_db
def Act_Estadisticas_Segun_ID(GciaSemanal, GciaMensual, GciaAnual, GciaTotal, CantVendSem, CantVendMes, CantVendAnual, CantVendTotal, SiniestrosTotal, ID_):
    '''Actualiza datos de la tabla "Estadisticas" según su ID.'''
    sql = 'UPDATE Estadistica SET GciaSemanal = {}, GciaMensual = {}, GciaAnual = {}, GciaTotal = {}, CantVendSem = {}, CantVendMes = {}, CantVendAnual = {}, CantVendTotal = {}, SiniestrosTotal = {} WHERE ID = {}'.format(GciaSemanal, GciaMensual, GciaAnual, GciaTotal, CantVendSem, CantVendMes, CantVendAnual, CantVendTotal, SiniestrosTotal, ID_)
    return "prod.db", sql, ()

def Act_Promo_S_Cod(Cod_producto, Cod_Promo):
    ID_ = Dev_Dato_Cod("Productos", "ID", Cod_producto)
    Act_Promo_S_Id(ID_, Cod_Promo)

def Act_Promo_S_Id(Id_producto, Cod_Promo):
    sql = 'UPDATE Adicionales SET Promo = "{}" WHERE ID = {}'.format(Cod_Promo, Id_producto)
    Realiza_consulta(mi_vs.BASE_DATOS_SEC, sql)

'''#############################################################################################################################################
    BUSCA INFORMACIÓN DEL PRODUCTO  '''

# Busca un código, si lo encuentra devuelve una variable con 0,1,2,3 que indican si no existe, si existe o si existe, es un código por bulto y prod desactivado.
    # Luego una lista de lo que hay en todas las tablas
    # Y por último indica si pudo conectarse con la DB ppal o secundaria, mediante un número entero ya que pueden haber varias ppales, siendo:
        # 0: Error, no se pudo conectar con nada.
        # 1: DB local.
        # 2...n DB remota.
# Primero lo busca en la lista normal y luego si no lo encuentra en la lista de código por bulto
    # Variables que devuelve:
    # Encontrado = 0,1,2 que indican si no existe, si existe o si existe y es un código por bulto.
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
                    # pos27 = Promo
                    # pos28 = Cantidad de stock de Preaviso
                    # pos29 = Días de Preaviso
# ACTUALIZADO CONEXIONES
''' 1 '''
def Dev_Info_Producto(Codigo, Todos = False):
    # El parámetro "Todos", es para indicar que busque todos los productos incluyendo los desactivados (valor 0 en stockverificado).
    Encontrado = 0
    valor = 0
    Lista_Datos = []
    Conexion = 1

    # Buscamos el producto según su código
    estado, Reg = Reg_Un_param("prod.db", "Productos", "Codigo", Codigo)
    if estado > (-1):
        Encontrado, Lista_Datos = Dev_Info_Producto2("prod.db", Reg)

        # Si no está según su código, lo buscamos entonces según el código por bulto
        if Encontrado == 0:
            estado, Reg = Reg_Un_param("prod.db", "Productos", "CodBulto", Codigo)
            Encontrado, Lista_Datos = Dev_Info_Producto2("prod.db", Reg)
            if Encontrado > 0:
                valor = 2

        elif Encontrado == 1:
            valor = 1

        if Encontrado > 0:
            if Todos == False and Lista_Datos[19] == 0:
                valor = 3

    return valor, Lista_Datos, Conexion

# Función de apoyo a la anterior, recibe un registro de un producto de la base de datos y buscando luego según su ID, completa una lista devolviendo todos los datos del prod.
def Dev_Info_Producto2(base_datos, Registro):
    encontrado = 0
    Lista_Datos = []
    cont = 0
    try:
        # Debería corresponder a la Tabla Productos
        for i in Registro:
            cont += 1
            if cont == 1:
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
        estado, Reg = Reg_Un_param(base_datos, "Stock", "ID", Id_)
        cont = 0
        for i in Reg:
            cont += 1
            if cont == 1:
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
        estado, Reg = Reg_Un_param(base_datos, "Adicionales", "ID", Id_)
        cont = 0
        for i in Reg:
            cont += 1
            if cont == 1:
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
        encontrado = 1
    except:
        pass
    
    if cont == 2:
        encontrado = 2
    return encontrado, Lista_Datos

# Lo mismo que "Dev_Info_Producto" pero en vez de buscar por el código que es un string, busca por el ID que es un Int ordenado de muchos menos caracteres. Lo lógico es que 
    # nunca tenga un error ésta función ya que mientras se busque un número entero que no supere la cantidad de productos, siempre devolverá una lista completa, por ello es que 
    # no le coloco variable de "aviso" de error o algo parecido.
def Dev_Info_Producto_S_ID(ID_):
    Lista_Datos = []    
    # Buscamos el producto según su código
    estado, Reg = Reg_Un_param("prod.db", "Productos", "ID", ID_)
    Encontrado, Lista_Datos = Dev_Info_Producto2(Reg)
    return Lista_Datos

# Para resultados rápidos, devuelve un dato en función a la búsqueda de ID
def Dev_Dato_Cod(Tabla, Nom_col, Cod):
    query = 'SELECT {} FROM {} WHERE Codigo = {}'.format(Nom_col, Tabla, Cod)
    rta = Realiza_consulta(mi_vs.BASE_DATOS_PPAL, query)
    result = 0
    for res in rta:
        result = res[0]
    return result

# Para resultados rápidos, devuelve un dato en función a la búsqueda de ID
def Dev_Dato_ID(Tabla, Nom_col, Id_):
    query = 'SELECT {} FROM {} WHERE ID = {}'.format(Nom_col, Tabla, Id_)
    rta = Realiza_consulta(mi_vs.BASE_DATOS_PPAL, query)
    result = 0
    for res in rta:
        result = res[0]
    return result

'''#############################################################################################################################################
    ELIMINA PRODUCTO  '''

'''#############################################################################################################################################
    FUNCIONES AUXILIARES  '''

# Devuelve el Valor solicitado del registro indicado en "DatoTexto", donde "Valor" es una columna del tipo float y "Nombre" es un texto en la tabla.
def Dev_Config(DatoTexto):
    sql = "SELECT Valor FROM Config WHERE Nombre = '{}'" .format(DatoTexto)
    Resultado = Realiza_consulta(mi_vs.BASE_DATOS_PPAL,sql)
    aux = 0
    for res in Resultado:
        aux = res[0] 
    return float(aux)

# Actualiza cualquier valor de la tabla "Config"
def Act_Config(Valor, Nombre):
    sql = "UPDATE Config SET Valor = {} WHERE Nombre = '{}'" .format(Valor, Nombre)
    Realiza_consulta(mi_vs.BASE_DATOS_PPAL, sql)

'''#############################################################################################################################################
    EJECUCIÓN  '''
# FUNCIÓN BASE DE ACTUALIZACIÓN CUANDO LA COMPARACIÓN ES NUMÉRICA
# ACTUALIZADO CONEXIONES
''' 1 '''
def Act_Valor_Num(BaseDeDatos, Tabla, Col_Actualiza, Valor_Actualiza, Col_Compara, Valor_Compara):
    sql = 'UPDATE {} SET {} = {} WHERE {} = {}'.format(Tabla, Col_Actualiza, Valor_Actualiza, Col_Compara, Valor_Compara)
    Realiza_consulta(BaseDeDatos, sql)

# FUNCIÓN BASE DE ACTUALIZACIÓN CUANDO LA COMPARACIÓN ES TEXTO
# ACTUALIZADO CONEXIONES
def Act_Valor_Texto(BaseDeDatos, Tabla, Col_Actualiza, Valor_Actualiza, Col_Compara, Texto_Compara):
    sql = "UPDATE {} SET {} = '{}' WHERE {} = '{}'".format(Tabla, Col_Actualiza, Valor_Actualiza, Col_Compara, Texto_Compara)
    Realiza_consulta(BaseDeDatos, sql)

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

def Dev_Tabla_Clie(Tabla):
    '''Función que devuelve 2 valores, una variable que va desde -1 hasta 4, indicando si hubo o no conexión y en caso de haber, la posición en la lista de path donde se pudo coenctar, y luego la tabla solicitada.'''
    estado, Tabla = Dev_Tabla("clie.db", Tabla)
    return estado, Tabla

# Devuelve el total de registros de la tabla solicitada de la base de datos de clientes
def Dev_Total_Tabla_Clie(Tabla):
    estado, reg = Reg_Un_param("prod.db", "sqlite_sequence", "name", Tabla)
    valor = 0
    for i in reg:
        valor = i[1]
    return valor

def Dev_ID_ClienteTexto(Tabla, ColumnaCompara, DatoTexto):
    sql = "SELECT ID FROM {} WHERE {} = '{}'" .format(Tabla, ColumnaCompara, DatoTexto)
    Resultado = Realiza_consulta(mi_vs.BASE_CLIENTES_PPAL,sql)
    aux = 0
    for res in Resultado:
        aux = res[0] 
    return int(aux)

# Devuelve un dato solicitado cuando el valor de comparación es un entero
def Dev_Dato_Int(BaseDeDatos, Tabla, ColumnaCompara, DatoCompara, ColumnaDevuelve):
    sql = 'SELECT {} FROM {} WHERE {} = {}'.format(ColumnaDevuelve, Tabla, ColumnaCompara, DatoCompara)
    Result = Realiza_consulta(BaseDeDatos, sql)
    aux = 0
    for i in Result:
        aux = i[0]
    return aux

@conexion_db
def Dev_Tabla(nameDb, Tabla, OrdenBy = ""):
    '''Función que devuelve 2 valores, una variable que va desde -1 hasta 4, indicando si hubo o no conexión y en caso de haber, la posición en la lista de path donde se pudo coenctar, y luego la tabla que se le ha solicitado.
    El parámetro "OrdenBy" debe ser llenado con las pal'''
    if OrdenBy == "":
        sql = 'SELECT * FROM {}' .format(Tabla)
    else:
        sql = 'SELECT * FROM {} ORDER BY {}'.format(Tabla, OrdenBy)
    return nameDb, sql, ()

@conexion_db
def Reg_Un_param(nameDb, Tabla, Columna, DatoCoincide):
    '''Función que devuelve 2 valores, una variable que va desde -1 hasta 4, indicando si hubo o no conexión y en caso de haber, la posición en la lista de path donde se pudo coenctar, y luego el registro solicitado.'''
    sql = "SELECT * FROM {} WHERE {} = '{}'" .format( Tabla, Columna, DatoCoincide)
    return nameDb, sql, ()

@conexion_db
def Update_State_Value(nameDb, namePc, state, nameUp):
    '''Actualiza el estado de una base de datos. Le deben llegar 4 parámetros:
    nameDb = Nombre de la base de datos a la que vamos a actualizar
    namePc = Nombre de la PC que debe informar que ya ha realizado la actualización
    state = Estado a escribir en su columna respectiva
    nameUp = Nombre de la actualización en cuestión.'''
    sql = "UPDATE Actualizaciones SET {} = {} WHERE db = '{}'" .format( namePc, state, nameUp)
    return nameDb, sql, ()

# Actualiza la tabla "Config", sirve para actualizar todos los totales de "Registros" que hay en cada una de las tablas
def Act_Reg_Cant(BaseDeDatos, Cantidad, NomTabla):
    query = 'UPDATE Config SET Registros = ? WHERE Tabla = ?'
    parameters = (Cantidad, NomTabla)
    Realiza_consulta(BaseDeDatos, query, parameters)

@conexion_db
def dateId_AUX(code):
    '''Devuelve un registro con el valor de ID del código indicado.'''
    sql = "SELECT ID FROM Productos WHERE Codigo = '{}'".format(code)
    return "prod.db", sql, "LOCAL"

@conexion_db
def dateUpdate_AUX(id_):
    '''Devuelve un registro con el valor de la fecha en que fue actualizado del ID indicado.'''
    sql = "SELECT Date FROM Update WHERE ID = '{}'".format(id_)
    return "prod.db", sql, "LOCAL"

def dateUpdate(code):
    '''Devuelve la fecha y hora de la última actualización realizada.'''

    # Obtenemos el ID del producto en función al código recibido
    state, reg = dateId_AUX(code)
    id_ = 0
    if state == 0:
        for i in reg:
            id_ = i[0]

        # Ahora con su ID, conseguimos la fecha de última actualización
        state, reg = dateUpdate_AUX(id_)
        if state == 0:
            for i in reg:
                date = i[0]
            return date

@conexion_db
def Update_Price_Act(nameDb_Act, namePc, state, nameUp):
    '''Actualiza el estado de una base de datos. Le deben llegar 4 parámetros:
    nameDb = Nombre de la base de datos a la que vamos a actualizar
    namePc = Nombre de la PC que debe informar que ya ha realizado la actualización
    state = Estado a escribir en su columna respectiva
    nameUp = Nombre de la actualización en cuestión.'''
    sql = "UPDATE Actualizaciones SET {} = {} WHERE db = '{}'" .format( namePc, state, nameUp)
    return nameDb, sql, ()

def Dev_Tabla_inicio():
    '''Esta función ya existía, pero tuve que realizarla ya que el decorador de conexión se basa en una tabla que primero tenemos que rellenar aquí.'''
    
    sql = 'SELECT * FROM url ORDER BY ID'
    Table = Realiza_consulta("./sources/db/path.db", sql, ())
    return Table