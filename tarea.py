
# Resolución del problema de Vecta Inversiones usando programación lineal
# Forma sencilla con scipy.optimize.linprog
# Requiere instalar scipy: pip install scipy

from scipy.optimize import linprog
import numpy as np




# MODELO VECTA INVERSIONES (con precios de acciones)
# Variables: X1, X2, X3, X4 = número de acciones A, B, C, D
precios = [100, 50, 80, 40]  # X1, X2, X3, X4
# Coeficientes de riesgo y rendimiento por dólar invertido
riesgo_unit = [0.10, 0.07, 0.05, 0.08]
rend_unit = [0.12, 0.08, 0.06, 0.10]
# Función objetivo A: Minimizar riesgo total
c_riesgo = [p*r for p, r in zip(precios, riesgo_unit)]
# Función objetivo B: Maximizar rendimiento total (negativo para linprog)
c_rendimiento = [-p*r for p, r in zip(precios, rend_unit)]


# Restricciones para minimizar riesgo (con rendimiento mínimo):
A_ub_riesgo = [
    [-precios[0]*rend_unit[0], -precios[1]*rend_unit[1], -precios[2]*rend_unit[2], -precios[3]*rend_unit[3]],  # -rendimiento <= -18000
    [precios[0], 0, 0, 0],  # Inversión en X1 <= 100000
    [0, precios[1], 0, 0],
    [0, 0, precios[2], 0],
    [0, 0, 0, precios[3]],
    [precios[0], precios[1], precios[2], precios[3]]  # presupuesto total
]
b_ub_riesgo = [
    -18000,
    100000,
    100000,
    100000,
    100000,
    200000
]

# Restricciones para maximizar rendimiento (sin rendimiento mínimo):
A_ub_rend = [
    [precios[0], 0, 0, 0],
    [0, precios[1], 0, 0],
    [0, 0, precios[2], 0],
    [0, 0, 0, precios[3]],
    [precios[0], precios[1], precios[2], precios[3]]
]
b_ub_rend = [
    100000,
    100000,
    100000,
    100000,
    200000
]


# Límites de las variables (todas >= 0)
bounds = [(0, None), (0, None), (0, None), (0, None)]



nombres = ['A', 'B', 'C', 'D']

print('--- Minimizar Riesgo (con rendimiento mínimo) ---')
res_riesgo = linprog(c_riesgo, A_ub=A_ub_riesgo, b_ub=b_ub_riesgo, bounds=bounds, method='highs')
if res_riesgo.success:
    for i, nombre in enumerate(nombres):
        print(f"Comprar {res_riesgo.x[i]:.2f} acciones de {nombre} (inversión: ${res_riesgo.x[i]*precios[i]:.2f})")
    riesgo_total = np.dot(c_riesgo, res_riesgo.x)
    rendimiento_total = sum(res_riesgo.x[i]*precios[i]*rend_unit[i] for i in range(4))
    print(f"Riesgo total: {riesgo_total:.2f}")
    print(f"Rendimiento total: {rendimiento_total:.2f}")
else:
    print(res_riesgo.message)

print('\n--- Maximizar Rendimiento (sin rendimiento mínimo) ---')
res_rend = linprog(c_rendimiento, A_ub=A_ub_rend, b_ub=b_ub_rend, bounds=bounds, method='highs')
if res_rend.success:
    for i, nombre in enumerate(nombres):
        print(f"Comprar {res_rend.x[i]:.2f} acciones de {nombre} (inversión: ${res_rend.x[i]*precios[i]:.2f})")
    riesgo_total = np.dot(c_riesgo, res_rend.x)
    rendimiento_total = sum(res_rend.x[i]*precios[i]*rend_unit[i] for i in range(4))
    print(f"Riesgo total: {riesgo_total:.2f}")
    print(f"Rendimiento total: {rendimiento_total:.2f}")
else:
    print(res_rend.message)
