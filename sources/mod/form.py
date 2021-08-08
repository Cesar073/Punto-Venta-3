''' 
FECHAS
    def Dev_Fecha_Act_Int():
    def R_T_Dev_Fecha_Act(Izq_Anio = True):
    def Devuelve_Valor_Mes(Texto):
    def Devuelve_Mes_Texto(Valor):
    def Es_Fecha(Fecha):
    def Autoriza_Guardar_Fecha_Aux(Dia_, Mes_, Ano_):
    def Trans_Fecha_Num(dd, mm, aaaa):
    def Trans_Num_Fecha(numero):
    def Determina_Biciesto(aaaa):
    def Extrae_Fecha(Fecha, Pos):

FORMATOS
    def Line_Solo_Num(Texto):
    def Line_Num_Coma_Punto(Texto):
    def Line_Num_Coma_(Texto):
    def Line_Numero_Signos(Texto):
    def Formato_Decimal(Valor, Decimales):
    def Formato_ValorF_Variable(Valor):
    def Formato_Unidades(Valor, Decimales):
    def Formato_Contabilidad(Valor, V_F_Signo=True):
    def Str_Float(Texto):
    def Formato_Mayuscula(Texto, espacios_ = False):

FUNCIONES GLOBALES
    def Es_Numero(Valor):
    def Redondear(Valor, Clave = 5):
    def Es_Numero_Int(Valor):

FUNCIONES INTERNAS
    def Devuelve_Entero_Signo(Caracter):
    def Ajusta_A_2_Dec(Valor):
    def Ajusta_Decimales(Valor, Decimales):
    def Separador_Int_Float(Valor):
    def Punto_Mil(Valor):
    def Quita_Simbol(Valor):
    def Normalize(Valor):
    def Line_A_Variable(Texto, Decimales = 0):
    def Variable_A_Line(Texto, Decimales = 0):
'''
from datetime import datetime
import sources.mod.vars as mi_vs
# Variables que se rellenan al final del módulo
DIA = 0
MES = 0
ANO = 0


'''#################################################################   FECHAS   #################################################################'''
# Devuelve 3 variables, 3 números enteros que representan la fecha actual en formato dd, mm, aaaa
def Dev_Fecha_Act_Int():
    dt = datetime.now()
    return dt.day, dt.month, dt.year

# Convierte la fecha actual para ser guardado en un string. El parámetro indica la posición inicial del Año, el orden del día, mes y año
def R_T_Dev_Fecha_Act(Izq_Anio = True):
    dt = datetime.now()
    if Izq_Anio == True:
        Resultado = str(dt.year) + '/' + str(dt.month) + '/' + str(dt.day)
    else:
        Resultado = str(dt.day) + '/' + str(dt.month) + '/' + str(dt.year)
    return Resultado

# Discrimina el mes de una fecha que viene en formato de string y devuelve el Mes en int
def Devuelve_Valor_Mes(Texto):
    Estado = 0
    Aux = ''
    for i in Texto:
        if i == '/':
            Estado += 1
        else:
            if Estado == 2:
                return int(Aux)
            elif Estado == 1:
                Aux += i

# Devuelve el mes en texto según un número del 1 al 12
def Devuelve_Mes_Texto(Valor):
    if Es_Numero_Int(Valor):
        Valor = int(Valor)
        if Valor > 0 and Valor < 13:
            if Valor == 1:
                return 'Enero'
            if Valor == 2:
                return 'Febrero'
            if Valor == 3:
                return 'Marzo'
            if Valor == 4:
                return 'Abril'
            if Valor == 5:
                return 'Mayo'
            if Valor == 6:
                return 'Junio'
            if Valor == 7:
                return 'Julio'
            if Valor == 8:
                return 'Agosto'
            if Valor == 9:
                return 'Septiembre'
            if Valor == 10:
                return 'Octubre'
            if Valor == 11:
                return 'Noviembre'
            if Valor == 12:
                return 'Diciembre'
    return False

# Devuelve True si es el formato de fecha normal de 10 caracteres 00/00/0000
def Es_Fecha(Fecha):
    if len(Fecha) == 10:
        if Fecha[2] == "/" and Fecha[5] == "/" and Es_Numero_Int(Fecha[0:2]) == True and Es_Numero_Int(Fecha[3:5]) == True and Es_Numero_Int(Fecha[6:]) == True:
            return True
        else:
            return False
    else:
        return False

