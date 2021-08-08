''' 
PLANTILLA PARA LISTAS

    AYUDAMEMORIA > FUNCIONES:
    Setea()
    Carga_Lista()
    Refresca_Lista()
    Elimina_Registro(Pos)
    Elimina_Lista(Valores=False)
    Agrega_Item_Final(Lista)
    
    Seleccion(Col)
    Actualiza_Lista()
    Configuracion()

    QUÉ ES:
        Es una plantilla de ejemplo que contiene 5 listwidgets y una barra lateral para desplazar los datos de los listwidgets.

    OBJETIVO:
        Su finalidad es la de evitar el problema de que cada listwidget es independiente de sus listas vecinas, que utilizo cuando hay tablas extensas o variables de datos con 
        varias columnas. Colocar varias listas pegadas pero que muestran datos relacionados entre sí como por ejemplo, los datos de productos que se venden, generan 
        dificultades visuales y de operatoria, cuando la cantidad de ítems superan el tamaño físico de la lista. De ésta manera, sólo importamos ésta clase y nos desligamos de 
        dicho problema.

    FORMA DE TRABAJAR:
        Le llega por parámetro una lista de listas, donde cada una de esas sublistas representa un registro de la tabla a mostrar. La clase contiene funciones para hacer las 
        tareas habituales que se pueden realizar en la tabla, pero tener en cuenta que otras tareas no puede ejecutarse desde acá porque no retornamos valores. Es decir, que si 
        por ej se quiere borrar un registro, aquí se recibe el valor de guía del mismo o bien se refresca la tabla con una nueva lista donde la misma ya viene actualizada con 
        dicho valor eliminado.
        Los datos que se ven en pantalla están cargados en una lista global llamada self.LISTA_GENERAL, la cuál puede ser accedida desde fuera como utilizando los métodos de 
        setters.

    FUNCIONES DE ACCESO EXTERNO:
        >> Setea:                           Setea los valores de variables para la correcta visualización de la tabla.
        >> Refresca_Lista:                  Elimina sólo los datos en pantalla para luego volver a cargar los datos que están en la self.LISTA_GENERAL.
        >> Elimina_Item(id = -1, quita_sel = True): Elimina sólo un ítem de la self.LISTA_GENERAL y de la tabla. Permite que se venga con la identificación por parámetro.
        >> Elimina_Lista(Valores=False):    Limpia todos los valores de la tabla en pantalla y por parámetro podemos indicar que también elimine los datos de la lista ppal 
                                            (self.LISTA_GENERAL).
        >> Agrega_Item_Final(Lista):        Le llega una lista y la agrega como un nuevo registro tanto en la self.LISTA_GENERAL como en la tabla en pantalla.

        >> Seleccion_Listas(Col):           Selecciona el mismo ítem en todas las listas, que el que se ha seleccionado en la Columna que viene indicada por parámetro.
        >> Quita_Seleccion:                 Luego de realizar una actividad que implicó seleccionar un registro, podemos llamar a ésta función que deja deseleccionado todo.
    
    FUNCIONES INTERNAS:
        >> Actualiza_Lista:                 Se encarga de mostrar en pantalla lo que respecta a los datos visibles de la tabla, ya que cuando los ítems superan la cantidad que 
                                            puede ser mostrada debemos limitar la cantidad de ítems en pantalla.
        >> Configuracion:                   Una vez seteado los datos, se configura la tabla entera.

    VARIABLES:
        self.UBICACION      bool >> True: Cada vez que se agrega ítems que supera el TOPE, se muestra el final de la lista. False: No se modifica la actividad.
        self.SIZE_ANCHO     int  >> Es el ancho de toda la tabla, incluyendo la barra vertical.
        self.SIZE_ALTO      int  >> El alto de la tabla.
        self.LISTA_PORC     int  >> Es una lista que contiene un dato por cada listWidgets, donde indican el porcentaje de ancho que deben tener las listas en función al ancho 
                                    que hay en total, la suma de éstos debe dar 100 y el ancho de la barra siempre será fijo.
        self.SIZE_LETRA     int  >> Es el tamaño de la letra actual, a partir de ella se calculan otros datos para reajustar los datos en pantalla.
        self.LISTA_GENERAL  Lista>> Es la lista que contienen las listas que cada una de esas representan los registros. pos=0 Es un id del tipo string, sobretodo para las 
                                    eliminaciones, ya que pueden haber varios registros relacionados, y si comparten el ID entonces eliminamos a todos con un sólo llamado a la 
                                    función. También se pueden desplegar sublistas más a futuro.

    VARIABLES CONSTANTES:
        Si bien dichas variables puede que en algún momento se modifiquen por el usuario, ahora necesito que sean constantes o que se calculen automáticamente.
        self.LETRA          string  >>   Letra utilizada en las listas. Se usa una genérica por el momento ya que tenemos sus valores de tamaños y así podemos actualizar los 
                                        demás datos en función a los datos que ya tenemos recopilados.
        self.TOPE           int     >>  La cantidad de ítems que se pueden mostrar en función al tamaño de las listas. Recordar dejar un renglón para la barra de desplazamiento 
                                        que aparece automáticamente cuando un ítem supera el ancho que se muestra en pantalla, suele ocupar un renglón.
        self.INICIO_TABLA   int     >>  Indica cuál es el primer valor que se debe cargar en la tabla, en función a la cantidad que se pueden mostrar y el total de items.
'''

