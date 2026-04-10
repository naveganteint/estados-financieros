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
    '<h1 style="text-align: center; color: #1b3865; margin-top: -40px;">Análisis de la Rentabilidad</h1>',
    unsafe_allow_html=True
)


años=df_resultado.columns.tolist()
años=ut.procesar_array (años)

fila=ut.buscar_fila(df_balance, "Total Assets")

activos = ut.fila_a_array(df_balance, fila+1)
activos = [float(x) for x in activos]




fila=ut.buscar_fila(df_balance, "Total Liabilities")

pasivos = ut.fila_a_array(df_balance, fila+1)
pasivos = [float(x) for x in pasivos]





patrimonio_neto=ut.restar_listas(activos, pasivos)
patrimonio_neto = [x * -1 for x in patrimonio_neto]


#ut.mostrar_dos_arrays(años, activos)
#ut.mostrar_dos_arrays(años, pasivos)
#ut.mostrar_dos_arrays(años, patrimonio_neto)




#------roe ------------------------------------

fila=ut.buscar_fila(df_resultado, "Net Income")
beneficio_neto=ut.fila_a_array (df_resultado,fila+1)
roe=rt.dividir_y_convertir_a_porcentaje(beneficio_neto, patrimonio_neto)

#------ roic -----------------------------------


fila=ut.buscar_fila(df_resultado, "Operating Profit")
beneficio_operativo=ut.fila_a_array (df_resultado,fila+1)

fila=ut.buscar_fila(df_resultado, "Pre-Tax Income")
pretax_income=ut.fila_a_array (df_resultado,11)
income_tax=ut.fila_a_array (df_resultado,12)

fila=ut.buscar_fila(df_resultado, "Income Tax")
tax_rate=rt.calculo_tasa(pretax_income,income_tax)
nopat=rt.calcular_nopat(beneficio_operativo, tax_rate)




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



long_debt=ex.long_debt(df_balance)

long_lease=ex.long_lease(df_balance)



suma_pn_deuda=rt.sumar_cinco_listas(current_debt, current_lease, long_debt, long_lease, patrimonio_neto)
roic=rt.dividir_listas(nopat,suma_pn_deuda)
roic = [round(x * (100),2) for x in roic]


#***************************************ROA ***************************************


roa=rt.dividir_listas(beneficio_neto,activos)
roa = [round(x * (100),2) for x in roa]




#ut.mostrar_dos_arrays(años, long_lease)
#ut.mostrar_dos_arrays(años, long_debt)






h3_especial ("ROE - ROIC - ROA")




ut.graficar_tres_lineas(roe, roic, roa,'brown', '#F5B427','blue', eje_x=años, etiquetas=("roe", "roic" , "roa"), eje_y="ratios rentabilidad %")



st.write("")
st.markdown(
    '<div style="text-align: center; font-size: 18px;"><b>ROE </b>(Beneficio neto / Patrimonio)</div>',
    unsafe_allow_html=True)
ut.mostrar_dos_arrays(años, roe)
st.markdown(
    '<div style="text-align: center; font-size: 18px;"><b>ROIC </b>(Nopat/(deudas+patrimonio neto))</div>',
    unsafe_allow_html=True)

ut.mostrar_dos_arrays(años, roic)
st.markdown(
    '<div style="text-align: center; font-size: 18px;"><b>ROA </b>(Beneficio neto / Activos)</div>',
    unsafe_allow_html=True)

ut.mostrar_dos_arrays(años, roa)

#*************************************************FCF ******************************
h3_especial ("FCF (Free cash flow)")


fila=ut.buscar_fila(df_flujo, "Cash From Operations")
flujo_operativo=ut.fila_a_array (df_flujo,fila+1)


st.markdown(
    '<div style="text-align: center; font-size: 16px;"><br><b>Flujo operativo</b></div>',
    unsafe_allow_html=True)

ut.mostrar_dos_arrays(años, flujo_operativo)


#··························capex promedio******************************


fila=ut.buscar_fila(df_flujo, "Depreciation & Amortization")
depreciacion=ut.fila_a_array (df_flujo,fila+1)

st.markdown(
    '<div style="text-align: center; font-size: 16px;"><b>Depreciacion</b></div>',
    unsafe_allow_html=True)
ut.mostrar_dos_arrays(años, depreciacion)




fila=ut.buscar_fila(df_flujo, "Property, Plant, & Equipment")
capex=ut.fila_a_array (df_flujo,fila+1)
st.markdown(
    '<div style="text-align: center; font-size: 16px;"><b>Capex total</b></div>',
    unsafe_allow_html=True)
ut.mostrar_dos_arrays(años, capex)


st.markdown(
    '<div style="text-align: center; font-size: 16px;"><b>Ratio depreciacion / capex </b></div>',
    unsafe_allow_html=True)

lista_promedio=rt.dividir_listas(depreciacion, capex)
ut.mostrar_dos_arrays(años, lista_promedio)

promedio_capex=rt.promedio(lista_promedio)


capex_mantenimiento = [-promedio_capex * x for x in capex]


capex_mantenimiento= [round(x, 2) if isinstance(x, (int, float)) else x for x in capex_mantenimiento]

