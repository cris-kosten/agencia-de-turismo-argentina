
# Estructura de cada paquete:
# [ id, destino, descripcion, precio, duracion_dias, fecha_salida, cupos_totales, cupos_disponibles, promo ]
# promo = porcentaje de descuento (0 significa "sin promocion")

IDX_ID          = 0
IDX_DESTINO     = 1
IDX_DESCRIPCION = 2
IDX_PRECIO      = 3
IDX_DURACION    = 4
IDX_FECHA       = 5
IDX_CUPOS_TOT   = 6
IDX_CUPOS_DISP  = 7
IDX_PROMO       = 8

paquetes = [
    ["P001", "Cancún",       "Resort todo incluido",      1500000,  7, "15/07/2025", 20, 20, 0],
    ["P002", "París",        "Tour cultural europeo",     2800000, 10, "20/07/2025", 15, 15, 0],
    ["P003", "Bariloche",    "Aventura en la Patagonia",   910000,  5, "10/07/2025", 25, 25, 0],
    ["P004", "Miami",        "Playa y shopping",          1200000,  6, "01/08/2025", 18, 18, 0],
    ["P005", "Machu Picchu", "Ruta inca histórica",        950000,  8, "05/08/2025", 12, 12, 0],
]

# Estructura de cada reserva:
# [ id_reserva, id_paquete, nombre_cliente, dni, cantidad_personas ]
reservas = []

sesion_activa = {
    "usuario": "",
    "nombre":  "",
    "dni":     "",
    "email":   "",
    "clave":   "",
    "rol":     ""
}

def mostrar_paquete(paquete):
    # Recibe un paquete y muestra todos sus datos por pantalla con formato prolijo
    print("-" * 50)
    print("ID:          %s"    % paquete[IDX_ID])
    print("Destino:     %s"    % paquete[IDX_DESTINO])
    print("Descripción: %s"    % paquete[IDX_DESCRIPCION])
    print("Precio:      $%s" % f"{paquete[IDX_PRECIO]:,.0f}".replace(",", "."))
    # Si el paquete tiene una promocion activa (promo > 0), mostramos
    # el descuento y el precio final ya rebajado.
    if paquete[IDX_PROMO] > 0:
        precio_final = paquete[IDX_PRECIO] * (100 - paquete[IDX_PROMO]) // 100
        print("PROMO:       %d%% OFF" % paquete[IDX_PROMO])
        print("Precio promo:$%s" % f"{precio_final:,.0f}".replace(",", "."))
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


# ============================================================
# PERSISTENCIA DE PAQUETES (archivo CSV, sin JSON)
# ============================================================
# Estructura del CSV (encabezado en la primera linea):
#   id,destino,descripcion,precio,duracion,fecha,cupos_tot,cupos_disp,promo

ARCHIVO_PAQUETES = "paquetes.csv"
ENCABEZADO_PAQUETES = "id,destino,descripcion,precio,duracion,fecha,cupos_tot,cupos_disp,promo"


def cargar_paquetes():
    # Lee paquetes.csv y reemplaza el contenido de la lista 'paquetes'.
    # Si el archivo no existe, deja los paquetes que ya estan por defecto.
    try:
        archivo = open(ARCHIVO_PAQUETES, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()

        # Vaciamos la lista actual para cargar lo que dice el archivo.
        paquetes.clear()
        for i in range(1, len(lineas)):
            linea = lineas[i].strip()
            if linea != "":
                campos = linea.split(",")
                # Los campos numericos se convierten de texto a entero.
                paquete = [
                    campos[IDX_ID],
                    campos[IDX_DESTINO],
                    campos[IDX_DESCRIPCION],
                    int(campos[IDX_PRECIO]),
                    int(campos[IDX_DURACION]),
                    campos[IDX_FECHA],
                    int(campos[IDX_CUPOS_TOT]),
                    int(campos[IDX_CUPOS_DISP]),
                    int(campos[IDX_PROMO])
                ]
                paquetes.append(paquete)
    except FileNotFoundError:
        # No existe todavia: usamos los paquetes por defecto de la lista.
        print("  (No existe paquetes.csv, se usan los paquetes por defecto.)")


def guardar_paquetes():
    # Guarda la lista 'paquetes' completa en el archivo CSV.
    try:
        archivo = open(ARCHIVO_PAQUETES, "w", encoding="utf-8")
        archivo.write(ENCABEZADO_PAQUETES + "\n")
        for paquete in paquetes:
            # Convertimos cada campo a texto para poder unirlos con comas.
            campos_texto = []
            for campo in paquete:
                campos_texto.append(str(campo))
            linea = ",".join(campos_texto)
            archivo.write(linea + "\n")
        archivo.close()
    except OSError:
        print("  No se pudo guardar el archivo de paquetes.")