# Es una auxiliar de la función anterior y sólo devuelve True or False dependiendo si con los datos recibidos se puede o no guardar la fecha
    # Nota: no permite cargar vencimientos de fechas pasadas ni del día actual
    # Devuelve 3 valores: -1: Hubo algún error. 0...n: Es un número entero que muestra la diferencia en días con la fecha actual. Nunca va a devolver un num negativo
def Autoriza_Guardar_Fecha_Aux(Dia_, Mes_, Ano_):
    DIA, MES, ANO = Dev_Fecha_Act_Int()
    # Controlamos que el día ingresado por el usuario sea superior al día actual
    if Dia_ > 0 and Mes_ > 0 and Ano_ > 0:
        if Ano_ > ANO:
            return True
        elif Ano_ < mi_vs.ANO:
            return False
        else:
            if Mes_ > mi_vs.MES:
                return True
            elif Mes_ < mi_vs.MES:
                return False
            else:
                if Dia_ > mi_vs.DIA:
                    return True
                else:
                    return False
    else:
        if Dia_ == 0 and Mes_ == 0 and Ano_ == 0:
            return True
        else:
            return False

# Transforma una fecha en formato: dd, mm, aaaa a un número que representa la cantidad de días transcurridos desde el 1 de enero del 2000
def Trans_Fecha_Num(dd, mm, aaaa):
    # Variable donde se guarda la cantidad de días pasados siendo 1 el 1ro de enero del 2000
    dias_pasados = 0

    # Buecle que sólo aumenta la cantidad de días calculando los años biciestos y no biciestos
    for i in range(1000):
        ano_ = 2000 + i
        if aaaa > ano_:
            dias_pasados += 365
            if Determina_Biciesto(ano_):
                dias_pasados += 1
        else:
            break

    # Sumamos los meses y días en ésta función
    if mm > 1:
        dias_pasados += 31
        if mm > 2:
            dias_pasados += 28
            if Determina_Biciesto(aaaa):
                dias_pasados += 1
            if mm > 3:
                dias_pasados += 31
                if mm > 4:
                    dias_pasados += 30
                    if mm > 5:
                        dias_pasados += 31
                        if mm > 6:
                            dias_pasados += 30
                            if mm > 7:
                                dias_pasados += 31
                                if mm > 8:
                                    dias_pasados += 31
                                    if mm > 9:
                                        dias_pasados += 30
                                        if mm > 10:
                                            dias_pasados += 31
                                            if mm > 11:
                                                dias_pasados += 30

    # Ahora le sumo los días y luego el mes
    dias_pasados += dd
    return dias_pasados

# Transforma un número a una fecha en formato: dd, mm, aaaa. El número que debe llegar es un entero entendiendo que 1 equivale al 1ro de enero del 2000
def Trans_Num_Fecha(numero):
    # Buecle que sólo aumenta la cantidad de días calculando los años biciestos y no biciestos
    ano_ = 2000
    mes_ = 1
    aux = 0
    bis = False
    for i in range(1000):
        aux = 365
        if Determina_Biciesto(ano_ + i):
            aux += 1
            bis = True
        else:
            bis = False
        if aux < numero:
            numero -= aux

        elif aux > numero:
            ano_ += i
            break
        else:
            ano_ += i
            return "31/12/" + str(ano_)
        

    # Sumamos los meses y días en ésta función
    auxD = 31
    if (numero - auxD) > 0:
        numero -= auxD
        mes_ += 1
        auxD = 28
        if bis:
            auxD += 1
        if (numero - auxD) > 0:
            numero -= auxD
            mes_ += 1
            auxD = 31
            if (numero - auxD) > 0:
                numero -= auxD
                mes_ += 1
                auxD = 30
                if (numero - auxD) > 0:
                    numero -= auxD
                    mes_ += 1
                    auxD = 31    
                    if (numero - auxD) > 0:
                        numero -= auxD
                        mes_ += 1
                        auxD = 30    
                        if (numero - auxD) > 0:
                            numero -= auxD
                            mes_ += 1
                            auxD = 31    
                            if (numero - auxD) > 0:
                                numero -= auxD
                                mes_ += 1
                                auxD = 31    
                                if (numero - auxD) > 0:
                                    numero -= auxD
                                    mes_ += 1
                                    auxD = 30 
                                    if (numero - auxD) > 0:
                                        numero -= auxD
                                        mes_ += 1
                                        auxD = 31    
                                        if (numero - auxD) > 0:
                                            numero -= auxD
                                            mes_ += 1
                                            auxD = 30
                                            if (numero - auxD) > 0:
                                                numero -= auxD
                                                mes_ += 1


    return str(numero) + "/" + str(mes_) + "/" + str(ano_)

