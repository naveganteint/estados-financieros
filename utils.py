import numpy as np
import streamlit as st
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import re





def fila_a_array(df, numero_fila, humana=True):
    """
    Devuelve la fila indicada como array de numpy, eliminando los dos primeros elementos
    y reordenando el resto en orden invertido (primero → último, segundo → penúltimo, ...).

    Parámetros:
    - df : DataFrame
    - numero_fila : número de fila
    - humana=True → la fila empieza en 1
      humana=False → la fila empieza en 0
    """
    try:
        # Seleccionar fila
        if humana:
            fila = df.iloc[numero_fila - 1]
        else:
            fila = df.iloc[numero_fila]

        # Convertir a array numpy
        arr = fila.to_numpy()

        # 1️⃣ eliminar los dos primeros elementos
        arr = arr[2:]

        # 2️⃣ invertir el orden de los elementos restantes
        arr = arr[::-1]

        return arr

    except IndexError:
        return None
    





def mostrar_array_horizontal(arr):
    """
    Muestra un array o lista en Streamlit como tabla horizontal centrada.
    """
    if arr is None or len(arr) == 0:
        st.info("El array está vacío.")
        return
    
    arr_np = np.array(arr)
    
    # Crear DataFrame de una fila
    df_horizontal = pd.DataFrame([arr_np], columns=[f"año {i+1}" for i in range(len(arr_np))])


    

    
    # Convertir DataFrame a HTML centrando los valores
    html_table = df_horizontal.to_html(index=False)
    
    # Añadir estilo CSS para centrar los valores
    html_table = html_table.replace(
        '<table border="1" class="dataframe">',
        '<table border="1" class="dataframe" style="width: 100%; text-align: center;">'
    )
    
    css_th = """
    <style>
    table.dataframe th {
        text-align: center;      /* Centra los encabezados */
        background-color: #f0f0f0;  /* Opcional: fondo gris para distinguir encabezado */
        padding: 5px;
    }
    table.dataframe td {
        padding: 5px;
    }
    </style>
    """
    
    st.markdown(css_th,  unsafe_allow_html=True)


    st.markdown(html_table, unsafe_allow_html=True)




def procesar_array(arr):
    """
    Toma un array o lista, elimina los dos primeros elementos
    y luego invierte el orden del resto.
    
    Parámetros:
    - arr: lista o array
    
    Retorna:
    - array procesado
    """
    if arr is None or len(arr) <= 2:
        return []  # No hay suficientes elementos
    
    # Eliminar los dos primeros elementos y voltear el resto
    arr_procesado = arr[2:][::-1]
    
    return arr_procesado

# Mostrar dos array  ********************************************************************************************************





def mostrar_dos_arrays(arr1, arr2):
    """
    Muestra dos arrays como tabla de 2 filas en Streamlit con celdas centradas,
    sin títulos ni encabezados. Convierte NumPy arrays a listas normales automáticamente.
    
    Parámetros:
    - arr1: primer array o lista
    - arr2: segundo array o lista
    """
    # Convertir a listas normales si son NumPy arrays
    if isinstance(arr1, np.ndarray):
        arr1 = arr1.tolist()
    if isinstance(arr2, np.ndarray):
        arr2 = arr2.tolist()
    




    # Verificar que tengan la misma longitud
    if len(arr1) != len(arr2):
        st.error("Los arrays deben tener la misma longitud")
        return
    

    datos=[]


    for x in arr2:
        
        if pd.isna(x):
            datos.append("-")
        
        elif x < 0:
            datos.append(f'<span style="color:red;">{x}</span>')
        
     
        else:
            datos.append(f"{x}")




    # Crear DataFrame de 2 filas
    df = pd.DataFrame([datos], columns=arr1)
    
    # Convertir DataFrame a HTML
    html_table = df.to_html(index=False, header=True,table_id="tabla_2lista",escape=False,)
    
    css ="""
    <style>
    table.dataframe#tabla_2lista {
      
        width: auto;            /* ancho automático según contenido */
        border-collapse: collapse;
        margin-left: auto;
        margin-right: auto;     /* centra la tabla */
}

  

    table.dataframe#tabla_2lista tbody tr{
        background-color: white;
        text-align: center;
        padding: 2px;
    }

    
    table#tabla_2lista thead th {
        background-color: #D9E6E7;   
        text-align: center;
        padding: 1px;
    }
    






    /* Opcional: bordes de celdas */
    table.dataframe td {
        border: 1px solid #ccc;
    }
    </style>
    """
    

  
    
    # Mostrar CSS y tabla
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)


