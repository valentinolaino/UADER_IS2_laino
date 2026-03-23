#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys
def verifyMaxMin(num): # Verifica que el numero este dentro del rango permitido
    if num < min or num > max:
        print(f"El numero ingresado debe estar entre {min} y {max}")
        sys.exit()

def determineOperation(strNum): # Determina que factoriales debe calcular
    if str(strNum)[0] == "-" : # Factoriales hasta strNum
        verifyMaxMin(int(str(strNum).strip("-")))
        for i in range(int(str(strNum).strip("-"))):
            print("Factorial ",i + 1,"! es ", factorial(i + 1))
        sys.exit()

    elif str(strNum)[-1] == "-": # Factoriales desde strNum
        newNum = int(str(strNum).strip("-"))
        verifyMaxMin(newNum)
        for i  in range(max + 1 - newNum ):
            print("Factorial ",i + newNum,"! es ", factorial(i + newNum))
        sys.exit()

    else: # Factoriales del minimo, maximo e ingresado
        num = int(strNum)
        verifyMaxMin(num)
        print("Factorial ",min,"! es ", factorial(min))
        print("Factorial ",num,"! es ", factorial(num))
        print("Factorial ",max,"! es ", factorial(max))

def factorial(num): 
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0: 
        return 1
        
    else: 
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 

num = None # Inicializa num
min = 0 # Minimo numero permitido
max = 60 # Maximo numero permitido

if len(sys.argv) == 1: # Verifica que exista el argumento
    while num is None or num == "": # Te permite ingresar un numero
        num = input(f"Ingrese un numero entre {min} y {max}: ")
else:
    num = sys.argv[1]

determineOperation(num); # Hace los factoriales necesarios
