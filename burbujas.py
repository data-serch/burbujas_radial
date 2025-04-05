import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.cm import rainbow
import matplotlib.patches as mpatches
from matplotlib.patches import Wedge

# -----------------------------
# DATOS BASE
# -----------------------------
data = {
    'App': ['OTAs', 'Aerolíneas', 'Noticias', 'Banca', 'Redes Sociales', 'Apps Gamificadas'],
    'Uso diario': [7, 6, 18, 12, 44, 25],
    'Interacción': [22.8, 22.8, 41, 38, 67, 150],
    'Respuesta': [10, 10, 95, 90, 50, 60],
    'Retención': [18, 18, 40, 45, 65, 50],
    'Influencia': [60, 50, 40, 20, 58, 55]
}
df = pd.DataFrame(data)
df_long = df.melt(id_vars='App', var_name='Métrica', value_name='Valor')

# -----------------------------
# COLORES DE BURBUJA 
# -----------------------------
bubble_colors = {
    'Uso diario': '#f06595',      # Rosa
    'Interacción': '#fcc419',     # Amarillo
    'Respuesta': '#20c997',       # Verde
    'Retención': '#5c7cfa',       # Azul
    'Influencia': '#adb5bd'       # Gris medio claro
}
df_long['Color'] = df_long['Métrica'].map(bubble_colors)

# -----------------------------
# ÁNGULOS Y COLORES DE CATEGORÍA
# -----------------------------
apps = data['App']
num_apps = len(apps)
segment_span = 2 * np.pi / num_apps
angles_start = np.linspace(0, 2 * np.pi, num_apps, endpoint=False)
angles_end = angles_start + segment_span
angles_mid = (angles_start + angles_end) / 2
app_angle_mid = dict(zip(apps, angles_mid))

# -----------------------------
# POSICIONES DE BURBUJAS
np.random.seed(42)
metric_order = {'Uso diario': 0, 'Interacción': 1, 'Respuesta': 2, 'Retención': 3, 'Influencia': 4}
angle_spread = 0.12

df_long['angle_jitter'] = df_long.apply(
    lambda row: app_angle_mid[row['App']] +
                (metric_order[row['Métrica']] - 2) * angle_spread +
                np.random.uniform(-0.003, 0.003),
    axis=1
)
radius_base = 0.92
df_long['radius'] = radius_base + np.random.uniform(-0.06, 0.06, size=len(df_long))
df_long['x'] = df_long['radius'] * np.cos(df_long['angle_jitter'])
df_long['y'] = df_long['radius'] * np.sin(df_long['angle_jitter'])

# -----------------------------
# PLOT
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')

# Anillo rainbow
segment_count = 100
r = 1.1
for i in range(segment_count):
    theta_start = 2 * np.pi * i / segment_count
    theta_end = 2 * np.pi * (i + 1) / segment_count
    x_segment = [r * np.cos(theta_start), r * np.cos(theta_end)]
    y_segment = [r * np.sin(theta_start), r * np.sin(theta_end)]
    ax.plot(x_segment, y_segment, color=rainbow(i / segment_count), linewidth=10.4, solid_capstyle='butt')

# Bordes negro del anillo
lw = 10.4
offset = lw / 72 / 2
circle_inner = plt.Circle((0, 0), r - offset + 0.045, color='black', fill=False, linewidth=1)
circle_outer = plt.Circle((0, 0), r + offset - 0.045, color='black', fill=False, linewidth=1)
ax.add_patch(circle_inner)
ax.add_patch(circle_outer)

# Etiquetas
label_radius = 1.15
for i, app in enumerate(apps):
    angle = angles_mid[i]
    angle_deg = np.degrees(angle)
    if 90 < angle_deg < 270:
        rotation = angle_deg + 180
        alignment = 'right'
    else:
        rotation = angle_deg
        alignment = 'left'
    ax.text(label_radius * np.cos(angle),
            label_radius * np.sin(angle),
            app,
            ha=alignment,
            va='center',
            rotation=rotation,
            rotation_mode='anchor',
            fontsize=10)

# Burbujas
for _, row in df_long.iterrows():
    ax.scatter(
        row['x'], row['y'],
        s=row['Valor'] * 26,
        color=row['Color'],
        edgecolor=row['Color'],
        alpha=0.85,
        linewidth=0.5
    )

# Leyenda 
legend_elements = [mpatches.Patch(color=color, label=metric) for metric, color in bubble_colors.items()]
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.25, 1))

# Título y subtítulo
fig.suptitle(
    'Comparativo de desempeño de aplicaciones móviles según métricas clave',
    fontsize=14, weight='bold', ha='center', y=1.01
)

fig.text(
    0.5, 0.975,
    'Tamaño de burbuja proporcional al desempeño por métrica (más grande = mejor)',
    ha='center', fontsize=10, color='black'
)

plt.axis('off')
plt.tight_layout()
plt.show()