#Funcion para introducir una grafica de barras*********************************************************************************


def grafica_columnas(arr1, arr2,eje_x,eje_y,color_barras):
    

    df = pd.DataFrame({'x':arr1, 'y':arr2})

    # Crear figura Matplotlib
    fig, ax = plt.subplots(figsize=(7,4))  # tamaño relativo
    ax.bar(df['x'], df['y'], color=color_barras)
    ax.set_xlabel(eje_x,color='gray',fontsize=12, labelpad=15)
    ax.set_ylabel(eje_y,color='gray',fontsize=12, labelpad=15)
    #ax.set_title('Gráfico de Barras con Matplotlib')
    ax.set_xticks(df['x'])

    ax.tick_params(axis='x', colors='gray', length=5, width=1)  # ticks eje X
    ax.tick_params(axis='y', colors='gray', length=5, width=1)  # ticks eje Y

    # Líneas horizontales de fondo (gridlines)
    ax.yaxis.grid(True, color='gray', linestyle='-', linewidth=1)  # gris claro y punteado
    ax.set_axisbelow(True)  # asegura que las líneas queden debajo de las barras


    # Eliminar todos los spines (bordes de la gráfica)
    for spine in ax.spines.values():
        spine.set_visible(False)


    # Guardar figura en buffer
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')  # bbox_inches evita recorte de etiquetas
    buf.seek(0)

    # Convertir a base64 para incrustar en HTML
    img_base64 = base64.b64encode(buf.read()).decode()

    # HTML para centrar imagen con ancho fijo de 700px
    st.markdown(f"""
    <div style="display:flex; justify-content:center;">
        <img src="data:image/png;base64,{img_base64}" width="700px">
    </div>
    """, unsafe_allow_html=True)


#************************ graficar tres lineas ***********************************

def graficar_tres_lineas(lista1, lista2, lista3,color1,color2,color3, eje_x=None, etiquetas=None, eje_y="margenes %"):
        """
        Genera una gráfica de líneas con tres listas de valores usando Matplotlib y la muestra en Streamlit.
        
        Parámetros:
        - lista1, lista2, lista3: listas de valores numéricos (misma longitud)
        - eje_x: lista de valores para el eje X (por ejemplo años). Por defecto 1..n
        - etiquetas: lista de 3 strings para la leyenda de cada línea (opcional)
        - titulo: título de la gráfica
        - eje_y: nombre del eje Y (por defecto "Valores")
        """
        # Validar longitud
        n = len(lista1)
        if len(lista2) != n or len(lista3) != n:
            raise ValueError("Todas las listas deben tener la misma longitud")
        
        # Eje X por defecto
        if eje_x is None:
            eje_x = list(range(1, n+1))
        
        if len(eje_x) != n:
            raise ValueError("La lista del eje X debe tener la misma longitud que las listas de valores")
        
        # Etiquetas por defecto
        if etiquetas is None:
            etiquetas = ["Línea 1", "Línea 2", "Línea 3"]
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(7,4))                             
        
        # Graficar líneas
        ax.plot(eje_x, lista1,  label=etiquetas[0], color=color1)
        ax.plot(eje_x, lista2,  label=etiquetas[1], color=color2)
        ax.plot(eje_x, lista3,  label=etiquetas[2], color=color3)
        

        # Eliminar todos los spines (bordes de la gráfica)
        for spine in ax.spines.values():
            spine.set_visible(False)


        # Títulos y etiquetas
        #ax.set_title(titulo, fontsize=14)
        ax.set_xlabel("Año" if eje_x else "Índice", fontsize=12, color='gray')
        ax.set_ylabel(eje_y, fontsize=12, color='gray')

        
        ax.tick_params(axis='x', colors='gray', length=5, width=1)  # ticks eje X
        ax.tick_params(axis='y', colors='gray', length=5, width=1)  # ticks eje Y

        
        # Leyenda y cuadrícula
        ax.legend()
     
        
        ax.yaxis.grid(True, color='gray', linestyle='-', linewidth=1)  # gris claro y punteado
        ax.axhline(y=0, color='black', linewidth=2, linestyle='-')

        plt.tight_layout()
        
        
        # Guardar figura en buffer
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')  # bbox_inches evita recorte de etiquetas
        buf.seek(0)

        # Convertir a base64 para incrustar en HTML
        img_base64 = base64.b64encode(buf.read()).decode()

        # HTML para centrar imagen con ancho fijo de 700px
        st.markdown(f"""
        <div style="display:flex; justify-content:center;">
            <img src="data:image/png;base64,{img_base64}" width="700px">
        </div>
        """, unsafe_allow_html=True)





