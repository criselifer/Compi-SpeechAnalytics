from dfa import *
import tkinter as tk
from tkinter import messagebox
from tokenizador import *
import datetime
from hash_function import HashFunction
from window_gestor_token import ventana_tokens
from window_seleccion_token import mostrar_emergente

def resumen(puntuacion_personal, puntuacion_cliente):
    """
    Función que genera un resumen de los resultados obtenidos.
    Parámetros:
        ATC_Puntaje([]): array de 3 elementos para almacenar el puntaje de cada tipo de lexema del personal
        EXP_Puntaje([]): array de 3 elementos para almacenar el puntaje de cada tipo de lexema del cliente
    Returns:
        None
    """
    print('Generando resumen...')

    puntuacion_global = (puntuacion_personal + puntuacion_cliente) / 2

    # Mostrar los resultados en una ventana emergente
    messagebox.showinfo("Resumen", "Resumen de los resultados:\n\n- PERSONAL: {:.2f} \n- CLIENTE: {:.2f} \n\nPUNTUACION DE LA LLAMADA: {:.2f}".format(puntuacion_personal, puntuacion_cliente, puntuacion_global))
    #messagebox.showinfo("Resumen", "Resumen de los resultados:\n\nPersonal:\nATC_BUENA: {}\nATC_NEUTRA: {}\nATC_MALA: {}\n\nCliente:\nEXP_BUENA: {}\nEXP_NEUTRA: {}\nEXP_MALA: {}".format(ATC_Puntaje[0], ATC_Puntaje[1], ATC_Puntaje[2], EXP_Puntaje[0], EXP_Puntaje[1], EXP_Puntaje[2]))
    print('Resumen generado con éxito')

def resaltar_palabras(raiz, id_peticion, lexemas):
    """
    Función que resalta las palabras segun el token al que corresponde en el texto ingresado por el usuario.
    Parámetros:
        id_peticion(int): 0 para el personal, 1 para el cliente
        lexemas_retorno([]): lista de lexemas
    Returns:
        None
    """
    # Cargar los tokens
    tokens = {}
    cargar_tokens(raiz, tokens, lexemas)

    # Crear un diccionario con las palabras a resaltar y el tag correspondiente
    palabras_a_resaltar = {}
    for lexema in lexemas:
        palabras_a_resaltar[lexema] = tokens[lexema]

    # Seleccionar el widget de texto correspondiente según la petición
    if id_peticion == 0:
        text_widget = texto_area_personal
    else:
        text_widget = texto_area_cliente
    
    # Borrar los resaltados anteriores
    for lexema in lexemas:
        text_widget.tag_remove('ATC_MALA', '1.0', tk.END)
        text_widget.tag_remove('ATC_NEUTRA', '1.0', tk.END)
        text_widget.tag_remove('ATC_BUENA', '1.0', tk.END)

        text_widget.tag_remove('EXP_MALA', '1.0', tk.END)
        text_widget.tag_remove('EXP_NEUTRA', '1.0', tk.END)
        text_widget.tag_remove('EXP_BUENA', '1.0', tk.END)
        
    # Resaltar las palabras en el texto
    text_content = text_widget.get("1.0", tk.END).lower()
    for palabra, tag in palabras_a_resaltar.items():
        start_idx = 0
        while True:
            # Buscar la palabra en el texto
            start_idx = text_content.find(palabra, start_idx)
            if start_idx == -1:
                break
            
            # Asegurarse de que la palabra no sea parte de otra palabra
            if (start_idx == 0 or not text_content[start_idx - 1].isalnum()) and (start_idx + len(palabra) == len(text_content) - 1 or not text_content[start_idx + len(palabra)].isalnum()):
                # Calcular la posición en el widget original
                line_idx = int(text_widget.index(f"1.0+{start_idx}c").split('.')[0])
                col_idx = int(text_widget.index(f"1.0+{start_idx}c").split('.')[1])
                start_tk_idx = f"{line_idx}.{col_idx}"
                end_tk_idx = f"{line_idx}.{col_idx + len(palabra)}"
                # Agregar la etiqueta para resaltar la palabra
                text_widget.tag_add(tag, start_tk_idx, end_tk_idx)
            
            start_idx += len(palabra)

    # Configurar los colores de los tags según el token
    text_widget.tag_config('ATC_MALA', background='#FFBABA', foreground='black')
    text_widget.tag_config('EXP_MALA', background='#FFBABA', foreground='black')

    text_widget.tag_config('ATC_NEUTRA', background='#E0E0E0', foreground='black')
    text_widget.tag_config('EXP_NEUTRA', background='#E0E0E0', foreground='black')

    text_widget.tag_config('ATC_BUENA', background='#DFF2BF', foreground='black')
    text_widget.tag_config('EXP_BUENA', background='#DFF2BF', foreground='black')