from PyQt5 import QtGui, QtWidgets
import copy

class Tabla_Propia(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super(Tabla_Propia, self).__init__(parent)

        self.UBICACION = False
        self.SIZE_ANCHO = int
        self.SIZE_ALTO = int
        self.LISTA_PORC = int
        self.SIZE_LETRA = int
        self.LETRA = ""
        self.TOPE = int
        self.INICIO_TABLA = 0
        self.LISTA_GENERAL = []
        self.ValorClave = 1.9
        
        self.initUI()

        self.Lista1.clicked.connect(lambda: self.Seleccion_Listas(1))
        self.Lista2.clicked.connect(lambda: self.Seleccion_Listas(2))
        self.Lista3.clicked.connect(lambda: self.Seleccion_Listas(3))
        self.Lista4.clicked.connect(lambda: self.Seleccion_Listas(4))
        self.Lista5.clicked.connect(lambda: self.Seleccion_Listas(5))
    
    def initUI(self):
        self.Lista1 = Lista(self)
        self.Lista2 = Lista(self)
        self.Lista3 = Lista(self)
        self.Lista4 = Lista(self)
        self.Lista5 = Lista(self)
        self.Scroll = Barra(self)
    
    def Setea(self, Ancho, Alto, Porcentajes, SizeLetra, Ubicacion):
        self.UBICACION = Ubicacion
        self.SIZE_ANCHO = Ancho
        self.SIZE_ALTO = Alto
        self.LISTA_PORC = Porcentajes
        self.SIZE_LETRA = SizeLetra
        Aux = Ancho - 25

        self.Scroll.setGeometry(self.SIZE_ANCHO - 25, 0, 25, self.SIZE_ALTO)
        
        Valor = (Aux/100)*Porcentajes[0]
        Ubi = 0
        self.Lista1.setGeometry(0,0,Valor,Alto)
        Ubi += Valor
        Valor = (Aux/100)*Porcentajes[1]
        self.Lista2.setGeometry(Ubi,0,Valor,Alto)
        Ubi += Valor
        Valor = (Aux/100)*Porcentajes[2]
        self.Lista3.setGeometry(Ubi,0,Valor,Alto)
        Ubi += Valor
        Valor = (Aux/100)*Porcentajes[3]
        self.Lista4.setGeometry(Ubi,0,Valor,Alto)
        Ubi += Valor
        Valor = (Aux/100)*Porcentajes[4]
        self.Lista5.setGeometry(Ubi,0,Valor,Alto)

        font = QtGui.QFont()
        font.setPointSize(SizeLetra)
        self.Lista1.setFont(font)
        self.Lista2.setFont(font)
        self.Lista3.setFont(font)
        self.Lista4.setFont(font)
        self.Lista5.setFont(font)

        # Calculamos la cantidad de renglones a mostrar en función al valor clave que traduce el tamaño de la letra a la cant de renglones que podrían entrar. Al final se le 
            # resta un valor debido a que se reserva espacio para la barra horizontal que aparece sola.
        self.TOPE = int((Alto / (self.ValorClave * SizeLetra)) - 1)

    def Refresca_Lista(self):
        self.Elimina_Lista()
        cont = 0
        for i in self.LISTA_GENERAL:
            if cont >= self.INICIO_TABLA and cont < (self.INICIO_TABLA + self.TOPE):
                self.Lista1.addItem(i[1])
                self.Lista2.addItem(i[2])
                self.Lista3.addItem(i[3])
                self.Lista4.addItem(i[4])
                self.Lista5.addItem(i[5])
            cont += 1

    def Elimina_Item(self, id="", pos=-1, selec=True, del_latest=True, quita_sel = True):
        # Devuelve el identificador que ha eliminado, ya que ésta clase detecta cuál ítem fue seleccionado o no. Esta bandera indica qué se devuelve
        eliminado = False

        # Cuando se llama a la función de manera directa con una "señal", sucede que el id = False, cuando debería quedar vacío, así que lo reajusto ya que es imposible que un 
        # identificador sea False, podemos sin problema editarlo
        if id == False: id = ""
        
        # PASO 1: El id viene por parámetro o lo busca y lo establece la función.
        # PASO 2: Una vez identificado el o los ítems a borrar, se eliminan todos aquellos que contengan dicho id.

        # PARAMETROS:
            # id            string  Es el identificador, el 1er dato de cada sublista de LISTA_GENERAL.
            # pos           int     Si no hay id, puede venir la posición del ítem a borrar. A partir de ahí se determina el id que contiene esa posición.
            # selec         bool    V-F Por defecto, cuando no hay id ni pos, busca lo seleccionado.
            # del_latest    bool    V-F indicando que si no viene ningún parámetro para la identificación, va a obtener el id del último ítem.
            # quita_sel     bool    V-F al terminar la eliminación se quita la selección que haya tenido la lista. Por defecto siempre se hace pero se puede evitar por parámetro
        
        # PASO 1
        # Bandera para indicar que ya se encontró la pos
        encontrado = False
        # Control: Si viene el id por parámetro directamente pasamos a eliminar los ítems. Aquí ingresamos a la obtención del id en caso de que no haya.
        if id == "":
            # True: Vino la posición por parámetro. False: Hay que encontrar la pos.
            if pos >= 0:
                id = self.LISTA_GENERAL[pos][0]
            else:
                if selec == True:
                    pos = self.Lista1.currentRow()
                    if pos >= 0:
                        id = self.LISTA_GENERAL[pos][0]
                        encontrado = True
                if encontrado == False and del_latest == True:
                    cantidad = self.Lista1.count()
                    if cantidad > 0:
                        pos = self.Lista1.count() - 1
                        id = self.LISTA_GENERAL[pos][0]
                        quita_sel = False

        # PASO 2
        # Una vez que sabemos el id del o los elementos que hay que eliminar, los quitamos
        if id != "":
            # Bucle para recorrer todas las listas y buscar las que coinciden con el id y eliminar los ítems
            cont = 0
            largo = len(self.LISTA_GENERAL)
            while cont < largo:
                if self.LISTA_GENERAL[cont][0] == id:
                    self.LISTA_GENERAL.pop(cont)
                    self.Lista1.takeItem(cont)
                    self.Lista2.takeItem(cont)
                    self.Lista3.takeItem(cont)
                    self.Lista4.takeItem(cont)
                    self.Lista5.takeItem(cont)
                    cont = 0
                    largo = len(self.LISTA_GENERAL)
                    eliminado = True
                else:
                    cont += 1
        if quita_sel == True:
            self.Quita_Seleccion()
        if eliminado == True:
            return id
        else:
            return False


    def Elimina_Lista(self, Valores=False):
        self.Lista1.clear()
        self.Lista2.clear()
        self.Lista3.clear()
        self.Lista4.clear()
        self.Lista5.clear()
        if Valores == True:
            self.LISTA_GENERAL = []

    def Agrega_Item_Final(self, Lista):
        # Actualizamos la lista general
        self.LISTA_GENERAL.append(Lista)
        
        # Actualizamos la tabla en pantalla, si es que debe aparecer en función a sus variables
        largo = len(self.LISTA_GENERAL)
        if largo > self.TOPE:
            if self.UBICACION == True:
                self.INICIO_TABLA = largo - self.TOPE + 1
                self.Refresca_Lista()
        else:
            self.Lista1.addItem(Lista[1])
            self.Lista2.addItem(Lista[2])
            self.Lista3.addItem(Lista[3])
            self.Lista4.addItem(Lista[4])
            self.Lista5.addItem(Lista[5])

    def Seleccion_Listas(self, Col):
        pos = -1
        if Col == 1:
            pos = self.Lista1.currentRow()
        elif Col == 2:
            pos = self.Lista2.currentRow()
        elif Col == 3:
            pos = self.Lista3.currentRow()
        elif Col == 4:
            pos = self.Lista4.currentRow()
        elif Col == 5:
            pos = self.Lista5.currentRow()
        
        self.Lista1.setCurrentRow(pos)
        self.Lista2.setCurrentRow(pos)
        self.Lista3.setCurrentRow(pos)
        self.Lista4.setCurrentRow(pos)
        self.Lista5.setCurrentRow(pos)

    def Quita_Seleccion(self):
        if self.Lista1.currentRow() >= 0:
            self.Lista1.setCurrentRow(-1)
            self.Lista2.setCurrentRow(-1)
            self.Lista3.setCurrentRow(-1)
            self.Lista4.setCurrentRow(-1)
            self.Lista5.setCurrentRow(-1)



class Lista(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        QtWidgets.QListWidget.__init__(self, parent)

class Barra(QtWidgets.QScrollBar):
    def __init__(self, parent=None):
        QtWidgets.QScrollBar.__init__(self, parent)