import matplotlib.pyplot as plt
import numpy as np

# Datos
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Total']
planificadas = [6, 4, 12, 5, 4, 5, 3, 4, 43]
ejecutadas = [5, 3, 15, 5, 4, 5, 3, 6, 46]
cumplimiento = [83, 75, 125, 100, 100, 100, 100, 150, 105]

# Crear el gráfico combinado
fig, ax1 = plt.subplots(figsize=(12, 7))

# Gráfico de barras
bar_width = 0.35
indices = np.arange(len(meses))

# Añadir transparencia y bordes a las barras
barras1 = ax1.bar(indices - bar_width/2, planificadas, bar_width, 
                  label='Planificadas', color='royalblue', edgecolor='black', alpha=0.8)
barras2 = ax1.bar(indices + bar_width/2, ejecutadas, bar_width, 
                  label='Ejecutadas', color='indianred', edgecolor='black', alpha=0.8)

# Eje para las barras
ax1.set_xlabel('Meses', fontsize=12, fontweight='bold')
ax1.set_ylabel('Cantidad', fontsize=12, fontweight='bold')
ax1.set_xticks(indices)
ax1.set_xticklabels(meses, fontsize=11)

# Gráfico de líneas para el % de cumplimiento
ax2 = ax1.twinx()
ax2.plot(indices, cumplimiento, color='darkgreen', marker='o', markersize=8, 
         label='% Cumplimiento', linewidth=3, linestyle='--')

# Etiquetas y ajustes del eje secundario
ax2.set_ylabel('% de Cumplimiento', fontsize=12, fontweight='bold')
ax2.set_ylim([0, 160])
ax2.tick_params(axis='y', labelsize=11)
ax2.grid(False)  # Desactiva las líneas de cuadrícula en el eje derecho

# Añadir etiquetas de porcentaje a la línea
for i, val in enumerate(cumplimiento):
    ax2.text(i, val + 3, f'{val}%', ha='center', fontsize=10, color='black')

# Añadir líneas de cuadrícula para mejorar la visibilidad
ax1.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)

# Mejorar la leyenda
ax1.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
ax2.legend(loc='upper right', fontsize=10, frameon=True, shadow=True)

# Título más estético
fig.suptitle('Planificación vs Ejecución y Cumplimiento (%)', fontsize=16, fontweight='bold', color='darkblue')

# Ajustes de los márgenes
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Mostrar gráfico
plt.show()