#******************************mostrar cuatro arrays ***********************************

def mostrar_cuatro_arrays(arr1, arr2, arr3, arr4):
    """
    Muestra una tabla en Streamlit con 4 listas:
    - arr1: encabezado de la tabla
    - arr2, arr3, arr4: filas de datos
    Las celdas están centradas y no se colorean los valores.
    
    Parámetros:
    - arr1: lista de nombres de columnas
    - arr2, arr3, arr4: listas de datos (misma longitud que arr1)
    """
    # Convertir a listas normales si son NumPy arrays
    for i, arr in enumerate([arr1, arr2, arr3, arr4]):
        if isinstance(arr, np.ndarray):
            if i == 0:
                arr1 = arr.tolist()
            elif i == 1:
                arr2 = arr.tolist()
            elif i == 2:
                arr3 = arr.tolist()
            elif i == 3:
                arr4 = arr.tolist()

    # Verificar que todas las listas tengan la misma longitud
    n = len(arr1)
    if not all(len(lst) == n for lst in [arr2, arr3, arr4]):
        st.error("Todas las listas deben tener la misma longitud que el encabezado")
        return

    datos1=[]
    datos2=[]
    datos3=[]    


    def cambia_celda (lista,datos):
        for x in lista:
                
                if pd.isna(x):
                    datos.append("-")
                
                elif x < 0:
                    datos.append(f'<span style="color:red;">{x}</span>')
                
            
                else:
                    datos.append(f"{x}")

    
    cambia_celda(arr2,datos1)
    cambia_celda(arr3,datos2)
    cambia_celda(arr4,datos3)



    # Crear DataFrame con arr1 como columnas y arr2, arr3, arr4 como filas
    df = pd.DataFrame([datos1, datos2, datos3], columns=arr1)

    # Convertir DataFrame a HTML
    html_table = df.to_html(index=False, header=True, table_id="tabla_4listas", escape=False)

    # CSS para centrar celdas y encabezado
    css = """
    <style>
    table.dataframe#tabla_4listas {
        width: auto;
        border-collapse: collapse;
        margin-left: auto;
        margin-right: auto; /* centra la tabla */
    }

    table.dataframe#tabla_4listas tbody tr{
        background-color: white;
        text-align: center;
        padding: 4px;
    }

    table#tabla_4listas thead th {
        background-color: #D9E6E7;
        text-align: center;
        padding: 4px;
    }

    table.dataframe#tabla_4listas td {
        border: 1px solid #ccc;
    }
    </style>
    """

    # Mostrar CSS y tabla
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)


#*************************limpiar lista*******************


def limpiar_porcentajes(lista):
        """
        Limpia una lista con valores tipo '1.86%' o '<span style="color:red;">-3.92%</span>'
        y devuelve solo los valores numéricos (float).
        """

        resultado = []

        for x in lista:

            if x in ["", "-", None]:
                resultado.append(None)
                continue

            # eliminar etiquetas HTML
            x = re.sub(r'<.*?>', '', x)

            # eliminar símbolo %
            x = x.replace('%', '')

            try:
                resultado.append(float(x))
            except:
                resultado.append(None)

        return resultado


#***********************************Restar listas *********************************************************

def restar_listas(lista1, lista2):
    """
    Resta dos listas elemento a elemento.
    Si alguno de los valores es None, devuelve "-".
    """

    if len(lista1) != len(lista2):
        raise ValueError("Las listas deben tener la misma longitud")

    resultado = []

    for a, b in zip(lista1, lista2):

        if a is None or b is None:
            resultado.append("-")
        else:
            resultado.append(round(b - a, 2))
   

    return resultado


# ******************** diferencia de cagr *******************

