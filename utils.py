import copy
import SistemaMembrana
import Objeto
import Regla
import time
import re
import random

def obtener_estructura(string):
    """
        Método de parseo para definir la estructura de una valquiria con la notación descrita en el capítulo 4
    
        Args:
        - string (str): Cadena con la representación con corchetes de la estructura de un sistema

        Returns:
        - dict: Diccionario que define la estructura de un sistema en la clase SistemaMembrana.
    """

     # Inicializamos contadores y un set para los números
    contador_corchete_abierto = 0
    contador_corchete_cerrado = 0
    contador_comilla = 0
    numeros = set()
    
    # Iteramos sobre cada caracter de la cadena
    i = 0
    while i < len(string):
        caracter = string[i]
        if caracter == '[':
            contador_corchete_abierto += 1
        elif caracter == ']':
            contador_corchete_cerrado += 1
        elif caracter == "'":
            contador_comilla += 1
        elif caracter.isdigit():
            # Recolectamos todos los dígitos consecutivos como un solo número
            numero = ''
            while i < len(string) and string[i].isdigit():
                numero += string[i]
                i += 1
            numeros.add(numero)
            continue  # Para evitar incrementar dos veces en el mismo ciclo
        else:
            # Si encontramos un caracter no permitido
            raise ValueError("Estructura incorrecta")
            
            
        i += 1
    
    # Verificamos si todos los contadores son iguales
    contador_numeros = len(numeros)
    if((contador_corchete_abierto == contador_corchete_cerrado == contador_comilla == contador_numeros)):     # Verificamos si todos los contadores son iguales

    



        string = "".join(string.split()) #eliminamos espacios en blanco en la estructura
        string
        posicionesabrir=[]
        for i in range(len(string)): #buscamos las posiciones de las aperturas de corchetes
            if string[i]=='[':
                posicionesabrir.append(i)
        posicionesabrir
        diccionariocontenidos={}

        for i in posicionesabrir:
            acum1=0
            acum2=0
            for e in range(i+1,len(string)): #para cada una de las posicioens de apertura de un corchete, buscamos cuál es el corchete de cierre de la membrana, que es el siguiente corchete sin un corchete de apertura previo.
                if string[e]=="[":
                    acum1=acum1+1
                elif string[e]=="]":
                    acum2=acum2+1
                if acum2>acum1:  #obtenemos la etiqueta de la membrana y los contenidos entre corchete, que representan el interior de cada membrana
                    diccionariocontenidos[int(string[e+2])]=sorted(re.findall(r'\d+', string[i:e+1]))
                    break
        listadelistas=[]
        for i  in diccionariocontenidos.keys(): #procesamos el interior de cada una de las membranas para determinar en el interior de qué membrana está cada membrana
            pertenece=0
            minimo=int(max(diccionariocontenidos.keys())+1)
            for e in diccionariocontenidos.keys():
                if (str(i) in diccionariocontenidos[e]) and len(diccionariocontenidos[e])<minimo:
                    minimo = len(diccionariocontenidos[e])
                    pertenece=e
            listadelistas.append([i,pertenece])

        estructura={}
        #generamos el diccionario con la estructura, donde cada clave representa una membrana y el valor es una lista de membranas hijas
        for e in listadelistas:
            if e[1] in estructura:
                estructura[e[1]].append(e[0])
            else:
                estructura[e[1]]=[e[0]]
        return estructura    
    else:
        raise ValueError("Estructura incorrecta")




def obtener_multiconjuntos_iniciales(stringmultilinea):

    """
        Método de parseo para obtener los diferentes multiconjuntos iniciales presentados en un fichero con la notación de pLingua
    
        Args:
        - stringmultilinea (str): Cadena multilinea donde cada línea representa el multiconjunto de objetos de una membrana

        Returns:
        - dict: Diccionario que define los multiconjuntos de objetos de un sistema en la clase SistemaMembrana.
    """


    diccionariomulticonjuntos={}
    lineas = stringmultilinea.splitlines()
    for linea in lineas:
        linea = linea.replace("@ms(", "")
        diccionariomulticonjuntos[int(linea[0])]=[elemento.strip() for elemento in linea[linea.find("=")+1:].split(',')] #dividimos la cadena de por las comas y obtenemos los objetos de la clase Objeto en función al nombre dado
    return diccionariomulticonjuntos

  

def conteo(sistema, membrana):
    """
        Método de conteo para obtener la cantidad de pares $\delta_t, \bar \delta_t$ que coexisten en el interior de una membrana en una configuración de sistema dada
    
        Args:
        - sistema (SistemaMembrana): configuración del sistema en la que buscar los pares de objetos $\delta_t, \bar \delta_t$ 
        - membrana (int): Etiqueta de la membrana para la que queremos obtener los pares de objetos $\delta_t, \bar \delta_t$ 

        Returns:
        - dict: Diccionario que almacena la cantidad de objetos $\delta_t, \bar \delta_t$ para cada timer presente en la configuración del sistema.
                Las claves de este diccionario son los distintos timers presentes en la configuración y los valores son una lista de dos elementos, cuya 
                primera posición contiene el número de objetos $\delta_t$ y la segunda posición contiene el número de objetos $\bar \delta_t$ 
    """
    dict={}
    for objeto in sistema.objetos[membrana]: #recorremos los diferentes objetos de la membrana
        if objeto.nombre=='delta' and objeto.timer!=0: 
            if objeto.timer in dict: #si ya teníamos algún objeto para ese timer
                dict[objeto.timer]= (dict[objeto.timer][0] + 1, dict[objeto.timer][1]) 
            else: #si no teníamos aún ningún objeto para ese timer, establecemos a 1.
                dict[objeto.timer] = (1,0)
        elif objeto.nombre=='anti-delta':
            if objeto.timer in dict:
                dict[objeto.timer]= (dict[objeto.timer][0], dict[objeto.timer][1]+1) 
            else:
                dict[objeto.timer] = (0,1)
            
    return dict


                
def redefinir_reglas(conjunto_reglas):
    """
        Método para especificar la membrana que genera un objeto al aplicar una regla, que se corresponde con la membrana de aplicación de la regla
    
        Args:
        - conjunto_reglas (list): Lista con las distintas reglas del sistema

        Returns:
        - dict: Lista con las distintas reglas del sistema en la que el atributo de la membrana que genera los objetos de RHS ha sido establecido como la membrana de aplicación de la regla.
    """

    for regla in conjunto_reglas:
        mem=regla.membrana
        if(regla.salida is not []):
            for objeto in regla.salida:
                objeto.membrana_genera=mem
        if(regla.salida_membrana_padre is not []):
            for objeto in regla.salida_membrana_padre:
                objeto.membrana_genera=mem
        if(regla.salida_membrana_hija is not []):
            for objeto in regla.salida_membrana_hija:
                objeto.membrana_genera=mem
    
    return conjunto_reglas

