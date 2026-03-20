from enum import Enum
from abc import ABCMeta, abstractmethod

# 1.10: Enumeraciones para tipos y clases (Punto 1.9 y 1.10 del PDF)
class EClaseNave(Enum):
    Ejecutor = "Ejecutor"
    Eclipse = "Eclipse"
    Soberano = "Soberano"

# 1.1: Clase abstracta base para todas las unidades imperiales
class Unidad(metaclass=ABCMeta):
    def __init__(self, id_combate, clave_transmision):
        self.id_combate = id_combate  # Texto [cite: 10]
        self.clave_transmision = clave_transmision  # Número [cite: 10]

    @abstractmethod
    def mostrar_info(self):
        pass

# --- SECCIÓN DE GESTIÓN DE REPUESTOS ---

class Repuesto:
    def __init__(self, nombre, proveedor, cantidad, precio):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad  # 1.13: ATRIBUTO PRIVADO [cite: 13]
        self.precio = precio

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if valor >= 0:
            self.__cantidad = valor
        else:
            raise ValueError("La cantidad de repuestos no puede ser negativa")

class Almacen:
    def __init__(self, nombre, localizacion):
        self.nombre = nombre # Texto [cite: 11]
        self.localizacion = localizacion # Texto [cite: 11]
        self.inventario = {} # 1.12: Diccionario para gestionar objetos Repuesto [cite: 12]

    def añadir_repuesto(self, repuesto):
        self.inventario[repuesto.nombre] = repuesto

    def reducir_stock(self, nombre_pieza, cantidad_pedida):
        if nombre_pieza not in self.inventario:
            raise Exception(f"Error: El repuesto '{nombre_pieza}' no existe en este almacén.")
        
        pieza = self.inventario[nombre_pieza]
        if pieza.cantidad < cantidad_pedida:
            raise Exception(f"Error: Stock insuficiente de '{nombre_pieza}'. Disponible: {pieza.cantidad}")
        
        pieza.cantidad -= cantidad_pedida
        print(f"Stock actualizado: {nombre_pieza} (-{cantidad_pedida}). Restante: {pieza.cantidad}")

# --- SECCIÓN DE NAVES (JERARQUÍA Y HERENCIA) ---

class Nave(Unidad, metaclass=ABCMeta):
    def __init__(self, id_combate, clave, nombre, catalogo):
        Unidad.__init__(self, id_combate, clave)
        self.nombre = nombre # Texto [cite: 7]
        self.catalogo = catalogo # Lista de nombres de piezas (texto) [cite: 7]

    @abstractmethod
    def realizar_mision(self):
        pass

class EstacionEspacial(Nave):
    def __init__(self, id_combate, clave, nombre, catalogo, tripulacion, pasaje, ubicacion):
        super().__init__(id_combate, clave, nombre, catalogo)
        self.tripulacion = tripulacion # Número [cite: 9]
        self.pasaje = pasaje # Número [cite: 9]
        self.ubicacion = ubicacion # Endor, Cúmulo Raimos, etc. [cite: 9]

    def mostrar_info(self):
        print(f"\n--- ESTACIÓN ESPACIAL: {self.nombre} ---")
        print(f"ID: {self.id_combate} | Ubicación: {self.ubicacion}")
        print(f"Personal: {self.tripulacion} tripulantes y {self.pasaje} pasajeros.")

    def realizar_mision(self):
        print(f"La estación {self.nombre} mantiene la vigilancia en {self.ubicacion}.")

class NaveEstelar(Nave):
    def __init__(self, id_combate, clave, nombre, catalogo, tripulacion, pasaje, clase_nave):
        super().__init__(id_combate, clave, nombre, catalogo)
        self.tripulacion = tripulacion # Número [cite: 9]
        self.pasaje = pasaje # Número [cite: 9]
        self.clase_nave = clase_nave # Enum EClaseNave [cite: 9]

    def mostrar_info(self):
        print(f"\n--- NAVE ESTELAR: {self.nombre} ---")
        print(f"ID: {self.id_combate} | Clase: {self.clase_nave.value}")
        print(f"Capacidad: {self.tripulacion + self.pasaje} personas totales.")

    def realizar_mision(self):
        print(f"La nave {self.nombre} de clase {self.clase_nave.value} inicia salto hiperespacial.")

class CazaEstelar(Nave):
    def __init__(self, id_combate, clave, nombre, catalogo, dotacion):
        super().__init__(id_combate, clave, nombre, catalogo)
        self.dotacion = dotacion # Número [cite: 9]

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

# 3.b: Código de prueba ejecutable 
if __name__ == "__main__":
    # 1. Configurar Almacén
    almacen_imperial = Almacen("Sector 7G", "Nebulosa Kaliida")
    r1 = Repuesto("Placas de Titanio", "Sienar Systems", 10, 1500.0)
    r2 = Repuesto("Célula de Energía", "Kuat Drive Yards", 5, 200.0)
    almacen_imperial.añadir_repuesto(r1)
    almacen_imperial.añadir_repuesto(r2)

    # 2. Instanciar Naves
    estacion = EstacionEspacial("STA-01", 9988, "Estrella de la Muerte", ["Placas de Titanio"], 50000, 10000, "Endor")
    caza = CazaEstelar("TIE-44", 1122, "TIE Advanced", ["Célula de Energía"], 1)

    # 3. Mostrar Información y Misiones
    estacion.mostrar_info()
    estacion.realizar_mision()
    caza.mostrar_info()
    
    # 4. Pruebas de Mantenimiento y Excepciones
    # Caso Exitoso
    solicitar_mantenimiento(caza, almacen_imperial, "Célula de Energía", 2)
    
    # Caso Error: Pieza no compatible
    solicitar_mantenimiento(estacion, almacen_imperial, "Célula de Energía", 1)
    
    # Caso Error: Stock insuficiente
    solicitar_mantenimiento(caza, almacen_imperial, "Célula de Energía", 10)