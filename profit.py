import streamlit as st
import pandas as pd
import altair as alt

# Título de la aplicación
st.title('Sistema de Profit Mejorado')

# Entradas del usuario
st.sidebar.header('Entradas del Usuario')
num_rows = st.sidebar.number_input('Número de filas', min_value=1, value=3)

data = {'Fecha': [], 'Concepto': [], 'Cantidad': []}

for i in range(num_rows):
    st.sidebar.subheader(f'Fila {i+1}')
    fecha = st.sidebar.date_input(f'Fecha {i+1}')
    concepto = st.sidebar.selectbox(f'Concepto {i+1}', ['Ingresos', 'Gastos'])
    cantidad = st.sidebar.number_input(f'Cantidad {i+1}', min_value=0)
    data['Fecha'].append(fecha)
    data['Concepto'].append(concepto)
    data['Cantidad'].append(cantidad)

df = pd.DataFrame(data)
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Cálculo del profit total
ingresos = df[df['Concepto'] == 'Ingresos']['Cantidad'].sum()
gastos = df[df['Concepto'] == 'Gastos']['Cantidad'].sum()
profit = ingresos - gastos

# Mostrar el DataFrame
st.subheader('Datos de Ingresos y Gastos')
st.write(df)

# Gráfico de barras de Ingresos y Gastos
bar_chart = alt.Chart(df).mark_bar().encode(
    x='Concepto',
    y='sum(Cantidad)',
    color='Concepto'
).properties(
    title='Ingresos vs Gastos'
)

# Gráfico de línea de la evolución de Ingresos y Gastos
line_chart = alt.Chart(df).mark_line().encode(
    x='Fecha',
    y='Cantidad',
    color='Concepto',
    strokeDash='Concepto'
).properties(
    title='Evolución de Ingresos y Gastos a lo largo del tiempo'
)

# Mostrar los gráficos
st.altair_chart(bar_chart, use_container_width=True)
st.altair_chart(line_chart, use_container_width=True)

# Mostrar el profit
st.subheader('Profit Total')
st.write(f'Ingresos Totales: ${ingresos}')
st.write(f'Gastos Totales: ${gastos}')
st.write(f'Profit: ${profit}')
st.write(f'Porcentaje de Profit respecto a los Ingresos: {profit/ingresos:.2%}' if ingresos > 0 else 'N/A')

# Gráfico de barras del Profit
profit_df = pd.DataFrame({
    'Concepto': ['Ingresos', 'Gastos', 'Profit'],
    'Cantidad': [ingresos, gastos, profit]
})

profit_chart = alt.Chart(profit_df).mark_bar().encode(
    x='Concepto',
    y='Cantidad',
    color='Concepto'
).properties(
    title='Profit'
)

# Mostrar el gráfico de profit
st.altair_chart(profit_chart, use_container_width=True)
