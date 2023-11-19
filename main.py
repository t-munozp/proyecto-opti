from gurobipy import GRB, Model, quicksum
from process_data import *
from random import randint

m = Model()
m.setParam("TimeLimit", 60*5)

# PARAMS

# VEHÍCULOS
rho, epsilon, M, B, D, tipo_camion, tipo_bus, aux = vehiculos()
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
m.addConstrs((quicksum(x[v, t] * i[c, v, t] * o[c] * tipo_camion[v]
             for c in C) <= M[v] * tipo_camion[v] for v in V for t in T), name="CargaMaximaCamion")
m.addConstrs((quicksum(x[v, t] * i[c, v, t] * o[c] * tipo_camion[v]
             for c in C) >= M[v] * 0.5 * tipo_camion[v]for v in V for t in T), name="CargaMinimaCamion")

m.addConstrs((quicksum(x[v, t] for v in V) <= len(V)
             for t in T), name="MaxVehiculos")
m.addConstrs((quicksum(x[v, t] for v in V) >= 1
             for t in T), name="MinVehiculos")


m.addConstrs((quicksum(quicksum(i[c, v, t] for c in C) * tipo_camion[v] for v in V) <= len(
    C) for t in T), name="TotalElementos1")
m.addConstrs((quicksum(quicksum(i[c, v, t] for c in C) * tipo_camion[v] for v in V) >= len(
    C) for t in T), name="TotalElementos2")

m.addConstrs((quicksum(g[h, v, t] * tipo_bus[v] for h in H for v in V) <= len(
    H) for t in T), name="TotalPersonas1")
m.addConstrs((quicksum(g[h, v, t] * tipo_bus[v] for h in H for v in V) >= len(
    H) for t in T), name="TotalPersonas2")


m.update()

# FUNCIÓN OBJETIVO


f_objetivo = quicksum(k[t] * quicksum(x[v, t] * rho[v] for v in V) for t in T)
m.setObjective(f_objetivo, GRB.MINIMIZE)


m.optimize()


if m.status == GRB.INFEASIBLE:
    print("El modelo es infactible")
    print("Obteniendo IIS...")
    m.computeIIS()
    m.write("iis.ilp")

# m.printStats()


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

print((quicksum(x[v, 1] for v in V)).getValue())
print(((quicksum(quicksum(i[c, v, 1] * tipo_camion[v]
      for c in C) for v in V))).getValue())
print(((quicksum(quicksum(g[h, v, 1] * tipo_bus[v]
      for h in H) for v in V))).getValue())

print()
print(len(T))
print(len(V))
print(len(C))
print(len(H))
print()
