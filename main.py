from gurobipy import GRB, Model

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

