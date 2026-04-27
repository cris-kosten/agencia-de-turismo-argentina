from datos import (
    paquetes, reservas,
    IDX_ID, IDX_DESTINO, IDX_PRECIO, IDX_CUPOS_DISP, IDX_CUPOS_TOT,
    mostrar_paquete
)

SEPARADOR = "=" * 5


def generar_id_reserva():
    return "R%03d" % (len(reservas) + 1)


def buscar_paquete_por_id(id_paquete):
    for paquete in paquetes:
        if paquete[IDX_ID].upper() == id_paquete.upper():
            return paquete
    return None


def validar_dni(dni):
    return dni.isdigit() and 7 <= len(dni) <= 8


def validar_cantidad(cantidad_str, cupos_disponibles):
    if not cantidad_str.isdigit():
        print("  La cantidad debe ser un número entero positivo.")
        return None
    cantidad = int(cantidad_str)
    if cantidad <= 0:
        print("  La cantidad debe ser mayor a cero.")
        return None
    if cantidad > cupos_disponibles:
        print("  No hay suficientes cupos. Disponibles: %d" % cupos_disponibles)
        return None
    return cantidad


def realizar_reserva():
    print("\n%s NUEVA RESERVA %s" % (SEPARADOR, SEPARADOR))

    # 1. ID del paquete
    id_paquete = input("  Ingrese el ID del paquete a reservar (ej: P001): ").strip()
    paquete = buscar_paquete_por_id(id_paquete)
    if paquete is None:
        print("  No existe un paquete con el ID '%s'." % id_paquete)
        return

    print("\n  Paquete seleccionado:")
    mostrar_paquete(paquete)

    if paquete[IDX_CUPOS_DISP] == 0:
        print("  Lo sentimos, este paquete no tiene cupos disponibles.")
        return

    # 2. Nombre del cliente
    nombre = input("\n  Nombre completo del cliente: ").strip()
    if nombre == "":
        print("  El nombre no puede estar vacío.")
        return

    # 3. DNI
    dni = input("  DNI del cliente: ").strip()
    if not validar_dni(dni):
        print("  DNI inválido. Debe tener entre 7 y 8 dígitos numéricos.")
        return

    # 4. Cantidad de personas
    cantidad_str = input("  Cantidad de personas (cupos disp.: %d): " % paquete[IDX_CUPOS_DISP]).strip()
    cantidad = validar_cantidad(cantidad_str, paquete[IDX_CUPOS_DISP])
    if cantidad is None:
        return

    # 5. Confirmación
    total = paquete[IDX_PRECIO] * cantidad
    print("\n  --- Resumen de la reserva ---")
    print("  Destino:    %s" % paquete[IDX_DESTINO])
    print("  Cliente:    %s" % nombre)
    print("  DNI:        %s" % dni)
    print("  Personas:   %d" % cantidad)
    print("  Total:      $%.2f" % total)

    confirmacion = input("\n  ¿Confirmar reserva? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("  Reserva cancelada.")
        return

    # 6. Actualizar cupos y registrar reserva
    paquete[IDX_CUPOS_DISP] -= cantidad

    id_reserva = generar_id_reserva()
    nueva_reserva = [id_reserva, paquete[IDX_ID], nombre, dni, cantidad]
    reservas.append(nueva_reserva)

    # 7. Comprobante
    print("\n  Reserva registrada exitosamente.")
    print("  ID de reserva: %s" % id_reserva)
    print("  Cupos restantes para '%s': %d" % (paquete[IDX_DESTINO], paquete[IDX_CUPOS_DISP]))


def mostrar_reserva(reserva):
    paquete = buscar_paquete_por_id(reserva[1])
    destino = paquete[IDX_DESTINO] if paquete else "Paquete no encontrado"
    precio_unit = paquete[IDX_PRECIO] if paquete else 0.0

    print("-" * 50)
    print("ID Reserva:  %s" % reserva[0])
    print("Paquete:     %s – %s" % (reserva[1], destino))
    print("Cliente:     %s" % reserva[2])
    print("DNI:         %s" % reserva[3])
    print("Personas:    %d" % reserva[4])
    print("Total:       $%.2f" % (precio_unit * reserva[4]))


def ver_todas_las_reservas():
    print("\n%s RESERVAS REGISTRADAS %s" % (SEPARADOR, SEPARADOR))

    if len(reservas) == 0:
        print("  No hay reservas registradas.")
        return

    for reserva in reservas:
        mostrar_reserva(reserva)
    print("-" * 50)
    print("  Total de reservas: %d" % len(reservas))

def cancelar_reserva():
    '''
    cancelar una reserva existente
    '''
    print("\n%s CANCELAR RESERVA %s" % (SEPARADOR, SEPARADOR))
    
    if len(reservas) == 0:
        print(" No se encontraron reservas registradas")
        return
    
    id_reserva = input("Ingrese el ID de la reserva a cancelar (ej: R001): ").strip().upper()
    
    resultados = [reserva for reserva in reservas if reserva[0] == id_reserva]
    
    if len(resultados) >0:
        reserva_encontrada = resultados[0]
    else:
        reserva_encontrada = None
        
    if reserva_encontrada is None:
        print("No existe una reserva con el ID '%s'." % id_reserva)
        return
    
    print("\n Reserva encontrada: ")
    mostrar_reserva(reserva_encontrada)
    
    confirmacion = input("\n ¿Desea confirmar su cancelacion? (S/N): ").strip().lower()
    if confirmacion != "s":
        print("La reserva no ha sido cancelada ")
        return
    
    paquete = buscar_paquete_por_id(reserva_encontrada[1])
    if paquete:
        paquete[IDX_CUPOS_DISP] += reserva_encontrada[4]
        
    reservas.remove(reserva_encontrada)
    print(" Reserva %s cancelada exitosamente" % id_reserva)