import folium # Permite crear mapas interactivos con Leaflet.js
import pandas as pd # Permite manipular y analizar datos tabulares
from pathlib import Path # Permite manejar rutas de archivos de manera independiente del sistema operativo

def create_base_map(boreholes_path: Path) -> folium.Map:
    """Genera el visor geoespacial base con capas intercambiables y marcadores."""
    # Coordenadas iniciales por defecto (Zona Sur / Archipiélago de Chiloé)
    m = folium.Map(location=[-42.628, -73.971], zoom_start=9, tiles="cartodbpositron")
    
    # Capa base alternativa (Satélite) // Esta sección incorpora una segunda cartografía al mapa.
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', # Dirección desde donde se obtienen las imágenes satelitales.
        attr='Esri',    # Atribución de la fuente de datos (Esri)
        name='Satélite Esri',   # Nombre que aparecerá en el control de capas para esta capa base.
        overlay=False,          # Indica que es un mapa base alternativo, no una capa superpuesta.
        control=True            # Permite seleccionarlo desde el control de capas.
    ).add_to(m)

    # Ingesta de sondajes (Manejo seguro por si el archivo está vacío)
    if boreholes_path.exists() and boreholes_path.stat().st_size > 0:
        try:
            df = pd.read_csv(boreholes_path)
            if 'latitud' in df.columns and 'longitud' in df.columns:
                for _, row in df.iterrows():
                    popup_html = f"<b>ID:</b> {row.get('id', 'N/A')}<br><b>Tipo:</b> {row.get('tipo', 'Sondaje')}"
                    folium.Marker(
                        location=[row['latitud'], row['longitud']],
                        popup=folium.Popup(popup_html, max_width=200),
                        icon=folium.Icon(color="darkblue", icon="info-sign"),
                        tooltip="Clic para detalles"
                    ).add_to(m)
        except Exception as e:
            print(f"Error cargando marcadores: {e}")

    # Habilitar el control de capas (arriba a la derecha)
    folium.LayerControl().add_to(m)
    
    return m