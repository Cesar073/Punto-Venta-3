'''
FUNCIONES PARA EL MANEJO DE PROMOCIONES Y ACTUALIZACIONES DE VARIABLES GENERALES
Los datos de cada promo deben guardarse con un formato específico, en éstas funciones convertimos los datos en esos formatos y también los transcribimos.
También contamos con 2 bases de datos para trabajar las ventas, por un lado la PPAL que es la que esté en la PC ppal del local, y una db local en caso de problemas de conexión.

FALTA SOLUCIONAR
Las funciones están incompletas o no devuelven lo que debe ser así que falta revisar una por una

FORMATO DE LAS PROMOS:
    PROMO 1: Es una promo fija, lo que quiere decir es que se indica la cantidad de productos que contiene la promo y también cuáles son esos productos. No son intercambiables
            ni nada parecido. Para facilitar la carga de los mismos ya que esta promo puede servir para 2 puré de tomates como así también para un pack de azúcar o 3 Cocas y un
            Fernet, es necesario contar con la cantidad para cada uno de sus productos, el código de los mismos y el precio X UNIDAD final de ellos.
            Cod_Prod1 / Cant_Prod1 * Pcio_Cod1 $ Cod_Prod2 / Cant_Prod2 * Pcio_Cod2 $
            Ejemplos:
            123456/2*50$987654/1*200$ (para promo de costo final: $ 300)
            456123/12*50$ (para promo de costo final: $ 600)
    
    PROMO 2: Es una promo que permite la combinación de diversos productos pero porque son del mismo PRECIO, por ejemplo los jugos en sobrecitos:
            Cant_Prods * Pcio_Individual $ Cod1 / Cod2 / Cod3 / Cod4...
            5*20.0$123/456/789/321/... (para promo de costo final: $ 100)
    
    Recordar que el precio final de las promos se encuentra en una columna de la DB.

FUNCIONES ADICIONALES
Son funciones exclusivas de éste programa que se repiten en más de una ventana, clase o módulo, que para evitar que se copien varias veces, las cargamos en éste módulo.
'''
from App import *
import sources.mod.mdbprom as mdbprom
import sources.mod.mdbprod as mdbprod
import sources.mod.vars as mi_vars
import sources.mod.form as form

# Le llega el texto que tiene guardado la db sobre los productos de una promo del Tipo 1, y devuelve 3 listas con los datos: 
    # Cod prod
    # cantidades
    # precio
def Dev_Info_Promo_1(Texto):
    lista_Codi = []
    lista_Pcio = []
    lista_Cant = []
    auxS = ""
    for caracter in Texto:
        if caracter == "/":
            lista_Codi.append(auxS)
            auxS = ""
        elif caracter == "*":
            lista_Cant.append(float(auxS))
            auxS = ""
        elif caracter == "$":
            lista_Pcio.append(float(auxS))
            auxS = ""
        else:
            auxS += caracter
    return lista_Codi, lista_Cant, lista_Pcio

# Le llega el texto que tiene guardado la db sobre los productos de una promo del Tipo 2, y devuelve 3 datos:
    # Variable_Float: Cantidad, Peso, etc... de los productos que se deben comprar para acceder a la promo.
    # Variable_Float: Precio de cada producto.
    # Lista_codigos: Es la lista de los códigos de productos que deben encontrarse para que la promo sea válida.
def Dev_Info_Promo_2(Texto):
    
    auxS = ""
    cant = 0.0
    precio = 0.0
    lista_Cods = []
    
    for caracter in Texto:
        if caracter == "/":
            lista_Cods.append(auxS)
            auxS = ""
        elif caracter == "*":
            cant = float(auxS)
            auxS = ""
        elif caracter == "$":
            precio = float(auxS)
            auxS = ""
        else:
            auxS += caracter
    
    return cant, precio, lista_Cods

# Agrega una promo a un producto que ya tiene o que no tiene promo. Se utiliza cada vez que se crea una promo o bien, cuando se agrega un producto a una promo preexistente.
# El formato de toda promo comienza con un número identificatorio y siempre termina con un guión
def Agrega_Promo_Producto(Promo_texto, ID):
    # Buscamos si el producto cuenta o no con una promo, de ser así la editamos
    Lista = mdbprod.Dev_Info_Producto_S_ID(ID)
    Lista[27] += Promo_texto + "-"
    mdbprod.Act_Promo_S_Id(ID, Lista[27])

