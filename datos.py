import json

# ============================================================
# MODULO DE DATOS - AGENCIA DE VIAJES
# ============================================================
# Estructura de cada paquete:
# [ id, destino, tipo, descripcion,
#   dias, noches, alojamiento, pension, personas,
#   vuelos (lista de 2 opciones),
#   adicionales: autos (2 op), excursiones (2 op), traslados (2 op),
#   precio_x_persona, precio_paquete,
#   cupos_totales, cupos_disponibles ]
#
# Cada vuelo   : [empresa_ida, sal_ida, ing_ida, empresa_vta, sal_vta, ing_vta, escala, lugar_escala, espera]
# Cada auto    : [modelo, precio]
# Cada excursion: [descripcion, precio]
# Cada traslado : [precio]
# ============================================================

IDX_ID              = 0
IDX_DESTINO         = 1
IDX_TIPO            = 2
IDX_DESCRIPCION     = 3
IDX_DIAS            = 4
IDX_NOCHES          = 5
IDX_ALOJAMIENTO     = 6
IDX_PENSION         = 7
IDX_PERSONAS        = 8
IDX_VUELOS          = 9   # lista de 2 opciones de vuelo
IDX_AUTOS           = 10  # lista de 2 opciones de auto
IDX_EXCURSIONES     = 11  # lista de 2 opciones de excursion
IDX_TRASLADOS       = 12  # lista de 2 opciones de traslado
IDX_PRECIO          = 13  # precio base x persona
IDX_PRECIO_PAQUETE  = 14  # precio base total (2 personas)
IDX_CUPOS_TOT       = 15
IDX_CUPOS_DISP      = 16
IDX_PROMO           = 17  # porcentaje de descuento (0 = sin promocion)

# Índices dentro de cada vuelo
IDX_V_EMP_IDA   = 0
IDX_V_SAL_IDA   = 1
IDX_V_ING_IDA   = 2
IDX_V_EMP_VTA   = 3
IDX_V_SAL_VTA   = 4
IDX_V_ING_VTA   = 5
IDX_V_ESCALA    = 6
IDX_V_LUGAR_ESC = 7
IDX_V_ESPERA    = 8

# Índices dentro de cada auto
IDX_A_MODELO    = 0
IDX_A_PRECIO    = 1

# Índices dentro de cada excursión
IDX_E_DESC      = 0
IDX_E_PRECIO    = 1

# Índice dentro de cada traslado
IDX_T_PRECIO    = 0


