"""
04_animated_chart.py
====================
Gráfica animada: Evolución del SR a lo largo de las partidas
Genera un GIF animado mostrando la progresión del jugador

Dataset: Overwatch Competitive Seasons (all_seasons.csv)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CARGA DE DATOS
# =============================================================================

df = pd.read_csv('/mnt/user-data/uploads/all_seasons__1_.csv')
df['End SR Numeric'] = pd.to_numeric(df['End SR'], errors='coerce')

# Preparar datos para la animación - usar temporada 10
season_10 = df[df['season'] == 10].copy()
season_10 = season_10.sort_values('Game #').reset_index(drop=True)
season_10['End SR Numeric'] = pd.to_numeric(season_10['End SR'], errors='coerce')
season_10 = season_10[season_10['End SR Numeric'].notna()].reset_index(drop=True)

# =============================================================================
# CREAR ANIMACIÓN
# =============================================================================

fig, ax = plt.subplots(figsize=(12, 6))

# Configuración inicial
ax.set_xlim(0, len(season_10) + 5)
sr_min = season_10['End SR Numeric'].min() - 100
sr_max = season_10['End SR Numeric'].max() + 100
ax.set_ylim(sr_min, sr_max)

ax.set_xlabel('Número de Partida', fontsize=12, fontweight='bold')
ax.set_ylabel('SR (Skill Rating)', fontsize=12, fontweight='bold')
ax.set_title('Temporada 10: Evolución del SR\n(Animación)', fontsize=14, fontweight='bold')

# Líneas de referencia para rangos
ax.axhline(y=2500, color='gold', linestyle='--', alpha=0.5, label='Platino')
ax.axhline(y=3000, color='#C0C0C0', linestyle='--', alpha=0.5, label='Diamante')
ax.fill_between([0, len(season_10) + 5], 2000, 2500, alpha=0.1, color='gold')
ax.fill_between([0, len(season_10) + 5], 2500, 3000, alpha=0.1, color='silver')

# Elementos a animar
line, = ax.plot([], [], 'b-', linewidth=2, label='SR')
point, = ax.plot([], [], 'ro', markersize=10)
sr_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, 
                  fontweight='bold', verticalalignment='top',
                  bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Datos para la animación
x_data = []
y_data = []

def init():
    line.set_data([], [])
    point.set_data([], [])
    sr_text.set_text('')
    return line, point, sr_text

def animate(frame):
    if frame < len(season_10):
        x_data.append(frame + 1)
        y_data.append(season_10.iloc[frame]['End SR Numeric'])
        
        line.set_data(x_data, y_data)
        point.set_data([frame + 1], [season_10.iloc[frame]['End SR Numeric']])
        
        current_sr = int(season_10.iloc[frame]['End SR Numeric'])
        result = season_10.iloc[frame]['Result']
        
        # Color del punto según resultado
        if result == 'Win':
            point.set_color('green')
        elif result == 'Loss':
            point.set_color('red')
        else:
            point.set_color('yellow')
        
        sr_text.set_text(f'Partida: {frame + 1}\nSR: {current_sr}\nResultado: {result}')
    
    return line, point, sr_text

# Crear animación
anim = animation.FuncAnimation(fig, animate, init_func=init, 
                               frames=len(season_10) + 10, 
                               interval=100, blit=True, repeat=False)

ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)

# Guardar como GIF
print("Generando animación... (esto puede tomar unos segundos)")
anim.save('/home/claude/overwatch_analysis/images/09_animated_sr_evolution.gif', 
          writer='pillow', fps=10)
plt.close()

print("✓ Animación guardada: images/09_animated_sr_evolution.gif")

# =============================================================================
# CREAR IMAGEN ESTÁTICA DEL FRAME FINAL PARA EL REPORTE
# =============================================================================

fig2, ax2 = plt.subplots(figsize=(12, 6))

# Datos completos
x_full = list(range(1, len(season_10) + 1))
y_full = season_10['End SR Numeric'].tolist()

# Colores por resultado
colors = ['#4CAF50' if r == 'Win' else '#F44336' if r == 'Loss' else '#FFC107' 
          for r in season_10['Result']]

# Gráfica de línea
ax2.plot(x_full, y_full, 'b-', linewidth=1.5, alpha=0.7, label='Evolución SR')
ax2.scatter(x_full, y_full, c=colors, s=50, zorder=5, edgecolors='white', linewidth=0.5)

# Configuración
ax2.set_xlim(0, len(season_10) + 5)
ax2.set_ylim(sr_min, sr_max)
ax2.set_xlabel('Número de Partida', fontsize=12, fontweight='bold')
ax2.set_ylabel('SR (Skill Rating)', fontsize=12, fontweight='bold')
ax2.set_title('Temporada 10: Evolución Completa del SR', fontsize=14, fontweight='bold')

# Líneas de referencia
ax2.axhline(y=2500, color='gold', linestyle='--', alpha=0.5, linewidth=2)
ax2.axhline(y=3000, color='#C0C0C0', linestyle='--', alpha=0.5, linewidth=2)
ax2.fill_between([0, len(season_10) + 5], 2000, 2500, alpha=0.1, color='gold', label='Platino')
ax2.fill_between([0, len(season_10) + 5], 2500, 3000, alpha=0.1, color='silver', label='Diamante')

# Estadísticas
sr_inicio = y_full[0]
sr_final = y_full[-1]
sr_max_val = max(y_full)
sr_min_val = min(y_full)

stats_text = f'SR Inicial: {int(sr_inicio)}\nSR Final: {int(sr_final)}\n'
stats_text += f'SR Máximo: {int(sr_max_val)}\nSR Mínimo: {int(sr_min_val)}'
ax2.text(0.02, 0.95, stats_text, transform=ax2.transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Leyenda personalizada
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#4CAF50', label='Victoria'),
    Patch(facecolor='#F44336', label='Derrota'),
    Patch(facecolor='#FFC107', label='Empate'),
]
ax2.legend(handles=legend_elements, loc='lower right', fontsize=9)

ax2.grid(True, alpha=0.3)

plt.savefig('/home/claude/overwatch_analysis/images/09b_sr_evolution_static.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Imagen estática guardada: images/09b_sr_evolution_static.png")
print("\n¡Gráficas animadas generadas exitosamente!")
