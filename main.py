from core import *
import tkinter as tk
import datetime
import pickle
from tkinter import messagebox

def actualizar_tokens(id_peticion, lexemas):
    """
        Actualiza los tokens de los lexemas en la interfaz gráfica y en el tokenizador.
        Parametros:
            id_peticion(int): 0 para el personal, 1 para el cliente
            lexemas([]): lista de lexemas
        Retorna:
            None
    """

    print('Actualizando los tokens de los lexemas... {}'.format(lexemas))

    def cargar_tokens(raiz, tokens, lexemas):
        """
            Carga los tokens de los lexemas recibidos en el parametro tokens. Los tokens son obtenidos del DFA apuntado por raiz.
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
                siguiente = mover(siguiente, caracter)
            siguiente.estado_final = True
            tokens[lexema] = siguiente.token

        print('Tokens cargados con éxito')

    def cambiar_token(palabra, nuevo_token):
        """
            Cambia el token de la palabra recibida en el parametro palabra por el token recibido en el parametro nuevo_token.
            Estos cambios se reflejan en la interfaz gráfica y en el tokenizador.
            Parametros:
                palabra(str): palabra cuyo token se va a cambiar
                nuevo_token(str): nuevo token
            Retorna:
                None
        """

        tokens[palabra] = nuevo_token
        actualizar_color(palabra)
        print(f"Token de '{palabra}' cambiado a '{nuevo_token}'")

        # Cargo el tokenizador
        if id_peticion == 0:
            raiz = cargar_tokenizador(0)
        else:
            raiz = cargar_tokenizador(1)
        siguiente = raiz

        # Actualizar el token del lexema cambiado en el Tokenizador
        for caracter in palabra:
            siguiente = mover(siguiente, caracter)
        siguiente.token = nuevo_token

        # Guardar el tokenizador actualizado
        if id_peticion == 0:
            guardar_tokenizador(raiz, 0)
        else:
            guardar_tokenizador(raiz, 1)

    def actualizar_color(palabra):
        color_mapping = {
            0: {
                "ATC_BUENA": "#DFF2BF",  # Verde claro
                "ATC_NEUTRA": "#E0E0E0", # Gris claro
                "ATC_MALA": "#FFBABA"    # Rojo claro
            },
            1: {
                "EXP_BUENA": "#DFF2BF",  # Verde claro
                "EXP_NEUTRA": "#E0E0E0", # Gris claro
                "EXP_MALA": "#FFBABA"    # Rojo claro
            }
        }
        
        color = color_mapping[id_peticion].get(tokens[palabra], "#FFFFFF")  # Default to white if token is not found
        token_labels[palabra].config(text=tokens[palabra], bg=color)


    def dibujar_contenido():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Añadir títulos de las columnas
        tk.Label(scrollable_frame, text="#", font=('Helvetica', 10, 'bold')).grid(column=0, row=0, pady=5, padx=5)
        tk.Label(scrollable_frame, text="Palabra", font=('Helvetica', 10, 'bold')).grid(column=1, row=0, pady=5, padx=5)
        tk.Label(scrollable_frame, text="Token Actual", font=('Helvetica', 10, 'bold')).grid(column=2, row=0, pady=5, padx=5)
        tk.Label(scrollable_frame, text="Cambio Token", font=('Helvetica', 10, 'bold')).grid(column=3, row=0, pady=5, padx=5, columnspan=3)

        # Mostrar la lista de palabras en una grilla junto con los botones
        for i, palabra in enumerate(lexemas, start=1):
            tk.Label(scrollable_frame, text=str(i)).grid(column=0, row=i, pady=5, padx=5)
            tk.Label(scrollable_frame, text=palabra).grid(column=1, row=i, pady=5, padx=5)
            token_label = tk.Label(scrollable_frame, text=tokens[palabra], bg="#E0E0E0")
            token_label.grid(column=2, row=i, pady=5, padx=5)
            token_labels[palabra] = token_label
            actualizar_color(palabra)
                
            # Crear botones para cambiar el token
            if id_peticion == 0:
                estados = ["ATC_MALA", "ATC_NEUTRA", "ATC_BUENA"]
                colores = ["#FFBABA", "#E0E0E0", "#DFF2BF"]
            else:
                estados = ["EXP_MALA", "EXP_NEUTRA", "EXP_BUENA"]
                colores = ["#FFBABA", "#E0E0E0", "#DFF2BF"]

            for j, estado in enumerate(estados):
                tk.Button(scrollable_frame, text=estado, bg=colores[j], command=lambda p=palabra, e=estado: cambiar_token(p, e)).grid(column=3+j, row=i, pady=5, padx=5)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    if id_peticion == 0:

        print('Actualizando los tokens del personal...')

        # Cargar el tokenizador
        raiz = cargar_tokenizador(id_peticion)

        # Crear la ventana principal
        root = tk.Tk()
        root.title("Gestor de Tokens")
        root.resizable(0, 0)
        root.geometry("500x600")

        # Establecer el icono de la ventana
        root.iconbitmap("static/lapiz.ico")

        # Crear un frame para contener el canvas y la scrollbar
        container = tk.Frame(root)
        container.pack(fill="both", expand=True)

        # Crear un canvas dentro del frame
        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        # Añadir una scrollbar vertical al canvas
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configurar el canvas para usar la scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Crear un frame dentro del canvas
        scrollable_frame = tk.Frame(canvas)

        # Crear una ventana en el canvas que contenga el frame
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Vincular el evento de configuración del frame con la función
        scrollable_frame.bind("<Configure>", on_frame_configure)

        # Crear un diccionario para almacenar los tokens de cada palabra
        tokens = {}
        token_labels = {}

        cargar_tokens(raiz, tokens, lexemas)

        # Dibujar el contenido inicial
        dibujar_contenido()

        root.mainloop()

    else:
        print('Actualizando los tokens del cliente...')

        # Cargar el tokenizador
        raiz = cargar_tokenizador(id_peticion)

        # Crear la ventana principal
        root = tk.Tk()
        root.title("Gestor de Tokens")
        root.resizable(0, 0)
        root.geometry("500x600")

        # Establecer el icono de la ventana
        root.iconbitmap("static/lapiz.ico")

        # Crear un frame para contener el canvas y la scrollbar
        container = tk.Frame(root)
        container.pack(fill="both", expand=True)

        # Crear un canvas dentro del frame
        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        # Añadir una scrollbar vertical al canvas
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configurar el canvas para usar la scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Crear un frame dentro del canvas
        scrollable_frame = tk.Frame(canvas)

        # Crear una ventana en el canvas que contenga el frame
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Vincular el evento de configuración del frame con la función
        scrollable_frame.bind("<Configure>", on_frame_configure)

        # Crear un diccionario para almacenar los tokens de cada palabra
        tokens = {}
        token_labels = {}

        cargar_tokens(raiz, tokens, lexemas)

        # Dibujar el contenido inicial
        dibujar_contenido()

        root.mainloop()

def resumen(ATC_Puntaje, EXP_Puntaje):
    """
        ATC_Puntaje: array de 3 elementos para almacenar el puntaje de cada tipo de lexema del personal
        EXP_Puntaje: array de 3 elementos para almacenar el puntaje de cada tipo de lexema del cliente
    """
    print('Generando resumen...')
    # Mostrar los resultados en una ventana emergente
    messagebox.showinfo("Resumen", "Resumen de los resultados:\n\nPersonal:\nATC_BUENA: {}\nATC_NEUTRA: {}\nATC_MALA: {}\n\nCliente:\nEXP_BUENA: {}\nEXP_NEUTRA: {}\nEXP_MALA: {}".format(ATC_Puntaje[0], ATC_Puntaje[1], ATC_Puntaje[2], EXP_Puntaje[0], EXP_Puntaje[1], EXP_Puntaje[2]))
    print('Resumen generado con éxito')

def guardar_tokenizador(raiz, id_peticion):

    # Guardar la estructura en un archivo
    nombre_archivo = 'tokenizador' + str(id_peticion) + '.pkl'
    if id_peticion == 0:
        print('Guardando el TOKENIZADOR del personal...')
    else:
        print('Guardando el TOKENIZADOR del cliente...')
    with open(nombre_archivo, 'wb') as archivo:
        pickle.dump(raiz, archivo)
        print('TOKENIZADOR guardado con éxito')

def cargar_tokenizador(id_peticion):

    # Cargar el AFD
    nombre_archivo = 'tokenizador' + str(id_peticion) + '.pkl'
    if id_peticion == 0:
        print('Cargando el TOKENIZADOR del personal...')
    else:
        print('Cargando el TOKENIZADOR del cliente...')
    raiz = None
    try:
        with open(nombre_archivo, 'rb') as archivo:
            raiz = pickle.load(archivo)
            print('TOKENIZADOR cargado con éxito')
    except (FileNotFoundError, IOError, EOFError) as e:
        print(f"No se pudo abrir el archivo: {e}")
        # Como aun no se ha creado el archivo entonces hay que crear el AFD desde cero
        raiz = Nodo()

    return raiz

def mostrar_emergente(siguiente, lexema, id_peticion):
    """
        id_peticion: 0 para el personal, 1 para el cliente
    """

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
        hash_alfabeto = crear_funcion_hash()

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
                    siguiente = mover(siguiente, caracter)
            else:

                if lexema == '':
                    continue
                else:
                
                    siguiente.estado_final = True
                    
                    # interfaz para preguntar al usuario que tipo de lexema es
                    if siguiente.token == '':
                        print('\t' + lexema + ' no pertenece a ningún token')
                        mostrar_emergente(siguiente, lexema, id_peticion)
                    else:
                        print('\t' + lexema + ' pertenece al token ' + siguiente.token)

                    lexemas.append(lexema)
                    
                    # contador de lexemas
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
    print(lexemas)

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
btn_procesar_personal = tk.Button(frm, text="Procesar", command=lambda: procesar(0, ATC_Puntaje, lexemas_personal)).grid(column=0, row=2, pady=5)
btn_actualizar_tokens_personal = tk.Button(frm, text="Actualizar Tokens", command=lambda: actualizar_tokens(0, lexemas_personal)).grid(column=0, row=3, pady=5)

# Crear un área de texto para el cliente junto con su boton
titulo_cliente = tk.Label(frm, text='Cliente', font=('', 13)).grid(column=1, row=0, pady=5)
texto_area_cliente = tk.Text(frm, bg="#E8DAC5")
texto_area_cliente.grid(column=1, row=1, pady=5, padx=2.5)
btn_procesar_cliente = tk.Button(frm, text="Procesar", command=lambda: procesar(1, EXP_Puntaje, lexemas_cliente)).grid(column=1, row=2, pady=5)
btn_actualizar_tokens_cliente = tk.Button(frm, text="Actualizar Tokens", command=lambda: actualizar_tokens(1, lexemas_cliente)).grid(column=1, row=3, pady=5)

# Boton resumen
btn_resumen = tk.Button(frm, text="Resumen", command=lambda: resumen(ATC_Puntaje, EXP_Puntaje)).grid(column=0, row=4, columnspan=2, pady=5)

# Ejecutar el bucle principal de la aplicación
root.mainloop()