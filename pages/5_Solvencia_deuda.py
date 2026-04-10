import streamlit as st
from styles import aplicar_estilos,h3_especial,h2_especial
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
    '<h1 style="text-align: center; color: #1b3865; margin-top: -40px;">Solvencia de la deuda</h1>',
    unsafe_allow_html=True
)




años=df_resultado.columns.tolist()
años=ut.procesar_array (años)

#******************************************************Pasivo **********************************************

#h3_especial("Pasivo balance")

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




#ut.graficar_tres_lineas(pasivos, pasivos_cp, pasivos_lp,"red","#FF8000","#FF5C5C", eje_x=años, etiquetas=("total","c/p","l/p"), eje_y="Pasivos")


#ut.mostrar_dos_arrays(años, pasivos)
#ut.mostrar_dos_arrays(años, pasivos_cp)
# ******************************************extrae años *********************************



pasivos_cp_porcentaje= rt.dividir_y_convertir_a_porcentaje(pasivos_cp,pasivos)
pasivos_lp_porcentaje= rt.dividir_y_convertir_a_porcentaje(pasivos_lp,pasivos)  
limite= [100] * 10
#ut.graficar_tres_lineas(pasivos_cp_porcentaje, pasivos_lp_porcentaje, limite,"#FF8000","#FF5C5C","red", eje_x=años, etiquetas=("c/p","l/p","total"), eje_y="Pasivos %")







#****************************************************** Deuda neta  **********************************************


h3_especial("deuda neta")
        # calculo deuda

fila=ut.buscar_fila(df_balance, "Short-Term Debt")
try:
    current_debt=ut.fila_a_array (df_balance,fila+1)
except :
    current_debt= 10* [0]

current_debt=ut.limpiar_a_numeros(current_debt)



fila=ut.buscar_fila(df_balance, "Capital Leases (Current)")
try:
    current_lease=ut.fila_a_array (df_balance,fila+1)
except :   
    current_lease= 10* [0]

current_lease=ut.limpiar_a_numeros(current_lease)


fila=ut.buscar_fila(df_balance, "Long-Term Debt")
long_debt=ut.fila_a_array (df_balance,fila+1)
long_debt=ut.limpiar_a_numeros(long_debt)




long_lease=ex.long_lease(df_balance)



fila=ut.buscar_fila(df_balance, "Cash & Equivalents")
caja=ut.fila_a_array (df_balance,fila+1)
caja=ut.limpiar_a_numeros(caja)

cero = [0] * 10

#ut.mostrar_dos_arrays(años, current_debt)
#ut.mostrar_dos_arrays(años, current_lease)
#ut.mostrar_dos_arrays(años, long_debt)
#ut.mostrar_dos_arrays(años, long_lease)



deuda =rt.sumar_cinco_listas(current_debt, current_lease, long_debt, long_lease, cero)
deuda_neta = [
    (a if isinstance(a, (int, float)) else 0) -
    (b if isinstance(b, (int, float)) else 0)
    for a, b in zip(deuda, caja) ]



ut.graficar_tres_lineas(deuda, caja, deuda_neta,"pink","lightgreen","red", eje_x=años, etiquetas=("Deuda","Caja","Deuda_neta"), eje_y="Deuda neta")

ut.crear_tabla_4_listas(años, deuda, caja, deuda_neta, "Deuda","Caja","Deuda neta")

st.write("")

#****************************************************************************************************
#****************************************************** Capacidad de pago ***************************
#****************************************************************************************************
h2_especial("Capacidad de Pago")

#*******************************************RAtio de cobertura************

h3_especial("Ratio de cobertura( ebit/ intereses)")

fila=ut.buscar_fila(df_resultado, "Net Interest Income")

try:
    intereses=ut.fila_a_array (df_resultado,fila+1)
except :   
    intereses= 10* [0]

intereses=ut.limpiar_a_numeros(intereses)
intereses= [round(-x,2) if isinstance(x, (int, float)) else x for x in intereses]



fila=ut.buscar_fila(df_resultado, "Operating Profit")

try:
    ebit=ut.fila_a_array (df_resultado,fila+1)
except :   
    ebit= 10* [0]

ebit=ut.limpiar_a_numeros(ebit)

lim_inf=10*[2]
lim_sup=10*[5]
cobertura= rt.dividir_y_convertir_a_porcentaje(ebit,intereses)
cobertura= [round(x/100,2) if isinstance(x, (int, float)) else x for x in cobertura]


ut.graficar_tres_lineas(cobertura, lim_sup, lim_inf,"brown","lightgreen","coral", eje_x=años, etiquetas=("ratio cobertura","limite_sano","limite_no aceptable"), eje_y="Ratio cobertura")

#ut.mostrar_dos_arrays(años, ebit)
#ut.mostrar_dos_arrays(años, intereses)
#ut.mostrar_dos_arrays(años, cobertura)

ut.crear_tabla_4_listas(años, ebit, intereses, cobertura, "Ebit","Intereses","ratio cobertura")

st.write("")


