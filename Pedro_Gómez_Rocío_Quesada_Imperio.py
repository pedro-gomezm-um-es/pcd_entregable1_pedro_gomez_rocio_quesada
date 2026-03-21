from enum import Enum
from abc import ABCMeta, abstractmethod

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

    # Método para OBTENER la cantidad
    def get_cantidad(self):
        return self.__cantidad

    # Método para CAMBIAR la cantidad con validación
    def set_cantidad(self, valor):
        if valor >= 0:
            self.__cantidad = valor
        else:
            raise ValueError("La cantidad no puede ser negativa")

class Almacen:
    def __init__(self, nombre, localizacion):
        self.nombre = nombre
        self.localizacion = localizacion
        self.inventario = {}

    def añadir_repuesto(self, repuesto):
        self.inventario[repuesto.nombre] = repuesto

    def reducir_stock(self, nombre_pieza, cantidad_pedida):
        if nombre_pieza not in self.inventario:
            raise Exception(f"Error: El repuesto '{nombre_pieza}' no existe.")
        
        pieza = self.inventario[nombre_pieza]
        
        # IMPORTANTE: Usamos get_cantidad() y set_cantidad()
        if pieza.get_cantidad() < cantidad_pedida:
            raise Exception(f"Error: Stock insuficiente. Disponible: {pieza.get_cantidad()}")
        
        nueva_qty = pieza.get_cantidad() - cantidad_pedida
        pieza.set_cantidad(nueva_qty)
        print(f"Stock actualizado: {nombre_pieza}. Restante: {pieza.get_cantidad()}")

    def reponer_stock(self, nombre_pieza, cantidad_nueva):
        if nombre_pieza in self.inventario:
            pieza = self.inventario[nombre_pieza]
            # IMPORTANTE: Usamos get_cantidad() y set_cantidad()
            pieza.set_cantidad(pieza.get_cantidad() + cantidad_nueva)
            print(f"[OPERARIO] Stock de {nombre_pieza} aumentado a {pieza.get_cantidad()}")

class Nave(Unidad, metaclass=ABCMeta):
    def __init__(self, id_combate, clave, nombre, catalogo):
        Unidad.__init__(self, id_combate, clave)
        self.nombre = nombre
        self.catalogo = catalogo

    @abstractmethod
    def realizar_mision(self):
        pass

    # Método para el Comandante: Consultar repuestos en un almacén
    def consultar_repuestos(self, almacen):
        print(f"\n[COMANDANTE - {self.nombre}] Consultando stock en {almacen.nombre}...")
        for nombre, repuesto in almacen.inventario.items():
            compatible = "SÍ" if nombre in self.catalogo else "NO"
            print(f"- {nombre}: {repuesto.get_cantidad()} unidades (Compatible: {compatible})")

    # Método para el Comandante: Adquirir repuesto
    def adquirir_repuesto(self, almacen, nombre_pieza, cantidad):
        # Usamos la función de mantenimiento que ya tenemos o la metemos aquí
        solicitar_mantenimiento(self, almacen, nombre_pieza, cantidad)

class EstacionEspacial(Nave):
    def __init__(self, id_combate, clave, nombre, catalogo, tripulacion, pasaje, ubicacion):
        super().__init__(id_combate, clave, nombre, catalogo)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion 
    def mostrar_info(self):
        print(f"\n--- ESTACIÓN ESPACIAL: {self.nombre} ---")
        print(f"ID: {self.id_combate} | Ubicación: {self.ubicacion}")
        print(f"Personal: {self.tripulacion} tripulantes y {self.pasaje} pasajeros.")

    def realizar_mision(self):
        print(f"La estación {self.nombre} mantiene la vigilancia en {self.ubicacion}.")

class NaveEstelar(Nave):
    def __init__(self, id_combate, clave, nombre, catalogo, tripulacion, pasaje, clase_nave):
        super().__init__(id_combate, clave, nombre, catalogo)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase_nave = clase_nave

    def mostrar_info(self):
        print(f"\n--- NAVE ESTELAR: {self.nombre} ---")
        print(f"ID: {self.id_combate} | Clase: {self.clase_nave.value}")
        print(f"Capacidad: {self.tripulacion + self.pasaje} personas totales.")

    def realizar_mision(self):
        print(f"La nave {self.nombre} de clase {self.clase_nave.value} inicia salto hiperespacial.")

class CazaEstelar(Nave):
    def __init__(self, id_combate, clave, nombre, catalogo, dotacion):
        super().__init__(id_combate, clave, nombre, catalogo)
        self.dotacion = dotacion

    def mostrar_info(self):
        print(f"\n--- CAZA ESTELAR: {self.nombre} ---")
        print(f"ID: {self.id_combate} | Dotación: {self.dotacion} pilotos.")

    def realizar_mision(self):
        print(f"El caza {self.nombre} sale en formación de ataque.")

# --- 2.3: GESTIÓN DE EXCEPCIONES Y PRUEBAS ---

def solicitar_mantenimiento(nave, almacen, pieza_nombre, cantidad):
    """Lógica centralizada para adquirir repuestos con control de errores [cite: 23]"""
    print(f"\n[SOLICITUD] {nave.nombre} solicita {cantidad} unidades de '{pieza_nombre}'")
    try:
        # Validación de catálogo (Regla de negocio)
        if pieza_nombre not in nave.catalogo:
            raise Exception(f"Incompatibilidad: La pieza '{pieza_nombre}' no figura en el catálogo de {nave.nombre}.")
        
        # Validación de Almacén
        almacen.reducir_stock(pieza_nombre, cantidad)
        print(f"[ÉXITO] Suministro completado para {nave.nombre}.")
        
    except Exception as e:
        print(f"[ERROR CAPTURADO] {e}")