def dif_cagr(resta_lista):
    st.write("")
    st.markdown(
    '<div style="text-align: center; font-size: 16px;">Diferencia entre <b>CAGR EPS - CAGR Net income</b></div>',
    unsafe_allow_html=True)


    # Crear DataFrame: primera columna vacía para la primera celda, sin generar columna extra
    columnas = ["dif CAGR", "9y", "7y", "5y", "3y", "1y"]

    resta_lista2=[]
    for x in resta_lista:
        try:
            # intentar convertir a float
            num = float(x)
            if num < 0:
                resta_lista2.append(f'<span style="color:red;">{num}%</span>')
            elif num > 2:
                resta_lista2.append(f'<span style="color:green;">{num}%</span>')
            else:
                resta_lista2.append(f"{num}")
        except (ValueError, TypeError):
            # si no se puede convertir, ponemos guion
            resta_lista2.append("-")





    df = pd.DataFrame([resta_lista2], columns=columnas)
    df.iloc[0, 0] = ""
    # Convertir a HTML sin índice
    

    
    html = df.to_html(index=False,escape=False, table_id="tabla_cagr")



    # CSS para centrar tabla
    estilo = """
    <style>
        table.dataframe#tabla_cagr {
            width: auto;
            border-collapse: collapse;
            margin-left: auto;
            margin-right: auto;
            text-align: center;
        }
        table.dataframe#tabla_cagr tbody tr{
            background-color: white;
            text-align: center;
            padding: 2px ;
        }
        table#tabla_cagr thead th {
            background-color: #D9E6E7;
            text-align: center;
            padding: 1px 8px;
        }
    </style>
        """
    
    st.markdown(estilo, unsafe_allow_html=True)

    st.markdown(html, unsafe_allow_html=True)



    #**************************graficar una linea ********************************************


def graficar_una_linea (lista, color, eje_x=None, etiqueta="Línea", eje_y="Valores"):
        """
        Genera una gráfica de una sola línea con Matplotlib y la muestra en Streamlit.
        
        Parámetros:
        - lista: lista de valores numéricos
        - eje_x: lista de valores para el eje X (por ejemplo años). Por defecto 1..n
        - etiqueta: nombre de la línea
        - eje_y: nombre del eje Y
        """

        n = len(lista)

        # Eje X por defecto
        if eje_x is None:
            eje_x = list(range(1, n+1))

        if len(eje_x) != n:
            raise ValueError("La lista del eje X debe tener la misma longitud que la lista de valores")

        # Crear figura
        fig, ax = plt.subplots(figsize=(7,4))

        # Graficar línea
        ax.plot(eje_x, lista, label=etiqueta, color=color)

        # Eliminar bordes
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Etiquetas
        ax.set_xlabel("Año" if eje_x else "Índice", fontsize=12, color='gray')
        ax.set_ylabel(eje_y, fontsize=12, color='gray')

        ax.tick_params(axis='x', colors='gray', length=5, width=1)
        ax.tick_params(axis='y', colors='gray', length=5, width=1)

        # Leyenda y grid
        ax.legend()
        ax.yaxis.grid(True, color='gray', linestyle='-', linewidth=1)
        ax.axhline(y=0, color='black', linewidth=2, linestyle='-')

        plt.tight_layout()

        # Guardar figura
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        buf.seek(0)

        img_base64 = base64.b64encode(buf.read()).decode()

        # Mostrar centrada en Streamlit
        st.markdown(f"""
        <div style="display:flex; justify-content:center;">
            <img src="data:image/png;base64,{img_base64}" width="700px">
        </div>
        """, unsafe_allow_html=True)

#****************************************** limpiar lista a solo numeros ***************************

def limpiar_a_numeros(lista):
    """
    Convierte los elementos de una lista a número.
    Si no se pueden convertir, los reemplaza por 0.
    """
    resultado = []

    for x in lista:
        try:
            num = int(x)
            resultado.append(num)
        except (ValueError, TypeError):
            resultado.append(0)

    return resultado

#******************************************************* buscar filar en df ********************************

def buscar_fila(df, texto):
    """
    Busca una cadena en la primera columna de un DataFrame
    y devuelve el número de la fila donde aparece.
    """
    
    col = df.iloc[:, 0]  # primera columna
    
    filas = col[col == texto].index
    
    if len(filas) > 0:
        return filas[0]   # devuelve la primera coincidencia
    else:
        return None
    
#*********************************************suma listas ******************

