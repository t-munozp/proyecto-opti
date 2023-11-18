import csv
from os import path


def obtener_longitud(data):
    longitud = len(data)
    lista = [i for i in range(1, longitud + 1)]
    return lista


def distancias():
    ruta_distancias = path.join("datos", "Distancias.csv")
    diccionario = {}
    with open(ruta_distancias, 'r') as archivo:
        data = csv.reader(archivo)
        fila = 0
        for filas in data:
            if fila == 0:
                fila += 1
            else:
                trayecto, distancia = filas
                diccionario[int(trayecto)] = int(distancia)
    return diccionario


def personas():
    ruta_distancias = path.join("datos", "Personas.csv")
    diccionario = {}
    with open(ruta_distancias, 'r') as archivo:
        data = csv.reader(archivo)
        fila = 0
        for n, filas in enumerate(data):
            if fila == 0:
                fila += 1
            else:
                diccionario[n] = 80.7
    return diccionario


def jornadas():
    ruta_distancias = path.join("datos", "Jornadas.csv")
    buses = {}
    camiones = {}
    with open(ruta_distancias, 'r') as archivo:
        data = csv.reader(archivo)
        fila = 0
        for filas in data:
            if fila == 0:
                fila += 1
            else:
                trayecto, camion, bus = filas
                buses[int(trayecto)] = int(bus)
                camiones[int(trayecto)] = int(camion)
    return buses, camiones


def elementos():
    ruta_distancias = path.join("datos", "Elementos.csv")
    pesos = {}

    with open(ruta_distancias, 'r') as archivo:
        data = csv.reader(archivo, delimiter=",")
        for n, filas in enumerate(data):
            if n == 0:
                pass
            elif (filas != []):
                pesos[n] = float(filas[1])
    return pesos


def vehiculos():
    ruta_distancias = path.join("datos", "Vehiculos.csv")
    Rho = {}
    Epsilon = {}
    M = {}
    combustible = {}
    tipo_camion = {}
    tipo_bus = {}

    with open(ruta_distancias, 'r') as archivo:
        data = csv.reader(archivo, delimiter=';')
        fila = 0
        numero_bus = 0
        numero_camion = 0
        n_total = 0
        for fila, filas in enumerate(data):
            if fila == 0:
                fila += 1
            elif (filas != []):
                type, _, rho, epsilon, m, B, D, _, _ = filas
                if type == "Camion 1" or type == "Camion 2":
                    Rho[fila] = float(epsilon)
                    M[fila] = int(m)
                    Rho[fila] = float(rho)
                    tipo_camion[fila] = 1
                    tipo_bus[fila] = 0
                else:
                    Epsilon[fila] = float(epsilon)
                    M[fila] = int(m)
                    Rho[fila] = float(rho)
                    tipo_camion[fila] = 0
                    tipo_bus[fila] = 1
                combustible[fila] = B
    return Rho, Epsilon, M, combustible, tipo_camion, tipo_bus, fila


def precios():
    ruta_distancias = path.join("datos", "Precios.csv")
    precio = {}

    with open(ruta_distancias, 'r') as archivo:
        data = csv.reader(archivo, delimiter=";")
        fila = 0
        for n, filas in enumerate(data):
            if fila == 0:
                fila += 1
            elif (filas != []):
                for t, val in enumerate(filas):
                    if t != 0:
                        precio[(n, t)] = int(float(val))
    return precio


def suma(lista1, lista2):
    sm = 0
    for i in lista1.values():
        sm += i

    for j in lista2.values():
        sm += j

    return sm
