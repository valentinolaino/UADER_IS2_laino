from abc import ABC, abstractmethod


# Producto abstracto
class Hamburguesa(ABC):

    @abstractmethod
    def entregar(self):
        pass


# Productos concretos
class Mostrador(Hamburguesa):

    def entregar(self):
        print("La hamburguesa será entregada en mostrador.")


class RetiroCliente(Hamburguesa):

    def entregar(self):
        print("La hamburguesa será retirada por el cliente.")


class Delivery(Hamburguesa):

    def entregar(self):
        print("La hamburguesa será enviada por delivery.")


# Factory
class HamburguesaFactory:

    @staticmethod
    def crear_hamburguesa(tipo_entrega):
        tipo_entrega = tipo_entrega.lower()
        if tipo_entrega == "mostrador":
            return Mostrador()
        elif tipo_entrega == "retiro":
            return RetiroCliente()
        elif tipo_entrega == "delivery":
            return Delivery()
        else:
            raise ValueError("Tipo de entrega no válido.")


# Programa principal
if __name__ == "__main__":
    opcion = input(
        "Ingrese tipo de entrega (mostrador / retiro / delivery): "
    )

    hamburguesa = HamburguesaFactory.crear_hamburguesa(opcion)
    hamburguesa.entregar()