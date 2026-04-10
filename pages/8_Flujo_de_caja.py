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
    '<h1 style="text-align: center; color: #1b3865; margin-top: -40px;">Flujo de caja</h1>',
    unsafe_allow_html=True
)




años=df_resultado.columns.tolist()
años=ut.procesar_array (años)

#******************************************************CFO **********************************************

h3_especial("CFO,FCF y Beneficio Neto")

fco= ex.FCO(df_flujo)
fcf=ex.FCF(años,df_flujo,0)
beneficio= ex.beneficio(df_resultado)





listas=[fco,fcf,beneficio]
colores=["#C980BF", "#8684F5", "#EBB44E"]
etiquetas=["FCO","FCF","Beneficio neto"]

ut.graficar_n_barras(listas, 
                     colores=colores,
                     eje_x=años,
                     etiquetas=etiquetas,
                     eje_y="Valores")


ut.crear_tabla_4_listas (años, fco, fcf, beneficio, "FCO","FCF","Beneficio neto")





#******************************************************Capex, capex mantenimiento y Depreciacion **********************************************

h3_especial("Capex")

capex= ex.capex(df_flujo)
capex_mantenimiento=ex.capex_mantenimiento(df_flujo)
depreciacion= ex.depreciacion(df_flujo)

capex = [round (float(-x),2) for x in capex]
capex_mantenimiento = [round (float(-x),2) for x in capex_mantenimiento]



listas=[capex,capex_mantenimiento,depreciacion]
colores=["#D1B65F", "#5F8594", "#B48966"]
etiquetas=["Capex","Capex mantenimientno","Depreciacion"]

ut.graficar_n_barras(listas, 
                     colores=colores,
                     eje_x=años,
                     etiquetas=etiquetas,
                     eje_y="Valores")







#ut.graficar_barras_y_linea(capex, capex_mantenimiento, depreciacion, "#D1B65F", "#5F8594", "#B48966",
#                           eje_x=años, etiquetas=("capex","capex_mantenimiento","depreciacion"),eje_y_izq="Millones",
#                           eje_y_der="Milloness")


st.markdown(
    '''
    <div style="text-align: center; font-size: 18px;">
        <b></b> <br>
        <span style="font-size:14px;">(capex mantenimiento tomado como promedio depreciación/capex 10 años)</span>
    </div>
    ''',
    unsafe_allow_html=True
)
ut.crear_tabla_4_listas (años, capex,  depreciacion, capex_mantenimiento,"capex","depreciacion","capex mantenimiento")





#************************************************************NET CASH **********************************
h3_especial("Net cash")

fco=fco
cash_from_inversion=ex.cash_inversion(df_flujo)
cash_from_finacing=ex.cash_financing(df_flujo)

resultado=ut.suma_listas(fco,cash_from_inversion)
net_cash=ut.suma_listas(resultado,cash_from_finacing)

cash_from_inversion2 = [round (float(-x),2) for x in cash_from_inversion]
cash_from_finacing2 = [round (float(-x),2) for x in cash_from_finacing]

ut.graficar_barras_apiladas_y_linea(fco, cash_from_inversion2, cash_from_finacing2, net_cash,
                                    "#F3B890","#318DB8", "#89A064", 'blue',
                                    eje_x=años,
                                    etiquetas=("fco","cash from inversion","cash from financing","net cash"),
                                    eje_y_izq="Millones",
                                    eje_y_der="Millones")



ut.crear_tabla_5_listas (años, fco,  cash_from_inversion, cash_from_finacing,net_cash,"FCO","cash from inversion","cash from financing","Net Cash")
ut.graficar_una_linea (net_cash, 'olive', eje_x=años, etiqueta="Net Cash", eje_y="Net Cash")

#************************************************************NET CASH **********************************
h3_especial("evolucion de cash")

net_cash=ut.suma_listas(resultado,cash_from_finacing)
caja=ex.caja(df_balance)
caja_inicial=ut.resta_listas(caja,net_cash)

ut.graficar_barras_y_linea(caja_inicial, caja, net_cash, "#B0E7C7", "#69B97B", "#4EB4E4",
                           eje_x=años, etiquetas=("caja_inicial","caja","net_cash"),eje_y_izq="Millones",
                           eje_y_der="Milloness")

