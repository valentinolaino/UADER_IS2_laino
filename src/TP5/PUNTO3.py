class Subject:
    def __init__(self):
        self._observers = []

    def notify(self, id_emitido):
        for observer in self._observers:
            observer.update(id_emitido)

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

class Emisor(Subject):
    def emitir(self, id_emitido):
        print(f"\n--- Emisor emitiendo ID: {id_emitido} ---")
        self.notify(id_emitido)

class Receptor:
    def __init__(self, id_propio):
        self.id_propio = id_propio

    def update(self, id_recibido):
        if id_recibido == self.id_propio:
            print(f"Receptor {self.id_propio}: Coincidencia encontrada!")

# Implementación solicitada
if __name__ == "__main__":
    # 1. Creamos el sujeto (Emisor)
    emisor = Emisor()

    # 2. Implementamos 4 clases con IDs específicos
    r1 = Receptor("ABCD")
    r2 = Receptor("1234")
    r3 = Receptor("WXYZ")
    r4 = Receptor("5678")

    # 3. Suscribimos las clases al emisor
    emisor.attach(r1)
    emisor.attach(r2)
    emisor.attach(r3)
    emisor.attach(r4)

    # 4. Emitimos 8 IDs (4 de ellos coinciden con los receptores)
    ids_a_emitir = ["ABCD", "0000", "1234", "9999", "WXYZ", "AAAA", "5678", "BBBB"]

    for id_emitido in ids_a_emitir:
        emisor.emitir(id_emitido)