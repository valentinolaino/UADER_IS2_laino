# ==========================================================
# Archivo: getJasonPoo.py
# Autores:
#       Laiño Valentino
#       Mout Santiago
#       Sandillú Axel
#
# copyright UADERFCyT-IS2©2026 todos los derechos reservados
# ==========================================================

"""Muestra los valores de los tokens solicitados en un archivo .json"""

import json
import sys
from abc import ABC, abstractmethod

VERSION = "1.1"


# =====================================================================
# LA CLASE ABSTRACTA
# =====================================================================
class ProcesadorJSON(ABC):
    """
    Interfaz que define cómo debe interactuar el cliente (main)
    con cualquier implementación del lector de JSON.
    """

    @abstractmethod
    def procesar(self, argv: list):
        """Metodo abstracto principal de ejecución

        Args:
            argv (list): Lista de argumentos
        """


# =====================================================================
# EL COMPONENTE ANTIGUO (Adaptado a la abstracción)
# =====================================================================
class LectorAntiguo(ProcesadorJSON):
    """
    Tu código original. Envolvemos tus funciones dentro de una clase
    para que cumpla con la interfaz ProcesadorJSON.
    """

    def getKeys(self, argv):
        """Obtiene los tokens que se dean bucar

        Args:
            argv (list): Lista de argumentos

        Returns:
            list: Lista de tokens a buscar
        """
        if len(argv) <= 2:
            return ["token1"]

        keys = []
        for i in range(2, len(sys.argv)):
            keys.append(sys.argv[i])
        return keys

    def getData(self, jsonfile):
        """Obteien los datos del json

        Args:
            jsonfile (str): Dirección del archivo

        Returns:
            dictionary: Objeto con los datos
        """
        with open(jsonfile, "r") as myfile:
            data = myfile.read()
        return json.loads(data)

    def printResults(self, data, keys):
        """Muestra los resultados por terminal

        Args:
            data (dictionary): Objeto con los datos
            keys (list): Lista con los tokens a buscar
        """
        for key in keys:
            print(str(data[key]))

    def procesar(self, argv: list):
        """El método de la interfaz coordina la lógica antigua

        Args:
            argv (list):Lista de argumentos
        """
        jsonkey = self.getKeys(argv)
        data = self.getData(argv[1])
        self.printResults(data, jsonkey)


# =====================================================================
# EL NUEVO COMPONENTE (Singleton y Mejorado)
# =====================================================================
class LectorNuevo(ProcesadorJSON):
    """
    El código refactorizado. Adaptado también para cumplir la interfaz.
    """

    _instancia = None

    def __new__(cls, *args, **kwargs):
        """Implementa el patron singleton"""
        if cls._instancia is None:
            cls._instancia = super(LectorNuevo, cls).__new__(cls)
            cls._instancia.datos_obtenidos = []
            cls._instancia.datos_json = {}
        return cls._instancia

    def cargar_json(self, jsonfile: str):
        """Abre el archivo .json

        Args:
            jsonfile (str): Dirección del archivo
        """
        try:
            with open(jsonfile, "r", encoding="utf-8") as myfile:
                self.datos_json = json.load(myfile)
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo '{jsonfile}'.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: El archivo '{jsonfile}' no es un JSON válido.")
            sys.exit(1)

    def obtener_claves(self, argv: list):
        """Obtiene el valor de las claves enviadas en los argumentos

        Args:
            argv (list): Lista de valores
        """
        claves = ["token1"] if len(argv) <= 2 else argv[2:]
        self.datos_obtenidos = []
        for clave in claves:
            valor = self.datos_json.get(clave, f"Clave '{clave}' no encontrada")
            self.datos_obtenidos.append(valor)

    def mostrar_resultados(self):
        """Muestra los valores en pantalla"""
        for valor in self.datos_obtenidos:
            print(str(valor))

    def procesar(self, argv: list):
        """Metodo de la interfaz que coordina la nueva logica

        Args:
            argv (list): lista de argumentos
        """
        self.cargar_json(argv[1])
        self.obtener_claves(argv)
        self.mostrar_resultados()


# =====================================================================
# EL CLIENTE Y EL SWITCH (Feature Toggle)
# =====================================================================
def main():
    """
    Punto de entrada. Aquí ocurre la magia de BbA mediante un Feature Toggle.
    """
    if len(sys.argv) < 2:
        print("Uso: python getJason.py <archivo.json> [clave1] [clave2] ...")
        return

    if "-v" in sys.argv:
        print(VERSION)
        return

    # ---------------------------------------------------------
    # FEATURE TOGGLE
    # Cambia esto a True para usar el nuevo código refactorizado.
    # Si falla, cámbialo a False y vuelve a tu código original instantáneamente.
    # ---------------------------------------------------------
    USAR_NUEVO_CODIGO = True

    if USAR_NUEVO_CODIGO:
        procesador = LectorNuevo()
    else:
        procesador = LectorAntiguo()

    # El cliente (main) no sabe si está usando el código viejo o el nuevo.
    # Solo sabe que la abstracción tiene un método `procesar()`.
    procesador.procesar(sys.argv)


if __name__ == "__main__":
    main()
