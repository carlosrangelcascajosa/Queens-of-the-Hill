import Objeto as Objeto
import copy
import random
import utils
class Regla:
    id=1 #variable de la clase para generar un identificador a cada regla de manera automática
    def __init__(self, membrana, entrada, salida=[], salida_membrana_padre=[], salida_membrana_hija=[]):
        """
        Inicializa una instancia de la clase Regla.

        Args:
        - membrana (int): Etiqueta de la membrana a la que se aplica la regla.
        - entrada (list): Lista de objetos de tipo Objeto que son necesarios para que la regla sea aplicable.
        - salida (list, opcional): Lista de objetos de tipo Objeto que se generarán como salida de la regla.
        - salida_membrana_padre (list, opcional): Lista de objetos de tipo Objeto que se enviarán a la membrana padre al aplicar la regla.
        - salida_membrana_hija (list, opcional): Lista de objetos de tipo Objeto que se enviarán a una membranas hija al aplicar la regla.
        """
        
        
        
        
        self.membrana = membrana
        self.entrada = entrada
        self.salida = salida
        self.salida_membrana_padre = salida_membrana_padre
        self.salida_membrana_hija = salida_membrana_hija
        self.id=Regla.id
        Regla.id+=1



        

    def __str__(self):
        """
        Devuelve una representación en cadena de la regla utilizando la función regla_a_string del módulo utils.
        """
        return utils.regla_a_string(self)
    
    def __repr__(self):
        """
        Devuelve una representación en cadena de la regla utilizando la función regla_a_string del módulo utils.
        """
        return utils.regla_a_string(self)
    
    
        
    def es_aplicable3(self,sistema):


        """
        Verifica si la regla es aplicable a una configuración de un sistema. Para ello, se comprueba que la membrana de aplicación de la regla
        aparezca en el sistema y que la lista de objetos de entrada de la regla estén presentes en el interior de la membrana en la que se aplica la regla

        Args:
        - sistema (SistemaMembrana): Objeto del tipo SistemaMembrana en el que se verifica la aplicabilidad de la regla.

        Returns:
        - bool: True si la regla es aplicable, False en caso contrario.
        """


        if self.membrana in sum(list(sistema.estructura.values()), []): #  En la estructura de membranas aparece una membrana etiquetada por i
            copia=copy.deepcopy(sistema.objetos[self.membrana])  #para comprobar que todos los objetos estén y se den las multiplicidades correspondientes, generamos una copia del sistema 
            for objeto in self.entrada: #comprobamos la existencia de todos los objetos con sus correspondientes multiplicidades
                if(objeto.objeto_en_lista(copia)):
                    copia=objeto.eliminar_objeto_lista3(copia)    #eliminamos de la copia progresivamente para garantizar las correspondientes multiplicidades
                else:
                    return False
        else:
            return False
            
        return True
    

                    
    
    def aplicar(self, sistema):
        """
        Aplica la regla en el sistema dado.

        Args:
        - sistema (SistemaMembrana): Objeto del tipo SistemaMembrana en el que se aplica la regla.

        Returns:
        - dict: Diccionario que contiene los ids de los objetos generados como resultado de aplicar la regla.
        """
        dict_genera={} #creamos una estructura en la que almacenaremos los ids de los objetos que generan cada objeto, estructura que nos permitirá estudiar la computación realizada
        if self.es_aplicable3(sistema):  #comprobamos si la regla es aplicable
            lista_genera=[]
            for elemento in self.entrada:     #eliminamos del conjunto de objetos los objetos necesarios para aplicar la regla
                id=elemento.eliminar_objeto_lista(sistema.objetos[self.membrana])
                lista_genera.append(id)
            if sistema.objetos[self.membrana]==None:   #si se queda vacio, el valor del diccionario conjunto para esa membrana pasa a None: volver a ponerlo lista vacia
                sistema.objetos[self.membrana]=[]
            if self.salida is not []: #si se envian objetos a la membrana de aplicación de la regla
                for objeto in self.salida:
                    añadir=[Objeto.Objeto(objeto.nombre,objeto.membrana_genera,objeto.timer)] #creamos una instancia del objeto para que tenga un nuevo id. La membrana que genera el objeto es la membrana de aplicación de la regla.
                    dict_genera[añadir[0].id]=lista_genera  #el objeto ha sido creado por los objetos de entrada de la regla
                    sistema.objetos[self.membrana]=sistema.objetos[self.membrana] + añadir
            if self.salida_membrana_padre is not []:  #si se envian objetos a la membrana padre
                padre=sistema.obtener_padre(self.membrana) #obtenemos la etiqueta de la membrana padre
                for objeto in self.salida_membrana_padre: #recorremos los objetos y los añadimos en la membrana padre del sistema. Almacenamos los identificadores de los objetos que generan la regla (LHS)
                    añadir=[Objeto.Objeto(objeto.nombre,objeto.membrana_genera,objeto.timer)]
                    dict_genera[añadir[0].id]=lista_genera
                    sistema.objetos[padre]=sistema.objetos[padre]+añadir
            if self.salida_membrana_hija is not []: #si se envian objetos a una membrana hija
                if(self.membrana in sistema.estructura): # si la membrana presenta membranas hijas
                    for objeto in self.salida_membrana_hija:
                        hijo=random.choice(sistema.estructura[self.membrana])  #seleccionamos una membrana hija de manera no determinista
                        añadir=[Objeto.Objeto(objeto.nombre,objeto.membrana_genera,objeto.timer)]
                        dict_genera[añadir[0].id]=lista_genera  #almacenamos los identificadores de los objetos que generan a cada objeto
                        sistema.objetos[hijo]=sistema.objetos[hijo]+añadir
                else:  #en estos sistemas, si un objeto con la etiqueta in aparece en RHS de la regla y la membrana no contiene membranas hijas, este objeto se envía a la membrana de aplicación de la regla.
                    for objeto in self.salida_membrana_hija:
                        añadir=[Objeto.Objeto(objeto.nombre,objeto.membrana_genera,objeto.timer)]
                        dict_genera[añadir[0].id]=lista_genera   #almacenamos los identificadores de los objetos que generan a cada objeto
                        sistema.objetos[self.membrana]=sistema.objetos[self.membrana]+añadir


        return dict_genera  
                    
                    

            