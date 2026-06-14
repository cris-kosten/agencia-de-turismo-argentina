# ============================================================
# LOGIN - Sistema de inicio de sesión y registro
# Algoritmos y Estructuras de Datos I - Grupo 2
# ============================================================
# Persistencia: archivo de texto CSV (NO se usa JSON).
# Cada línea del archivo representa un usuario, con sus campos
# separados por comas en el siguiente orden:
#
#   usuario,clave,nombre,dni,email,fecha_nac,edad,sexo,celular,rol
#
# La primera línea del archivo es el encabezado (header).
# ============================================================

from utils import calcular_edad
from datos import sesion_activa

ARCHIVO_USUARIOS = "usuarios.csv"

# -- Constantes de indice de columna (evitan "numeros magicos") --
IDX_USUARIO   = 0
IDX_CLAVE     = 1
IDX_NOMBRE    = 2
IDX_DNI       = 3
IDX_EMAIL     = 4
IDX_FECHA_NAC = 5
IDX_EDAD      = 6
IDX_SEXO      = 7
IDX_CELULAR   = 8
IDX_ROL       = 9

ENCABEZADO = "usuario,clave,nombre,dni,email,fecha_nac,edad,sexo,celular,rol"


# ============================================================
# PERSISTENCIA (lectura / escritura del CSV)
# ============================================================

