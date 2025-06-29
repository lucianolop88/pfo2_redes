import requests

API_URL = "http://127.0.0.1:5000"

session = requests.Session() 

def registrar():
    usuario = input("Usuario nuevo: ")
    contraseña = input("Contraseña: ")
    datos = {"usuario": usuario, "contraseña": contraseña}
    r = session.post(f"{API_URL}/registro", json=datos)
    print(f"[{r.status_code}] {r.json()['mensaje']}")

def login():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    datos = {"usuario": usuario, "contraseña": contraseña}
    r = session.post(f"{API_URL}/login", json=datos)
    print(f"[{r.status_code}] {r.json()['mensaje']}")

def logout():
    r = session.post(f"{API_URL}/logout")
    print(f"[{r.status_code}] {r.json()['mensaje']}")

def ver_tareas():
    r = session.get(f"{API_URL}/tareas")
    if r.status_code == 200:
        print("[200] Página de bienvenida HTML cargada:")
        print(r.text)
    else:
        print(f"[{r.status_code}] {r.json()['mensaje']}")

def menu():
    while True:
        print("\n--- MENÚ ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver tareas (requiere login)")
        print("0. Salir")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()