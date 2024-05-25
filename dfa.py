import numpy as np
from hash_function import HashFunction

class Nodo:
    """
    Clase que representa un nodo de DFA (Deterministic Finite Automaton) que permita identificar palabras en un texto.
    Atributos:
        siguiente([]): arreglo de 37 elementos, que representa las transiciones del nodo.
        token(str): token al que pertenecen las letras que forman la palabra que llega al nodo en caso de ser un estado final.
        estado_final(bool): indica si el nodo es un estado final o no.
    Ejemplo:
        siguiente = [Nodo1, Nodo2, Nodo3, ..., Nodo37]
            Nodo1: transición con la letra 'a'
            Nodo2: transición con la letra 'b'
            ...
            Nodo37: transición con la letra 'ü'
        token = 'ATC_BUENA'
        estado_final = True
    """
    def __init__(self):
        self.siguiente = np.empty(37, dtype=object)
        self.token = ''
        self.estado_final = False

    def mover(self, caracter):
        """
        Metodo que permite moverse de un nodo a otro, dependiendo de la letra que se recibe como parámetro.
        Parametros:
            caracter(str): letra que se recibe para moverse al siguiente nodo.
        Returns:
            nodo_siguiente(Nodo): nodo al que se movió.
        """
        print("Moviendo al siguiente nodo con {}...".format(caracter))

        nodo_siguiente = None
        hash_alfabeto = HashFunction().get_funcion_hash()
        
        if self.siguiente[hash_alfabeto[caracter]]:
            nodo_siguiente = self.siguiente[hash_alfabeto[caracter]]
        else:
            nodo_siguiente = Nodo()
            self.siguiente[hash_alfabeto[caracter]] = nodo_siguiente 

        print("Transición realizada.")
        return nodo_siguiente