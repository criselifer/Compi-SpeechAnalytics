import pickle
from dfa import Nodo

@staticmethod
def guardar_tokenizador(raiz, id_peticion):
    """
    Guarda la estructura del tokenizador en un archivo. El archivo se guarda con el nombre 'tokenizador<id>.pkl', 
    donde <id> es el identificador de la petición. Si id_peticion es 0, se guarda el tokenizador del personal,
    si id_peticion es 1, se guarda el tokenizador del cliente.
    Parametros:
        raiz(Nodo): raiz del tokenizador
        id_peticion(int): 0 para el personal, 1 para el cliente
    Retorna:
        None
    """
    # Guardar la estructura en un archivo
    nombre_archivo = 'tokenizador' + str(id_peticion) + '.pkl'
    if id_peticion == 0:
        print('Guardando el TOKENIZADOR del personal...')
    else:
        print('Guardando el TOKENIZADOR del cliente...')
    with open(nombre_archivo, 'wb') as archivo:
        pickle.dump(raiz, archivo)
        print('TOKENIZADOR guardado con éxito')

@staticmethod
def cargar_tokenizador(id_peticion):
    """
    Carga la estructura del tokenizador desde un archivo. El archivo se carga con el nombre 'tokenizador<id>.pkl',
    donde <id> es el identificador de la petición. Si id_peticion es 0, se carga el tokenizador del personal,
    si id_peticion es 1, se carga el tokenizador del cliente.
    Parametros:
        id_peticion(int): 0 para el personal, 1 para el cliente
    Retorna:
        raiz(Nodo): raiz del tokenizador
    """
    # Cargar la estructura
    raiz = None
    nombre_archivo = 'tokenizador' + str(id_peticion) + '.pkl'
    if id_peticion == 0:
        print('Cargando el TOKENIZADOR del personal...')
    else:
        print('Cargando el TOKENIZADOR del cliente...')
    try:
        with open(nombre_archivo, 'rb') as archivo:
            raiz = pickle.load(archivo)
            print('TOKENIZADOR cargado con éxito')
    except (FileNotFoundError, IOError, EOFError) as e:
        print(f"No se pudo abrir el archivo: {e}")
        # Como aun no se ha creado el archivo entonces hay que crear el AFD desde cero
        raiz = Nodo()

    return raiz

def cargar_tokens(raiz, tokens, lexemas):
    """
    Carga los tokens correspondientes a los lexemas recibidos en el parametro tokens. Los tokens son obtenidos del DFA apuntado 
    por el parametro raiz.
    El parametro tokens es modificado en el proceso. Los tokens son cargados en el mencionado parametro. 
    Parametros:
        raiz(Nodo): raiz del tokenizador
        tokens(dict): diccionario de tokens
        lexemas([]): lista de lexemas
    Retorna:
        None
    """
    print('Cargando los tokens de los lexemas...')
    for lexema in lexemas:
        siguiente = raiz
        for caracter in lexema:
            siguiente = siguiente.mover(caracter)
        siguiente.estado_final = True
        tokens[lexema] = siguiente.token
    print('Tokens cargados con éxito')