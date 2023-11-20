from gurobipy import GRB, Model, quicksum
from process_data import *
from random import randint
import numpy as np

m = Model()
m.setParam("TimeLimit", 60*5)

# PARAMS

# VEHÍCULOS
rho, epsilon, M, B, D, tipo_camion, tipo_bus, aux, Y, Z, tipo = vehiculos()
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
B[v] = {1, 0} 1 si usa bencina, 0 si disel
D[v] = {1, 0} 0 si usa bencina, 1 si disel
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
m.addConstrs((quicksum(i[c, v, t] * o[c] * tipo_camion[v]
             for c in C) <= M[v] * tipo_camion[v] * x[v, t]for v in V for t in T), name="CargaMaximaCamion")
m.addConstrs((quicksum(i[c, v, t] * o[c] * tipo_camion[v]
             for c in C) >= M[v] * 0.5 * tipo_camion[v] * x[v, t] for v in V for t in T), name="CargaMinimaCamion")

m.addConstrs((quicksum(x[v, t] for v in V) <= len(V)
             for t in T), name="MaxVehiculos")
m.addConstrs((quicksum(x[v, t] * tipo_camion[v] for v in V) >= 1
             for t in T), name="MinVehiculosCamion")
m.addConstrs((quicksum(x[v, t] * tipo_bus[v] for v in V) >= 1
             for t in T), name="MinVehiculosBus")


m.addConstrs((quicksum(quicksum(i[c, v, t] for c in C) * tipo_camion[v] for v in V) == len(
    C) for t in T), name="TotalElementos")
m.addConstrs((quicksum(quicksum(g[h, v, t] for h in H) * tipo_bus[v] for v in V) == len(
    H) for t in T), name="TotalPersonas")

# Agrega restricciones para que las personas no se transporten en camiones
for h in H:
    for v in V:
        for t in T:
            if tipo_camion[v] == 1:
                m.addConstr(g[h, v, t] == 0)

for c in C:
    for v in V:
        for t in T:
            if tipo_bus[v] == 1:
                m.addConstr(i[c, v, t] == 0)

# Las personas deben compartir vehículos, considerando las limitaciones de este
m.addConstrs((quicksum(g[h, v, t] * p[h] for h in H) <= M[v]
             * tipo_bus[v] for v in V for t in T), name="CapacidadBus")

# Cada persona solo puede ser asignada a un vehículo
m.addConstrs((quicksum(g[h, v, t] for v in V) <=
             1 for h in H for t in T), name="AsignacionUnica")

# PRESUPUESTO


# Restricción de presupuesto transporte
m.addConstr((quicksum(quicksum(x[v, t]*k[t] for t in T) * epsilon[v] * B[v] for v in V) * S +
             quicksum(quicksum(x[v, t]*k[t] for t in T) * epsilon[v] * D[v] for v in V) * R <= tau), name="PresupuestoTransporte")

# Restricción de presupuesto salarios
m.addConstr((quicksum(quicksum(g[h, v, t] * theta * tipo_bus[v] for v in V) for t in T) +
             quicksum(quicksum(i[c, v, t] * omega * tipo_camion[v] for v in V) for t in T) <= Q), name="PresupuestoSalarios")

# Restricción de presupuesto total
m.addConstr((quicksum(quicksum(x[v, t]*k[t] for t in T) * epsilon[v] * B[v] for v in V) * S +
             quicksum(quicksum(x[v, t]*k[t] for t in T) * epsilon[v] * D[v] for v in V) * R +
             quicksum(quicksum(g[h, v, t] * theta * tipo_bus[v] for v in V) for t in T) +
             quicksum(quicksum(i[c, v, t] * omega * tipo_camion[v] for v in V) for t in T) <= U), name="PresupuestoTotal")

m.update()

# FUNCIÓN OBJETIVO


f_objetivo = quicksum(k[t] * quicksum(x[v, t] * rho[v] for v in V) for t in T)
m.setObjective(f_objetivo, GRB.MINIMIZE)


m.optimize()


if m.status == GRB.INFEASIBLE:
    print("El modelo es infactible")
    print("Obteniendo IIS...")
    # m.computeIIS()
    # m.write("iis.ilp")

# m.printStats()
print()

print('El costo total usado en transporte fue: ', end="")
print(
    f'{quicksum(quicksum(x[v, t]*k[t] for t in T) * epsilon[v] * B[v] for v in V).getValue() * S}[CLP] en bencina')
print('El costo total usado en transporte fue:', end="")
print(
    f'{quicksum(quicksum(x[v, t]*k[t] for t in T) * epsilon[v] * D[v] for v in V).getValue() * R}[CLP] en petroleo')

# for t in T:
#     cantidad_elementos = quicksum(quicksum(i[v, c, t] for c in C) for v in V).getValue()
#     print(f'La cantidad de elementos transportados en trayecto {t} es: {cantidad_elementos}')


print(
    f"\n-------------\n------------------\nEl valor objetivo de emisiones de CO2 es de: {m.ObjVal/1000} kg\n------------------\n-------------\n")


# imprime en que bus se transporta cada persona para el trayecto 1.
for t in T:
    for h in H:
        for v in V:
            if g[h, v, t].X == 1:
                print(
                    f'La persona {h} se transporta en el vehiculo {v} para el trayecto {t}')

cant_bus = 0
cant_camion = 0
for t in T:
    for v in V:
        val = x[v, t].X
        if tipo_bus[v] == 1:
            cant_bus += 1
        else:
            cant_camion += 1

print(f'La cantidad de buses usados es: {cant_bus}')
print(f"La cantidad de camiones usados es: {cant_camion}")
dinero_usado = (quicksum(quicksum(x[v, t]*k[t] for t in T) * epsilon[v] * B[v] for v in V) * S +
                quicksum(quicksum(x[v, t]*k[t] for t in T) * epsilon[v] * D[v] for v in V) * R +
                quicksum(quicksum(g[h, v, t] * theta * tipo_bus[v] for v in V) for t in T) +
                quicksum(quicksum(i[c, v, t] * omega * tipo_camion[v] for v in V) for t in T)).getValue()

print(f"El dinero usado en Total es: {dinero_usado} CLP")

dinero_salarios = (quicksum(quicksum(g[h, v, t] * theta * tipo_bus[v] for v in V) for t in T) +
                   quicksum(quicksum(i[c, v, t] * omega * tipo_camion[v] for v in V) for t in T)).getValue()
print(f"El dinero usado en salarios es: {dinero_salarios} CLP")

dinero_transporte = (quicksum(quicksum(x[v, t]*k[t] for t in T) * epsilon[v] * B[v] for v in V) * S +
                     quicksum(quicksum(x[v, t]*k[t] for t in T) * epsilon[v] * D[v] for v in V) * R).getValue()
print(f"El dinero usado en transporte es: {dinero_transporte} CLP")
