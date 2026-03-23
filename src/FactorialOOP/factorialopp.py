#!/usr/bin/python
import sys

class Factorial:
    def __init__(self):
        """Constructor de la clase Factorial."""
        pass

    def _calcular(self, n):
        """Método privado para el cálculo matemático del factorial."""
        if n < 0:
            return 0
        if n == 0:
            return 1
        fact = 1
        for i in range(1, n + 1):
            fact *= i
        return fact

    def run(self, min_val, max_val):
        """
        Calcula y muestra el factorial para cada número 
        en el rango inclusivo entre min_val y max_val.
        """
        for i in range(min_val, max_val + 1):
            resultado = self._calcular(i)
            print(f"Factorial {i}! es {resultado}")

def verifyMaxMin(num, min, max): # Verifica que el numero este dentro del rango permitido
    if num < min or num > max:
        print(f"El numero ingresado debe estar entre {min} y {max}")
        sys.exit()

def determineOperation(strNum, fact, min, max): # Determina que factoriales debe calcular
    if str(strNum)[0] == "-" : # Factoriales hasta strNum
        verifyMaxMin(int(str(strNum).strip("-")), min, max)
        fact.run(min, int(str(strNum).strip("-")))

    elif str(strNum)[-1] == "-": # Factoriales desde strNum
        newNum = int(str(strNum).strip("-"))
        verifyMaxMin(newNum, min, max)
        fact.run(newNum, max)

    else: # Factoriales del minimo, maximo e ingresado
        num = int(strNum)
        verifyMaxMin(num, min, max)
        fact.run(min, min)
        fact.run(num, num)
        fact.run(max, max)

# Bloque de ejecución principal
if __name__ == "__main__":
    # Definición de límites por defecto o vía argumentos
    min = 1
    max = 60
    arg = None

    try:
        if len(sys.argv) == 1: # Verifica que exista el argumento
            while arg is None or arg == "": # Te permite ingresar un numero
                arg = input(f"Ingrese un numero entre {min} y {max}: ")
        else:
            arg = sys.argv[1]
        
        # Instanciación y ejecución de la lógica OOP
        app = Factorial()
        determineOperation(arg, app, min, max)
        
    except ValueError:
        print("Error: Por favor ingrese números enteros válidos.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")