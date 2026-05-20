import os

#*--------------------------------------------------------------------
#* Ejemplo de design pattern de tipo state
#*--------------------------------------------------------------------

"""State class: Base State class"""
class State:

    def scan(self):

        self.pos += 1

        # Cantidad total = estaciones normales + memorias
        total = len(self.stations) + len(self.memories)

        if self.pos >= total:
            self.pos = 0

        # Si está dentro de las estaciones normales
        if self.pos < len(self.stations):
            station = self.stations[self.pos]
            print("Sintonizando... Estación {} {}".format(station, self.name))

        # Si está dentro de las memorias
        else:
            mem_index = self.pos - len(self.stations)
            mem_name, mem_freq = self.memories[mem_index]

            print(
                "Sintonizando memoria {} -> {} {}".format(
                    mem_name,
                    mem_freq,
                    self.name
                )
            )

#*------- Implementa como barrer las estaciones de AM
class AmState(State):

    def __init__(self, radio):

        self.radio = radio

        # Estaciones normales
        self.stations = ["1250", "1380", "1510"]

        # Memorias AM
        self.memories = [
            ("M1", "1100"),
            ("M2", "1260"),
            ("M3", "1450"),
            ("M4", "1600")
        ]

        self.pos = -1
        self.name = "AM"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate

#*------- Implementa como barrer las estaciones de FM
class FmState(State):

    def __init__(self, radio):

        self.radio = radio

        # Estaciones normales
        self.stations = ["81.3", "89.1", "103.9"]

        # Memorias FM
        self.memories = [
            ("M1", "88.5"),
            ("M2", "92.7"),
            ("M3", "98.3"),
            ("M4", "104.1")
        ]

        self.pos = -1
        self.name = "FM"

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.state = self.radio.amstate

#*--------- Construye la radio con todas sus formas de sintonía
class Radio:

    def __init__(self):

        self.fmstate = FmState(self)
        self.amstate = AmState(self)

        #*--- Inicialmente en FM
        self.state = self.fmstate

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()

#*---------------------

if __name__ == "__main__":

    os.system("clear")

    print("\nCrea un objeto radio y almacena las siguientes acciones")

    radio = Radio()

    # Barridos FM + cambio + barridos AM
    actions = (
        [radio.scan] * 7 +
        [radio.toggle_amfm] +
        [radio.scan] * 7
    )

    #*---- Recorre las acciones ejecutando la acción
    print("Recorre las acciones ejecutando la acción, el objeto cambia la interfaz según el estado")

    for action in actions:
        action()