# ============================================================
# PAQUETES TURÍSTICOS (DATOS ACTUALIZADOS DESDE EL EXCEL)
# ============================================================
paquetes = [

    # ──────────────── NACIONALES ────────────────

    ["P001", "Puerto Iguazú", "Nacional", "Cataratas del Iguazú - Resort todo incluido",
     5, 4, "Apart del Huesped 2", "Media", 2,
     # vuelos: [emp_ida, sal_ida, ing_ida, emp_vta, sal_vta, ing_vta, escala, lugar, espera]
     [
         ["JetSmart",   "06:10", "07:59", "JetSmart",   "19:20", "21:16", "N", "", ""],
         ["Aerolíneas", "10:00", "12:10", "Aerolíneas", "18:00", "20:10", "N", "", ""],
     ],
     # autos: [modelo, precio]
     [
         ["Toyota Yaris Xs",  850000],
         ["Toyota Etios",     950000],
     ],
     # excursiones: [descripcion, precio]
     [
         ["Cascadas Argentinas y Brasileñas",       145000],
         ["Cataratas del Iguazú - Lago Argentino",  100000],
     ],
     # traslados: [precio]
     [
         [130000],
         [145000],
     ],
     250000, 500000, 20, 20, 0],

    ["P002", "Bariloche", "Nacional", "Aventura en la Patagonia",
     5, 4, "Hotel Concorde", "Completa", 2,
     [
         ["Aerolíneas", "04:35", "07:00", "Aerolíneas", "21:40", "23:45", "N", "", ""],
         ["Aerolíneas", "06:30", "09:00", "Aerolíneas", "17:30", "19:35", "N", "", ""],
     ],
     [
         ["Citroën C4 Cactus",  690000],
         ["Toyota Yaris",      1000000],
     ],
     [
         ["Ruta de los 7 Lagos",                         155000],
         ["Cerro Tronador - Glaciar Ventisquero Negro",  130000],
     ],
     [
         [ 85000],
         [120000],
     ],
     450000, 900000, 20, 20, 0],

    ["P003", "Salta", "Nacional", "El Norte Argentino",
     5, 4, "Hotel Marilian", "Media", 2,
     [
         ["Aerolíneas", "05:00", "07:15", "Aerolíneas", "19:05", "21:10", "N", "", ""],
         ["JetSmart",   "10:15", "12:30", "JetSmart",   "16:00", "18:15", "N", "", ""],
     ],
     [
         ["Fiat Cronos",       300000],
         ["Citroën C4 Cactus", 650000],
     ],
     [
         ["Cafayate, Tierra del Vino",          70000],
         ["Salinas Grandes por Purmamarca",     80000],
     ],
     [
         [40000],
         [45000],
     ],
     380000, 760000, 20, 20, 0],

    ["P004", "Ushuaia", "Nacional", "El Fin del Mundo",
     6, 5, "Hotel Monaco", "Completa", 2,
     [
         ["JetSmart",   "18:00", "21:45", "JetSmart",   "21:00", "00:30", "N", "", ""],
         ["Aerolíneas", "01:30", "05:15", "Aerolíneas", "17:30", "21:00", "N", "", ""],
     ],
     [
         ["Toyota Hilux",        1000000],
         ["Chevrolet Tracker",    770000],
     ],
     [
         ["Parque Nac. T. del Fuego + Tren Fin del Mundo", 340000],
         ["Navegación por el Canal de Beagle",              240000],
     ],
     [
         [190000],
         [250000],
     ],
     560000, 1120000, 20, 20, 0],

    # ──────────────── INTERNACIONALES ────────────────

    ["P005", "Río de Janeiro", "Internacional", "Playas y maravillas de Brasil",
     6, 5, "Hotel Atlántico", "Completa", 2,
     [
         ["Aerolíneas", "06:00", "09:00", "Aerolíneas", "01:00", "04:30", "N", "", ""],
         ["Aerolíneas", "10:00", "13:00", "Aerolíneas", "19:30", "22:30", "N", "", ""],
     ],
     [
         ["Volkswagen Polo", 120000],
         ["Fiat Mobi",       140000],
     ],
     [
         ["Cristo Redentor + Pan de Azúcar", 130000],
         ["Arraial Do Cabo",                 130000],
     ],
     [
         [45000],
         [60000],
     ],
     740000, 1480000, 15, 15, 0],

    ["P006", "Búzios", "Internacional", "Paraíso playero en Brasil",
     6, 5, "Búzios Beach Resort", "Completa", 2,
     [
         ["Aerolíneas", "06:00", "09:00", "Aerolíneas", "19:15", "22:40", "N", "", ""],
         ["JetSmart",   "04:30", "07:30", "JetSmart",   "15:00", "18:00", "N", "", ""],
     ],
     [
         ["Nissan Sentra", 400000],
         ["Fiat Mobi",     200000],
     ],
     [
         ["Tour Río de Janeiro",       270000],
         ["Paseo en Barco por Búzios",  55000],
     ],
     [
         [250000],
         [100000],
     ],
     850000, 1700000, 15, 15, 0],

    ["P007", "Punta Cana", "Internacional", "Resort Caribeño todo incluido",
     8, 7, "Bahía Príncipe Explore Turquesa", "Completa", 2,
     [
         ["Arajet", "21:15", "04:10", "Latam",  "18:40", "06:05", "S", "LIMA", "1 HS"],
         ["Latam",  "10:00", "17:00", "Latam",  "18:00", "01:00", "N", "",     ""],
     ],
     [
         ["", 0],
         ["", 0],
     ],
     [
         ["Isla Saona Catamarán - Lancha",  200000],
         ["Santo Domingo City Tour",         200000],
     ],
     [
         [150000],
         [200000],
     ],
     2080000, 4160000, 15, 15, 0],

    ["P008", "Santiago de Chile", "Internacional", "La capital andina",
     7, 6, "Hotel Fundador", "Completa", 2,
     [
         ["Latam",    "09:00", "11:40", "Latam",    "17:00", "19:00", "N", "", ""],
         ["JetSmart", "05:45", "08:00", "JetSmart", "19:10", "21:20", "N", "", ""],
     ],
     [
         ["Suzuki Swift",  140000],
         ["Toyota Raize",  200000],
     ],
     [
         ["Laguna del Inca - Centro de Ski Portillo", 150000],
         ["Tour a Valle Nevado y Farellones",          100000],
     ],
     [
         [ 70000],
         [ 80000],
     ],
     500000, 1000000, 15, 15, 0],
]

# ============================================================
# RESERVAS y SESION
# ============================================================
reservas = []

sesion_activa = {
    "usuario":   "",
    "nombre":    "",
    "dni":       "",
    "email":     "",
    "clave":     "",
    "rol":       "",
    "celular":   "",
    "edad":      "",
    "sexo":      "",
    "fecha_nac": ""
}


# ============================================================
# MOSTRAR PAQUETE
# ============================================================

def _fmt(n):
    return f"${n:,.0f}".replace(",", ".")