def suma_listas (lista1,lista2):
    
    lista3=[(a if isinstance(a, (int, float)) else 0) +
    (b if isinstance(b, (int, float)) else 0)
    for a, b in zip(lista1, lista2) ]

    return lista3

#*********************************************resta listas ******************

def resta_listas (lista1,lista2):
    
    lista3=[(a if isinstance(a, (int, float)) else 0) -
    (b if isinstance(b, (int, float)) else 0)
    for a, b in zip(lista1, lista2) ]
    return lista3


#*********************************************dividir listas ******************

def divide_listas (lista1,lista2):
    
    try:
        lista3=[ round((a if isinstance(a, (int, float)) else 0) /
        (b if isinstance(b, (int, float)) else 0),2)
        for a, b in zip(lista1, lista2) ]
    except:
        lista3= 10 * [1]  

    return lista3


#*********************************************mostrar dos barras y una lina ******************




def graficar_barras_y_linea(lista1, lista2, lista3,
                           color1, color2, color3,
                           eje_x=None,
                           etiquetas=None,
                           eje_y_izq="Valores",
                           eje_y_der="Ratio (%)"):

    # Validar longitud
    n = len(lista1)
    if len(lista2) != n or len(lista3) != n:
        raise ValueError("Todas las listas deben tener la misma longitud")

    # Eje X
    if eje_x is None:
        eje_x = list(range(n))

    if len(eje_x) != n:
        raise ValueError("El eje X debe tener la misma longitud")

    # Etiquetas
    if etiquetas is None:
        etiquetas = ["Barras 1", "Barras 2", "Línea"]

    # Crear figura
    fig, ax = plt.subplots(figsize=(7,4))

    x = range(n)
    width = 0.35

    # 🔵 BARRAS (eje izquierdo)
    ax.bar([i - width/2 for i in x], lista1,
           width=width, label=etiquetas[0], color=color1)

    ax.bar([i + width/2 for i in x], lista2,
           width=width, label=etiquetas[1], color=color2)

    # 🔴 LÍNEA (eje derecho)
    ax2 = ax.twinx()
    ax2.plot(x, lista3,
             label=etiquetas[2],
             color=color3,
             marker='o',
             linewidth=2)

    # Eje X
    ax.set_xticks(x)
    ax.set_xticklabels(eje_x)

    # Estilo limpio
    for spine in ax.spines.values():
        spine.set_visible(False)
    for spine in ax2.spines.values():
        spine.set_visible(False)

    # Etiquetas ejes
    ax.set_xlabel("Año", fontsize=12, color='gray')
    ax.set_ylabel(eje_y_izq, fontsize=12, color='gray' )
    ax2.set_ylabel(eje_y_der, fontsize=12,color='gray' )
    

    # Ticks
    ax.tick_params(axis='x', color='gray')
    ax.tick_params(axis='y', color='gray')
    ax2.tick_params(axis='y', color='gray')

    # Grid solo en eje principal
    ax.yaxis.grid(True, color='gray', linestyle='-', linewidth=1)
    ax.axhline(y=0, color='black', linewidth=2)
    ax.set_axisbelow(True)
    
    # 🔥 Leyenda combinada
    lines_1, labels_1 = ax.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax.legend(lines_1 + lines_2, labels_1 + labels_2)

    plt.tight_layout()

    # Exportar a imagen
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode()

    # Mostrar en Streamlit centrado
    st.markdown(f"""
    <div style="display:flex; justify-content:center;">
        <img src="data:image/png;base64,{img_base64}" width="700px">
    </div>
    """, unsafe_allow_html=True)




