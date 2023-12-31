import csv
import os
from listas.double_list import DoubleList  # Importa la clase DoubleList para usarla en el sistema de mensajería
from .empleado import Empleado
from .fecha import Fecha
from .direccion import Direccion

class Sistema_Empleados:
    def __init__(self):
        self.empleados = DoubleList()  # Lista de empleados
        self.noEmpleados = 0

    def agregarEmpleado(self, empleado):
        # Agregar un nuevo usuario
        id = int(input("\nID del usuario: "))

        if self.buscarUsuario(id):
            print(f"\nYa existe un usuario con el ID {id}.")
            return False

        else:         
            nombre = input("Nombre del usuario: ")
            fecha_nac = Fecha(*map(int, input("Fecha de nacimiento (dd/mm/aaaa): ").split("/")))
            ciudad_nac = input("Ciudad de nacimiento: ")

            dir = Direccion(*input("Dirección (calle, noCalle, nomenclatura, barrio, ciudad): ").split(", "))

            tel = int(input("Teléfono: "))
            email = input("Correo electrónico: ")

            cargo = input("Usuario: ¿empleado o administrador?: ")
            password = input("Ingrese la contraseña: ")

            empleado = Empleado(id, nombre, fecha_nac, ciudad_nac, dir, tel, email, cargo, password)

            self.empleados.addOrder(empleado)
            self.noEmpleados +=1
            self.createtxt(empleado.id)
            
            print("\nUsuario agregado con éxito.")
       
        return True

    def eliminarEmpleado(self, id):
        empleado = self.buscarUsuario(id)
        if empleado:
            self.empleados.remove(empleado)
            self.noEmpleados -= 1
            return f"Empleado con ID {id} eliminado correctamente."
        return f"No se encontró ningún empleado con el ID {id}."
      
    def mostrarEmpleados(self):
        current = self.empleados.head
        while current is not None:
            print("\n", current.get_data())  # Aquí asumimos que get_data() devuelve el valor almacenado en el nodo
            current = current.get_next()  

    def buscarUsuario(self, id):
        current = self.empleados.head
        while current:
            if current.data.id == id:
                return current
            current = current.next
        return None
    
    def buscarCorreo(self, correo):
        current = self.empleados.head
        while current:
            if current.data.email == correo:
                return current
            current = current.next
        return None

    def cargarEmpleados(self, archivo_empleados):
        with open(archivo_empleados, "r", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.noEmpleados = 0
            for row in reader:
                id = int(row['ID'])
                nombre = row['Nombre']
                fecha_nac_str = row['Fecha de nacimiento']
                fecha_nac_data = fecha_nac_str.split('/')
                dia, mes, año = map(int, fecha_nac_data)
                fecha_nac = Fecha(dia, mes, año)
                ciudad_nac = row['Ciudad de nacimiento']

                direccion_data = row['Direccion'].split('-')
                calle = direccion_data[0]
                noCalle = direccion_data[1]
                nomenclatura = direccion_data[2]
                barrio = direccion_data[3]
                ciudad = direccion_data[-1]

                dir = Direccion(calle, noCalle, nomenclatura, barrio, ciudad)
                tel = int(row['Telefono'])
                email = row['Correo electronico']

                empleado = Empleado(id, nombre, fecha_nac, ciudad_nac, dir, tel, email, None, None)
                
                self.empleados.addOrder(empleado)
                self.noEmpleados +=1
                self.createtxt(empleado.id)
        return "Todos los empleados fueron cargados con éxito"

    def cargarPassword(self, archivo_password):
        
        with open(archivo_password, 'r') as file:
            for line in file:
                data = [x.strip() for x in line.split(" ")]
                id = data[0]
                password = data[1]
                cargo = data[2]

                #print(id, password, cargo)

                current_node = self.buscarUsuario(int(id))
                #print(current_node)
                if current_node.data.id == int(id):
                    current_node.data.setPassword(password)
                    current_node.data.setCargo(cargo)

    def toFileEmpleados(self, filename):
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)

            # Escribir los encabezados
            writer.writerow(["ID", "Nombre", "Fecha de nacimiento", "Ciudad de nacimiento", "Direccion", "Telefono", "Correo electronico"])

            # Recorrer los nodos de la lista doblemente enlazada y escribir los datos en el archivo
            current = self.empleados.head
            while current is not None:
                usuario = current.get_data()

                # Formatear la dirección con espacios en lugar de comas
                direccion_str = f"{usuario.dir.calle}-{usuario.dir.noCalle}-{usuario.dir.nomenclatura}-{usuario.dir.barrio}-{usuario.dir.ciudad}"

                writer.writerow([usuario.id, usuario.nombre, usuario.fecha_nac.obtener_fecha(),
                                usuario.ciudad_nac, direccion_str, usuario.tel, usuario.email])
                current = current.get_next()
                
    def toFilePassword(self, filename):
        with open(filename, "w") as file:
            for empleado in self.empleados:
                line = f"{empleado.getId()} {empleado.password} {empleado.cargo}\n"
                file.write(line)

    def verificarAcceso(self, id, password):
        current = self.buscarUsuario(int(id))
        if current.data.password == password:
            return current.data.cargo
        return None
    
    def createtxt(self, id):
        carpeta_destino = "./txt"
        nombre_archivoBA = f"{str(id)}_BA.txt"
        nombre_archivoML = f"{str(id)}_ML.txt"
        nombre_archivoB = f"{str(id)}_B.txt"
        ruta_completa1 = os.path.join(carpeta_destino, nombre_archivoBA)
        ruta_completa2 = os.path.join(carpeta_destino, nombre_archivoML)
        ruta_completa3 = os.path.join(carpeta_destino, nombre_archivoB)
        
        # Verificar si el archivo ya existe
        if os.path.exists(ruta_completa1):
            return None
        else:
            # Intenta crear el archivo en la carpeta de destino
            try:
                with open(ruta_completa1, "w") as archivo:
                    archivo.write("")
            except Exception as e:
                print(f"\nError al crear el archivo: {str(e)}")

        # Verificar si el archivo ya existe
        if os.path.exists(ruta_completa2):
            return None
        else:
            # Intenta crear el archivo en la carpeta de destino
            try:
                with open(ruta_completa2, "w") as archivo:
                    archivo.write("")
            except Exception as e:
                print(f"\nError al crear el archivo: {str(e)}")

        # Verificar si el archivo ya existe
        if os.path.exists(ruta_completa3):
            return None
        else:
            # Intenta crear el archivo en la carpeta de destino
            try:
                with open(ruta_completa3, "w") as archivo:
                    archivo.write("")
            except Exception as e:
                print(f"\nError al crear el archivo: {str(e)}")


    def cambiarPassword(self):
        #Busca la contraseña del empleado 
        id = int(input("\nIngrese ID del usuario a cambiar contraseña: "))
        current = self.buscarUsuario(int(id))
        # Cambia la contraseña del empleado
        if current is not None:
            new_password = input("Ingrese la nueva contraseña: ")
            current.data.setPassword(new_password)
            return print(f"\nContraseña del empleado {current.data.nombre} cambiada con éxito.")
        else:
            return print("\nNingun usuario asignado a esa ID")