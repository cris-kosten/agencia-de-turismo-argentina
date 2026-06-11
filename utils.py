from datetime import date

def calcular_edad(fecha_nac):
    partes = fecha_nac.split("/") 
    dia = int(partes[0])
    mes = int(partes[1])
    anio = int(partes[2])
    nacimiento = date(anio, mes, dia)
    hoy = date.today()
    edad = hoy.year - nacimiento.year
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        edad -= 1
    return edad

def es_mayor_de_edad(fecha_nac):
    return calcular_edad(fecha_nac) >=18