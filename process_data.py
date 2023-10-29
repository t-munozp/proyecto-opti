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
    B = {}
    D = {}
    Y = {}
    Z = {}

    with open(ruta_distancias, 'r') as archivo:
        data = csv.reader(archivo, delimiter=';')
        fila = 0
        numero_auto = 0
        for n, filas in enumerate(data):
            if fila == 0:
                fila += 1
            elif (filas != []):
                _, _, rho, epsilon, m, b, d, y, z = filas
                Rho[n] = float(rho)
                if float(epsilon) == 0:
                    epsilon = 0.0000000001
                Epsilon[n] = float(epsilon)
                M[n] = int(m)
                B[n] = int(b)
                D[n] = int(d)
                Y[n] = int(y)
                Z[n] = int(z)
                numero_auto = n
    return Rho, Epsilon, M, B, D, Y, Z, numero_auto


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
                        precio[n, t] = int(val)

    return precio
