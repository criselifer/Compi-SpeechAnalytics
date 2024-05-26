class HashFunction:
    """
    Clase que implementa el patrón Singleton para crear una función hash que asigna un valor a cada letra del alfabeto español.
    Ejemplo:
        hash_function = HashFunction().get_funcion_hash()
    """
    _instance = None  # Variable de clase para almacenar la instancia única
    _funcion_hash = None  # Variable de clase para almacenar la función hash

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._funcion_hash is None:  # Evitar la re-creación del hash
            self._funcion_hash = self.crear_funcion_hash()

    def get_funcion_hash(self):
        return self._funcion_hash

    @staticmethod
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