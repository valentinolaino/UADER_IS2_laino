#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys
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

num = None
min = 4
max = 8

if len(sys.argv) == 1:
    while num is None or num == "":
        num = input(f"Ingrese un numero entre {min} y {max}: ")
    num = int(num)
else:
    num = int(sys.argv[1])

if num < min or num > max:
    print(f"El numero ingresado debe estar entre {min} y {max}")
    sys.exit()

print("Factorial (valor minimo)",min,"! es ", factorial(min))
print("Factorial (valor ingresado)",num,"! es ", factorial(num))
print("Factorial (valor maximo)",max,"! es ", factorial(max))


