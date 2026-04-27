import streamlit as st
import requests

st.set_page_config(page_title="Actualizador de Imágenes PrestaShop", page_icon="📸")

st.title("🚀 Actualizador de Imágenes por SKU")
st.markdown("Pega tu lista de SKUs abajo (uno por línea) para generar la actualización.")

# Área de texto para pegar los SKUs
sku_input = st.text_area("Lista de SKUs:", height=300, placeholder="A01_EU01_101437\nA01_EU01_116606...")

if sku_input:
    # 1. Limpiar y procesar la lista
    # Separamos por saltos de línea, quitamos espacios y filtramos líneas vacías
    lista_skus = [line.strip() for line in sku_input.split('\n') if line.strip()]
    
    # 2. Unir por comas
    skus_concatenados = ",".join(lista_skus)
    
    # 3. Construir la URL base
    url_base = "https://turaco.es/marketplaces/resources/generate.php"
    params = {
        "metodo": "imagen",
        "sku": skus_concatenados
    }
    
    # Mostrar resumen
    st.info(f"Se han detectado **{len(lista_skus)}** SKUs.")

    # Opción A: Botón para ejecutar la petición directamente desde el servidor
    if st.button("Ejecutar actualización ahora"):
        with st.spinner("Conectando con el servidor..."):
            try:
                response = requests.get(url_base, params=params, timeout=60)
                if response.status_code == 200:
                    st.success("✅ Petición enviada con éxito.")
                    st.write("Respuesta del servidor:")
                    st.code(response.text)
                else:
                    st.error(f"Error en el servidor: {response.status_code}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")

    # Opción B: Generar el enlace para abrir manualmente
    full_url = f"{url_base}?metodo=imagen&sku={skus_concatenados}"
    st.markdown(f"---")
    st.markdown(f"**O usa este enlace directo:**")
    st.link_button("Abrir URL de actualización", full_url)