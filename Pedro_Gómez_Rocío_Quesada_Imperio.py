from enum import Enum
from abc import ABCMeta, abstractmethod

# Definimos las clases
class EClaseNave(Enum):
    Ejecutor = "Ejecutor"
    Eclipse = "Eclipse"
    Soberano = "Soberano"

class Unidad(metaclass=ABCMeta):
    def __init__(self, id_combate, clave_transmision):
        self.id_combate = id_combate
        self.clave_transmision = clave_transmision

    @abstractmethod
    def mostrar_info(self):
        pass

class Repuesto:
    def __init__(self, nombre, proveedor, cantidad, precio):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad  # Atributo privado
        self.precio = precio

    # Método para obtener la cantidad
    def get_cantidad(self):
        return self.__cantidad

    # Método para cambiar la cantidad
    def set_cantidad(self, valor):
        if valor >= 0: # comprobamos que el valor de la cantidad es positivo
            self.__cantidad = valor
        else:
            raise ValueError("La cantidad no puede ser negativa")

class Almacen:
    def __init__(self, nombre, localizacion):
        self.nombre = nombre
        self.localizacion = localizacion
        self.inventario = {}

    # Método para añadir un nuevo repuesto
    def añadir_repuesto(self, repuesto):
        self.inventario[repuesto.nombre] = repuesto

    # Método para reducir el stock
    def reducir_stock(self, nombre_pieza, cantidad_pedida):
        if nombre_pieza not in self.inventario: # comprueba que exista la pieza en el inventario
            raise Exception(f"Error: El repuesto '{nombre_pieza}' no existe.")
        
        pieza = self.inventario[nombre_pieza]
        
        # Comprobamos que hay stock suficiente
        if pieza.get_cantidad() < cantidad_pedida:
            raise Exception(f"Error: el stock es insuficiente. El stock disponible es: {pieza.get_cantidad()}")
        
        # Actualizamos si se puede realizar la operación
        nueva_qty = pieza.get_cantidad() - cantidad_pedida
        pieza.set_cantidad(nueva_qty)
        print(f"Stock actualizado: {nombre_pieza}. Restante: {pieza.get_cantidad()}")

    # Método para aumentar el stock
    def reponer_stock(self, nombre_pieza, cantidad_nueva):
        if nombre_pieza in self.inventario:
            pieza = self.inventario[nombre_pieza]
            # Aumentamos el stock usando las funciones que ya tenemos definidas
            pieza.set_cantidad(pieza.get_cantidad() + cantidad_nueva)
            print(f"Stock de {nombre_pieza} aumentado a {pieza.get_cantidad()}")

class Nave(Unidad, metaclass=ABCMeta):
    def __init__(self, id_combate, clave, nombre, catalogo):
        Unidad.__init__(self, id_combate, clave)
        self.nombre = nombre
        self.catalogo = catalogo

    # Método para consultar repuestos en un almacén
    def consultar_repuestos(self, almacen):
        print(f"\nEl comandante {self.nombre} está consultando stock en {almacen.nombre}.")
        for nombre, repuesto in almacen.inventario.items():
            compatible = "SÍ" if nombre in self.catalogo else "NO"
            print(f"{nombre}: {repuesto.get_cantidad()} unidades (Compatible: {compatible})")

    # Método para adquirir repuesto
    def adquirir_repuesto(self, almacen, nombre_pieza, cantidad):
        # Usamos la función de mantenimiento que ya tenemos o la metemos aquí
        solicitar_mantenimiento(self, almacen, nombre_pieza, cantidad)

class EstacionEspacial(Nave):
    def __init__(self, id_combate, clave, nombre, catalogo, tripulacion, pasaje, ubicacion):
        super().__init__(id_combate, clave, nombre, catalogo)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion 

    # Método para mostrar la información    
    def mostrar_info(self):
        print(f"\nESTACIÓN ESPACIAL: {self.nombre}")
        print(f"ID: {self.id_combate}.  Ubicación: {self.ubicacion}")
        print(f"Personal: {self.tripulacion} tripulantes y {self.pasaje} pasajeros.")

    # Método para realizar misión
    def realizar_mision(self):
        print(f"La estación {self.nombre} mantiene la vigilancia en {self.ubicacion}.")