# Le llega el ID de un producto y devuelve una variable V_F si es que ese prod contiene o no una promo, y si tiene promo/s, devuelve una lista con las promos en formato
    # texto
def Dev_Promo(ID):
    Lista_Aux = []
    Lista = mdbprod.Dev_Info_Producto_S_ID(ID)
    if Lista[27] == "":
        return False, Lista_Aux
    else:
        auxS = ""
        for i in Lista[27]:
            if i == "-" or i == "+":
                Lista_Aux.append(auxS)
                auxS = ""
            else:
                auxS += i
    
    return True, Lista_Aux

'''
FUNCIONES VIEJAS OBSOLTAS
'''

# Le llega el texto que tiene guardado la db sobre los productos de una promo del Tipo 2, y devuelve 3 datos:
    # Variable_Int: Cantidad de los productos que se deben comprar para acceder a la promo.
    # Variable_Float: Precio. Un sólo precio ya que todos los productos tendrán el mismo precio a la hora de venderlos.
    # Lista_codigos: Es la lista de los códigos de productos que deben encontrarse para que la promo sea válida.
def Dev_Info_Promo_2_Codigos(Texto):
    
    auxS = ""
    cant = 0
    precio = 0.0
    lista_codigos = []
    
    for caracter in Texto:
        if caracter == "*":
            cant = float(auxS)
            auxS = ""
        elif caracter == "/":
            lista_codigos.append(auxS)
            auxS = ""
        elif caracter == "$":
            precio = float(auxS)
            auxS = ""
        else:
            auxS += caracter
    
    return cant, precio, lista_codigos

# Busca en los códigos de las promos un producto y devuelve:
    # 0: Si no lo encuentra
    # 1: Si lo encuentra y está todo OK
    # 2: Si lo encuentra pero la promo está desactivada
    # 3: Si lo encuentra pero no hay más stock
    # 4: Si lo encuentra pero no alcanza la cantidad del stock total para una promo
    # 5: Si lo encuentra pero no alcanza la cantidad restante en "CANTIDAD MÁXIMA" para una promo
    # 6: Si lo encuentra pero caducó la fecha de la promo
    # 7: Si lo encuentra pero todavía no ha iniciado la promo

    # El 2do dato que devuelve es el código de la promo si es que la encuentra, sino devuelve 0
def Dev_Estado_Cod_En_Promo(ID):
    ID2 = str(ID)
    # Traemos toda la tabla de promociones para controlarlas todas
    Tabla = mdbprom.Dev_Tabla("Promos")
    # Recorremos los registros a ver si encontramos el código buscado
    for reg in Tabla:
        
        encontrado = False
        pos = (-1)

        # Buscamos código por código para ver a donde lo encontramos
        if reg[4] == 1:
            # Buscamos en los códigos si coincide el id
            id_, cant_, precio_ = Dev_Info_Promo_1(reg[5])
            if ID2 == id_:
                encontrado = True
        if reg[4] == 2:
            cant_, lista_Ids, lista_precio_ = Dev_Info_Promo_2(reg[5])
            if ID in lista_Ids:
                encontrado = True
                pos = lista_Ids.index(ID)
        
        if encontrado == True:
            # Primero revisamos si la promo está activa
            if reg[14] == 1:

                # Controlamos si respeta las fechas
                if reg[6] > 0 or reg[7] > 0:
                    # Obtenemos el valor numérico del día de hoy, ya que en la db se guarda con el mismo formato, un entero que comienza en 1 el 1ro de Enero del 2000
                    dia = form.Trans_Fecha_Num(mi_vars.DIA, mi_vars.MES, mi_vars.ANO)
                    # Ahora revisamos si tiene fecha de inicio y se encuentra superando la fecha
                    if reg[6] > 0:
                        if dia < reg[6]:
                            return 7, reg
                    # Revisamos si tiene fecha de caducidad y estamos o no en fecha
                    if reg[7] > 0:
                        if dia > reg[7]:
                            return 6, reg

                return 1, reg

            else:
                # Retornamos que está desactivada
                return 2, reg
    # Si llegamos a esta instancia es xq no se encontró el producto
    return 0, 0


