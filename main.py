# SISTEMA DE BÚSQUEDA Y RESERVA DE PAQUETES TURÍSTICOS
# Algoritmos y Estructuras de Datos I
# Docente: Ricardo Thompson
# Grupo 2

from login    import ejecutar_login, es_admin, gestionar_roles
from datos    import mostrar_todos_los_paquetes, cargar_paquetes
from busqueda import buscar_x_destino, buscar_x_tipo, buscar_x_precio
from reserva  import realizar_reserva, ver_todas_las_reservas, cancelar_reserva
from admin    import menu_admin_paquetes

SEPARADOR = "=" * 5


def mostrar_bienvenida():
    print("=" * 55)
    print("   AGENCIA DE VIAJES - GRUPO 2")
    print("   Sistema de búsqueda y reserva de paquetes turísticos")
    print("=" * 55)


def mostrar_menu():
    print(f"\n {SEPARADOR} MENÚ PRINCIPAL {SEPARADOR}")
    print("  --- Paquetes ---")
    print("  1. Ver todos los paquetes")
    print("  2. Buscar por destino")
    print("  3. Buscar por tipo  (Nacional / Internacional)")
    print("  4. Buscar por precio máximo")
    print("  --- Reservas ---")
    print("  5. Realizar una reserva")
    print("  6. Ver mis reservas")
    print("  7. Cancelar una reserva")
    print("  0. Salir")


def ejecutar_menu():
    opcion = ""
    while opcion != "0":
        mostrar_menu()
        opcion = input("\n  Seleccione una opción: ").strip()

        if opcion == "1":
            mostrar_todos_los_paquetes()
        elif opcion == "2":
            destino = input("  Ingrese el destino a buscar: ").strip()
            buscar_x_destino(destino)
        elif opcion == "3":
            print("  Tipos disponibles: Nacional / Internacional")
            tipo = input("  Ingrese el tipo: ").strip()
            buscar_x_tipo(tipo)
        elif opcion == "4":
            precio_str = input("  Ingrese el precio máximo por persona: $").strip()
            if not precio_str.isdigit():
                print("  El precio debe ser un número entero.")
            else:
                buscar_x_precio(int(precio_str))
        elif opcion == "5":
            realizar_reserva()
        elif opcion == "6":
            ver_todas_las_reservas()
        elif opcion == "7":
            cancelar_reserva()
        elif opcion != "0":
            print("  Opción inválida, intente nuevamente.")

        if opcion != "0":
            input("\n  Presione Enter para continuar...")

    print("\n  ¡Hasta pronto! Gracias por usar nuestro sistema.")


def menu_admin():
    salir = False
    while not salir:
        print(f"\n {SEPARADOR} PANEL DE ADMINISTRADOR {SEPARADOR}")
        print("  1. Gestionar paquetes turísticos")
        print("  2. Gestionar roles de usuarios")
        print("  3. Ir al menú de cliente")
        print("  0. Salir")
        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            menu_admin_paquetes()
        elif opcion == "2":
            gestionar_roles()
        elif opcion == "3":
            ejecutar_menu()
        elif opcion == "0":
            salir = True
        else:
            print("  Opción inválida.")


# -----------------------------------------------------------
# Programa principal
# -----------------------------------------------------------

mostrar_bienvenida()
cargar_paquetes()   # carga paquetes desde paquetes.json si el archivo existe

if not ejecutar_login():
    print("\n  Gracias por visitarnos. ¡Hasta pronto!")
else:
    if es_admin():
        print("\n  Iniciaste sesión como ADMINISTRADOR.")
        menu_admin()
    else:
        print("\n  Iniciaste sesión como CLIENTE.")
        ejecutar_menu()