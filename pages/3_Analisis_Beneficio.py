import streamlit as st
from styles import aplicar_estilos,h3_especial
import ratios as rt
import utils as ut
import pandas as pd
import extraccion as ex



st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)




aplicar_estilos()



st.markdown(
    '<h1 style="text-align: center; color: #1b3865; margin-top: -40px;">Análisis de Beneficios</h1>',
    unsafe_allow_html=True
)

# Comprobar que la hoja "resultado" está cargada
if "hojas" in st.session_state and "resultado" in st.session_state.hojas:
    df_resultado = st.session_state.hojas["resultado"]

   # st.table(df_resultado)


h3_especial("Ventas")


años=df_resultado.columns.tolist()
años=ut.procesar_array (años)

fila=ut.buscar_fila(df_resultado, "Revenue")

ventas = ut.fila_a_array(df_resultado, fila+1)

st.write("")


ut.grafica_columnas(años,ventas,"Años","Ventas (m)","#B5E1F2")


# Mostrar tablas de ventas ***********************************

ventas=ex.ventas(df_resultado)

ut.mostrar_dos_arrays_texto(años, ventas,"Ventas")

rt.mostrar_cagr_tabla(ventas,5)
st.write("")

#*********Beneficio neto *****************

h3_especial("Beneficio neto")

fila=ut.buscar_fila(df_resultado, "Net Income")
beneficio_neto=ut.fila_a_array (df_resultado,fila+1)


ut.grafica_columnas(años,beneficio_neto,"Años","Beneficio Neto (m)","#A1634C")



beneficio_neto=ex.beneficio(df_resultado)
ut.mostrar_dos_arrays_texto(años, beneficio_neto,"Beneficio neto")

cagr_beneficio_neto =rt.mostrar_cagr_tabla(beneficio_neto,10)


h3_especial("Márgenes")

fila=ut.buscar_fila(df_resultado, "Gross Profit")
beneficio_bruto=ut.fila_a_array (df_resultado,fila+1)
fila=ut.buscar_fila(df_resultado, "Operating Profit")
beneficio_operativo=ut.fila_a_array (df_resultado,fila+1)

margen_bruto=rt.dividir_y_convertir_a_porcentaje(beneficio_bruto,ventas)
margen_operativo=rt.dividir_y_convertir_a_porcentaje(beneficio_operativo,ventas)
margen_neto=rt.dividir_y_convertir_a_porcentaje(beneficio_neto,ventas)


ut.graficar_tres_lineas(margen_bruto, margen_operativo, margen_neto,'red', 'green','blue', eje_x=años, etiquetas=("margen bruto", "margen operativo" , "margen neto"), eje_y="Márgenes %")

ut.mostrar_cuatro_arrays(años, margen_bruto, margen_operativo, margen_neto)

#*********Beneficio por Accion *****************

h3_especial("Beneficio por accion (EPS)")

fila=ut.buscar_fila(df_resultado, "Shares (Diluted)")
num_acciones=ut.fila_a_array (df_resultado,fila+1)
num_acciones_num=rt.convertir_a_numero(num_acciones)


eps=rt.dividir_listas(beneficio_neto, num_acciones_num)



ut.grafica_columnas(años,eps,"Años","Beneficio por accion (Uds)","#EDB477")
eps = [round (float(x),2) for x in eps]
ut.mostrar_dos_arrays_texto(años, eps,"Beneficio por accion")


cagr_eps=rt.mostrar_cagr_tabla(eps,10)

cagr_beneficio_neto=ut.limpiar_porcentajes (cagr_beneficio_neto)
cagr_eps=ut.limpiar_porcentajes(cagr_eps)



resta_lista=ut.restar_listas(cagr_beneficio_neto, cagr_eps)



ut.dif_cagr(resta_lista)