def crear_tabla_4_listas(lista1, lista2, lista3, lista4, texto1, texto2, texto3):
        """
        Crea una tabla de 4 filas:
        
        - Fila 1: "años" + lista1
        - Fila 2: texto1 + lista2
        - Fila 3: texto2 + lista3
        - Fila 4: texto3 + lista4
        """

        # Validar longitudes
        n = len(lista1)
        if not (len(lista2) == len(lista3) == len(lista4) == n):
            raise ValueError("Todas las listas deben tener la misma longitud")



        # Crear DataFrame
        df = pd.DataFrame(
            [lista2, lista3, lista4],
            columns=lista1  # 👈 los años como columnas
        )

        # Añadir primera columna con etiquetas
        df.insert(0, "años", [texto1, texto2, texto3])

      

        # Convertir DataFrame a HTML
        html_table = df.to_html(index=False, header=True,table_id="tabla_2lista",escape=False,)
        
        css ="""
        <style>
        table.dataframe#tabla_2lista {
        
            width: auto;            /* ancho automático según contenido */
            border-collapse: collapse;
            margin-left: auto;
            margin-right: auto;     /* centra la tabla */
        }
    
        table.dataframe#tabla_2lista tbody tr{
           
            text-align: center;
  
        }

      
        table#tabla_2lista thead th {
            background-color: #D9E6E7;   
            text-align: center;
    
        }
        



        /* Opcional: bordes de celdas */
        table.dataframe td {
            border: 1px solid #ccc;
        }


        table#tabla_2lista tbody tr:nth-child(3) {
        background-color: #E7D6FC !important;
        }
        table.dataframe#tabla_2lista tbody td:first-child {
            font-weight: bold;
        }
        
        table#tabla_2lista td {
        line-height: 1.2; /* más compacto */

        </style>




        """
        

    
        
        # Mostrar CSS y tabla
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(html_table, unsafe_allow_html=True)




def crear_tabla_5_listas(lista1, lista2, lista3, lista4,lista5, texto1, texto2, texto3,texto4):
        """
        Crea una tabla de 4 filas:
        
        - Fila 1: "años" + lista1
        - Fila 2: texto1 + lista2
        - Fila 3: texto2 + lista3
        - Fila 4: texto3 + lista4
        """

        # Validar longitudes
        n = len(lista1)
        if not (len(lista2) == len(lista3) == len(lista4) == len (lista5) ):
            raise ValueError("Todas las listas deben tener la misma longitud")



        # Crear DataFrame
        df = pd.DataFrame(
            [lista2, lista3, lista4,lista5],
            columns=lista1  # 👈 los años como columnas
        )

        # Añadir primera columna con etiquetas
        df.insert(0, "años", [texto1, texto2, texto3,texto4])

      

        # Convertir DataFrame a HTML
        html_table = df.to_html(index=False, header=True,table_id="tabla_5lista",escape=False,)
        
        css ="""
        <style>
        table.dataframe#tabla_5lista {
        
            width: auto;            /* ancho automático según contenido */
            border-collapse: collapse;
            margin-left: auto;
            margin-right: auto;     /* centra la tabla */
        }
    
        table.dataframe#tabla_5lista tbody tr{
           
            text-align: center;
  
        }

      
        table#tabla_5lista thead th {
            background-color: #D9E6E7;   
            text-align: center;
    
        }
        



        /* Opcional: bordes de celdas */
        table.dataframe td {
            border: 1px solid #ccc;
        }

        table.dataframe#tabla_5lista tbody tr:nth-child(4) td {
        background-color: #E7D6FC !important;
        }

        table.dataframe#tabla_5lista tbody td:first-child {
            font-weight: bold;
        }
        
        table#tabla_5lista td {
        line-height: 1.2; /* más compacto */

        </style>




        """
        

    
        
        # Mostrar CSS y tabla
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(html_table, unsafe_allow_html=True)    






#graficas de barras 1+ 2 en 1 y con linea



