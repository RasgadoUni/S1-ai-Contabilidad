import streamlit as st
import pandas as pd

# Inicialización de variables en el estado de la sesión
if 'transacciones' not in st.session_state:
    st.session_state.transacciones = []

if 'cuentas' not in st.session_state:
    st.session_state.cuentas = {
        'Caja': 0,
        'Proveedores': 0,
        'Clientes': 0,
        'Papelería': 0,
        'Rentas Pagadas por Anticipo': 0,
        'Capital': 0,
        'Compras': 0,
        'Anticipo de Clientes': 0
    }

# Función para registrar transacciones
def registrar_transaccion(tipo, monto, descripcion):
    st.session_state.transacciones.append({
        'Tipo': tipo,
        'Descripción': descripcion,
        'Detalles': monto
    })
    actualizar_cuentas(tipo, monto)

# Función para actualizar las cuentas
def actualizar_cuentas(tipo, monto):
    if tipo == 'Asiento de apertura':
        st.session_state.cuentas['Capital'] += monto
        st.session_state.cuentas['Caja'] += monto
    elif tipo == 'Compra en efectivo':
        st.session_state.cuentas['Caja'] -= monto
        st.session_state.cuentas['Compras'] += monto
    elif tipo == 'Compra a crédito':
        st.session_state.cuentas['Proveedores'] += monto
        st.session_state.cuentas['Compras'] += monto
    elif tipo == 'Compra en efectivo y a crédito':
        efectivo = monto['Efectivo']
        credito = monto['Crédito']
        st.session_state.cuentas['Caja'] -= efectivo
        st.session_state.cuentas['Proveedores'] += credito
        st.session_state.cuentas['Compras'] += efectivo + credito
    elif tipo == 'Anticipo de clientes':
        st.session_state.cuentas['Caja'] += monto
        st.session_state.cuentas['Anticipo de Clientes'] += monto
    elif tipo == 'Compra de papelería':
        st.session_state.cuentas['Caja'] -= monto
        st.session_state.cuentas['Papelería'] += monto
    elif tipo == 'Pago de rentas pagadas por anticipado':
        st.session_state.cuentas['Caja'] -= monto
        st.session_state.cuentas['Rentas Pagadas por Anticipo'] += monto
    elif tipo == 'Añadir dinero a caja':
        st.session_state.cuentas['Caja'] += monto

# Configuración de la página
st.set_page_config(page_title="Sistema Contable", layout="wide", page_icon="💰")

# Título principal con estilo
st.markdown(
    """
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #326273;
        text-align: center;
        padding: 20px;
    }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    <div class="title">Sistema de Registro Contable</div>
    """,
    unsafe_allow_html=True
)

# Formulario de registro de transacciones
st.markdown("### 📝 Registrar Nueva Transacción")
with st.form(key="form_transaccion"):
    col1, col2 = st.columns(2)
    with col1:
        tipo_transaccion = st.selectbox(
            'Tipo de Transacción',
            ['Asiento de apertura', 'Compra en efectivo', 'Compra a crédito', 'Compra en efectivo y a crédito', 'Anticipo de clientes', 'Compra de papelería', 'Pago de rentas pagadas por anticipado', 'Añadir dinero a caja']
        )
    with col2:
        descripcion = st.text_input('Descripción de la transacción')

    if tipo_transaccion == 'Compra en efectivo y a crédito':
        col3, col4 = st.columns(2)
        with col3:
            efectivo = st.number_input('Monto en efectivo', min_value=0.0)
        with col4:
            credito = st.number_input('Monto a crédito', min_value=0.0)
        monto = {'Efectivo': efectivo, 'Crédito': credito}
    else:
        monto = st.number_input('Monto', min_value=0.0)

    if st.form_submit_button("Registrar Transacción"):
        registrar_transaccion(tipo_transaccion, monto, descripcion)
        st.success("Transacción registrada correctamente.")

# Mostrar transacciones registradas
st.markdown("### 📋 Transacciones Registradas")
if st.session_state.transacciones:
    st.dataframe(pd.DataFrame(st.session_state.transacciones), use_container_width=True)
else:
    st.info("No hay transacciones registradas.")

# Mostrar esquemas de mayor
st.markdown("### 📊 Esquemas de Mayor")
st.dataframe(pd.DataFrame.from_dict(st.session_state.cuentas, orient='index', columns=['Saldo']), use_container_width=True)

# Mostrar balanza de comprobación
st.markdown("### ⚖️ Balanza de Comprobación")
balanza = pd.DataFrame.from_dict(st.session_state.cuentas, orient='index', columns=['Saldo'])
balanza['Debe'] = balanza['Saldo'].apply(lambda x: x if x > 0 else 0)
balanza['Haber'] = balanza['Saldo'].apply(lambda x: -x if x < 0 else 0)
st.dataframe(balanza, use_container_width=True)

# Mostrar balance general
st.markdown("### 📈 Balance General")
balance_general = balanza[['Debe', 'Haber']]
st.dataframe(balance_general, use_container_width=True)

# Gráfico de saldos de cuentas
st.markdown("### 📉 Gráfico de Saldos de Cuentas")
st.bar_chart(pd.DataFrame.from_dict(st.session_state.cuentas, orient='index', columns=['Saldo']))