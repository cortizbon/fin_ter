import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from io import BytesIO
from plotly import graph_objects as go

DIC_COLORES = {'verde':["#009966"],
               'ro_am_na':["#FFE9C5", "#F7B261","#D8841C", "#dd722a","#C24C31", "#BC3B26"],
               'az_verd': ["#CBECEF", "#81D3CD", "#0FB7B3", "#009999"],
               'ax_viol': ["#D9D9ED", "#2F399B", "#1A1F63", "#262947"],
               'ofiscal': ["#F9F9F9", "#2635bf"]}

custom_palette = ["#2F399B", "#dd722a", "#F7B261", "#009999", "#81D3CD", "#CBECEF", "#D9D9ED"]
st.set_page_config(layout='wide')

st.title("Finanzas territoriales")

ing = pd.read_csv('ingresos_limpios.csv')
ing['AFORO_DEFINITIVO'] = (ing['AFORO_DEFINITIVO'] / 1_000_000).round(1)
rubros = ing['RUBRO'].unique().tolist()

custom_map = dict(zip(rubros, custom_palette))
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

tab2 = filtro2.groupby(['Año','col_2'])['APROPIACION_DEFINITIVA'].sum().reset_index()

fig1 = px.area(tab, 
               x='Año',
               y='AFORO_DEFINITIVO',
               color='RUBRO',
              title='Ingresos',
              color_discrete_map=custom_map)
fig2 = px.area(tab2, 
               x='Año',
               y='APROPIACION_DEFINITIVA',
               color='col_2',
              title='Gastos',
              color_discrete_map=custom_map)

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

fig1 = px.pie(tab, names='RUBRO', values='AFORO_DEFINITIVO', title='Ingresos')
fig2 = px.pie(tab2, names='col_2', values='APROPIACION_DEFINITIVA', title='Gastos')

# Create Subplots
fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

# Add traces with color specification
fig.add_trace(go.Pie(labels=tab['RUBRO'], 
                     values=tab['AFORO_DEFINITIVO'], 
                     marker=dict(colors=custom_palette)), 
              row=1, col=1)

fig.add_trace(go.Pie(labels=tab2['col_2'], 
                     values=tab2['APROPIACION_DEFINITIVA'], 
                     marker=dict(colors=custom_palette)), 
              row=1, col=2)

# Update layout
fig.update_layout(title_text=ent, showlegend=False)

# Display in Streamlit
st.plotly_chart(fig)

# binary_output = BytesIO()
# ing.to_excel(binary_output, index=False)
# st.download_button(label = 'Descargar ingresos',
#                     data = binary_output.getvalue(),
#                     file_name = 'ingresos.xlsx')

# binary_output = BytesIO()
# gas.to_excel(binary_output, index=False)
# st.download_button(label = 'Descargar gastos',
#                     data = binary_output.getvalue(),
#                     file_name = 'gastos.xlsx')