def graficar_barras_apiladas_y_linea(lista1, lista2, lista3, lista4,
                                    color1, color2, color3, color4,
                                    eje_x=None,
                                    etiquetas=None,
                                    eje_y_izq="Valores",
                                    eje_y_der="Ratio (%)"):

    # Validar longitud
    n = len(lista1)
    if not (len(lista2) == len(lista3) == len(lista4) == n):
        raise ValueError("Todas las listas deben tener la misma longitud")

    # Eje X
    if eje_x is None:
        eje_x = list(range(n))

    if len(eje_x) != n:
        raise ValueError("El eje X debe tener la misma longitud")

    # Etiquetas
    if etiquetas is None:
        etiquetas = ["Barra 1", "Parte 1", "Parte 2", "Línea"]

    # Figura
    fig, ax = plt.subplots(figsize=(7,4))

    x = range(n)
    width = 0.35

    # 🔵 Barra individual (izquierda)
    ax.bar([i - width/2 for i in x], lista1,
           width=width, label=etiquetas[0], color=color1)

    # 🟢 Barras apiladas (derecha)
    ax.bar([i + width/2 for i in x], lista2,
           width=width, label=etiquetas[1], color=color2)

    ax.bar([i + width/2 for i in x], lista3,
           width=width, bottom=lista2,
           label=etiquetas[2], color=color3)

    # 🔴 Línea (eje secundario)
    ax2 = ax.twinx()
    ax2.plot(x, lista4,
             label=etiquetas[3],
             color=color4,
             marker='o',
             linewidth=2)

    # Eje X
    ax.set_xticks(x)
    ax.set_xticklabels(eje_x)

    # Estilo
    for spine in ax.spines.values():
        spine.set_visible(False)
    for spine in ax2.spines.values():
        spine.set_visible(False)

    ax.set_xlabel("Año", fontsize=12, color='gray')
    ax.set_ylabel(eje_y_izq, fontsize=12, color='gray')
    ax2.set_ylabel(eje_y_der, fontsize=12, color='gray')

    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')
    ax2.tick_params(axis='y', colors='gray')

    ax.yaxis.grid(True, color='gray', linestyle='-', linewidth=1)
    ax.axhline(y=0, color='black', linewidth=2)
    ax.set_axisbelow(True)

    # 🔥 Leyenda combinada
    lines_1, labels_1 = ax.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax.legend(lines_1 + lines_2, labels_1 + labels_2)

    plt.tight_layout()

    # Exportar
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode()

    st.markdown(f"""
    <div style="display:flex; justify-content:center;">
        <img src="data:image/png;base64,{img_base64}" width="700px">
    </div>
    """, unsafe_allow_html=True)



    


######################################################### grafica de dos barras ************************************************

def graficar_2barras(lista1, lista2, 
                     color1="blue", color2="orange",
                     eje_x=None,
                     etiquetas=None,
                     eje_y="Valores"):

    # Validar longitud
    if len(lista1) != len(lista2):
        raise ValueError("Las listas deben tener la misma longitud")

    n = len(lista1)

    # Eje X
    if eje_x is None:
        eje_x = list(range(n))

    if len(eje_x) != n:
        raise ValueError("El eje X debe tener la misma longitud")

    # Etiquetas
    if etiquetas is None:
        etiquetas = ["Serie 1", "Serie 2"]

    # Crear figura
    fig, ax = plt.subplots(figsize=(7, 4))

    x = range(n)
    width = 0.35

    # Barras
    ax.bar([i - width/2 for i in x], lista1,
           width=width, label=etiquetas[0], color=color1)

    ax.bar([i + width/2 for i in x], lista2,
           width=width, label=etiquetas[1], color=color2)

    # Eje X
    ax.set_xticks(list(x))
    ax.set_xticklabels(eje_x)

    # Estilo limpio
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Etiquetas
    ax.set_xlabel("Categoría", fontsize=12, color='gray')
    ax.set_ylabel(eje_y, fontsize=12, color='gray')

    # Grid
    ax.yaxis.grid(True, linestyle='-', linewidth=0.5, alpha=0.7)
    ax.axhline(y=0, linewidth=1)
    ax.set_axisbelow(True)

    # Leyenda (corregida)
    ax.legend()

    plt.tight_layout()

    # Exportar a imagen
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode()

    # Mostrar en Streamlit
    st.markdown(f"""
    <div style="display:flex; justify-content:center;">
        <img src="data:image/png;base64,{img_base64}" width="700px">
    </div>
    """, unsafe_allow_html=True)



######################################################### grafica N barras ************************************************