def procesar(id_peticion, puntaje, lexemas_retorno, puntuacion):
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
    
    ban_saludo, ban_despedida = False, False
    if id_peticion == 0:

        # Mapear si en la entrada hay algun saludo
        print('Mapeando saludos...')
        saludos = ['buenos días', 'buen día', 'buenas tardes', 'buenas noches']
        ban_saludo = False
        for saludo in saludos:
            if saludo in entrada:
                ban_saludo = True
                break
        if ban_saludo:
            print('Saludo encontrado')
        else:
            print('Saludo no encontrado')

        # Mapear si en la entrada hay alguna despedida
        print('Mapeando despedidas...')
        despedidas = ['hasta luego']
        ban_despedida = False
        for despedida in despedidas:
            if despedida in entrada:
                ban_despedida = True
                break
        if ban_despedida:
            print('Despedida encontrada')
        else:
            print('Despedida no encontrada')
        
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
            if not(caracter in [' ', '\n', '\t', '\r', '.']):
                # Si el caracter es un caracter especial, no se considera caso contrario se agrega al lexema y se mueve al siguiente nodo
                if caracter in ['/', ',', '?', '¿', '!', '¡', '(', ')', '"', ':', ';', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]:
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

        # Inicializar las puntuaciones
        puntuacion_buena = buena
        puntuacion_mala = mala

        # Ajustar las puntuaciones basadas en los indicadores de saludo y despedida
        if ban_saludo:
            puntuacion_buena += 1
        else:
            puntuacion_mala += 1
            
        if ban_despedida:
            puntuacion_buena += 1
        else:
            puntuacion_mala += 1

        # Verificar que no haya división por cero
        total_puntuaciones = puntuacion_buena + puntuacion_mala
        if total_puntuaciones == 0:
            puntuacion_personal = 1
        else:

            # Normalizar los puntajes
            buena_normalizado = puntuacion_buena / total_puntuaciones
            mala_normalizado = puntuacion_mala / total_puntuaciones

            # Calcular la ponderación final en escala del 1 al 5
            puntuacion_personal = 1 + ( 0 if (buena_normalizado - mala_normalizado) <= 0 else (buena_normalizado - mala_normalizado) ) * 4

        puntuacion[0] = puntuacion_personal

        messagebox.showinfo("Resultados", "El analisis ha arrojado los siguientes resultados :\n\n- {} : {}\n- {}: {}\n- {}: {} \n- SALUDO: {} \n- DESPEDIDA: {} \n\n- Balance buenas: {} \n- Balance malas: {} \nPuntuacion final: {:.2f}".format(token_buena, buena, token_neutra, neutra, token_mala, mala, 'Si' if ban_saludo else 'No', 'Si' if ban_despedida else 'No', puntuacion_buena, puntuacion_mala, puntuacion_personal))
    else:
    
        # Inicializar las puntuaciones
        puntuacion_buena = buena
        puntuacion_mala = mala

        # Verificar que no haya división por cero
        total_puntuaciones = puntuacion_buena + puntuacion_mala
        if total_puntuaciones == 0:
            puntuacion_cliente = 1
        else:

            # Normalizar los puntajes
            buena_normalizado = puntuacion_buena / total_puntuaciones
            mala_normalizado = puntuacion_mala / total_puntuaciones

            # Calcular la ponderación final en escala del 1 al 5
            puntuacion_cliente = 1 + ( 0 if (buena_normalizado - mala_normalizado) <= 0 else (buena_normalizado - mala_normalizado) ) * 4
        
        puntuacion[1] = puntuacion_cliente
    
        messagebox.showinfo("Resultados", "El analisis ha arrojado los siguientes resultados :\n\n- {}: {}\n- {}: {}\n- {}: {} \n\nPuntuacion final: {:.2f}".format(token_buena, buena, token_neutra, neutra, token_mala, mala, puntuacion_cliente))
    
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

    resaltar_palabras(raiz, id_peticion, lexemas_retorno)

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

puntuacion = [0, 0]

# Crear un área de texto para el personal junto con su boton
titulo_personal = tk.Label(frm, text='Personal', font=('', 13)).grid(column=0, row=0)
texto_area_personal = tk.Text(frm)
texto_area_personal.grid(column=0, row=1, pady=5, padx=2.5)
# Crear un marco para los botones del personal en el marco frm en la grilla de la columna 0 y fila 2
frm_personal = tk.Frame(frm)
frm_personal.grid(column=0, row=2)
# Agregamos los botones en dos columnas en el marco generado anteriormente
btn_procesar_personal = tk.Button(frm_personal, text="Procesar", command=lambda: procesar(0, ATC_Puntaje, lexemas_personal, puntuacion)).grid(column=0, row=0, pady=5, padx=5)
btn_actualizar_tokens_personal = tk.Button(frm_personal, text="Administrar Tokens", command=lambda: ventana_tokens(0, lexemas_personal)).grid(column=1, row=0, pady=5)

# Crear un área de texto para el cliente junto con su boton
titulo_cliente = tk.Label(frm, text='Cliente', font=('', 13)).grid(column=1, row=0, pady=5)
texto_area_cliente = tk.Text(frm)
texto_area_cliente.grid(column=1, row=1, pady=5, padx=2.5)
# Crear un marco para los botones del cliente en el marco frm en la grilla de la columna 1 y fila 2
frm_cliente = tk.Frame(frm)
frm_cliente.grid(column=1, row=2)
# Agregamos los botones en dos columnas en el marco generado anteriormente
btn_procesar_cliente = tk.Button(frm_cliente, text="Procesar", command=lambda: procesar(1, EXP_Puntaje, lexemas_cliente, puntuacion)).grid(column=0, row=0, pady=5, padx=5)
btn_actualizar_tokens_cliente = tk.Button(frm_cliente, text="Administrar Tokens", command=lambda: ventana_tokens(1, lexemas_cliente)).grid(column=1, row=0, pady=5)

# Boton resumen
btn_resumen = tk.Button(frm, text="Generar Resumen", command=lambda: resumen(puntuacion[0], puntuacion[1])).grid(column=0, row=4, columnspan=2, pady=5)

# Ejecutar el bucle principal de la aplicación
root.mainloop()