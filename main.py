import os
import pymysql
import ventas
import usuarios
import clientes
import productos

try:
    conexion = pymysql.connect(host='remotemysql.com',
                               user='0PBDM6NaXW',
                               password='24F7qj6bbk',
                               db='0PBDM6NaXW')
except (pymysql.err.Error) as e:
    print("Ocurrió un error al conectar con la base de datos: ", e)

clear = lambda: os.system('cls')

exito = False
with conexion.cursor() as cursor:
    while exito == False:
        clear()
        nombre = input("Ingrese su usuario: ")
        print()
        clave = input("Ingrese su clave: ")
        print()
        consulta = "SELECT * FROM usuario WHERE binary nombre = %s AND binary clave = %s;"
        cursor.execute(consulta, (nombre, clave))
        usuario = cursor.fetchall()
        if not usuario:
            anykey = input("Los datos ingresados no son válidos, presione ENTER para intentar nuevamente.")
            exito = False
        else:
            exito = True

def menu():
    while True:
        clear()
        print("--MENÚ PRINCIPAL--\n")
        print("1) Ventas")
        print("2) Usuarios")
        print("3) Clientes")
        print("4) Productos")
        print("5) Salir\n")
        try:
            seleccion = int(input("Seleccione una opción: "))
            if seleccion == 1:
                ventas.menu()
                menu()
            elif seleccion == 2:
                usuarios.menu()
                menu()
            elif seleccion == 3:
                clientes.menu()
                menu()
            elif seleccion == 4:
                productos.menu()
                menu()
            elif seleccion == 5:
                break
            else:
                clear()
                anykey = input("Ingrese un número de 1 al 5, presione ENTER para intentar nuevamente.")
        except ValueError:
            clear()
            anykey = input("Ingrese un número de 1 al 5, presione ENTER para intentar nuevamente.")
    exit()


if __name__ == '__main__':
    menu()

conexion.close()
