import os
import pymysql
from prettytable import PrettyTable

try:
    conexion = pymysql.connect(host='remotemysql.com',
                               user='0PBDM6NaXW',
                               password='24F7qj6bbk',
                               db='0PBDM6NaXW')
except (pymysql.err.Error) as e:
    print("Ocurrió un error al conectar con la base de datos: ", e)

clear = lambda: os.system('cls')

def menu():
    while True:
        clear()
        print("--MENU USUARIOS--\n")
        print("1) Dar de alta usuario")
        print("2) Dar de baja usuario")
        print("3) Modificar usuario")
        print("4) Listar usuarios")
        print("5) Regresar al menú principal\n")

        try:
            seleccion = int(input("Seleccione una opción: "))
            if seleccion == 1:
                clear()
                altausuario()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea dar de alta otro usuario? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        altausuario()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 2:
                clear()
                bajausuario()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea dar de baja otro usuario? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        bajausuario()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 3:
                clear()
                modificarusuario()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea modificar otro usuario? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        modificarusuario()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 4:
                clear()
                listarusuario()
                anykey = input("Presione ENTER para continuar.")
            elif seleccion == 5:
                break
            else:
                clear()
                anykey = input("Ingrese un número de 1 al 5, presione ENTER para intentar nuevamente.")
        except ValueError:
            clear()
            anykey = input("Ingrese un número de 1 al 5, presione ENTER para intentar nuevamente.")
    return


def altausuario():
    try:
        with conexion.cursor() as cursor:
            x = 0
            T = PrettyTable(["ID", "Nombre", "Clave"])
            nombre = input("Ingrese el nombre del usuario: ")
            clave = input("Ingrese la clave del usuario: ")
            consulta = "INSERT INTO usuario(nombre,clave) VALUES (%s, %s);"
            cursor.execute(consulta, (nombre, clave))
            consulta = "SELECT * FROM usuario WHERE nombre = %s;"
            cursor.execute(consulta, (nombre))
            usuario = cursor.fetchall()
        conexion.commit()
        clear()
        for x in usuario:
            T.add_row(x)
        print(T)
        print("")
        print("USUARIO DADO DE ALTA CORRECTAMENTE")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al dar de alta el usuario: ", f)


def bajausuario():
    try:
        with conexion.cursor() as cursor:
            seleccion3 = ""
            x = 0
            T = PrettyTable(["ID", "Nombre", "Clave"])
            id = input("Ingrese el ID del usuario a dar de baja: ")
            while seleccion3 not in ["s","n"]:
                consulta = "SELECT * FROM usuario WHERE id = %s;"
                cursor.execute(consulta, (id))
                usuario = cursor.fetchall()
                if not usuario:
                    print("El ID ingresado no es válido.\n")
                    exito = False
                    return
                else:
                    exito = True
                clear()
                for x in usuario:
                    T.add_row(x)
                print(T)
                print("")
                seleccion3 = input("¿Desea dar de baja el usuario? s/n: ")
                seleccion3 = seleccion3.lower()
                if seleccion3 == "s":
                    clear()
                    consulta = "DELETE FROM usuario WHERE id = %s"
                    cursor.execute(consulta, (id))
                    conexion.commit()
                    if exito == True:
                        print("USUARIO DADO DE BAJA CORRECTAMENTE")
                    else:
                        return
                elif seleccion3 == "n":
                    clear()
                    anykey = input("Se canceló la baja del usuario. Presione ENTER para continuar.")
                else:
                    clear()
                    print("Opción ingresada no válida, por favor ingrese s/n.")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al dar de baja el usuario: ", f)


def modificarusuario():
    try:
        with conexion.cursor() as cursor:
            seleccion3 = 0
            x = 0
            T = PrettyTable(["ID", "Nombre", "Clave"])
            id = input("Ingrese el ID del usuario a modificar: ")
            while seleccion3 != 3:
                consulta = "SELECT * FROM usuario WHERE id = %s;"
                cursor.execute(consulta, (id))
                usuario = cursor.fetchall()
                if not usuario:
                    print("El ID ingresado no es válido.\n")
                    exito = False
                    return
                else:
                    exito = True
                clear()
                T.clear_rows()
                for x in usuario:
                    T.add_row(x)
                print(T)
                print("")
                seleccion3 = int(input("¿Qué desea modificar? (1= Nombre / 2= Clave / 3= Cancelar): "))
                if seleccion3 == 1:
                    nombre = input("Ingrese el nuevo nombre del usuario: ")
                    consulta = "UPDATE usuario SET nombre = %s WHERE id = %s ;"
                    cursor.execute(consulta, (nombre, id))
                elif seleccion3 == 2:
                    clave = input("Ingrese la nueva clave del usuario: ")
                    consulta = "UPDATE usuario SET clave = %s WHERE id = %s ;"
                    cursor.execute(consulta, (clave, id))
                elif seleccion3 == 3:
                    break
                else:
                    clear()
                    anykey = input("Ingrese un número de 1 al 3, presione ENTER para intentar nuevamente.")
        conexion.commit()
        clear()
        if exito == True:
            print("USUARIO MODIFICADO CON ÉXITO")
        else:
            return
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al modificar el usuario: ", f)


def listarusuario():
    try:
        with conexion.cursor() as cursor:
            x = 0
            T = PrettyTable(["ID", "Nombre", "Clave"])
            cursor.execute("SELECT * FROM usuario;")
            usuario = cursor.fetchall()
            for x in usuario:
                T.add_row(x)
            print(T.get_string(title="USUARIOS"))
        print("")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al mostrar los usuarios: ", f)