def paso_computacion(sistema, dict_reglas):
    """
        Método que implementa toda la lógica de aplicación de un paso de computación sobre un sistema
    
        Args:
        - sistema (SistemaMembrana): objeto de la clase SistemaMembrana sobre el que se aplica el paso de computación
        - dict_reglas (dict): diccionario con pares clave valor membrana:conjunto de reglas de la membrana

        Returns:
        sistema,dicti, reglas_aplicadas, dict_paso, sistema_antes_de_aniquilar
        - sistema: objeto de la clase SistemaMembrana tras la aplicación del paso de computación
        - dicti: diccionario de pares clave valor membrana:lista de identificadores de los objetos \delta presentes en la membrana en el momento de su disolución
        - reglas_aplicadas: lista de reglas aplicadas en el paso de computación
        - dict_paso: diccionario de pares clave valor identificador de un objeto : lista de identificadores de los objetos que permiten la aplicación de la regla (LHS) que genera a cada objeto
        - sistema_antes_de_aniquilar: objeto de la clase SistemaMembrana antes de las disoluciones del paso
    """

    profundidades=sistema.obtener_profundidades()  #en primer lugar obtenemos las profundidades de cada una de las membranas, para recorrerlas desde las mas profunda a la
                                                #a la más externa. De esta forma garantizamos que los objetos de una membrana disuelta pasen al primer antecesor no disuelto en el paso
    iterar=[]
    reglas_aplicadas=[]

    for profundidad in sorted(profundidades.keys(),reverse=True):
        iterar+=profundidades[profundidad]
    for objeto in iterar:    
        conteos=conteo(sistema, objeto)   # obtenemos el número de objetos $\delta_t \bar \delta_t$ en cada membrana
        b={}
        for a in conteos:    #recorremos los distintos timers presentes en la membrana
            if min(conteos[a])>0:
                b[a]=[min(conteos[a]),min(conteos[a])]   #tenemos que eliminar cada par de copias de ambos objetos 
                for _ in range(min(conteos[a])):
                    reglas_aplicadas = reglas_aplicadas + ['anti-aniquilación ('+ str(a) + ') [' + str(objeto) + ']']  #se añade en la lista de reglas aplicables por cada antianiquilación realizada para cada timer
        if b:  #una vez que hemos determinado cuántos objetos de cada tipo hay que eliminar, recorremos los objetos de la membrana y realizamos las eliminaciones necesarioas
            c=[]
            for obj in sistema.objetos[objeto]:
                if(obj.nombre=='delta' and obj.timer in b):
                    if(b[obj.timer][0]!=0):
                        b[obj.timer]=[b[obj.timer][0]-1, b[obj.timer][1]]
                    else:
                        c.append(obj)
                elif(obj.nombre=='anti-delta' and obj.timer in b):
                    if(b[obj.timer][1]!=0):
                        b[obj.timer]=[b[obj.timer][0], b[obj.timer][1]-1]
                    else:
                        c.append(obj)
                else:
                    c.append(obj)
            sistema.objetos[objeto]=c
           
         
    for clave in sistema.objetos:  #recorremos los objetos delta_t cuyos timers será necesario reducir. No importa el momento en el que se haga esto o si se hace sobre la estructura original, ya que no quedan más reglas con este tipo de objetos en LHS
        if clave!=0:  #la regla de reducción de timer es la única regla aplicable en este tipo de objetos en todas las membranas excepto en la etiquetada por 0, estos objetos también pueden entrar en una de las membranas hijas de manera no determinista.
            for a in sistema.objetos[clave]:
                if(a.nombre=='delta' and a.timer!=0):
                    reglas_aplicadas = reglas_aplicadas + ["reducción (" + str(a.timer) +  ") [" + str(clave) + "]"]
                    a.timer=a.timer-1

    
    #para lo que hay en 0 tengo dos opciones: o disminuir el timer o introducir objetos en el entorno.
    # si no es delta meter
    # si es delta podemos meter o disminuir timer y ahi se queda.
    #almacenaremos en estructuras secundarias para no aplicar las reglas sobre los objetos que ya han evolucionado en el paso de computación
    meter = []
    dejar = []
    for objeto in sistema.objetos[0]:
        if objeto.nombre=='delta' and objeto.timer!=0:
            if random.choice([0,1])==0: #podemos o disminuir su timer o insertarlo en una membrana
                meter = meter + [objeto]
                reglas_aplicadas = reglas_aplicadas + ['insercción (' + str(objeto) + ')'] 
            else: 
                reglas_aplicadas = reglas_aplicadas + ["reducción (" + str(objeto.timer) +  ") [0]"]
                objeto.timer = objeto.timer - 1
                dejar = dejar + [objeto]
        else:  #el resto de objetos entra obligatoriamente en alguna membrana
            meter = meter + [objeto]
            reglas_aplicadas = reglas_aplicadas + ['insercción (' + str(objeto) + ')'] 
    sistema.objetos[0] = []
    
    copia_sistema=copy.deepcopy(sistema)  #creamos una copia del sistema. Sobre una de las copias eliminamos los objetos de LHS de la regla y sobre la otra aplicamos las reglas. De
                            #Así garantizamos no aplicar reglas sobre objetos que ya han evolucionado en en paso de computación
    dict_paso={}
    lista_membranas=set(list(sistema.estructura.keys())+sum(list(sistema.estructura.values()),[]))
    for membrana in lista_membranas:   #recorremos las membranas del sistema
        if membrana in dict_reglas:  
            lista_reglas=dict_reglas[membrana]
            a=False
            while(a==False):    #aplicaremos reglas sobre la membrana de manera maximal
                long=len(lista_reglas)
                random.shuffle(lista_reglas)   #desordenamos constantemente la lista de reglas para que la selección del multiconjunto de reglas aplicables se haga de manera no determinista.
                for regla in lista_reglas:
                    long=long-1
                    if regla.es_aplicable3(copia_sistema):    #si la regla es aplicable, eliminamos los objetos de LHS y la aplicamos sobre la otra copia del sistema
                        reglas_aplicadas.append(regla)
                        dict_genera_regla=regla.aplicar(sistema)
                        dict_paso.update(dict_genera_regla)
                        for elemento in regla.entrada:
                            elemento.eliminar_objeto_lista(copia_sistema.objetos[membrana])  #eliminar los objetos de LHS para comprobar la aplicabilidad de las siguientes reglas sobre los objetos que no hayan evolucionado
                        break
                    #si he recorrido el bucle entero y no habia ninguna, es cuando pongo el false
                    if(long==0):
                        a=True
    
    sistema.objetos[0] = sistema.objetos[0] + dejar   #volvemos a meter en el entorno los objetos \delta_t cuyos timers han sido reducidos
    
    for objeto in meter:   #metemos en una de las membranas hijas seleccionada de manera no determinista los objetos a introducir
        hija_aleatoria=random.choice(sistema.estructura[0])
        sistema.objetos[hija_aleatoria]=sistema.objetos[hija_aleatoria]+[objeto]
    
    
            
    #aniquilar
    sistema_antes_de_aniquilar = copy.deepcopy(sistema)   #guardamos el sistema antes de las disoluciones del paso
    sistema, dicti = aniquilar(sistema)    #aplicamos las correspondientes disoluciones de membranas

    
    
    return sistema,dicti, reglas_aplicadas, dict_paso, sistema_antes_de_aniquilar




