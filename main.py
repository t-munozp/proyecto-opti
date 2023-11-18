from gurobipy import GRB, Model, quicksum
from process_data import *
from random import randint

m = Model()
m.setParam("TimeLimit", 60)

# PARAMS

# VEHÍCULOS
rho, epsilon, M, Bencina, tipo_camion, tipo_bus, aux = vehiculos()
omega = 295368
theta = 27080
beta, gamma = jornadas()
u = precios()
S = 1356
R = 1200

'''
rho[v] = emision de co2 del vehiculo v
epsilon[v] = eficiencia del vehiculo v
M[v] = carga máxima del vehiculo v
Bencina[v] = {1, 0} 1 si usa bencina, 0 si disel
Disel[v] = {1, 0} 0 si usa bencina, 1 si disel
tipo_camion[v] = {1, 0} 1 si es camion, 0 si es bus.
tipo_bus[v] = {1, 0} 0 si es camion, 1 si es bus.
omega = precio por conducir un camion por 8 horas
theta = precio por conducir un bus por 8 horas
beta = jornadas necesarias para hacer el trayecto t en bus
gamma = jornadas necesarias para hcer el trayecto t en camion
u[v] = precio por arrendar el vehiculo v en el trayecto t
S = costo bencia por litro
R = Costo petroleo por litro
'''


# CARGA
o = elementos()
p = personas()

'''
o[c] = Peso del elemento c
p[h] = Peso de la persona h
'''

# OTROS
k = distancias()
tau = 526944260000000
Q = 6000000000000000
U = 1000000000000

'''
k = kilometros del trayecto t
tau= presupuesto en transporte
Q = presupuesto salarios
U = presupuesto total
'''


# INDICES
T = list(beta.keys())
C = obtener_longitud(o)
H = obtener_longitud(p)
V = [i for i in range(1, aux)]

# VARIABLES
x = m.addVars(V, T, vtype=GRB.BINARY, name="x_vt")
g = m.addVars(H, V, T, vtype=GRB.BINARY, name="g_hvt")
i = m.addVars(C, V, T, vtype=GRB.BINARY, name="i_vct")

'''
x[v, t] = {1, 0} 1 si se escogio el vehiculo v para el trayecto t.
g[h, v, t] = {1, 0} 1 si la persona h se transporta en el vehiculo v para el trayecto t.
i[c, v, t] = {1, 0} 1 si el elemento c se transporta en el vehiculo v para el trayecto t.
'''


m.update()

# RESTRICCIONES
m.addConstrs((quicksum(quicksum(x[v, t] * i[c, v, t] * o[c]
             for c in C) for t in T) <= M[v] for v in V), name="CargaMaxima")
m.addConstrs((quicksum(x[v, t] for v in V) <= len(V)
             for t in T), name="MaxVehiculos")
m.addConstrs((quicksum(x[v, t] for v in V) > 0
             for t in T), name="MinVehiculos")
m.addConstrs((quicksum(quicksum(x[v, t] * i[c, v, t] * o[c] for c in C) for t in T)
             >= 0.5 * M[v] * quicksum(x[v, t] for t in T) for v in V), name="CargaMinima")
m.addConstrs((quicksum(i[c, v, t] * tipo_camion[v] for v in V) >=
             1 for c in C for t in T), name="TotalElementos")
m.addConstrs((quicksum(g[h, v, t] * tipo_bus[v] for v in V) >=
             1 for h in H for t in T), name="TotalPersonas")


m.update()

# FUNCIÓN OBJETIVO

f_objetivo = (
    quicksum(quicksum(x[v, t] * k[t] * rho[v] * epsilon[v] for v in V) for t in T))
m.setObjective(f_objetivo, GRB.MINIMIZE)

# m.setParam("Crossover", 0)
# m.setParam("Method", 2)
# # m.setParam("Cuts", 0)
m.optimize()


if m.status == GRB.INFEASIBLE:
    print("El modelo es infactible")
    print("Obteniendo IIS...")
    m.computeIIS()
    m.write("iis.ilp")

m.printStats()
