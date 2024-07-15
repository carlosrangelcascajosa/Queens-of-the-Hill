import utils
class SistemaMembrana:
    def __init__(self, estructura, objetos):
        """
        Inicializa un objeto SistemaMembrana con una estructura y los multiconjuntos de objetos de sus membranas

        Args:
        - estructura (dict): Diccionario que representa la jerarquía en la estructura de la membrana
        - objetos (dict): Diccionario de pares membrana:lista de objetos en el interior de la membrana
        """
        self.estructura = estructura
        self.objetos = objetos



    
    def __str__(self):
        """
        Devuelve una representación en cadena del objeto SistemaMmebrana
        """
        return f"SistemaMembrana: Estructura={utils.estructura_a_string(self.estructura)[1:-3]}, Objetos={self.objetos}"
    
    def to_string(self):
        """
        Devuelve una representación en cadena del objeto SistemaMembrana incluyendo la etiqueta del entorno
        """
        return f"SistemaMembrana: Estructura={utils.estructura_a_string(self.estructura)}, Objetos={self.objetos}"

    def __repr__(self):
        """
        Devuelve una representación en cadena del objeto SistemaMmebrana
        """
        return f"SistemaMembrana: Estructura={utils.estructura_a_string(self.estructura)[1:-3]}, Objetos={self.objetos}"


    def __eq__(self, other):
        """
        Compara si dos objetos SistemaMembrana son iguales-

        Dos objetos son iguales si tienen la misma estructura y los mismos multiconjuntos de objetos en el interior de cada membrana
        """
        if self.estructura != other.estructura:
            return False

        # Verificar que ambos objetos tengan las mismas claves
        if self.objetos.keys() != other.objetos.keys():
            return False

        # Verificar que los objetos en las listas sean iguales por ID
        for key in self.objetos:
            self_ids = sorted(obj.id for obj in self.objetos[key])
            other_ids = sorted(obj.id for obj in other.objetos[key])
            if self_ids != other_ids:
                return False

        return True


    def lista_objetos_membrana(self,membrana):
        """
        Devuelve una lista de nombres de objetos en el interior de una membrana específica.

        Args:
        - membrana (int): Etiqueta de la membrana 

        Returns:
        - list: Lista de nombres de los objetos en el interior de la membrana
        """

        return [objeto.nombre for objeto in self.objetos[membrana]]
    
    def membrana_contiene_objeto(self,membrana,objeto):
        """
        Verifica si una membrana contiene un objeto específico

        Args:
        - membrana (int): Etiqueta de la membrana
        - objeto (Objeto): Objeto a verificar si está contenido en la membrana

        Returns:
        - bool: True si el objeto está contenido en la membrana, False en caso contrario
        """
        return objeto.nombre in self.lista_objetos_membrana(membrana)
      
        
        
    def reglas_aplicables(self,reglas):
        """
        Obtiene la lista de reglas aplicables en cada una de las membranas a partir de una lista de reglas

        Args:
        - reglas (list): Lista de objetos Regla

        Returns:
        - dict: Diccionario donde las claves son las etiquetas de las membranas y los valores son las listas de reglas aplicables en dicha membrana
        
        """

        dict={}
        recorrer=[]
        for regla in reglas:
            if regla.es_aplicable3(self):
                recorrer.append(regla)
        for e in recorrer:
            if e.membrana in dict:
                dict[e.membrana] = dict[e.membrana] + [e]
            else:
                dict[e.membrana] = [e]
        return dict
    
    def obtener_padre(self, membrana):
        """
        Obtiene la etiqueta de la membrana padre a una dada. En caso de que la membrana sea la membrana 
        más externa del sistema, se obtiene el identificador del entorno.

        Args:
        - membrana (int): Etiqueta de la membrana hija

        Returns:
        - int: etiqueta de la membrana padre 
        """
        return [x for x in list(self.estructura.keys()) if membrana in self.estructura[x]][0]
    
    
    def obtener_profundidades(self):
        """
        Obtiene un diccionario con las profundidades de cada membrana en la estructura

        Returns:
        -dict : Diccionario donde las claves son las profundidades y los valores son la lista de membranas que se encuentran
        a dicha profundidad en la estructura del sitema
        """
        profundidades={}
        profundidades[0] = [0]
        profundidades[1] = self.estructura[0]
        i=2
        while(True):
            profundidades[i]=[]
            for objeto in profundidades[i-1]:
                if objeto in self.estructura.keys():
                    profundidades[i]=profundidades[i]+self.estructura[objeto]
            if profundidades[i]==[]:
                del profundidades[i]
                break
            i=i+1
                    
            
        return profundidades






