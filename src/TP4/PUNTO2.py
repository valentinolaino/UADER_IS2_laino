from abc import ABC, abstractmethod

# Clase abstracta de bridge
class TrenLaminador(ABC):
    @abstractmethod
    def producir(self, espesor: float, ancho: float):
        pass

# Implementaciones concretas
class Tren5m(TrenLaminador):
    def producir(self, espesor: float, ancho: float):
        largo = 5
        return f"Lámina producida: {espesor}\" x {ancho}m x {largo}m (Tren 5m)"

class Tren10m(TrenLaminador):
    def producir(self, espesor: float, ancho: float):
        largo = 10
        return f"Lámina producida: {espesor}\" x {ancho}m x {largo}m (Tren 10m)"

# Abstracción
class Lamina:
    def __init__(self, espesor: float, ancho: float, tren: TrenLaminador):
        self.espesor = espesor
        self.ancho = ancho
        self.tren = tren  # Bridge

    def producir(self):
        return self.tren.producir(self.espesor, self.ancho)

    def set_tren(self, tren: TrenLaminador):
        self.tren = tren

# Ejemplo de uso
if __name__ == "__main__":
    tren5 = Tren5m()
    tren10 = Tren10m()

    lamina = Lamina(0.5, 1.5, tren5)
    print(lamina.producir())

    lamina.set_tren(tren10)
    print(lamina.producir())