ut.crear_tabla_4_listas (años, caja_inicial,  net_cash, caja,"Caja inicial","Net_cash","Caja final")







#ut.mostrar_dos_arrays(años, inversion)


#******************************************************Calculo Asignacion del Cash flow **********************************************



adquisiciones=ex.adquisiciones(df_flujo)
capex = [round (float(-x),2) for x in capex]
inversion=ex.inversiones_varias(df_flujo)
cash_from_inversion=cash_from_inversion









recompras=ex.recompras(df_flujo)
dividendos=ex.dividendos(df_flujo)
pago_deuda=ex.pago_deuda(df_flujo)
financiacion_varia=ex.financiacion(df_flujo)
cash_from_finacing=cash_from_finacing






#******************************************************Adquisiciones **********************************************

h3_especial("Adquisiciones")
adquisiciones=adquisiciones
ut.grafica_columnas(años,adquisiciones,"Años","Adquisiciones","#351D03")

#******************************************************Inversion **********************************************

h3_especial("Inversion")
inversion=inversion
ut.grafica_columnas(años,inversion,"Años","Inversiones","#C46807")

#******************************************************recompras **********************************************

h3_especial("Recompras")
recompras=recompras
ut.grafica_columnas(años,recompras,"Años","Recompras","#5D9414")

#******************************************************Dividendos **********************************************

h3_especial("Dividendos")
dividendos=dividendos
ut.grafica_columnas(años, dividendos, "Años","Dividendos","#E76C1A")





#******************************************************Financiacion varia **********************************************


h3_especial("Financiacion varia")



financiacion_varia=financiacion_varia
ut.grafica_columnas(años, financiacion_varia[0], "Años","Financiacion varia","#476096")

#******************************************************Pago deuda **********************************************


h3_especial("Pago deuda")



pago_deuda=pago_deuda
ut.grafica_columnas(años, pago_deuda, "Años","Financiacion varia","#EE5A6E")









#******************************************************Net cashs **********************************************


h3_especial("net cash")
net_cash=net_cash
ut.grafica_columnas(años, net_cash, "Años","net cash","#6DC065")







#******************************************************Deuda VS CFO **********************************************
h3_especial("Deuda VS FCO")

fco=fco
deuda_cp=ex.deuda_cp(df_balance)
deuda_lp=ex.deuda_lp(df_balance)
deuda=ut.suma_listas(deuda_cp,deuda_lp)


ut.graficar_2barras(deuda, fco, "#F33F3F", "#52815D",
                      eje_x= años,
                     etiquetas= ("Deuda", "FCO"), eje_y="Millones")


ratio_deuda_fco=ut.divide_listas(deuda,fco)

ut.mostrar_dos_arrays_texto (años, ratio_deuda_fco,"ratio fco/deuda")





#******************************************************Asignacion de cash-flow**********************************************
#listas=[deuda, fco, capex,adquisiciones,inversion,recompras,dividendos,pago_deuda,financiacion_varia ]   
#etiquetas= ["deuda","FCO","Capex","Adquisiciones","Inversion","Recompra","Dividendos","Pago_deuda","financiacion_varia"]
h3_especial("Asignacion del cash flow")

listas=[fco,capex,adquisiciones,inversion,recompras,dividendos,financiacion_varia[0],pago_deuda,net_cash ]   
etiquetas= ["FCO","Capex","Aquisiciones","Inversion","Recompras","Dividendos","financiacion_varia","pago_deuda","net_cash"]
colores=["#52815D","#D1B65F","#351D03","#C46807","#5D9414","#E76C1A","#476096","#EC4D42","#8DF16E"]


ut.mostrar_dos_arrays_texto(años, fco ,"Flujo de caja")

ut.crear_tabla_5_listas (años, capex,  adquisiciones, inversion,cash_from_inversion,"Capex","Adquisiciones","Inversiones","cash_from_inversion")
ut.crear_tabla_6_listas (años, recompras,  dividendos, pago_deuda,financiacion_varia[0],cash_from_finacing,"recompras","dividendos","pago_deuda","financiacion varia","cash_from_financing")




ut.graficar_n_barras(listas, 
                     colores=colores,
                     eje_x=años,
                     etiquetas=etiquetas,
                     eje_y="Valores")

st.write("")