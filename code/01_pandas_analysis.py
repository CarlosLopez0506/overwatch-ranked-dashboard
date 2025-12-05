"""
01_pandas_analysis.py
=====================
Análisis de datos con Pandas: Series y DataFrames
Este script demuestra el uso de estructuras de datos fundamentales de Pandas
para el análisis del dataset de Overwatch Competitive.

Autor: Análisis de Datos - Curso
Dataset: Overwatch Competitive Seasons (all_seasons.csv)
"""

import pandas as pd
import numpy as np

# =============================================================================
# CARGA Y PREPARACIÓN DE DATOS
# =============================================================================

# Cargar el dataset
df = pd.read_csv('/mnt/user-data/uploads/all_seasons__1_.csv')

# Convertir columnas SR a numérico (tienen valores 'P' para placement)
df['Start SR Numeric'] = pd.to_numeric(df['Start SR'], errors='coerce')
df['End SR Numeric'] = pd.to_numeric(df['End SR'], errors='coerce')
df['Team SR avg Numeric'] = pd.to_numeric(df['Team SR avg'], errors='coerce')
df['Enemy SR avg Numeric'] = pd.to_numeric(df['Enemy SR avg'], errors='coerce')

# =============================================================================
# ANÁLISIS CON SERIES
# =============================================================================

print("=" * 60)
print("ANÁLISIS CON PANDAS SERIES")
print("=" * 60)

# Serie 1: Resultados de partidas
results_series = df['Result']
print("\n1. Serie de Resultados:")
print(f"   Tipo: {type(results_series)}")
print(f"   Longitud: {len(results_series)}")
print(f"   Conteo de valores:")
print(results_series.value_counts())

# Serie 2: SR Changes
sr_changes = df['SR Change'].dropna()
print("\n2. Serie de Cambios de SR:")
print(f"   Media: {sr_changes.mean():.2f}")
print(f"   Mediana: {sr_changes.median():.2f}")
print(f"   Desv. Estándar: {sr_changes.std():.2f}")
print(f"   Máximo: {sr_changes.max():.2f}")
print(f"   Mínimo: {sr_changes.min():.2f}")

# Serie 3: Operaciones con Series
win_sr_changes = df[df['Result'] == 'Win']['SR Change'].dropna()
loss_sr_changes = df[df['Result'] == 'Loss']['SR Change'].dropna()
print("\n3. Comparación de SR Change por Resultado:")
print(f"   Victorias - Media: {win_sr_changes.mean():.2f}")
print(f"   Derrotas - Media: {loss_sr_changes.mean():.2f}")

# =============================================================================
# ANÁLISIS CON DATAFRAMES
# =============================================================================

print("\n" + "=" * 60)
print("ANÁLISIS CON PANDAS DATAFRAMES")
print("=" * 60)

# DataFrame 1: Estadísticas por temporada
season_stats = df.groupby('season').agg({
    'Game #': 'max',  # Número de partidas
    'Result': lambda x: (x == 'Win').sum(),  # Victorias
    'SR Change': ['mean', 'sum'],  # Cambio de SR
    'Elim': 'mean',
    'Death': 'mean',
    'Heal': 'mean',
    'Dmg': 'mean'
}).round(2)

season_stats.columns = ['Partidas', 'Victorias', 'SR_Promedio', 'SR_Total', 
                        'Elim_Promedio', 'Muertes_Promedio', 'Heal_Promedio', 'Dmg_Promedio']

# Calcular winrate
season_stats['Winrate %'] = (season_stats['Victorias'] / season_stats['Partidas'] * 100).round(1)

print("\n1. DataFrame de Estadísticas por Temporada:")
print(season_stats)

# DataFrame 2: Análisis por mapa
map_stats = df[df['Map'].notna()].groupby('Map').agg({
    'Result': [
        lambda x: len(x),  # Total partidas
        lambda x: (x == 'Win').sum(),  # Victorias
        lambda x: ((x == 'Win').sum() / len(x) * 100)  # Winrate
    ],
    'SR Change': 'mean'
}).round(2)

map_stats.columns = ['Partidas', 'Victorias', 'Winrate %', 'SR_Promedio']
map_stats = map_stats.sort_values('Winrate %', ascending=False)

print("\n2. DataFrame de Estadísticas por Mapa:")
print(map_stats)

# DataFrame 3: Análisis por rol
role_stats = df[df['Role 1'].notna()].groupby('Role 1').agg({
    'Result': [
        lambda x: len(x),
        lambda x: (x == 'Win').sum(),
        lambda x: ((x == 'Win').sum() / len(x) * 100)
    ],
    'Elim': 'mean',
    'Death': 'mean',
    'Heal': 'mean',
    'Dmg': 'mean'
}).round(2)

role_stats.columns = ['Partidas', 'Victorias', 'Winrate %', 'Elim', 'Muertes', 'Heal', 'Dmg']

print("\n3. DataFrame de Estadísticas por Rol:")
print(role_stats)

# DataFrame 4: Análisis por modo de juego
mode_stats = df[df['Mode'].notna()].groupby('Mode').agg({
    'Result': [
        lambda x: len(x),
        lambda x: (x == 'Win').sum(),
        lambda x: ((x == 'Win').sum() / len(x) * 100)
    ],
    'SR Change': 'mean'
}).round(2)

mode_stats.columns = ['Partidas', 'Victorias', 'Winrate %', 'SR_Promedio']

print("\n4. DataFrame de Estadísticas por Modo de Juego:")
print(mode_stats)

# =============================================================================
# OPERACIONES AVANZADAS CON DATAFRAMES
# =============================================================================

print("\n" + "=" * 60)
print("OPERACIONES AVANZADAS")
print("=" * 60)

# Filtrado avanzado: Partidas con alto rendimiento
high_performance = df[
    (df['Gold medals'] >= 3) & 
    (df['Result'] == 'Win') &
    (df['Elim'].notna())
]
print(f"\n1. Partidas con 3+ medallas de oro y victoria: {len(high_performance)}")

# Análisis de rachas
max_win_streak = df['Streak'].max()
max_loss_streak = df['Streak'].min()
print(f"\n2. Rachas:")
print(f"   Máxima racha de victorias: {max_win_streak}")
print(f"   Máxima racha de derrotas: {abs(max_loss_streak)}")

# Análisis de leavers
leaver_impact = df.groupby('Leaver').agg({
    'Result': lambda x: (x == 'Win').sum() / len(x) * 100
}).round(2)
print("\n3. Impacto de Leavers en Winrate:")
print(leaver_impact)

# Correlaciones
numeric_cols = ['SR Change', 'Elim', 'Death', 'Heal', 'Dmg', 'Gold medals']
correlations = df[numeric_cols].corr()
print("\n4. Matriz de Correlaciones (primeras 3 columnas):")
print(correlations.iloc[:, :3].round(3))

# =============================================================================
# GUARDAR RESULTADOS
# =============================================================================

# Guardar DataFrames procesados para uso posterior
season_stats.to_csv('/home/claude/overwatch_analysis/data_season_stats.csv')
map_stats.to_csv('/home/claude/overwatch_analysis/data_map_stats.csv')
role_stats.to_csv('/home/claude/overwatch_analysis/data_role_stats.csv')
mode_stats.to_csv('/home/claude/overwatch_analysis/data_mode_stats.csv')

print("\n" + "=" * 60)
print("ARCHIVOS GENERADOS:")
print("- data_season_stats.csv")
print("- data_map_stats.csv")
print("- data_role_stats.csv")
print("- data_mode_stats.csv")
print("=" * 60)
