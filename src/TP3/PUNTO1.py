# Provea una clase que dado un número entero cualquiera retorne el factorial del mismo, 
# debe asegurarse que todas las clases que lo invoquen utilicen la misma instancia de clase.
from threading import Lock


class Factorial:
    """
    Singleton para calcular el factorial de un número.
    """

    _instancia = None
    _lock = Lock() 

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:  # doble verificación
                    cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self, archivo_config: str = None):
        """
        Inicializa...
        """
        if not hasattr(self, "_inicializado"):
            self._config = {}
            if archivo_config:
                self._cargar_desde_archivo(archivo_config)
            self._inicializado = True



    def calculo_factorial(self, n):
        if n == 0:
            return 1
        else:
            return n * self.calculo_factorial(n - 1)



