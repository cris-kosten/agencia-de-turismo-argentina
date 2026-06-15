# SISTEMA DE BÚSQUEDA Y RESERVA DE PAQUETES TURÍSTICOS
# Algoritmos y Estructuras de Datos I
# Docente: Ricardo Thompson
# Grupo 2

from login  import ejecutar_login, es_admin, gestionar_roles, agregar_paquete, gestionar_promociones
from datos  import mostrar_todos_los_paquetes, cargar_paquetes
from busqueda import buscar_x_destino, buscar_x_fecha
from reserva  import realizar_reserva, ver_todas_las_reservas, cancelar_reserva

SEPARADOR = "=" * 5


def mostrar_bienvenida():
    print("=" * 50)
    print("   AGENCIA DE VIAJES - GRUPO 2")
    print("   Sistema de búsqueda y reserva de paquetes turísticos")
    print("=" * 50)


def mostrar_menu():
    print("\n", SEPARADOR, "MENÚ PRINCIPAL", SEPARADOR)
    print("  --- Paquetes ---")
    print("  1. Ver todos los paquetes")
    print("  2. Buscar por destino")
    print("  3. Buscar por fecha de salida")
    print("  --- Reservas ---")
    print("  5. Realizar una reserva")
    print("  6. Ver todas las reservas")
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
            dia = input("  Ingrese el dia: ").strip()
            mes = input("  Ingrese el mes: ").strip()
            año = input("  Ingrese el año: ").strip()
            if not dia.isdigit() or not mes.isdigit() or not año.isdigit():
                print("  Los valores deben ser numéricos.")
            else:
                buscar_x_fecha(int(dia), int(mes), int(año))

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
    # Panel exclusivo para administradores.
    # Aca se concentran las operaciones que solo puede hacer un admin.
    salir = False
    while not salir:
        print("\n", SEPARADOR, "PANEL DE ADMINISTRADOR", SEPARADOR)
        print("   1. Gestionar roles (designar / quitar admins)")
        print("   2. Agregar un nuevo paquete")
        print("   3. Gestionar promociones (poner / quitar)")
        print("   4. Ir al menu principal de la agencia")
        print("   0. Salir")
        opcion = input("   Seleccione una opcion: ").strip()

        if opcion == "1":
            gestionar_roles()
        elif opcion == "2":
            agregar_paquete()
        elif opcion == "3":
            gestionar_promociones()
        elif opcion == "4":
            ejecutar_menu()
        elif opcion == "0":
            salir = True
        else:
            print("   Opcion invalida.")


# -----------------------------------------------------------
# Programa principal
# -----------------------------------------------------------

mostrar_bienvenida()
cargar_paquetes()   # carga paquetes desde paquetes.csv si el archivo existe

if not ejecutar_login():
    print("\n  Gracias por visitarnos. ¡Hasta pronto!")
else:
    # Redireccion basica segun el rol del usuario logueado.
    if es_admin():
        print("\n  Iniciaste sesion como ADMINISTRADOR.")
        menu_admin()
    else:
        print("\n  Iniciaste sesion como CLIENTE.")
        ejecutar_menu()