#*******************************************Debt service coverage ratio************

h3_especial("Debt service coverage ratio")

flujo = ex.FCO(df_flujo)
deuda_cp=ex.deuda_cp(df_balance)
denominador=ut.suma_listas(intereses,deuda_cp)

DSCR=ut.divide_listas(flujo,denominador)



ut.graficar_barras_y_linea(flujo, denominador, DSCR, "#C0CEDF", "#CA9FC1", "#2E88D1",
                           eje_x=años, etiquetas=("CFO","int+deuda_cp","DSCR"),eje_y_izq="Millones",
                           eje_y_der="Ratio")
ut.crear_tabla_4_listas(años, flujo, denominador, DSCR, "CFO","Intereses+deuda_cp","DSCR")

ut.mostrar_dos_arrays(años, deuda_cp)

st.write("")

#****************************************************************************************************
#****************************************************** Nivel de endeudamiento **********************
#****************************************************************************************************


#****************************************************** solvencia deuda neta  **********************************************


h2_especial("Nivel de endeudamiento")
h3_especial("Solvencia deuda neta / ebitda (nivel de endeudamiento)")


fila=ut.buscar_fila(df_flujo, "Depreciation & Amortization")
depreciacion=ut.fila_a_array (df_flujo,fila+1)


#ut.mostrar_dos_arrays(años, depreciacion)

fila=ut.buscar_fila(df_resultado, "Operating Profit")
beneficio_operativo=ut.fila_a_array (df_resultado,fila+1)


ebitda = [
    (a if isinstance(a, (int, float)) else 0) +
    (b if isinstance(b, (int, float)) else 0)
    for a, b in zip(beneficio_operativo, depreciacion) ]



ratio_deuda_ebitda= rt.dividir_y_convertir_a_porcentaje(deuda_neta,ebitda)
ratio_deuda_ebitda= [round(x/100,2) if isinstance(x, (int, float)) else x for x in ratio_deuda_ebitda]





ut.graficar_barras_y_linea(deuda_neta, ebitda, ratio_deuda_ebitda, "#FF6E4A", "#BDF2A4", "#2E88D1",
                           eje_x=años, etiquetas=("deuda neta","ebitda","ratio"),eje_y_izq="Millones",
                           eje_y_der="Ratio")

ut.crear_tabla_4_listas(años, deuda_neta, ebitda, ratio_deuda_ebitda, "Deuda_neta","Ebitda","ratio deuda neta/ebitda")
st.write("")

#ut.mostrar_dos_arrays(años, deuda_neta)
#ut.mostrar_dos_arrays(años, ebitda)
#ut.mostrar_dos_arrays(años, ratio_deuda_ebitda)

#****************************************************** solvencia deuda neta  patrimonio **********************************************

h3_especial("Solvencia deuda neta / patrimonio")
patrimonio = ex.patrimonio(df_balance)
ratio_deuda_patrimonio = ut.divide_listas(deuda_neta,patrimonio)


ut.graficar_barras_y_linea(deuda_neta, patrimonio, ratio_deuda_patrimonio, "#FF6E4A", "#AB8868", "#2E88D1",
                           eje_x=años, etiquetas=("deuda neta","patrimonio","ratio"),eje_y_izq="Millones",
                           eje_y_der="Ratio")


ut.crear_tabla_4_listas(años, deuda_neta, patrimonio, ratio_deuda_patrimonio, "Deuda_neta","Patrimonio","ratio deuda neta/patrimonio")
st.write("")



#****************************************************************************************************
#****************************************************** Estructura de la deuda **********************
#****************************************************************************************************

h2_especial("Estructura y calidad de la deuda")
#****************************************************** Calidad de la deuda (estructura temporal) **********************************************
h3_especial(" Estructura temporal deuda cp/lp (presion temporal)")


deuda_cp=deuda_cp
deuda_lp=ex.deuda_lp(df_balance)
deuda=ut.suma_listas(deuda_cp,deuda_lp)

estructura_deuda= ut.divide_listas(deuda_cp,deuda_lp)




ut.graficar_barras_apiladas_y_linea(deuda, deuda_lp, deuda_cp, estructura_deuda,
                                    "#967B8A","#FD4E37", "#FF9980", 'blue',
                                    eje_x=años,
                                    etiquetas=("Deuda total","deuda_lp","deuda_cp","ratio (cp/lp)"),
                                    eje_y_izq="Valores",
                                    eje_y_der="Ratio")




ut.crear_tabla_5_listas(años, deuda_cp, deuda_lp, deuda,estructura_deuda, "Deuda_cp","Deuda_lp","Deuda total","Ratio estructura_deuda")




lim_sup= 10 * [1]
lim_inf= 10 * [0.2]

ut.graficar_tres_lineas(estructura_deuda, lim_sup, lim_inf,"#8B0000","coral","lightgreen", eje_x=años, etiquetas=("estructura temporal deuda","limite_no aceptable","limite_sano"), eje_y="calidad temporal deuda")

ratio_lp_total=ut.divide_listas(deuda_lp,deuda)
lim_sup= 10 * [0.8]
lim_inf= 10 * [0.6]