def tiene_objetos_delta(sistema):
    """
        Método para comprobar si un sistema tiene objetos \delta en sus multiconjuntos de objetos 
        
        Args:
        - sistema (SistemaMembrana): objeto de la clase SistemaMembrana sobre el que se quiere determinar la existencia de objetos \delta

        Returns:
        - boolean: True si tiene objetos \delta, False en caso contrario
    
    """
    for clave in sistema.objetos:
        for objeto in sistema.objetos[clave]:
            if objeto.nombre == 'delta':
                return True
    return False





                                                
def computacion(sistema,conjunto_reglas, tiempo_computacion=60, num_pasos=1):
    """
        Método para llevar a cabo la computación de un sistema de membranas 
        
        Args:
        - sistema (SistemaMembrana): objeto de la clase SistemaMembrana sobre el se quiere llevar a cabo la computación
        - conjunto_reglas (list): lista de objetos de la clase Regla que contienen las reglas de todas las membranas del sistema
        - tiempo_computacion (int): tiempo en segundos máximo de computación
        - num_pasos (int): número máximo de pasos de comptuación

        Returns:
        - sistema: objeto de la clase SistemaMembrana tras la computación realizada
        - dict_computacion: diccionario de pares clave valor identificador del objeto: lista de objetos que han generado dicho objeto (LHS) por la aplicación de una regla
        - dict_aniquilacion: diccionario de pares clave valor membrana:lista de identificadores de los objetos \delta presentes en la membrana en el momento de su disolución
        - diccionario_a_devolver: diccionario con pares clave valor que contienen las reglas_aplicadas y el sistema antes y después de las disoluciones por paso
        - mensaje_fin: string con el motivo del fin de la computación
        - aniquiladas_por_paso : diccionario con la lista de etiquetas de membranas disueltas por cada paso de computación realizado
    
    """

    conjunto_reglas=redefinir_reglas(conjunto_reglas)   #redefinimos las reglas para que los objetos de RHS tengan la propiedad membrana_genera correcta
    dict_computacion={}
    dict_aniquilacion={}
    aniquiladas_por_paso = {}
    dict_reglas={}
    diccionario_a_devolver = {}
    contador_paso=1
    for regla in conjunto_reglas:     #para la mejora de la eficiencia, en lugar de trabajar sobre una lista de reglas de todo el sistema, generamos un diccionario con la lista de reglas por membrana
        if regla.membrana in dict_reglas:
            dict_reglas[regla.membrana]=dict_reglas[regla.membrana]+[regla]
        else:
            dict_reglas[regla.membrana]=[regla]
    tiempo_inicio = time.time()

    
    while(sistema.reglas_aplicables(conjunto_reglas) or tiene_objetos_delta(sistema) or sistema.objetos[0]!=[]):   #repetir constantemente mientras el sistema lo permita
        if(time.time()>tiempo_inicio+tiempo_computacion):  #al principio del paso se comprueba si se ha superado el tiempo de computación, en este caso paramos
            mensaje_fin = "FIN DEL TIEMPO DE COMPUTACIÓN"
            print(mensaje_fin)
            return sistema, dict_computacion, dict_aniquilacion, diccionario_a_devolver, mensaje_fin, aniquiladas_por_paso
            sys.exit()
        if(num_pasos < contador_paso ):   #comprobamos si hemos alcanzado el número máximo de pasos de computación permitido
            mensaje_fin = "NUMERO DE PASOS ALCANZADO"
            print(mensaje_fin)
            return sistema, dict_computacion, dict_aniquilacion, diccionario_a_devolver, mensaje_fin, aniquiladas_por_paso
            sys.exit()
        sistema, dict_aniquilacion_paso, reglas_aplicadas_paso, dict_paso, sistema_antes_de_aniquilar_paso =paso_computacion(sistema,dict_reglas)   #aplicamos un paso de computación 
            

    
        
        
        #almacenamos la información obtenida del paso de computación

        lista_aniquiladas_por_paso = list(dict_aniquilacion_paso.keys())
        sistema_tras_aniquilar = copy.deepcopy(sistema)
        dict_computacion.update(dict_paso)
        dict_aniquilacion.update(dict_aniquilacion_paso)
        aniquiladas_por_paso[contador_paso] = lista_aniquiladas_por_paso

        diccionario_a_devolver[contador_paso] = [reglas_aplicadas_paso, sistema_antes_de_aniquilar_paso,sistema_tras_aniquilar] 
        contador_paso=contador_paso+1
        
        if(sistema.estructura=={} or sistema.estructura=={0:[]}):  #si la estructura resultante es vacía, detenemos la computación
            mensaje_fin = "FIN DE LA EJECUCIÓN, ESTRUCTURA VACÍA"
            print(mensaje_fin)
            return sistema, dict_computacion, dict_aniquilacion, diccionario_a_devolver, mensaje_fin, aniquiladas_por_paso
            sys.exit()
        if(len(sistema.estructura[0])==1):  #si solo queda una valquiria en la competición, esta se detiene y se declara ganadora
            mensaje_fin = "SOLO QUEDA UNA VALQUIRIA GANADORA"
            print(mensaje_fin)
            return sistema, dict_computacion, dict_aniquilacion, diccionario_a_devolver, mensaje_fin, aniquiladas_por_paso
            sys.exit()
       

    #una vez que el sistema no permite la aplicación de más reglas para su evolución, la computación se para   
    if contador_paso > 2:
        mensaje_fin = "FIN DE LA EJECUCIÓN, NO HAY MÁS REGLAS APLICABLES"  
        print(mensaje_fin)
        return sistema,dict_computacion, dict_aniquilacion, diccionario_a_devolver, mensaje_fin, aniquiladas_por_paso
    else:
        mensaje_fin = "NO SE PRODUCE NINGUNA EVOLUCIÓN DEL SISTEMA"
        return sistema,dict_computacion, dict_aniquilacion, diccionario_a_devolver, mensaje_fin, aniquiladas_por_paso



