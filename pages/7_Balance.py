import streamlit as st
from styles import aplicar_estilos,h3_especial
import ratios as rt
import utils as ut
import pandas as pd
import extraccion as ex



# Comprobar que la hoja "balance" está cargada
if "hojas" in st.session_state and "balance" in st.session_state.hojas:
    df_balance = st.session_state.hojas["balance"]

# Comprobar que la hoja "resultado" está cargada
if "hojas" in st.session_state and "resultado" in st.session_state.hojas:
    df_resultado = st.session_state.hojas["resultado"]


# Comprobar que la hoja "resultado" está cargada
if "hojas" in st.session_state and "flujo" in st.session_state.hojas:
    df_flujo = st.session_state.hojas["flujo"]



aplicar_estilos()




st.markdown(
    '<h1 style="text-align: center; color: #1b3865; margin-top: -40px;">Balance</h1>',
    unsafe_allow_html=True
)




años=df_resultado.columns.tolist()
años=ut.procesar_array (años)

#*****************************************************Patrimonio neto **********************************************

h3_especial("Patrimonio Neto")

fila=ut.buscar_fila(df_balance, "Shareholders' Equity")

patrimonio = ut.fila_a_array(df_balance, fila+1)
patrimonio = [float(x) for x in patrimonio]


ut.grafica_columnas(años,patrimonio,"Años","Patrimonio (m)","#DEB887")


ut.mostrar_dos_arrays_texto(años, patrimonio,"Patrimonio")



rt.mostrar_cagr_tabla(patrimonio,5)
st.write("")


#******************************************************Retained Earnings**********************************************

h3_especial("Retained Earnings")

fila=ut.buscar_fila(df_balance, "Retained Earnings")

retained = ut.fila_a_array(df_balance, fila+1)
retained = [float(x) for x in retained]


ut.grafica_columnas(años,retained,"Años","Retained Earnings (m)","#BDB76B")


ut.mostrar_dos_arrays_texto(años, retained ,"Retained earnings")


rt.mostrar_cagr_tabla(retained,5)


#****************************************************** Intagibles **********************************************

goodwill=ex.goodwill(df_balance)
intangible=ex.intangibles(df_balance)
activos_intagibles=ut.suma_listas (goodwill,intangible)




activos=ex.activos(df_balance)
porcen_godwill= ut.divide_listas (goodwill,activos)
porcen_intangibles=ut.divide_listas (intangible,activos)
porcen_total_intagibles=ut.divide_listas(activos_intagibles,activos)

porcen_godwill = [round(x*100,2) for x in porcen_godwill]
porcen_intangibles = [round(x*100,2) for x in porcen_intangibles]
porcen_total_intagibles = [round(x*100,2) for x in porcen_total_intagibles]


ut.graficar_tres_lineas(porcen_godwill, porcen_intangibles, porcen_total_intagibles,"#7EC5E6", "#2F7392","#02354D", eje_x=años, etiquetas=("Goodwill", "Otros intangibles" , "Total intangibles"), eje_y=" intangibles/activos %")


#****************************************************** Nº acciones **********************************************

h3_especial("Nª de acciones")

fila=ut.buscar_fila(df_resultado, "Shares (Diluted)")
num_acciones=ut.fila_a_array (df_resultado,fila+1)
num_acciones_num=rt.convertir_a_numero(num_acciones)


ut.graficar_una_linea (num_acciones_num, '#20B2AA', eje_x=años, etiqueta="numº de acciones", eje_y="Acciones")


ut.mostrar_dos_arrays_texto(años, num_acciones_num ,"Nº de acciones (Millones)")


rt.mostrar_cagr_tabla(num_acciones_num,100)


#****************************************************** Estructura Global de la empresa  *********************************************
h3_especial("Estructura Global de la empresa (ratio de endeudamiento)")

fila=ut.buscar_fila(df_balance, "Total Assets")
activos = ut.fila_a_array(df_balance, fila+1)
activos = [float(x) for x in activos]

#ut.mostrar_dos_arrays(años, activos)

Liabilities= [
    round((a if isinstance(a, (int, float)) else 0) -
    (b if isinstance(b, (int, float)) else 0),2)
    for a, b in zip(activos, patrimonio)
]


Debt_to_equity=  rt.dividir_y_convertir_a_porcentaje(Liabilities,patrimonio)
Debt_to_equity= [round(x/100,2) if isinstance(x, (int, float)) else x for x in Debt_to_equity]
#ut.graficar_una_linea (Debt_to_equity, "#EB5D44", eje_x=años, etiqueta="Ratio de endeudamiento", eje_y="Pasivo en relacion a patrimonio")


ut.graficar_barras_y_linea(Liabilities, patrimonio, Debt_to_equity, "#DF7E7E","#AF9476", "#2E88D1",
                           eje_x=años, etiquetas=("Pasivo","Patrimonio","ratio"),eje_y_izq="Millones",
                           eje_y_der="Ratio")


ut.crear_tabla_4_listas(años, Liabilities, patrimonio, Debt_to_equity, "Pasivos","Patrimonio","Ratio  pasivo/patrimonio")





total=ut.suma_listas(Liabilities,patrimonio)

porc_patrimonio=ut.divide_listas(patrimonio,total)
porc_patrimonio = [round(x*100,2) for x in porc_patrimonio]

lim_sup = 10*[50]
lim_inf=10*[30]




