'''
ATENCIÓN:
Se agregó recientemente el concepto y función de "Adecua_Ruta", por ende, si alguna función arroja error se debería solucionar en el momento

Funciones que hacen referencia a la navegación dentro de las carpetas y manejo de archivos.
    Aplicable a cualquier programa

    * Busca archivos (todos o por formato específico)
    * Recorre carpetas con la posibilidad de recorrer subcarpetas
    * Mueve archivos de lugar
    * Elimina archivos
    * Devuelve información sobre los archivos

CODIGOS DEL MÓDULO os    
    * Devuelve la carpeta actual del programa
        - carpeta_actual = os.getcwd()
    
    * Crea una carpeta, en éste caso, en la carpeta actual
        - os.mkdir("Nombre_de_Carpeta")
    
    * Devuelve True/False si en cuentra una carpeta buscada, si es el path de un archivo devuelve False
        - os.path.isdir("Nombre_de_carpeta_buscada")
    
    * Devuelve información de un archivo en bytes
        - Tamaño: os.path.getsize("Archivo.exe")

    * Devuelve una LISTA con todos los archivos y carpetas
        - os.listdir("")
        - os.listdir("D:\\Programación\\Python\\Proyectos\\")
    
    * Elimina carpetas
    * Nota: Únicamente elimina carpetas que estén vacías (VER SHUTIL)
        - os.rmdir("Nombre_del_archivo")

    * Elimina archivos
        - os.unlink("Nombre_del_archivo")

CODIGOS DEL MÓDULO shutil
    * Copia archivos
        - shutil.copy("Ubicacion_completa_del_archivo","Ubicacion_destino")

    * Mueve archivos
        - shutil.move("Ubicacion_completa_del_archivo\\archivo.txt","Ubicacion_destino\\archivo.txt")
    * Al mismo tiempo, si le cambiamos el nombre al segundo parámetro lo renombramos
        - shutil.move("Ubicacion_completa_del_archivo\\archivo.txt","Ubicacion_destino\\archivo_modificado.txt")
    
    * Elimina carpetas con archivos
        - shutil.rmtree("Nombre_de_la_carpeta")
'''
import os
import shutil
# plataform la utilizamos para saber en qué sistema estamos para adecuar las rutas según corresponda
import platform

# Dejamos acentado en una variable si es que estamos en windows o linux, para no tener que estar constantemente ejecutando la función de platform
WIN = False
sistema = platform.system()
if sistema == "Windows":
    WIN = True

# Recibe parámetros para realizar búsqueda de archivos o carpetas y los devuelve en una Lista.
    # Parámetros:
    # Carpeta: Es la CARPETA PRINCIPAL de donde se buscarían los archivos (Cuando se hace referencia a la CARPETA PRINCIPAL, se refiere a ésta que ingresa por parámetro).
    # SubCarpetas_VF: Con True/False, se indica si se desea mantener la búsqueda en las subcarpetas.
    # Tipo1,2,3,4 y 5: Se le puede indicar hasta 5 extenciones de archivos distintas para realizar búsquedas(xej: xls, xlsx, xlsm, etc). Si no se indican archivos incluye todos.