def agrupar_valquirias(lista_valquirias, lista_reglas):
    """
        Método para agrupar todas las valquirias en una membrana común etiquetada por 0
        
        Args:
        - lista_valquirias (list(SistemaMembrana)): lista de objetos de la clase SistemaMembrana que se introducen en la competición.
        - lista_reglas (list(list(Reglas))): lista de las reglas de cada valquiria. Las reglas de cada valquiria están agrupadas en listas diferentes.


        Returns:
        - objeto de la clase SistemaMembrana con todas las valquirias agrupadas
        - reglas_común: lista de las reglas del sistema agrupado
        - membranas_por_valquiria: diccionario con pares clave valor valquiria: lista de membranas de la valquiria
        - relacion_membranas: diccionario con la relación entre las etiquetas de cada valquiria y las etiquetas del sistema agrupado

    
    """

    relacion_membranas = {}
    membranas_por_valquiria={}
    sumar=max(set(list(lista_valquirias[0].estructura.keys())+sum(list(lista_valquirias[0].estructura.values()),[])))  

    membranas_por_valquiria[1]=[x for x in range(1,sumar+1)] #redefinimos las etiquetas de cada valquiria para que no presenten la misma etiqueta que otra valquiria.
    estructura_comun=copy.deepcopy(lista_valquirias[0].estructura)
    objetos_comun=copy.deepcopy(lista_valquirias[0].objetos)
    ss = set(list(lista_valquirias[0].estructura.keys())+sum(list(lista_valquirias[0].estructura.values()),[]))
    ss.remove(0)  
    for s in ss:
        relacion_membranas[s] = (1, s)   #almacenamos la relación entre las nuevas etiquetas y las etiquetas de cada valquiria
    reglas_comun = lista_reglas[0]
    for i in range(1,len(lista_valquirias)): #recorremos la lista de valquirias
        sumar_act = sumar
        for est in lista_valquirias[i].estructura.keys():
            if est==0:
                estructura_comun[0]=estructura_comun[0] + [x+sumar for x in lista_valquirias[i].estructura[0]]
            else:
                estructura_comun[est+sumar]=[x+sumar for x in lista_valquirias[i].estructura[est]]  #vamos agrupando la estructura de las valquirias en una valquiria común, reetiquetando sus membranas
        for obj in lista_valquirias[i].objetos.keys():   #introducimos los multiconjuntos de objetos de cada valquiria en el sistema agrupado
            if(obj!=0):
                objetos_comun[obj+sumar]=lista_valquirias[i].objetos[obj]
                relacion_membranas[obj+sumar] = (i+1, obj)
        for regla in lista_reglas[i]:   #recorremos la lista de reglas para redefinir las etiquetas de aplicación de la regla con la nueva etiqueta de la membrana donde se aplica la regla.
            copia = copy.deepcopy(regla)

            copia.membrana = copia.membrana + sumar

            reglas_comun.append(copia)
        sumar=max(set(list(lista_valquirias[i].estructura.keys())+sum(list(lista_valquirias[i].estructura.values()),[])))
        membranas_por_valquiria[i+1]=[x for x in range(sumar_act+1,sumar_act+sumar+1)]
        sumar=sumar+sumar_act
        
    
    return SistemaMembrana.SistemaMembrana(estructura_comun,objetos_comun), reglas_comun, membranas_por_valquiria, relacion_membranas

def aniquilar(sistema):
    """
        Método para llevar a cabo las correspondientes disoluciones de membrana de un paso de computación
        
        Args:
        - sisteema (SistemaMembrana):  objeto de la clase SistemaMembrana.

        Returns:
        - objeto de la clase SistemaMembrana tras las correspondientes disoluciones de membrana llevadas a cabo
        - dict: dicionario con pares clave valor membrana disuelta: objetos \delta que han llevado a cabo al disolución de la membrana
    
    """
    sistema=sistema
    estructura=copy.deepcopy(sistema.estructura)
    profundidades=sistema.obtener_profundidades()
    iterar=[]
    dict={}
    for profundidad in sorted(profundidades.keys(),reverse=True):    #obtenemos la profundidad de cada membrana, de esta forma garantizamos que los objetos de la membrana disuelta y la estructura de su interior
                                                    # pasen al primer antecesor no disuelto en el paso de computación.
        iterar+=profundidades[profundidad]
    iterar.remove(0)
    objetos=copy.deepcopy(sistema.objetos) 
    for objeto in iterar:
        if any([a.nombre=='delta' and a.timer==0 for a in sistema.objetos[objeto]]):   #si la membrana tiene algún objeto \delta con timer=0
            dict[objeto]=[x for x in objetos[objeto] if x.timer==0]   #almacenamos los identificadores de los objetos \delta que hay en la membrana a disolver
            padre=sistema.obtener_padre(objeto)   #obtenemos la membrana padre de la memrbaana a disolver
            if(objeto in estructura):  #si la membrana tiene membranas hijas, estas pasan también al primer antecesor no disuelto
                estructura[padre]=estructura[padre] + estructura[objeto]
                del estructura[objeto]   #eliminamos la membrana de la estructura
            estructura[padre].remove(objeto)
            if(estructura[padre]==[]):    #si la estructura del padre queda vacía, no aparecerá como clave en la definición de estructura del sistema por la notación utilizada
                del estructura[padre]
            sin_aniquilador=[x for x in objetos[objeto] if  x.timer!=0] #eliminamos todos los objetos \delta de la membrana aniquilada
            objetos[padre]=objetos[padre]+sin_aniquilador #el resto de objetos pasan al primer antecesor no disuelto
            del objetos[objeto]

            
      
    return SistemaMembrana.SistemaMembrana(estructura,objetos), dict      






        