ut.graficar_tres_lineas(ratio_lp_total, lim_inf, lim_sup,"#F14848","coral","lightgreen", eje_x=años, etiquetas=("ratio deuda lp","limite_no aceptable","limite_sano"), eje_y="calidad temporal deuda lp")




#****************************************************** Coste de la deuda **********************************************
h3_especial(" Coste de la deuda")





try:
    coste_deuda= [
        round((a if isinstance(a, (int, float)) else 0) /
        (b if isinstance(b, (int, float)) else 0),4)
        for a, b in zip(intereses, deuda)
    ]
except:
    coste_deuda=10*[1]

coste_deuda = [round(100*x,2) if isinstance(x, (int, float)) else x for x in coste_deuda]

lim_sup= 10 * [6]
lim_inf= 10 * [4]
ut.graficar_tres_lineas(coste_deuda, lim_sup, lim_inf,"#3B3C42","coral","lightgreen", eje_x=años, etiquetas=("tipo interes medio deuda %","limite con riesgo","limite_sano"), eje_y="Coste de la deuda")

ut.crear_tabla_4_listas(años, intereses, deuda, coste_deuda, "Intereses","Deuda","Coste deuda %")
st.write("")



#****************************************************************************************************
#****************************************************** Generacion de caja VS deuda******************
#****************************************************************************************************

h2_especial("Generacion caja Vs deuda")

#****************************************************** FCF / Deuda total **********************************************
h3_especial("Deuda total / FCF")


FCF=ex.FCF(años,df_flujo,0)
deuda=deuda

ratio_fcf_deuda= ut.divide_listas(deuda,FCF)
ut.graficar_barras_y_linea(deuda, FCF, ratio_fcf_deuda, "#FA6E6E", "#8684F5", "#2E88D1",
                           eje_x=años, etiquetas=("deuda","FCF","ratio"),eje_y_izq="Millones",
                           eje_y_der="Ratio")




ut.crear_tabla_4_listas(años, deuda, FCF, ratio_fcf_deuda, "FCF","Deuda","Ratio deuda/FCF")

lim_sup= 10 * [0.15]
lim_inf= 10 * [0.10]
ut.graficar_tres_lineas(ratio_fcf_deuda, lim_inf, lim_sup,"#2E88D1","coral","#4A8637", eje_x=años, etiquetas=("ratio fcf/deuda","limite con aceptable","limite_sano"), eje_y="Generacion de caja")


st.write("")

#****************************************************** Deuda cp / FCF**********************************************
h3_especial("Deuda total_cp / FCF")


FCF=FCF
deuda_cp=deuda_cp

ratio_fcf_deuda_cp= ut.divide_listas(deuda_cp,FCF)
ut.graficar_barras_y_linea(deuda_cp, FCF, ratio_fcf_deuda_cp, "#C98080", "#8684F5", "#5181A8",
                           eje_x=años, etiquetas=("deuda_cp","FCF","ratio"),eje_y_izq="Millones",
                           eje_y_der="Ratio")




ut.crear_tabla_4_listas(años, deuda_cp,FCF, ratio_fcf_deuda_cp, "Deuda_cp","FCF","Ratio deuda_cp/ FCF")

lim_sup= 10 * [0.7]
lim_inf= 10 * [0.5]
ut.graficar_tres_lineas(ratio_fcf_deuda_cp, lim_inf, lim_sup,"#2E88D1","coral","#4A8637", eje_x=años, etiquetas=("ratio fcf/deuda_cp","limite con aceptable","limite_sano"), eje_y="Generacion de caja")


st.write("")

#****************************************************** FCF / Deuda cp-caja neta **********************************************
h3_especial("  (Deuda total_cp - caja) / FCF")


FCF=FCF
deuda_cp_neta=ut.resta_listas(deuda_cp,caja)

ratio_fcf_deuda_cp_neta= ut.divide_listas(deuda_cp_neta,FCF)

ut.graficar_barras_y_linea(deuda_cp_neta, FCF, ratio_fcf_deuda_cp_neta, "#F58888", "#8684F5", "#5181A8",
                           eje_x=años, etiquetas=("deuda_cp_neta","FCF","ratio"),eje_y_izq="Millones",
                           eje_y_der="Ratio")




ut.crear_tabla_4_listas(años,  deuda_cp_neta,FCF, ratio_fcf_deuda_cp_neta, "Deuda_cp_neta","FCF","Ratio deuda_cp_neta/FCF")

#ut.mostrar_dos_arrays(años, deuda_cp)
#ut.mostrar_dos_arrays(años, caja)



lim_sup= 10 * [1]
lim_inf= 10 * [0.5]

ut.graficar_tres_lineas(ratio_fcf_deuda_cp_neta, lim_inf, lim_sup,"#2E88D1","coral","#4A8637", eje_x=años, etiquetas=("ratio fcf/deuda_cp_neta","limite con aceptable","limite_sano"), eje_y="Generacion de caja")




st.write("")


