import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from io import BytesIO

st.set_page_config(layout='wide')

st.title("Finanzas territoriales")

ing = pd.read_csv('ingresos_limpios.csv')
ing['AFORO_DEFINITIVO'] = (ing['AFORO_DEFINITIVO'] / 1_000_000).round(1)
gas = pd.read_csv('gastos_limpios.csv')
gas['APROPIACION_DEFINITIVA'] = (gas['APROPIACION_DEFINITIVA'] / 1_000_000).round(1)

ents = ing['NOMBRE_ENTIDAD'].sort_values().unique().tolist() 
years = ing['Año'].sort_values().unique().tolist()

# seleccionar entidades únicas

ent = st.selectbox("Seleccione entidad", ents)

# histórico

filtro = ing[ing['NOMBRE_ENTIDAD'] == ent]

tab = filtro.groupby(['Año','RUBRO'])['AFORO_DEFINITIVO'].sum().reset_index()


filtro2 = gas[gas['NOMBRE_ENTIDAD'] == ent]

tab2 = filtro2.groupby(['Año','col_2'])['AFORO_DEFINITIVO'].sum().reset_index()

fig1 = px.area(tab, 
               x='Año',
               y='AFORO_DEFINITIVO',
               color='RUBRO',
              title='Ingresos')
fig2 = px.area(tab2, 
               x='Año',
               y='AFORO_DEFINITIVO',
               color='col_2',
              title='Gastos')

fig = make_subplots(rows=1, cols=2)

for trace in fig1.data:
    fig.add_trace(trace, row=1, col=1)

for trace in fig2.data:
    fig.add_trace(trace, row=1, col=2)

# Update layout (optional: remove legend)
fig.update_layout(title="Histórico", showlegend=False)


fig.update_layout(title_text=ent,
                  showlegend=False)

st.plotly_chart(fig)

# seleccionar año

year = st.select_slider("Seleccione el año", years)

tab = tab[tab['Año'] == year].drop(columns='Año')

tab2 = tab2[tab2['Año'] == year].drop(columns='Año')

# graficar en dos piebars los ingresos y los gastos

fig1 = px.pie(tab, 
              names='RUBRO',
              values='APROPIACION_DEFINITIVA',
              title='Ingresos')
fig2 = px.pie(tab2, 
              names='col_2',
              values='APROPIACION_DEFINITIVA',
              title='Gastos')

fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

fig.add_trace(fig1.data[0], row=1, col=1)
fig.add_trace(fig2.data[0], row=1, col=2)

fig.update_layout(title_text=ent,
                  showlegend=False)

st.plotly_chart(fig)

binary_output = BytesIO()
ing.to_excel(binary_output, index=False)
st.download_button(label = 'Descargar ingresos',
                    data = binary_output.getvalue(),
                    file_name = 'ingresos.xlsx')

binary_output = BytesIO()
gas.to_excel(binary_output, index=False)
st.download_button(label = 'Descargar gastos',
                    data = binary_output.getvalue(),
                    file_name = 'gastos.xlsx')