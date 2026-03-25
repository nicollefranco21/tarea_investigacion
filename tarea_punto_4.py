# Resolución del modelo de optimización para Sinergia Portafolios (Liliana Duque)
# Usando PuLP

import pulp

# Crear el problema de maximización
prob = pulp.LpProblem("Portafolio_Duque", pulp.LpMaximize)

# Variables de decisión: fracciones de inversión en cada fondo
X1 = pulp.LpVariable('X1', lowBound=0.10, upBound=1, cat='Continuous')  # Crecimiento
X2 = pulp.LpVariable('X2', lowBound=0.10, upBound=1, cat='Continuous')  # Ingresos
X3 = pulp.LpVariable('X3', lowBound=0.20, upBound=1, cat='Continuous')  # Mercado de Dinero

# Función objetivo: Maximizar el rendimiento esperado
prob += 0.20 * X1 + 0.10 * X2 + 0.06 * X3, "Rendimiento_Esperado"

# Restricción: La suma de las fracciones debe ser 1
prob += X1 + X2 + X3 == 1, "Suma_fracciones"

# Restricción de riesgo
prob += 0.10 * X1 + 0.05 * X2 + 0.01 * X3 <= 0.05, "Indice_Riesgo"

# Resolver el problema
prob.solve()

# Mostrar resultados
print("Estado:", pulp.LpStatus[prob.status])
print(f"Mejor mezcla de inversiones para Liliana Duque:")
print(f"  Fondo de Crecimiento (X1): {X1.varValue:.4f} ({X1.varValue*300000:.2f} USD)")
print(f"  Fondo de Ingresos (X2):    {X2.varValue:.4f} ({X2.varValue*300000:.2f} USD)")
print(f"  Fondo de Mercado Dinero (X3): {X3.varValue:.4f} ({X3.varValue*300000:.2f} USD)")
print(f"Rendimiento esperado: {pulp.value(prob.objective)*300000:.2f} USD anuales")
print(f"Índice de riesgo del portafolio: {0.10*X1.varValue + 0.05*X2.varValue + 0.01*X3.varValue:.4f}")
