"""
05_map_visualization.py
=======================
Visualización sobre mapas: Rendimiento por ubicación de mapas
Crea una representación geográfica conceptual de los mapas de Overwatch

Dataset: Overwatch Competitive Seasons (all_seasons.csv)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
import matplotlib.colors as mcolors

# =============================================================================
# CARGA DE DATOS
# =============================================================================

df = pd.read_csv('/mnt/user-data/uploads/all_seasons__1_.csv')

# Calcular estadísticas por mapa
map_stats = df[df['Map'].notna()].groupby('Map').agg({
    'Result': [
        lambda x: len(x),
        lambda x: (x == 'Win').sum() / len(x) * 100
    ],
    'SR Change': 'mean',
    'Elim': 'mean'
}).round(2)
map_stats.columns = ['Partidas', 'Winrate', 'SR_Change', 'Elim_Avg']
map_stats = map_stats.reset_index()

# =============================================================================
# MAPA CONCEPTUAL DE UBICACIONES DE OVERWATCH
# =============================================================================

# Ubicaciones conceptuales de los mapas (inspiradas en el lore de Overwatch)
# Formato: (x, y, continente/región)
map_locations = {
    # Europa
    'Eichenwalde': (10, 52, 'Europa'),
    "King's Row": (0, 51, 'Europa'),
    'Hollywood': (-118, 34, 'América'),
    'Numbani': (7, 9, 'África'),
    'Rialto': (12, 45, 'Europa'),
    
    # Asia
    'Hanamura': (140, 35, 'Asia'),
    'Lijiang Tower': (104, 30, 'Asia'),
    'Nepal': (85, 28, 'Asia'),
    'Temple of Anubis': (31, 30, 'África'),
    
    # América
    'Route 66': (-110, 35, 'América'),
    'Dorado': (-105, 20, 'América'),
    'Blizzard World': (-120, 33, 'América'),
    'Watchpoint: Gibraltar': (-5, 36, 'Europa'),
    'Junkertown': (138, -34, 'Oceanía'),
    
    # Otros
    'Ilios': (25, 37, 'Europa'),
    'Oasis': (47, 24, 'Asia'),
    'Volskaya Industries': (37, 56, 'Europa'),
    'Horizon Lunar Colony': (0, 70, 'Espacio'),  # Luna
}

# =============================================================================
# FIGURA 1: MAPA MUNDIAL CON RENDIMIENTO POR UBICACIÓN
# =============================================================================

fig, ax = plt.subplots(figsize=(16, 10))

# Dibujar un mapa mundial simplificado
# Fondo
ax.set_facecolor('#E8F4F8')

# Continentes simplificados (representación artística)
# América del Norte
na_x = [-170, -170, -50, -50, -80, -120, -170]
na_y = [15, 70, 70, 45, 25, 15, 15]
ax.fill(na_x, na_y, color='#C8E6C9', alpha=0.7, edgecolor='#388E3C', linewidth=1)

# América del Sur
sa_x = [-80, -35, -35, -80, -80]
sa_y = [-55, -55, 10, 10, -55]
ax.fill(sa_x, sa_y, color='#C8E6C9', alpha=0.7, edgecolor='#388E3C', linewidth=1)

# Europa
eu_x = [-10, 60, 60, -10, -10]
eu_y = [35, 35, 70, 70, 35]
ax.fill(eu_x, eu_y, color='#BBDEFB', alpha=0.7, edgecolor='#1976D2', linewidth=1)

# África
af_x = [-20, 50, 50, -20, -20]
af_y = [-35, -35, 35, 35, -35]
ax.fill(af_x, af_y, color='#FFE0B2', alpha=0.7, edgecolor='#F57C00', linewidth=1)

# Asia
as_x = [60, 180, 180, 60, 60]
as_y = [0, 0, 70, 70, 0]
ax.fill(as_x, as_y, color='#F8BBD9', alpha=0.7, edgecolor='#C2185B', linewidth=1)

# Oceanía
oc_x = [110, 180, 180, 110, 110]
oc_y = [-50, -50, 0, 0, -50]
ax.fill(oc_x, oc_y, color='#D1C4E9', alpha=0.7, edgecolor='#7B1FA2', linewidth=1)

# Colormap para winrate
cmap = plt.cm.RdYlGn
norm = mcolors.Normalize(vmin=30, vmax=70)

# Plotear cada mapa
for _, row in map_stats.iterrows():
    map_name = row['Map']
    if map_name in map_locations:
        x, y, region = map_locations[map_name]
        winrate = row['Winrate']
        partidas = row['Partidas']
        
        # Color basado en winrate
        color = cmap(norm(winrate))
        
        # Tamaño basado en número de partidas
        size = max(100, partidas * 40)
        
        # Dibujar círculo
        circle = ax.scatter(x, y, s=size, c=[color], alpha=0.8, 
                           edgecolors='black', linewidth=2, zorder=5)
        
        # Etiqueta
        ax.annotate(f'{map_name}\n{winrate:.0f}%', 
                   (x, y), 
                   textcoords="offset points", 
                   xytext=(0, -25),
                   ha='center', 
                   fontsize=8, 
                   fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Configuración
ax.set_xlim(-180, 180)
ax.set_ylim(-60, 80)
ax.set_xlabel('Longitud', fontsize=12, fontweight='bold')
ax.set_ylabel('Latitud', fontsize=12, fontweight='bold')
ax.set_title('Mapa Mundial: Rendimiento por Ubicación de Mapas de Overwatch\n(Tamaño = Partidas Jugadas, Color = Winrate)', 
             fontsize=14, fontweight='bold', pad=15)

# Colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, shrink=0.6, pad=0.02)
cbar.set_label('Winrate (%)', fontsize=11, fontweight='bold')

# Leyenda de regiones
region_colors = {
    'América': '#C8E6C9',
    'Europa': '#BBDEFB', 
    'África': '#FFE0B2',
    'Asia': '#F8BBD9',
    'Oceanía': '#D1C4E9'
}
legend_patches = [plt.Rectangle((0, 0), 1, 1, fc=color, alpha=0.7, label=region) 
                  for region, color in region_colors.items()]
ax.legend(handles=legend_patches, loc='lower left', fontsize=9, title='Regiones')

ax.grid(True, alpha=0.3, linestyle='--')

plt.savefig('/home/claude/overwatch_analysis/images/10_world_map_performance.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Mapa mundial guardado: images/10_world_map_performance.png")

# =============================================================================
# FIGURA 2: MAPA DE CALOR POR MODO Y MAPA
# =============================================================================

fig2, ax2 = plt.subplots(figsize=(14, 10))

# Preparar datos
mode_map_data = df[df['Map'].notna() & df['Mode'].notna()].copy()
pivot_data = mode_map_data.pivot_table(
    values='SR Change', 
    index='Map', 
    columns='Mode', 
    aggfunc='mean'
).round(2)

# Ordenar por SR Change promedio total
pivot_data['Total'] = pivot_data.mean(axis=1)
pivot_data = pivot_data.sort_values('Total', ascending=True)
pivot_data = pivot_data.drop('Total', axis=1)

# Crear heatmap
import seaborn as sns
sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='RdBu_r', center=0,
            linewidths=0.5, ax=ax2, cbar_kws={'label': 'SR Change Promedio'},
            annot_kws={'fontsize': 9, 'fontweight': 'bold'})

ax2.set_title('Mapa de Calor: SR Change Promedio por Mapa y Modo de Juego', 
              fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('Modo de Juego', fontsize=12, fontweight='bold')
ax2.set_ylabel('Mapa', fontsize=12, fontweight='bold')

plt.savefig('/home/claude/overwatch_analysis/images/11_map_mode_heatmap.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Heatmap Mapa/Modo guardado: images/11_map_mode_heatmap.png")

# =============================================================================
# FIGURA 3: DIAGRAMA RADIAL DE MAPAS POR TIPO
# =============================================================================

fig3, axes = plt.subplots(2, 2, figsize=(14, 14), subplot_kw=dict(projection='polar'))

modes = ['Assault', 'Assault/Escort', 'Control', 'Escort']
colors = ['#E91E63', '#9C27B0', '#3F51B5', '#00BCD4']

for idx, (mode, ax, color) in enumerate(zip(modes, axes.flatten(), colors)):
    mode_maps = map_stats[map_stats['Map'].isin(
        df[df['Mode'] == mode]['Map'].unique()
    )].copy()
    
    if len(mode_maps) == 0:
        continue
    
    # Preparar datos para gráfica polar
    N = len(mode_maps)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # Cerrar el círculo
    
    values = mode_maps['Winrate'].tolist()
    values += values[:1]
    
    # Dibujar
    ax.plot(angles, values, 'o-', linewidth=2, color=color, markersize=8)
    ax.fill(angles, values, alpha=0.25, color=color)
    
    # Etiquetas
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(mode_maps['Map'].tolist(), size=8)
    ax.set_ylim(0, 100)
    ax.set_title(f'{mode}\n(Winrate por Mapa)', fontsize=12, fontweight='bold', pad=20)
    
    # Línea de referencia en 50%
    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5)

plt.suptitle('Diagrama Radial: Winrate por Mapa según Modo de Juego', 
             fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('/home/claude/overwatch_analysis/images/12_radar_maps.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Diagrama Radial guardado: images/12_radar_maps.png")

print("\n¡Todas las visualizaciones de mapas generadas exitosamente!")