def queens_of_the_hill(lista_valquirias, lista_reglas, tiempo_computacion, num_pasos):
    """
        Método para realizar una única competición entre valquirias
        
        Args:
        - lista_valquirias (list(SistemaMembrana)): lista de objetos de la clase SistemaMembrana para la competición
        - lista_reglas (list(list(Reglas))): lista de la lista de objetos de la clase Regla de cada contrincante
        - tiempo_computacion (int): tiempo máximo de computación del torneo
        - num_pasos (int): número máximo de pasos de computación del torneo




        Returns:
        - sistema: objeto de la clase SistemaMembrana tras la computación realizada
        - dict_computacion: diccionario de pares clave valor identificador del objeto: lista de objetos que han generado dicho objeto (LHS) por la aplicación de una regla
        - dict_aniquilacion: diccionario de pares clave valor membrana:lista de identificadores de los objetos \delta presentes en la membrana en el momento de su disolución
        - mpv: diciconario de pares clave valor valquiria:etiquetas de las membranas de la valquiria
        - vpm: diccionario de pares etiqueta de membrana:valquiria a la que pertenece, para mayor eficiencia
        - relacion_membranas: diccionario con la relación entre las etiquetas de cada valquiria y las etiquetas del sistema agrupado
        - diccionario_a_devolver: diccionario con pares clave valor que contienen las reglas_aplicadas y el sistema antes y después de las disoluciones por paso
        - mensaje_fin: string con el motivo del fin de la computación
        - aniquiladas_por_paso : diccionario con la lista de etiquetas de membranas disueltas por cada paso de computación realizado   
        - lista de las diccionarios con las métricas obtenidas por cada una de las valquirias en la competición 
    """



    sistema,reglas,mpv, relacion_membranas =agrupar_valquirias(lista_valquirias, lista_reglas)   #comenzamos la competición agrupando todas las valquirias en un único sistema
    vpm={}
    for valquiria in mpv:   #guardamos la valquiria a la que pertenece cada membrana
        for membrana in mpv[valquiria]:
            vpm[membrana]=valquiria
    n_total_membranas = len(list(vpm.keys()))
    sistema,dict_computacion,dict_aniquilacion, diccionario_a_devolver, mensaje_fin, aniquiladas_por_paso = computacion(sistema,reglas, tiempo_computacion, num_pasos)  #aplicamos la computación del sistema agrupado

    
    m=len(diccionario_a_devolver)
    scores_basico = {}
    scores_articulo = {}
    scores_atacantes_basico2 = {}
    scores_atacante_articulo = {}
    scores_autoataque = {}
    scores_influencia = {}


    if m>0:
    
        #METRICA DEFENSA BÁSICA
        membranas_aniquiladas=list(dict_aniquilacion.keys())   #membranas aniquiladas en la computación
        for valquiria in list(mpv.keys()):
            membranas_aniquiladas_valquiria = sum([1 for x in mpv[valquiria] if x in  membranas_aniquiladas])  #buscamos cuáles de las membranas aniquiladas en la computación pertenecen a la calquiria
            scores_basico[valquiria] = (len(mpv[valquiria]) - membranas_aniquiladas_valquiria) / len(mpv[valquiria])  




        #MÉTRICA DEFENSA MÁS COMPLEJA
        for valquiria in list(mpv.keys()):
            pi_j = len(mpv[valquiria])
            total_sumatorio = 0
            for paso in diccionario_a_devolver.keys():   #recorremos los pasos para ponderar más aquellas membranas que han sobrevivido más tiempo en la competición
                estructura = list(diccionario_a_devolver[paso][2].estructura.values())
                membranas = set(sum(list(estructura),[]))
                membranas_restantes = len(set(mpv[valquiria])- membranas)
                total_sumatorio = total_sumatorio + membranas_restantes
            scores_articulo[valquiria] = 1 - (total_sumatorio/(m*pi_j))







        #MÉTRICA atacante basica
        matriz = [[0 for _ in range(len(lista_valquirias))] for _ in range(len(lista_valquirias))]   #generamos una matriz de tamaño nxn, donde n es el número de valquirias
        for a in dict_aniquilacion:   #recorremos las membranas aniquiladas
            for e in set(dict_aniquilacion[a]):   #recorremos los objetos \delta que había en una membrana en el momento de su disolución
                valquiria_genera=vpm[e.membrana_genera]    #buscamos qué valquiria ha sido culpable de esa aniquilación
                matriz[vpm[a]-1][valquiria_genera-1]=matriz[vpm[a]-1][valquiria_genera-1]+1   #almacenamos la inforamación en una matriz donde la columna i representa
                                                                                        # las membranas disueltas de las diferentes valquirias por la valquiria i


        for a in range(len(matriz)):
            print("la valquiria " + str(a+1) + "ha aniquilado " + str(sum([m[a] for m in matriz])) + " y "+ str(matriz[a][a]) +" son suyas y tenia " + str(len(mpv[a+1])))
            try:
                membranas_valquiria = len(mpv[a+1])
                scores_atacantes_basico2[a+1] = (sum([m[a] for m in matriz]) - matriz[a][a]) / (n_total_membranas - membranas_valquiria)
            except:
                scores_atacantes_basico2[a+1] = 0
            scores_autoataque[a+1] =  1 - (matriz[a][a] / len(mpv[a+1]))


        





        #metrica ATACANTE MÁS COMPLEJA

        for valquiria in list(mpv.keys()):
            n_membranas_resto = n_total_membranas - len(mpv[valquiria])
            total_sumatorio = 0
            for paso in diccionario_a_devolver.keys():   #recorremos los distintos pasos de la computación
                sumatorio_paso = 0   
                aniquiladas = aniquiladas_por_paso[paso]   #obtenemos las membranas aniquiladas en el paso
                for membrana_aniquilada in aniquiladas: #recorremos las membranas aniquiladas en el paso
                    if membrana_aniquilada not in mpv[valquiria] and any(y in [x.membrana_genera for x in dict_aniquilacion[membrana_aniquilada]] for y in mpv[valquiria]):    #si la membrana aniquilada no pertenece a la valquiria y ha sido aniquilada por algún objeto \delta generado por dicha valquiria
                        sumatorio_paso = sumatorio_paso + 1
                total_sumatorio = total_sumatorio + ((m + 1) - paso)*sumatorio_paso
            scores_atacante_articulo[valquiria] = total_sumatorio/(m*n_membranas_resto)

            # MÉTRICA INFLUENCIAS
            
            aniquiladas_otras = [x for x in membranas_aniquiladas if x not in mpv[valquiria]]
            total_sumatorio = 0
            for membrana_aniquilada in aniquiladas_otras:
                sumatorio_aniquilada = 0
                deltas_aniquilan = dict_aniquilacion[membrana_aniquilada]
                for delta in deltas_aniquilan:
                    generan_delta = dict_computacion[delta.id]
                    sumatorio_aniquilada = sumatorio_aniquilada + len([x for x in generan_delta if Objeto.Objeto.objetos_por_id[x].membrana_genera in mpv[valquiria]])/len(generan_delta)
                total_sumatorio = total_sumatorio + sumatorio_aniquilada/len(deltas_aniquilan)
            try:
                scores_influencia[valquiria] = total_sumatorio / len(aniquiladas_otras)
            except:
                scores_influencia[valquiria] = 0




        

    else:
        for valquiria in list(mpv.keys()):
            scores_basico[valquiria] = 0
            scores_articulo[valquiria] = 0
            scores_atacantes_basico2[valquiria] = 0
            scores_atacante_articulo[valquiria] = 0
            scores_autoataque[valquiria] = 0
            scores_influencia[valquiria] = 0




    return sistema, dict_computacion, dict_aniquilacion, vpm, mpv, relacion_membranas, diccionario_a_devolver, mensaje_fin, aniquiladas_por_paso, [scores_basico, scores_articulo, scores_atacantes_basico2, scores_atacante_articulo, scores_autoataque, scores_influencia]
    
        
        
        
    
