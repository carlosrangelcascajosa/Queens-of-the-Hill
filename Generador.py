import Objeto
import Regla
import SistemaMembrana

def generador(num_valquirias=10, num_elementos=7,max_conexiones=4, alfabeto=['a','b','c','d','e'], max_objetos=5, max_num_obj_lhs=3, max_num_obj_rhs=3, max_num_obj_padre=2, max_num_obj_hijas=2, max_reglas=10, max_timer=5):
    
    """
        Método para generar aleatoriamente una serie de valquirias

        Args:
        - num_valquirias (int): Número de valquirias a generar
        - num_elementos (int): Número máximo de membranas por valquiria
        - max_conexiones (int): Número máximo de membranas hijas permitido por membrana
        - alfabeto (list): Alfabetos sobre los que definir los multiconjuntos de objetos
        - max_objetos (int): Número máximo de objetos en los multiconjuntos de objetos de cada membrana
        - max_num_objetos_lhs (int): Máximo número de objetos en la parte izquierda LHS de la regla
        - max_num_obj_rhs (int): Máximo número de objetos en la parte derecha RHS de la regla enviados a la misma membrana
        - max_num_obj_padre (int): Máximo número de objetos en la parte derecha RHS de la regla enviados a la membrana padre
        - max_num_obj_hijas (int): Máximo número de objetos en la parte derecha RHS de la regla enviados a una membrana hija
        - max_reglas (int): Máximo número de reglas por membrana
        - max_timer (int): Máximo timer permitido sobre los objetos $\delta_t, \bar \delta_t$

        Return:
        - lista_estructuras (list): lista de estructuras de las valquirias generadas
        - lista_objetos (list): lista de los multiconjuntos de objetos de las valquirias generadas
        - lista_reglas (list): lista de los conjuntos de reglas de las valquirias generadas.
    """
    
    lista_estructuras=[]
    lista_objetos=[]
    lista_reglas=[]
    for _ in range(0,num_valquirias):
        estructura=generar_estructura(num_elementos, max_conexiones)
        lista_estructuras = lista_estructuras + [estructura]
        lista_objetos=lista_objetos + [generar_objetos(estructura, alfabeto, max_objetos)]
        lista_reglas=lista_reglas + [generar_reglas(estructura, alfabeto, max_num_obj_lhs, max_num_obj_rhs, max_num_obj_padre, max_num_obj_hijas, max_reglas, max_timer)]
    return lista_estructuras, lista_objetos, lista_reglas

import random

def generar_estructura(num_elementos, max_conexiones):

    """
        Método para generar aleatoriamente una estructura de membranas

        Args:
        - num_elementos (int): Número máximo de membranas del sistema generado
        - max_conexiones (int): Número máximo de membranas hijas de una membrana del sistema generado

        Returns:
        - estructura (dict): Estructura de un sistema generado aleatoriamente con los límites establecidos
    """

    estructura = {0:[1]}   #inicializamos una estructura con unaúnica membrana
    iterador=2 #inicializamos las etiquetas de las membranas a 2, ya que 0 y 1 ya han sido utilizadas
    clave=[1] #membranas que se usarán para añadir conexiones
    while(iterador<num_elementos):   #mientras que no superemos el número máximo de membranas del sistema
        parar=True
        clave_aux=[]
        for elemento in clave:
            #determinamos el número de membranas hijas para el elemento actual
            if(abs(iterador-num_elementos)<max_conexiones):   #no establecemos un número de membranas hijas que haga superar el número de membranas permitido en la estructura generada
                num_membranas=random.randint(0, num_elementos-iterador)
            else:
                num_membranas=random.randint(0, max_conexiones)
            estructura[elemento]=[]  #inicializamos la lista vacía de membranas hijas para el elemento actual
            for _ in range(num_membranas):
                estructura[elemento]=estructura[elemento]+[iterador]   #añadimos nuevas membranas hijas a la membrana actual
                clave_aux=clave_aux+[iterador] #añadimos la nueva membrana para poder generar membranas hijas sobre ella también
                iterador=iterador+1
        for elemento in clave: 
            if(estructura[elemento]!=[]): 
                parar=False
        if(parar==True): #si no han podido añadirse más membranas hijas, paramos
            break
        clave=clave_aux
    
    for est in list(estructura.keys()):  #eliminamos por formato de la estructura las membranas que no tienen membranas hijas
        if(estructura[est]==[]):
            del estructura[est]
                
    return estructura






