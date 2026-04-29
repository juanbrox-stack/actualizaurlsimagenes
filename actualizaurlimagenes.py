import streamlit as st
import requests

st.set_page_config(page_title="Actualizador de Imágenes", page_icon="📸")

# Inicializar el estado de la lista si no existe
if 'skus' not in st.session_state:
    st.session_state['skus'] = ""

def limpiar_lista():
    st.session_state['skus'] = ""

st.title("🚀 Actualizador de URLs de las Imágenes PrestaShop")
st.markdown("Pega tu lista de SKUs abajo. La aplicación los detectará automáticamente.")

# El área de texto ahora está vinculada al session_state
sku_input = st.text_area(
    "Lista de SKUs:", 
    value=st.session_state['skus'], 
    height=300, 
    key="skus",
    placeholder="A01_EU01_101437\nA01_EU01_116606..."
)

if sku_input:
    # 1. Procesamiento de la lista
    lista_skus = [line.strip() for line in sku_input.split('\n') if line.strip()]
    skus_concatenados = ",".join(lista_skus)
    
    st.info(f"✅ Se han detectado **{len(lista_skus)}** SKUs listos para procesar.")

    # 2. Configuración de la URL
    url_base = "https://turaco.es/marketplaces/resources/generate.php"
    params = {"metodo": "imagen", "sku": skus_concatenados}
    full_url = f"{url_base}?metodo=imagen&sku={skus_concatenados}"

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Ejecutar actualización", use_container_width=True):
            with st.spinner("Actualizando..."):
                try:
                    response = requests.get(url_base, params=params, timeout=60)
                    if response.status_code == 200:
                        st.success("¡Completado!")
                        st.text_area("Respuesta del servidor:", value=response.text, height=100)
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")

    with col2:
        # Botón para limpiar
        st.button("🗑️ Limpiar lista", on_click=limpiar_lista, use_container_width=True)

    st.markdown("---")
    st.markdown("**Enlace directo (por si prefieres abrirlo en el navegador):**")
    st.link_button("Abrir URL en nueva pestaña", full_url)

else:
    st.warning("Esperando a que pegues los SKUs...")