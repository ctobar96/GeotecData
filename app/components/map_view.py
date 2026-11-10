import folium
import pandas as pd
from pathlib import Path

def create_base_map(boreholes_path: Path) -> folium.Map:
    """Genera el visor geoespacial base enfocado en las ubicaciones de sondajes."""
    
    # Coordenadas y zoom de respaldo en caso de que no existan puntos cargados
    default_location = [-42.628, -73.971]
    default_zoom = 9
    
    # Inicializar mapa base sin azulejos por defecto
    m = folium.Map(
        location=default_location,
        zoom_start=default_zoom,
        tiles=None
    )

    # 1. Capas base
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        attr='&copy; CARTO',
        name='Mapa Claro (Blanco)',
        overlay=False,
        control=True,
        show=True
    ).add_to(m)

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satélite Esri',
        overlay=False,
        control=True,
        show=False
    ).add_to(m)

    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='&copy; OpenStreetMap',
        name='OpenStreetMap (Estándar)',
        overlay=False,
        control=True,
        show=False
    ).add_to(m)

    # 2. Cargar marcadores y recolectar coordenadas
    points = []
    if boreholes_path.exists() and boreholes_path.stat().st_size > 0:
        try:
            df = pd.read_csv(boreholes_path)
            if 'latitud' in df.columns and 'longitud' in df.columns:
                for _, row in df.iterrows():
                    lat, lng = row['latitud'], row['longitud']
                    points.append([lat, lng])
                    
                    popup_html = f"<b>ID:</b> {row.get('id', 'N/A')}<br><b>Tipo:</b> {row.get('tipo', 'Sondaje')}"
                    folium.Marker(
                        location=[lat, lng],
                        popup=folium.Popup(popup_html, max_width=200),
                        icon=folium.Icon(color="blue", icon="info-sign"),
                        tooltip=f"Sondaje: {row.get('id', '')}"
                    ).add_to(m)
        except Exception as e:
            print(f"Error cargando marcadores: {e}")

    # 3. Autozoom: Encadra automáticamente todos los sondajes detectados
    if points:
        m.fit_bounds(points, padding=(30, 30))

    # 4. Control de capas en la esquina superior derecha
    folium.LayerControl(position='topright', collapsed=False).add_to(m)

    return m