import numpy as np

class Nodo:
    def __init__(self):
        self.siguiente = np.empty(37, dtype=object)
        self.token = ''
        self.estado_final = False

def crear_funcion_hash():
    
    funcion_hash = {}
    valor = 0
    
    # de a a la n
    for char in range(ord('a'), ord('n')+1):
        funcion_hash[chr(char)] = valor
        valor += 1
    
    # la ñ
    funcion_hash['ñ'] = valor
    valor += 1
    
    # de la o hasta la z
    for char in range(ord('o'), ord('z')+1):
        funcion_hash[chr(char)] = valor
        valor += 1
    
    # caracteres especiales
    acentuadas = "áéíóú"
    for char in acentuadas:
        funcion_hash[char] = valor
        valor += 1
        
    # letras con diéresis
    dieresis = "äëïöü"
    for char in dieresis:
        funcion_hash[char] = valor
        valor += 1
    return funcion_hash

def mover(nodo_actual, caracter):
    
    nodo_siguiente = None
    hash_alfabeto = crear_funcion_hash()
    
    if nodo_actual.siguiente[hash_alfabeto[caracter]]:
        nodo_siguiente = nodo_actual.siguiente[hash_alfabeto[caracter]]
        return nodo_siguiente
    else:
        nodo_siguiente = Nodo()
        nodo_actual.siguiente[hash_alfabeto[caracter]] = nodo_siguiente 
        return nodo_siguiente