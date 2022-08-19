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
        print("--MENÚ VENTAS--\n")
        print("1) Realizar venta")
        print("2) Eliminar venta")
        print("3) Modificar venta")
        print("4) Listar ventas")
        print("5) Regresar al menú principal\n")

        try:
            seleccion = int(input("Seleccione una opción: "))
            if seleccion == 1:
                clear()
                realizarventa()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea realizar otra venta? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        realizarventa()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 2:
                clear()
                eliminarventa()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea eliminar otra venta? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        eliminarventa()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 3:
                clear()
                modificarventa()
                seleccion2 = "s"
                while seleccion2 != "n":
                    seleccion2 = input("¿Desea modificar otra venta? s/n: ")
                    seleccion2 = seleccion2.lower()
                    if seleccion2 == "s":
                        clear()
                        modificarventa()
                    elif seleccion2 == "n":
                        break
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
            elif seleccion == 4:
                clear()
                listarrventa()
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


def realizarventa():
    try:
        with conexion.cursor() as cursor:
            x = 0
            T = PrettyTable(["ID", "Fecha", "Total", "ID Cliente", "Nombre", "Dirección", "Teléfono", "Mail"])
            fecha = "SELECT CURDATE()"
            total = float(0)
            subtotal= float(0)
            cursor.execute(fecha)
            fecha = cursor.fetchone()
            idcliente = input("Ingrese el ID del cliente: ")
            consulta = "SELECT * FROM cliente WHERE id = %s;"
            cursor.execute(consulta, (idcliente))
            idcliente2 = cursor.fetchall()
            if not idcliente2:
                print("El cliente ingresado ingresado no es válido.\n")
                return
            else:
                T.clear_rows()
            consulta = "INSERT INTO compra(fecha, id_cliente) VALUES (%s, %s);"
            cursor.execute(consulta, (fecha, idcliente))
            consulta = "SELECT id, CAST(fecha AS CHAR), id_cliente, total FROM compra ORDER BY id DESC LIMIT 1"
            cursor.execute(consulta)
            compra = cursor.fetchone()
            consulta2 = "SELECT id FROM compra ORDER BY id DESC LIMIT 1;"
            cursor.execute(consulta2)
            idcompra = cursor.fetchone()
            idproducto = input("Ingrese ID del producto a vender: ")
            consulta = "SELECT * FROM producto WHERE id = %s;"
            cursor.execute(consulta, (idproducto))
            idproducto2 = cursor.fetchall()
            if not idproducto2:
                print("El producto ingresado no es válido.\n")
                return
            else:
                T.clear_rows()
            cantidad = int(input("Ingrese la cantidad deseada: "))
            aprobado = controlstock(idproducto, cantidad)
            if aprobado == 0:
                return
            else:
                consultaprecio = "SELECT precio FROM producto WHERE id = %s"
                cursor.execute(consultaprecio, (idproducto))
                subtotal = float(cursor.fetchone()[0])
                subtotal = subtotal * cantidad
                total = total + subtotal
                consulta3 = "INSERT INTO detalle_compra(id_compra, id_producto, cantidad, total) VALUES (%s, %s, %s, %s);"
                cursor.execute(consulta3, (idcompra, idproducto, cantidad, subtotal))
                seleccion3 = ""
                while seleccion3 !="n":
                    seleccion3 = input("¿Desea agregar otro producto a la venta? s/n: ")
                    seleccion3 = seleccion3.lower()
                    if seleccion3 == "s":
                        clear()
                        idproducto = input("Ingrese ID del producto a vender: ")
                        cantidad = int(input("Ingrese la cantidad deseada: "))
                        aprobado = controlstock(idproducto, cantidad)
                        if aprobado == 0:
                            return
                        else:
                            consultaprecio = "SELECT precio FROM producto WHERE id = %s"
                            cursor.execute(consultaprecio, (idproducto))
                            subtotal = float(cursor.fetchone()[0])
                            subtotal = subtotal * cantidad
                            total = total + subtotal
                            consulta3 = "INSERT INTO detalle_compra(id_compra, id_producto, cantidad, total) VALUES (%s, %s, %s, %s);"
                            cursor.execute(consulta3, (idcompra, idproducto, cantidad, subtotal))
                    elif seleccion3 == "n":
                        clear()
                        consulta = "UPDATE compra SET total = %s WHERE id = %s"
                        cursor.execute(consulta, (total, idcompra))
                        consulta = "SELECT compra.id, CAST(compra.fecha AS CHAR), compra.total, compra.id_cliente, cliente.nombre, cliente.direccion, cliente.telefono, cliente.mail FROM compra INNER JOIN cliente ON compra.id_cliente = cliente.id ORDER BY id DESC LIMIT 1"
                        cursor.execute(consulta)
                        compra = cursor.fetchall()
                        T.clear_rows()
                        for x in compra:
                            T.add_row(x)
                        clear()
                        print(T)
                        seleccion4 = ""
                        seleccion4 = input("¿CONFIRMAR VENTA? s/n: ")
                        seleccion4 = seleccion4.lower()
                        if seleccion4 == "s":
                            clear()
                            conexion.commit()
                            print("VENTA REALIZADA EXITOSAMENTE")
                        elif seleccion4 == "n":
                            clear()
                            conexion.rollback()
                            anykey = input("Se canceló la venta. Presione ENTER para continuar.")
                        else:
                            clear()
                            print("Opción ingresada no válida, por favor ingrese s/n.")
                    else:
                        clear()
                        print("Opción ingresada no válida, por favor ingrese s/n.")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al realizar la venta: ", f)


