from datos import  IDX_PRECIO, mostrar_paquete, IDX_DESTINO, IDX_CUPOS_DISP, IDX_DESCRIPCION
from datos import paquetes

import random 

SEPARADOR = "=" * 5

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