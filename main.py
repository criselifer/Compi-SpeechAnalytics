from dfa import *
import tkinter as tk
from tkinter import messagebox
from tokenizador import *
import datetime
from hash_function import HashFunction
from window_gestor_token import ventana_tokens
from window_seleccion_token import mostrar_emergente

def resumen(ATC_Puntaje, EXP_Puntaje):
    """
    Función que genera un resumen de los resultados obtenidos.
    Parámetros:
        ATC_Puntaje([]): array de 3 elementos para almacenar el puntaje de cada tipo de lexema del personal
        EXP_Puntaje([]): array de 3 elementos para almacenar el puntaje de cada tipo de lexema del cliente
    Returns:
        None
    """
    print('Generando resumen...')
    # Mostrar los resultados en una ventana emergente
    messagebox.showinfo("Resumen", "Resumen de los resultados:\n\nPersonal:\nATC_BUENA: {}\nATC_NEUTRA: {}\nATC_MALA: {}\n\nCliente:\nEXP_BUENA: {}\nEXP_NEUTRA: {}\nEXP_MALA: {}".format(ATC_Puntaje[0], ATC_Puntaje[1], ATC_Puntaje[2], EXP_Puntaje[0], EXP_Puntaje[1], EXP_Puntaje[2]))
    print('Resumen generado con éxito')

def procesar(id_peticion, puntaje, lexemas_retorno):
    """
    Función que procesa el texto ingresado por el usuario y muestra los resultados en una ventana emergente.
    Parámetros:
        id_peticion(int): 0 para el personal, 1 para el cliente
        puntaje([]): array de 3 elementos para almacenar el puntaje de cada tipo de lexema
        lexemas_retorno([]): lista de lexemas
    Returns:
        None
    """
    # Cargar el tokenizador
    raiz = cargar_tokenizador(id_peticion)

    token_mala = ''
    token_neutra = ''
    token_buena = ''

    if id_peticion == 0:
        token_mala = 'ATC_MALA'
        token_neutra = 'ATC_NEUTRA'
        token_buena = 'ATC_BUENA'
    else:
        token_mala = 'EXP_MALA'
        token_neutra = 'EXP_NEUTRA'
        token_buena = 'EXP_BUENA'

    # Procesar el texto dependiendo de la petición
    if id_peticion == 0:
        print('Procesando el texto del personal...')
        entrada = texto_area_personal.get("1.0", "end-1c")
    else:
        print('Procesando el texto del cliente...')
        entrada = texto_area_cliente.get("1.0", "end-1c")
    
    # Si no hay texto, no hacer nada
    if not entrada:
        print('No hay texto para procesar')
        return
    else:
        print('Texto a procesar: ' + entrada)

        # Generar la función hash
        hash_alfabeto = HashFunction().get_funcion_hash()

        siguiente = raiz
        lexema = ''
        lexemas = []

        # Preprocesamiento de la entrada
        entrada = entrada.lower()
        entrada = entrada + ' '

        # Contadores de lexemas por token
        buena = 0
        neutra = 0
        mala = 0

        # Por cada caracter en la entrada
        for caracter in entrada:
            
            # Si el caracter no es un espacio, salto de línea, tabulación o retorno de carro seguir procesando caracteres, caso contrario o es un lexema ya
            # completo o es un espacio en blanco 
            if not(caracter in [' ', '\n', '\t', '\r']):
                # Si el caracter es un caracter especial, no se considera caso contrario se agrega al lexema y se mueve al siguiente nodo
                if caracter in ['/', '.', ',', '?', '¿', '!', '¡', '(', ')', '"', ':', ';', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]:
                    continue
                else:
                    lexema = lexema + caracter
                    siguiente = siguiente.mover(caracter)
            else:
                # Si el lexema es vacío, no hacer nada caso contrario se marca el nodo actual como estado final
                if lexema == '':
                    continue
                else:
                    siguiente.estado_final = True
                    # Interfaz para preguntar al usuario que tipo de lexema es en caso de no tener un token asignado
                    if siguiente.token == '':
                        print('\t' + lexema + ' no pertenece a ningún token')
                        # Mostrar ventana emergente
                        mostrar_emergente(siguiente, lexema, id_peticion)
                    else:
                        print('\t' + lexema + ' pertenece al token ' + siguiente.token)

                    # Agregar el lexema a la lista de lexemas
                    lexemas.append(lexema)
                    
                    # Contador de lexemas por token
                    if siguiente.token[-5:] == "BUENA":
                        buena += 1
                    elif siguiente.token[-6:] == "NEUTRA":
                        neutra += 1
                    else:
                        mala += 1
                    
                    # Reiniciar el lexema y el nodo actual vuelve a la raiz
                    lexema = ''
                    siguiente = raiz
    
    # Mostrar los resultados en una ventana emergente
    if id_peticion ==  0:
        messagebox.showinfo("Resultados", "El analisis ha arrojado los siguientes resultados :\n\n{}: {}\n{}: {}\n{}: {}".format(token_buena, buena, token_neutra, neutra, token_mala, mala))
    else:
        messagebox.showinfo("Resultados", "El analisis ha arrojado los siguientes resultados :\n\n{}: {}\n{}: {}\n{}: {}".format(token_buena, buena, token_neutra, neutra, token_mala, mala))
    
    # Actualizar el puntaje
    puntaje[0] = buena
    puntaje[1] = neutra
    puntaje[2] = mala

    # Eliminar lexemas duplicados convirtiendo a conjunto y luego a lista
    lexemas = list(set(lexemas))
    # Ordenar lexicográficamente
    lexemas.sort()

    # Copiar lexemas en lexemas_retorno
    lexemas_retorno.clear()
    for lexema in lexemas:
        lexemas_retorno.append(lexema)

    # Guardar el tokenizador
    guardar_tokenizador(raiz, id_peticion)

    # Liberar la memoria
    raiz = None

