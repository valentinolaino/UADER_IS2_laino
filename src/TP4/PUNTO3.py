from abc import ABC, abstractmethod

# Componente base
class Componente(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def mostrar(self, nivel=0):
        pass

class Pieza(Componente):
    def mostrar(self, nivel=0):
        print("  " * nivel + f"- Pieza: {self.nombre}")

# Clase Composite
class Conjunto(Componente):
    def __init__(self, nombre: str):
        super().__init__(nombre)
        self.hijos = []

    def agregar(self, componente: Componente):
        self.hijos.append(componente)

    def remover(self, componente: Componente):
        self.hijos.remove(componente)

    def mostrar(self, nivel=0):
        print("  " * nivel + f"+ Conjunto: {self.nombre}")
        for hijo in self.hijos:
            hijo.mostrar(nivel + 1)

if __name__ == "__main__":
    producto = Conjunto("Producto Principal")

    # Crear 3 subconjuntos con 4 piezas cada uno
    for i in range(1, 4):
        subconjunto = Conjunto(f"Subconjunto {i}")
        for j in range(1, 5):
            subconjunto.agregar(Pieza(f"Pieza {i}.{j}"))
        producto.agregar(subconjunto)

    print("=== Estructura inicial ===")
    producto.mostrar()

    # Añadir subconjunto opcional
    subconjunto_opcional = Conjunto("Subconjunto Opcional")
    for j in range(1, 5):
        subconjunto_opcional.agregar(Pieza(f"Pieza O.{j}"))

    producto.agregar(subconjunto_opcional)

    print("\n=== Con subconjunto opcional ===")
    producto.mostrar()