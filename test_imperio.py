import pytest
from Pedro_Gómez_Rocío_Quesada_Imperio import Almacen, Repuesto, CazaEstelar, EstacionEspacial, solicitar_mantenimiento

# Test de lógica de negocio: Stock insuficiente
def test_stock_insuficiente():
    almacen = Almacen("Test", "Endor")
    repuesto = Repuesto("Tornillo", "Empresa X", 5, 10.0)
    almacen.añadir_repuesto(repuesto)
    
    with pytest.raises(Exception) as excinfo:
        almacen.reducir_stock("Tornillo", 10)
    assert "Stock insuficiente" in str(excinfo.value)

# Test de lógica de negocio: Pieza no existente
def test_pieza_no_existe():
    almacen = Almacen("Test", "Endor")
    with pytest.raises(Exception) as excinfo:
        almacen.reducir_stock("Inexistente", 1)
    assert "no existe" in str(excinfo.value)

# Test de atributo privado y validación
def test_cantidad_negativa_repuesto():
    r = Repuesto("Placa", "Prov", 10, 50)
    with pytest.raises(ValueError):
        r.set_cantidad(-5)

# Test de compatibilidad de catálogo
def test_compatibilidad_catalogo():
    almacen = Almacen("Test", "Endor")
    r = Repuesto("Motor TIE", "Sienar", 10, 500)
    almacen.añadir_repuesto(r)
    caza = CazaEstelar("T-1", 123, "Caza", ["Laser"], 1) # No tiene 'Motor TIE' en catálogo
    
    # Verificamos que no se permite el mantenimiento por catálogo
    # En tu función 'solicitar_mantenimiento' imprimes el error, podrías modificarla 
    # para que lance la excepción si quieres testearla con pytest.raises