def m_queens_of_the_hill(lista_valquirias, lista_reglas, tiempo_computacion, pasos, m):

    """
        Método para realizar las m competiciones entre valquirias y mitigar el efecto en las métricas del no determinismo en una única competición
        
        Args:
        - lista_valquirias (list(SistemaMembrana)): lista de objetos de la clase SistemaMembrana para la competición
        - lista_reglas (list(list(Reglas))): lista de la lista de objetos de la clase Regla de cada contrincante
        - tiempo_computacion (int): tiempo máximo de computación de cada torneo
        - pasos (int): número máximo de pasos de computación de cada torneo
        - m (int): número de torneos a realizar

    return sistemas_agrupados, dict_computacion_agrupados, dict_aniquilacion_agrupados, vpm_agrupados, mpv_agrupados, diccionario_a_devolver_agrupados, mensaje_fin_agrupados, aniquiladas_por_paso_agrupados, lista_scores_agrupados,  lista_total


        Returns:
        - sistemas_agrupados: lista de objetos de la clase SistemaMembrana tras las diferentes computaciones realizadas
        - dict_computacion_agrupados: lista de los diccionarios de pares clave valor identificador del objeto: lista de objetos que han generado dicho objeto (LHS) por la aplicación de una regla en cada competición
        - dict_aniquilacion_agrupados: lista de los diccionarios de pares clave valor membrana:lista de identificadores de los objetos \delta presentes en la membrana en el momento de su disolución en cada competición
        - mpv_agrupados: diciconario de pares clave valor valquiria:etiquetas de las membranas de la valquiria 
        - vpm_agrupados: diccionario de pares etiqueta de membrana:valquiria a la que pertenece, para mayor eficiencia
        - diccionario_a_devolver_agrupados: lista de diccionarios con pares clave valor que contienen las reglas_aplicadas y el sistema antes y después de las disoluciones por paso en cada competición
        - mensaje_fin_agrupados: lista de string con el motivo del fin de la computación en cada competición   
        - aniquiladas_por_paso_agrupados : lista de diccionarios con la lista de etiquetas de membranas disueltas por cada paso de computación realizado en cada competición 
        - lista_scores_agrupados: lista de las listas de las métricas obtenidas por cada una de las valquirias en cada una de las competiciones
        - lista_total: lista con las medias de las métricas obtenidas por cada valquiria en todas las competiciones
    """
    sistemas_agrupados = []
    dict_computacion_agrupados = []
    dict_aniquilacion_agrupados = []
    vpm_agrupados = []
    mpv_agrupados = []
    relacion_membranas_agrupados = []
    diccionario_a_devolver_agrupados = []
    mensaje_fin_agrupados = []
    aniquiladas_por_paso_agrupados = []
    lista_scores_agrupados = []
    
    for i in range(0, m):   #realizamos las m competiciones
        copia_lista_valquirias = copy.deepcopy(lista_valquirias)
        copia_lista_reglas = copy.deepcopy(lista_reglas)
        sistema,dict_computacion,dict_aniquilacion,vpm, mpv, relacion_membranas, diccionario_a_devolver,mensaje_fin,aniquiladas_por_paso,lista_scores = queens_of_the_hill(copia_lista_valquirias, copia_lista_reglas, tiempo_computacion, pasos)
        sistemas_agrupados = sistemas_agrupados + [sistema]
        dict_computacion_agrupados = dict_computacion_agrupados + [dict_computacion]
        dict_aniquilacion_agrupados = dict_aniquilacion_agrupados + [dict_aniquilacion]
        vpm_agrupados = vpm_agrupados + [vpm]
        mpv_agrupados = mpv_agrupados + [mpv]
        relacion_membranas_agrupados = relacion_membranas_agrupados + [relacion_membranas]
        diccionario_a_devolver_agrupados = diccionario_a_devolver_agrupados + [diccionario_a_devolver]
        mensaje_fin_agrupados = mensaje_fin_agrupados + [mensaje_fin]
        aniquiladas_por_paso_agrupados = aniquiladas_por_paso_agrupados + [aniquiladas_por_paso]
        lista_scores_agrupados = lista_scores_agrupados + [lista_scores]

    

    #calculamos la media de cada una de las métricas en las distintas valquirias en todas las competiciones
    lista_total = copy.deepcopy(lista_scores_agrupados[0])
    for i in range(1, len(lista_scores_agrupados)):
        lista = copy.deepcopy(lista_scores_agrupados[i])
        for diccionario in range(len(lista)):
            for clave in list(lista[diccionario].keys()):
                lista_total[diccionario][clave] = lista_total[diccionario][clave] + lista[diccionario][clave]


    

    for diccionario in lista_total:
        for clave in list(diccionario.keys()):
            diccionario[clave] = diccionario[clave] / m
    return sistemas_agrupados, dict_computacion_agrupados, dict_aniquilacion_agrupados, vpm_agrupados, mpv_agrupados, diccionario_a_devolver_agrupados, mensaje_fin_agrupados, aniquiladas_por_paso_agrupados, lista_scores_agrupados,  lista_total
    





def split_and_sort_numbers(string): #MÉTODO UTILIZADO PARA OBTENER LAS ETIQUETAS DE UNA ESTRUCTURA DE MEMRBANAS
    # Crear una lista para almacenar los números encontrados
    numeros = []
    # Recorrer cada carácter del string
    for char in string:
        # Comprobar si el carácter es un número
        if char.isdigit():
            # Convertir el carácter en un número entero y añadirlo a la lista
            numeros.append(int(char))
    # Ordenar la lista de números
    numeros.sort()
    # Devolver la lista ordenada
    return numeros



def transformar_objetos(lista):  #MÉTODO UTILIZADO PARA OBTENER UNA LSITA DE OBJETOS DE LA CLASE OBJETO A PARTIR DE UNA LISTA DE NOMBRES CON LA NOTACIÓN ESPECÍFICA
    if lista != ['']:
        lista_objetos=[]
        for objeto in lista:
            objeto = objeto.strip()
            if objeto == '':
                raise ValueError("No está permitido generar un objeto sin nombre")

            if es_forma_bar_delta_k(objeto)[0]==True:
                lista_objetos = lista_objetos + [Objeto.Objeto('anti-delta', timer=es_forma_bar_delta_k(objeto)[1])]
            elif es_forma_delta_k(objeto)[0]==True:
                lista_objetos = lista_objetos + [Objeto.Objeto('delta', timer=es_forma_delta_k(objeto)[1])]
            else:
                lista_objetos=lista_objetos + [Objeto.Objeto(objeto)]
    else: 
        lista_objetos = []
    return lista_objetos

