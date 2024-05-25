from dfa import *
import tkinter as tk
from tkinter import messagebox
from tokenizador import *
import datetime
from hash_function import HashFunction
from window_gestor_token import ventana_actualizar_tokens

def resumen(ATC_Puntaje, EXP_Puntaje):
    """
        ATC_Puntaje: array de 3 elementos para almacenar el puntaje de cada tipo de lexema del personal
        EXP_Puntaje: array de 3 elementos para almacenar el puntaje de cada tipo de lexema del cliente
    """
    print('Generando resumen...')
    # Mostrar los resultados en una ventana emergente
    messagebox.showinfo("Resumen", "Resumen de los resultados:\n\nPersonal:\nATC_BUENA: {}\nATC_NEUTRA: {}\nATC_MALA: {}\n\nCliente:\nEXP_BUENA: {}\nEXP_NEUTRA: {}\nEXP_MALA: {}".format(ATC_Puntaje[0], ATC_Puntaje[1], ATC_Puntaje[2], EXP_Puntaje[0], EXP_Puntaje[1], EXP_Puntaje[2]))
    print('Resumen generado con éxito')

def mostrar_emergente(siguiente, lexema, id_peticion):
    """
    Función que muestra una ventana emergente para que el usuario seleccione el token correspondiente a un lexema.
    Parámetros:
        siguiente(Nodo): nodo actual del DFA.
        lexema(str): lexema a categorizar.
        id_peticion(int): 0 para el personal, 1 para el cliente.
    Returns:
        None
    """
    if id_peticion == 0:
        token_mala = 'ATC_MALA'
        token_neutra = 'ATC_NEUTRA'
        token_buena = 'ATC_BUENA'
    else:
        token_mala = 'EXP_MALA'
        token_neutra = 'EXP_NEUTRA'
        token_buena = 'EXP_BUENA'

    ventana_emergente = tk.Toplevel()
    ventana_emergente.title("Categorización de lexemas")
    ventana_emergente.resizable(0, 0)

    # Crear un contenedor para la etiqueta de texto
    contenedor_texto = tk.Frame(ventana_emergente)
    contenedor_texto.pack(pady=5)
    etiqueta_texto = tk.Label(contenedor_texto, text="¿A qué token pertenece el lexema '{}' ?".format(lexema), font=("Arial", 12))
    etiqueta_texto.pack()

    # Funciones para asignar el token correspondiente
    def func_mala(siguiente, lexema):
        siguiente.token = token_mala
        print("\t\t" + token_mala + " seleccionado")
        ventana_emergente.destroy()

    def func_neutral(siguiente, lexema):
        siguiente.token = token_neutra
        print("\t\t" + token_neutra + " seleccionado")
        ventana_emergente.destroy()

    def func_buena(siguiente, lexema):
        siguiente.token = token_buena
        print("\t\t" + token_buena + " seleccionado")
        ventana_emergente.destroy()

    # Función para crear botones con colores específicos y texto en blanco
    def crear_boton(contenedor, texto, bg_color, opcion, funcion):
        return tk.Button(contenedor, text=texto, bg=bg_color, fg="black", command=lambda: funcion(siguiente, lexema))

    # Crear un contenedor para los botones
    contenedor_botones = tk.Frame(ventana_emergente)
    contenedor_botones.pack(pady=5)

    # Crear los botones dentro del contenedor de botones
    btn_mala = crear_boton(contenedor_botones, token_mala, "#FFBABA", 1, func_mala)
    btn_mala.pack(side=tk.LEFT, padx=3, pady=5)

    btn_neutral = crear_boton(contenedor_botones, token_neutra, "#E0E0E0", 2, func_neutral)
    btn_neutral.pack(side=tk.LEFT, padx=3, pady=5)

    btn_buena = crear_boton(contenedor_botones, token_buena, "#DFF2BF", 3, func_buena)
    btn_buena.pack(side=tk.LEFT, padx=3, pady=5)

    # Centrar el contenedor de texto en la ventana emergente
    contenedor_texto.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    # Centrar el contenedor de botones debajo del contenedor de texto
    contenedor_botones.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    # Establecer el tamaño de la ventana emergente
    ventana_emergente.geometry("400x100")

    # Centrar la ventana emergente en la pantalla
    ventana_emergente.update_idletasks()
    wventana = ventana_emergente.winfo_width()
    hventana = ventana_emergente.winfo_height()
    pwidth = (ventana_emergente.winfo_screenwidth() - wventana) // 2
    pheight = (ventana_emergente.winfo_screenheight() - hventana) // 2
    ventana_emergente.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

    # Mostrar la ventana emergente y esperar a que se cierre
    ventana_emergente.wait_window(ventana_emergente)

