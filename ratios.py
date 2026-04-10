
import streamlit as st
import pandas as pd
import numpy as np


def mostrar_cagr_tabla(lista_valores, limite_sup):
    valores = list(lista_valores)

    def cagr(inicio, final, n):
        # Control completo de errores
        if inicio is None or final is None:
            return None
        
        if inicio <= 0 or final <= 0:
            return None
        
        ratio = final / inicio
        
        if ratio <= 0:
            return None
        
        return (ratio) ** (1/n) - 1

    periodos = [9, 7, 5, 3, 1]

    resultados = []
    for p in periodos:
        try:
            resultados.append(cagr(valores[-(p+1)], valores[-1], p))
        except:
            resultados.append(None)

    # Convertir a porcentaje
    resultados_num = [r*100 if r is not None else np.nan for r in resultados]

    columnas = ["CAGR", "9y", "7y", "5y", "3y", "1y"]
    fila = [""]

    for x in resultados_num:

        if pd.isna(x):
            fila.append("-")

        elif x < 0:
            fila.append(f'<span style="color:red;">{x:.2f}%</span>')

        elif x > limite_sup:
            fila.append(f'<span style="color:green;">{x:.2f}%</span>')

        else:
            fila.append(f"{x:.2f}%")

    df = pd.DataFrame([fila], columns=columnas)

    html = df.to_html(index=False, escape=False, table_id="tabla_cagr")

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

    return fila


#******* Calcular margenes % *************************************************************


def dividir_y_convertir_a_porcentaje(lista1, lista2):
    """
    Divide cada elemento de lista1 entre el correspondiente de lista2,
    multiplica el resultado por 100 y devuelve una nueva lista.
    
    Parámetros:
    - lista1: primera lista de números
    - lista2: segunda lista de números (debe tener la misma longitud que lista1)
    
    Retorna:
    - lista de resultados en porcentaje
    """
    if len(lista1) != len(lista2):
        raise ValueError("Las listas deben tener la misma longitud")

    resultados = []
    for a, b in zip(lista1, lista2):
        if b == 0:
            resultados.append(None)  # evitar división por cero
        else:
            resultados.append(round((a / b) * 100, 2))
    return resultados



#************************** convertir a numero B o M ************************************************************


def convertir_a_numero(lista):
    """
    Convierte valores tipo '1.7B', '500M', etc. a números reales.
    B = miles de millones
    M = millones
    """
    
    resultado = []

    for x in lista:
        if isinstance(x, str):

            if x.endswith("B"):
                valor = float(x[:-1]) * 1_000

            elif x.endswith("M"):
                valor = float(x[:-1]) * 1

            else:
                valor = float(x)

        else:
            valor = x

        resultado.append(valor)

    return resultado


#***************************** Calcular EPS y formula similares

def dividir_listas(beneficios, acciones):
    """
    Calcula el beneficio por acción (EPS).

    Parámetros:
    - beneficios: lista de beneficios netos
    - acciones: lista de número de acciones

    Retorna:
    - lista con el EPS para cada elemento
    """

    if len(beneficios) != len(acciones):
        raise ValueError("Las listas deben tener la misma longitud")

    eps = []

    for b, a in zip(beneficios, acciones):
        if a == 0:
            eps.append(None)  # evitar división por cero
        else:
            eps.append(round(float(b / a), 4))

   
    return eps


#*************************************calcula tax rate (tasa de impuesto) ********************************

def calculo_tasa(beneficios_a_i, impuesto):
    """
    Calcula el tax rate (tasa de impuesto)

   
    """

    if len(beneficios_a_i) != len(impuesto):
        raise ValueError("Las listas deben tener la misma longitud")

    tax_rate = []

    for a, b in zip(beneficios_a_i, impuesto):
        if a == 0:
            tax_rate.append(None)  # evitar división por cero
        else:
            if a > 0:
                if b > 0:
                    tax_rate.append(round(b/a, 2))
                else:
                    tax_rate.append(round(0.25, 2))                   
            else:
                    tax_rate.append(round(0, 2))     
                 
   
    return tax_rate



#**************************************** Multiplicar dos listas *******************************
def calcular_nopat(lista1, lista2):
    """
    Calcula el beneficio por acción (EPS).

    Parámetros:
    - beneficios: lista de beneficios netos
    - acciones: lista de número de acciones

    Retorna:
    - lista con el EPS para cada elemento
    """

    if len(lista1) != len(lista2):
        raise ValueError("Las listas deben tener la misma longitud")

    resultado = []

    for b, a in zip(lista1, lista2):
            resultado.append(round(b * (1-a) , 2))

   
    return resultado



#****************************************** sumar 5 listas ***************************************

def sumar_cinco_listas(l1, l2, l3, l4, l5):
    """
    Suma los elementos de cinco listas por posición
    y devuelve una nueva lista con los resultados.
    """
    resultado = []

    for a, b, c, d, e in zip(l1, l2, l3, l4, l5):
        resultado.append(a + b + c + d + e)

    return resultado


#*********************** promedio lista ***********************************************

def promedio(lista):
    valores = []

    for x in lista:
        try:
            valores.append(float(x))
        except:
            continue

    return sum(valores) / len(valores) if valores else None