# Se ejecuta cuando se inicia el programa, y se encarga de buscar qué productos pertenecen a una promo y dsp actualiza su valor en ADICIONALES
def Actualiza_Promos():

    PONE_EN_CERO_LAS_PROMOS()

    fecha = form.Trans_Fecha_Num(mi_vars.DIA, mi_vars.MES, mi_vars.ANO)
    Tabla = mdbprom.Dev_Tabla("Promos")

    # Controlamos registro por registro
    for reg in Tabla:
        
        # Bandera para avisar si está activa la promo
        ok = True

        # Controlamos con su fecha de inicio
        if reg[6] > 0:
            if reg[6] > fecha:
                ok = False

        # Controlamos con su fecha de fin
        if reg[7] > 0:
            if reg[7] < fecha:
                ok = False

        # Controlamos si está activo
        if reg[14] == 0:
            ok = False

        if reg[4] == 1:
            lista = Dev_Info_Promo_1(reg[5])
            valor = 0
            if ok == True:
                valor = 1
            mdbprod.Act_Valor_Num("Adicionales", "Promo", 1, "ID", int(lista[0]))
            print(lista[0])

        elif reg[4] == 2:
            valor = 0
            if ok == True:
                valor = 2
            cant, lista1, lista2 = Dev_Info_Promo_2(reg[5])
            for i in lista1:
                mdbprod.Act_Valor_Num("Adicionales", "Promo", valor, "ID", i)
                print(str(i))

    # Todos los espacios vacíos quedarán en valor 0
    lista_Id = []
    Tabla = mdbprod.Dev_Tabla(mi_vars.BASE_DATOS, "Adicionales")
    for reg in Tabla:
        if reg[8] == "":
            lista_Id.append(reg[0])
    
    for n in lista_Id:
        mdbprod.Act_Valor_Num("Adicionales", "Promo", 0, "ID", n)
        print(str(n))


def PONE_EN_CERO_LAS_PROMOS():
    for i in range(1572):
        if i == 1138:
            print(valor)
        valor = i + 1
        try:
            lista = mdbprod.Dev_Info_Producto_S_ID(valor)
            if len(lista) < 5:
                print(valor)
            mdbprod.Act_Promo_a_Cero(valor)
        except:
            print(valor)
    print(valor)





# Limpia la columna Promo de cada producto en aquellos que coincidan con el nombre de la promo. A ésta función se la llama siempre que se guarda algún cambio de Promo.
def Quita_Producto_Promo(Cod_Promo):
    # Bucle para buscar tantos productos contengan la promo actual del tipo 1. Recordar que el código llega sin el símbolo.
    Cod_Aux = Cod_Promo + "-"
    bucle = True
    while bucle == True:
        Reg = ""
        Id = 0
        try:
            Reg = mdbprod.Reg_Un_param(mi_vars.BASE_DATOS_PPAL, "Adicionales", "Promo", Cod_Aux)
            for pos in Reg:
                Id = pos[0]
            if Id > 0:
                mdbprod.Act_Promo_S_Id(Id, "")
            else:
                bucle = False
        except:
            bucle = False

    # Bucle para buscar tantos productos contengan la promo actual del tipo 2
    # Tengo que volver a  buscar porque si el usuario cambió el tipo de promo, no lo encontraría si lo busco con el signo - o +. Recordar que el código llega sin el símbolo.
    Cod_Aux = Cod_Promo + "+"
    bucle = True
    while bucle == True:
        Reg = ""
        Id = 0
        try:
            Reg = mdbprod.Reg_Un_param(mi_vars.BASE_DATOS_PPAL, "Adicionales", "Promo", Cod_Aux)
            for pos in Reg:
                Id = pos[0]
            if Id > 0:
                mdbprod.Act_Promo_S_Id(Id, "")
            else:
                bucle = False
        except:
            bucle = False

# Para guardar en la base de datos los productos con sus precios, necesitamos realizar una serie de cálculos previos y le asignamos el precio en función a su participación.
    # Devuelve una lista de precios en el orden de los productos que nos fueron entregados
