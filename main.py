from gurobipy import GRB, Model, quicksum

m = Model()

# ÍNDICES
c, v, t, h = 50

C = [i for i in range(1, c)]
V = [i for i in range(1, v)]
T = [i for i in range(1, t)]
H = [i for i in range(1, h)]


# PARAMS

# Vehículos

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


# Carga

# Cantidad de elementos a transportar
L = 1000

# Cantidad de personas a transportar
H = 100

# Peso elemento c
o = {}

# Peso persona h
p = {}


# Otros

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

#El peso mínimo de la carga del vehículo v tiene que ser mayor o igual al 50% de la carga máxima de este
m.addConstrs(0.5 * M[v] <= quicksum(g[])) 


# Los costos de transporte del tour no deben superar el presupuesto para transporte
m.addConstrs((quicksum(quicksum(x[v,t]*k) for t in T * (1/epsilon) * (S*B*R*D)) for v in V <= T), name="R4")