def eliminarventa():
    try:
        with conexion.cursor() as cursor:
            x = 0
            T = PrettyTable(["ID", "Fecha", "Total", "ID Cliente", "Nombre", "Dirección", "Teléfono", "Mail"])
            seleccion3 = ""
            id = input("Ingrese el ID de la venta a eliminar: ")
            while seleccion3 not in ["s","n"]:
                consulta = "SELECT compra.id, CAST(compra.fecha AS CHAR), compra.total, compra.id_cliente, cliente.nombre, cliente.direccion, cliente.telefono, cliente.mail FROM compra INNER JOIN cliente ON compra.id_cliente = cliente.id WHERE compra.id = %s;"
                cursor.execute(consulta, (id))
                compra = cursor.fetchall()
                if not compra:
                    print("El ID ingresado no es válido.\n")
                    exito = False
                    return
                else:
                    exito = True
                T.clear_rows()
                for x in compra:
                    T.add_row(x)
                clear()
                print(T)
                print("")
                seleccion3 = input("¿Desea eliminar la venta? s/n: ")
                seleccion3 = seleccion3.lower()
                if seleccion3 == "s":
                    clear()
                    consulta = "DELETE FROM compra WHERE id = %s"
                    cursor.execute(consulta, (id))
                    consulta = "DELETE FROM detalle_compra WHERE id_compra = %s"
                    cursor.execute(consulta, (id))
                    conexion.commit()
                    if exito == True:
                        print("VENTA ELIMINADA CON ÉXITO")
                    else:
                        return
                elif seleccion3 == "n":
                    clear()
                    anykey = input("Se canceló la eliminación de la venta. Presione ENTER para continuar.")
                else:
                    clear()
                    print("Opción ingresada no válida, por favor ingrese s/n.")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al eliminar la venta: ", f)


def modificarventa():
    try:
        with conexion.cursor() as cursor:
            x = 0
            seleccion3 = 0
            T = PrettyTable(["ID", "Fecha", "ID Cliente", "Total"])
            id = input("Ingrese el ID de la venta a modificar: ")
            while seleccion3 != 3:
                consulta = "SELECT id, CAST(fecha AS CHAR), id_cliente, total FROM compra WHERE id = %s;"
                cursor.execute(consulta, (id))
                compra = cursor.fetchall()
                if not compra:
                    print("El ID ingresado no es válido.\n")
                    exito = False
                    return
                else:
                    exito = True
                T.clear_rows()
                for x in compra:
                    T.add_row(x)
                clear()
                print(T)
                print("")
                seleccion3 = int(input("¿Qué desea modificar? (1= Fecha / 2= ID del cliente / 3= Cancelar): "))
                if seleccion3 == 1:
                    fecha = input("Ingrese la nueva fecha de la venta (AAAA-MM-DD): ")
                    consulta = "UPDATE compra SET fecha = %s WHERE id = %s ;"
                    cursor.execute(consulta, (fecha, id))
                elif seleccion3 == 2:
                    idcliente = input("Ingrese el nuevo ID del cliente: ")
                    consulta = "UPDATE compra SET id_cliente = %s WHERE id = %s ;"
                    cursor.execute(consulta, (idcliente, id))
                elif seleccion3 == 3:
                    break
                else:
                    clear()
                    anykey = input("Ingrese un número de 1 al 3, presione ENTER para intentar nuevamente.")
        conexion.commit()
        clear()
        if exito == True:
            print("VENTA MODIFICADA CON ÉXITO")
        else:
            return
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al modificar la venta: ", f)


