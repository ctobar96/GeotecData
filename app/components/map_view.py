import folium
import pandas as pd
from pathlib import Path

def create_base_map(boreholes_path: Path) -> folium.Map:
    """Genera el visor geoespacial base con alto nivel de zoom predial."""
    
    # Coordenadas por defecto
    center_lat, center_lng = -42.628, -73.971
    zoom_level = 16  # Zoom cercano para ver el punto exacto en el terreno
    
    puntos_validos = []
    if boreholes_path.exists() and boreholes_path.stat().st_size > 0:
        try:
            df = pd.read_csv(boreholes_path)
            if 'latitud' in df.columns and 'longitud' in df.columns:
                puntos_validos = df.dropna(subset=['latitud', 'longitud']).to_dict('records')
                
                if puntos_validos:
                    # Centrar en el primer sondaje
                    center_lat = puntos_validos[0]['latitud']
                    center_lng = puntos_validos[0]['longitud']
        except Exception as e:
            print(f"Error cargando marcadores: {e}")

    # Inicializar el mapa con zoom cercano
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=zoom_level,
        tiles=None
    )

    # Capas base
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satélite Esri',
        overlay=False,
        control=True,
        show=True  # Inicia directamente en Satélite para ubicar el punto en terreno
    ).add_to(m)

    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        attr='&copy; CARTO',
        name='Mapa Claro (Blanco)',
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

    # Agregar marcadores
    for row in puntos_validos:
        popup_html = f"<b>ID:</b> {row.get('id', 'N/A')}<br><b>Tipo:</b> {row.get('tipo', 'Sondaje')}"
        folium.Marker(
            location=[row['latitud'], row['longitud']],
            popup=folium.Popup(popup_html, max_width=200),
            icon=folium.Icon(color="red", icon="info-sign"),
            tooltip=f"Sondaje: {row.get('id', '')}"
        ).add_to(m)

    folium.LayerControl(position='topright', collapsed=False).add_to(m)

    return m