import json
from datos import (
    paquetes, reservas, sesion_activa,
    IDX_ID, IDX_DESTINO, IDX_PRECIO,
    IDX_CUPOS_DISP, IDX_CUPOS_TOT,
    mostrar_paquete
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
    return "R%03d" % (len(reservas) + 1)


def buscar_paquete_por_id(id_paquete):
    for paquete in paquetes:
        if paquete[IDX_ID].upper() == id_paquete.upper():
            return paquete
    return None


def confirmar_identidad():
    """
    Pide la clave al turista para confirmar la operación.
    Tiene 3 intentos.
    """
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
        paquete = buscar_paquete_por_id(id_paquete)
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

    # ── resumen ──
    total = paquete[IDX_PRECIO] * cantidad
    print("\n  --- Resumen de la reserva ---")
    print(f"  Destino  : {paquete[IDX_DESTINO]}")
    print(f"  Cliente  : {sesion_activa['nombre']}")
    print(f"  DNI      : {sesion_activa['dni']}")
    print(f"  Email    : {sesion_activa['email']}")
    print(f"  Personas : {cantidad}")
    print(f"  Total    : ${'%s' % f'{total:,.0f}'.replace(',', '.')}")

    # ── confirmar con clave ──
    print("\n  Para confirmar la reserva ingresá tu contraseña.")
    if not confirmar_identidad():
        print("  Reserva cancelada.")
        return

    # ── registrar reserva ──
    id_reserva  = generar_id_reserva()
    nueva_reserva = [
        id_reserva,
        paquete[IDX_ID],
        sesion_activa["nombre"],
        sesion_activa["dni"],
        sesion_activa["email"],
        cantidad,
        total
    ]
    reservas.append(nueva_reserva)
    paquete[IDX_CUPOS_DISP] -= cantidad
    guardar_reservas()

    print(f"\n  ✔ Reserva confirmada exitosamente.")
    print(f"  N° de reserva : {id_reserva}")
    print(f"  Se enviará un comprobante a {sesion_activa['email']}")


# ============================================================
# VER RESERVAS
# ============================================================

def mostrar_reserva(reserva):
    paquete     = buscar_paquete_por_id(reserva[1])
    destino     = paquete[IDX_DESTINO] if paquete else "Paquete no encontrado"
    print("-" * 50)
    print(f"  ID Reserva : {reserva[0]}")
    print(f"  Paquete    : {reserva[1]} — {destino}")
    print(f"  Cliente    : {reserva[2]}")
    print(f"  DNI        : {reserva[3]}")
    print(f"  Email      : {reserva[4]}")
    print(f"  Personas   : {reserva[5]}")
    print(f"  Total      : ${'%s' % f'{reserva[6]:,.0f}'.replace(',', '.')}")


def ver_todas_las_reservas():
    print("\n===== MIS RESERVAS =====")

    mis_reservas = [r for r in reservas if r[2] == sesion_activa["nombre"]]

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

    mis_reservas = [r for r in reservas if r[2] == sesion_activa["nombre"]]

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