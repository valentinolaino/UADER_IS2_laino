from __future__ import annotations
from abc import ABC, abstractmethod


# Producto
class Avion:
    """Objeto complejo que se construye paso a paso."""

    def __init__(self):
        self.componentes = []

    def agregar(self, componente):
        self.componentes.append(componente)

    def mostrar(self):
        return "Avión con:\n - " + "\n - ".join(self.componentes)


# Builder abstracto
class BuilderAvion(ABC):

    def __init__(self):
        self.reset()

    def reset(self):
        self._producto = Avion()

    def obtener_resultado(self):
        producto = self._producto
        self.reset()
        return producto

    @abstractmethod
    def construir_body(self):
        pass

    @abstractmethod
    def construir_turbinas(self):
        pass

    @abstractmethod
    def construir_alas(self):
        pass

    @abstractmethod
    def construir_tren_aterrizaje(self):
        pass


# Builder concreto 1
class BuilderAvionComercial(BuilderAvion):

    def construir_body(self):
        self._producto.agregar("Body comercial de pasajeros")

    def construir_turbinas(self):
        self._producto.agregar("2 turbinas de gran potencia")

    def construir_alas(self):
        self._producto.agregar("2 alas largas comerciales")

    def construir_tren_aterrizaje(self):
        self._producto.agregar("Tren de aterrizaje reforzado")


# Builder concreto 2
class BuilderAvionPrivado(BuilderAvion):

    def construir_body(self):
        self._producto.agregar("Body ejecutivo pequeño")

    def construir_turbinas(self):
        self._producto.agregar("2 turbinas medianas")

    def construir_alas(self):
        self._producto.agregar("2 alas aerodinámicas")

    def construir_tren_aterrizaje(self):
        self._producto.agregar("Tren de aterrizaje liviano")


# Director
class Director:

    def __init__(self, builder):
        self._builder = builder

    def construir_avion_completo(self):
        self._builder.construir_body()
        self._builder.construir_turbinas()
        self._builder.construir_alas()
        self._builder.construir_tren_aterrizaje()


# Programa principal
def main():

    # Avión comercial
    builder1 = BuilderAvionComercial()
    director = Director(builder1)

    director.construir_avion_completo()
    avion1 = builder1.obtener_resultado()

    print("Avión Comercial")
    print(avion1.mostrar())
    print()

    # Avión privado
    builder2 = BuilderAvionPrivado()
    director = Director(builder2)

    director.construir_avion_completo()
    avion2 = builder2.obtener_resultado()

    print("Avión Privado")
    print(avion2.mostrar())


if __name__ == "__main__":
    main()