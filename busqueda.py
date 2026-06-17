# MODULO DE BUSQUEDA DE PAQUETES TURISTICOS
# Las funciones de búsqueda sobre listas se implementan de forma RECURSIVA

from datos import (paquetes, mostrar_paquete,
                   IDX_DESTINO, IDX_PRECIO, IDX_TIPO)

SEPARADOR = "=" * 5


def normalizar_texto(texto):
    texto = texto.lower()
    texto = texto.replace("á", "a")
    texto = texto.replace("é", "e")
    texto = texto.replace("í", "i")
    texto = texto.replace("ó", "o")
    texto = texto.replace("ú", "u")
    return texto


# ============================================================
# BÚSQUEDA RECURSIVA POR DESTINO
# ============================================================

def _buscar_destino_rec(lista, destino_norm, inicio=0):
    '''
    Caso base  : llegamos al final → []
    Caso recursivo: compara el elemento actual y llama al siguiente
    '''
    if inicio >= len(lista):
        return []
    resultados = _buscar_destino_rec(lista, destino_norm, inicio + 1)
    if destino_norm in normalizar_texto(lista[inicio][IDX_DESTINO]):
        resultados = [lista[inicio]] + resultados
    return resultados


def buscar_x_destino(destino_a_buscar):
    resultados = _buscar_destino_rec(paquetes, normalizar_texto(destino_a_buscar))
    if len(resultados) == 0:
        print(f"  No se encontró ningún paquete para el destino: {destino_a_buscar}")
        return
    print(f"\n{SEPARADOR} RESULTADO PARA: {destino_a_buscar.upper()} {SEPARADOR}")
    for paquete in resultados:
        mostrar_paquete(paquete)


# ============================================================
# BÚSQUEDA RECURSIVA POR TIPO (Nacional / Internacional)
# ============================================================

def _buscar_tipo_rec(lista, tipo_norm, inicio=0):
    '''
    Caso base  : fin de lista → []
    Caso recursivo: compara tipo y avanza al siguiente
    '''
    if inicio >= len(lista):
        return []
    resultados = _buscar_tipo_rec(lista, tipo_norm, inicio + 1)
    if tipo_norm in normalizar_texto(lista[inicio][IDX_TIPO]):
        resultados = [lista[inicio]] + resultados
    return resultados


def buscar_x_tipo(tipo):
    resultados = _buscar_tipo_rec(paquetes, normalizar_texto(tipo))
    if len(resultados) == 0:
        print(f"  No se encontraron paquetes de tipo: {tipo}")
        return
    print(f"\n{SEPARADOR} PAQUETES {tipo.upper()} {SEPARADOR}")
    for paquete in resultados:
        mostrar_paquete(paquete)


# ============================================================
# BÚSQUEDA RECURSIVA POR PRECIO MÁXIMO
# ============================================================

def _buscar_precio_rec(lista, precio_max, inicio=0):
    '''
    Caso base  : fin de lista → []
    Caso recursivo: compara precio y avanza
    '''
    if inicio >= len(lista):
        return []
    resultados = _buscar_precio_rec(lista, precio_max, inicio + 1)
    if lista[inicio][IDX_PRECIO] <= precio_max:
        resultados = [lista[inicio]] + resultados
    return resultados


def buscar_x_precio(precio_max):
    resultados = _buscar_precio_rec(paquetes, precio_max)
    if len(resultados) == 0:
        precio_fmt = f"${precio_max:,.0f}".replace(",", ".")
        print(f"  No hay paquetes con precio igual o menor a {precio_fmt}")
        return
    precio_fmt = f"${precio_max:,.0f}".replace(",", ".")
    print(f"\n{SEPARADOR} PAQUETES HASTA {precio_fmt} POR PERSONA {SEPARADOR}")
    for paquete in resultados:
        mostrar_paquete(paquete)