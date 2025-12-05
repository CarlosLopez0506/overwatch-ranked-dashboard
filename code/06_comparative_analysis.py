"""
06_comparative_analysis.py
==========================
Análisis comparativo completo: variables y categorías
Incluye comparaciones entre temporadas, roles, mapas y rendimiento

Dataset: Overwatch Competitive Seasons (all_seasons.csv)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración
plt.style.use('seaborn-v0_8-whitegrid')

# =============================================================================
# CARGA DE DATOS
# =============================================================================

df = pd.read_csv('/mnt/user-data/uploads/all_seasons__1_.csv')
df['Start SR Numeric'] = pd.to_numeric(df['Start SR'], errors='coerce')
df['End SR Numeric'] = pd.to_numeric(df['End SR'], errors='coerce')
df['SR Change'] = pd.to_numeric(df['SR Change'], errors='coerce')

# =============================================================================
# FIGURA 1: COMPARATIVA ENTRE TEMPORADAS
# =============================================================================

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Análisis Comparativo: Evolución entre Temporadas', fontsize=16, fontweight='bold', y=1.02)

seasons = sorted(df['season'].unique())
colors = ['#E91E63', '#9C27B0', '#3F51B5', '#00BCD4']

# 1. Winrate por temporada
ax1 = axes[0, 0]
winrates = [df[df['season'] == s]['Result'].apply(lambda x: x == 'Win').mean() * 100 for s in seasons]
bars = ax1.bar([f'S{s}' for s in seasons], winrates, color=colors)
ax1.axhline(y=50, color='gray', linestyle='--', linewidth=2)
ax1.set_ylabel('Winrate (%)', fontweight='bold')
ax1.set_title('Winrate por Temporada', fontweight='bold')
for bar, wr in zip(bars, winrates):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{wr:.1f}%', 
             ha='center', fontsize=10, fontweight='bold')
ax1.set_ylim(0, 70)

# 2. Partidas jugadas por temporada
ax2 = axes[0, 1]
partidas = [len(df[df['season'] == s]) for s in seasons]
bars = ax2.bar([f'S{s}' for s in seasons], partidas, color=colors)
ax2.set_ylabel('Número de Partidas', fontweight='bold')
ax2.set_title('Partidas Jugadas por Temporada', fontweight='bold')
for bar, p in zip(bars, partidas):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(p), 
             ha='center', fontsize=10, fontweight='bold')

# 3. SR Range por temporada
ax3 = axes[0, 2]
for i, s in enumerate(seasons):
    season_data = df[df['season'] == s]
    sr_start = pd.to_numeric(season_data['Start SR'].iloc[0], errors='coerce')
    sr_end = pd.to_numeric(season_data['End SR'].iloc[-1], errors='coerce')
    sr_max = season_data['End SR Numeric'].max()
    sr_min = season_data['End SR Numeric'].min()
    
    if pd.notna(sr_min) and pd.notna(sr_max):
        ax3.barh(f'S{s}', sr_max - sr_min, left=sr_min, color=colors[i], alpha=0.7)
        ax3.scatter([sr_start, sr_end], [f'S{s}', f'S{s}'], color=['green', 'red'], s=100, zorder=5)

ax3.set_xlabel('Skill Rating (SR)', fontweight='bold')
ax3.set_title('Rango de SR por Temporada\n(Verde=Inicio, Rojo=Final)', fontweight='bold')
ax3.axvline(x=2500, color='gold', linestyle='--', alpha=0.5)

# 4. Promedio de medallas por temporada
ax4 = axes[1, 0]
medal_data = []
for s in seasons:
    season_medals = df[df['season'] == s][['Gold medals', 'Silver medals', 'Bronze medals']].mean()
    medal_data.append(season_medals)

medal_df = pd.DataFrame(medal_data, index=[f'S{s}' for s in seasons])
medal_df.plot(kind='bar', ax=ax4, color=['#FFD700', '#C0C0C0', '#CD7F32'], width=0.7)
ax4.set_ylabel('Promedio de Medallas', fontweight='bold')
ax4.set_title('Medallas Promedio por Temporada', fontweight='bold')
ax4.tick_params(axis='x', rotation=0)
ax4.legend(loc='upper right', fontsize=8)

# 5. K/D Ratio por temporada (temporadas con datos)
ax5 = axes[1, 1]
kd_data = []
for s in [9, 10]:  # Solo temporadas con datos de K/D
    season_data = df[df['season'] == s]
    avg_elim = season_data['Elim'].mean()
    avg_death = season_data['Death'].mean()
    if pd.notna(avg_elim) and pd.notna(avg_death) and avg_death > 0:
        kd_data.append({'Season': f'S{s}', 'Elim': avg_elim, 'Death': avg_death, 'K/D': avg_elim/avg_death})

if kd_data:
    kd_df = pd.DataFrame(kd_data)
    x = np.arange(len(kd_df))
    width = 0.35
    bars1 = ax5.bar(x - width/2, kd_df['Elim'], width, label='Eliminaciones', color='#4CAF50')
    bars2 = ax5.bar(x + width/2, kd_df['Death'], width, label='Muertes', color='#F44336')
    ax5.set_xticks(x)
    ax5.set_xticklabels(kd_df['Season'])
    ax5.set_ylabel('Promedio', fontweight='bold')
    ax5.set_title('Eliminaciones vs Muertes (S9-S10)', fontweight='bold')
    ax5.legend()

# 6. Tendencia de rachas
ax6 = axes[1, 2]
for i, s in enumerate(seasons):
    season_data = df[df['season'] == s].copy()
    season_data = season_data.sort_values('Game #')
    ax6.plot(range(len(season_data)), season_data['Streak'].cumsum(), 
             label=f'S{s}', color=colors[i], linewidth=2)

ax6.set_xlabel('Número de Partida', fontweight='bold')
ax6.set_ylabel('Racha Acumulada', fontweight='bold')
ax6.set_title('Tendencia de Rachas Acumuladas', fontweight='bold')
ax6.axhline(y=0, color='gray', linestyle='-', linewidth=1)
ax6.legend()

plt.tight_layout()
plt.savefig('/home/claude/overwatch_analysis/images/13_comparative_seasons.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Comparativa de Temporadas guardada: images/13_comparative_seasons.png")

# =============================================================================
# FIGURA 2: COMPARATIVA ENTRE ROLES
# =============================================================================

fig2, axes2 = plt.subplots(2, 2, figsize=(14, 12))
fig2.suptitle('Análisis Comparativo: Rendimiento por Rol', fontsize=16, fontweight='bold', y=1.02)

role_data = df[df['Role 1'].notna()]
roles = ['Tank', 'Support', 'Offense', 'Defense']
role_colors = {'Tank': '#2196F3', 'Support': '#4CAF50', 'Offense': '#F44336', 'Defense': '#9C27B0'}

# 1. Radar de rendimiento por rol
ax1 = axes2[0, 0]
metrics = ['Winrate', 'Elim', 'Death', 'Heal', 'Dmg']
role_metrics = []

for role in roles:
    role_subset = role_data[role_data['Role 1'] == role]
    winrate = (role_subset['Result'] == 'Win').mean() * 100
    elim = role_subset['Elim'].mean() / 60 * 100 if role_subset['Elim'].mean() > 0 else 0  # Normalizado
    death = (1 - role_subset['Death'].mean() / 20) * 100 if role_subset['Death'].mean() > 0 else 0  # Invertido
    heal = role_subset['Heal'].mean() / 150 if role_subset['Heal'].mean() > 0 else 0
    dmg = role_subset['Dmg'].mean() / 120 if role_subset['Dmg'].mean() > 0 else 0
    role_metrics.append([winrate, elim, death, heal, dmg])

# Barras agrupadas
x = np.arange(len(roles))
width = 0.15
metrics_labels = ['Winrate%', 'Elim*', 'Surviv*', 'Heal*', 'Dmg*']

for i, (metric, label) in enumerate(zip(np.array(role_metrics).T, metrics_labels)):
    ax1.bar(x + i*width, metric, width, label=label)

ax1.set_xticks(x + width*2)
ax1.set_xticklabels(roles)
ax1.set_ylabel('Valor (normalizado)', fontweight='bold')
ax1.set_title('Métricas de Rendimiento por Rol\n(*valores normalizados)', fontweight='bold')
ax1.legend(loc='upper right', fontsize=8)

# 2. Distribución de partidas por rol
ax2 = axes2[0, 1]
role_counts = role_data['Role 1'].value_counts()
ax2.pie(role_counts, labels=role_counts.index, autopct='%1.1f%%', 
        colors=[role_colors.get(r, '#999') for r in role_counts.index],
        explode=[0.02]*len(role_counts), startangle=90)
ax2.set_title('Distribución de Partidas por Rol', fontweight='bold')

# 3. SR Change por rol
ax3 = axes2[1, 0]
role_sr = role_data.groupby('Role 1')['SR Change'].agg(['mean', 'std'])
x = np.arange(len(role_sr))
bars = ax3.bar(x, role_sr['mean'], yerr=role_sr['std'], 
               color=[role_colors.get(r, '#999') for r in role_sr.index],
               capsize=5, edgecolor='white')
ax3.set_xticks(x)
ax3.set_xticklabels(role_sr.index)
ax3.axhline(y=0, color='gray', linestyle='-', linewidth=1)
ax3.set_ylabel('SR Change Promedio', fontweight='bold')
ax3.set_title('SR Change por Rol (con Desv. Estándar)', fontweight='bold')

# 4. Boxplot de rendimiento
ax4 = axes2[1, 1]
role_data_melt = role_data.melt(id_vars=['Role 1'], value_vars=['Elim', 'Death'],
                                 var_name='Métrica', value_name='Valor')
sns.boxplot(data=role_data_melt, x='Role 1', y='Valor', hue='Métrica', ax=ax4,
            palette=['#4CAF50', '#F44336'])
ax4.set_title('Distribución de Elim/Death por Rol', fontweight='bold')
ax4.tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig('/home/claude/overwatch_analysis/images/14_comparative_roles.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Comparativa de Roles guardada: images/14_comparative_roles.png")

# =============================================================================
# FIGURA 3: TABLA RESUMEN COMPLETA
# =============================================================================

fig3, ax = plt.subplots(figsize=(14, 8))
ax.axis('off')

# Crear tabla resumen
summary_data = []
for s in seasons:
    season_data = df[df['season'] == s]
    wins = (season_data['Result'] == 'Win').sum()
    losses = (season_data['Result'] == 'Loss').sum()
    draws = (season_data['Result'] == 'Draw').sum()
    total = len(season_data)
    winrate = wins / total * 100 if total > 0 else 0
    
    sr_start = pd.to_numeric(season_data['Start SR'].iloc[0], errors='coerce')
    sr_end = pd.to_numeric(season_data['End SR'].iloc[-1], errors='coerce')
    sr_change = sr_end - sr_start if pd.notna(sr_start) and pd.notna(sr_end) else 'N/A'
    
    avg_elim = season_data['Elim'].mean()
    avg_death = season_data['Death'].mean()
    kd = avg_elim / avg_death if pd.notna(avg_elim) and pd.notna(avg_death) and avg_death > 0 else 'N/A'
    
    summary_data.append([
        f'Temporada {s}',
        total,
        wins,
        losses,
        draws,
        f'{winrate:.1f}%',
        f'{sr_start:.0f}' if pd.notna(sr_start) else 'N/A',
        f'{sr_end:.0f}' if pd.notna(sr_end) else 'N/A',
        f'{sr_change:+.0f}' if isinstance(sr_change, (int, float)) else sr_change,
        f'{kd:.2f}' if isinstance(kd, float) else kd
    ])

columns = ['Temporada', 'Partidas', 'Victorias', 'Derrotas', 'Empates', 
           'Winrate', 'SR Inicial', 'SR Final', 'Δ SR', 'K/D']

table = ax.table(cellText=summary_data, colLabels=columns,
                 cellLoc='center', loc='center',
                 colColours=['#E3F2FD']*len(columns))

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 2)

# Colorear celdas según winrate
for i, row in enumerate(summary_data):
    winrate_val = float(row[5].replace('%', ''))
    if winrate_val >= 50:
        table[(i+1, 5)].set_facecolor('#C8E6C9')
    else:
        table[(i+1, 5)].set_facecolor('#FFCDD2')

ax.set_title('Tabla Resumen: Estadísticas por Temporada', fontsize=16, fontweight='bold', pad=20)

plt.savefig('/home/claude/overwatch_analysis/images/15_summary_table.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Tabla Resumen guardada: images/15_summary_table.png")

# =============================================================================
# GUARDAR DATOS PROCESADOS PARA EL REPORTE
# =============================================================================

# Estadísticas generales
total_games = len(df)
total_wins = (df['Result'] == 'Win').sum()
total_losses = (df['Result'] == 'Loss').sum()
total_draws = (df['Result'] == 'Draw').sum()
overall_winrate = total_wins / total_games * 100

general_stats = {
    'Total Partidas': total_games,
    'Victorias': total_wins,
    'Derrotas': total_losses,
    'Empates': total_draws,
    'Winrate General': f'{overall_winrate:.1f}%',
    'Temporadas Analizadas': len(seasons),
    'Mapas Únicos': df['Map'].nunique(),
    'SR Promedio Change': f'{df["SR Change"].mean():.2f}'
}

stats_df = pd.DataFrame([general_stats]).T
stats_df.columns = ['Valor']
stats_df.to_csv('/home/claude/overwatch_analysis/data_general_stats.csv')

print("✓ Estadísticas generales guardadas: data_general_stats.csv")
print("\n¡Análisis comparativo completado!")
