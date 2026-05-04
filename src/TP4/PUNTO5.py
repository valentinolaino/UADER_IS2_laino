# Flyweight (estado compartido)
class TipoMarcador:
    def __init__(self, tipo: str, icono: str):
        self.tipo = tipo
        self.icono = icono

    def mostrar(self, lat: float, lon: float, nombre: str):
        print(f"[{self.icono}] {self.tipo} - {nombre} "
              f"en ({lat}, {lon})")

# Flyweight Factory
class FabricaMarcadores:
    _tipos = {}

    @classmethod
    def obtener_tipo(cls, tipo: str, icono: str):
        clave = (tipo, icono)

        if clave not in cls._tipos:
            cls._tipos[clave] = TipoMarcador(tipo, icono)

        return cls._tipos[clave]

    @classmethod
    def total_tipos(cls):
        return len(cls._tipos)

class Marcador:
    def __init__(self, lat: float, lon: float, nombre: str, tipo: TipoMarcador):
        self.lat = lat
        self.lon = lon
        self.nombre = nombre
        self.tipo = tipo

    def mostrar(self):
        self.tipo.mostrar(self.lat, self.lon, self.nombre)

if __name__ == "__main__":
    marcadores = []

    # Crear muchos marcadores reutilizando tipos
    marcadores.append(Marcador(-32.48, -58.23, "Hospital Urquiza",
        FabricaMarcadores.obtener_tipo("Hospital", "H")))

    marcadores.append(Marcador(-32.49, -58.24, "Clínica Central",
        FabricaMarcadores.obtener_tipo("Hospital", "H")))

    marcadores.append(Marcador(-32.50, -58.25, "Parrilla Don José",
        FabricaMarcadores.obtener_tipo("Restaurante", "R")))

    marcadores.append(Marcador(-32.51, -58.26, "Pizzería Roma",
        FabricaMarcadores.obtener_tipo("Restaurante", "R")))

    for m in marcadores:
        m.mostrar()

    print("\nTipos de marcador creados (Flyweight):",
          FabricaMarcadores.total_tipos())
    