ut.graficar_tres_lineas(porc_patrimonio,lim_sup, lim_inf,'#9370D8', 'lightgreen','coral', eje_x=años, etiquetas=("ratio patrimonio/activos %", "lim recomendado" , "lim min recomendado"), eje_y="% patrimonio")

ut.mostrar_dos_arrays_texto(años, porc_patrimonio ,"% patrimonio / activos")






#****************************************************** ACtivos  **********************************************

h3_especial("Activos")

fila=ut.buscar_fila(df_balance, "Total Assets")
activos = ut.fila_a_array(df_balance, fila+1)
activos = [float(x) for x in activos]

#ut.mostrar_dos_arrays(años, activos)


fila=ut.buscar_fila(df_balance, "Total Current Assets")
activos_current = ut.fila_a_array(df_balance, fila+1)
activos_current = [float(x) for x in activos_current]

#ut.mostrar_dos_arrays(años, activos_current)


fila=ut.buscar_fila(df_balance, "Goodwill")
goodwill = ut.fila_a_array(df_balance, fila+1)
goodwill = [0 if pd.isna(x) else x for x in goodwill]
goodwill = [float(x) for x in goodwill]


#ut.mostrar_dos_arrays(años, goodwill)


fila=ut.buscar_fila(df_balance, "Other Intangible Assets")
other_intagibles = ut.fila_a_array(df_balance, fila+1)
other_intagibles = [0 if pd.isna(x) else x for x in other_intagibles]


other_intagibles = [float(x) for x in other_intagibles]



#ut.mostrar_dos_arrays(años, goodwill)
#ut.mostrar_dos_arrays(años, other_intagibles)



intangibles= [
    round((a if isinstance(a, (int, float)) else 0) +
    (b if isinstance(b, (int, float)) else 0),2)
    for a, b in zip(other_intagibles, goodwill)
]


#ut.mostrar_dos_arrays(años, intangibles)


suma_aux= [
    round((a if isinstance(a, (int, float)) else 0) +
    (b if isinstance(b, (int, float)) else 0),2)
    for a, b in zip(intangibles, activos_current)
]


activo_non_current= [
    round((a if isinstance(a, (int, float)) else 0) -
    (b if isinstance(b, (int, float)) else 0),2)
    for a, b in zip(activos, suma_aux)
]


porc_activos_current= rt.dividir_y_convertir_a_porcentaje(activos_current,activos)
porc_activos_non_current= rt.dividir_y_convertir_a_porcentaje(activo_non_current,activos)
porc_intangibles= rt.dividir_y_convertir_a_porcentaje(intangibles,activos)



ut.graficar_tres_lineas(porc_activos_current,porc_activos_non_current, porc_intangibles,'#87CEFA', '#6495ED','#FF69B4', eje_x=años, etiquetas=("current", "Non current" , "Intagibles"), eje_y="% Activos")


ut.crear_tabla_4_listas(años, porc_activos_current, porc_intangibles, porc_activos_non_current, "activos cp","activos tangibles","Activos lp")





#******************************************************Pasivo **********************************************

h3_especial("Pasivo balance")

fila=ut.buscar_fila(df_balance, "Total Liabilities")

pasivos = ut.fila_a_array(df_balance, fila+1)
pasivos = [float(x) for x in pasivos]


fila=ut.buscar_fila(df_balance, "Total Current Liabilities")
pasivos_cp=ut.fila_a_array (df_balance, fila+1)
pasivos_cp=ut.limpiar_a_numeros(pasivos_cp)


pasivos_lp= [
    (a if isinstance(a, (int, float)) else 0) -
    (b if isinstance(b, (int, float)) else 0)
    for a, b in zip(pasivos, pasivos_cp) ]




ut.graficar_tres_lineas(pasivos, pasivos_cp, pasivos_lp,"red","#FF8000","#FF5C5C", eje_x=años, etiquetas=("total","c/p","l/p"), eje_y="Pasivos")

ut.crear_tabla_4_listas(años, pasivos_cp, pasivos_lp, pasivos, "Pasivos cp","Pasivo lp","Pasivo total")




pasivos_cp_porcentaje= rt.dividir_y_convertir_a_porcentaje(pasivos_cp,pasivos)
pasivos_lp_porcentaje= rt.dividir_y_convertir_a_porcentaje(pasivos_lp,pasivos)  
limite= [100] * 10
ut.graficar_tres_lineas(pasivos_cp_porcentaje, pasivos_lp_porcentaje, limite,"#FF8000","#FF5C5C","red", eje_x=años, etiquetas=("c/p","l/p","total"), eje_y="Pasivos %")




#***************************************************** Ratio de deuda **********************************************
años=ex.años(df_resultado)

h3_especial("Ratio de pasivo/activo")

activos=ex.activos(df_balance)
pasivos=ex.pasivos(df_balance)


ratio_deuda=ut.divide_listas(pasivos,activos)

ratio_deuda = [round(x*100,2) for x in ratio_deuda]


lim_sup = 10*[75]
lim_inf=10*[50]


ut.graficar_tres_lineas(ratio_deuda, lim_sup, lim_inf,"#0000CD","coral","lightgreen", eje_x=años, etiquetas=("pasivos/activos","limite_sano","limite_no aceptable"), eje_y="Ratio de deuda")

ut.mostrar_dos_arrays_texto(años, ratio_deuda ,"ratio pasivo / activo %")


