from datos import IDX_CUPOS_TOT, IDX_PRECIO, mostrar_paquete, IDX_DESTINO, IDX_CUPOS_DISP
from datos import paquetes

SEPARADOR = "=" * 40

def reporte_paquete_mas_caro_y_mas_barato():

    if len(paquetes) == 0:
        print("No hay paquetes cargados para generar el reporte.")
        return

    # Suponemos que el primer paquete es el mas caro y tambien el mas barato
    # Despues los comparamos con los demas para confirmarlo
    
    mas_caro = paquetes[0]
    mas_barato = paquetes[0]

    # Recorremos todos los paquetes con un ciclo for
    for paquete in paquetes:
        
        # Si el precio del paquete actual es mayor que el de mas_caro,
        # entonces este paquete pasa a ser el nuevo mas_caro
        
        if paquete[IDX_PRECIO] > mas_caro[IDX_PRECIO]:
            mas_caro = paquete

        # Si el precio del paquete actual es menor que el de mas_barato,
        # entonces este paquete pasa a ser el nuevo mas_barato
        
        if paquete[IDX_PRECIO] < mas_barato[IDX_PRECIO]:
            mas_barato = paquete

    # Mostramos los resultados
    print(f"\n{SEPARADOR} PAQUETE MAS CARO {SEPARADOR}")
    mostrar_paquete(mas_caro)

    print(f"\n{SEPARADOR} PAQUETE MAS BARATO {SEPARADOR}")
    mostrar_paquete(mas_barato)


def reporte_promedio_de_precios():
    # Calcula y muestra el precio promedio de todos los paquetes turisticos. Si no hay paquetes, muestra un aviso.

    # sum() suma todos los precios de los paquetes
    # Usamos una lista por comprension para obtener solo los precios
    if len(paquetes) == 0:
        print("No hay paquetes cargados.")
        return
    suma_precios = sum(paquete[IDX_PRECIO] for paquete in paquetes)
    cantidad = len(paquetes)
    promedio = suma_precios / cantidad

    print(f"\n{SEPARADOR} PROMEDIO DE PRECIOS {SEPARADOR}")
    print(f"Hay {cantidad} paquete(s) cargado(s).")
    print(f"El precio promedio es: ${promedio:.2f}")


def reporte_cupos_totales():
    # Muestra un resumen de los cupos totales y disponibles de cada paquete. Tambien suma y muestra el total general de cupos ofrecidos por la agencia.
    print("ENTRAMOS A LA FUNCION")
    if len(paquetes) == 0:
        print("No hay paquetes cargados.")
        return

    total_cupos = 0
    total_disponibles = 0

    print(f"\n{SEPARADOR} RESUMEN DE CUPOS POR PAQUETE {SEPARADOR}")

    # Recorremos todos los paquetes y mostramos los cupos de cada uno
    
    for paquete in paquetes:
        destino = paquete[IDX_DESTINO]
        disponibles = paquete[IDX_CUPOS_DISP]
        totales = paquete[IDX_CUPOS_TOT]
        print(f"  {destino:15s} -> {disponibles:2d} / {totales:2d} cupos")

        # Acumulamos para el total general
        total_cupos = total_cupos + totales
        total_disponibles = total_disponibles + disponibles

    # Mostramos el total general
    print("-" * 5)
    print(f"  TOTAL GENERAL -> {total_disponibles} / {total_cupos} cupos")