def generar_objetos(estructura, alfabeto, max_objetos):


    """
        Método para generar aleatoriamente los multiconjuntos de objetos de un sistema de membranas

        Args:
        - estructura (dict): Estructura del sistema de membranas
        - alfabeto (list): Alfabetos sobre los que definir los multiconjuntos de objetos
        - max_objetos(int): Máximo número de objetos en cada membrana

        Returns:
        - multiconjunto (dict): Multiconjuntos de objetos de un sistema generado aleatoriamente con el alfabeto y límites establecidos
    """

    multiconjunto={0:[]}
    lista_membranas=list(set(list(estructura.keys())+sum(list(estructura.values()),[])))  #obtenemos las diferentes membranas de la estructura de membranas
    lista_membranas.remove(0)
    for membrana in lista_membranas:
        multiconjunto[membrana]=[]
        numero=random.randint(0, max_objetos)   #seleccionamos un número de objetos para el conjunto
        for _ in range(numero):
            objeto=random.choice(alfabeto)  #obtenemos un elemento del alfabeto aleatoriamente y lo añadimos al multiconjunto de objetos de la membrana
            multiconjunto[membrana]=multiconjunto[membrana]+[Objeto.Objeto(objeto)]
    return multiconjunto

def generar_reglas(estructura, alfabeto, max_num_obj_lhs=3, max_num_obj_rhs=3, max_num_obj_padre=2, max_num_obj_hijas=2, max_reglas=10, max_timer=5):


    """
        Método para generar aleatoriamente los conjuntos de reglas de un sistema de membranas

        Args:
        - estructura (dict): Estructura del sistema de membranas
        - alfabeto (list): Alfabetos sobre los que definir los multiconjuntos de objetos
        - max_num_objetos_lhs (int): Máximo número de objetos en la parte izquierda LHS de la regla
        - max_num_obj_rhs (int): Máximo número de objetos en la parte derecha RHS de la regla enviados a la misma membrana
        - max_num_obj_padre (int): Máximo número de objetos en la parte derecha RHS de la regla enviados a la membrana padre
        - max_num_obj_hijas (int): Máximo número de objetos en la parte derecha RHS de la regla enviados a una membrana hija
        - max_reglas (int): Máximo número de reglas por membrana
        - max_timer (int): Máximo timer permitido sobre los objetos $\delta_t, \bar \delta_t$

        Returns:
        - reglas (list): Conjunto de objetos de la clase Regla generados aleatoriamente con el alfabeto y límites establecidos.
    """
        
    rhs=alfabeto+['delta','anti-delta']
    lista_membranas=list(set(list(estructura.keys())+sum(list(estructura.values()),[])))
    lista_membranas.remove(0)
    reglas=[]
    t=0
    for membrana in lista_membranas:
        num_reglas=random.randint(0, max_reglas)
        for regla in range(num_reglas):
            obj_lhs=[]
            obj_rhs=[]
            obj_padre=[]
            obj_hija=[]
            for _ in range(random.randint(1,max_num_obj_lhs)):
                nombre=random.choice(alfabeto)
                if(nombre=='delta'):
                    t=random.randint(0, max_timer)
                elif(nombre=='anti-delta'):
                    t=random.randint(1, max_timer)
                obj_lhs=obj_lhs + [Objeto.Objeto(nombre, timer=t)]
            for _ in range(random.randint(1,max_num_obj_rhs)):
                nombre=random.choice(rhs)
                if(nombre=='delta'):
                    t=random.randint(0, max_timer)
                elif(nombre=='anti-delta'):
                    t=random.randint(1, max_timer)
                obj_rhs=obj_rhs + [Objeto.Objeto(nombre, timer=t)]
            for _ in range(random.randint(0,max_num_obj_padre)):
                nombre=random.choice(rhs)
                if(nombre=='delta'):
                    t=random.randint(0, max_timer)
                elif(nombre=='anti-delta'):
                    t=random.randint(1, max_timer)
                obj_padre=obj_padre + [Objeto.Objeto(nombre, timer=t)]
            if(membrana in estructura):
                for _ in range(random.randint(0,max_num_obj_hijas)):
                    nombre=random.choice(rhs)
                    if(nombre=='delta'):
                        t=random.randint(0, max_timer)
                    elif(nombre=='anti-delta'):
                        t=random.randint(1, max_timer)
                    obj_hija=obj_hija + [Objeto.Objeto(nombre, timer=t)]
            reglas=reglas+[Regla.Regla(membrana, obj_lhs, obj_rhs, obj_padre, obj_hija)]
    return reglas
            
            
            

    