# Calcula si un año determinado es biciesto o no
def Determina_Biciesto(aaaa):
    if (aaaa / 4) == (aaaa // 4):
        aux = str(aaaa)
        if aux[2:] == "00":
            if (aaaa / 400) == (aaaa // 400):
                return True
            else:
                return False
        else:
            return True
    else:
        return False

# Recibe un string en formato de fecha y devuelve el valor solicitado, debido a que las fechas pueden tener en el día o el mes uno o dos dígitos y a veces complica su uso
def Extrae_Fecha(Fecha, Pos):
    # Devuelve el día de la fecha
    if Pos == 1:
        auxI = Fecha.find("/")
        return Fecha[0:auxI]
    # Devuelve el mes
    elif Pos == 2:
        auxI = Fecha.find("/")
        return Fecha[(auxI + 1):(-5)]
    elif Pos == 3:
        return Fecha[(-2):]

'''################################################################   FORMATOS   ################################################################'''
# PARA LOS LINEEDIT
# SÓLO PERMITE NÚMEROS
    # Le llega texto y ésto sólo permite los números, y lo devuelve por defecto en string para que se coloque nuevamente en el lineEdit
def Line_Solo_Num(Texto):
    aux = ""
    for i in Texto:
        if Es_Numero_Int(i):
            aux += i
    return aux

# SÓLO PERMITE NÚMEROS, COMA (,) Y PUNTO (.)
    # Le llega texto y ésto sólo permite los números, y lo devuelve por defecto en string para que se coloque nuevamente en el lineEdit
def Line_Num_Coma_Punto(Texto):
    aux = ""
    for i in Texto:
        if Es_Numero_Int(i) or i == "," or i == ".":
            aux += i
    return aux

# SÓLO PERMITE NÚMEROS, COMA (,) Y PUNTO (.), pero en el caso del punto lo transforma en coma y además permite una única coma. Es para poder ingresar números decimales con el 
    # teclado numérico. Le llega texto y ésto sólo permite los números, y lo devuelve por defecto en string para que se coloque nuevamente en el lineEdit
def Line_Num_Coma_(Texto):
    aux = ""
    coma = False
    for i in Texto:
        if Es_Numero_Int(i):
            aux += i
        elif (i == "," or i == ".") and coma == False:
            # Si se ha borrado un valor anterior a la coma o bien el usuario sólo apretó el punto, le escribimos un cero delante
            if aux == "":
                aux = "0,"
            else:
                aux += ","
            coma = True
    return aux

# SÓLO PERMITE NÚMEROS y los siguientes signos " . , + ¡ * -"
    # Le llega texto y ésto sólo permite los números, y lo devuelve por defecto en string para que se coloque nuevamente en el lineEdit.
def Line_Numero_Signos(Texto):
    aux = ""
    for i in Texto:
        if Es_Numero_Int(i) or i == "+" or i == "-" or i == "*" or i == "¡":
            aux += i
    return aux

#FORMATO CONTABLE
# 1005 >>> 1.005,00
    # Devuelve False si no es un número que se pueda tratar
def Formato_Decimal(Valor, Decimales):
    # Recibe un valor numérico y siempre devuelve un valor con formato Contable con la cantidad de decimales indicados.
    # En caso de que el valor que llega venga con decimales coloca los verdaderos decimales.
    if Es_Numero(Valor):
        Aux1 = round(float(Valor), Decimales)
        Entero, Decimal = Separador_Int_Float(Aux1)
        return (Punto_Mil(Entero) + ',' + Ajusta_Decimales(Decimal, Decimales))
    else:
        return False

# 1005 >>> 1005,00 - Formato Decimal sin el PUNTO MIL
    # Devuelve False si no es un número que se pueda tratar
def Formato_Decimal_S_Punto_Mil(Valor, Decimales):
    # Recibe un valor numérico y siempre devuelve un valor con formato Contable con la cantidad de decimales indicados. 
    # En caso de que el valor que llega venga con decimales coloca los verdaderos decimales.
    if Es_Numero(Valor):
        Aux1 = round(float(Valor), Decimales)
        Entero, Decimal = Separador_Int_Float(Aux1)
        return (Entero + ',' + Ajusta_Decimales(Decimal, Decimales))
    else:
        return False

# En las bases de datos se guardan valores tipo float, pero ese valor en la variable del LineEdit dentro de la ventana debe tener un formato de string específico
    # y acá se lo devolvemos. Es decir, que si un número tiene un punto y ceros después del punto, no hay razón para que exista un valor, así que hay que dejar
    # el valor como si fuera tan sólo un número entero, pero por el contrario, si tiene valor decimal, ya sea uno o 2, se debe colocar su valor exacto.
def Formato_ValorF_Variable(Valor):
    VEntero, Decimal = Separador_Int_Float(Valor)
    Aux = int(Decimal)
    if Aux > 0:
        Aux2 = str(VEntero)
        resultado = Aux2 + '.' + str(Aux)
        return resultado
    else:
        return str(VEntero)

# De un valor que viene de una base de datos, lo devuelve para un line, siendo que si es float usa la coma y sino sólo devuelve un valor entero
def Formato_ValorF_Line(Valor):
    VEntero, Decimal = Separador_Int_Float(Valor)
    Aux = int(Decimal)
    if Aux > 0:
        Aux2 = str(VEntero)
        resultado = Aux2 + ',' + str(Aux)
        return resultado
    else:
        return str(VEntero)

# FORMATO SÓLO PARA UNIDADES: CANTIDADES ENTERAS O KG. SI UN VALOR LLEGA TIPO FLOAT PERO SU PARTE DECIMAL ES 0 (CERO), ENTONCES DEVUELVE UN NÚMERO ENTERO, DE LO CONTRARIO, DEVUELVE UN DECIMAL CON LA CANTIDAD DE DÍGITOS INDICADOS 
# 5000 >>> 5.000
# 1243.50 >>> 1.243,500
def Formato_Unidades(Valor, Decimales):
    # Recibe un valor numérico que puede ser del tipo float. Si el valor es entero, devuelve un número sin coma. De lo contrario, devuelve la cantidad de
    # decimales indicados por parámetro.

    if Es_Numero(Valor):
        Aux1 = str(Valor)
        if (Valor / 1) != (Valor // 1):
            Entero , Decimal = Separador_Int_Float(Valor)
            Entero = Punto_Mil(Entero)
            Decimal = Ajusta_Decimales(Decimal, Decimales)
            return Entero + ',' + Decimal
        else:
            return Punto_Mil(Aux1)


# AJUSTA EL FORMATO CONTABILIDAD AGREGANDO EL SIGO $, PERO DEJANDO EL ESPACIO ENTRE EL SIGNO Y LOS NÚMERO PARA QUE APROXIMADAMENTE QUEDEN A LA MISMA DISTANCIA
# DEVUELVE UN STRING
# EJEMPLO: Si se va a rellenar una lista donde tenemos un número de 4 dígitos (58,50) y otro de 3 (2,50), lo que hacemos es agregar el signo $ adelante, y darle
    # la cantidad de espacios necesarios para mas o menos estar a la misma distancia, es decir, que el número de 4 dígitos tendrá el signo pesos, una cierta
    # cantidad de espacios y el número en cuestión, luego, cuando se haga el mismo proceso pero con el número de 3 dígitos, se le agregará un espacio más entre
    # el signo pesos y su número real.
    # De momento, preparándonos para la devaluación posible, lo que vamos a hacer es prepararlo para números de hasta 1 millón. Es decir, que todos los números
    # empezarán con un espacio, cuando sea 8 dígitos (###.###,##) tendrá 2 espacios, y así sucesivamente hasta el menor que son 3 dígitos.
def Formato_Contabilidad(Valor, V_F_Signo=True):
    Valor = Formato_Decimal(Valor, 2)
    if Valor == False:
        return False
    Aux = len(Valor)
    Aux2 = '  '
    if V_F_Signo == True:
        Aux2 = '$ '
    for i in range(12):
        if 13 - Aux > i:
            Aux2 += ' '
        else:
            break
    return Aux2 + Valor

# TRANSFORMA UN TEXTO A NÚMERO FLOAT
# 1.254,50  >>> 1254.5
def Str_Float(Texto):
    Texto = Line_Num_Coma_Punto(Texto)
    if len(Texto) > 0 and Texto != "," or Texto != ".":
        Texto = Texto.replace(".","")
        Aux = Texto.replace(",",".")
        return float(Aux)
    else:
        return ""

def Str_Float_Punto(Texto):
    Texto = Line_Num_Coma_Punto(Texto)
    if len(Texto) > 0 and Texto != "," or Texto != ".":
        Aux = Texto.replace(",",".")
        return float(Aux)
    else:
        return ""

# Devuelve una letra o palabra pasada a mayúscula. Si la Frase tiene "espacios", se puede mediante parámetro indicar que se conviertan a un guión bajo.
def Formato_Mayuscula(Texto, espacios_ = False):
    Texto = Texto.upper()
    if espacios_ == True:
        Texto = Texto.replace(" ", "_")
    Texto = Texto.replace("Á", "A")
    Texto = Texto.replace("É", "E")
    Texto = Texto.replace("Í", "I")
    Texto = Texto.replace("Ó", "O")
    Texto = Texto.replace("Ú", "U")
    return Texto

'''################################################################   FUNCIONES GLOBALES   ################################################################'''

# Determina si es un número float o int, pero no distingue uno de otro. El parámetro "coma" es para indicarle que puede estar llegando un texto que contiene una "," y que debe 
    # transformarse a "." para intentar convertirlo a float
# Devuelve: V o F
def Es_Numero(Valor, coma = False):
    if coma == True:
        Valor = Valor.replace(",", ".")
    try:
        resultado = float(Valor)
        return True
    except ValueError:
        return False

# Redondea un valor Decimal. Por defecto interpreta que si es mayor a 5 redondea para arriba. Se puede cambiar
def Redondear_int(Valor, Clave = 5):
    Valor = float(Valor)
    Entero, Decimal = Separador_Int_Float(Valor)
    Entero = int(Entero)
    Decimal = int(Ajusta_Decimales(Decimal,1))
    if Decimal > Clave:
        return Entero + 1
    else:
        return Entero

# Redondea un valor Decimal. Por defecto interpreta que si es mayor a 5 redondea para arriba. Se puede cambiar
def Redondear_float(Valor, Decimales, Clave = 5):
    Valor = float(Valor)
    Entero, Decimal = Separador_Int_Float(Valor)
    Decimal = str(Ajusta_Decimales(Decimal,Decimales + 1))
    if int(Decimal[-1]) > Clave:
        Decimal = Decimal[0:Decimales]
        Decimal = str(int(Decimal) + 1)
    else:
        Decimal = Decimal[0:Decimales]
    return float(Entero + "." + Decimal)

# Determina si es un número int.
# Devuelve: V o F
def Es_Numero_Int(Valor):
    try:
        resultado = int(Valor)
        return True
    except ValueError:
        return False

'''################################################################   FUNCIONES INTERNAS   ################################################################'''

# Recibe un valor en cualquier formato, y devuelve un string de 2 decimales
    # 234 >>> 234
    # 12.365 >>> 12.36
def Ajusta_A_2_Dec(Valor):
    Aux1 = str(Valor)
    Bucle = 0
    Cont_Dec = 0
    largo = len(Aux1)
    Aux2 = ''
    Coma = False
    while Bucle < largo:
        Caracter = Aux1[Bucle]
        if Coma == True:
            Cont_Dec += 1
            if Cont_Dec == 2:
                Aux2 += Caracter
                return Aux2
            else:
                Aux2 += Caracter
        else:
            if Caracter == ',' or Caracter == '.':
                Aux2 += '.'
                Coma = True
            else:
                Aux2 += Caracter
        Bucle += 1
    return Aux2

# LLEGA LA PARTE DECIMAL DE UN NÚMERO, Y COMPLETAMOS O QUITAMOS PARA DEVOLVER EL MISMO NÚMERO REDONDEADO Y CON LA CANTIDAD DECIMALES QUE SE DESEEN
    # Básicamente sirve para rellenar o quitar los decimales de otro número
    # 024 // 4 >>> 0240
    # 12504 // 2 >>> 12
def Ajusta_Decimales(Valor, Decimales):
    Aux1 = str(Valor)
    Contador = 0
    largo = len(Aux1)
    Aux2 = ''
    while Decimales > Contador:
        Contador += 1
        if Contador > largo:
            Aux2 += '0'
        else:
            Aux2 += Aux1[Contador - 1]
    return Aux2


# SEPARA PARTE DECIMAL Y ENTERA DE UN NÚMERO FLOAT DEVOLVIENDO 2 STRING. SI VINIERA: .2 POR EJ, ENTONCES INTERPRETA 0 DE VALOR ENTERO
# 145.32 >>> 145 // 32
def Separador_Int_Float(Valor):
    AuxStr = str(Valor)
    if AuxStr[0] == '.':
        Valor = '0' + Valor
    Aux1 = str(float(Valor))
    Aux2 = ''
    Aux3 = ''
    coma = False
    for i in range(len(Aux1)):
        if coma == False:
            if Aux1[i] == '.':
                coma = True
            else:
                Aux2 += Aux1[i]
        else:
            Aux3 += Aux1[i]
    return Aux2, Aux3

# COLOCA EL PUNTO DE MIL, EN LA PARTE ENTERA DE CUALQUIER NÚMERO
# SIEMPRE DEBE VENIR UN NÚMERO ENTERO SIN PUNTOS NI COMAS
def Punto_Mil(Valor):
    # Tener en cuenta, que a ésta función la llaman desde otras donde ya se ha corroborado que el valor es numérico
    Valor = str(Valor)
    if Valor.count('.') > 0:
        Valor = float(Valor)
    aux = int(Valor)
    texto = str(aux)
    largo = len(texto)
    lista = []
    contador1 = 0
    contador2 = 0
    for i in texto:
        contador1 += 1
        contador2 += 1
        lista.append(texto[largo - contador1])
        if contador2 == 3 and contador1 < largo:
            lista.append('.')
            contador2 = 0
    lista.reverse()
    resultado = ''
    for n in range(len(lista)):
        resultado = resultado + lista[n]

    return resultado

# Quita las comas y puntos de un número
# 1.957,50 >>> 195750
def Quita_Simbol(Valor):
    Valor = str(Valor)
    Aux = ""
    Valor = Valor.replace(".", "")
    Aux = Valor.replace(",", "")
    return Aux

# Devuelve un texto en mayúsculas y sin acentos
def Normalize(Valor):
    Valor = Valor.lower()
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        Valor = Valor.replace(a, b).replace(a.upper(), b.upper())
    Valor = Valor.upper()
    return Valor


# LAS SIGUIENTES FUNCIONES TRABAJAN EN CONJUNTO.
    # SE USAN PARA LOS LINE_EDIT DE VALORES NUMÉRICOS, ESTO SIRVE PARA QUE EL USUARIO INGRESE NÚMEROS EN UN EDIT, Y SE VAYAN COMPLETANDO TODO AUTOMÁTICAMENTE.
    # SI POR EJEMPLO ES UN LINE_EDIT DONDE SE COLOCAN PRECIOS CON 2 DECIMALES, ENTONCES CON SÓLO INGRESAR POR EJEMPLO: .2 >>> AL USUARIO LE VAMOS A MOSTRAR: 0,20
    # ES NECESARIO QUE LA VENTANA TENGA UNA VARIABLE TIPO STRING, PARA QUE GUARDE DE MANERA OCULTA PARA EL USUARIO, LO QUE SE ESTÁ INGRESANDO EN EL EDIT. 
    # LA PRIMER FUNCIÓN SE ENCARGA DE COLOCAR EN DICHA VARIABLE, EL VALOR CORRECTO QUE DEBE CONTENER, Y LA SEGUNDA FUNCIÓN LE DA EL FORMATO NECESARIO PARA DICHO
    # VALOR GUARDADO.

    # EL PRIMER PASO ES PURIFICAR LOS DATOS TIPEADOS POR EL USUARIO PARA SER ALMACENADOS EN LA VARIABLE ASOCIADA AL LINE_EDIT. A ESTO LO HACEMOS CUANDO ENVIAMOS 
    # A LA FUNCIÓN Texto_A_Num1 LO TIPEADO EN EL LINE_EDIT, LA CUÁL LE DEVUELVE EL VALOR CORRECTO QUE DEBE TENER ALMACENADO, DEBIDO A LOS SIGUIENTES ERRORES QUE SE
    # PUEDAN OCASIONAR. SI POR EJEMPLO EL USUARIO INGRESARÍA LETRAS O VARIAS COMAS Y PUNTOS, ESTO DEBE PURIFICARSE Y ALMACENARSE DE MANERA CORRECTA EN LA VARIABLE
    # INDICADA PARA EL LINE_EDIT, PORQUE SI ALMACENAMOS TODO LO QUE EL USUARIO TIPEA, PODEMOS DEVOLVERLE EL VALOR CORRECTO, PERO SI EL USUARIO POR EJEMPLO TIPEA
    # ALGO COMO: LSDF,SSDF2 >>> SE LE VA A MOSTAR: 0,20. HASTA EL MOMENTO TODO BIEN, PERO SI SE HA CONFUNDIDO Y QUIERE BORRAR LA COMA PARA INGRESAR UN VALOR
    # ENTERO DELANTE, DEBE PRESIONAR 6 VECES PARA BORRAR EL NÚMERO, YA QUE TIENE ANTES DE LA COMA UNOS 6 CARACTERES QUE EL EN REALIDAD NO LOS ESTARÍA VIENDO.
    # POR ELLO ES QUE LIMPIAMOS EL TEXTO Y LO DEJAMOS ALMACENADO COMO: .2 >>> ASÍ SÓLO PRESIONA 2 VECES BACKSPACE Y YA PUEDE TIPEAR EL VALOR CORRECTO.

    # EL SEGUNDO PASO ES ENVIAR DICHA VARIABLE A LA FUNCIÓN Texto_A_Num2, QUE SE ENCARGA DE TRANSFORMARLO A LO QUE SE QUIERE MOSTAR. EN EL EJEMPLO, DICHA VARIABLE
    # RECIBE: .2 Y DEVUELVE: 0,20

    # CABE ACLARAR QUE LA FUNCION CHANGE DEL EDIT, DEBE PERMITIR TANTO PUNTOS COMO COMAS, LUEGO TRANSFORMARLAS A AMBAS EN UN ÚNICO PUNTO.
    # LOS PUNTOS MIL LOS COLOCAMOS DE ACÁ, NO ES TAREA DEL USUARIO. EL USUARIO SÓLO COLOCA UN PUNTO O UNA COMA CUANDO QUIERA INDICAR DECIMALES. 
    # SI UN NÚMERO DEBE SER ENTERO, SÓLO DE INDICARSE QUE TIENE 0 DECIMALES.
    # 145asdf5  >>>  1455

# Esta función es la que recibe del line_edit lo tipeado y devuelve un string que es lo que se debe guardar en la variable asociada al line_edit
def Line_A_Variable(Texto, Decimales = 0):
    Aux = ''
    Coma = False
    Cont = 0
    if len(Texto) > 0:
        for letra in Texto:
            if Es_Numero(letra) == True:
                if Coma == True: 
                    Cont += 1
                    if Cont <= Decimales:
                        Aux += letra
                else:
                    Aux += letra
            else:
                if (letra == ',' or letra == '.') and Coma == False:
                    Coma = True
                    Aux += '.'
    if Decimales == 0:
        Aux = Aux.replace('.','')
    return Aux

# SU EXPLICACIÓN SE ENCUENTRA EN LA FUNCION Texto_A_Num1
# Esta función recibe el valor de la variable asociada al line_edit y devuelve lo que debe mostrarse en el line_Edit
def Variable_A_Line(Texto, Decimales = 0):
    AuxEntero, AuxDecimal = Separador_Int_Float(Texto)
    AuxEntero = Punto_Mil(AuxEntero)
    if Decimales > 0:
        AuxDecimal = Ajusta_Decimales(AuxDecimal, Decimales)
        return AuxEntero + "," + AuxDecimal
    else:
        return AuxEntero

# Analiza un caracter y lo devuelve si es un entero, o si es un punto o una coma devuelve punto
# Devuelve "F" de falso si no es una de esas opciones
# A ésta función se la llama desde el keyPressEvent
def Devuelve_Entero_Signo(Caracter):
    if Es_Numero(Caracter) == True:
        return Caracter
    elif Caracter == '.' or Caracter == ',':
        return '.'
    else:
        return 'F'

print('Módulo Formatos.py cargado correctamente.')

'''
for i in range(10):
    dia = int(input())
    mes = int(input())
    ano = int(input())
    resultado = Trans_Fecha_Num(dia, mes, ano)
    print(resultado)
    print(Trans_Num_Fecha(resultado))
'''

