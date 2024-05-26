import tkinter as tk

def func_mala(siguiente, ventana_emergente, token):
    """
    Función que asigna el token correspondiente a un lexema malo.
    Parámetros:
        siguiente(Nodo): nodo actual del DFA.
        ventana_emergente(Toplevel): ventana emergente.
        token(str): token seleccionado.
    Returns:
        None
    """
    siguiente.token = token
    print("\t\t" + token + " seleccionado")
    ventana_emergente.destroy()

def func_neutral(siguiente, ventana_emergente, token):
    """
    Función que asigna el token correspondiente a un lexema neutro.
    Parámetros:
        siguiente(Nodo): nodo actual del DFA.
        ventana_emergente(Toplevel): ventana emergente.
        token(str): token seleccionado.
    Returns:
        None
    """
    siguiente.token = token
    print("\t\t" + token + " seleccionado")
    ventana_emergente.destroy()

def func_buena(siguiente, ventana_emergente, token):
    """
    Función que asigna el token correspondiente a un lexema bueno.
    Parámetros:
        siguiente(Nodo): nodo actual del DFA.
        ventana_emergente(Toplevel): ventana emergente.
        token(str): token seleccionado.
    Returns:
        None
    """
    siguiente.token = token
    print("\t\t" + token + " seleccionado")
    ventana_emergente.destroy()

def crear_boton(contenedor, token, bg_color, funcion, ventana_emergente, nodo):
    """
    Función que crea un botón con un color de fondo y una función asociada.
    Parámetros:
        contenedor(Frame): contenedor del botón.
        token(str): token del botón.
        bg_color(str): color de fondo del botón.
        funcion(func): función asociada al botón.
        ventana_emergente(Toplevel): ventana emergente.
        nodo(Nodo): nodo actual del DFA.
    Returns:
        Button: botón creado.
    """
    return tk.Button(contenedor, text=token, bg=bg_color, fg="black", command=lambda: funcion(nodo, ventana_emergente, token))

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

    # Crear un contenedor para los botones
    contenedor_botones = tk.Frame(ventana_emergente)
    contenedor_botones.pack(pady=5)

    # Crear los botones dentro del contenedor de botones
    btn_mala = crear_boton(contenedor_botones, token_mala, "#FFBABA", func_mala, ventana_emergente, siguiente)
    btn_mala.pack(side=tk.LEFT, padx=3, pady=5)
    btn_neutral = crear_boton(contenedor_botones, token_neutra, "#E0E0E0", func_neutral, ventana_emergente, siguiente)
    btn_neutral.pack(side=tk.LEFT, padx=3, pady=5)
    btn_buena = crear_boton(contenedor_botones, token_buena, "#DFF2BF", func_buena, ventana_emergente, siguiente)
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