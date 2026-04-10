import streamlit as st
from styles import aplicar_estilos,h3_especial
import ratios as rt
import utils as ut
import extraccion as ex
import pandas as pd



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
    '<h1 style="text-align: center; color: #1b3865; margin-top: -40px;">Análisis liquidez</h1>',
    unsafe_allow_html=True)



años=ex.años(df_resultado)


#***************************************************** Current ratio **********************************************

h3_especial("current Ratio")

activo_cp=ex.activo_cp(df_balance)
pasivos_cp=ex.pasivos_cp(df_balance)

ratio_corrientes= rt.dividir_y_convertir_a_porcentaje(activo_cp,pasivos_cp)
ratio_corrientes= [round(x/100,2) if isinstance(x, (int, float)) else x for x in ratio_corrientes]

lim_sup = 10*[1.5]
lim_inf=10*[1]


ut.graficar_tres_lineas(ratio_corrientes, lim_sup, lim_inf,"olive","lightgreen","coral", eje_x=años, etiquetas=("ratio corrientes","limite_sano","limite_no aceptable"), eje_y="solvencia corrientes")
ut.mostrar_dos_arrays(años, ratio_corrientes)


#***************************************************** Test acido **********************************************

h3_especial("Test acido")

inventarios=ex.inventarios(df_balance)

arriba=ut.resta_listas(activo_cp,inventarios)

test_acido= rt.dividir_y_convertir_a_porcentaje(arriba,pasivos_cp)
test_acido= [round(x/100,2) if isinstance(x, (int, float)) else x for x in test_acido]

lim_inf=10*[0.8]

ut.graficar_tres_lineas(test_acido, lim_sup, lim_inf,"#9ACD32","lightgreen","coral", eje_x=años, etiquetas=("solvencia sin inventarios","limite_sano","limite_no aceptable"), eje_y="Test acido")

ut.mostrar_dos_arrays(años, test_acido)


#***************************************************** RAtio de caja **********************************************

h3_especial("Cash Ratio")

caja=ex.caja(df_balance)

ratio_caja= rt.dividir_y_convertir_a_porcentaje(caja,pasivos_cp)
ratio_caja= [round(x/100,2) if isinstance(x, (int, float)) else x for x in ratio_caja]

lim_sup = 10*[1.1]
lim_inf=10*[0.9]


ut.graficar_tres_lineas(ratio_caja, lim_sup, lim_inf,"green","lightgreen","coral", eje_x=años, etiquetas=("ratio caja","limite_sano","limite_no aceptable"), eje_y="Cash ratio")
ut.mostrar_dos_arrays(años, ratio_caja)


#***************************************************** RAtio de CFO **********************************************


h3_especial("Operating Cash Flow Ratio (Ratio de liquidez operativa)")

flujo_de_caja=ex.FCO(df_flujo)
liquidez_operativa= rt.dividir_y_convertir_a_porcentaje(flujo_de_caja,pasivos_cp)
liquidez_operativa= [round(x/100,2) if isinstance(x, (int, float)) else x for x in liquidez_operativa]

lim_sup = 10*[1.1]
lim_inf=10*[0.9]


ut.graficar_tres_lineas(liquidez_operativa, lim_sup, lim_inf,"brown","lightgreen","coral", eje_x=años, etiquetas=("FCO/pasivos","limite_sano","limite_no aceptable"), eje_y="Liquidez operativa")
ut.mostrar_dos_arrays(años, liquidez_operativa)

#***************************************************** Ratio de FCF **********************************************


h3_especial("FCF Ratio (Ratio de liquidez operativa ajustada FCF)")
fcf=ex.FCF(años,df_flujo,0)



liquidez_operativa_ajustada= rt.dividir_y_convertir_a_porcentaje(fcf,pasivos_cp)
liquidez_operativa_ajustada= [round(x/100,2) if isinstance(x, (int, float)) else x for x in liquidez_operativa_ajustada]

lim_sup = 10*[1.1]
lim_inf=10*[0.9]


ut.graficar_tres_lineas(liquidez_operativa_ajustada, lim_sup, lim_inf,"#8B4513","lightgreen","coral", eje_x=años, etiquetas=("FCF/pasivos","limite_sano","limite_no aceptable"), eje_y="Liquidez operativa ajustada")
ut.mostrar_dos_arrays(años, liquidez_operativa_ajustada)


#***************************************************** Debt covering ratio **********************************************


h3_especial("Debt covering ratio (ingresos operativos/pasivos_cp)")

ingresos_operativos=ex.ingresos_operativos(df_resultado)
covering= rt.dividir_y_convertir_a_porcentaje(ingresos_operativos,pasivos_cp)
covering= [round(x/100,2) if isinstance(x, (int, float)) else x for x in covering]

lim_sup = 10*[1.1]
lim_inf=10*[0.9]


ut.graficar_tres_lineas(covering, lim_sup, lim_inf,"#C71585","lightgreen","coral", eje_x=años, etiquetas=("FCO/pasivos","limite_sano","limite_no aceptable"), eje_y="Liquidez operativa")
ut.mostrar_dos_arrays(años, liquidez_operativa)