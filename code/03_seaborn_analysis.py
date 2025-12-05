"""
03_seaborn_analysis.py
======================
Análisis y visualización avanzada con Seaborn
Incluye: distribuciones, violinplots, jointplots, pairplots, regplots

Dataset: Overwatch Competitive Seasons (all_seasons.csv)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de estilo Seaborn
sns.set_theme(style="whitegrid", palette="husl")
sns.set_context("notebook", font_scale=1.1)

# =============================================================================
# CARGA DE DATOS
# =============================================================================

df = pd.read_csv('/mnt/user-data/uploads/all_seasons__1_.csv')
df['Start SR Numeric'] = pd.to_numeric(df['Start SR'], errors='coerce')
df['End SR Numeric'] = pd.to_numeric(df['End SR'], errors='coerce')
df['SR Change'] = pd.to_numeric(df['SR Change'], errors='coerce')

# Paleta de colores
result_palette = {'Win': '#4CAF50', 'Loss': '#F44336', 'Draw': '#FFC107'}
role_palette = {'Tank': '#2196F3', 'Support': '#4CAF50', 'Offense': '#F44336', 'Defense': '#9C27B0'}

# =============================================================================
# FIGURA 1: DASHBOARD SEABORN - DISTRIBUCIONES
# =============================================================================

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Seaborn: Análisis de Distribuciones', fontsize=16, fontweight='bold', y=1.02)

# 1. KDE Plot - Distribución de SR Change por resultado
ax1 = axes[0, 0]
for result in ['Win', 'Loss']:
    data = df[df['Result'] == result]['SR Change'].dropna()
    sns.kdeplot(data=data, ax=ax1, label=result, fill=True, alpha=0.4, color=result_palette[result])
ax1.set_title('KDE: Distribución SR Change por Resultado', fontweight='bold')
ax1.set_xlabel('SR Change')
ax1.legend()
ax1.axvline(x=0, color='gray', linestyle='--', alpha=0.7)

# 2. Histogram - Distribución de Eliminaciones
ax2 = axes[0, 1]
sns.histplot(data=df, x='Elim', hue='Result', palette=result_palette, ax=ax2, 
             kde=True, alpha=0.6, bins=20)
ax2.set_title('Histograma: Eliminaciones por Resultado', fontweight='bold')
ax2.set_xlabel('Eliminaciones')

# 3. Box Plot - SR Change por temporada
ax3 = axes[0, 2]
sns.boxplot(data=df, x='season', y='SR Change', palette='Set2', ax=ax3)
ax3.set_title('Boxplot: SR Change por Temporada', fontweight='bold')
ax3.set_xlabel('Temporada')
ax3.axhline(y=0, color='gray', linestyle='--', alpha=0.7)

# 4. Violin Plot - Eliminaciones por rol
ax4 = axes[1, 0]
role_data = df[df['Role 1'].notna()]
sns.violinplot(data=role_data, x='Role 1', y='Elim', palette=role_palette, ax=ax4, 
               inner='box', cut=0)
ax4.set_title('Violinplot: Eliminaciones por Rol', fontweight='bold')
ax4.set_xlabel('Rol')
ax4.tick_params(axis='x', rotation=15)

# 5. Swarm Plot - Muertes por resultado
ax5 = axes[1, 1]
sample_data = df.dropna(subset=['Death']).sample(min(150, len(df.dropna(subset=['Death']))))
sns.swarmplot(data=sample_data, x='Result', y='Death', palette=result_palette, ax=ax5, size=4, alpha=0.7)
ax5.set_title('Swarmplot: Muertes por Resultado (muestra)', fontweight='bold')
ax5.set_xlabel('Resultado')

# 6. Strip Plot - Gold medals por modo
ax6 = axes[1, 2]
mode_data = df[df['Mode'].notna()]
sns.stripplot(data=mode_data, x='Mode', y='Gold medals', hue='Result', 
              palette=result_palette, ax=ax6, dodge=True, alpha=0.6, jitter=True)
ax6.set_title('Stripplot: Medallas Oro por Modo', fontweight='bold')
ax6.tick_params(axis='x', rotation=15)
ax6.legend(loc='upper right', fontsize=8)

plt.tight_layout()
plt.savefig('/home/claude/overwatch_analysis/images/04_seaborn_distribuciones.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Seaborn Distribuciones guardado: images/04_seaborn_distribuciones.png")

# =============================================================================
# FIGURA 2: SEABORN - RELACIONES Y REGRESIONES
# =============================================================================

fig2, axes2 = plt.subplots(2, 2, figsize=(14, 12))
fig2.suptitle('Seaborn: Análisis de Relaciones', fontsize=16, fontweight='bold', y=1.02)

# 1. Regplot - Eliminaciones vs SR Change
ax1 = axes2[0, 0]
valid_data = df.dropna(subset=['Elim', 'SR Change'])
sns.regplot(data=valid_data, x='Elim', y='SR Change', ax=ax1, 
            scatter_kws={'alpha': 0.4, 'color': '#2196F3'}, 
            line_kws={'color': '#F44336', 'linewidth': 2})
ax1.set_title('Regplot: Eliminaciones vs SR Change', fontweight='bold')
ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

# 2. Lmplot simulado - Por resultado
ax2 = axes2[0, 1]
for result in ['Win', 'Loss']:
    result_data = df[df['Result'] == result].dropna(subset=['Death', 'Elim'])
    sns.regplot(data=result_data, x='Death', y='Elim', ax=ax2,
                scatter_kws={'alpha': 0.4}, label=result, color=result_palette[result],
                line_kws={'linewidth': 2})
ax2.set_title('Regplot: Muertes vs Eliminaciones por Resultado', fontweight='bold')
ax2.legend()

# 3. Heatmap - Rendimiento por rol y resultado
ax3 = axes2[1, 0]
role_result_elim = df.pivot_table(values='Elim', index='Role 1', columns='Result', aggfunc='mean')
sns.heatmap(role_result_elim, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax3,
            linewidths=0.5, cbar_kws={'label': 'Eliminaciones Promedio'})
ax3.set_title('Heatmap: Eliminaciones por Rol y Resultado', fontweight='bold')

# 4. Heatmap - Rendimiento por modo y resultado
ax4 = axes2[1, 1]
mode_result_sr = df.pivot_table(values='SR Change', index='Mode', columns='Result', aggfunc='mean')
sns.heatmap(mode_result_sr, annot=True, fmt='.1f', cmap='RdBu_r', center=0, ax=ax4,
            linewidths=0.5, cbar_kws={'label': 'SR Change Promedio'})
ax4.set_title('Heatmap: SR Change por Modo y Resultado', fontweight='bold')

plt.tight_layout()
plt.savefig('/home/claude/overwatch_analysis/images/05_seaborn_relaciones.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Seaborn Relaciones guardado: images/05_seaborn_relaciones.png")

# =============================================================================
# FIGURA 3: PAIRPLOT - ANÁLISIS MULTIVARIABLE
# =============================================================================

# Seleccionar columnas para pairplot
pair_cols = ['SR Change', 'Elim', 'Death', 'Dmg', 'Result']
pair_data = df[pair_cols].dropna()

# Limitar muestra para rendimiento
if len(pair_data) > 200:
    pair_data = pair_data.sample(200, random_state=42)

g = sns.pairplot(pair_data, hue='Result', palette=result_palette, 
                 diag_kind='kde', plot_kws={'alpha': 0.6, 's': 30},
                 height=2.5, aspect=1)
g.fig.suptitle('Pairplot: Relaciones Multivariables', fontsize=14, fontweight='bold', y=1.02)

plt.savefig('/home/claude/overwatch_analysis/images/06_seaborn_pairplot.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Seaborn Pairplot guardado: images/06_seaborn_pairplot.png")

# =============================================================================
# FIGURA 4: FACETGRID - ANÁLISIS POR CATEGORÍAS
# =============================================================================

# FacetGrid: SR Change por temporada y resultado
facet_data = df[df['season'].isin([9, 10])].dropna(subset=['SR Change'])

g = sns.FacetGrid(facet_data, col='season', hue='Result', palette=result_palette,
                  height=5, aspect=1.2)
g.map(sns.histplot, 'SR Change', kde=True, alpha=0.6, bins=15)
g.add_legend()
g.fig.suptitle('FacetGrid: Distribución SR Change por Temporada y Resultado', 
               fontsize=14, fontweight='bold', y=1.05)

plt.savefig('/home/claude/overwatch_analysis/images/07_seaborn_facetgrid.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Seaborn FacetGrid guardado: images/07_seaborn_facetgrid.png")

# =============================================================================
# FIGURA 5: CATPLOT - ANÁLISIS CATEGÓRICO COMPLETO
# =============================================================================

fig5, axes5 = plt.subplots(1, 2, figsize=(14, 6))
fig5.suptitle('Seaborn: Análisis Categórico', fontsize=14, fontweight='bold', y=1.02)

# 1. Count plot - Partidas por mapa y resultado
ax1 = axes5[0]
map_result = df[df['Map'].notna()].copy()
map_order = map_result['Map'].value_counts().head(10).index
sns.countplot(data=map_result[map_result['Map'].isin(map_order)], 
              y='Map', hue='Result', palette=result_palette, ax=ax1, order=map_order)
ax1.set_title('Countplot: Partidas por Mapa (Top 10)', fontweight='bold')
ax1.legend(loc='lower right')

# 2. Bar plot - Promedio de rendimiento por rol
ax2 = axes5[1]
role_perf = df[df['Role 1'].notna()].melt(id_vars=['Role 1'], 
                                           value_vars=['Elim', 'Death'], 
                                           var_name='Métrica', value_name='Valor')
sns.barplot(data=role_perf, x='Role 1', y='Valor', hue='Métrica', 
            palette=['#2196F3', '#F44336'], ax=ax2)
ax2.set_title('Barplot: Rendimiento Promedio por Rol', fontweight='bold')
ax2.tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig('/home/claude/overwatch_analysis/images/08_seaborn_catplot.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("✓ Seaborn Catplot guardado: images/08_seaborn_catplot.png")

print("\n¡Todas las gráficas de Seaborn generadas exitosamente!")