def Dev_Dir(Carpeta, SubCarpetas_VF = False, Tipo1 = "", Tipo2 = "", Tipo3 = "", Tipo4 = "", Tipo5 = ""):
    
    Carpeta = Adecua_Ruta(Carpeta)

    # Creamos las listas necesarias para la búsqueda
    Lista_Final = []
    Lista_AuxF = []
    Lista_AuxC = []
    Lista_AuxA = []
    Lista_Aux_Car = []
    
    # Este if es sólo verdadero si la carpeta principal existe
    if os.path.isdir(Carpeta):
        
        # Cargamos 2 listas que contienen las carpetas y archivos de la "Carpeta Principal"
        Lista_AuxC, Lista_AuxA = Dev_Carpetas_Archivos(Carpeta)
        
        # Creamos el primer dato de la lista
        Lista_AuxF = Dev_Filtrado(Carpeta, Lista_AuxA, Tipo1, Tipo2, Tipo3, Tipo4, Tipo5)
        Lista_Final.append(Lista_AuxF)
        if SubCarpetas_VF:
            
            # Preparamos y ejecutamos un bucle para recorrer todas las carpetas que hayan
            cont = 0
            Largo = len(Lista_AuxC)
            while cont < Largo:
                
                # Aunque no sea necesario porque se van a sobreescribir, limpiamos las 3 listas que vamos a utilizar en el bucle
                Lista_AuxF = []
                Lista_Aux_Car = []
                Lista_AuxA = []
                
                # Desde la lista "Lista_AuxC", obtenemos los archivos y carpetas que hay en esa lista de carpetas
                Lista_Aux_Car, Lista_AuxA = Dev_Carpetas_Archivos(Lista_AuxC[cont])
                
                # Si dentro de una carpeta se encontraron más carpetas, se agregan sus Path para luego poder recorrerlos con éste mismo bucle
                if len(Lista_Aux_Car) > 0:
                    Lista_AuxC += Lista_Aux_Car
                    # Actualizamos el valor de la variable que se usa para determinar el fin del bucle en el while
                    Largo += len(Lista_Aux_Car)
                
                # Empezamos a preparar el siguiente dato
                Lista_AuxF = Dev_Filtrado(Lista_AuxC[cont], Lista_AuxA, Tipo1, Tipo2, Tipo3, Tipo4, Tipo5)
                
                # Cargamos un nuevo dato a la lista final
                Lista_Final.append(Lista_AuxF)
                cont += 1

    return Lista_Final

# Puede eliminar tanto carpetas como archivos, en el caso de que la carpeta contenga archivos, necesita una confirmación
# Devuelve resultados en números enteros indicando: 0= Se eliminó sin problemas. 1= Hubo algún error. 2= No se eliminó por falta de confirmación
def Elimina(Direccion, Elimina_Interior_VF = False):
    # Para evitar que una falla cierre el programa, utilizamos un try
    try:
        # True: Cuando es una carpeta. False: Cuando es un archivo
        if os.path.isdir(Direccion):

            # Primero debemos determinar si es un archivo o una carpeta, luego, en caso de ser carpeta, debemos controlar si contiene archivos dentro
            Lista_Carpetas = []
            Lista_Archivos = []
            Lista_Carpetas, Lista_Archivos = Dev_Carpetas_Archivos(Direccion)

            # True: Cuando la carpeta contiene archivos. False: Carpeta vacía
            if len(Lista_Archivos) > 0:
                if Elimina_Interior_VF == True:
                    shutil.rmtree(Direccion)
                    return 0
                else:
                    return 2
            else:
                os.rmdir(Direccion)
                return 0
        else:
            os.unlink(Direccion)
            return 0
    except:
        return 1

# Los parámetros deben venir en con el path completo
def Copiar_Lista(Lista_Archivos, Destino):
    for i in Lista_Archivos:
        shutil.copy(i,Destino)

# Ambos parámetros deben venir en con el path completo
def Copiar(Archivo, Destino):
    shutil.copy(Archivo,Destino)

'''########################################################################################################################################
###########################################################################################################################################
                                FUNCIONES AUXILIARES (Internas utilizadas para ayuda de éste módulo)                                    '''

# Recibe un string y devuelve la extención en formato string sin el punto, ej: "mp3"
    # Recorre desde atrás hasta que encuentra un punto, y devuelve los caracteres recorridos
def Dev_Extencion(Texto):
    Largo = len(Texto)
    cont = 0
    while cont < Largo:
        cont += 1
        pos = 0 - cont
        if Texto[pos] == ".":
            return Texto[pos + 1:]

# Devuelve por separado el nombre del archivo y su extensión. Tener en cuenta que si viene una ruta completa su nombre formará parte de la parte "Archivo"
def Dev_Carpeta_Archivo_Extencion(Ruta):
    archivo, extension = Dev_Archivo_Extension(Ruta)
    return os.path.dirname(Ruta), archivo, extension

# Devuelve 2 variables, una con el nombre del archivo y otra con la extensión del mismo por separado.
def Dev_Archivo_Extension(Ruta):
    Ruta = os.path.basename(Ruta)
    Largo = len(Texto)
    cont = 0
    while cont < Largo:
        cont += 1
        pos = 0 - cont
        if Texto[pos] == ".":
            return Texto[0:pos], Texto[pos + 1:]

# Busca según el path indicado por parámetro y devuelve una lista de carpetas y archivos encontrados.
    # Nota1: La existencia de la carpeta debe controlarse antes de que se llame a ésta función.
    # Nota2: Las carpetas que devuelve, es con su Path completo.
