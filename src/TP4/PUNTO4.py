from abc import ABC, abstractmethod

class Numero(ABC):
    @abstractmethod
    def valor(self) -> float:
        pass

class NumeroBase(Numero):
    def __init__(self, valor: float):
        self._valor = valor

    def valor(self) -> float:
        return self._valor

# Decorator base
class OperacionDecorator(Numero):
    def __init__(self, numero: Numero):
        self._numero = numero

# Decoradores concretos
class Sumar2(OperacionDecorator):
    def valor(self) -> float:
        return self._numero.valor() + 2

class MultiplicarPor2(OperacionDecorator):
    def valor(self) -> float:
        return self._numero.valor() * 2

class DividirPor3(OperacionDecorator):
    def valor(self) -> float:
        return self._numero.valor() / 3

if __name__ == "__main__":
    base = NumeroBase(6)

    print("Valor original:", base.valor())

    # Aplicación de decoradores en forma anidada
    operado = DividirPor3(
                MultiplicarPor2(
                    Sumar2(base)
                )
             )

    print("\nValor con operaciones anidadas ((6 + 2) * 2) / 3:", operado.valor())
