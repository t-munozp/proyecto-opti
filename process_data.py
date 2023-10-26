import csv

M = range(1 , 5 + 1) #materiales
I = range(1, 7 + 1) #regiones
D = range(1, 3 + 1) #dimensión
T = range(1, 50 + 1) #tiempo

materiales = {'Rachel 35%': 1, 'Rachel 50%': 2, 'Tela quirurguica': 3, 'Costal de fique': 4, 'Guata': 5}
regiones = {'Atacama': 1, 'Coquimbo': 2, 'Valparaiso': 3, 'Metropolitana': 4, 'Ohiggins': 5, 'Maule': 6, 'Nuble': 7}
dimensiones = {'48': 1, '100': 2, '150': 3}


def demanda_anual():
    diccionario = {}
    with open('data/demanda3.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for fila in data:
            region, año, demanda = fila
            numero_region_dict = regiones[region]
            diccionario[numero_region_dict, int(año) - 2024] = float(demanda)*(10**6) * 0.03
    return diccionario

def demanta_total():
    demanta_total = 0
    with open('data/demanda3.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for fila in data:
            region, año, demanda = fila
            demanta_total += float(demanda)*(10**6) * 0.03
    return demanta_total

def costo_mantencion():

    diccionario = {}

    with open('data/costo_mantencion.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for fila in data:
            material, dimension, precio = fila
            numero_material = materiales[material]
            numero_dimension = dimensiones[dimension]
            for año in range(1,51):
                for region in range(1,7 + 1):
                    diccionario[numero_material, region, numero_dimension, año] = float(precio)

    return diccionario


def costo_instalacion():

    diccionario = {}

    with open('data/costo_instalacion.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for fila in data:
            material, dimension, precio = fila
            numero_material = materiales[material]
            numero_dimension = dimensiones[dimension]
            for año in range(1,51):
                for region in range(1,7 + 1):
                    diccionario[numero_material, region, numero_dimension, año] = float(precio)
        
    
    return diccionario



#no debería depender de la región, es el mismo atrapanieblas

def capacidad_maxima():
    diccionario = {}
    with open('data/capacidad_maxima.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for fila in data:
            material, dimension, recoleccion  = fila
            numero_dimension = dimensiones[dimension]
            numero_material = materiales[material]
            for region in range(1,7 + 1):
                diccionario[numero_material,region,numero_dimension] = float(recoleccion)*365


    return diccionario


def humedad_anual():
    diccionario = {}
    with open('data/humedad.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for fila in data:
            region, humedad = fila
            numero_region = regiones[region]
            for año in range(1,51):
                diccionario[numero_region,año] = float(humedad)
    return diccionario

def eficiencia_material():
    diccionario = {}
    with open('data/eficiencia.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for fila in data:
            material, eficiencia = fila
            numero_material = materiales[material]
            diccionario[numero_material] = float(eficiencia)
    
    return diccionario

def superficie_efectiva():
    diccionario = {}
    with open('data/superficie.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for fila in data:
            region, superficie = fila
            numero_region = regiones[region]
            diccionario[numero_region] = float(superficie) * (10**6)
    
    return diccionario

def area_ocupada():
    diccionario = {}
    with open('data/area.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for fila in data:
            dimension, area = fila
            numero_dimension = dimensiones[dimension]
            diccionario[numero_dimension] = float(area)

    return diccionario

def plazo_mantenimiento():
    diccionario = {}
    with open('data/plazo_mantenimiento.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for fila in data:
            region, plazo = fila
            numero_region = regiones[region]
            diccionario[numero_region] = int(plazo) - 2
    
    return diccionario
