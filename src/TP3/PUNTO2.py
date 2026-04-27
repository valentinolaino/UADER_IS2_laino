from threading import Lock


class Impuesto:
    _instancia = None
    _lock = Lock()

    def __new__(cls):
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:
                    cls._instancia = super(Impuesto, cls).__new__(cls)
        return cls._instancia

    def __str__(self):
        # Devuelve la posición en memoria para comprobar Singleton
        return hex(id(self))

    def calcular_impuestos(self, base_imponible):
        if base_imponible < 0:
            raise ValueError("La base imponible no puede ser negativa.")

        total_impuestos = base_imponible * 0.21 + base_imponible * 0.05 + base_imponible * 0.012
        return total_impuestos


# Programa principal
if __name__ == "__main__":
    obj1 = Impuesto()
    obj2 = Impuesto()

    base = float(input("Ingrese el importe base imponible: "))

    print("Total de impuestos:", obj1.calcular_impuestos(base))

    # Verificación del patrón Singleton
    print(obj1)
    print(obj2)