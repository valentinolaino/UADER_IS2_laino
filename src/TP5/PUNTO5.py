# Patrón Memento
# Permite guardar hasta 4 estados anteriores
# y recuperarlos en cualquier orden


class Memento:
    """Guarda el estado del objeto."""

    def __init__(self, estado):
        self.estado = estado

    def obtener_estado(self):
        return self.estado


class Originator:
    """Objeto cuyo estado cambia."""

    def __init__(self):
        self.estado = ""

    def set_estado(self, estado):
        print(f"Asignando estado: {estado}")
        self.estado = estado

    def get_estado(self):
        return self.estado

    def guardar(self):
        return Memento(self.estado)

    def restaurar(self, memento):
        self.estado = memento.obtener_estado()


class Caretaker:
    """Administra los estados guardados."""

    def __init__(self, originator):
        self.originator = originator
        self.historial = []

    def save(self):
        # Guarda el estado actual
        self.historial.insert(0, self.originator.guardar())

        # Mantener máximo 4 estados
        if len(self.historial) > 4:
            self.historial.pop()

    def undo(self, posicion=0):
        """
        posicion:
        0 -> estado inmediatamente anterior
        1 -> un estado más atrás
        2 -> dos estados más atrás
        3 -> tres estados más atrás
        """

        if posicion < len(self.historial):
            memento = self.historial[posicion]
            self.originator.restaurar(memento)

            print(
                f"Estado recuperado ({posicion}):",
                self.originator.get_estado()
            )
        else:
            print("No existe un estado guardado en esa posición.")


# Programa principal
if __name__ == "__main__":

    originator = Originator()
    caretaker = Caretaker(originator)

    # Estados
    originator.set_estado("Estado 1")
    caretaker.save()

    originator.set_estado("Estado 2")
    caretaker.save()

    originator.set_estado("Estado 3")
    caretaker.save()

    originator.set_estado("Estado 4")
    caretaker.save()

    originator.set_estado("Estado 5")
    caretaker.save()

    print("\nEstado actual:", originator.get_estado())

    print("\nRecuperar estado inmediato anterior")
    caretaker.undo(0)

    print("\nRecuperar estado más antiguo")
    caretaker.undo(3)

    print("\nRecuperar segundo estado anterior")
    caretaker.undo(1)