def cargar_usuarios():
    # Lee el archivo CSV y devuelve una lista de usuarios.
    # Cada usuario es a su vez una lista con sus 10 campos.
    # Si el archivo no existe todavia, devuelve una lista vacia.
    usuarios = []
    try:
        archivo = open(ARCHIVO_USUARIOS, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()

        # Recorremos desde la linea 1 para saltar el encabezado (linea 0)
        for i in range(1, len(lineas)):
            linea = lineas[i].strip()
            if linea != "":
                campos = linea.split(",")
                usuarios.append(campos)
    except FileNotFoundError:
        # Si el archivo no existe, no es un error grave:
        # simplemente todavia no hay usuarios registrados.
        print("  (Aun no existe el archivo de usuarios, se creara al registrar.)")

    return usuarios


def guardar_usuarios(usuarios):
    # Escribe la lista completa de usuarios en el archivo CSV.
    try:
        archivo = open(ARCHIVO_USUARIOS, "w", encoding="utf-8")
        archivo.write(ENCABEZADO + "\n")
        for usuario in usuarios:
            linea = ",".join(usuario)
            archivo.write(linea + "\n")
        archivo.close()
    except OSError:
        print("  No se pudo guardar el archivo de usuarios.")


def buscar_usuario(usuarios, nombre_usuario):
    # Busca un usuario por su nombre dentro de la lista.
    # Devuelve la fila (lista de campos) si lo encuentra, o None si no existe.
    encontrado = None
    for usuario in usuarios:
        if usuario[IDX_USUARIO] == nombre_usuario:
            encontrado = usuario
    return encontrado


# ============================================================
# VALIDACIONES
# ============================================================
# Cada funcion devuelve True si el dato es valido, False si no.
# Se usan tanto en el registro como (algunas) en otras partes.

def tiene_coma(texto):
    # El CSV separa campos por coma, asi que ningun dato puede tener una.
    resultado = "," in texto
    return resultado


def validar_usuario(usuarios, usuario):
    # Usuario: no vacio, sin comas, entre 3 y 20 caracteres y unico.
    valido = True
    if len(usuario) < 3 or len(usuario) > 20:
        print("  El usuario debe tener entre 3 y 20 caracteres.")
        valido = False
    elif tiene_coma(usuario):
        print("  El usuario no puede contener comas.")
        valido = False
    elif buscar_usuario(usuarios, usuario) is not None:
        print("  Ese nombre de usuario ya existe.")
        valido = False
    return valido


def validar_nombre(nombre):
    # Nombre: no vacio, sin comas, solo letras y espacios.
    valido = True
    sin_espacios = nombre.replace(" ", "")
    if nombre == "":
        print("  El nombre no puede estar vacio.")
        valido = False
    elif tiene_coma(nombre):
        print("  El nombre no puede contener comas.")
        valido = False
    elif not sin_espacios.isalpha():
        print("  El nombre solo puede tener letras y espacios.")
        valido = False
    return valido


def validar_clave(clave):
    # Clave: minimo 6 caracteres, sin comas, al menos una letra y un numero.
    valido = True
    tiene_letra = False
    tiene_numero = False
    for caracter in clave:
        if caracter.isalpha():
            tiene_letra = True
        elif caracter.isdigit():
            tiene_numero = True

    if len(clave) < 6:
        print("  La contrasena debe tener al menos 6 caracteres.")
        valido = False
    elif tiene_coma(clave):
        print("  La contrasena no puede contener comas.")
        valido = False
    elif not tiene_letra or not tiene_numero:
        print("  La contrasena debe tener al menos una letra y un numero.")
        valido = False
    return valido


def validar_dni(dni):
    # DNI: exactamente 8 digitos numericos.
    valido = True
    if not dni.isdigit():
        print("  El DNI solo puede tener numeros.")
        valido = False
    elif len(dni) != 8:
        print("  El DNI debe tener exactamente 8 digitos.")
        valido = False
    return valido


def validar_email(email):
    # Email: sin comas, con un solo @, y con un punto despues del @.
    valido = True
    if tiene_coma(email):
        print("  El email no puede contener comas.")
        valido = False
    elif email.count("@") != 1:
        print("  El email debe tener exactamente un signo @.")
        valido = False
    else:
        parte_usuario = email.split("@")[0]
        parte_dominio = email.split("@")[1]
        if parte_usuario == "" or parte_dominio == "":
            print("  El email esta incompleto (falta texto antes o despues del @).")
            valido = False
        elif "." not in parte_dominio:
            print("  El dominio del email debe tener un punto (ej: gmail.com).")
            valido = False
    return valido


def validar_sexo(sexo):
    # Sexo: solo M o F.
    valido = sexo in ("M", "F")
    if not valido:
        print("  Ingresa M para masculino o F para femenino.")
    return valido


def validar_celular(celular):
    # Celular: exactamente 11 digitos numericos.
    valido = True
    if not celular.isdigit():
        print("  El celular solo puede tener numeros.")
        valido = False
    elif len(celular) != 11:
        print("  El celular debe tener exactamente 11 digitos.")
        valido = False
    return valido


# ============================================================
# REGISTRO DE USUARIOS
# ============================================================

def registrarse():
    print("\n===== REGISTRO DE NUEVO USUARIO =====")

    usuarios = cargar_usuarios()

    # -- usuario --
    usuario = ""
    valido = False
    while not valido:
        usuario = input("  Nombre de usuario (3 a 20 caracteres): ").strip()
        valido = validar_usuario(usuarios, usuario)

    # -- nombre completo --
    nombre = ""
    valido = False
    while not valido:
        nombre = input("  Nombre completo: ").strip()
        valido = validar_nombre(nombre)

    # -- clave --
    clave = ""
    valido = False
    while not valido:
        clave = input("  Contrasena (min 6, con letras y numeros): ").strip()
        valido = validar_clave(clave)

    # -- dni --
    dni = ""
    valido = False
    while not valido:
        dni = input("  DNI (8 digitos): ").strip()
        valido = validar_dni(dni)

    # -- email --
    email = ""
    valido = False
    while not valido:
        email = input("  Email: ").strip()
        valido = validar_email(email)

    # -- fecha de nacimiento --
    edad = -1
    fecha_nac = ""
    while edad == -1:
        fecha_nac = input("  Fecha de nacimiento (DD/MM/AAAA): ").strip()
        try:
            edad = calcular_edad(fecha_nac)
        except ValueError:
            print("  Fecha invalida. El dia, mes o anio no corresponden.")
        except IndexError:
            print("  Formato incorrecto. Usa DD/MM/AAAA.")

    # -- sexo --
    sexo = ""
    valido = False
    while not valido:
        sexo = input("  Sexo (M/F): ").strip().upper()
        valido = validar_sexo(sexo)

    # -- celular --
    celular = ""
    valido = False
    while not valido:
        celular = input("  Celular (11 digitos): ").strip()
        valido = validar_celular(celular)

    # -- rol --
    # Si el sistema todavia no tiene ningun usuario, el primero
    # que se registra queda como "admin" (asi siempre hay un admin).
    # El resto de los usuarios se registran como "cliente".
    if len(usuarios) == 0:
        rol = "admin"
        print("  Sos el primer usuario: se te asigna el rol ADMIN.")
    else:
        rol = "cliente"

    # -- guardar nuevo usuario --
    # El orden de los campos DEBE coincidir con el del encabezado.
    nuevo_usuario = [
        usuario,
        clave,
        nombre,
        dni,
        email,
        fecha_nac,
        str(edad),   # se guarda como texto porque el CSV es texto
        sexo,
        celular,
        rol
    ]
    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)

    print("\n  Bienvenido %s, tu cuenta fue creada exitosamente." % nombre)
    print("  Tu edad registrada es: %d anios." % edad)
    print("  Tu rol es: %s." % rol)


# ============================================================
# INICIO DE SESION
# ============================================================