def Dev_Carpetas_Archivos(Carpeta):
    # Creamos las listas donde se van a guardar los nombres de carpetas y archivos
    ListaCar = []
    ListaArc = []
    # Guardamos todos los archivos encontrados en una lista
    Lista2 = os.listdir(Carpeta)
    # Recorremos la lista para separar las carpetas de los archivos y ya quedan las listas cargadas
    Largo = len(Lista2)
    cont = 0
    while cont < Largo:
        Carpeta_Aux = Carpeta + "\\" + Lista2[cont]
        if os.path.isdir(Carpeta_Aux):
            ListaCar.append(Carpeta_Aux)
        else:
            ListaArc.append(Lista2[cont])
        cont += 1
    return ListaCar, ListaArc

# Recibe un Path de una carpeta, una lista de archivos y los parámetros para filtrar los archivos
# Devuelve una lista donde su primer elemento es el Path de la carpeta, y le siguen los archivos que coincidan con los formatos buscados, y si no especifica formatos
    # devuelve todos los archivos
def Dev_Filtrado(Carpeta, Lista, Tipo1 = "", Tipo2 = "", Tipo3 = "", Tipo4 = "", Tipo5 = ""):
    Lista_Aux = []
    Lista_Aux.append(Carpeta)
    for pos in Lista:
        if Tipo1 != "":
            Extension = Dev_Extencion(pos)
            if Extension == Tipo1:
                Lista_Aux.append(pos)
            else:
                if Tipo2 != "":
                    if Extension == Tipo2:
                        Lista_Aux.append(pos)
                    else:
                        if Tipo3 != "":
                            if Extension == Tipo3:
                                Lista_Aux.append(pos)
                            else:
                                if Tipo4 != "":
                                    if Extension == Tipo4:
                                        Lista_Aux.append(pos)
                                    else:
                                        if Tipo5 != "":
                                            if Extension == Tipo5:
                                                Lista_Aux.append(pos)
        else:
            Lista_Aux.append(pos)
    return Lista_Aux

# Recibe una ruta en forma de string, y devuelve 2 variables, la ruta y el archivo
def Dev_Carpeta_Archivo(Ruta):
    Ruta = Adecua_Ruta(Ruta)
    return os.path.dirname(Ruta), os.path.basename(Ruta)

# Funciones para evitar importar el módulo os en otras partes del programa, porque son una única línea de código
def Dev_Ruta(Ruta):
    Ruta = Adecua_Ruta(Ruta)
    return os.path.dirname(Ruta)
def Dev_Archivo(Ruta):
    Ruta = Adecua_Ruta(Ruta)
    return os.path.basename(Ruta)
def Dev_Existe_Dir(Ruta):
    return os.path.isdir(Ruta)
def Dev_Existe_File(Ruta):
    return os.path.isfile(Ruta)

# Toma cualquier Ruta que venga y la convierte para manejar un único formato, que es el de la barra invertida para separar las carpetas
def Adecua_Ruta(Ruta):
    if WIN == True:
        Ruta = Ruta.replace("/", "\\")
    else:
        Ruta = Ruta.replace("\\", "/")
    return Ruta

def Imprimimos():
    Lista = Dev_Dir(r"D:\Programación\Python\Proyectos", True, "mp3")
    for i in Lista:
        print(i)
        print()

#print(Dev_Archivo_Extencion("ñladfjkl/alsfka/imagen.jpg"))

'''
FUNCIONES ELIMINADAS, LAS GUARDO POR SI LUEGO SE DEBEN RECUPERAR
    # Recibe una ruta en forma de string, y devuelve 2 variables, la ruta y el archivo
    def Dev_Carpeta_Archivo(Ruta):
        largo = len(Ruta)
        cont = largo
        Archivo = ""
        while cont > 0:
            cont -= 1
            if Ruta[cont] == "/":
                Archivo = Ruta[cont + 1:]
                Ruta = Ruta[0:cont]
                return Ruta, Archivo
    

    # Devuelve por separado el nombre del archivo y su extensión. Tener en cuenta que si viene una ruta completa su nombre formará parte de la parte "Archivo"
    def Dev_Carpeta_Archivo_Extencion(Texto):
        Largo = len(Texto)
        cont = 0
        while cont < Largo:
            cont += 1
            pos = 0 - cont
            if Texto[pos] == ".":
                return Texto[0:pos], Texto[pos + 1:]
'''
