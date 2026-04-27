from threading import Lock


class Factorial:
    _instancia = None
    _lock = Lock()

    def __new__(cls):
        # Verifica si ya existe una instancia
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:
                    cls._instancia = super(Factorial, cls).__new__(cls)
        return cls._instancia

    def factorial(self, n):
        if n < 0:
            raise ValueError("El factorial no está definido para números negativos.")
        
        resultado = 1
        for i in range(1, n + 1):
            resultado *= i
        return resultado
    
    def __str__(self):
        return hex(id(self))


# Programa principal
if __name__ == "__main__":
    # Se crean dos variables, pero apuntan a la misma instancia
    obj1 = Factorial()
    obj2 = Factorial()

    numero = int(input("Ingrese un número entero: "))

    print("Factorial:", obj1.factorial(numero))

    # Verificación del patrón Singleton
    if obj1 is obj2:
        print("Ambos objetos comparten la misma instancia.")
    else:
        print("Son instancias diferentes.")

    print(obj1)
    print(obj2)