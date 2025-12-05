"""
02_matplotlib_dashboard.py
==========================
Dashboard con múltiples gráficas usando Matplotlib
Incluye: scatter, pie, plot, barras, barras apiladas, barras verticales

Parámetros modificados: leyendas, ticks, tamaños, etiquetas, títulos, 
                        tamaños, colores, anchuras, alturas

Dataset: Overwatch Competitive Seasons (all_seasons.csv)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# Configuración global de estilo
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# =============================================================================
# CARGA DE DATOS
# =============================================================================

df = pd.read_csv('/mnt/user-data/uploads/all_seasons__1_.csv')
df['Start SR Numeric'] = pd.to_numeric(df['Start SR'], errors='coerce')
df['End SR Numeric'] = pd.to_numeric(df['End SR'], errors='coerce')
df['SR Change'] = pd.to_numeric(df['SR Change'], errors='coerce')

# Colores personalizados para el tema de Overwatch
COLORS = {
    'win': '#4CAF50',      # Verde
    'loss': '#F44336',     # Rojo
    'draw': '#FFC107',     # Amarillo
    'primary': '#FF9800',  # Naranja Overwatch
    'secondary': '#2196F3', # Azul
    'tank': '#2196F3',     # Azul
    'support': '#4CAF50',  # Verde
    'offense': '#F44336',  # Rojo
    'defense': '#9C27B0',  # Púrpura
    'seasons': ['#E91E63', '#9C27B0', '#3F51B5', '#00BCD4']  # Paleta temporadas
}

# =============================================================================
# FIGURA 1: DASHBOARD PRINCIPAL
# =============================================================================

fig = plt.figure(figsize=(16, 12))
fig.suptitle('Overwatch Competitive Analysis - Dashboard Principal', 
             fontsize=18, fontweight='bold', y=0.98)

gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)

# -----------------------------------------------------------------------------
# Gráfica 1: SCATTER - SR Change vs Eliminaciones
# -----------------------------------------------------------------------------
ax1 = fig.add_subplot(gs[0, 0])

scatter_data = df[df['Elim'].notna() & df['SR Change'].notna()].copy()
colors_scatter = scatter_data['Result'].map({'Win': COLORS['win'], 'Loss': COLORS['loss'], 'Draw': COLORS['draw']})

scatter = ax1.scatter(scatter_data['Elim'], scatter_data['SR Change'], 
                      c=colors_scatter, alpha=0.6, s=50, edgecolors='white', linewidth=0.5)

ax1.set_xlabel('Eliminaciones', fontsize=10, fontweight='bold')
ax1.set_ylabel('Cambio de SR', fontsize=10, fontweight='bold')
ax1.set_title('Scatter: SR Change vs Eliminaciones', fontsize=11, fontweight='bold', pad=10)
ax1.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
ax1.set_xlim(0, scatter_data['Elim'].max() + 5)

# Leyenda personalizada
legend_elements = [mpatches.Patch(color=COLORS['win'], label='Victoria'),
                   mpatches.Patch(color=COLORS['loss'], label='Derrota'),
                   mpatches.Patch(color=COLORS['draw'], label='Empate')]
ax1.legend(handles=legend_elements, loc='upper right', fontsize=8, framealpha=0.9)

# Ticks personalizados
ax1.tick_params(axis='both', which='major', labelsize=9)
ax1.set_xticks(np.arange(0, scatter_data['Elim'].max() + 10, 10))

# -----------------------------------------------------------------------------
# Gráfica 2: PIE - Distribución de Resultados
# -----------------------------------------------------------------------------
ax2 = fig.add_subplot(gs[0, 1])

results_counts = df['Result'].value_counts()
colors_pie = [COLORS['win'], COLORS['loss'], COLORS['draw']]
explode = (0.05, 0.02, 0.02)

wedges, texts, autotexts = ax2.pie(results_counts, 
                                    explode=explode,
                                    labels=results_counts.index,
                                    colors=colors_pie,
                                    autopct='%1.1f%%',
                                    startangle=90,
                                    shadow=True,
                                    textprops={'fontsize': 10, 'fontweight': 'bold'})

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax2.set_title('Pie: Distribución de Resultados', fontsize=11, fontweight='bold', pad=10)

# Añadir número total en el centro
centre_circle = plt.Circle((0, 0), 0.50, fc='white')
ax2.add_artist(centre_circle)
ax2.text(0, 0, f'Total\n{len(df)}', ha='center', va='center', fontsize=12, fontweight='bold')

# -----------------------------------------------------------------------------
# Gráfica 3: LINE PLOT - Evolución del SR por temporada
# -----------------------------------------------------------------------------
ax3 = fig.add_subplot(gs[0, 2])

for idx, season in enumerate(df['season'].unique()):
    season_data = df[df['season'] == season].copy()
    season_data = season_data.sort_values('Game #')
    ax3.plot(season_data['Game #'], season_data['End SR Numeric'], 
             label=f'Temporada {season}', 
             color=COLORS['seasons'][idx % len(COLORS['seasons'])],
             linewidth=2, alpha=0.8)

ax3.set_xlabel('Número de Partida', fontsize=10, fontweight='bold')
ax3.set_ylabel('SR', fontsize=10, fontweight='bold')
ax3.set_title('Plot: Evolución del SR por Temporada', fontsize=11, fontweight='bold', pad=10)
ax3.legend(loc='best', fontsize=8, framealpha=0.9)

# Añadir líneas de referencia para rangos
ax3.axhline(y=2500, color='gold', linestyle=':', linewidth=1.5, alpha=0.7, label='Platino')
ax3.axhline(y=3000, color='silver', linestyle=':', linewidth=1.5, alpha=0.7, label='Diamante')
ax3.tick_params(axis='both', which='major', labelsize=9)

# -----------------------------------------------------------------------------
# Gráfica 4: BARRAS VERTICALES - Winrate por Mapa
# -----------------------------------------------------------------------------
ax4 = fig.add_subplot(gs[1, :2])

map_data = df[df['Map'].notna()].groupby('Map').agg({
    'Result': [lambda x: len(x), lambda x: (x == 'Win').sum() / len(x) * 100]
}).round(2)
map_data.columns = ['Partidas', 'Winrate']
map_data = map_data.sort_values('Winrate', ascending=True)

bars = ax4.barh(range(len(map_data)), map_data['Winrate'], 
                color=[COLORS['win'] if wr >= 50 else COLORS['loss'] for wr in map_data['Winrate']],
                height=0.7, edgecolor='white', linewidth=0.5)

ax4.set_yticks(range(len(map_data)))
ax4.set_yticklabels(map_data.index, fontsize=9)
ax4.set_xlabel('Winrate (%)', fontsize=10, fontweight='bold')
ax4.set_title('Barras Horizontales: Winrate por Mapa', fontsize=11, fontweight='bold', pad=10)
ax4.axvline(x=50, color='gray', linestyle='--', linewidth=2, alpha=0.7)

# Añadir valores al final de cada barra
for i, (bar, wr) in enumerate(zip(bars, map_data['Winrate'])):
    ax4.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
             f'{wr:.1f}%', va='center', fontsize=8, fontweight='bold')

ax4.set_xlim(0, 85)
ax4.tick_params(axis='x', which='major', labelsize=9)

# -----------------------------------------------------------------------------
# Gráfica 5: BARRAS APILADAS - Resultados por Temporada
# -----------------------------------------------------------------------------
ax5 = fig.add_subplot(gs[1, 2])

season_results = df.groupby(['season', 'Result']).size().unstack(fill_value=0)
season_results = season_results[['Win', 'Loss', 'Draw']]

x = np.arange(len(season_results))
width = 0.6

bottom = np.zeros(len(season_results))
for col, color in zip(['Win', 'Loss', 'Draw'], [COLORS['win'], COLORS['loss'], COLORS['draw']]):
    ax5.bar(x, season_results[col], width, label=col, bottom=bottom, color=color, edgecolor='white')
    bottom += season_results[col]

ax5.set_xlabel('Temporada', fontsize=10, fontweight='bold')
ax5.set_ylabel('Número de Partidas', fontsize=10, fontweight='bold')
ax5.set_title('Barras Apiladas: Resultados por Temporada', fontsize=11, fontweight='bold', pad=10)
ax5.set_xticks(x)
ax5.set_xticklabels([f'S{s}' for s in season_results.index], fontsize=9)
ax5.legend(loc='upper right', fontsize=8, framealpha=0.9)
ax5.tick_params(axis='y', which='major', labelsize=9)

# -----------------------------------------------------------------------------
# Gráfica 6: BARRAS VERTICALES AGRUPADAS - Estadísticas por Rol
# -----------------------------------------------------------------------------
ax6 = fig.add_subplot(gs[2, 0])

role_data = df[df['Role 1'].notna()].groupby('Role 1').agg({
    'Elim': 'mean',
    'Death': 'mean'
}).round(2)

x = np.arange(len(role_data))
width = 0.35

bars1 = ax6.bar(x - width/2, role_data['Elim'], width, label='Eliminaciones', 
                color=COLORS['secondary'], edgecolor='white')
bars2 = ax6.bar(x + width/2, role_data['Death'], width, label='Muertes', 
                color=COLORS['loss'], edgecolor='white')

ax6.set_xlabel('Rol', fontsize=10, fontweight='bold')
ax6.set_ylabel('Promedio', fontsize=10, fontweight='bold')
ax6.set_title('Barras Agrupadas: Elim/Muertes por Rol', fontsize=11, fontweight='bold', pad=10)
ax6.set_xticks(x)
ax6.set_xticklabels(role_data.index, fontsize=9)
ax6.legend(loc='upper right', fontsize=8, framealpha=0.9)

# Añadir valores sobre las barras
for bar in bars1:
    height = bar.get_height()
    ax6.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}',
             ha='center', va='bottom', fontsize=8)

# -----------------------------------------------------------------------------
# Gráfica 7: SCATTER con tamaño variable - Rendimiento vs Medallas
# -----------------------------------------------------------------------------
ax7 = fig.add_subplot(gs[2, 1])

medal_data = df[df['Dmg'].notna() & df['Gold medals'].notna()].copy()
sizes = (medal_data['Gold medals'] + 1) * 30

scatter2 = ax7.scatter(medal_data['Dmg'], medal_data['Heal'], 
                       s=sizes, alpha=0.5,
                       c=medal_data['Gold medals'], cmap='YlOrRd',
                       edgecolors='white', linewidth=0.5)

ax7.set_xlabel('Daño', fontsize=10, fontweight='bold')
ax7.set_ylabel('Curación', fontsize=10, fontweight='bold')
ax7.set_title('Scatter: Daño vs Curación\n(Tamaño = Medallas Oro)', fontsize=11, fontweight='bold', pad=10)

cbar = plt.colorbar(scatter2, ax=ax7, shrink=0.8)
cbar.set_label('Medallas de Oro', fontsize=9)
ax7.tick_params(axis='both', which='major', labelsize=9)

# -----------------------------------------------------------------------------
# Gráfica 8: BARRAS - Impacto de rachas
# -----------------------------------------------------------------------------
ax8 = fig.add_subplot(gs[2, 2])

streak_data = df[df['SR Change'].notna()].groupby('Streak')['SR Change'].mean().round(2)
streak_data = streak_data.sort_index()

colors_streak = [COLORS['win'] if s > 0 else COLORS['loss'] for s in streak_data.index]

ax8.bar(streak_data.index.astype(str), streak_data.values, color=colors_streak, 
        edgecolor='white', linewidth=0.5)
ax8.set_xlabel('Racha', fontsize=10, fontweight='bold')
ax8.set_ylabel('SR Change Promedio', fontsize=10, fontweight='bold')
ax8.set_title('Barras: SR Change por Racha', fontsize=11, fontweight='bold', pad=10)
ax8.axhline(y=0, color='gray', linestyle='-', linewidth=1)
ax8.tick_params(axis='x', which='major', labelsize=8, rotation=45)
ax8.tick_params(axis='y', which='major', labelsize=9)

# Guardar figura
plt.savefig('/home/claude/overwatch_analysis/images/01_dashboard_principal.png', 
            dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("✓ Dashboard Principal guardado: images/01_dashboard_principal.png")

# =============================================================================
# FIGURA 2: MAPA DE PIXELES (HEATMAP) - Matriz de correlaciones
# =============================================================================

fig2, ax = plt.subplots(figsize=(10, 8))

# Preparar datos para heatmap
numeric_cols = ['SR Change', 'Elim', 'Death', 'Heal', 'Dmg', 'Gold medals', 'Silver medals', 'Bronze medals']
corr_matrix = df[numeric_cols].corr()

# Crear heatmap manual (mapa de pixeles)
im = ax.imshow(corr_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)

# Configuración de ejes
ax.set_xticks(np.arange(len(numeric_cols)))
ax.set_yticks(np.arange(len(numeric_cols)))
ax.set_xticklabels(numeric_cols, rotation=45, ha='right', fontsize=10)
ax.set_yticklabels(numeric_cols, fontsize=10)

# Añadir valores en cada celda
for i in range(len(numeric_cols)):
    for j in range(len(numeric_cols)):
        text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                       ha='center', va='center', color='black' if abs(corr_matrix.iloc[i, j]) < 0.5 else 'white',
                       fontsize=9, fontweight='bold')

# Colorbar
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Correlación', fontsize=11, fontweight='bold')

ax.set_title('Mapa de Pixeles: Matriz de Correlaciones\nEntre Variables de Rendimiento', 
             fontsize=14, fontweight='bold', pad=15)

plt.savefig('/home/claude/overwatch_analysis/images/02_heatmap_correlaciones.png', 
            dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("✓ Heatmap de Correlaciones guardado: images/02_heatmap_correlaciones.png")

# =============================================================================
# FIGURA 3: DASHBOARD DE MODO DE JUEGO
# =============================================================================

fig3, axes = plt.subplots(2, 2, figsize=(14, 10))
fig3.suptitle('Análisis por Modo de Juego', fontsize=16, fontweight='bold', y=0.98)

mode_data = df[df['Mode'].notna()]

# Gráfica 1: Winrate por modo
ax_mode1 = axes[0, 0]
mode_winrate = mode_data.groupby('Mode').apply(lambda x: (x['Result'] == 'Win').sum() / len(x) * 100)
colors_mode = ['#E91E63', '#9C27B0', '#3F51B5', '#00BCD4']
bars = ax_mode1.bar(mode_winrate.index, mode_winrate.values, color=colors_mode, edgecolor='white')
ax_mode1.set_ylabel('Winrate (%)', fontweight='bold')
ax_mode1.set_title('Winrate por Modo de Juego', fontweight='bold')
ax_mode1.axhline(y=50, color='gray', linestyle='--', linewidth=1.5)
ax_mode1.tick_params(axis='x', rotation=15)
for bar, val in zip(bars, mode_winrate.values):
    ax_mode1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.1f}%', 
                  ha='center', fontsize=10, fontweight='bold')

# Gráfica 2: Distribución de partidas por modo
ax_mode2 = axes[0, 1]
mode_counts = mode_data['Mode'].value_counts()
ax_mode2.pie(mode_counts, labels=mode_counts.index, autopct='%1.1f%%', colors=colors_mode,
             startangle=90, explode=[0.02]*len(mode_counts))
ax_mode2.set_title('Distribución de Partidas por Modo', fontweight='bold')

# Gráfica 3: SR Change promedio por modo
ax_mode3 = axes[1, 0]
mode_sr = mode_data.groupby('Mode')['SR Change'].mean()
colors_sr = [COLORS['win'] if sr > 0 else COLORS['loss'] for sr in mode_sr.values]
bars = ax_mode3.bar(mode_sr.index, mode_sr.values, color=colors_sr, edgecolor='white')
ax_mode3.set_ylabel('SR Change Promedio', fontweight='bold')
ax_mode3.set_title('SR Change Promedio por Modo', fontweight='bold')
ax_mode3.axhline(y=0, color='gray', linestyle='-', linewidth=1)
ax_mode3.tick_params(axis='x', rotation=15)

# Gráfica 4: Boxplot de rendimiento por modo
ax_mode4 = axes[1, 1]
mode_elim = [mode_data[mode_data['Mode'] == mode]['Elim'].dropna().values for mode in mode_data['Mode'].unique()]
bp = ax_mode4.boxplot(mode_elim, labels=mode_data['Mode'].unique(), patch_artist=True)
for patch, color in zip(bp['boxes'], colors_mode):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax_mode4.set_ylabel('Eliminaciones', fontweight='bold')
ax_mode4.set_title('Distribución de Eliminaciones por Modo', fontweight='bold')
ax_mode4.tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig('/home/claude/overwatch_analysis/images/03_dashboard_modos.png', 
            dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("✓ Dashboard de Modos guardado: images/03_dashboard_modos.png")

print("\n¡Todas las gráficas de Matplotlib generadas exitosamente!")