import re

def es_forma_bar_delta_k(string):   #MÉTODO PARA COMPROBAR SI EL OBJETO ES DEL TIPO $\bar \delta_t$
    # Expresión regular para comprobar la forma "anti-delta{k}"
    patron = r'^anti-delta\{(\d+)\}$'
    # Comprobar si el string coincide con el patrón
    coincidencia = re.match(patron, string)
    if coincidencia:
        # Si coincide, extraer el número k
        k = int(coincidencia.group(1))
        return True, k
    else:
        # Si no coincide, devolver False
        return False, None

def es_forma_delta_k(string):     #MÉTODO PARA COMPROBAR SI EL OBJETO ES DEL TIPO $\delta_t$
    # Expresión regular para comprobar la forma "delta{k}"
    patron = r'^delta\{(\d+)\}$'
    # Comprobar si el string coincide con el patrón
    coincidencia = re.match(patron, string)
    if coincidencia:
        # Si coincide, extraer el número k
        k = int(coincidencia.group(1))
        return True, k
    else:
        # Si no coincide, devolver False
        return False, None
    
def split_string(string):   #MÉTODO PARA OBTENER UN OBJETO DE LA CLASE REGLA A PARTIR UN STRING CON LA NOTACIÓN ESPECÍFICA PARA LA DEFINICIÓN DE LAS REGLAS.
    # Expresión regular para extraer las partes del string
    patron = r'\[(.*?)\s*-->\s*(.*?)\]\'(\d+)'
    
    # Buscar coincidencias en el string
    coincidencia = re.match(patron, string)
    
    if coincidencia:
        # Extraer las partes del string y limpiar los espacios en blanco
        entrada = coincidencia.group(1).strip()
        salida = coincidencia.group(2).strip()
        membrana = int(coincidencia.group(3))
        
        # Dividir las cadenas de entrada y salida en objetos individuales
        entrada = [objeto.strip() for objeto in entrada.split(",")]
        salida = [match.strip() for match in re.findall(r'\([^)]*\)|[^,]+', salida)]
        #salida = [objeto.strip() for objeto in salida.split(",")]
        
        entrada=transformar_objetos(entrada)
        salida_regla=[]
        salida_membrana_padre=[]
        salida_membrana_hija=[]
        for objeto in salida:  #BUSCAMOS LOS OBJETOS DE RHS ENVIADOS A LA MISMA MEMBRANA
            if sigue_patron_in(objeto):
                nombre = obtener_nombre_objeto_in(objeto)
                if es_forma_bar_delta_k(nombre)[0]==True:
                    salida_membrana_hija = salida_membrana_hija + [Objeto.Objeto('anti-delta', timer=es_forma_bar_delta_k(nombre)[1])]
                elif es_forma_delta_k(nombre)[0]==True:
                    salida_membrana_hija = salida_membrana_hija + [Objeto.Objeto('delta', timer=es_forma_delta_k(nombre)[1])]
                else:
                    salida_membrana_hija=salida_membrana_hija + [Objeto.Objeto(nombre)]
                
                
            elif sigue_patron_out(objeto):    #BUSCAMOS LOS OBJETOS DE RHS ENVIADOS A LA MEMBRANA PADRE
                nombre=obtener_nombre_objeto_out(objeto)
                if es_forma_bar_delta_k(nombre)[0]==True:
                    salida_membrana_padre = salida_membrana_padre + [Objeto.Objeto('anti-delta', timer=es_forma_bar_delta_k(nombre)[1])]
                elif es_forma_delta_k(nombre)[0]==True:
                    salida_membrana_padre = salida_membrana_padre + [Objeto.Objeto('delta', timer=es_forma_delta_k(nombre)[1])]
                else:
                    salida_membrana_padre=salida_membrana_padre + [Objeto.Objeto(nombre)]
                
            else:    #BUSCAMOS LOS OBETJOS DE RHS ENVIADOS A LA MEMBRANA HIJA
                if es_forma_bar_delta_k(objeto)[0]==True:
                    salida_regla = salida_regla + [Objeto.Objeto('anti-delta', timer=es_forma_bar_delta_k(objeto)[1])]
                elif es_forma_delta_k(objeto)[0]==True:
                    salida_regla = salida_regla + [Objeto.Objeto('delta', timer=es_forma_delta_k(objeto)[1])]
                else:
                    salida_regla=salida_regla + [Objeto.Objeto(objeto)]
                
                
        
        # Devolver las partes en un diccionario
        return Regla.Regla(entrada = entrada, salida = salida_regla, membrana=membrana, salida_membrana_padre=salida_membrana_padre, salida_membrana_hija=salida_membrana_hija)
    else:
        # Si no hay coincidencia, devolver None
        raise Exception(f"{string} No es una regla definida correctamente")






def regla_a_string(regla):    #MÉTODO PARA REPRESENTAR UN OBJETO DE LA CLASE REGLA COMO UN STRING CON LA NOTACIÓN ESPECÍFICA
    string="["
    for objeto in regla.entrada:
        string = string + str(objeto.nombre) + ","
    string= string[:-1]
    string = string + " --> "
    for objeto in regla.salida:
        if objeto.timer == None or objeto.timer == 0:
            string = string + str(objeto.nombre) + ","
        else:
            string = string + str(objeto.nombre) + "{" + str(objeto.timer) + "}," 
    if regla.salida_membrana_padre is not []:
        for objeto in regla.salida_membrana_padre:
            if objeto.timer == None or objeto.timer == 0:
                string = string + "(" + objeto.nombre + ",out)" + ","
            else:
                string = string + "(" + objeto.nombre + "{" + str(objeto.timer) + "}"+  ",out)" + ","
    if regla.salida_membrana_hija is not []:
        for objeto in regla.salida_membrana_hija:
            if objeto.timer == None or objeto.timer == 0:
                string = string + "(" + objeto.nombre + ",in)" + ","
            else:
                string = string + "(" + objeto.nombre +"{" +str(objeto.timer) +"}" + ",in)" + ","
    string = string[:-1]
    string = string + "]'"
    string = string + str(regla.membrana)
    return string
    
        

def estructura_a_string(diccionario):  #MÉTODO PARA REPRESENTAR UNA ESTRUCTURA COMO UN STRING CON LA NOTACIÓN ESPECÍFICA

    string = estructura_a_string_aux(diccionario)

    return string


