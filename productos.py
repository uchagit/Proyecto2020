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
        print("--MENU PRODUCTOS--\n")
        print("1) Agregar producto")
        print("2) Eliminar producto")
        print("3) Modificar producto")
        print("4) Listar productos")
        print("5) Regresar al menú principal\n")

        try:
            seleccion = int(input("Seleccione una opción: "))
            if seleccion == 1:
                clear()
                agregarproducto()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea agregar otro producto? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        agregarproducto()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 2:
                clear()
                eliminarproducto()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea eliminar otro producto? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        eliminarproducto()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 3:
                clear()
                modificarproducto()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea modificar otro producto? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        modificarproducto()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 4:
                clear()
                listarproducto()
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


def agregarproducto():
    try:
        with conexion.cursor() as cursor:
            x = 0
            T = PrettyTable(["ID", "Nombre", "Precio", "Stock"])
            nombre = input("Ingrese el nombre del producto: ")
            precio = input("Ingrese el precio del producto: ")
            stock = input("Ingrese el stock del producto: ")
            consulta = "INSERT INTO producto(nombre,precio,stock) VALUES (%s, %s, %s);"
            cursor.execute(consulta, (nombre, precio, stock))
            consulta = "SELECT * FROM producto WHERE nombre = %s;"
            cursor.execute(consulta, (nombre))
            producto = cursor.fetchall()
        conexion.commit()
        clear()
        T.clear_rows()
        for x in producto:
            T.add_row([x[0], x[1], x[2], x[3]])
        print(T)
        print("")
        print("PRODUCTO AGREGADO CON ÉXITO")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al agregar el producto: ", f)


def eliminarproducto():
    try:
        with conexion.cursor() as cursor:
            seleccion3 = ""
            x = 0
            T = PrettyTable(["ID", "Nombre", "Precio", "Stock"])
            id = input("Ingrese el ID del producto a eliminar: ")
            while seleccion3 not in ["s","n"]:
                consulta = "SELECT * FROM producto WHERE id = %s;"
                cursor.execute(consulta, (id))
                producto = cursor.fetchall()
                if not producto:
                    print("El ID ingresado no es válido.\n")
                    exito = False
                    return
                else:
                    exito = True
                clear()
                T.clear_rows()
                for x in producto:
                    T.add_row([x[0], x[1], x[2], x[3]])
                print(T)
                print("")
                seleccion3 = input("¿Desea eliminar el producto? s/n: ")
                seleccion3 = seleccion3.lower()
                if seleccion3 == "s":
                    clear()
                    consulta = "DELETE FROM producto WHERE id = %s"
                    cursor.execute(consulta, (id))
                    conexion.commit()
                    if exito == True:
                        print("PRODUCTO ELIMINADO CON ÉXITO")
                    else:
                        return
                elif seleccion3 == "n":
                    clear()
                    anykey = input("Se canceló la eliminación del producto. Presione ENTER para continuar.")
                else:
                    clear()
                    print("Opción ingresada no válida, por favor ingrese s/n.")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al eliminar el producto: ", f)


def modificarproducto():
    try:
        with conexion.cursor() as cursor:
            seleccion3 = 0
            x = 0
            T = PrettyTable(["ID", "Nombre", "Precio", "Stock"])
            id = input("Ingrese el ID del producto a modificar: ")
            while seleccion3 != 4:
                consulta = "SELECT * FROM producto WHERE id = %s;"
                cursor.execute(consulta, (id))
                producto = cursor.fetchall()
                if not producto:
                    print("El ID ingresado no es válido.\n")
                    exito = False
                    return
                else:
                    exito = True
                clear()
                T.clear_rows()
                for x in producto:
                    T.add_row([x[0], x[1], x[2], x[3]])
                print(T)
                print("")
                seleccion3 = int(input("¿Qué desea modificar? (1= Nombre / 2= Precio / 3= Stock / 4= Cancelar): "))
                if seleccion3 == 1:
                    nombre = input("Ingrese el nuevo nombre del producto: ")
                    consulta = "UPDATE producto SET nombre = %s WHERE id = %s ;"
                    cursor.execute(consulta, (nombre, id))
                elif seleccion3 == 2:
                    precio = input("Ingrese el nuevo precio del producto: ")
                    consulta = "UPDATE producto SET precio = %s WHERE id = %s ;"
                    cursor.execute(consulta, (precio, id))
                elif seleccion3 == 3:
                    stock = input("Ingrese el nuevo stock del producto: ")
                    consulta = "UPDATE producto SET stock = %s WHERE id = %s ;"
                    cursor.execute(consulta, (stock, id))
                elif seleccion3 == 4:
                    break
                else:
                    clear()
                    anykey = input("Ingrese un número de 1 al 4, presione ENTER para intentar nuevamente.")
        conexion.commit()
        clear()
        if exito == True:
            print("PRODUCTO MODIFICADO CON ÉXITO")
        else:
            return
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al modificar el producto: ", f)


def listarproducto():
    try:
        with conexion.cursor() as cursor:
            x = 0
            T = PrettyTable(["ID", "Nombre", "Precio", "Stock"])
            cursor.execute("SELECT * FROM producto;")
            producto = cursor.fetchall()
            for x in producto:
                T.add_row([x[0], x[1], x[2], x[3]])
            print(T.get_string(title="PRODUCTOS"))
        print("")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al mostrar los productos: ", f)