def mostrar_paquete(paquete):
    print("-" * 60)
    print(f"ID:           {paquete[IDX_ID]}")
    print(f"Tipo:         {paquete[IDX_TIPO]}")
    print(f"Destino:      {paquete[IDX_DESTINO]}")
    print(f"Descripción:  {paquete[IDX_DESCRIPCION]}")
    print(f"Duración:     {paquete[IDX_DIAS]} días / {paquete[IDX_NOCHES]} noches")
    print(f"Alojamiento:  {paquete[IDX_ALOJAMIENTO]}")
    print(f"Pensión:      {paquete[IDX_PENSION]}")
    print(f"Personas:     {paquete[IDX_PERSONAS]}")

    print("  ── Opciones de Vuelo ──")
    for i, v in enumerate(paquete[IDX_VUELOS], 1):
        escala = f"  [Escala: {v[IDX_V_LUGAR_ESC]} — espera {v[IDX_V_ESPERA]}]" if v[IDX_V_ESCALA] == "S" else "  [Sin escala]"
        print(f"    Opción {i}: {v[IDX_V_EMP_IDA]} — IDA  {v[IDX_V_SAL_IDA]} → {v[IDX_V_ING_IDA]}"
              f"  |  {v[IDX_V_EMP_VTA]} — VUELTA  {v[IDX_V_SAL_VTA]} → {v[IDX_V_ING_VTA]}{escala}")

    print("  ── Adicionales ──")
    print("    Alquiler de Auto:")
    for i, a in enumerate(paquete[IDX_AUTOS], 1):
        if a[IDX_A_MODELO]:
            print(f"      Opción {i}: {a[IDX_A_MODELO]}  →  {_fmt(a[IDX_A_PRECIO])}")
        else:
            print(f"      Opción {i}: No disponible")

    print("    Excursiones:")
    for i, e in enumerate(paquete[IDX_EXCURSIONES], 1):
        print(f"      Opción {i}: {e[IDX_E_DESC]}  →  {_fmt(e[IDX_E_PRECIO])}")

    print("    Traslados:")
    for i, t in enumerate(paquete[IDX_TRASLADOS], 1):
        print(f"      Opción {i}: {_fmt(t[IDX_T_PRECIO])}")

    print(f"Precio base x persona:  {_fmt(paquete[IDX_PRECIO])}")
    print(f"Precio base paquete:    {_fmt(paquete[IDX_PRECIO_PAQUETE])}")
    # Si el paquete tiene una promocion activa (promo > 0), mostramos el precio rebajado.
    if len(paquete) > IDX_PROMO and paquete[IDX_PROMO] > 0:
        promo         = paquete[IDX_PROMO]
        promo_persona = paquete[IDX_PRECIO] * (100 - promo) // 100
        promo_paquete = paquete[IDX_PRECIO_PAQUETE] * (100 - promo) // 100
        print(f"PROMO:        {promo}% OFF")
        print(f"  Precio promo x persona: {_fmt(promo_persona)}")
        print(f"  Precio promo paquete:   {_fmt(promo_paquete)}")
    print(f"  * El precio varía según los adicionales seleccionados")
    print(f"Cupos disp.:  {paquete[IDX_CUPOS_DISP]} / {paquete[IDX_CUPOS_TOT]}")


def mostrar_todos_los_paquetes():
    if len(paquetes) == 0:
        print("No hay paquetes cargados.")
        return
    print("\n========== PAQUETES DISPONIBLES ==========")
    for paquete in paquetes:
        mostrar_paquete(paquete)
    print("-" * 60)


# ============================================================
# PERSISTENCIA DE PAQUETES (archivo JSON)
# ============================================================
# Se usa JSON porque cada paquete tiene listas anidadas (vuelos, autos,
# excursiones, traslados) que serian muy dificiles de guardar en CSV.
# Asi, los paquetes que el admin agrega/modifica/elimina se conservan
# entre ejecuciones del programa.

ARCHIVO_PAQUETES = "paquetes.json"


def cargar_paquetes():
    # Lee paquetes.json y reemplaza la lista 'paquetes'.
    # Si el archivo no existe, deja los paquetes por defecto.
    try:
        with open(ARCHIVO_PAQUETES, "r", encoding="utf-8") as archivo:
            datos_guardados = json.load(archivo)
        paquetes.clear()
        paquetes.extend(datos_guardados)
        # Compatibilidad: si un paquete guardado no tiene el campo promo, se lo agregamos.
        for p in paquetes:
            if len(p) <= IDX_PROMO:
                p.append(0)
    except FileNotFoundError:
        print("  (No existe paquetes.json, se usan los paquetes por defecto.)")
    except (OSError, json.JSONDecodeError) as e:
        print(f"  Error al cargar paquetes: {e}")


def guardar_paquetes():
    # Guarda la lista 'paquetes' completa en el archivo JSON.
    try:
        with open(ARCHIVO_PAQUETES, "w", encoding="utf-8") as archivo:
            json.dump(paquetes, archivo, indent=4, ensure_ascii=False)
    except OSError as e:
        print(f"  Error al guardar paquetes: {e}")