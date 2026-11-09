import folium
import pandas as pd
from pathlib import Path

def create_base_map(boreholes_path: Path) -> folium.Map:
    """Genera el visor geoespacial base con capas intercambiables y marcadores."""
    # Coordenadas iniciales por defecto (Zona Sur / Archipiélago de Chiloé)
    m = folium.Map(location=[-42.628, -73.971], zoom_start=9, tiles="cartodbpositron")
    
    # Capa base alternativa (Satélite)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satélite Esri',
        overlay=False,
        control=True
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