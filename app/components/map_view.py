import folium
import pandas as pd
from pathlib import Path

def create_base_map(boreholes_path: Path) -> folium.Map:
    """Genera el visor geoespacial base con capas intercambiables y marcadores."""
    
    # 1. Inicializar el mapa sin azulejos por defecto (tiles=None)
    m = folium.Map(
        location=[-42.628, -73.971],
        zoom_start=9,
        tiles=None
    )

    # 2. Capa Clara / En Blanco (CartoDB Positron) - Visible por defecto
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
        name='Mapa Claro (Blanco)',
        overlay=False,
        control=True,
        show=True
    ).add_to(m)

    # 3. Capa Satelital (Esri World Imagery)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satélite Esri',
        overlay=False,
        control=True,
        show=False
    ).add_to(m)

    # 4. Capa Callejera Estándar (OpenStreetMap)
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='&copy; OpenStreetMap contributors',
        name='OpenStreetMap (Estándar)',
        overlay=False,
        control=True,
        show=False
    ).add_to(m)

    # 5. Ingesta de marcadores de sondajes (Manejo seguro)
    if boreholes_path.exists() and boreholes_path.stat().st_size > 0:
        try:
            df = pd.read_csv(boreholes_path)
            if 'latitud' in df.columns and 'longitud' in df.columns:
                for _, row in df.iterrows():
                    popup_html = f"<b>ID:</b> {row.get('id', 'N/A')}<br><b>Tipo:</b> {row.get('tipo', 'Sondaje')}"
                    folium.Marker(
                        location=[row['latitud'], row['longitud']],
                        popup=folium.Popup(popup_html, max_width=200),
                        icon=folium.Icon(color="blue", icon="info-sign"),
                        tooltip=f"Sondaje: {row.get('id', '')}"
                    ).add_to(m)
        except Exception as e:
            print(f"Error cargando marcadores: {e}")

    # 6. Desplegar el selector de capas visible en la esquina superior derecha
    folium.LayerControl(position='topright', collapsed=False).add_to(m)

    return m