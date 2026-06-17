# ============================================================
# MODULO DE ADMINISTRACION - PANEL DEL VENDEDOR/ADMIN
# ============================================================
# Funciones disponibles para el administrador:
#   1. Agregar un nuevo paquete
#   2. Modificar un paquete existente
#   3. Eliminar un paquete
#   4. Ver disponibilidad de todos los paquetes
#   5. Ver todos los clientes que compraron paquetes
#   6. Ver reservas por paquete
# ============================================================

from datos import (
    paquetes, reservas, sesion_activa,
    mostrar_paquete, mostrar_todos_los_paquetes, guardar_paquetes, _fmt,
    IDX_ID, IDX_DESTINO, IDX_TIPO, IDX_DESCRIPCION,
    IDX_DIAS, IDX_NOCHES, IDX_ALOJAMIENTO, IDX_PENSION,
    IDX_PERSONAS, IDX_VUELOS, IDX_AUTOS, IDX_EXCURSIONES,
    IDX_TRASLADOS, IDX_PRECIO, IDX_PRECIO_PAQUETE,
    IDX_CUPOS_TOT, IDX_CUPOS_DISP, IDX_PROMO,
    IDX_V_EMP_IDA, IDX_V_SAL_IDA, IDX_V_ING_IDA,
    IDX_V_EMP_VTA, IDX_V_SAL_VTA, IDX_V_ING_VTA,
    IDX_V_ESCALA, IDX_V_LUGAR_ESC, IDX_V_ESPERA,
    IDX_A_MODELO, IDX_A_PRECIO,
    IDX_E_DESC, IDX_E_PRECIO,
    IDX_T_PRECIO
)

SEPARADOR = "=" * 5


# ============================================================
# UTILIDADES INTERNAS
# ============================================================

def _buscar_paquete_por_id(id_paquete):
    """Devuelve el paquete con ese ID o None si no existe."""
    for paquete in paquetes:
        if paquete[IDX_ID].upper() == id_paquete.upper():
            return paquete
    return None


def _generar_id():
    """Genera el próximo ID de paquete (P009, P010, ...)."""
    if len(paquetes) == 0:
        return "P001"
    ultimo = max(int(p[IDX_ID][1:]) for p in paquetes)
    return "P%03d" % (ultimo + 1)