def iniciar_sesion():
    print("\n==== INICIAR SESION ====")

    exito = False
    usuarios = cargar_usuarios()

    if len(usuarios) == 0:
        print("  No hay usuarios registrados. Registrate primero.")
    else:
        intentos = 0
        while intentos < 3 and not exito:
            usuario = input("  Usuario: ").strip()
            clave = input("  Contrasena: ").strip()

            # Tratamos de leer los datos del usuario encontrado.
            # Si el archivo CSV estuviera mal formado (a una fila le
            # faltan columnas), el acceso por indice lanzaria IndexError;
            # lo capturamos en forma especifica para no caernos.
            try:
                fila = buscar_usuario(usuarios, usuario)
                if fila is not None and fila[IDX_CLAVE] == clave:
                    sesion_activa["usuario"]   = fila[IDX_USUARIO]
                    sesion_activa["nombre"]    = fila[IDX_NOMBRE]
                    sesion_activa["dni"]       = fila[IDX_DNI]
                    sesion_activa["email"]     = fila[IDX_EMAIL]
                    sesion_activa["clave"]     = fila[IDX_CLAVE]
                    sesion_activa["celular"]   = fila[IDX_CELULAR]
                    sesion_activa["edad"]      = fila[IDX_EDAD]
                    sesion_activa["sexo"]      = fila[IDX_SEXO]
                    sesion_activa["fecha_nac"] = fila[IDX_FECHA_NAC]
                    sesion_activa["rol"]       = fila[IDX_ROL]
                    print("\n  Bienvenido, %s!" % sesion_activa["nombre"])
                    exito = True
                else:
                    intentos += 1
                    restantes = 3 - intentos
                    if restantes > 0:
                        print("  Usuario o contrasena incorrectos. Intentos restantes: %d" % restantes)
            except IndexError:
                print("  El archivo de usuarios tiene una fila incompleta o danada.")
                intentos += 1

        if not exito:
            print("\n  Demasiados intentos. El sistema se cerrara.")

    return exito


# ============================================================
# MENU DE LOGIN
# ============================================================

def mostrar_menu_login():
    print("\n" + "=" * 50)
    print(" Bienvenido a nuestra Agencia de Turismo")
    print("=" * 50)
    print(" 1. Iniciar sesion")
    print(" 2. Registrarse")
    print(" 0. Salir")
    print("=" * 50)


def ejecutar_login():
    # Devuelve True si el usuario logro iniciar sesion,
    # o False si decidio salir. Un unico return al final.
    resultado = False
    salir = False

    while not salir:
        mostrar_menu_login()
        opcion = input("\n Seleccione una opcion: ").strip()

        if opcion == "1":
            if iniciar_sesion():
                resultado = True
                salir = True
        elif opcion == "2":
            registrarse()
        elif opcion == "0":
            resultado = False
            salir = True
        else:
            print(" Opcion invalida.")

    return resultado


# ============================================================
# ROLES: utilidad para distinguir admin de cliente
# ============================================================

def es_admin():
    # Devuelve True si el usuario logueado tiene rol de administrador.
    resultado = sesion_activa.get("rol", "") == "admin"
    return resultado


# ============================================================
# GESTION DE ROLES (solo para administradores)
# ============================================================

def contar_admins(usuarios):
    # Cuenta cuantos usuarios tienen rol "admin".
    # Sirve para no permitir que el sistema se quede sin ningun admin.
    cantidad = 0
    for usuario in usuarios:
        if usuario[IDX_ROL] == "admin":
            cantidad = cantidad + 1
    return cantidad


def mostrar_lista_usuarios(usuarios):
    # Muestra todos los usuarios con su rol, para que el admin elija.
    print("\n  --- USUARIOS REGISTRADOS ---")
    for usuario in usuarios:
        print("   %-20s -> %s" % (usuario[IDX_USUARIO], usuario[IDX_ROL]))
    print("  ----------------------------")


def cambiar_rol(nuevo_rol):
    # Da o quita el rol admin a un usuario elegido.
    # nuevo_rol debe ser "admin" (para designar) o "cliente" (para quitar).
    usuarios = cargar_usuarios()

    mostrar_lista_usuarios(usuarios)
    objetivo = input("\n  Nombre de usuario a modificar: ").strip()
    fila = buscar_usuario(usuarios, objetivo)

    if fila is None:
        print("  Ese usuario no existe.")
    elif nuevo_rol == "admin" and fila[IDX_ROL] == "admin":
        print("  Ese usuario ya es administrador.")
    elif nuevo_rol == "cliente" and fila[IDX_ROL] == "cliente":
        print("  Ese usuario ya es cliente (no es admin).")
    elif nuevo_rol == "cliente" and objetivo == sesion_activa["usuario"]:
        # Seguridad: un admin no puede quitarse el admin a si mismo.
        print("  No podes quitarte el rol de administrador a vos mismo.")
    elif nuevo_rol == "cliente" and contar_admins(usuarios) == 1:
        # Seguridad: no se puede quitar el ultimo admin que queda.
        print("  No se puede quitar el admin: es el unico administrador del sistema.")
    else:
        fila[IDX_ROL] = nuevo_rol
        guardar_usuarios(usuarios)
        print("  Listo. Ahora '%s' tiene el rol: %s." % (objetivo, nuevo_rol))


def gestionar_roles():
    # Menu para que un admin designe o saque administradores.
    salir = False
    while not salir:
        print("\n  ===== GESTION DE ROLES =====")
        print("   1. Designar un usuario como ADMIN")
        print("   2. Quitar el rol ADMIN (volver a cliente)")
        print("   3. Ver lista de usuarios")
        print("   0. Volver")
        opcion = input("   Opcion: ").strip()

        if opcion == "1":
            cambiar_rol("admin")
        elif opcion == "2":
            cambiar_rol("cliente")
        elif opcion == "3":
            usuarios = cargar_usuarios()
            mostrar_lista_usuarios(usuarios)
        elif opcion == "0":
            salir = True
        else:
            print("   Opcion invalida.")