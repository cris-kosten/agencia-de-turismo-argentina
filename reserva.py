import json
from datos import (
    paquetes, reservas, sesion_activa,
    IDX_ID, IDX_DESTINO, IDX_PRECIO, IDX_PROMO,
    IDX_CUPOS_DISP, IDX_VUELOS, IDX_AUTOS, IDX_EXCURSIONES, IDX_TRASLADOS,
    IDX_V_EMP_IDA, IDX_V_SAL_IDA, IDX_V_ING_IDA,
    IDX_V_EMP_VTA, IDX_V_SAL_VTA, IDX_V_ING_VTA,
    IDX_V_ESCALA, IDX_V_LUGAR_ESC, IDX_V_ESPERA,
    IDX_A_MODELO, IDX_A_PRECIO,
    IDX_E_DESC, IDX_E_PRECIO,
    IDX_T_PRECIO,
    mostrar_paquete, _fmt
)

ARCHIVO_RESERVAS = "reservas.json"


# ============================================================
# PERSISTENCIA
# ============================================================

def cargar_reservas():
    try:
        with open(ARCHIVO_RESERVAS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            reservas.extend(datos)
    except FileNotFoundError:
        pass
    except (OSError, json.JSONDecodeError) as e:
        print(f"  Error al cargar reservas: {e}")


def guardar_reservas():
    try:
        with open(ARCHIVO_RESERVAS, "w", encoding="utf-8") as archivo:
            json.dump(reservas, archivo, indent=4)
    except OSError as e:
        print(f"  Error al guardar reservas: {e}")


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def generar_id_reserva():
    # Genera un ID unico tipo "R001" tomando el mayor numero ya usado + 1.
    # Antes se usaba len(reservas)+1, pero eso repetia IDs al cancelar:
    # con R001 y R002, si se cancelaba R001 la siguiente volvia a ser R002.
    mayor = 0
    for reserva in reservas:
        numero = int(reserva[0][1:])   # saca la "R" inicial y lo pasa a entero
        if numero > mayor:
            mayor = numero
    return "R%03d" % (mayor + 1)


def buscar_paquete_por_id(id_paquete):
    for paquete in paquetes:
        if paquete[IDX_ID].upper() == id_paquete.upper():
            return paquete
    return None


def confirmar_identidad():
    intentos = 0
    while intentos < 3:
        clave = input("  Ingresá tu contraseña para confirmar: ").strip()
        if clave == sesion_activa["clave"]:
            return True
        intentos += 1
        restantes = 3 - intentos
        if restantes > 0:
            print(f"  Contraseña incorrecta. Intentos restantes: {restantes}")
    print("  Demasiados intentos fallidos.")
    return False


def _pedir_opcion(mensaje, opciones_validas):
    """Pide al usuario que elija entre las opciones válidas."""
    while True:
        valor = input(mensaje).strip().upper()
        if valor in opciones_validas:
            return valor
        print(f"  Opción inválida. Ingresá una de: {', '.join(opciones_validas)}")


# ============================================================
# SELECCIÓN DE VUELO
# ============================================================

def elegir_vuelo(paquete):
    """
    Muestra las 2 opciones de vuelo del paquete y el cliente elige una.
    Devuelve el índice elegido (0 o 1) y el vuelo seleccionado.
    """
    vuelos = paquete[IDX_VUELOS]

    print("\n  ── Opciones de Vuelo ──")
    for i, v in enumerate(vuelos, 1):
        escala = f"[Escala: {v[IDX_V_LUGAR_ESC]} — espera {v[IDX_V_ESPERA]}]" \
                 if v[IDX_V_ESCALA] == "S" else "[Sin escala]"
        print(f"    Opción {i}: {v[IDX_V_EMP_IDA]} — IDA  {v[IDX_V_SAL_IDA]} → {v[IDX_V_ING_IDA]}"
              f"  |  {v[IDX_V_EMP_VTA]} — VUELTA  {v[IDX_V_SAL_VTA]} → {v[IDX_V_ING_VTA]}  {escala}")

    opcion = _pedir_opcion("  ¿Qué opción de vuelo elegís? (1/2): ", ["1", "2"])
    idx = int(opcion) - 1
    vuelo_elegido = vuelos[idx]

    print(f"  ✔ Vuelo seleccionado: {vuelo_elegido[IDX_V_EMP_IDA]} — "
          f"IDA {vuelo_elegido[IDX_V_SAL_IDA]}→{vuelo_elegido[IDX_V_ING_IDA]}  |  "
          f"{vuelo_elegido[IDX_V_EMP_VTA]} — VUELTA {vuelo_elegido[IDX_V_SAL_VTA]}→{vuelo_elegido[IDX_V_ING_VTA]}")
    return idx, vuelo_elegido


# ============================================================
# SELECCIÓN DE AUTO
# ============================================================

def elegir_auto(paquete):
    """
    Pregunta si el cliente quiere alquilar un auto.
    Si quiere, muestra las 2 opciones y devuelve (idx, auto, precio).
    Si no quiere, devuelve (None, None, 0).
    """
    autos = paquete[IDX_AUTOS]
    disponibles = [a for a in autos if a[IDX_A_MODELO] != ""]

    if len(disponibles) == 0:
        print("\n  ── Alquiler de Auto ──")
        print("    No hay autos disponibles para este destino.")
        return None, None, 0

    print("\n  ── Alquiler de Auto ──")
    quiere = _pedir_opcion("  ¿Deseás alquilar un auto? (S/N): ", ["S", "N"])

    if quiere == "N":
        print("  ✔ Sin alquiler de auto.")
        return None, None, 0

    for i, a in enumerate(autos, 1):
        if a[IDX_A_MODELO] != "":
            print(f"    Opción {i}: {a[IDX_A_MODELO]}  →  {_fmt(a[IDX_A_PRECIO])}")
        else:
            print(f"    Opción {i}: No disponible")

    # Opciones válidas: solo las que tienen modelo
    validas = [str(i+1) for i, a in enumerate(autos) if a[IDX_A_MODELO] != ""]
    opcion  = _pedir_opcion(f"  ¿Qué auto elegís? ({'/'.join(validas)}): ", validas)
    idx     = int(opcion) - 1
    auto    = autos[idx]

    print(f"  ✔ Auto seleccionado: {auto[IDX_A_MODELO]}  →  {_fmt(auto[IDX_A_PRECIO])}")
    return idx, auto, auto[IDX_A_PRECIO]


# ============================================================
# SELECCIÓN DE EXCURSIÓN
# ============================================================

def elegir_excursion(paquete):
    """
    Pregunta si el cliente quiere hacer una excursión.
    Si quiere, muestra las 2 opciones y devuelve (idx, excursion, precio).
    Si no quiere, devuelve (None, None, 0).
    """
    excursiones = paquete[IDX_EXCURSIONES]

    print("\n  ── Actividades / Excursiones ──")
    quiere = _pedir_opcion("  ¿Deseás incluir una excursión? (S/N): ", ["S", "N"])

    if quiere == "N":
        print("  ✔ Sin excursión.")
        return None, None, 0

    for i, e in enumerate(excursiones, 1):
        print(f"    Opción {i}: {e[IDX_E_DESC]}  →  {_fmt(e[IDX_E_PRECIO])}")

    opcion = _pedir_opcion("  ¿Qué excursión elegís? (1/2): ", ["1", "2"])
    idx    = int(opcion) - 1
    exc    = excursiones[idx]

    print(f"  ✔ Excursión seleccionada: {exc[IDX_E_DESC]}  →  {_fmt(exc[IDX_E_PRECIO])}")
    return idx, exc, exc[IDX_E_PRECIO]


# ============================================================
# SELECCIÓN DE TRASLADO
# ============================================================

def elegir_traslado(paquete):
    """
    Pregunta si el cliente quiere traslado.
    Si quiere, muestra las 2 opciones y devuelve (idx, traslado, precio).
    Si no quiere, devuelve (None, None, 0).
    """
    traslados = paquete[IDX_TRASLADOS]

    print("\n  ── Traslado ──")
    quiere = _pedir_opcion("  ¿Deseás incluir traslado? (S/N): ", ["S", "N"])

    if quiere == "N":
        print("  ✔ Sin traslado.")
        return None, None, 0

    for i, t in enumerate(traslados, 1):
        print(f"    Opción {i}: {_fmt(t[IDX_T_PRECIO])}")

    opcion    = _pedir_opcion("  ¿Qué opción de traslado elegís? (1/2): ", ["1", "2"])
    idx       = int(opcion) - 1
    traslado  = traslados[idx]

    print(f"  ✔ Traslado seleccionado: {_fmt(traslado[IDX_T_PRECIO])}")
    return idx, traslado, traslado[IDX_T_PRECIO]


# ============================================================
# RESUMEN FINAL DE COSTOS
# ============================================================

def mostrar_resumen_costos(paquete, cantidad,
                            vuelo_idx,
                            auto_idx,  auto_precio,
                            exc_idx,   exc_precio,
                            tras_idx,  tras_precio):
    """
    Muestra el desglose completo del costo y devuelve
    (total_x_persona, total_paquete).
    """
    precio_base = paquete[IDX_PRECIO]
    # Si el paquete tiene una promocion activa, se aplica al precio por persona.
    promo = paquete[IDX_PROMO] if len(paquete) > IDX_PROMO else 0
    if promo > 0:
        precio_base = precio_base * (100 - promo) // 100
    adicionales   = auto_precio + exc_precio + tras_precio
    total_persona = precio_base + adicionales
    total_paquete = total_persona * cantidad

    vuelo  = paquete[IDX_VUELOS][vuelo_idx]

    print("\n" + "=" * 55)
    print("           RESUMEN DE TU PAQUETE")
    print("=" * 55)
    print(f"  Destino       : {paquete[IDX_DESTINO]}")
    print(f"  Cliente       : {sesion_activa['nombre']}")
    print(f"  DNI           : {sesion_activa['dni']}")
    print(f"  Email         : {sesion_activa['email']}")
    print(f"  Personas      : {cantidad}")
    print("-" * 55)
    print("  VUELO ELEGIDO:")
    escala = f"  [Escala: {vuelo[IDX_V_LUGAR_ESC]} — espera {vuelo[IDX_V_ESPERA]}]" \
             if vuelo[IDX_V_ESCALA] == "S" else "  [Sin escala]"
    print(f"    IDA    : {vuelo[IDX_V_EMP_IDA]}  {vuelo[IDX_V_SAL_IDA]} → {vuelo[IDX_V_ING_IDA]}")
    print(f"    VUELTA : {vuelo[IDX_V_EMP_VTA]}  {vuelo[IDX_V_SAL_VTA]} → {vuelo[IDX_V_ING_VTA]}{escala}")
    print("-" * 55)
    print("  DESGLOSE DE COSTOS (por persona):")
    if promo > 0:
        print(f"    Precio de lista         : {_fmt(paquete[IDX_PRECIO])}")
        print(f"    Promoción aplicada      : {promo}% OFF")
        print(f"    Precio con promoción    : {_fmt(precio_base)}")
    else:
        print(f"    Precio base del paquete : {_fmt(precio_base)}")

    if auto_precio > 0:
        auto        = paquete[IDX_AUTOS][auto_idx] if auto_idx is not None else None
        nombre_auto = auto[IDX_A_MODELO] if auto else ""
        print(f"    Alquiler de auto        : {nombre_auto}  {_fmt(auto_precio)}")
    else:
        print(f"    Alquiler de auto        : No incluido")

    if exc_precio > 0:
        exc = paquete[IDX_EXCURSIONES][exc_idx]
        print(f"    Excursión               : {exc[IDX_E_DESC]}")
        print(f"                              {_fmt(exc_precio)}")
    else:
        print(f"    Excursión               : No incluida")

    if tras_precio > 0:
        print(f"    Traslado                : {_fmt(tras_precio)}")
    else:
        print(f"    Traslado                : No incluido")

    print("-" * 55)
    print(f"  TOTAL POR PERSONA         : {_fmt(total_persona)}")
    print(f"  TOTAL PAQUETE ({cantidad} personas): {_fmt(total_paquete)}")
    print("=" * 55)

    return total_persona, total_paquete


# ============================================================
# REALIZAR RESERVA
# ============================================================

def realizar_reserva():
    print("\n===== NUEVA RESERVA =====")

    # ── mostrar paquetes disponibles ──
    disponibles = [p for p in paquetes if p[IDX_CUPOS_DISP] > 0]
    if not disponibles:
        print("  No hay paquetes con cupos disponibles.")
        return

    for p in disponibles:
        mostrar_paquete(p)

    # ── seleccionar paquete ──
    while True:
        id_paquete = input("\n  Ingresá el ID del paquete a reservar (ej: P001): ").strip()
        paquete    = buscar_paquete_por_id(id_paquete)
        if paquete is None:
            print(f"  No existe un paquete con el ID '{id_paquete}'.")
        elif paquete[IDX_CUPOS_DISP] == 0:
            print("  Ese paquete no tiene cupos disponibles.")
        else:
            break

    # ── cantidad de personas ──
    while True:
        cantidad_str = input(f"  Cantidad de personas (cupos disp.: {paquete[IDX_CUPOS_DISP]}): ").strip()
        if not cantidad_str.isdigit():
            print("  Ingresá un número válido.")
        elif int(cantidad_str) <= 0:
            print("  La cantidad debe ser mayor a cero.")
        elif int(cantidad_str) > paquete[IDX_CUPOS_DISP]:
            print(f"  No hay suficientes cupos. Disponibles: {paquete[IDX_CUPOS_DISP]}")
        else:
            cantidad = int(cantidad_str)
            break

    # ── elección de adicionales ──
    print("\n  A continuación personalizá tu paquete:")

    vuelo_idx, vuelo_elegido          = elegir_vuelo(paquete)
    auto_idx,  auto_elegido,  p_auto  = elegir_auto(paquete)
    exc_idx,   exc_elegida,   p_exc   = elegir_excursion(paquete)
    tras_idx,  tras_elegido,  p_tras  = elegir_traslado(paquete)

    # ── resumen y totales ──
    total_persona, total_paquete = mostrar_resumen_costos(
        paquete, cantidad,
        vuelo_idx,
        auto_idx,  p_auto,
        exc_idx,   p_exc,
        tras_idx,  p_tras
    )

    # ── confirmar con clave ──
    print("\n  Para confirmar la reserva ingresá tu contraseña.")
    if not confirmar_identidad():
        print("  Reserva cancelada.")
        return

    # ── armar descripciones de los adicionales elegidos ──
    # Se guardan como texto para poder mostrarlos despues en "ver mis reservas",
    # sin depender de que el paquete siga existiendo o no cambie.
    v = vuelo_elegido
    if v[IDX_V_ESCALA] == "S":
        escala_txt = f" (escala {v[IDX_V_LUGAR_ESC]}, espera {v[IDX_V_ESPERA]})"
    else:
        escala_txt = " (sin escala)"
    vuelo_txt = (f"{v[IDX_V_EMP_IDA]} IDA {v[IDX_V_SAL_IDA]}->{v[IDX_V_ING_IDA]} | "
                 f"{v[IDX_V_EMP_VTA]} VUELTA {v[IDX_V_SAL_VTA]}->{v[IDX_V_ING_VTA]}{escala_txt}")

    if p_auto > 0 and auto_elegido is not None:
        auto_txt = f"{auto_elegido[IDX_A_MODELO]} ({_fmt(p_auto)})"
    else:
        auto_txt = "No incluido"

    if p_exc > 0 and exc_elegida is not None:
        exc_txt = f"{exc_elegida[IDX_E_DESC]} ({_fmt(p_exc)})"
    else:
        exc_txt = "No incluida"

    if p_tras > 0:
        tras_txt = _fmt(p_tras)
    else:
        tras_txt = "No incluido"

    # ── registrar reserva ──
    id_reserva    = generar_id_reserva()
    nueva_reserva = [
        id_reserva,
        paquete[IDX_ID],
        sesion_activa["nombre"],
        sesion_activa["dni"],
        sesion_activa["email"],
        cantidad,
        total_paquete,
        vuelo_txt,   # adicionales elegidos
        auto_txt,
        exc_txt,
        tras_txt
    ]
    reservas.append(nueva_reserva)
    paquete[IDX_CUPOS_DISP] -= cantidad
    guardar_reservas()

    print("\n  ✔ Reserva confirmada exitosamente.")
    print(f"  N° de reserva : {id_reserva}")
    print(f"  Se enviará un comprobante a {sesion_activa['email']}")


# ============================================================
# VER RESERVAS
# ============================================================

def mostrar_reserva(reserva):
    paquete = buscar_paquete_por_id(reserva[1])
    destino = paquete[IDX_DESTINO] if paquete else "Paquete no encontrado"
    print("-" * 50)
    print(f"  ID Reserva : {reserva[0]}")
    print(f"  Paquete    : {reserva[1]} — {destino}")
    print(f"  Cliente    : {reserva[2]}")
    print(f"  DNI        : {reserva[3]}")
    print(f"  Email      : {reserva[4]}")
    print(f"  Personas   : {reserva[5]}")
    print(f"  Total      : {_fmt(reserva[6])}")

    # Adicionales elegidos (solo si la reserva los tiene guardados).
    if len(reserva) > 7:
        print(f"  Vuelo      : {reserva[7]}")
        print(f"  Auto       : {reserva[8]}")
        print(f"  Excursión  : {reserva[9]}")
        print(f"  Traslado   : {reserva[10]}")


def ver_todas_las_reservas():
    print("\n===== MIS RESERVAS =====")
    mis_reservas = [r for r in reservas if r[3] == sesion_activa["dni"]]
    if not mis_reservas:
        print("  No tenés reservas registradas.")
        return
    for reserva in mis_reservas:
        mostrar_reserva(reserva)
    print("-" * 50)
    print(f"  Total de reservas: {len(mis_reservas)}")


# ============================================================
# CANCELAR RESERVA
# ============================================================

def cancelar_reserva():
    print("\n===== CANCELAR RESERVA =====")
    mis_reservas = [r for r in reservas if r[3] == sesion_activa["dni"]]

    if not mis_reservas:
        print("  No tenés reservas para cancelar.")
        return

    for reserva in mis_reservas:
        mostrar_reserva(reserva)

    while True:
        id_reserva = input("\n  Ingresá el ID de la reserva a cancelar (ej: R001): ").strip().upper()
        ids        = [r[0] for r in mis_reservas]
        if id_reserva not in ids:
            print(f"  No existe la reserva '{id_reserva}'.")
        else:
            break

    reserva_encontrada = mis_reservas[ids.index(id_reserva)]
    mostrar_reserva(reserva_encontrada)

    print("\n  Para cancelar ingresá tu contraseña.")
    if not confirmar_identidad():
        print("  Cancelación abortada.")
        return

    paquete = buscar_paquete_por_id(reserva_encontrada[1])
    if paquete:
        paquete[IDX_CUPOS_DISP] += reserva_encontrada[5]

    reservas.remove(reserva_encontrada)
    guardar_reservas()
    print(f"  ✔ Reserva {id_reserva} cancelada. Cupo devuelto al paquete.")


cargar_reservas()