############################### main ###############################

print('Iniciando la aplicación...')
print('Fecha y hora: ' + str(datetime.datetime.now()))

# Crear la ventana principal
root = tk.Tk()
root.title("Speech Analytics")
root.resizable(0, 0)

# Establecer el icono de la ventana
root.iconbitmap("static/lapiz.ico")

# Creamos un marco dentro de root
frm = tk.Frame(root, pady=5, padx=5)
frm.grid()

# Array de 3 elementos
ATC_Puntaje = [0, 0, 0]
EXP_Puntaje = [0, 0, 0]

# Lista de lexemas
lexemas_personal = []
lexemas_cliente = []

# Crear un área de texto para el personal junto con su boton
titulo_personal = tk.Label(frm, text='Personal', font=('', 13)).grid(column=0, row=0)
texto_area_personal = tk.Text(frm, bg="#D0E8C5")
texto_area_personal.grid(column=0, row=1, pady=5, padx=2.5)
# Crear un marco para los botones del personal en el marco frm en la grilla de la columna 0 y fila 2
frm_personal = tk.Frame(frm)
frm_personal.grid(column=0, row=2)
# Agregamos los botones en dos columnas en el marco generado anteriormente
btn_procesar_personal = tk.Button(frm_personal, text="Procesar", command=lambda: procesar(0, ATC_Puntaje, lexemas_personal)).grid(column=0, row=0, pady=5, padx=5)
btn_actualizar_tokens_personal = tk.Button(frm_personal, text="Administrar Tokens", command=lambda: ventana_tokens(0, lexemas_personal)).grid(column=1, row=0, pady=5)

# Crear un área de texto para el cliente junto con su boton
titulo_cliente = tk.Label(frm, text='Cliente', font=('', 13)).grid(column=1, row=0, pady=5)
texto_area_cliente = tk.Text(frm, bg="#E8DAC5")
texto_area_cliente.grid(column=1, row=1, pady=5, padx=2.5)
# Crear un marco para los botones del cliente en el marco frm en la grilla de la columna 1 y fila 2
frm_cliente = tk.Frame(frm)
frm_cliente.grid(column=1, row=2)
# Agregamos los botones en dos columnas en el marco generado anteriormente
btn_procesar_cliente = tk.Button(frm_cliente, text="Procesar", command=lambda: procesar(1, EXP_Puntaje, lexemas_cliente)).grid(column=0, row=0, pady=5, padx=5)
btn_actualizar_tokens_cliente = tk.Button(frm_cliente, text="Administrar Tokens", command=lambda: ventana_tokens(1, lexemas_cliente)).grid(column=1, row=0, pady=5)

# Boton resumen
btn_resumen = tk.Button(frm, text="Generar Resumen", command=lambda: resumen(ATC_Puntaje, EXP_Puntaje)).grid(column=0, row=4, columnspan=2, pady=5)

# Ejecutar el bucle principal de la aplicación
root.mainloop()