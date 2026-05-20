from abc import ABC, abstractmethod


# Clase Handler abstracta
class Manejador(ABC):

    def __init__(self):
        self.siguiente = None

    def set_siguiente(self, siguiente):
        self.siguiente = siguiente

    @abstractmethod
    def manejar(self, numero):
        pass


# Clase que consume números primos
class ManejadorPrimos(Manejador):

    def es_primo(self, numero):
        if numero < 2:
            return False

        for i in range(2, int(numero ** 0.5) + 1):
            if numero % i == 0:
                return False

        return True

    def manejar(self, numero):
        if self.es_primo(numero):
            print(f"{numero} consumido por ManejadorPrimos")
        elif self.siguiente:
            self.siguiente.manejar(numero)
        else:
            print(f"{numero} no consumido")


# Clase que consume números pares
class ManejadorPares(Manejador):

    def manejar(self, numero):
        if numero % 2 == 0:
            print(f"{numero} consumido por ManejadorPares")
        elif self.siguiente:
            self.siguiente.manejar(numero)
        else:
            print(f"{numero} no consumido")


# Programa principal
if __name__ == "__main__":

    # Crear manejadores
    manejador_primos = ManejadorPrimos()
    manejador_pares = ManejadorPares()

    # Construir cadena de responsabilidad
    manejador_primos.set_siguiente(manejador_pares)

    # Procesar números del 1 al 100
    for numero in range(1, 101):
        manejador_primos.manejar(numero)