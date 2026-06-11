import json
from utils import calcular_edad
from datos import sesion_activa

ARCHIVO_USUARIOS = "usuarios.json"
def cargar_usuarios():
    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}
    
def guardar_usuarios(usuarios):
    try:
        with open(ARCHIVO_USUARIOS, "w", encoding= "utf-8") as archivo:
            json.dump(usuarios, archivo, indent=4) #guarda el diccionario
    except OSError:
        print("No se pudo guardar el archivo de usuarios. ")
        
        
def registrarse():
    print("\n===== REGISTRO DE NUEVO USUARIO =====")

    usuarios = cargar_usuarios()

    # ── usuario ──────────────────────────────────────────
    while True:
        usuario = input("  Nombre de usuario: ").strip()
        if not usuario:
            print("  El usuario no puede estar vacío.")
        elif usuario in usuarios:
            print("  Ese nombre de usuario ya existe.")
        else:
            break

    # ── nombre completo ───────────────────────────────────
    while True:
        nombre = input("  Nombre completo: ").strip()
        if not nombre:
            print("  El nombre no puede estar vacío.")
        else:
            break

    # ── clave ─────────────────────────────────────────────
    while True:
        clave = input("  Contraseña (mínimo 4 caracteres): ").strip()
        if len(clave) < 4:
            print("  La contraseña debe tener al menos 4 caracteres.")
        else:
            break

    # ── dni ───────────────────────────────────────────────
    while True:
        dni = input("  DNI (7 u 8 dígitos): ").strip()
        if not dni.isdigit() or not (7 <= len(dni) <= 8):
            print("  DNI inválido. Solo números, 7 u 8 dígitos.")
        else:
            break

    # ── email ─────────────────────────────────────────────
    while True:
        email = input("  Email: ").strip()
        if "@" not in email or "." not in email:
            print("  Email inválido. Debe contener @ y punto.")
        else:
            break

    # ── fecha de nacimiento ───────────────────────────────
    while True:
        fecha_nac = input("  Fecha de nacimiento (DD/MM/AAAA): ").strip()
        try:
            edad = calcular_edad(fecha_nac)
            break
        except ValueError:
            print("  Fecha inválida. El día, mes o año no corresponden.")
        except IndexError:
            print("  Formato incorrecto. Usá DD/MM/AAAA.")

    # ── sexo ──────────────────────────────────────────────
    while True:
        sexo = input("  Sexo (M/F): ").strip().upper()
        if sexo not in ("M", "F"):
            print("  Ingresá M para masculino o F para femenino.")
        else:
            break

    # ── celular ───────────────────────────────────────────
    while True:
        celular = input("  Celular (10 u 11 dígitos): ").strip()
        if not celular.isdigit() or not (10 <= len(celular) <= 11):
            print("  Celular inválido. Solo números, 10 u 11 dígitos.")
        else:
            break

    # ── guardar nuevo usuario ─────────────────────────────
    usuarios[usuario] = {
        "nombre":    nombre,
        "clave":     clave,
        "dni":       dni,
        "email":     email,
        "fecha_nac": fecha_nac,
        "edad":      edad,
        "sexo":      sexo,
        "celular":   celular
    }

    guardar_usuarios(usuarios)
    print(f"\n  Bienvenido {nombre}, tu cuenta fue creada exitosamente.")
    print(f"  Tu edad registrada es: {edad} años.")
    

#Funcion del login 
def iniciar_sesion():
    print("\n==== INICIAR SESION ====")
    
    usuarios = cargar_usuarios()
    
    if not usuarios:
        print("No hay usuarios registrados. Registrate primero")
        return False
    
    intentos = 0
    while intentos <3:
        usuario = input(" Usuario: ").strip()
        clave = input(" Contraseñal: ").strip()
        
        if usuario in usuarios and usuarios[usuario]["clave"] == clave:
            sesion_activa["usuario"] = usuario
            sesion_activa["nombre"] = usuarios[usuario]["nombre"]
            sesion_activa["dni"] = usuarios[usuario]["dni"]
            sesion_activa["email"] = usuarios[usuario]["email"]
            sesion_activa["clave"] = usuarios[usuario]["clave"]
            sesion_activa["celular"] = usuarios[usuario]["celular"]
            sesion_activa["edad"] = usuarios[usuario]["edad"]
            sesion_activa["sexo"] = usuarios[usuario]["sexo"]
            sesion_activa["fecha_nac"] = usuarios[usuario]["fecha_nac"]
            sesion_activa["fecha_nac"] = usuarios[usuario]["fecha_nac"]
            print(f"\n Bienvenido, {sesion_activa["nombre"]}!!.")
            return True
        
        else:
            intentos += 1
            restantes = 3 - intentos
            if restantes >0:
                print(f"Usuario o contraseña incorrectos. Intentos restantes {restantes}")
    print("\n Demasiados intentos. El sistema se cerrara. ")
    return False


# Funcion Mostrar menu
def mostrar_menu_login():
    print("\n" + "=" *50)
    print(" Bienvenido a nuestra Agencia de Turismo")
    print("=" * 50)
    print(" 1. Iniciar sesion")
    print(" 2. Registrarse")
    print(" 0. Salir")
    print("=" * 50)
    
def ejecutar_login():
    while True:
        mostrar_menu_login()
        opcion = input("\n Seleccione una opcion: ").strip()
        
        if opcion == "1":
            if iniciar_sesion():
                return True
        elif opcion == "2":
            registrarse()
        elif opcion == "0":
            return False
        else:
            print("Opcion invalida. ")