class NaveEstelar(Nave):
    def __init__(self, id_combate, clave, nombre, catalogo, tripulacion, pasaje, clase_nave):
        super().__init__(id_combate, clave, nombre, catalogo)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase_nave = clase_nave

    # Método para mostrar información
    def mostrar_info(self):
        print(f"\nNAVE ESTELAR: {self.nombre}")
        print(f"ID: {self.id_combate}. Clase: {self.clase_nave.value}")
        print(f"Capacidad: {self.tripulacion + self.pasaje} personas totales.")

    def realizar_mision(self):
        print(f"La nave {self.nombre} de clase {self.clase_nave.value} inicia salto hiperespacial.")

class CazaEstelar(Nave):
    def __init__(self, id_combate, clave, nombre, catalogo, dotacion):
        super().__init__(id_combate, clave, nombre, catalogo)
        self.dotacion = dotacion

    def mostrar_info(self):
        print(f"\n Caza estelar: {self.nombre}.")
        print(f"El id de combate es {self.id_combate}. La dotación es {self.dotacion} pilotos.")

    def realizar_mision(self):
        print(f"El caza {self.nombre} sale en formación de ataque.")

# Ahora hacemos la gestión de errores
def solicitar_mantenimiento(nave, almacen, pieza_nombre, cantidad):
    """Adquirir repuestos con control de errores"""
    print(f"\n{nave.nombre} solicita {cantidad} unidades de '{pieza_nombre}'")
    try:
        # Validación de catálogo (comprobamos que la pieza existe en el catálogo)
        if pieza_nombre not in nave.catalogo:
            raise Exception(f"Incompatibilidad: La pieza '{pieza_nombre}' no figura en el catálogo de {nave.nombre}.")
        
        # Validación de Almacén (comprobamos que tenemos stock suficiente y lo actualizamos)
        almacen.reducir_stock(pieza_nombre, cantidad)
        print(f"Suministro completado para {nave.nombre}.")
        
    except Exception as e:
        print(f"Error: {e}")

class EUbicacionEstacion(Enum):
    ENDOR = "Endor"
    RAIMOS = "Cúmulo Raimos"
    KALIIDA = "Nebulosa Kaliida"

# Código de prueba
if __name__ == "__main__":
    # Configurar Almacén
    almacen_imperial = Almacen("Sector 7G", "Nebulosa Kaliida")
    r1 = Repuesto("Placas de Titanio", "Sienar Systems", 10, 1500.0)
    r2 = Repuesto("Célula de Energía", "Kuat Drive Yards", 5, 200.0)
    almacen_imperial.añadir_repuesto(r1)
    almacen_imperial.añadir_repuesto(r2)

    # Instanciar Naves
    estacion = EstacionEspacial("STA-01", 9988, "Estrella de la Muerte", ["Placas de Titanio"], 50000, 10000, "Endor")
    caza = CazaEstelar("TIE-44", 1122, "TIE Advanced", ["Célula de Energía"], 1)

    # Mostrar Información y Misiones
    estacion.mostrar_info()
    estacion.realizar_mision()
    caza.mostrar_info()
    
    # Pruebas de Mantenimiento y Excepciones
    # Caso Exitoso
    solicitar_mantenimiento(caza, almacen_imperial, "Célula de Energía", 2)
    
    # Caso Error: Pieza no compatible
    solicitar_mantenimiento(estacion, almacen_imperial, "Célula de Energía", 1)
    
    # Caso Error: Stock insuficiente
    solicitar_mantenimiento(caza, almacen_imperial, "Célula de Energía", 10)