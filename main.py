from gurobipy import GRB, Model, quicksum
from process_data import *

m = Model()
m.setParam("TimeLimit", 60)

# ÍNDICES
# REDEFINIDOS MÁS ADELANTE
# C = [i for i in range(1, 7)]
# V = [i for i in range(1, 8)]
# T = [i for i in range(1, 11)]
# H = [i for i in range(1, 5)]


# PARAMS
# TODO: editar cantidadmaxdevehiculos
cantidadmaxdevehiculos = 7

# VEHÍCULOS
# Emisión co2 vehículo v
rho, epsilon, M, B, D, Y, Z, aux = vehiculos()
V = [i for i in range(1, aux)]


# Carga máxima (en kg) vehículo v


# Peso (en kg) del vehículo v
W = {1: 1000, 2: 1000, 3: 1000, 4: 1750, 5: 1500, 6: 3000, 7: 3000}

# Precio que cobra un conductor por conducir un camión 8 horas
omega = 295368

# Precio que cobra un conductor por conducir un bus por 8 horas
theta = 27080

# Cantidad de jornadas laborales necesarias para recorrer el trayecto t en bus.
# Cantidad de jornadas laborales necesarias para recorrer el trayecto t en camion.
beta, gamma = jornadas()
T = list(beta.keys())

# Vehículo v bencinero {0,1}


# Costo de bencina por litro
S = 1356

# Costo de petróleo por litro
R = 1200


# CARGA
# Cantidad de elementos a transportar
# L = 6

# Cantidad de personas a transportar
# H = 4

# Peso elemento c
o = elementos()
C = obtener_longitud(o)

# Peso persona h
p = personas()
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
m.addConstrs((quicksum(g[h, v, t] * p[h] for h in H) + quicksum(i[v, c, t] * o[c]
             for c in C) <= M[v] for v in V for t in T), name="R1")

# La cantidad de vehículos v usados en el trayecto t no debe superar la cantidad disponible de vehículos
# cantidadmaxdevehiculos HAY QUE DEF
m.addConstrs((quicksum(x[v, t] for v in V) <=
             cantidadmaxdevehiculos for t in T), name="R2")

# El peso mínimo de la carga del vehículo v tiene que ser mayor o igual al 50% de la carga máxima de este
m.addConstrs((0.5 * M[v] <= quicksum(g[h, v, t] * p[h] for h in H) +
             quicksum(i[v, c, t] * o[c] for c in C) for v in V for t in T), name="R3")

# Los costos de transporte del tour no deben superar el presupuesto para transporte
m.addConstr((quicksum(quicksum(x[v, t]*k[t] for t in T) * (1/epsilon[v])
            * (S * B[v] + R * D[v]) for v in V) <= tau), name="R4")

# Los costos de sueldos no deben superar el presupuesto de salario
m.addConstr((quicksum(quicksum(x[v, t]*omega[v]
            for t in T) for v in V) <= Q), name="R5")

# Los gastos totales deben ser menores o igules al presupuesto final
m.addConstr((quicksum(quicksum(x[v, t]*omega[v] for t in T)for v in V) + quicksum(quicksum(
    x[v, t]*k[t] for t in T) * (1/epsilon[v]) * (S * B[v] + R * D[v]) for v in V) <= U), name="R6")

# En cada trayecto se deben transportar todos los elementos
m.addConstrs((quicksum(quicksum(i[v, c, t] for c in C)
             for v in V) <= len(C) for t in T), name="R7")
m.addConstrs((quicksum(quicksum(i[v, c, t] for c in C)
             for v in V) >= len(C) for t in T), name="R")

# En cada trayecto se deben transportar todas las personas
m.addConstrs((quicksum(quicksum(g[h, v, t] for h in H)
             for v in V) <= len(H) for t in T), name="R9")
m.addConstrs((quicksum(quicksum(g[h, v, t] for h in H)
             for v in V) >= len(H) for t in T), name="R10")


m.update()

# FUNCIÓN OBJETIVO

f_objetivo = (quicksum(quicksum(x[v, t] * k[t] * (quicksum(i[v, c, t] * o[c]
              for c in C)) + W[v] for t in T) * rho[v] for v in V))
m.setObjective(f_objetivo, GRB.MINIMIZE)

m.optimize()
m.printStats()

print(f"El valor objetivo de emisiones de CO2 es de: {m.ObjVal}")
