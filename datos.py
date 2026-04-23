# =============================================================
#   SISTEMA DE BÚSQUEDA Y RESERVA DE PAQUETES TURÍSTICOS
#   Programación I – Algoritmos y Estructuras de Datos I
#   Docente: Ricardo Thompson
# =============================================================

# Estructura de cada paquete:
# [ id, destino, descripcion, precio, duracion_dias, fecha_salida, cupos_totales, cupos_disponibles ]

IDX_ID          = 0
IDX_DESTINO     = 1
IDX_DESCRIPCION = 2
IDX_PRECIO      = 3
IDX_DURACION    = 4
IDX_FECHA       = 5
IDX_CUPOS_TOT   = 6
IDX_CUPOS_DISP  = 7

paquetes = [
    ["P001", "Cancún",       "Resort todo incluido",      1500.00,  7, "15/07/2025", 20, 20],
    ["P002", "París",        "Tour cultural europeo",     2800.00, 10, "20/07/2025", 15, 15],
    ["P003", "Bariloche",    "Aventura en la Patagonia",   850.00,  5, "10/07/2025", 25, 25],
    ["P004", "Miami",        "Playa y shopping",          1200.00,  6, "01/08/2025", 18, 18],
    ["P005", "Machu Picchu", "Ruta inca histórica",        950.00,  8, "05/08/2025", 12, 12],
]

# Estructura de cada reserva:
# [ id_reserva, id_paquete, nombre_cliente, dni, cantidad_personas ]
reservas = []


def mostrar_paquete(paquete):
    # Recibe un paquete y muestra todos sus datos por pantalla con formato prolijo
    print("-" * 50)
    print("ID:          %s"    % paquete[IDX_ID])
    print("Destino:     %s"    % paquete[IDX_DESTINO])
    print("Descripción: %s"    % paquete[IDX_DESCRIPCION])
    print("Precio:      $%.2f" % paquete[IDX_PRECIO])
    print("Duración:    %d días" % paquete[IDX_DURACION])
    print("Salida:      %s"    % paquete[IDX_FECHA])
    print("Cupos disp.: %d / %d" % (paquete[IDX_CUPOS_DISP], paquete[IDX_CUPOS_TOT]))


def mostrar_todos_los_paquetes():
    # Recorre la lista de paquetes y muestra cada uno por pantalla
    # Si no hay paquetes cargados, avisa al usuario
    if len(paquetes) == 0:
        print("No hay paquetes cargados.")
        return
    print("\n========== PAQUETES DISPONIBLES ==========")
    for paquete in paquetes:
        mostrar_paquete(paquete)
    print("-" * 50)