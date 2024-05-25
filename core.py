import numpy as np

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

def crear_funcion_hash():
    """
        Función que crea una función hash que asigna un valor a cada letra del alfabeto español.
        Retorna:
            funcion_hash(dict): diccionario que contiene la función hash.
        Ejemplo:
            {'a': 0, 'b': 1, ..., 'z': 13, 'ñ': 14, 'á': 15, 'é': 16, 'í': 17, 'ó': 18, 'ú': 19, 'ä': 20, 'ë': 21, 'ï': 22, 'ö': 23, 'ü': 24}
    """

    print("Creando función hash...")

    funcion_hash = {}
    valor = 0
    
    # De a a la n
    for char in range(ord('a'), ord('n')+1):
        funcion_hash[chr(char)] = valor
        valor += 1
    
    # La ñ
    funcion_hash['ñ'] = valor
    valor += 1
    
    # De la o hasta la z
    for char in range(ord('o'), ord('z')+1):
        funcion_hash[chr(char)] = valor
        valor += 1
    
    # Caracteres correspondientes a las vocales con tilde
    acentuadas = "áéíóú"
    for char in acentuadas:
        funcion_hash[char] = valor
        valor += 1
        
    # Caracteres correspondientes a las vocales con dieresis
    dieresis = "äëïöü"
    for char in dieresis:
        funcion_hash[char] = valor
        valor += 1

    print("Función hash creada.")
    return funcion_hash

def mover(nodo_actual, caracter):
    """
        Función que realiza la transición de un nodo a otro, dado un caracter.
        Parámetros:
            nodo_actual(Nodo): nodo actual.
            caracter(str): caracter que se utiliza para realizar la transición.
        Retorna:
            nodo_siguiente(Nodo): nodo siguiente al que se llega al realizar la transición.
    """
    
    print("Moviéndose de nodo...")

    nodo_siguiente = None
    hash_alfabeto = crear_funcion_hash()
    
    if nodo_actual.siguiente[hash_alfabeto[caracter]]:
        nodo_siguiente = nodo_actual.siguiente[hash_alfabeto[caracter]]
        return nodo_siguiente
    else:
        nodo_siguiente = Nodo()
        nodo_actual.siguiente[hash_alfabeto[caracter]] = nodo_siguiente 
        return nodo_siguiente

    print("Transición realizada.")