import streamlit as st
from pathlib import Path
import sys
from streamlit_folium import st_folium

# 1. Configuración de rutas (Permite ejecutar desde cualquier nivel del proyecto)
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from app.components.map_view import create_base_map

# 2. Configuración de la página
st.set_page_config(page_title="Cartografía | GeoData", page_icon="🗺️", layout="wide")

st.title("Cartografía")
st.caption("Exploración geológica, topográfica y geotécnica interactiva")

# Rutas de datos
BOREHOLES_FILE = ROOT / "data" / "processed" / "geospatial" / "sondajes.csv"

# 3. Panel de Filtros Superior
col1, col2, col3 = st.columns(3)
with col1:
    proyecto = st.selectbox("Proyecto Activo", ["Archipiélago Sur (Demo)", "Nuevo Proyecto Geotécnico"])
with col2:
    capa_activa = st.multiselect("Capas Visibles", ["Sondajes (SPT/CPT)", "Muestras de Laboratorio"], default=["Sondajes (SPT/CPT)"])
with col3:
    st.info("Interactúa con el mapa o selecciona un marcador para inspeccionar su perfil estratigráfico.")

st.divider()

# 4. Renderizado del Visor Geoespacial
st.subheader("Visor Geoespacial Integrado")

with st.spinner("Renderizando modelo cartográfico..."):
    # Instanciar el mapa desde el componente
    folium_map = create_base_map(BOREHOLES_FILE)
    
    # Renderizado responsivo para evitar recortes de interfaz
    map_data = st_folium(
        folium_map, 
        use_container_width=True, 
        height=600, 
        returned_objects=["last_object_clicked"]
    )

# 5. Panel de Información Dinámica (Reacciona al mapa)
if map_data and map_data.get("last_object_clicked"):
    lat = map_data["last_object_clicked"]["lat"]
    lng = map_data["last_object_clicked"]["lng"]
    
    st.success(f"**Coordenada inspeccionada:** Latitud {lat:.5f}, Longitud {lng:.5f}")
    
    # Simulación de conexión futura con FastAPI y XGBoost
    with st.expander("Ver resultados geotécnicos de esta coordenada"):
        st.dataframe({
            "Profundidad (m)": [5.0, 10.0, 15.0],
            "FS Licuación (XGBoost)": [1.2, 0.85, 2.1],
            "Tipo Suelo": ["SM", "SP-SM", "ML"]
        })