def listarrventa():
    try:
        seleccion = 0
        with conexion.cursor() as cursor:
            x = 0
            total = 0
            T = PrettyTable(["ID", "Fecha", "Total", "ID Cliente", "Nombre", "Dirección", "Teléfono", "Mail"])
            T2 = PrettyTable(["ID", "ID Compra", "ID Producto", "Cantidad", "Subtotal"])
            cursor.execute("SELECT compra.id, CAST(compra.fecha AS CHAR), compra.total, compra.id_cliente, cliente.nombre, cliente.direccion, cliente.telefono, cliente.mail FROM compra INNER JOIN cliente ON compra.id_cliente = cliente.id;")
            compra = cursor.fetchall()
            cursor.execute("SELECT SUM(total) AS totalsum FROM compra;")
            total = (cursor.fetchone()[0])
            for x in compra:
                T.add_row(x)
        while seleccion not in ["n", "N"]:
            T2.clear_rows()
            clear()
            print(T.get_string(title="VENTAS REALIZADAS"))
            print("")
            print(f"Total de ventas realizadas: ${total}")
            print("")
            if seleccion == 0:
                seleccion = input("¿Desea ver el detalle de alguna venta? s/n: ")
            else:
                seleccion = input("¿Desea ver el detalle de otra venta? s/n: ")
            try:
                with conexion.cursor() as cursor:
                    if seleccion in ["s", "S"]:
                        print("")
                        iddetalle = input("Ingrese el ID de la venta a detallar: ")
                        print("")
                        consultadetalle = ("SELECT * FROM detalle_compra WHERE id_compra = %s")
                        cursor.execute(consultadetalle, (iddetalle))
                        ventadetalle = cursor.fetchall()
                        if not ventadetalle:
                            print("El ID ingresado no es válido.\n")
                            exito = False
                            return
                        for x in ventadetalle:
                            T2.add_row(x)
                        print(T2.get_string(title=f"DETALLE VENTA NÚMERO {iddetalle}"))
                        print("")
                        anykey = input("Presione ENTER para volver al listado de ventas.")
                    elif seleccion in ["n", "N"]:
                        print("")
                        return
                    else:
                        print("Opción ingresada no válida, por favor ingrese s/n.\n")
            except (pymysql.err.Error) as f:
                print("Ocurrió un error al mostrar las ventas: ", f)
        print("")
    except (pymysql.err.Error) as f:
        print("Ocurrió un error al mostrar las ventas: ", f)


def controlstock(idproducto, cantidad):
    aprobado = 0
    with conexion.cursor() as cursor:
        consultastock = ("SELECT stock FROM producto WHERE id = %s")
        cursor.execute(consultastock, (idproducto))
        stock = cursor.fetchone()
        T1 = int(cantidad)
        T2 = int(stock[0])
        T3 = T2 - T1
        if T2 == 0:
            aprobado = 0
            clear()
            conexion.rollback()
            print("El producto seleccionado no cuenta con stock disponible para venta.\n")
            return aprobado
        elif T1 > T2:
            aprobado = 0
            clear()
            conexion.rollback()
            print("La cantidad ingresada (",T1,") supera el stock del producto (",T2,").\n")
            return aprobado
        else:
            aprobado = 1
            consultastock = ("UPDATE producto SET stock = %s WHERE id = %s")
            cursor.execute(consultastock, (T3, idproducto))
            return aprobado