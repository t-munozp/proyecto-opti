from gurobipy import GRB, Model, quicksum
from process_data import *
from random import randint

m = Model()
m.setParam("TimeLimit", 60)

# PARAMS

# VEHÍCULOS
# Emisión co2, eficiencia, carga máx, bencinero, petrolero, camión, bus
rho, epsilon, M, B, D, Y, Z, aux = vehiculos()

# Cantidad de vehículos (conjunto V)
V = [i for i in range(1, aux + 1)]

# Precio que cobra un conductor por conducir un camión 8 horas
omega = 295368

# Precio que cobra un conductor por conducir un bus por 8 horas
theta = 27080

# Cantidad de jornadas laborales necesarias para recorrer el trayecto t en bus y camión respectivamente.
beta, gamma = jornadas()
# conjunto T
T = list(beta.keys())

# Precio que tiene que arrendar el vehiculo v por el trayecto t
u = precios()

# Vehículo v bencinero {0,1}

# Costo de bencina por litro
S = 1356

# Costo de petróleo por litro
R = 1200


# CARGA

# Peso elemento c
o = elementos()
# Cantidad de elementos a cargar (conjunto C)
C = obtener_longitud(o)

# Peso persona h
p = personas()
# Cantidad de personas (conjunto H)
H = obtener_longitud(p)


# OTROS
# Kilómetros en trayecto t
k = distancias()

# Presupuesto transporte
tau = 50000000

# Presupuesto salarios
Q = 60000000

# Prespuesto total
U = 100000000

# VARIABLES
x = m.addVars(V, T, vtype=GRB.BINARY, name="x_vt")
g = m.addVars(H, V, T, vtype=GRB.BINARY, name="g_hvt")
i = m.addVars(V, C, T, vtype=GRB.BINARY, name="i_vct")


m.update()

# RESTRICCIONES
# El peso de la carga del vehículo v no debe superar el máximo permitido
m.addConstrs((quicksum(g[h, v, t] * p[h] for h in H) + quicksum(i[v, c, t] * o[c] for c in C) <= M[v] for v in V for t in T), name="R1")

# La cantidad de vehículos v usados en el trayecto t no debe superar la cantidad disponible de vehículos
m.addConstrs((quicksum(x[v, t] for v in V) <= len(V) for t in T), name="R2")

# El peso mínimo de la carga del vehículo v tiene que ser mayor o igual al 50% de la carga máxima de este
m.addConstrs((0.5 * M[v] <= quicksum(g[h, v, t] * p[h] for h in H) + quicksum(i[v, c, t] * o[c] for c in C) for v in V for t in T), name="R3")

# Los costos de transporte del tour no deben superar el presupuesto para transporte
m.addConstr((quicksum(quicksum(x[v, t]*k[t] for t in T) * (1/epsilon[v]) * (S * B[v] + R * D[v]) + quicksum(x[v, t] * u[v, t] for t in T) for v in V) <= tau), name="R4")

# Los costos de sueldos no deben superar el presupuesto de salario
m.addConstr((quicksum(quicksum(x[v, t]*omega for t in T) for v in V) <= Q), name="R5")

# Los gastos totales deben ser menores o igules al presupuesto final
m.addConstr(quicksum(quicksum(x[v, t] * ((omega * Y[t] * gamma[t]) + (theta * Z[t] * beta[t])) for t in T) for v in V) + quicksum(quicksum(x[v, t] * k[t] for t in T) * (1/epsilon[v])*(S*B[v] + R * D[v]) * (quicksum(x[v, t] * u[v, t] for t in T)) for v in V) <= U, name="R6")

# En cada trayecto se deben transportar todos los elementos
m.addConstrs((quicksum(quicksum(i[v, c, t] for c in C) for v in V) <= len(C) for t in T), name="R7")
m.addConstrs((quicksum(quicksum(i[v, c, t] for c in C) for v in V) >= len(C) for t in T), name="R8")

# En cada trayecto se deben transportar todas las personas
m.addConstrs((quicksum(quicksum(g[h, v, t] for h in H) for v in V) <= len(H) for t in T), name="R9")
m.addConstrs((quicksum(quicksum(g[h, v, t] for h in H) for v in V) >= len(H) for t in T), name="R10")


m.update()

# FUNCIÓN OBJETIVO

f_objetivo = quicksum((quicksum((k[t]*quicksum(i[v, c, t] * o[c] for c in C) * rho[v] + 1/epsilon[v]) for t in T)) for v in V)
m.setObjective(f_objetivo, GRB.MINIMIZE)

m.optimize()
m.printStats()

print(f"El valor objetivo de emisiones de CO2 es de: {m.ObjVal}")
