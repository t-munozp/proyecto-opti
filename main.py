from gurobipy import GRB, Model, quicksum

m = Model()

# ÍNDICES
c, v, t, h = 50

C = [i for i in range(1, c)]
V = [i for i in range(1, v)]
T = [i for i in range(1, t)]
H = [i for i in range(1, h)]


# PARAMS

# VEHÍCULOS
# Emisión co2 vehículo v
rho = {}

# Eficiencia vehículo v
epsilon = {}

# Carga máxima (en kg) vehículo v
M = {}

# Peso (en kg) del vehículo v
W = {}

# Precio de conductor de vehículo v en trayecto t
omega = {}

# Vehículo v bencinero {0,1}
B = {}

# Vehículo v petrolero {0,1}
D = {}

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
o = {}

# Peso persona h
p = {}


# OTROS
# Kilómetros en trayecto t
k = {}

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
m.addConstrs((quicksum(g[h,v,t]*p) for h in H + quicksum(i[v,c,t]*o) for c in C <= M for v in V for t in T), name="R1")

# La cantidad de vehículos v usados en el trayecto t no debe superar la cantidad disponible de vehículos
m.addContrs((quicksum(x[v,t])for v in V <= cantidadmaxdevehiculos for t in T), name="R2") #cantidadmaxdevehiculos HAY QUE DEF

# El peso mínimo de la carga del vehículo v tiene que ser mayor o igual al 50% de la carga máxima de este
m.addConstrs((0.5 * M[v] <= quicksum(g[h,v,t]*p) for h in H + quicksum(i[v,c,t]*o) for c in C for v in V), name="R3") 

# Los costos de transporte del tour no deben superar el presupuesto para transporte
m.addConstrs((quicksum(quicksum(x[v,t]*k) for t in T * (1/epsilon) * (S*B*R*D)) for v in V <= T), name="R4")

# Los costos de sueldos no deben superar el presupuesto de salario
m.addConstrs((quicksum(quicksum(x[v,t]*omega) for t in T) for v in V <= Q), name="R5")

# Los gastos totales deben ser menores o igules al presupuesto final
m.addConstrs((quicksum(quicksum(x[v,t]*omega) for t in T) for v in V + quicksum(quicksum(x[v,t]*k) for t in T * (1/epsilon) * (S*B*R*D)) for v in V <= U), name="R6")

# En cada trayecto se deben transportar todos los elementos 
m.addConstrs((quicksum(quicksum(i[v,c,t]) for c in C) for v in V <= L for t in T), name="R7")
m.addConstrs((quicksum(quicksum(i[v,c,t]) for c in C) for v in V >= L for t in T), name="R8")

# En cada trayecto se deben transportar todas las personas
m.addConstrs((quicksum(quicksum(g[h,v,t])for h in H) for v in V <= H), name="R9")
m.addConstrs((quicksum(quicksum(g[h,v,t])for h in H) for v in V >= H), name="R9")


m.update()

# FUNCIÓN OBJETIVO

f_objetivo = (quicksum(quicksum(x[v, t] * k * (quicksum(i[v, c, t] * o for c in C)) + W for t in T) * rho for v in V))
m.setObjective(f_objetivo, GRB.MINIMIZE)
m.Params.timeLimit = 1200

m.optimize()
m.printStats()