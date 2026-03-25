# Solución al problema de portafolio conservador usando programación lineal (PuLP)
import pulp

# Definir los rendimientos de cada fondo por año
rendimientos = [
	[0.1006, 0.1312, 0.1347, 0.4542, -0.2193],  # Capital extranjero
	[0.1764, 0.0325, 0.0751, -0.0133, 0.0736],   # Bono a mediano plazo
	[0.3241, 0.1871, 0.3328, 0.4146, -0.2326],   # Crecimiento gran capitalización
	[0.3236, 0.2061, 0.1293, 0.0706, -0.0537],   # Valor gran capitalización
	[0.3344, 0.1940, 0.0385, 0.5868, -0.0902],   # Crecimiento baja capitalización
	[0.2456, 0.2532, -0.0670, 0.0543, 0.1731],   # Valor baja capitalización
]

# Crear el problema de optimización (maximizar X7)
prob = pulp.LpProblem("Portafolio_Conservador_Maximin", pulp.LpMaximize)

# Variables de decisión: proporciones de inversión en cada fondo (X1 a X6) y el rendimiento mínimo (X7)
x = [pulp.LpVariable(f"X{i+1}", lowBound=0) for i in range(6)]
x7 = pulp.LpVariable("X7")

# Función objetivo: maximizar X7
prob += x7, "Rendimiento_minimo_maximo"

# Restricción: suma de proporciones = 1
prob += pulp.lpSum(x) == 1, "Suma_proporciones"

# Restricciones de rendimiento por año (escenario)
for j in range(5):
	prob += (
		pulp.lpSum([rendimientos[i][j] * x[i] for i in range(6)]) >= x7,
		f"Rendimiento_ano_{j+1}"
	)

# Resolver el problema
prob.solve()

# Mostrar resultados
print("Estado de la solución:", pulp.LpStatus[prob.status])
for i in range(6):
	print(f"Proporción en fondo {i+1}: {x[i].varValue:.4f}")
print(f"Rendimiento mínimo garantizado (X7): {x7.varValue:.4%}")