def graficar_n_barras(listas, 
                     colores=None,
                     eje_x=None,
                     etiquetas=None,
                     eje_y="Valores"):

    n_series = len(listas)   # número de barras (ej: 9)
    n = len(listas[0])       # número de categorías

    # Validar que todas las listas tengan la misma longitud
    for lista in listas:
        if len(lista) != n:
            raise ValueError("Todas las listas deben tener la misma longitud")

    # Eje X
    if eje_x is None:
        eje_x = list(range(n))

    if len(eje_x) != n:
        raise ValueError("El eje X debe tener la misma longitud")

    # Etiquetas
    if etiquetas is None:
        etiquetas = [f"Serie {i+1}" for i in range(n_series)]

    # Colores
    if colores is None:
        colores = plt.cm.tab10.colors[:n_series]

    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 5))

    x = list(range(n))
    width = 0.8 / n_series   # 👈 clave: repartir espacio

    # Dibujar barras
    for i, lista in enumerate(listas):
        desplazamiento = (i - n_series/2) * width + width/2

        ax.bar([xi + desplazamiento for xi in x],
               lista,
               width=width,
               label=etiquetas[i],
               color=colores[i])

    # Eje X
    ax.set_xticks(x)
    ax.set_xticklabels(eje_x)
    ax.set_axisbelow(True)

    # Estilo
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xlabel("Año", fontsize=12, color='gray')
    ax.set_ylabel(eje_y, fontsize=12, color='gray')

    ax.yaxis.grid(True, linestyle='-', linewidth=0.5, alpha=0.7)
    ax.axhline(y=0, linewidth=1)

    ax.legend(ncol=3)  # 👈 útil cuando hay muchas series

    plt.tight_layout()

    # Exportar a imagen
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode()

    st.markdown(f"""
    <div style="display:flex; justify-content:center;">
        <img src="data:image/png;base64,{img_base64}" width="900px">
    </div>
    """, unsafe_allow_html=True) 



#**************************************mostrar dos array con titulo

    
def mostrar_dos_arrays_texto(lista1, lista2 ,texto):
        # Validar longitudes
    if len(lista1) != len(lista2):
        raise ValueError("Las listas deben tener la misma longitud")

    # Crear encabezado (años)
    columnas = ["años"] + lista1

    # Crear fila de datos
    fila = [texto] + lista2

    # Crear DataFrame
    df = pd.DataFrame([fila], columns=columnas)
    
    # Convertir DataFrame a HTML
    html_table = df.to_html(index=False, header=True,table_id="tabla_2lista",escape=False,)
    
    css ="""
    <style>
    table.dataframe#tabla_2lista {
      
        width: auto;            /* ancho automático según contenido */
        border-collapse: collapse;
        margin-left: auto;
        margin-right: auto;     /* centra la tabla */
}

  

    table.dataframe#tabla_2lista tbody tr{
        background-color: white;
        text-align: center;
        padding: 2px;
    }

    
    table#tabla_2lista thead th {
        background-color: #D9E6E7;   
        text-align: center;
        padding: 1px;
    }
    






    /* Opcional: bordes de celdas */
    table.dataframe td {
        border: 1px solid #ccc;
    }
    </style>
    """
    

  
    
    # Mostrar CSS y tabla
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)








def crear_tabla_6_listas(lista1, lista2, lista3, lista4,lista5,lista6, texto1, texto2, texto3,texto4,texto5):
        """
        Crea una tabla de 4 filas:
        
        - Fila 1: "años" + lista1
        - Fila 2: texto1 + lista2
        - Fila 3: texto2 + lista3
        - Fila 4: texto3 + lista4
        """

        # Validar longitudes
        n = len(lista1)
        if not (len(lista2) == len(lista3) == len(lista4) == len (lista5)== len (lista6) ):
            raise ValueError("Todas las listas deben tener la misma longitud")



        # Crear DataFrame
        df = pd.DataFrame(
            [lista2, lista3, lista4,lista5,lista6],
            columns=lista1  # 👈 los años como columnas
        )

        # Añadir primera columna con etiquetas
        df.insert(0, "años", [texto1, texto2, texto3,texto4,texto5])

      

        # Convertir DataFrame a HTML
        html_table = df.to_html(index=False, header=True,table_id="tabla_6lista",escape=False,)
        
        css ="""
        <style>
        table.dataframe#tabla_6lista {
        
            width: auto;            /* ancho automático según contenido */
            border-collapse: collapse;
            margin-left: auto;
            margin-right: auto;     /* centra la tabla */
        }
    
        table.dataframe#tabla_5lista tbody tr{
           
            text-align: center;
  
        }

      
        table#tabla_6lista thead th {
            background-color: #D9E6E7;   
            text-align: center;
    
        }
        



        /* Opcional: bordes de celdas */
        table.dataframe td {
            border: 1px solid #ccc;
        }

        table.dataframe#tabla_6lista tbody tr:nth-child(5) td {
        background-color: #E7D6FC !important;
        }

        table.dataframe#tabla_6lista tbody td:first-child {
            font-weight: bold;
        }
        
        table#tabla_6lista td {
        line-height: 1.2; /* más compacto */

        </style>




        """
        

    
        
        # Mostrar CSS y tabla
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(html_table, unsafe_allow_html=True)    