def _pedir_entero(mensaje, minimo=None, maximo=None):
    """Pide un entero validando rango opcional."""
    while True:
        valor_str = input(mensaje).strip()
        if not valor_str.isdigit():
            print("  Debe ingresar un número entero positivo.")
            continue
        valor = int(valor_str)
        if minimo is not None and valor < minimo:
            print(f"  El valor mínimo es {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"  El valor máximo es {maximo}.")
            continue
        return valor


def _pedir_texto(mensaje, puede_vacio=False):
    """Pide un texto no vacío (a menos que se permita vacío)."""
    while True:
        valor = input(mensaje).strip()
        if valor == "" and not puede_vacio:
            print("  El campo no puede estar vacío.")
            continue
        return valor


def _pedir_sn(mensaje):
    """Pide S o N."""
    while True:
        valor = input(mensaje).strip().upper()
        if valor in ("S", "N"):
            return valor
        print("  Ingresá S o N.")


# ============================================================
# INGRESAR UN VUELO
# ============================================================

def _ingresar_vuelo(numero):
    print(f"\n    ── Vuelo Opción {numero} ──")
    emp_ida     = _pedir_texto("      Aerolínea IDA      : ")
    sal_ida     = _pedir_texto("      Horario salida IDA  (HH:MM): ")
    ing_ida     = _pedir_texto("      Horario llegada IDA (HH:MM): ")
    emp_vta     = _pedir_texto("      Aerolínea VUELTA    : ")
    sal_vta     = _pedir_texto("      Horario salida VUELTA  (HH:MM): ")
    ing_vta     = _pedir_texto("      Horario llegada VUELTA (HH:MM): ")
    escala      = _pedir_sn   ("      ¿Tiene escala? (S/N): ")
    lugar_esc   = ""
    espera      = ""
    if escala == "S":
        lugar_esc = _pedir_texto("      Lugar de escala: ")
        espera    = _pedir_texto("      Tiempo de espera (ej: 1 hs): ")
    return [emp_ida, sal_ida, ing_ida, emp_vta, sal_vta, ing_vta,
            escala, lugar_esc, espera]


# ============================================================
# INGRESAR ADICIONALES
# ============================================================

def _ingresar_auto(numero):
    print(f"\n    ── Auto Opción {numero} ──")
    disponible = _pedir_sn("      ¿Hay auto disponible? (S/N): ")
    if disponible == "N":
        return ["", 0]
    modelo = _pedir_texto("      Modelo: ")
    precio = _pedir_entero("      Precio: $", minimo=0)
    return [modelo, precio]


def _ingresar_excursion(numero):
    print(f"\n    ── Excursión Opción {numero} ──")
    desc   = _pedir_texto("      Descripción: ")
    precio = _pedir_entero("      Precio: $", minimo=0)
    return [desc, precio]


def _ingresar_traslado(numero):
    print(f"\n    ── Traslado Opción {numero} ──")
    precio = _pedir_entero("      Precio: $", minimo=0)
    return [precio]


# ============================================================
# 1. AGREGAR PAQUETE
# ============================================================

def agregar_paquete():
    print(f"\n{SEPARADOR} AGREGAR NUEVO PAQUETE {SEPARADOR}")

    nuevo_id = _generar_id()
    print(f"  ID asignado automáticamente: {nuevo_id}")

    destino     = _pedir_texto("  Destino         : ")
    tipo        = ""
    while tipo not in ("Nacional", "Internacional"):
        tipo = _pedir_texto("  Tipo (Nacional / Internacional): ").capitalize()
        if tipo not in ("Nacional", "Internacional"):
            print("  Ingresá 'Nacional' o 'Internacional'.")
    descripcion = _pedir_texto("  Descripción      : ")
    dias        = _pedir_entero("  Días             : ", minimo=1)
    noches      = _pedir_entero("  Noches           : ", minimo=1)
    alojamiento = _pedir_texto("  Alojamiento      : ")
    pension     = ""
    while pension not in ("Media", "Completa"):
        pension = _pedir_texto("  Pensión (Media / Completa): ").capitalize()
        if pension not in ("Media", "Completa"):
            print("  Ingresá 'Media' o 'Completa'.")
    personas    = _pedir_entero("  Personas         : ", minimo=1)

    print("\n  ── VUELOS ──")
    vuelos = [_ingresar_vuelo(1), _ingresar_vuelo(2)]

    print("\n  ── AUTOS ──")
    autos = [_ingresar_auto(1), _ingresar_auto(2)]

    print("\n  ── EXCURSIONES ──")
    excursiones = [_ingresar_excursion(1), _ingresar_excursion(2)]

    print("\n  ── TRASLADOS ──")
    traslados = [_ingresar_traslado(1), _ingresar_traslado(2)]

    precio_x_persona = _pedir_entero("\n  Precio base x persona: $", minimo=1)
    # El precio del paquete se calcula automáticamente para que sea coherente
    # con el precio por persona y la cantidad de personas base.
    precio_paquete   = precio_x_persona * personas
    cupos            = _pedir_entero("  Cupos totales        : ", minimo=1)

    nuevo_paquete = [
        nuevo_id, destino, tipo, descripcion,
        dias, noches, alojamiento, pension, personas,
        vuelos, autos, excursiones, traslados,
        precio_x_persona, precio_paquete,
        cupos, cupos,
        0               # promo: el paquete nace sin promocion
    ]

    paquetes.append(nuevo_paquete)
    guardar_paquetes()
    print(f"\n  ✔ Paquete '{destino}' agregado con ID {nuevo_id}.")


# ============================================================
# 2. MODIFICAR PAQUETE
# ============================================================

def modificar_paquete():
    print(f"\n{SEPARADOR} MODIFICAR PAQUETE {SEPARADOR}")
    mostrar_todos_los_paquetes()

    id_paquete = _pedir_texto("\n  Ingresá el ID del paquete a modificar: ").upper()
    paquete = _buscar_paquete_por_id(id_paquete)

    if paquete is None:
        print(f"  No existe un paquete con el ID '{id_paquete}'.")
        return

    print(f"\n  Modificando: {paquete[IDX_DESTINO]} ({paquete[IDX_ID]})")
    print("  (Presioná Enter para mantener el valor actual)\n")

    # ── Datos básicos ──
    nuevo_destino = input(f"  Destino [{paquete[IDX_DESTINO]}]: ").strip()
    if nuevo_destino:
        paquete[IDX_DESTINO] = nuevo_destino

    nuevo_tipo = input(f"  Tipo [{paquete[IDX_TIPO]}]: ").strip().capitalize()
    if nuevo_tipo in ("Nacional", "Internacional"):
        paquete[IDX_TIPO] = nuevo_tipo

    nueva_desc = input(f"  Descripción [{paquete[IDX_DESCRIPCION]}]: ").strip()
    if nueva_desc:
        paquete[IDX_DESCRIPCION] = nueva_desc

    nueva_dias = input(f"  Días [{paquete[IDX_DIAS]}]: ").strip()
    if nueva_dias.isdigit() and int(nueva_dias) > 0:
        paquete[IDX_DIAS] = int(nueva_dias)

    nueva_noches = input(f"  Noches [{paquete[IDX_NOCHES]}]: ").strip()
    if nueva_noches.isdigit() and int(nueva_noches) > 0:
        paquete[IDX_NOCHES] = int(nueva_noches)

    nuevo_aloj = input(f"  Alojamiento [{paquete[IDX_ALOJAMIENTO]}]: ").strip()
    if nuevo_aloj:
        paquete[IDX_ALOJAMIENTO] = nuevo_aloj

    nueva_pension = input(f"  Pensión [{paquete[IDX_PENSION]}]: ").strip().capitalize()
    if nueva_pension in ("Media", "Completa"):
        paquete[IDX_PENSION] = nueva_pension

    # ── Precios y cupos ──
    nuevo_precio_pp = input(f"  Precio x persona [{_fmt(paquete[IDX_PRECIO])}]: $").strip()
    if nuevo_precio_pp.isdigit() and int(nuevo_precio_pp) > 0:
        paquete[IDX_PRECIO] = int(nuevo_precio_pp)

    # El precio del paquete se recalcula para mantener la coherencia.
    paquete[IDX_PRECIO_PAQUETE] = paquete[IDX_PRECIO] * paquete[IDX_PERSONAS]

    nuevos_cupos = input(f"  Cupos totales [{paquete[IDX_CUPOS_TOT]}]: ").strip()
    if nuevos_cupos.isdigit() and int(nuevos_cupos) > 0:
        diferencia = int(nuevos_cupos) - paquete[IDX_CUPOS_TOT]
        paquete[IDX_CUPOS_TOT]  = int(nuevos_cupos)
        paquete[IDX_CUPOS_DISP] = max(0, paquete[IDX_CUPOS_DISP] + diferencia)

    # ── Vuelos ──
    mod_vuelos = _pedir_sn("  ¿Modificar opciones de vuelo? (S/N): ")
    if mod_vuelos == "S":
        for i in range(2):
            mod = _pedir_sn(f"  ¿Modificar vuelo opción {i+1}? (S/N): ")
            if mod == "S":
                paquete[IDX_VUELOS][i] = _ingresar_vuelo(i + 1)

    # ── Autos ──
    mod_autos = _pedir_sn("  ¿Modificar opciones de auto? (S/N): ")
    if mod_autos == "S":
        for i in range(2):
            mod = _pedir_sn(f"  ¿Modificar auto opción {i+1}? (S/N): ")
            if mod == "S":
                paquete[IDX_AUTOS][i] = _ingresar_auto(i + 1)

    # ── Excursiones ──
    mod_exc = _pedir_sn("  ¿Modificar opciones de excursión? (S/N): ")
    if mod_exc == "S":
        for i in range(2):
            mod = _pedir_sn(f"  ¿Modificar excursión opción {i+1}? (S/N): ")
            if mod == "S":
                paquete[IDX_EXCURSIONES][i] = _ingresar_excursion(i + 1)

    # ── Traslados ──
    mod_tras = _pedir_sn("  ¿Modificar opciones de traslado? (S/N): ")
    if mod_tras == "S":
        for i in range(2):
            mod = _pedir_sn(f"  ¿Modificar traslado opción {i+1}? (S/N): ")
            if mod == "S":
                paquete[IDX_TRASLADOS][i] = _ingresar_traslado(i + 1)

    guardar_paquetes()
    print(f"\n  ✔ Paquete '{paquete[IDX_DESTINO]}' modificado correctamente.")
    mostrar_paquete(paquete)


# ============================================================
# 3. ELIMINAR PAQUETE
# ============================================================

def eliminar_paquete():
    print(f"\n{SEPARADOR} ELIMINAR PAQUETE {SEPARADOR}")
    mostrar_todos_los_paquetes()

    id_paquete = _pedir_texto("\n  Ingresá el ID del paquete a eliminar: ").upper()
    paquete = _buscar_paquete_por_id(id_paquete)

    if paquete is None:
        print(f"  No existe un paquete con el ID '{id_paquete}'.")
        return

    # Verificar si tiene reservas activas
    reservas_activas = [r for r in reservas if r[1] == id_paquete]
    if len(reservas_activas) > 0:
        print(f"  ⚠ Este paquete tiene {len(reservas_activas)} reserva(s) activa(s).")
        print("  No se puede eliminar un paquete con reservas activas.")
        return

    print(f"\n  Paquete a eliminar:")
    mostrar_paquete(paquete)
    confirmar = _pedir_sn("\n  ¿Confirmar eliminación? (S/N): ")

    if confirmar == "S":
        paquetes.remove(paquete)
        guardar_paquetes()
        print(f"  ✔ Paquete '{paquete[IDX_DESTINO]}' eliminado.")
    else:
        print("  Eliminación cancelada.")


# ============================================================
# 4. VER DISPONIBILIDAD DE PAQUETES
# ============================================================

def ver_disponibilidad():
    print(f"\n{SEPARADOR} DISPONIBILIDAD DE PAQUETES {SEPARADOR}")

    if len(paquetes) == 0:
        print("  No hay paquetes cargados.")
        return

    print(f"\n  {'ID':<6} {'Destino':<22} {'Tipo':<16} {'Disp':>5} {'Total':>6}  Estado")
    print("  " + "-" * 65)

    for p in paquetes:
        disp  = p[IDX_CUPOS_DISP]
        total = p[IDX_CUPOS_TOT]
        if disp == 0:
            estado = "❌ SIN CUPOS"
        elif disp <= total * 0.2:
            estado = "⚠ ÚLTIMOS CUPOS"
        else:
            estado = "✔ DISPONIBLE"
        print(f"  {p[IDX_ID]:<6} {p[IDX_DESTINO]:<22} {p[IDX_TIPO]:<16} {disp:>5} {total:>6}  {estado}")

    print("  " + "-" * 65)
    print(f"  Total de paquetes: {len(paquetes)}")


# ============================================================
# 5. VER CLIENTES QUE COMPRARON PAQUETES
# ============================================================

def ver_clientes():
    print(f"\n{SEPARADOR} CLIENTES CON RESERVAS {SEPARADOR}")

    if len(reservas) == 0:
        print("  No hay reservas registradas.")
        return

    print(f"\n  {'ID Res':<8} {'Cliente':<25} {'DNI':<10} {'Paquete':<8} {'Destino':<22} {'Pers':>5} {'Total':>14}")
    print("  " + "-" * 100)

    for r in reservas:
        paquete = _buscar_paquete_por_id(r[1])
        destino = paquete[IDX_DESTINO] if paquete else "N/D"
        print(f"  {r[0]:<8} {r[2]:<25} {r[3]:<10} {r[1]:<8} {destino:<22} {r[5]:>5} {_fmt(r[6]):>14}")

    print("  " + "-" * 100)
    print(f"  Total de reservas: {len(reservas)}")


# ============================================================
# 6. VER RESERVAS POR PAQUETE
# ============================================================

def ver_reservas_por_paquete():
    print(f"\n{SEPARADOR} RESERVAS POR PAQUETE {SEPARADOR}")
    ver_disponibilidad()

    id_paquete = _pedir_texto("\n  Ingresá el ID del paquete a consultar: ").upper()
    paquete = _buscar_paquete_por_id(id_paquete)

    if paquete is None:
        print(f"  No existe un paquete con el ID '{id_paquete}'.")
        return

    reservas_paquete = [r for r in reservas if r[1].upper() == id_paquete]

    print(f"\n  Paquete: {paquete[IDX_DESTINO]} ({id_paquete})")
    print(f"  Cupos: {paquete[IDX_CUPOS_DISP]} disponibles de {paquete[IDX_CUPOS_TOT]} totales")

    if len(reservas_paquete) == 0:
        print("  Sin reservas para este paquete.")
        return

    print(f"\n  {'ID Res':<8} {'Cliente':<25} {'DNI':<10} {'Email':<28} {'Pers':>5} {'Total':>14}")
    print("  " + "-" * 95)

    total_personas = 0
    total_recaudado = 0
    for r in reservas_paquete:
        print(f"  {r[0]:<8} {r[2]:<25} {r[3]:<10} {r[4]:<28} {r[5]:>5} {_fmt(r[6]):>14}")
        total_personas  += r[5]
        total_recaudado += r[6]

    print("  " + "-" * 95)
    print(f"  Reservas: {len(reservas_paquete)}  |  "
          f"Personas totales: {total_personas}  |  "
          f"Recaudado: {_fmt(total_recaudado)}")


# ============================================================
# 7. GESTION DE PROMOCIONES
# ============================================================

def _confirmar_clave_admin():
    # Segunda barrera de seguridad: el admin reescribe su clave.
    clave = input("  Confirmá tu clave de administrador: ").strip()
    if clave != sesion_activa.get("clave", ""):
        print("  Clave incorrecta. Operación cancelada.")
        return False
    return True


def poner_promocion():
    print(f"\n{SEPARADOR} PONER PROMOCIÓN A UN PAQUETE {SEPARADOR}")
    if len(paquetes) == 0:
        print("  No hay paquetes cargados.")
        return

    mostrar_todos_los_paquetes()
    id_paquete = _pedir_texto("\n  Ingresá el ID del paquete: ").upper()
    paquete = _buscar_paquete_por_id(id_paquete)
    if paquete is None:
        print(f"  No existe un paquete con el ID '{id_paquete}'.")
        return

    descuento = _pedir_entero("  Porcentaje de descuento (1 a 90): ", minimo=1, maximo=90)

    if _confirmar_clave_admin():
        paquete[IDX_PROMO] = descuento
        guardar_paquetes()
        print(f"  ✔ Promoción del {descuento}% aplicada al paquete {id_paquete}.")


def quitar_promocion():
    print(f"\n{SEPARADOR} QUITAR PROMOCIÓN DE UN PAQUETE {SEPARADOR}")
    if len(paquetes) == 0:
        print("  No hay paquetes cargados.")
        return

    # Mostramos solo los paquetes que tienen promoción activa.
    con_promo = [p for p in paquetes if p[IDX_PROMO] > 0]
    if len(con_promo) == 0:
        print("  No hay ningún paquete con promoción activa.")
        return

    for p in con_promo:
        mostrar_paquete(p)

    id_paquete = _pedir_texto("\n  Ingresá el ID del paquete a quitar la promo: ").upper()
    paquete = _buscar_paquete_por_id(id_paquete)
    if paquete is None:
        print(f"  No existe un paquete con el ID '{id_paquete}'.")
    elif paquete[IDX_PROMO] == 0:
        print("  Ese paquete no tiene promoción.")
    elif _confirmar_clave_admin():
        paquete[IDX_PROMO] = 0
        guardar_paquetes()
        print(f"  ✔ Promoción quitada del paquete {id_paquete}.")


def gestionar_promociones():
    salir = False
    while not salir:
        print(f"\n{SEPARADOR} GESTIÓN DE PROMOCIONES {SEPARADOR}")
        print("  1. Poner promoción a un paquete")
        print("  2. Quitar promoción de un paquete")
        print("  0. Volver")
        opcion = input("  Opción: ").strip()
        if opcion == "1":
            poner_promocion()
        elif opcion == "2":
            quitar_promocion()
        elif opcion == "0":
            salir = True
        else:
            print("  Opción inválida.")


# ============================================================
# 7. REPORTE POR TIPO (NACIONAL / INTERNACIONAL)
# ============================================================
# Arma una matriz (lista de listas) por cada tipo, con una fila por paquete
# y estas columnas: [ destino, cupos_totales, cupos_vendidos, ingresos ].

def _ingresos_paquete(id_paquete):
    # Suma lo facturado por un paquete recorriendo sus reservas (total en la posicion 6).
    total = 0
    for r in reservas:
        if r[1].upper() == id_paquete.upper():
            total += r[6]
    return total


def _armar_matriz(tipo):
    matriz = []
    for p in paquetes:
        if p[IDX_TIPO] == tipo:
            vendidos = p[IDX_CUPOS_TOT] - p[IDX_CUPOS_DISP]
            ingresos = _ingresos_paquete(p[IDX_ID])
            matriz.append([p[IDX_DESTINO], p[IDX_CUPOS_TOT], vendidos, ingresos])
    return matriz


def _mostrar_bloque(titulo, matriz):
    # Recorre la matriz con un for, imprime cada fila y acumula los totales.
    print(f"\n{SEPARADOR} {titulo} {SEPARADOR}")
    if len(matriz) == 0:
        print("  (No hay paquetes en esta categoría.)")
        return 0, 0

    print(f"  {'DESTINO':<22} {'CUPOS':>6} {'VENDIDOS':>9} {'OCUP.':>7}   INGRESOS")
    print("  " + "-" * 58)

    total_cupos = 0
    total_vendidos = 0
    total_ingresos = 0
    for fila in matriz:
        destino, cupos, vendidos, ingresos = fila
        ocupacion = (vendidos * 100 // cupos) if cupos > 0 else 0
        print(f"  {destino:<22} {cupos:>6} {vendidos:>9} {ocupacion:>6}%   {_fmt(ingresos)}")
        total_cupos    += cupos
        total_vendidos += vendidos
        total_ingresos += ingresos

    print("  " + "-" * 58)
    print(f"  {'TOTALES':<22} {total_cupos:>6} {total_vendidos:>9} {'':>7}   {_fmt(total_ingresos)}")
    return total_vendidos, total_ingresos


def reporte_por_tipo():
    print(f"\n{SEPARADOR} REPORTE POR TIPO (NACIONAL / INTERNACIONAL) {SEPARADOR}")
    if len(paquetes) == 0:
        print("  No hay paquetes cargados.")
        return

    matriz_nac = _armar_matriz("Nacional")
    matriz_int = _armar_matriz("Internacional")

    vend_nac, ing_nac = _mostrar_bloque("PAQUETES NACIONALES", matriz_nac)
    vend_int, ing_int = _mostrar_bloque("PAQUETES INTERNACIONALES", matriz_int)

    print(f"\n{SEPARADOR} RESUMEN GENERAL {SEPARADOR}")
    print(f"  Plazas vendidas nacionales....: {vend_nac}")
    print(f"  Plazas vendidas internacionales: {vend_int}")
    print(f"  Ingresos nacionales...........: {_fmt(ing_nac)}")
    print(f"  Ingresos internacionales......: {_fmt(ing_int)}")
    print(f"  INGRESOS TOTALES..............: {_fmt(ing_nac + ing_int)}")


# ============================================================
# MENU ADMIN COMPLETO
# ============================================================

def menu_admin_paquetes():
    salir = False
    while not salir:
        print(f"\n{SEPARADOR} PANEL DE ADMINISTRACIÓN {SEPARADOR}")
        print("  --- Gestión de Paquetes ---")
        print("  1. Agregar nuevo paquete")
        print("  2. Modificar un paquete")
        print("  3. Eliminar un paquete")
        print("  --- Seguimiento ---")
        print("  4. Ver disponibilidad de paquetes")
        print("  5. Ver todos los clientes con reservas")
        print("  6. Ver reservas por paquete")
        print("  7. Reporte por tipo (Nacional / Internacional)")
        print("  --- Promociones ---")
        print("  8. Gestionar promociones")
        print("  0. Volver")

        opcion = input("\n  Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_paquete()
        elif opcion == "2":
            modificar_paquete()
        elif opcion == "3":
            eliminar_paquete()
        elif opcion == "4":
            ver_disponibilidad()
        elif opcion == "5":
            ver_clientes()
        elif opcion == "6":
            ver_reservas_por_paquete()
        elif opcion == "7":
            reporte_por_tipo()
        elif opcion == "8":
            gestionar_promociones()
        elif opcion == "0":
            salir = True
        else:
            print("  Opción inválida.")

        if not salir and opcion in ("1","2","3","4","5","6","7"):
            input("\n  Presione Enter para continuar...")