"""
07_geopandas_heroes_map.py
===========================
Mapa de distribución mundial de héroes de Overwatch usando GeoPandas
Reemplaza el mapa interactivo de Leaflet.js con una visualización estática de GeoPandas

Características:
- Mapa mundial con países usando GeoPandas
- Marcadores de héroes por rol con colores
- Leyenda interactiva con conteos
- Anotaciones para ubicaciones especiales
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# =============================================================================
# DATOS DE HÉROES
# =============================================================================

heroes_data = [
    # Africa
    {"name": "Ana", "role": "Support", "country": "Egypt", "lat": 26.8206, "lng": 30.8025},
    {"name": "Pharah", "role": "Damage", "country": "Egypt", "lat": 27.5, "lng": 31.5},
    {"name": "Doomfist", "role": "Tank", "country": "Nigeria", "lat": 9.0820, "lng": 8.6753},
    {"name": "Orisa", "role": "Tank", "country": "Numbani", "lat": 6.5244, "lng": 3.3792},
    # Americas
    {"name": "Ashe", "role": "Damage", "country": "United States", "lat": 35.5, "lng": -105.5},
    {"name": "Cassidy", "role": "Damage", "country": "United States", "lat": 33.5, "lng": -112.0},
    {"name": "Reaper", "role": "Damage", "country": "United States", "lat": 34.0522, "lng": -118.2437},
    {"name": "Soldier: 76", "role": "Damage", "country": "United States", "lat": 39.7392, "lng": -104.9903},
    {"name": "Sojourn", "role": "Damage", "country": "Canada", "lat": 43.6532, "lng": -79.3832},
    {"name": "Venture", "role": "Damage", "country": "Canada", "lat": 45.5017, "lng": -73.5673},
    {"name": "Sombra", "role": "Damage", "country": "Mexico", "lat": 19.4326, "lng": -99.1332},
    {"name": "Baptiste", "role": "Support", "country": "Haiti", "lat": 18.9712, "lng": -72.2852},
    {"name": "Lúcio", "role": "Support", "country": "Brazil", "lat": -22.9068, "lng": -43.1729},
    {"name": "Illari", "role": "Support", "country": "Peru", "lat": -13.5319, "lng": -71.9675},
    # Europe
    {"name": "Tracer", "role": "Damage", "country": "United Kingdom", "lat": 51.5074, "lng": -0.1278},
    {"name": "Hazard", "role": "Damage", "country": "Scotland", "lat": 55.9533, "lng": -3.1883},
    {"name": "Widowmaker", "role": "Damage", "country": "France", "lat": 48.8566, "lng": 2.3522},
    {"name": "Reinhardt", "role": "Tank", "country": "Germany", "lat": 52.5200, "lng": 13.4050},
    {"name": "Sigma", "role": "Tank", "country": "Netherlands", "lat": 52.3676, "lng": 4.9041},
    {"name": "Mercy", "role": "Support", "country": "Switzerland", "lat": 46.9480, "lng": 7.4474},
    {"name": "Moira", "role": "Support", "country": "Ireland", "lat": 53.3498, "lng": -6.2603},
    {"name": "Brigitte", "role": "Support", "country": "Sweden", "lat": 59.3293, "lng": 18.0686},
    {"name": "Torbjörn", "role": "Damage", "country": "Sweden", "lat": 57.7089, "lng": 11.9746},
    {"name": "Zarya", "role": "Tank", "country": "Russia", "lat": 55.7558, "lng": 37.6173},
    # Asia
    {"name": "Genji", "role": "Damage", "country": "Japan", "lat": 35.6762, "lng": 139.6503},
    {"name": "Hanzo", "role": "Damage", "country": "Japan", "lat": 34.6937, "lng": 135.5023},
    {"name": "Kiriko", "role": "Support", "country": "Japan", "lat": 35.0116, "lng": 135.7681},
    {"name": "D.Va", "role": "Tank", "country": "South Korea", "lat": 37.5665, "lng": 126.9780},
    {"name": "Mei", "role": "Damage", "country": "China", "lat": 31.2304, "lng": 121.4737},
    {"name": "Symmetra", "role": "Damage", "country": "India", "lat": 28.6139, "lng": 77.2090},
    {"name": "Lifeweaver", "role": "Support", "country": "Thailand", "lat": 13.7563, "lng": 100.5018},
    {"name": "Echo", "role": "Damage", "country": "Singapore", "lat": 1.3521, "lng": 103.8198},
    {"name": "Ramattra", "role": "Tank", "country": "Nepal", "lat": 27.7172, "lng": 85.3240},
    {"name": "Zenyatta", "role": "Support", "country": "Nepal", "lat": 28.3949, "lng": 84.1240},
    # Oceania
    {"name": "Junker Queen", "role": "Tank", "country": "Australia", "lat": -33.8688, "lng": 151.2093},
    {"name": "Junkrat", "role": "Damage", "country": "Australia", "lat": -27.4698, "lng": 153.0251},
    {"name": "Roadhog", "role": "Tank", "country": "Australia", "lat": -31.9505, "lng": 115.8605},
    {"name": "Mauga", "role": "Tank", "country": "Samoa", "lat": -13.8333, "lng": -171.75},
    # Special Locations
    {"name": "Winston", "role": "Tank", "country": "The Moon", "lat": 70, "lng": 0},
    {"name": "Wrecking Ball", "role": "Tank", "country": "The Moon", "lat": 72, "lng": 10},
    {"name": "Juno", "role": "Support", "country": "Mars", "lat": 75, "lng": -20},
    {"name": "Bastion", "role": "Damage", "country": "Unknown", "lat": 50, "lng": 10}
]

# Crear DataFrame
heroes_df = pd.DataFrame(heroes_data)

# Colores por rol (igual que Leaflet)
role_colors = {
    "Tank": "#3498db",      # Azul
    "Damage": "#e74c3c",    # Rojo
    "Support": "#2ecc71"    # Verde
}

# =============================================================================
# CREAR MAPA CON GEOPANDAS
# =============================================================================

print("Cargando mapa mundial...")

# Intentar cargar el mapa mundial de diferentes fuentes
try:
    # Opción 1: Usar Natural Earth directamente desde la URL
    world = gpd.read_file("https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip")
    print("Mapa cargado desde Natural Earth")
except Exception as e:
    print("No se pudo cargar desde Natural Earth")
    print("Usando mapa simplificado")
    # Opción 2: Crear un mapa simplificado si falla
    from shapely.geometry import box
    import numpy as np

    # Crear continentes simplificados
    continents = {
        'geometry': [
            box(-170, 15, -30, 75),   # América del Norte
            box(-80, -60, -35, 15),   # América del Sur
            box(-15, 35, 40, 70),     # Europa
            box(-20, -40, 55, 40),    # África
            box(25, -10, 180, 75),    # Asia
            box(110, -50, 180, -10),  # Oceanía
        ],
        'name': ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Oceania']
    }
    world = gpd.GeoDataFrame(continents, crs="EPSG:4326")

# Crear figura
fig, ax = plt.subplots(figsize=(20, 12), facecolor='#1a1a2e')
ax.set_facecolor('#0d1117')

# Dibujar países
world.plot(ax=ax, color='#2d3748', edgecolor='#4a5568', linewidth=0.5, alpha=0.8)

# =============================================================================
# AÑADIR HÉROES AL MAPA
# =============================================================================

print("Añadiendo héroes al mapa...")

# Plotear cada héroe
for _, hero in heroes_df.iterrows():
    color = role_colors[hero['role']]

    # Marcador principal (círculo grande)
    ax.scatter(hero['lng'], hero['lat'],
               s=400,
               c=color,
               alpha=0.8,
               edgecolors='white',
               linewidth=2.5,
               zorder=5)

    # Círculo interior (efecto de borde)
    ax.scatter(hero['lng'], hero['lat'],
               s=250,
               c=color,
               alpha=1.0,
               edgecolors='none',
               zorder=6)

    # Añadir nombre del héroe (solo para ubicaciones no aglomeradas)
    # Para evitar superposición, solo mostramos nombres en ubicaciones especiales
    if hero['country'] in ['The Moon', 'Mars', 'Unknown']:
        ax.annotate(hero['name'],
                   (hero['lng'], hero['lat']),
                   xytext=(10, 10),
                   textcoords='offset points',
                   fontsize=9,
                   color='white',
                   fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5',
                            facecolor=color,
                            edgecolor='white',
                            alpha=0.9),
                   zorder=7)

# =============================================================================
# AÑADIR LEYENDA
# =============================================================================

# Contar héroes por rol
role_counts = heroes_df['role'].value_counts()

# Crear elementos de leyenda
legend_elements = []
for role, color in role_colors.items():
    count = role_counts.get(role, 0)
    legend_elements.append(
        Line2D([0], [0],
               marker='o',
               color='w',
               label=f'{role} ({count})',
               markerfacecolor=color,
               markeredgecolor='white',
               markeredgewidth=2,
               markersize=12)
    )

# Añadir leyenda
legend = ax.legend(handles=legend_elements,
                   loc='lower right',
                   fontsize=13,
                   frameon=True,
                   facecolor='#1a1a2e',
                   edgecolor='#F99E1A',
                   framealpha=0.95,
                   title='Roles',
                   title_fontsize=15)
legend.get_title().set_color('#F99E1A')
for text in legend.get_texts():
    text.set_color('white')

# =============================================================================
# AÑADIR ANOTACIONES ESPECIALES
# =============================================================================

# Cuadro de información de ubicaciones especiales
info_text = (
    "Ubicaciones Especiales:\n"
    "Luna: Winston, Wrecking Ball\n"
    "Marte: Juno\n"
    "Desconocido: Bastion"
)

# Añadir cuadro de información
ax.text(0.02, 0.98, info_text,
        transform=ax.transAxes,
        fontsize=11,
        verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.7',
                 facecolor='#1a1a2e',
                 edgecolor='#F99E1A',
                 alpha=0.95,
                 linewidth=2),
        color='white',
        fontweight='bold',
        zorder=10)

# Añadir contador total
total_heroes = len(heroes_df)
ax.text(0.98, 0.98, f'Total: {total_heroes} héroes',
        transform=ax.transAxes,
        fontsize=13,
        verticalalignment='top',
        horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.7',
                 facecolor='#1a1a2e',
                 edgecolor='#F99E1A',
                 alpha=0.95,
                 linewidth=2),
        color='#F99E1A',
        fontweight='bold',
        zorder=10)

# =============================================================================
# CONFIGURACIÓN FINAL
# =============================================================================

# Título
ax.set_title('Mapa Mundial Interactivo - Distribución de Héroes de Overwatch\n' +
             'Por Origen según el Lore del Juego',
             fontsize=18,
             fontweight='bold',
             color='#F99E1A',
             pad=20)

# Quitar ejes
ax.set_xlabel('Longitud', fontsize=12, color='white', fontweight='bold')
ax.set_ylabel('Latitud', fontsize=12, color='white', fontweight='bold')

# Configurar límites
ax.set_xlim(-180, 180)
ax.set_ylim(-60, 85)

# Grid sutil
ax.grid(True, alpha=0.2, linestyle='--', color='#4a5568', linewidth=0.5)

# Color de ticks
ax.tick_params(colors='white', labelsize=10)

# Agregar créditos
fig.text(0.99, 0.01, 'Generado con GeoPandas + Matplotlib | Overwatch Heroes Map',
         ha='right', va='bottom', fontsize=9, color='#666', style='italic')

# Ajustar layout
plt.tight_layout()

# =============================================================================
# GUARDAR FIGURA
# =============================================================================

import os
os.makedirs('../images', exist_ok=True)

output_path = '../images/10_geopandas_heroes_map.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
print(f"Mapa de heroes guardado: {output_path}")

plt.close()

# =============================================================================
# CREAR VERSIÓN CON ETIQUETAS (MÁS DETALLADA)
# =============================================================================

print("\nCreando versión detallada con etiquetas de héroes...")

fig2, ax2 = plt.subplots(figsize=(24, 14), facecolor='#1a1a2e')
ax2.set_facecolor('#0d1117')

# Dibujar países
world.plot(ax=ax2, color='#2d3748', edgecolor='#4a5568', linewidth=0.5, alpha=0.8)

# Plotear cada héroe con etiquetas
for idx, hero in heroes_df.iterrows():
    color = role_colors[hero['role']]

    # Marcador
    ax2.scatter(hero['lng'], hero['lat'],
               s=300,
               c=color,
               alpha=0.8,
               edgecolors='white',
               linewidth=2,
               zorder=5)

    # Etiqueta con nombre
    ax2.annotate(hero['name'],
                (hero['lng'], hero['lat']),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=7,
                color='white',
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3',
                         facecolor=color,
                         edgecolor='white',
                         alpha=0.85,
                         linewidth=1),
                zorder=7)

# Leyenda
legend2 = ax2.legend(handles=legend_elements,
                    loc='lower right',
                    fontsize=14,
                    frameon=True,
                    facecolor='#1a1a2e',
                    edgecolor='#F99E1A',
                    framealpha=0.95,
                    title='Roles',
                    title_fontsize=16)
legend2.get_title().set_color('#F99E1A')
for text in legend2.get_texts():
    text.set_color('white')

# Título
ax2.set_title('Mapa Mundial Detallado - Todos los Héroes de Overwatch con Nombres\n' +
             f'Total: {total_heroes} héroes distribuidos por el mundo',
             fontsize=20,
             fontweight='bold',
             color='#F99E1A',
             pad=20)

# Configuración
ax2.set_xlabel('Longitud', fontsize=13, color='white', fontweight='bold')
ax2.set_ylabel('Latitud', fontsize=13, color='white', fontweight='bold')
ax2.set_xlim(-180, 180)
ax2.set_ylim(-60, 85)
ax2.grid(True, alpha=0.2, linestyle='--', color='#4a5568', linewidth=0.5)
ax2.tick_params(colors='white', labelsize=10)

fig2.text(0.99, 0.01, 'Generado con GeoPandas + Matplotlib | Overwatch Heroes Map (Detailed)',
         ha='right', va='bottom', fontsize=9, color='#666', style='italic')

plt.tight_layout()

# Guardar versión detallada
output_path2 = '../images/10_geopandas_heroes_map_detailed.png'
plt.savefig(output_path2, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
print(f"Mapa detallado de heroes guardado: {output_path2}")

plt.close()

# =============================================================================
# ESTADÍSTICAS FINALES
# =============================================================================

print("\n" + "="*60)
print("ESTADÍSTICAS DEL MAPA DE HÉROES")
print("="*60)
print(f"\nTotal de héroes: {total_heroes}")
print("\nHéroes por rol:")
for role, count in role_counts.items():
    print(f"  {role}: {count}")

print("\nHéroes por región geográfica:")
regions = {
    'América': ['United States', 'Canada', 'Mexico', 'Haiti', 'Brazil', 'Peru'],
    'Europa': ['United Kingdom', 'Scotland', 'France', 'Germany', 'Netherlands',
               'Switzerland', 'Ireland', 'Sweden', 'Russia'],
    'Asia': ['Japan', 'South Korea', 'China', 'India', 'Thailand', 'Singapore', 'Nepal'],
    'África': ['Egypt', 'Nigeria', 'Numbani'],
    'Oceanía': ['Australia', 'Samoa'],
    'Especial': ['The Moon', 'Mars', 'Unknown']
}

for region, countries in regions.items():
    count = heroes_df[heroes_df['country'].isin(countries)].shape[0]
    print(f"  {region}: {count}")

print("\nMapas generados exitosamente!")
print("  - Version simple: images/10_geopandas_heroes_map.png")
print("  - Version detallada: images/10_geopandas_heroes_map_detailed.png")
