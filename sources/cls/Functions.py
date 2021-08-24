################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################

## ==> GUI FILE
import PyQt5
from PyQt5.QtCore import QAbstractAnimation
from App_Caja import *

'''
FUNCIONES DE CONTENIDO Y ANIMACIONES DE LOS MENÚES
    Son las funciones para expandir o contraer y mostrar los botones correspondientes con el texto correspondiente de los menúes.

    Hay un primer menú que se expande y contrae. Cuando está contraído sólo muestra un ícono, cuando se expande muestra el ícono con un texto. A su vez, a su costado contamos con otro subMenú que tiene 10 botones ya preestablecidos, donde lo que hacemos es mostrar u ocultar dichos botones.
'''
import time
class UIFunctions_Menu(MainWindow):

    '''###############################################################################################################################################################
    ###############################################################################################################################################################'''
    #                                                                   CONFIGURACIONES

    # Configura los botones existentes
    def configura_boton(self, grosor_borde=(-1), texto =(-1), tam_texto=(-1), posx=(-1), posy=(-1), ancho=(-1), alto=(-1), config_color=False, Lista_Colores=[]):
        if grosor_borde != (-1):
            self.setStyleSheet("border: {}px solid;".format(str(grosor_borde)))
        if texto != (-1):
            self.setText(texto)
        if tam_texto != (-1):
            fuente = self.font()
            fuente.setPointSize(tam_texto)
        pos1 = self.pos().x()
        pos2 = self.pos().y()
        tam1 = self.width()
        tam2 = self.height()
        cambiar = False
        if posx != (-1):
            cambiar = True
            pos1 = posx
        if posy != (-1):
            cambiar = True
            pos2 = posy
        if ancho != (-1):
            cambiar = True
            tam1 = ancho
        if alto != (-1):
            cambiar = True
            tam2 = alto
        if cambiar == True:
            self.setGeometry(pos1, pos2, tam1, tam2)
        if config_color == True:
            self.setStyleSheet("background-color: rgb({},{},{});".format(str(Lista_Colores[0]),str(Lista_Colores[1]),str(Lista_Colores[2])))

    '''###############################################################################################################################################################
    ###############################################################################################################################################################'''
    #                                                        FUNCIONES DE LOS BOTONES DEL 1ER MENU

    # Expande y contrae el Menú Ppal. Se llama a ésta función desde el 1er botón y cuando se hace clic en alguno del Menú secundario.
    def Boton_1(vtn, minWidth, maxWidth, Lista_Btns, Lista_Textos):

        # Cargamos las animaciones
        UIFunctions_Menu.sf(vtn.frame_1, minWidth, maxWidth)
        UIFunctions_Menu.sf(vtn.frame_menu1_btns, minWidth, maxWidth)

        # Colocamos la leyenda a los botones o las borramos
        ancho = vtn.frame_1.width()
        if ancho == maxWidth:
            # Configuramos los botones para ser contraídos
            for i in Lista_Btns:
                i.setText("")
        else:
            # Configuramos los botones para ser expandidos
            cont = 0
            for i in Lista_Btns:
                i.setText(Lista_Textos[cont])
                cont += 1
        '''
        # Ubicamos la posición del 2do menú
        posW1 = vtn.frame_1.width()
        posW2 = vtn.frame_2.width()
        posH2 = vtn.frame_1.width()
        vtn.frame_2.setGeometry(QtCore.QRect(posW1, 0, posW2, posH2))
        '''

    # Boton de Fijar 1
    def Boton_Op1(page):
        pass

    # Boton de Fijar 2
    def Boton_Op2(page):
        pass

    # Boton con función variable, acceso directo 2
    def Boton_Extiende_Menu2(vtn, maxWidth, btn_ant, btn_post, Lista_Btns, Lista_Textos):

        animacion = False
        borrar = False
        ancho = vtn.frame_menu2_btns.width()

        # True: Barra expandida. False: Barra contraida.
        if maxWidth == ancho:

            # True: se presiona el mismo boton. False: Boton distinto al anterior.
            if btn_ant == btn_post:
                animacion = True
                borrar = True
        else:
            animacion = True

        # Asignamos movimiento a la barra. Tener en cuenta que las respectivas funciones saben si deben contraerse o expandirse
        if animacion == True:
            UIFunctions_Menu.sf(vtn.frame_2, 0, maxWidth)
            UIFunctions_Menu.sf(vtn.frame_menu2_btns, 0, maxWidth)
        
        # Configuramos los botones para ser contraídos
        if borrar == True:
            for i in Lista_Btns:
                i.setText("")
        
        # Colocamos la leyenda a los botones para ser expandidos
        else:
            cont = 0
            max = len(Lista_Textos)
            for i in Lista_Btns:
                if cont < max:
                    i.setVisible(True)
                    i.setText(Lista_Textos[cont])
                else:
                    i.setText("")
                    i.setVisible(False)
                cont += 1
        return btn_post

    '''###############################################################################################################################################################
    ###############################################################################################################################################################'''
    #                                                        FUNCIONES DE LOS BOTONES DEL 2DO MENU

    def Seleccion_Pages(vtn, ID):
        if ID == "Carga Fondos":
            vtn.stackedWidget.setCurrentWidget(vtn.page_carga_venta)
        elif ID == "Reg. de Ventas":
            vtn.stackedWidget.setCurrentWidget(vtn.page_Reg_de_Ventas)
        elif ID == "Ventas":
            vtn.stackedWidget.setCurrentWidget(vtn.page_Ventas)
        elif ID == "Ingresos":
            vtn.stackedWidget.setCurrentWidget(vtn.page_msjs)

    '''###############################################################################################################################################################
    ###############################################################################################################################################################'''
    #                                                                FUNCIONES ADICIONALES

    '''
    def sf(vtn, minWidth, maxWidth):
        print("Expandir Menu 1")
        # Parametros:
        # vtn: debería ser el "self", es el objeto del menú a expandir, el 2do menu.
        # minWidth: es el mínimo a expandir.
        # maxWidth: es el máximo a expandir.

        # Determinamos si tenemos que expandir o contraer los botones
        ancho = vtn.width()
        fin = 0
        alto = vtn.height()
        if ancho == maxWidth:
            # Configuramos los botones para ser contraídos
            fin = minWidth
        else:
            # Configuramos los botones para ser expandidos
            fin = maxWidth

        # ANIMATION
        vtn.animation = QPropertyAnimation(vtn, b"geometry")
        vtn.animation.setDuration(200)
        vtn.animation.setEndValue(QRect(0,0,fin,alto))
        vtn.animation.start(QAbstractAnimation.DeleteWhenStopped)
    '''
    # Se encarga de configurar los botones que vienen nombrados en una lista por parametro, y luego si tiene que expandir el menu lo hace.
    def sf(menu, minWidth, maxWidth):
        print("Expandir Menu 2")
        # Parametros:
        # menu: debería ser el "self", es el objeto del menú a expandir, el 2do menu.
        # maxWidth: es el maximo a expandir, y que usamos como parámetro para controlar si ya no está en ese tamaño.
        # Lista_Btns: Son los 10 objetos, 10 botones del menu.
        # Lista_Textos: Es una lista con un max de 10 nombres, que en sí será el texto que tendran hasta 10 botones del 2do menu.

        ancho = menu.width()
        
        # GET WIDTH
        width = menu.width()
        maxExtend = maxWidth
        standard = minWidth

        # SET MAX WIDTH
        if width == minWidth:
            widthExtended = maxExtend
        else:
            widthExtended = standard
        
        # ANIMATION
        menu.animation = QPropertyAnimation(menu, b"minimumWidth")
        menu.animation.setDuration(400)
        menu.animation.setStartValue(ancho)
        menu.animation.setEndValue(widthExtended)
        menu.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        menu.animation.start()
        
    def Expande_Productos(self, maxHeight, enable):
        Inicio_btn = self.ui.push_sub2_1_reponer.height()
        Fin_btn = 0
        if enable:
            Inicio_btn = 0
            Fin_btn = 60
            self.ui.push_sub2_1_reponer.setVisible(True)
            self.ui.push_sub2_2_promo.setVisible(True)
            self.ui.push_sub2_3_cargar_prod.setVisible(True)
        else:
            self.ui.push_sub2_1_reponer.setVisible(False)
            self.ui.push_sub2_2_promo.setVisible(False)
            self.ui.push_sub2_3_cargar_prod.setVisible(False)

        self.anima1 = QPropertyAnimation(self.ui.push_sub2_1_reponer, b"minimumHeight")
        self.anima2 = QPropertyAnimation(self.ui.push_sub2_2_promo, b"minimumHeight")
        self.anima3 = QPropertyAnimation(self.ui.push_sub2_3_cargar_prod, b"minimumHeight")
        self.anima1.setDuration(400)
        self.anima2.setDuration(400)
        self.anima3.setDuration(400)
        self.anima1.setStartValue(Inicio_btn)
        self.anima2.setStartValue(Inicio_btn)
        self.anima3.setStartValue(Inicio_btn)
        self.anima1.setEndValue(Fin_btn)
        self.anima2.setEndValue(Fin_btn)
        self.anima3.setEndValue(Fin_btn)
        self.anima1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.anima2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.anima3.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.anima1.start()
        self.anima2.start()
        self.anima3.start()