def estructura_a_string_aux(diccionario, clave = 0):
    if clave not in diccionario or not diccionario[clave]:
        return f"[]'{clave}"
    
    hijos = diccionario[clave]
    cadena_hijos = ''.join(f"{estructura_a_string_aux(diccionario, hijo)}" for hijo in hijos)
    cadena_hijos = "[" + cadena_hijos + "]"
    
    return f"{cadena_hijos}'{clave}"


        

def sigue_patron_out(cadena):   #MÉTODO PARA COMPROBAR SI EL OBJETO EN RHS ES ENVIADO A LA MEMBRANA PADRE
    # Expresión regular para el patrón (algo, out)
    patron = r'\(.*?,\s*out\)'
    
    # Buscar coincidencias en la cadena
    coincidencia = re.match(patron, cadena)
    
    if coincidencia:
        return True
    else:
        return False

def sigue_patron_in(cadena):    #MÉTODO PARA COMPROBAR SI EL OBJETO EN RHS ES ENVIADO A LA MEMBRANA HIJA
    # Expresión regular para el patrón (algo, in)
    patron = r'\(.*?,\s*in\)'
    
    # Buscar coincidencias en la cadena
    coincidencia = re.match(patron, cadena)
    
    if coincidencia:
        return True
    else:
        return False



def obtener_nombre_objeto_out(cadena):     #MÉTODO PARA OBTENER EL NOMBRE A PARTIR DE LA NOTACIÓN UTILIZADA PARA ENVIAR EL OBJETO A LA MEMBRANA PADRE 
    # Expresión regular para el patrón (algo, out)
    patron = r'\((.*?),\s*out\)'
    
    # Buscar coincidencias en la cadena
    coincidencia = re.match(patron, cadena)
    
    if coincidencia:
        # Extraer el nombre del objeto
        nombre_objeto = coincidencia.group(1)
        return nombre_objeto
    else:
        return None
        

def obtener_nombre_objeto_in(cadena):  #MÉTODO PARA OBTENER EL NOMBRE A PARTIR DE LA NOTACIÓN UTILIZADA PARA ENVIAR EL OBJETO A UNA MEMBRANA HIJA
    # Expresión regular para el patrón (algo, in)
    patron = r'\((.*?),\s*in\)'
    
    # Buscar coincidencias en la cadena
    coincidencia = re.match(patron, cadena)
    
    if coincidencia:
        # Extraer el nombre del objeto
        nombre_objeto = coincidencia.group(1)
        return nombre_objeto
    else:
        return None



def objetos_a_string(lista):   #MÉTODO UTILIZADO PARA REPRESENTAR UN MULTICONJUNTO DE OBJETOS COMO UN STRING
    string = ""
    for objeto in lista:
        if objeto.nombre=="delta":
            string = string + "delta{" + str(objeto.timer) + "}"
        elif objeto.nombre=="anti-delta":
            string = string + "anti-delta{" + str(objeto.timer) + "}"
        else:
            string = string + str(objeto.nombre)
        string = string + ", "
    string = string[:-2]
    string = string + ""
    return string


def exportar_txt(listasistemas,listareglas,nombrearchivo):   #MÉTODO UTILIZADO PARA EXPORTAR UNA SERIE DE VALQUIRIAS CON LA NOTACIÓN ESPECÍFICA EN UN ARCHIVO .TXT

    # Escribir los datos en un archivo de texto plano
    with open(nombrearchivo, "w", encoding='utf-8') as f:
        for indice in range(len(listasistemas)):
            f.write("Valquiria\n\ // Estructura\n")
            f.write("@mu = ")
            f.write(estructura_a_string(listasistemas[indice].estructura)[1:-3])
            f.write("\n")
            f.write("\\\ Objetos\n")
            for membrana_objetos in listasistemas[indice].objetos:
                if listasistemas[indice].objetos[membrana_objetos] != []:
                    f.write("@ms(" + str(membrana_objetos) + ") = " + objetos_a_string(listasistemas[indice].objetos[membrana_objetos]) + "\n")
            f.write("\\\ Reglas\n")
            for regla in listareglas[indice]:
                f.write(regla_a_string(regla))
                f.write("\n")
            f.write("\n")  # Separador entre personas

    print("Archivo de texto plano creado exitosamente.")






def leer_archivo_y_guardar_informacion(nombre_archivo):   #MÉTODO UTILIZADO PARA IMPORTAR UNA SERIE DE VALQUIRIAS CON LA NOTACIÓN ESPECÍFICA A PARTIR DE UN ARCHIVO .TXT
    with open(nombre_archivo, 'r') as archivo:
        contenido = archivo.read()

    # Dividir el contenido por cada "Valquiria"
    bloques = contenido.split('Valquiria')

    listasistemas = []
    listareglas = []

    for bloque in bloques:
        # Saltar bloques vacíos que puedan resultar de la división
        if not bloque.strip():
            continue

        # Dividir el bloque en líneas
        lineas = bloque.split('\n')
        objetos_sistema = {}
        reglas_sistema = []

        for linea in lineas:
            linea = linea.strip()  # Eliminar espacios en blanco alrededor

            # Omitir comentarios
            if linea.startswith('//'):
                continue

            # Guardar las líneas que empiezan por @mu en la lista sistemas
            if linea.startswith('@mu'):
                linea = linea[6:]
                estructura = obtener_estructura(linea)
                

            # Guardar las líneas que empiezan por @ms en la lista listamulticonjuntos
            elif linea.startswith('@ms'):
                linea = linea.replace(" ", "")                
                membrana = linea[4]
                linea = linea[7:]
                objetos = linea.split(",")
                objetos = transformar_objetos(objetos)
                objetos_sistema[int(membrana)] = objetos
            
            else:
                try:
                    linea = linea.replace(" ", "")
                    reglas_sistema = reglas_sistema + [split_string(linea)]
                except:
                    pass


                

            
                    
        lista_membranas=set(list(estructura.keys())+sum(list(estructura.values()),[]))
        for membrana in lista_membranas:
            if membrana not in objetos_sistema:
                objetos_sistema[membrana] = []
        
        listasistemas.append(SistemaMembrana.SistemaMembrana(estructura, objetos_sistema))
      
        listareglas = listareglas + [reglas_sistema]

    return listasistemas, listareglas



def parse_personalizado(personalizado, length):   #MÉTODO PARA OBTENER LAS VALQUIRIAS DESEADAS PARA EXPORTAR CON EL MÉTODO PERSONALIZADO
    indices = set()
    partes = personalizado.split(',')
    for parte in partes:
        if '-' in parte:
            start, end = parte.split('-')
            start = int(start) - 1
            end = length if end.lower() in ['end', 'END'] else int(end)
            indices.update(range(start, end))
        else:
            indices.add(int(parte) - 1)
    return sorted(indices)