st.markdown(
    f'<div style="text-align: center; font-size: 16px;"><b>Capex mantenimiento calculado</b> (ratio medio <b>{round(promedio_capex,2)}</b>) </div>',
    unsafe_allow_html=True)
ut.mostrar_dos_arrays(años, capex_mantenimiento)


st.markdown(
    '''
    <div style="text-align: center; font-size: 18px;">
        <b>FCF</b> (Flujo de caja operativo − CAPEX mantenimiento)<br>
        <span style="font-size:14px;">(capex mantenimiento tomado como promedio depreciación/capex 10 años)</span>
    </div>
    ''',
    unsafe_allow_html=True
)



FCF= [
    round((a if isinstance(a, (int, float)) else 0) +
    (b if isinstance(b, (int, float)) else 0),2)
    for a, b in zip(flujo_operativo, capex_mantenimiento)
]






ut.grafica_columnas(años,FCF,"Años","FCF (m)","#76F7A7")
ut.mostrar_dos_arrays(años, FCF)

ut.graficar_tres_lineas(flujo_operativo, capex_mantenimiento, FCF,"#134113", "#803A12","#906CE4", eje_x=años, etiquetas=("CFO", "Capex mantenimiento" , "FCF"), eje_y="Datos FCF")

#------------------------- FCF margin --------------------------------------
fila=ut.buscar_fila(df_resultado, "Revenue")
ventas = ut.fila_a_array(df_resultado, fila+1)


marginFCF = [
    round(100*(a if isinstance(a, (int, float)) else 0) /
    (b if isinstance(b, (int, float)) else 0),2)
    for a, b in zip(FCF, ventas)
]



st.markdown(
    '<div style="text-align: center; font-size: 16px;"><br><b>Margin FCF</b></div>',
    unsafe_allow_html=True)
#ut.mostrar_dos_arrays(años, ventas)
ut.graficar_una_linea (marginFCF, 'violet', eje_x=None, etiqueta="Margin FCF", eje_y="margin FCF/Ventas %")
ut.mostrar_dos_arrays(años, marginFCF)




#****************************************Dividendos *****************************************************************
h3_especial ("Dividendos")

st.markdown(
    '<div style="text-align: center; font-size: 16px;"><br></div>',
    unsafe_allow_html=True)




#ut.mostrar_dos_arrays(años, beneficio_neto)



fila=ut.buscar_fila(df_flujo, "Cash Paid for Dividends")
Dividendos=ut.fila_a_array (df_flujo,fila+1)
Dividendos = [x * -1 if isinstance(x, (int, float)) else x for x in Dividendos]
#ut.mostrar_dos_arrays(años, Dividendos)



fila=ut.buscar_fila(df_resultado, "Shares (Diluted)")
num_acciones=ut.fila_a_array (df_resultado,fila+1)
num_acciones_num=rt.convertir_a_numero(num_acciones)
#ut.mostrar_dos_arrays(años, num_acciones_num)


#ut.mostrar_dos_arrays(años, FCF)



beneficio_accion=rt.dividir_listas(beneficio_neto, num_acciones_num)
beneficio_accion= [round(x,2) if isinstance(x, (int, float)) else x for x in beneficio_accion]
dividendo_accion=rt.dividir_listas(Dividendos , num_acciones_num)
dividendo_accion = [round(x,2) if isinstance(x, (int, float)) else x for x in dividendo_accion]
FCF_accion=rt.dividir_listas(FCF , num_acciones_num)
FCF_accion= [round(x,2) if isinstance(x, (int, float)) else x for x in FCF_accion]

ut.graficar_tres_lineas(beneficio_accion, dividendo_accion, FCF_accion,'brown', 'orange','violet', eje_x=años, etiquetas=("Beneficio/a", "Dividendo/a" , "FCF/a"), eje_y="Solvencia Dividendos")

ut.mostrar_cuatro_arrays(años, beneficio_accion, dividendo_accion, FCF_accion)

st.markdown(
    '<div style="text-align: center; font-size: 16px;"><br><b>PAY OUT</b></div>',
    unsafe_allow_html=True)


#****************************************PAY OUT*****************************************************************







pay_out=rt.dividir_y_convertir_a_porcentaje(dividendo_accion,beneficio_accion )
pay_out= [round(x,2) if isinstance(x, (int, float)) else x for x in pay_out]
pay_out2= [x if isinstance(x, (int, float)) and x >= 0 else 0 for x in pay_out]


pay_out_fcf=rt.dividir_y_convertir_a_porcentaje(dividendo_accion,FCF_accion )
pay_out_fcf= [round(x,2) if isinstance(x, (int, float)) else x for x in pay_out_fcf]
pay_out_fcf2 = [x if isinstance(x, (int, float)) and x >= 0 else 0 for x in pay_out_fcf]

limite= [90] * 10





ut.graficar_tres_lineas(pay_out2, pay_out_fcf2, limite,"brown","violet","red", eje_x=años, etiquetas=("pay_out","pay_out_fcf","limite"), eje_y="Pay out sobre eps y fcf %")

ut.crear_tabla_4_listas(años, pay_out, pay_out_fcf, limite, "Pay-out","Pay-put_fcf","limite aceptable")

