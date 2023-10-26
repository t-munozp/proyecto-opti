from gurobipy import GRB, Model, quicksum

m = Model()

# ÍNDICES
C = [i for i in range(1, 6)]
V = [i for i in range(1, 7)]
T = [i for i in range(1, 10)]
H = [i for i in range(1, 4)]


# PARAMS
# TODO: editar cantidadmaxdevehiculos
cantidadmaxdevehiculos = 7

# VEHÍCULOS
# Emisión co2 vehículo v
rho = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}

# Eficiencia vehículo v
epsilon = {1: 1, 2: 1, 3: 2, 4: 0.3, 5: 0.4, 6: 0.2, 7: 0.2}

# Carga máxima (en kg) vehículo v
M = {1: 300, 2: 300, 3: 300, 4: 550, 5: 500, 6: 1000, 7: 1000}

# Peso (en kg) del vehículo v
W = {1: 1000, 2: 1000, 3: 1000, 4: 1750, 5: 1500, 6: 3000, 7: 3000}

# Precio de conductor de vehículo v en trayecto t
omega = {1: 123213, 2: 1238974, 3: 30000, 4: 1234586, 5: 8912673, 6: 78632, 7: 91823}

# Vehículo v bencinero {0,1}
B = {1: 0, 2: 0, 3: 1, 4: 0, 5: 1, 6: 1, 7: 0}

# Vehículo v petrolero {0,1}
D = {1: 1, 2: 1, 3: 0, 4: 1, 5: 0, 6: 0, 7: 1}

# Costo de bencina por litro
S = 50

# Costo de petróleo por litro
R = 30


# CARGA
# Cantidad de elementos a transportar
L = 1000

# Cantidad de personas a transportar
H = 100

# Peso elemento c
o = {1: 50, 2: 200, 3: 30, 4: 1000, 5: 800, 6: 10}

# Peso persona h
p = {1: 50, 2: 60, 3: 70, 4: 80}


# OTROS
# Kilómetros en trayecto t
k = {1: 100, 2: 200, 3: 300, 4: 350, 5: 400, 6: 140, 7: 240, 8: 320, 9: 500, 10: 800}

# Presupuesto transporte
T = 50000000

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
m.addConstrs(quicksum(quicksum((quicksum(g[h,v,t]*p[h] for h in H) + quicksum(i[v,c,t]*o[c] for c in C <= M[v]) for v in V) for t in T)), name="R1")

# La cantidad de vehículos v usados en el trayecto t no debe superar la cantidad disponible de vehículos
m.addContrs((quicksum(x[v,t])for v in V <= cantidadmaxdevehiculos for t in T), name="R2") #cantidadmaxdevehiculos HAY QUE DEF

# El peso mínimo de la carga del vehículo v tiene que ser mayor o igual al 50% de la carga máxima de este
m.addConstrs(quicksum(quicksum((0.5 * M[v] <= quicksum(g[h,v,t]*p[h] for h in H) + quicksum(i[v,c,t]*o[c] for c in C) for v in V) for t in T)), name="R3") 

# Los costos de transporte del tour no deben superar el presupuesto para transporte
m.addConstrs((quicksum(quicksum(x[v,t]*k[t] for t in T) * (1/epsilon[v]) * (S * B[v] + R * D[v])) for v in V <= T), name="R4")

# Los costos de sueldos no deben superar el presupuesto de salario
m.addConstrs((quicksum(quicksum(x[v,t]*omega[v] for t in T) for v in V) <= Q), name="R5")

# Los gastos totales deben ser menores o igules al presupuesto final
m.addConstrs((quicksum(quicksum(x[v,t]*omega[v] for t in T)for v in V) + quicksum(quicksum(x[v,t]*k[t] for t in T) * (1/epsilon) * (S * B[v] + R * D[v]) for v in V) <= U), name="R6")

# En cada trayecto se deben transportar todos los elementos 
m.addConstrs((quicksum(quicksum(i[v,c,t] for c in C) for v in V) <= L for t in T), name="R7")
m.addConstrs((quicksum(quicksum(i[v,c,t] for c in C) for v in V) >= L for t in T), name="R")

# En cada trayecto se deben transportar todas las personas
m.addConstrs((quicksum(quicksum(g[h,v,t] for h in H) for v in V) <= H for t in T), name="R9")
m.addConstrs((quicksum(quicksum(g[h,v,t] for h in H) for v in V) >= H for t in T), name="R10")


m.update()

# FUNCIÓN OBJETIVO

f_objetivo = (quicksum(quicksum(x[v, t] * k[t] * (quicksum(i[v, c, t] * o[c] for c in C)) + W[v] for t in T) * rho[v] for v in V))
m.setObjective(f_objetivo, GRB.MINIMIZE)
m.Params.timeLimit = 1200

m.optimize()
m.printStats()

print(f"El valor objetivo es de: {m.ObjVal}[CLP]")