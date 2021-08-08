# Indica a la ventana BUSCAR PRODUCTO, a qué ventana tiene que volver
ORIGEN_BUSCAR_PROD = 0
# Indica a la ventana que buscó un producto, qué ID debe cargar
ID_BUSCADO = 0

# Indica a la ventana de productos, que se viene con un producto que no existe desde la ventana reponer
COD_NUEVO = ""

# Dejamos guardado la fecha del día de hoy
DIA = 0
MES = 0
ANO = 0

# Debido a que el signo "=" que figura en el teclado numérico muestra diversos caracteres en pantalla según la PC, vamos a hacer configurable su acción. Es decir, que la idea
    # es que al apretar ese botón funcione como un comando especial en todas las ventanas, dirigiendo el foco al line donde se coloca el CODIGO en las ventanas que lo posean,
    # luego de haberlo limpiado y en donde sea necesario desconfigura todo lo que corresponda. Por ende su valor tipo string va a estar cargado en ésta variable que tomará
    # dicho dato de la base de datos de configuración. Al mismo tiempo servirá para ser configurado manualmente.
BTN_IGUAL = "¿"

# Si un tipo de FONDO tiene incremento o descuento, se especifica en una base de datos y luego se actualizan acá en función a su ORDEN y no al ID.
    # 0: Sin modificaciones

    # MODIFICACIONES SIN AFECTAR EL VALOR QUE VIENE DEL PRODUCTO
    # 1: Tiene incrementos del tipo %
    # 2: Tiene descuentos del tipo %
    # 3: Tiene incremento del tipo $
    # 4: Tiene descuentos del tipo $

    # MODIFICACIONES QUE AFECTAN EL VALOR QUE VIENE DEL PRODUCTO
    # 5: Tiene incrementos del tipo %
    # 6: Tiene descuentos del tipo %
    # 7: Tiene incremento del tipo $
    # 8: Tiene descuentos del tipo $
INCREMENTOS = [0, 1, 0]

# Path Base de Datos de Productos
BASE_DATOS_PPAL = ""
BASE_DATOS_SEC = ""

# Path Base de Datos de Estado General
BASE_GENERAL_PPAL = ""
BASE_GENERAL_SEC = ""

# Path Base de Datos de las Promociones
BASE_PROMOS_PPAL = ""
BASE_PROMOS_SEC = ""

# Path Base de Datos de las Configuraciones
BASE_CONFIG_PPAL = ""
BASE_CONFIG_SEC = ""

# Path Base de Datos de Varios
BASE_VARIOS_PPAL = ""
BASE_VARIOS_SEC = ""

# Path Base de Datos de Clientes
BASE_CLIENTES_PPAL = ""
BASE_CLIENTES_SEC = ""

# Cuando está en False, se le restringe todo y sólo sirve para cargar ventas
ADMIN = False