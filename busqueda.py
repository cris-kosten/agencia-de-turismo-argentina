# MODULO DE BUSQUEDA DE PAQUETES TURISTICOS

from datos import paquetes, IDX_DESTINO, IDX_PRECIO, IDX_FECHA, IDX_CUPOS_DISP
import mostrar_paquete

def normalizar_texto(texto):
    '''
    Convierte un texto a minusculas y remplaza las vocales con tilde por vocales sin tilde.
    '''
    texto = texto.lower()
    texto = texto.replace("á", "a")
    texto = texto.replace("é", "e")
    texto = texto.replace("í", "i")
    texto = texto.replace("ó", "o")
    texto = texto.replace("ú", "u")
    return texto


def buscar_x_destino(destino_a_buscar):
    '''
    Busca paquetes turisticos por nombre del destino.
    recibe el nombre del destino como string.
    usamos lower() para no distinguir la busqueda.
    muestra el resultado o un aviso si no encuentra nada
    '''
    
    SEPARADOR = "=" * 5
    resultados = []
    for paquete in paquetes:
        if destino_a_buscar.lower() in paquete[IDX_DESTINO].lower():
            resultados.append(paquete)
            
    if len(resultados) == 0:
        print(f"no se encontro el paquete para el destino: {destino_a_buscar}")
        return
    
    print(f"\n{SEPARADOR} RESULTADO PARA: ✈️ {destino_a_buscar.upper()} 🏖️ ")
    for paquete in resultados:
        mostrar_paquete(paquete)
        


def buscar_x_precio(precio_maximo):
    '''
    Busca paquetes cuyo precio sea menor o igual al precio maximo
    Se valida que el precio no sea negativo.
    Muestra los resultados por pantalla y/o avisa si no encuentra nada
    '''
    
    SEPARADOR = "=" * 5
    if precio_maximo < 0:
        print("El precio ingresado es negativo ❌.")
        return 
    
    resultados = []
    for paquete in paquetes:
        if paquete[IDX_PRECIO] <= precio_maximo:
            resultados.append(paquete)
            
    if len(resultados) == 0:
        print(f"No hay paquetes disponibles a partir del precio ${precio_maximo:.2f}")
        
    print(f"\n{SEPARADOR} PAQUETES HASTA ${precio_maximo:.2f} {SEPARADOR}")
    for paquete in resultados:
        mostrar_paquete(paquete)


# busqueda por fechas 
def convertir_fechas(fecha_srt):
    '''
    convierte una fecha de formato DD/MM/AAAA a AAAA/MM/DD
    para que pueda comparar con el texto.
    '''
    partes = fecha_srt.split("/")
    return partes[2] + partes[1] + partes[0]

def validar_y_convertir_fecha(dia, mes, año):
    '''
    recibe dia, mes, año como enteros.
    valida que el año sea mayor a 2024, el mes entre 1 y 12, y
    el dia valido segun la cantidad de dias de cada mes.
    Devuelve el string AAAAMMDD para comparar, o None si la fecha
    es invalida 
    '''
    
    DIAS_POR_MES = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    #               -  E   F   M   A   M   J   J   A   S   O   N   D
    if año < 2024:
        print("El año ingresado no es valido ❌")
        return None
    if mes <1 or mes >12:
        print("El mes ingresado no es valido ❌")
        return None
    if dia <1 or dia >31:
        print("El dia ingresado no es valido ❌")
        return None
    return str(año) + str(mes).zfill(2) + str(dia).zfill(2)