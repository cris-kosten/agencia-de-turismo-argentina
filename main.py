# SISTEMA DE BÚSQUEDA Y RESERVA DE PAQUETES TURÍSTICOS
# Algoritmos y Estructuras de Datos I
# Docente: Ricardo Thompson
# Grupo 2

from datos    import mostrar_todos_los_paquetes
from busqueda import buscar_x_destino, buscar_x_precio, buscar_con_cupos

SEPARADOR = "=" * 5


def mostrar_bienvenida():
    '''
    Muestra el mensaje de bienvenida al iniciar el sistema.
    '''
    print("=" * 50)
    print("   AGENCIA DE VIAJES - GRUPO 2")
    print("   Sistema de búsqueda y reserva de paquetes turísticos")
    print("=" * 50)


def mostrar_menu():
    '''
    Muestra las opciones disponibles del menú principal.
    '''
    print("\n", SEPARADOR, "MENÚ PRINCIPAL", SEPARADOR)
    print("  1. Ver todos los paquetes")
    print("  2. Buscar por destino")
    print("  3. Buscar por precio máximo")
    print("  4. Ver paquetes con cupos disponibles")
    print("  0. Salir")


# -----------------------------------------------------------
# Programa principal
# -----------------------------------------------------------

mostrar_bienvenida()

opcion = ""
while opcion != "0":
    mostrar_menu()
    opcion = input("\n  Seleccione una opción: ").strip()

    if opcion == "1":
        mostrar_todos_los_paquetes()

    elif opcion == "2":
        destino = input("  Ingrese el destino a buscar: ")
        buscar_x_destino(destino)

    elif opcion == "3":
        precio = float(input("Ingrese precio: "))
        buscar_x_precio(precio)

    elif opcion == "4":
        buscar_con_cupos()

    elif opcion != "0":
        print("  Opción inválida, intente nuevamente: ")

    if opcion != "0":
        input("\n  Presione Enter para continuar...")

print("\n¡Hasta pronto! Gracias por usar nuestro sistema.")