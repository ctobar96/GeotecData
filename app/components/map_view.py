import folium
import pandas as pd
from pathlib import Path

def create_base_map(boreholes_path: Path) -> folium.Map:
    """Genera el visor geoespacial base con acercamiento automático al centro de los datos."""
    
    # 1. Valores por defecto (Vista regional) por si no hay datos
    center_lat, center_lng = -42.628, -73.971
    zoom_level = 9
    
    # 2. Leer los datos PRIMERO para calcular el centro exacto
    puntos_validos = []
    if boreholes_path.exists() and boreholes_path.stat().st_size > 0:
        try:
            df = pd.read_csv(boreholes_path)
            if 'latitud' in df.columns and 'longitud' in df.columns:
                # Filtrar filas sin coordenadas y convertir a diccionario
                puntos_validos = df.dropna(subset=['latitud', 'longitud']).to_dict('records')
                
                if puntos_validos:
                    # Calcular el centroide (promedio de todas las latitudes y longitudes)
                    center_lat = sum(p['latitud'] for p in puntos_validos) / len(puntos_validos)
                    center_lng = sum(p['longitud'] for p in puntos_validos) / len(puntos_validos)
                    # Forzar un acercamiento profundo (13 o 14 es ideal para ver terreno)
                    zoom_level = 13 
        except Exception as e:
            print(f"Error cargando marcadores: {e}")

    # 3. Inicializar el mapa exactamente en el centro de los datos
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=zoom_level,
        tiles=None
    )

    # 4. Capas base
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

    # 5. Agregar los marcadores al mapa
    for row in puntos_validos:
        popup_html = f"<b>ID:</b> {row.get('id', 'N/A')}<br><b>Tipo:</b> {row.get('tipo', 'Sondaje')}"
        folium.Marker(
            location=[row['latitud'], row['longitud']],
            popup=folium.Popup(popup_html, max_width=200),
            icon=folium.Icon(color="blue", icon="info-sign"),
            tooltip=f"Sondaje: {row.get('id', '')}"
        ).add_to(m)

    # 6. Forzar que el control de capas se muestre expandido
    folium.LayerControl(position='topright', collapsed=False).add_to(m)

    return m