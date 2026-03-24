
# Resolución del problema de Vecta Inversiones usando programación lineal
# Forma sencilla con scipy.optimize.linprog
# Requiere instalar scipy: pip install scipy

from scipy.optimize import linprog
import numpy as np

# 1. Definimos los coeficientes de riesgo por cada acción (función objetivo)
# Queremos minimizar: 0.10*xA + 0.07*xB + 0.05*xC + 0.08*xD
c = [0.10, 0.07, 0.05, 0.08]

# 2. Definimos las restricciones
# a) Suma de inversiones = 200,000
# b) Rendimiento mínimo: 0.12*xA + 0.08*xB + 0.06*xC + 0.10*xD >= 18,000
# c) Ninguna acción > 100,000
# d) Todas las inversiones >= 0

# Para linprog, las restricciones deben ser de la forma Ax <= b
# Igualdades se ponen aparte

# Restricción de rendimiento (multiplicamos por -1 para que sea <=)
A_ub = [
	[-0.12, -0.08, -0.06, -0.10],  # -rendimiento <= -18000
	[1, 0, 0, 0],                  # xA <= 100000
	[0, 1, 0, 0],                  # xB <= 100000
	[0, 0, 1, 0],                  # xC <= 100000
	[0, 0, 0, 1]                   # xD <= 100000
]
b_ub = [
	-18000,    # -rendimiento mínimo
	100000,    # xA <= 100000
	100000,    # xB <= 100000
	100000,    # xC <= 100000
	100000     # xD <= 100000
]

# Restricción de igualdad: suma de inversiones = 200,000
A_eq = [[1, 1, 1, 1]]
b_eq = [200000]

# Límites de las variables (todas >= 0)
bounds = [(0, None), (0, None), (0, None), (0, None)]

# 3. Ejecutamos el solver
res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

# 4. Mostramos los resultados de forma clara
if res.success:
	nombres = ['A', 'B', 'C', 'D']
	print('Solución óptima encontrada:')
	for i, nombre in enumerate(nombres):
		print(f"Invertir en acción {nombre}: ${res.x[i]:.2f}")
	riesgo_total = np.dot(c, res.x)
	rendimiento_total = 0.12*res.x[0] + 0.08*res.x[1] + 0.06*res.x[2] + 0.10*res.x[3]
	print(f"Riesgo total: {riesgo_total:.2f}")
	print(f"Rendimiento total: {rendimiento_total:.2f}")
else:
	print('No se encontró solución óptima.')
