# SISTEMA DE BÚSQUEDA Y RESERVA DE PAQUETES TURÍSTICOS
# Algoritmos y Estructuras de Datos I
# Docente: Ricardo Thompson
# Grupo 2

from datos    import mostrar_todos_los_paquetes
from busqueda import buscar_x_destino, buscar_x_precio, buscar_con_cupos, buscar_x_fecha
from reportes import reporte_paquete_mas_caro_y_mas_barato, reporte_promedio_de_precios, reporte_cupos_totales
from reserva  import realizar_reserva,ver_todas_las_reservas


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
    print("  --- Paquetes ---")
    print("  1. Ver todos los paquetes")
    print("  2. Buscar por destino")
    print("  3. Buscar por precio máximo")
    print("  4. Ver paquetes con cupos disponibles")
    print("  5. Buscar por fecha de salida")
    print("  6. Paquete mas economico y mas caro.")
    print("  7. Promedio de precios.")
    print("  8. Resumen de cupos ")
    print("  --- Reservas ---")
    print("  9. Realizar una reserva")
    print("  10. Ver todas las reservas")
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
        precio = input("Ingrese precio: ").strip()
        if not precio.isdigit():
            print(" El precio debe ser un numero valido. ")
        else:
            buscar_x_precio(float(precio))

    elif opcion == "4":
        buscar_con_cupos()
        
    elif opcion == "5":
        dia = input("Ingrese el dia: ").strip()
        mes = input("Ingrese el mes: ").strip()
        año = input("Ingrese el año: ").strip()
        
        if not dia.isdigit() or not mes.isdigit() or not año.isdigit():
            print(" Los valores deben ser numericos. ")
        else:
            buscar_x_fecha(int(dia), int(mes), int(año))

    elif opcion == "6":
        reporte_paquete_mas_caro_y_mas_barato()
    
    elif opcion == "7":
        reporte_promedio_de_precios()

    elif opcion == "8":
        reporte_cupos_totales()

    elif opcion == "9":
        realizar_reserva()

    elif opcion == "10":
        ver_todas_las_reservas()

    elif opcion != "0":
        print("  Opción inválida, intente nuevamente: ")

    if opcion != "0":
        input("\n  Presione Enter para continuar...")

print("\n¡Hasta pronto! Gracias por usar nuestro sistema.")