def procesar(id_peticion, puntaje, lexemas_retorno):
    """
        id_peticion: 0 para el personal, 1 para el cliente
        puntaje: array de 3 elementos para almacenar el puntaje de cada tipo de lexema
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

        # Creamos nuestra función hash
        hash_alfabeto = HashFunction().get_funcion_hash()

        siguiente = raiz
        lexema = ''
        lexemas = []

        # Preprocesamiento de la entrada
        entrada = entrada.lower()
        entrada = entrada + ' '

        # contadores
        buena = 0
        neutra = 0
        mala = 0

        for caracter in entrada:
            
            if not(caracter in [' ', '\n', '\t', '\r']):
                if caracter in ['/', '.', ',', '?', '¿', '!', '¡', '(', ')', '"', ':', ';', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]:
                    continue
                else:
                    lexema = lexema + caracter
                    siguiente = siguiente.mover(caracter)
            else:

                if lexema == '':
                    continue
                else:
                
                    siguiente.estado_final = True
                    
                    # Interfaz para preguntar al usuario que tipo de lexema es
                    if siguiente.token == '':
                        print('\t' + lexema + ' no pertenece a ningún token')
                        mostrar_emergente(siguiente, lexema, id_peticion)
                    else:
                        print('\t' + lexema + ' pertenece al token ' + siguiente.token)

                    lexemas.append(lexema)
                    
                    # Contador de lexemas
                    if siguiente.token[-5:] == "BUENA":
                        buena += 1
                    elif siguiente.token[-6:] == "NEUTRA":
                        neutra += 1
                    else:
                        mala += 1
                    
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

    # Eliminar duplicados convirtiendo a conjunto y luego a lista
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
btn_actualizar_tokens_personal = tk.Button(frm_personal, text="Actualizar Tokens", command=lambda: ventana_actualizar_tokens(0, lexemas_personal)).grid(column=1, row=0, pady=5)

# Crear un área de texto para el cliente junto con su boton
titulo_cliente = tk.Label(frm, text='Cliente', font=('', 13)).grid(column=1, row=0, pady=5)
texto_area_cliente = tk.Text(frm, bg="#E8DAC5")
texto_area_cliente.grid(column=1, row=1, pady=5, padx=2.5)
# Crear un marco para los botones del cliente en el marco frm en la grilla de la columna 1 y fila 2
frm_cliente = tk.Frame(frm)
frm_cliente.grid(column=1, row=2)
# Agregamos los botones en dos columnas en el marco generado anteriormente
btn_procesar_cliente = tk.Button(frm_cliente, text="Procesar", command=lambda: procesar(1, EXP_Puntaje, lexemas_cliente)).grid(column=0, row=0, pady=5, padx=5)
btn_actualizar_tokens_cliente = tk.Button(frm_cliente, text="Actualizar Tokens", command=lambda: ventana_actualizar_tokens(1, lexemas_cliente)).grid(column=1, row=0, pady=5)

# Boton resumen
btn_resumen = tk.Button(frm, text="Generar Resumen", command=lambda: resumen(ATC_Puntaje, EXP_Puntaje)).grid(column=0, row=4, columnspan=2, pady=5)

# Ejecutar el bucle principal de la aplicación
root.mainloop()