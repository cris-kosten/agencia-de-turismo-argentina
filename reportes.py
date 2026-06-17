# ============================================================
# MODULO DE REPORTES
# Reporte matricial de paquetes: NACIONAL e INTERNACIONAL
# ============================================================

from datos import (
    paquetes, reservas,
    IDX_ID, IDX_DESTINO,
    IDX_CUPOS_TOT, IDX_CUPOS_DISP,
)
from busqueda import normalizar_texto

SEPARADOR = "=" * 5

# -- Indices de columna de la matriz del reporte (evita numeros magicos) --
COL_DESTINO  = 0
COL_CUPOS    = 1
COL_VENDIDOS = 2
COL_INGRESOS = 3

# ============================================================
# CLASIFICACION NACIONAL / INTERNACIONAL
# ============================================================
# Conjunto con los destinos nacionales (Argentina). Al ser una agencia
# argentina, todo destino que no este aca se considera internacional.
DESTINOS_NACIONALES = {
    "bariloche", "mendoza",
}


def es_nacional(destino):
    # Devuelve True si el destino es argentino.
    # Se compara en minusculas y sin tildes para no fallar por el formato.
    # Se usa 'in' como subcadena para tolerar nombres largos
    # (ej: "San Carlos de Bariloche" contiene "bariloche").
    destino_normalizado = normalizar_texto(destino)
    for nacional in DESTINOS_NACIONALES:
        if nacional in destino_normalizado:
            return True
    return False


# ============================================================
# CONSTRUCCION DE LA MATRIZ
# ============================================================

def calcular_ingresos(paquete):
    # Suma cuanto facturo un paquete recorriendo las reservas que lo apuntan.
    # reserva = [ id, id_paquete, nombre, dni, email, cantidad, total, metodo, estado ]
    # El total facturado ya esta guardado en la posicion 6 de cada reserva.
    total = 0
    for reserva in reservas:
        if reserva[1] == paquete[IDX_ID]:
            total = total + reserva[6]
    return total


def armar_matriz(es_nacional_buscado):
    # Arma una matriz (lista de listas) con una fila por destino.
    # es_nacional_buscado: True -> solo nacionales / False -> solo internacionales.
    matriz = []
    for paquete in paquetes:
        if es_nacional(paquete[IDX_DESTINO]) == es_nacional_buscado:
            vendidos = paquete[IDX_CUPOS_TOT] - paquete[IDX_CUPOS_DISP]
            ingresos = calcular_ingresos(paquete)
            fila = [
                paquete[IDX_DESTINO],
                paquete[IDX_CUPOS_TOT],
                vendidos,
                ingresos,
            ]
            matriz.append(fila)
    return matriz


# ============================================================
# RECORRIDO RECURSIVO DE LA MATRIZ
# ============================================================

def formatear_pesos(monto):
    # Devuelve el monto con separador de miles, igual estilo que el resto del sistema.
    return "$" + ("%s" % f"{monto:,.0f}").replace(",", ".")


def imprimir_filas(matriz, fila=0):
    # Imprime la matriz FILA POR FILA en forma RECURSIVA (sin usar for).
    # el caso base: ya no quedan filas por imprimir.
    if fila >= len(matriz):
        return
    destino  = matriz[fila][COL_DESTINO]
    cupos    = matriz[fila][COL_CUPOS]
    vendidos = matriz[fila][COL_VENDIDOS]
    ingresos = matriz[fila][COL_INGRESOS]

    if cupos > 0:
        ocupacion = vendidos * 100 // cupos
    else:
        ocupacion = 0

    print("  %-22s %6d %9d %7d%%   %s" % (
        destino, cupos, vendidos, ocupacion, formatear_pesos(ingresos)
    ))
    # Llamada recursiva con la siguiente fila.
    imprimir_filas(matriz, fila + 1)


def total_columna(matriz, columna, fila=0):
    # Suma una COLUMNA de la matriz en forma RECURSIVA (sin usar for ni sum()).
    # Caso base: no quedan filas -> aporta 0.
    if fila >= len(matriz):
        return 0
    return matriz[fila][columna] + total_columna(matriz, columna, fila + 1)


# ============================================================
# IMPRESION DE UN BLOQUE DEL REPORTE
# ============================================================

def mostrar_bloque(titulo, matriz):
    print(f"\n{SEPARADOR} {titulo} {SEPARADOR}")
    if len(matriz) == 0:
        print("  (No hay paquetes en esta categoria.)")
        return

    print("  %-22s %6s %9s %8s   %s" % ("DESTINO", "CUPOS", "VENDIDOS", "OCUP.", "INGRESOS"))
    print("  " + "-" * 56)

    imprimir_filas(matriz)   # recorrido recursivo

    total_cupos    = total_columna(matriz, COL_CUPOS)      # suma recursiva
    total_vendidos = total_columna(matriz, COL_VENDIDOS)   # suma recursiva
    total_ingresos = total_columna(matriz, COL_INGRESOS)   # suma recursiva

    print("  " + "-" * 56)
    print("  %-22s %6d %9d %8s   %s" % (
        "TOTALES", total_cupos, total_vendidos, "", formatear_pesos(total_ingresos)
    ))


# ============================================================
# REPORTE PRINCIPAL
# ============================================================

def reporte_matricial():
    print("\n" + "=" * 64)
    print("   REPORTE MATRICIAL DE PAQUETES (NACIONAL / INTERNACIONAL)")
    print("=" * 64)

    if len(paquetes) == 0:
        print("  No hay paquetes cargados.")
        return

    matriz_nacional      = armar_matriz(True)
    matriz_internacional = armar_matriz(False)

    mostrar_bloque("PAQUETES NACIONALES", matriz_nacional)
    mostrar_bloque("PAQUETES INTERNACIONALES", matriz_internacional)

    # -- Resumen general combinando ambas matrices (tambien recursivo) --
    ingresos_nac = total_columna(matriz_nacional, COL_INGRESOS)
    ingresos_int = total_columna(matriz_internacional, COL_INGRESOS)
    vendidos_nac = total_columna(matriz_nacional, COL_VENDIDOS)
    vendidos_int = total_columna(matriz_internacional, COL_VENDIDOS)

    print("\n" + "=" * 64)
    print("   RESUMEN GENERAL")
    print("=" * 64)
    print("  Plazas vendidas nacionales....: %d" % vendidos_nac)
    print("  Plazas vendidas internacionales: %d" % vendidos_int)
    print("  Ingresos nacionales...........: %s" % formatear_pesos(ingresos_nac))
    print("  Ingresos internacionales......: %s" % formatear_pesos(ingresos_int))
    print("  INGRESOS TOTALES..............: %s" % formatear_pesos(ingresos_nac + ingresos_int))
