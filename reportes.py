from datos import IDX_CUPOS_TOT, IDX_PRECIO, mostrar_paquete, IDX_DESTINO, IDX_CUPOS_DISP, IDX_DESCRIPCION
from datos import paquetes

import random 

SEPARADOR = "=" * 5

def reporte_paquete_mas_caro_y_mas_barato():
    '''
    Muestra el paquete con el precio mas alto y el mas bajo
    '''
    if len(paquetes) == 0:
        print("No hay paquetes cargados para generar el reporte.")
        return

    mas_caro = paquetes[0]
    mas_barato = paquetes[0]

    for paquete in paquetes:
        if paquete[IDX_PRECIO] > mas_caro[IDX_PRECIO]:
            mas_caro = paquete
            
        if paquete[IDX_PRECIO] < mas_barato[IDX_PRECIO]:
            mas_barato = paquete

    print(f"\n{SEPARADOR} PAQUETE MAS CARO {SEPARADOR}")
    mostrar_paquete(mas_caro)

    print(f"\n{SEPARADOR} PAQUETE MAS BARATO {SEPARADOR}")
    mostrar_paquete(mas_barato)


def reporte_cupos_totales():
    if len(paquetes) == 0:
        print("No hay paquetes cargados.")
        return

    total_cupos = 0
    total_disponibles = 0

    print(f"\n{SEPARADOR} RESUMEN DE CUPOS POR PAQUETE {SEPARADOR}")

    for paquete in paquetes:
        destino = paquete[IDX_DESTINO]
        disponibles = paquete[IDX_CUPOS_DISP]
        totales = paquete[IDX_CUPOS_TOT]
        print(f"  {destino:15s} -> {disponibles:2d} / {totales:2d} cupos")

        total_cupos = total_cupos + totales
        total_disponibles = total_disponibles + disponibles

    print(SEPARADOR)
    print(f"  TOTAL GENERAL -> {total_disponibles} / {total_cupos} cupos")
    

def paquete_al_azar():
    '''
    Selecciona un paquete al azar y aplica descuentos aleatorios entre 5 y 20%
    '''
    if len(paquetes) == 0:
        print("No hay paquetes cargados")
        return
    
    paquete = random.choice(paquetes)
    descuento = random.randint(5, 20)
    precio_original = paquete[IDX_PRECIO]
    off_del_dia = precio_original * (1 - descuento / 100)
    
    print(f"\n{SEPARADOR} PAQUETE DEL DIA {SEPARADOR}")
    print(f" Destino: {paquete[IDX_DESTINO]}")
    print(f" Descripcion: {paquete[IDX_DESCRIPCION]}")
    print(f" Precio original: ${precio_original:.2f}")
    print(f" Descuento: {descuento}%")
    print(f" Precio del dia: ${off_del_dia:.2f}")
    print(f" Cupos disponible: {paquete[IDX_CUPOS_DISP]}")