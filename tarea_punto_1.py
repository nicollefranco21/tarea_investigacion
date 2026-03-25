import pulp

# Crear el problema de maximización
prob = pulp.LpProblem("Spencer_Enterprises", pulp.LpMaximize)

# Variables de decisión binarias
X1 = pulp.LpVariable("X1", cat="Binary")  # Expansión almacén A
X2 = pulp.LpVariable("X2", cat="Binary")  # Expansión almacén B
X3 = pulp.LpVariable("X3", cat="Binary")  # Prueba de mercado
X4 = pulp.LpVariable("X4", cat="Binary")  # Publicidad
X5 = pulp.LpVariable("X5", cat="Binary")  # I+D
X6 = pulp.LpVariable("X6", cat="Binary")  # Equipo nuevo

# Función objetivo
prob += (
	4000 * X1 +
	6000 * X2 +
	10500 * X3 +
	4000 * X4 +
	8000 * X5 +
	3000 * X6
), "Valor_Presente_Neto"

# Restricciones de presupuesto por año
prob += 3000*X1 + 2500*X2 + 6000*X3 + 2000*X4 + 5000*X5 + 1000*X6 <= 10500, "Año_1"
prob += 1000*X1 + 3500*X2 + 4000*X3 + 1500*X4 + 1000*X5 + 500*X6 <= 7000, "Año_2"
prob += 4000*X1 + 3500*X2 + 5000*X3 + 1800*X4 + 4000*X5 + 900*X6 <= 8750, "Año_3"

# Resolver el problema sin mostrar salida del solver
prob.solve(pulp.PULP_CBC_CMD(msg=False))

# Mostrar resultados
print("Estado de la solución:", pulp.LpStatus[prob.status])
for v in prob.variables():
	print(f"{v.name} = {int(v.varValue)}")
print("Valor presente neto máximo:", pulp.value(prob.objective))
