class Objeto:
    id=1 #variable de la clase para generar automáticamente un identificador a cada objeto
    objetos_por_id={} #variable de la calse para almacenar los objetos a partir de su identificador en un diccionario
    def __init__(self, nombre, membrana_genera=None, timer=0):
        """
        Inicializa un objeto Objeto con un nombre, la etiqueta de la membrana que lo ha generado (opcional) y el timer del objeto
        para los objetos $\delta_t, \bar \delta_t$

        Args:
        - nombre (str): Nombre del objeto
        - membrana_genera (str, opcional): Nombre de la membrana generadora del objeto.
        - timer (int, opcional): Temporizador del objeto, solo se establece 
        si el nombre del objeto es delta o anti-delta
        """




        self.nombre= nombre
        self.membrana_genera = membrana_genera
        self.timer= timer if (nombre=='delta' or nombre=='anti-delta') else None
        self.id = Objeto.id
        Objeto.objetos_por_id[self.id]=self
        Objeto.id+=1
        
    
    def __str__(self):
        """
        Devuelve una representación en cadena del objeto. Para los objetos 
        $\delta_t, \bar \delta_t$, se devuelve el nombre junto a su timer entre corchetes.
        El resto de objetos se representan mediante su nombre.
        """
        if self.nombre=='delta' or self.nombre=='anti-delta':
            return str(self.nombre) + "{" + str(self.timer) + "}"
        else:
            return str(self.nombre)
    
    def __repr__(self):
    
        if self.nombre=='delta' or self.nombre=='anti-delta':
            return str(self.nombre) + "{" + str(self.timer) + "}"
        else:
            return str(self.nombre)
    
            
    
    
    def objeto_en_lista(self,lista):
        """
        Verifica si un objeto está en una lista de objetos. 

        Args:
        - lista (list): Lista de objetos para verificar.

        Returns:
        - bool: True si el objeto está en la lista, False en caso contrario.
        """
        
        return (self.nombre, self.timer) in [(objeto.nombre, objeto.timer) for objeto in lista]
    
    
    def eliminar_objeto_lista(self,lista):
        """
        Elimina el objeto de la lista basándose en el nombre.

        Args:
        - lista (list): Lista de objetos donde se eliminará el objeto.
        """
        for objeto in lista:
            if objeto.nombre == self.nombre:
                lista.remove(objeto)
                break
        return objeto.id

    
    
    def eliminar_objeto_lista3(self,lista):
         
        """
        Elimina el objeto de la lista basándose en el nombre y el temporizador.

        Args:
        - lista (list): Lista de objetos donde se eliminará el objeto.

        Returns:
        - list: La lista actualizada después de la eliminación.
        """
         
        for objeto in lista:
            if objeto.nombre == self.nombre and objeto.timer==self.timer:
                lista.remove(objeto)
                break;
        return lista
    

