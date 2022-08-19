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
        print("--MENU CLIENTES--\n")
        print("1) Agregar cliente")
        print("2) Eliminar cliente")
        print("3) Modificar cliente")
        print("4) Listar clientes")
        print("5) Regresar al menú principal\n")

        try:
            seleccion = int(input("Seleccione una opción: "))
            if seleccion == 1:
                clear()
                agregarcliente()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea agregar otro cliente? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        agregarcliente()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 2:
                clear()
                eliminarcliente()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea eliminar otro cliente? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        eliminarcliente()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 3:
                clear()
                modificarcliente()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea modificar otro cliente? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        modificarcliente()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 4:
                clear()
                listarcliente()
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


def agregarcliente():
    try:
        with conexion.cursor() as cursor:
            x = 0
            T = PrettyTable(["ID", "Nombre", "Dirección", "Teléfono", "Mail"])
            nombre = input("Ingrese el nombre del cliente: ")
            direccion = input("Ingrese el dirección del cliente: ")
            telefono = input("Ingrese el teléfono del cliente: ")
            mail = input("Ingrese el mail del cliente: ")
            consulta = "INSERT INTO cliente(nombre,direccion,telefono,mail) VALUES (%s, %s, %s, %s);"
            cursor.execute(consulta, (nombre, direccion, telefono, mail))
            consulta = "SELECT * FROM cliente WHERE nombre = %s;"
            cursor.execute(consulta, (nombre))
            cliente = cursor.fetchall()
            conexion.commit()
            clear()
            T.clear_rows()
            for x in cliente:
                T.add_row([x[0], x[1], x[2], x[3], x[4]])
            print(T)
            print("")
            print("CLIENTE AGREGADO CON ÉXITO")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al agregar el cliente: ", f)


def eliminarcliente():
    try:
        with conexion.cursor() as cursor:
            seleccion3 = ""
            x = 0
            T = PrettyTable(["ID", "Nombre", "Dirección", "Teléfono", "Mail"])
            id = input("Ingrese el ID del cliente a eliminar: ")
            while seleccion3 not in ["s","n"]:
                consulta = "SELECT * FROM cliente WHERE id = %s;"
                cursor.execute(consulta, (id))
                cliente = cursor.fetchall()
                if not cliente:
                    print("El ID ingresado no es válido.\n")
                    exito = False
                    return
                else:
                    exito = True
                clear()
                T.clear_rows()
                for x in cliente:
                    T.add_row([x[0], x[1], x[2], x[3], x[4]])
                print(T)
                print("")
                seleccion3 = input("¿Desea eliminar el cliente? s/n: ")
                seleccion3 = seleccion3.lower()
                if seleccion3 == "s":
                    clear()
                    consulta = "DELETE FROM cliente WHERE id = %s"
                    cursor.execute(consulta, (id))
                    conexion.commit()
                    if exito == True:
                        print("CLIENTE ELIMINADO CON ÉXITO")
                    else:
                        return
                elif seleccion3 == "n":
                    clear()
                    anykey = input("Se canceló la eliminación del cliente. Presione ENTER para continuar.")
                else:
                    clear()
                    print("Opción ingresada no válida, por favor ingrese s/n.")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al eliminar el cliente: ", f)


def modificarcliente():
    try:
        with conexion.cursor() as cursor:
            seleccion3 = 0
            x = 0
            T = PrettyTable(["ID", "Nombre", "Dirección", "Teléfono", "Mail"])
            id = input("Ingrese el ID del cliente a modificar: ")
            while seleccion3 != 5:
                consulta = "SELECT * FROM cliente WHERE id = %s;"
                cursor.execute(consulta, (id))
                cliente = cursor.fetchall()
                if not cliente:
                    print("El ID ingresado no es válido.\n")
                    exito = False
                    return
                else:
                    exito = True
                clear()
                T.clear_rows()
                for x in cliente:
                    T.add_row([x[0], x[1], x[2], x[3], x[4]])
                print(T)
                print("")
                seleccion3 = int(input("¿Qué desea modificar? (1= Nombre / 2= Dirección / 3= Teléfono / 4= Mail / 5= Cancelar): "))
                if seleccion3 == 1:
                    nombre = input("Ingrese el nuevo nombre del cliente: ")
                    consulta = "UPDATE cliente SET nombre = %s WHERE id = %s ;"
                    cursor.execute(consulta, (nombre, id))
                elif seleccion3 == 2:
                    direccion = input("Ingrese la nueva dirección del cliente: ")
                    consulta = "UPDATE cliente SET direccion = %s WHERE id = %s ;"
                    cursor.execute(consulta, (direccion, id))
                elif seleccion3 == 3:
                    telefono = input("Ingrese el nuevo teléfono del cliente: ")
                    consulta = "UPDATE cliente SET telefono = %s WHERE id = %s ;"
                    cursor.execute(consulta, (telefono, id))
                elif seleccion3 == 4:
                    mail = input("Ingrese el nuevo mail del cliente: ")
                    consulta = "UPDATE cliente SET mail = %s WHERE id = %s ;"
                    cursor.execute(consulta, (mail, id))
                elif seleccion3 == 5:
                    break
                else:
                    clear()
                    anykey = input("Ingrese un número de 1 al 5, presione ENTER para intentar nuevamente.")
        conexion.commit()
        clear()
        if exito == True:
            print("CLIENTE MODIFICADO CON ÉXITO")
        else:
            return
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al modificar el producto: ", f)


def listarcliente():
    try:
        with conexion.cursor() as cursor:
            x = 0
            T = PrettyTable(["ID", "Nombre", "Dirección", "Teléfono", "Mail"])
            cursor.execute("SELECT * FROM cliente;")
            cliente = cursor.fetchall()
            for x in cliente:
                T.add_row([x[0], x[1], x[2], x[3], x[4]])
            print(T.get_string(title="CLIENTES"))
        print("")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al mostrar los clientes: ", f)