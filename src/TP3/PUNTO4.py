from abc import ABC, abstractmethod


# Producto abstracto
class Factura(ABC):

    def __init__(self, importe):
        self.importe = importe

    @abstractmethod
    def mostrar_factura(self):
        pass


# Productos concretos
class FacturaIVAResponsable(Factura):

    def mostrar_factura(self):
        print("Factura - Cliente IVA Responsable")
        print("Total a pagar: $", self.importe)


class FacturaIVANoInscripto(Factura):

    def mostrar_factura(self):
        print("Factura - Cliente IVA No Inscripto")
        print("Total a pagar: $", self.importe)


class FacturaIVAExento(Factura):

    def mostrar_factura(self):
        print("Factura - Cliente IVA Exento")
        print("Total a pagar: $", self.importe)


# Factory
class FacturaFactory:

    @staticmethod
    def crear_factura(condicion, importe):
        condicion = condicion.lower()
        if condicion == "responsable":
            return FacturaIVAResponsable(importe)
        elif condicion == "no inscripto":
            return FacturaIVANoInscripto(importe)
        elif condicion == "exento":
            return FacturaIVAExento(importe)
        else:
            raise ValueError("Condición impositiva no válida.")


# Programa principal
if __name__ == "__main__":
    importe = float(input("Ingrese el importe total: $"))
    condicion = input(
        "Ingrese condición impositiva (responsable / no inscripto / exento): "
    )

    factura = FacturaFactory.crear_factura(condicion, importe)
    factura.mostrar_factura()