def Dev_Texto_Precios(Pcio_Total, Lista_Pcios):
    # Para solucionar temas de redondeo, vamos a calcular el valor que corresponde a cada producto y al último le asignamos el costo faltante lo que nos redondearía unos ctvs.

    # Lista donde vamos a devolver los precios
    Lista_part = []
    
    # Vamos a buscar la participación que cada producto tiene sobre el total, por ello es que primero tenemos que saber lo que saldría a precio normal el tot de todos los prod.
    suma = 0.0
    for i in Lista_Pcios:
        suma += i
    Tope = len(Lista_Pcios)
    for i in range(Tope):
        Lista_part.append(form.Redondear_float(Pcio_Total * (Lista_Pcios[i] / suma),2))
    suma = 0.0
    for i in range(Tope - 1):
        suma += Lista_part[i]

    Lista_part[-1] = form.Redondear_float(Pcio_Total - suma,2)

    return Lista_part

#print(Dev_Texto_Productos(200, [10.5,50.4,200.2,40.1]))


def Actualiza_Path():
    '''Los Path's de las bases de datos los tenemos cargados en variables, ésta función actualiza dichas variables con los datos de una base de datos que tenemos que tener en ésta misma PC (./sources/db/path.db). Devuelve un número del 1 al 5 indicando la cantidad de Path que encontró, y 0 en caso de que no haya podido cargar ningún Path.
    '''
    count = 0
    try:
        Tabla = mdbprod.Dev_Tabla("./sources/db/path.db", "url", "ID")
        for reg in Tabla:
            # Path Base de Datos Pos 2 en la DB. REMOTA PPAL. Es la DB con la cuál se debería trabajar siempre, la más actualizada.
            if reg[1] == "POS_2" and reg[2] != "":
                mi_vars.BASE_DATOS_PPAL = reg[2] + "prod.db"
                mi_vars.BASE_GENERAL_PPAL = reg[2] + "egen.db"
                mi_vars.BASE_PROMOS_PPAL = reg[2] + "prom.db"
                mi_vars.BASE_CONFIG_PPAL = reg[2] + "config.db"
                mi_vars.BASE_VARIOS_PPAL = reg[2] + "vari.db"
                count += 1

            # Path Base de Datos Pos 1 en la DB. LOCAL. Es el recurso para cuando no hay conexión, o para las configuraciones locales.
            if reg[1] == "POS_1" and reg[2] != "":
                mi_vars.BASE_DATOS_SEC = reg[2] + "prod.db"
                mi_vars.BASE_GENERAL_SEC = reg[2] + "egen.db"
                mi_vars.BASE_PROMOS_SEC = reg[2] + "prom.db"
                mi_vars.BASE_CONFIG_SEC = reg[2] + "config.db"
                mi_vars.BASE_VARIOS_SEC = reg[2] + "vari.db"
                count += 1
        return count
    except:
        return count

def Actualiza_Configuraciones(vtn, Lista_Datos):
    '''Sirve para actualizar variables globales en función a los datos que hayan en la db de config, valores de las configuraciones iniciales del sistema, aunque si hubieron cambios se puede volver a llamar a la función. Retorna una lista con los datos que sean necesarios, que por el momento sólo tenemos que retornar el estado de la variable que permite cargar ventas con productos desactivados.
    
    Pos 1: de 0 a 5 - Ver pos 32 de la lista de Ventas.'''

    Tabla = mdbprod.Dev_Tabla(mi_vars.BASE_CONFIG_SEC, "Generales", "ID")
    Rta1 = 0
    act_1 = False
    Rta2 = ""
    act_2 = False
    for reg in Tabla:
        if reg[3] == "Vta_Prod_Desact":
            Lista_Datos[0] = reg[4]
        if reg[3] == "Barra":
            if reg[1] == 1:
                if reg[5] == "":
                    bucle = False
                    while bucle == False:
                        Rta2, Ok = QInputDialog.getText(vtn, "Configuración.", "Ingrese SÓLO una tecla especial del teclado para generar la orden de ...")
                        if len(Rta2) == 1 and Ok == True:
                            bucle = True
                            act_2 = True
    if act_1 == True:
        mdbprod.Act_Valor_Texto(mi_vars.BASE_CONFIG_SEC, "Generales", "Valor_I", Rta1 - 1, "Nombre", "renglones_listas")
    if act_2 == True:
        mdbprod.Act_Valor_Texto(mi_vars.BASE_CONFIG_SEC, "Generales", "Valor_S", Rta2, "Nombre", "Barra")
        mi_vars.BTN_IGUAL = Rta2

