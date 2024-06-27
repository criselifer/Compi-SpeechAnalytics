import tkinter as tk
from tokenizador import *

def ventana_tokens(id_peticion, lexemas):
    """
    Actualiza los tokens de los lexemas en la interfaz gráfica y en el tokenizador.
    Parametros:
        id_peticion(int): 0 para el personal, 1 para el cliente
        lexemas([]): lista de lexemas
    Retorna:
        None
    """
    print('Actualizando los tokens de los lexemas... {}'.format(lexemas))

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
            siguiente = siguiente.mover(caracter)
        siguiente.token = nuevo_token

        # Guardar el tokenizador actualizado
        if id_peticion == 0:
            guardar_tokenizador(raiz, 0)
        else:
            guardar_tokenizador(raiz, 1)

        # Liberar la memoria
        raiz = None

    def actualizar_color(palabra):
        """
        Actualiza el color del token en la interfaz gráfica según el valor del token.
        Parametros:
            palabra(str): palabra cuyo token se va a cambiar
        Retorna:
            None
        """
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
        # Cambiar el color del token en la interfaz gráfica según el valor del token
        color = color_mapping[id_peticion].get(tokens[palabra], "#FFFFFF")
        token_labels[palabra].config(text=tokens[palabra], bg=color)

    def dibujar_contenido():
        """
        Dibuja el contenido de la interfaz gráfica.
        Retorna:
            None
        """
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Añadir títulos de las columnas
        tk.Label(scrollable_frame, text="#", font=('Helvetica', 10, 'bold')).grid(column=0, row=0, pady=5, padx=5)
        tk.Label(scrollable_frame, text="Palabra", font=('Helvetica', 10, 'bold')).grid(column=1, row=0, pady=5, padx=5)
        tk.Label(scrollable_frame, text="Token Actual", font=('Helvetica', 10, 'bold')).grid(column=2, row=0, pady=5, padx=5)
        tk.Label(scrollable_frame, text="Cambio Token", font=('Helvetica', 10, 'bold')).grid(column=3, row=0, pady=5, padx=5, columnspan=3)

        # Mostrar la lista de palabras en una grilla junto con los botones para cambiar el token
        for i, palabra in enumerate(lexemas, start=1):

            tk.Label(scrollable_frame, text=str(i)).grid(column=0, row=i, pady=5, padx=5)
            tk.Label(scrollable_frame, text=palabra).grid(column=1, row=i, pady=5, padx=5)
            token_label = tk.Label(scrollable_frame, text=tokens[palabra], bg="#E0E0E0")
            token_label.grid(column=2, row=i, pady=5, padx=5)
            token_labels[palabra] = token_label
            actualizar_color(palabra)
                
            # Colores y estados de los tokens según el tipo de petición. 0 para el personal, 1 para el cliente
            if id_peticion == 0:
                estados = ["ATC_MALA", "ATC_NEUTRA", "ATC_BUENA"]
                colores = ["#FFBABA", "#E0E0E0", "#DFF2BF"]
            else:
                estados = ["EXP_MALA", "EXP_NEUTRA", "EXP_BUENA"]
                colores = ["#FFBABA", "#E0E0E0", "#DFF2BF"]

            # Crear botones para cambiar el token
            for j, estado in enumerate(estados):
                tk.Button(scrollable_frame, text=estado, bg=colores[j], command=lambda p=palabra, e=estado: cambiar_token(p, e)).grid(column=3+j, row=i, pady=5, padx=5)

    def on_frame_configure(event):
        """
        Configura el tamaño del canvas y el scrollregion del canvas.
        Parametros:
            event(tk.Event): evento de configuración
        Retorna:
            None
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

    if id_peticion == 0:
        print('Actualizando los tokens del personal...')
    else:
        print('Actualizando los tokens del cliente...')

    # Cargar el tokenizador
    raiz = cargar_tokenizador(id_peticion)

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Gestor de Tokens")
    root.resizable(0, 0)
    root.geometry("530x600")

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

    # Crear un diccionario para almacenar los tokens de cada palabra, y otro para almacenar los labels de los tokens.
    # Esto es necesario para actualizar los tokens en la interfaz gráfica.
    tokens = {}
    token_labels = {}

    # Cargar los tokens de los lexemas en el diccionario tokens. Necesario para actualizar los tokens en la interfaz gráfica.
    cargar_tokens(raiz, tokens, lexemas)

    # Dibujar el contenido inicial
    dibujar_contenido()

    root.mainloop()
    
    if id_peticion == 0:
        print('Tokens del personal actualizados con éxito')
    else:
        print('Tokens del cliente actualizados con éxito')

    # Liberar la memoria
    raiz = None
