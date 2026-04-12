import random

# Matriz de paquete turistico[id, destino, provincias, dias, precio, cupos]
paquetes = [
    [100, "Cataratas del Iguazu",       "Misiones",         5,  1900000,    7],
    [101, "Glaciar Perito Moreno",      "Santa Cruz",       7,  3600000,    10],
    [102, "Bariloche y Lagos",          "Rio Negro",        5,  2150000,    5],
    [103, "Puerto Madryn y Ballenas",   "Chubut",           4,  2030000,    8],
    [104, "Ushuaia Fin del Mundo",      "Tierra del Fuego", 5,  2850000,    3],
    [105, "Sierras de Cordoba",         "Cordoba",          3,  998000,     10],
]


def mostrar_paquetes(paquetes):
    print("\n" + "🔹" * 39)
    print("                     NUESTRO CATALOGO DE PAQUETES        ")
    print("🔹" * 39)
    # Encabezado de COLUMNAS
    print(f"{'COD':<4} {'   DESTINO':<28} {'PROVINCIA':<18} {'DIAS':<5} {'  PRECIO':<12} {'CUPOS':<3}")
    print("=" * 77)
    
    for p in paquetes:
        print(f"{p[0]:<5} {p[1]:<28} {p[2]:<18} {p[3]:<5} {p[4]:<12} {p[5]:<3}")
        

# mostramos el menu de busqueda
def menu():
    print()
    print("     TURISMO ARGENTINA   ")
    print(" 1.  Ver nuestro catalogo completo")
    print(" 2.  Buscar destino")
    print(" 3.  Buscar por codigo")
    print(" 4.  Buscar segun orden de los paquetes")
    print(" 5.  Realizar una reserva de paquete")
    print(" 6.  Ver mis reservas")
    print(" 7.  Cancelar una reserva")
    print(" 0.  Salir")



def main():
    while True:
        menu()
        opcion = input("  Elegi una opcion: ").strip() 
        
        if opcion == "1":
            mostrar_paquetes(paquetes)
        
        elif opcion == "2":
            print("▶️    Proximamente ")
        elif opcion == "3":
            print("▶️    Proximamente")
        elif opcion == "4":
            while True:
                print("\n   ORDENAR POR : ")
                print(" 1.  Precio")
                print(" 2.  Cantidad de dias")
                print(" 3.  Por destino A-Z")
                print(" 0.  Volver al menu principal")
                sub = input('Elegi tu opcion: ').strip()
                
                if sub == "1":
                    print("Menor a mayor precio --> Proximamente")
                elif sub == "2":
                    print("Paquetes x cantidad de dias --> Proximamente")
                elif sub == "3":
                    print("Por destinos --> Proximamente ")
                elif sub == "0":
                    break
                else:
                    print("Opcion invalida")
                    
        elif opcion == "5":
            print("Reservar --> Continuara ...")
        elif opcion == "6":
            print("Ver mis reservas..... continuara")
        elif opcion == "7":
            print("Cancelar reservas ---> proximamente")
        elif opcion == "0":
            print("Gracias por visitarnos 🛣️")
            break
        else:
            print(" Opcion invalida")
main()
