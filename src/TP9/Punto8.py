#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#* PNR_sistemis
#* Programa para procesar modelos dinámicos basado en el modelo de Putman-Norden_Rayleigh
#*
#* UADER - FCyT
#* Ingeniería de Software II
#*
#* Dr. Pedro E. Colla
#* copyright (c) 2023,2024
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
import pandas as pd
import numpy as np
import sys
import os
import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from scipy.optimize import root_scalar
from scipy.integrate import quad
from scipy.optimize import root_scalar
import argparse

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*                             Librerias y funciones de soporte
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*--- Estima el esfuero consumido al momento de la liberación del proyecto, el remanente será un residual para soporte post-instalación
def E_proyecto(K,a,gamma):  
   tf=np.sqrt(-np.log(1-gamma)/a)
   Ef=gamma*K
   return tf,Ef

#*--- Calcula el esfuerzo acumulado en función del tiempo E(t)
def E_acum(K,a,t):
    return K*(1-np.exp(-a*(t**2)))

#*--- Calcula el esfuerzo instantaneo o staff p(t) en un momento t
def E(t, K, a):
    """Calcula el valor de la función E(t)"""
    return 2 * K * a * t * np.exp(-a * t**2)

#*--- Encuentra un valor próximo a cero en la asíntota final
#*--- Encuentra un valor próximo a cero en la asíntota final
def find_near_zero(K, a, tolerance):
    def equation(t):
        return E(t, K, a) - tolerance

    # Primero encontramos dónde está el máximo de la curva (tmax)
    tmax = 1 / np.sqrt(2 * a)
    
    # Buscamos el cero únicamente en la cola descendente [tmax, 100]
    try:
        # Verificamos si hay cambio de signo en la cola descendente
        if equation(tmax) * equation(100) <= 0:
            result = root_scalar(equation, bracket=[tmax, 100], method='brentq')
            return result.root if result.converged else None
        else:
            # Si a t=100 todavía no bajó o ya era menor desde tmax
            return None
    except Exception:
        return None


#*--- Encuentra el valor máximo de la función p(t)
def find_maximum(K, a):

    # Derivada de la función p(t) con respecto a t
    def negative_E(t):
        return -E(t, K, a)
    
    # Encuentra el máximo usando el método de minimización de la función negativa
    result = minimize_scalar(negative_E, bounds=(0, 100), method='bounded')
    t_max = result.x
    E_max = E(t_max, K, a)
    
    return t_max, E_max

#*--- Calcula un valor corregido de p(t) restando el staff asignado para poder calcular los ceros de la función p(t)-pr 
def y(t, K, a, z):
    """Calcula el valor de la función y(t)."""
    return 2 * K * a * t * np.exp(-a * t**2) - z

#*--- Encuentra ceros en un intervalo dado
def find_zeros(K, a, z):
    zeros = []
    intervals = np.linspace(0, 100, 500)  # Ajusta los límites según el contexto

    for i in range(len(intervals) - 1):
        t1, t2 = intervals[i], intervals[i + 1]
        if y(t1, K, a, z) * y(t2, K, a, z) < 0:  # Verifica cambio de signo
            zero = root_scalar(y, args=(K, a, z), bracket=[t1, t2], method='bisect')
            if zero.converged:
                zeros.append(zero.root)

    return sorted(zeros)

#*--- Calcula el área bajo la curva (integral definida) en el intervalo [t1,t2]
def area_under_curve(t1, t2, K, a, z):
    integral, _ = quad(lambda t: max(y(t, K, a, z), 0), t1, t2)
    return integral

#*--- encuentra ceros de la función
def encuentra_restriccion(K, a, pr):
    ceros = find_zeros(K, a, pr)

    if len(ceros) >= 2:
        return ceros[0], ceros[-1]
    else:
        print(f"No hay restricción: el staff máximo pmax no supera pr = {pr:.1f}")
        return None, None

#def encuentra_restriccion(K,a,pr):
#    ceros = find_zeros(K, a, pr)

# Calcula el área bajo la curva para y(t) >= 0
#    if len(ceros) >= 2:
#       t1, t2 = ceros[0], ceros[-1]  # Considera los ceros extremos
#       E2 = area_under_curve(t1, t2, K, a, pr)
#       #print(f"El Área bajo la curva donde p(t)-pr >= 0: E2={E2:.2f} PM quedará sin satisfacción")
#    else:
#       print("No se encontraron suficientes ceros para calcular el área.")
#       sys.exit()
#   return ceros[0],ceros[-1]

#*--- Calcula intervalo del proyecto que opera bajo restricción de recursos
def calcula_restriccion(K,a,pr,t1,t2):
    Er=E_acum(K,a,t2)-E_acum(K,a,t1)
    E3=pr*(t2-t1)
    E2=Er-E3
    return Er,E2,E3

#*--- Calcula el tiempo que debe asignar un staff fijo pr para acumular un esfuerzo E
def esfuerzo_fijo(E,pr):
    return E/pr

#*--- Calcula el valor medio de la función en el intervalo [0,tx]
def average_value(K, a, tx):
    integral, _ = quad(E, 0, tx, args=(K, a))
    average = integral / tx
    return average

#*=*=*=*=*=*=*=* Funciones auxiliares de graficación

#*--- Calcula el esfuerzo instantaneo sobre un vector numpy t
def esfuerzo_instantaneo(t, a):
    return 2 * K * a * t * np.exp(-a * t**2)

#*--- Calcula el esfuerzo constante sobre un vector numpy t
def esfuerzo_constante(t,pr):
    l=len(t)
    return np.full(l,pr) 

#*--- Calcula el esfuerzo acumulado sobre un vector numpy t
def esfuerzo_acumulado(t,a):
    return K*(1-np.exp(-a * t**2))
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*                      Fin de librerias y funciones de soporte
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

#*--- Asume datos default para el proyecto testigo y la restricción de recursos

Kp=0 #CAMBIO: Porque el esfuerzo del proyecto ahora debería venir del argumento -k
pr=15
version="1.0"
name="noname"
rr=False

os.system('cls' if os.name == 'nt' else 'clear')

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-v", "--version",required=False,help="version",action="store_true")
ap.add_argument("-k", "--esfuerzo", required=False,help="Esfuerzo total")
ap.add_argument("-p", "--pmax", required=False,help="Staff máximo")
ap.add_argument("-n", "--name", required=False,help="Nombre proyecto")
ap.add_argument("-r", "--restriccion", required=False,help="Calcula corrección por restricción",action="store_true")

args = vars(ap.parse_args())

if args['name'] == False:
   name='NoName'

if args['esfuerzo'] is not None: #CAMBIO: args['esfuerzo'] puede ser None si no pasás -k
    Kp=float(args['esfuerzo'])

if args['restriccion'] == True:
   if args['pmax'] != 0:
      pr=float(args['pmax'])
   rr=True
   print("Calcula proyecto con restricción de recursos pmax=%.1f" % (pr))

if args['version'] == True:
   print("Programa %s version %s" % (sys.argv[0],version))
   sys.exit(0)

name=args['name']

#*--- Define el dataset histórico de referencia, obtiene el K del mismo y calibra
#*--- usa un método de "best-fit" para la calibración
#*--- obtiene una estimación del valor "a" (a_estimada)

t_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])        # Tiempo en meses
E_data = np.array([8, 21, 25, 30, 25, 24, 17, 15, 11, 6])  # Esfuerzo instantáneo en persona-mes
df = pd.DataFrame(E_data,t_data)
print(df)
K = np.sum(E_data)
print("El esfuerzo total del proyecto es K=%d PM" % (K))
popt, pcov = curve_fit(esfuerzo_instantaneo, t_data, E_data, p0=[0.1])
a_estimada = popt[0]
print(f"Parámetro a estimado: {a_estimada:.3f}")

#CAMBIO: 8.c - Cuadruplicar el parámetro a
a_cuadruple = 4 * a_estimada
print(f"Parámetro a cuadruplicado: {a_cuadruple:.3f}")

#*--- Grafica el dataset histórico de calibración y el modelo de best-fit encontrado

t_fit = np.linspace(min(t_data), max(t_data), 100)
E_fit = esfuerzo_instantaneo(t_fit, a_estimada)
plt.scatter(t_data, E_data, label='Datos observados')
plt.plot(t_fit, E_fit, label='E(t) modelado', color='red')
plt.xlabel('Tiempo (meses)')
plt.ylabel('Esfuerzo instantáneo (personas)')
plt.legend()
plt.show()

#*--- Define un proyecto testigo

K=Kp    #Esfuerzo total expresado en PM

#*--- Grafica el proyecto testigo comparado con el modelo de best-fit y el dataset histórico

t_fit = np.linspace(min(t_data), max(t_data), 100)
O_fit = esfuerzo_instantaneo(t_fit, a_estimada)
plt.plot(t_fit, O_fit, label='Nuevo proyecto', color='blue')
plt.plot(t_fit, E_fit, label='Modelo', color='red')
plt.scatter(t_data, E_data, label='Datos observados', color='blue')
plt.xlabel('Tiempo (meses)')
plt.ylabel('Esfuerzo instantáneo (persona-mes)')
plt.legend()
plt.show()


#*--- Grafica el esfuerzo acumulado para el proyecto testigo

O_fit = esfuerzo_acumulado(t_fit, a_estimada)
t_fit = np.linspace(min(t_data), max(t_data), 100)

plt.plot(t_fit, O_fit, label='Esfuerzo E(t)', color='blue')
plt.xlabel('Tiempo (meses)')
plt.ylabel('Esfuerzo acumulado (persona-mes)')
plt.legend()
plt.show()


#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*       Calcula el proyecto testigo asumiendo que no hay restricciones de staff
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

#*--- Estima los parámetros del proyecto
#*--- Tiempo de entrega (tf), asumido en la condición E(t)=0.9K

gamma=0.9
tf,Ef = E_proyecto (K,a_estimada,gamma)

print("Solución de planeamiento sin restricciones proyecto %s" % (name))
print("\t")
print("\tEsfuerzo nominal            (K)=%.1f PM" % (K))
print("\tTiempo para entrega        (tf)=%.1f meses" % (tf))
print("\tEsfuerzo acumulado@tf   (E(tf))=%.1f PM" % (Ef)) 

#*--- Estima el tiempo en el que ocurre el máximo staff y el valor de éste

# Encuentra el tiempo t y el valor máximo de E(t)
tmax, pmax = find_maximum(K, a_estimada)

print("\t ")
print("\tMaxima alocación       (tmax)=%.1f meses" % (tmax))
print("\tMaxima staff asignado  (pmax)=%.1f personas" % (pmax))

#*--- Encuentra pasada la entrega el esfuerzo residual y el tiempo en obtenerlo
#*--- aproxima un valor cercano a cero pues la función no se hace cero nunca 
t_near_zero = find_near_zero(K, a_estimada, 1)

if t_near_zero is None:
    # Si la cola cae muy rápido, asignamos tf como límite y el esfuerzo residual queda en 0
    t_near_zero = tf
    Enz = 0.0
else:
    Enz = E_acum(K, a_estimada, t_near_zero) - E_acum(K, a_estimada, tf)

print("\t")
print("\tTiempo residual         (tnz)=%.1f meses" % (t_near_zero))
print("\tEsfuerzo residual       (Enz)=%.1f PM" % (Enz))

#t_near_zero = find_near_zero(K, a_estimada,1)
#if t_near_zero is None:
#    print("No se encontró un valor de t donde y(t) sea cercano a cero.")
#    sys.exit()
#Enz=E_acum(K,a_estimada,t_near_zero)-E_acum(K,a_estimada,tf)

print("\t")
print("\tTiempo residual         (tnz)=%.1f meses" % (t_near_zero))
print("\tEsfuerzo residual       (Enz)=%.1f PM" % (Enz))

#*--- Calcula el valor medio del staff requerido
#*--- Calcula cual es el staff requerido al momento de la liberación

# Calcula el valor medio de la función en el intervalo [0, tx]
pmed = average_value(K, a_estimada, tf)
prel = E(tf,K,a_estimada)
print("\t")
print("\tStaff promedio [0,%.1f]   (pmed)=%.1f personas" % (tf,pmed))
print("\tStaff al release         (prel)=%.1f personas" % (prel))

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*       Calcula el proyecto testigo asumiendo que hay restricciones de staff (p(t) <= pr)
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

if rr == False:
    print("\t")
    print("Cálculo con restricción de recursos no fue requerido")
else:
    print("\t")
    print("Se calcula con restricción de recursos requeridos pr=%.1f" % (pr))

    t1, t2 = encuentra_restriccion(K, a_estimada, pr)

    if t1 is not None and t2 is not None:
        if t2 > tf:
            print("La restricción dura más que el proyecto, incrementar recursos")
        else:
            Er, E2, E3 = calcula_restriccion(K, a_estimada, pr, t1, t2)
            E1 = E_acum(K, a_estimada, t1)
            E4 = E_acum(K, a_estimada, tf) - E_acum(K, a_estimada, t2)
            tx = esfuerzo_fijo(E2, pr)
            print("\tDuración total con restricción = %.1f meses" % (tf + tx))
    else:
        print("El proyecto de 72 PM no supera la restricción asignada.")

#if rr==False:
#   print("\t")
#   print("Cálculo con restricción de recursos no fue requerido")
#   sys.exit(0)
#else:
#   print("\t")
#   print("Se calcula con restricción de recursos requeridos pr=%.1f" % (pr))

#*--- No acepta recursos por debajo del nivel prel 
#*--- Al no hacerlo las ventanas de optimización se irían para arriba
#*--- y ocurriría la condición t2>tf lo que es inconsistente

if pr<prel:
    print("** Error ** Los recursos deben ser superiores a %.1f personas" % (prel))
    pr=round(prel+0.5)
    print("Se ajusta recursos mínimos a pr=%.1f" % (pr))

#*--- Calcula las ventanas de restricción, es el intervalo [t1,t2] donde los 
#*--- recursos naturalmente requeridos por el proyecto superan el número de
#*--- recursos máximos

t1,t2 = encuentra_restriccion(K,a_estimada,pr)

if t2>tf:
    print("La restricción dura mas que el proyecto, incrementar recursos")
    exit


#CAMBIO: 8.c - Zona imposible utilizando a = 4 * a_estimada
print("\n========== PUNTO 8.c ==========")
print("Análisis utilizando a = 4 * a_estimada")
print("a original = %.3f" % (a_estimada))
print("a cuadruplicada = %.3f" % (a_cuadruple))

# Buscar la Zona imposible utilizando el nuevo valor de a
t1_c, t2_c = encuentra_restriccion(K, a_cuadruple, pr)

print("\nCon a cuadruplicada:")
print("La restricción ocurre en el intervalo [%.2f, %.2f] meses" % (t1_c, t2_c))

# Curvas para comparar el modelo original y el modelo con a x 4
t_c = np.linspace(0, tf, 200)

E_original_c = esfuerzo_instantaneo(t_c, a_estimada)
E_cuadruple_c = esfuerzo_instantaneo(t_c, a_cuadruple)

# Gráfico de comparación
plt.figure(figsize=(10, 6))

plt.plot(t_c, E_original_c,
         label='Modelo calibrado')

plt.plot(t_c, E_cuadruple_c,
         label='Modelo con a x 4')

# Línea correspondiente a la restricción de recursos
plt.axhline(pr,
            linestyle='--',
            label='Restricción de recursos')

# Zona imposible para a x 4
plt.axvspan(t1_c, t2_c,
            alpha=0.3,
            label='Zona imposible (a x 4)')

plt.xlabel('Tiempo (meses)')
plt.ylabel('Esfuerzo instantáneo (personas)')
plt.title('8.c - Efecto de cuadruplicar el parámetro a')
plt.legend()
plt.grid()
plt.show()

#*--- Estima durante la ventana cuanto esfuerzo puede ser solventado con los recursos disponibles (E3)
#*--- y cuando esfuerzo queda sin solución por falta de recursos (E2)
#*--- Calcula también los esfuerzos acumulados antes de t1 (E1) y luego de t2 (E4)

Er,E2,E3 = calcula_restriccion(K,a_estimada,pr,t1,t2)
E1=E_acum(K,a_estimada,t1)
E4=E_acum(K,a_estimada,tf)-E_acum(K,a_estimada,t2)

print("Solución de planeamiento con restricciones proyecto %s" % (name))
print("\t")
print("\tEsfuerzo nominal            (K)=%.1f PM" % (K))
print("\tTiempo para entrega        (tf)=%.1f meses" % (tf))
print("\t")
print("\tLa restriccion ocurre en el intervalo [%.1f,%.1f] meses" % (t1,t2))


print("\t\tEsfuerzo intervalo [0,%.1f] meses hasta restricción E1=%.1f PM" % (t1,E1))
print("\t\tEl total del esfuerzo en intervalo de restricción [%.1f,%.1f] Er=%.2f PM" % (t1,t2,Er))
print("\t\t\tEsfuerzo posible con recursos disponibles E3=%.2f PM" % (E3))
print("\t\t\tEsfuerzo pediente sin solución            E2=%.2f PM" % (E2))
print("\t\tEl esfuerzo en el intervalo [%.1f,%.1f]  despues de la restricción E4=%.1f PM" % (t2,tf,E4))
print("\t")

#*--- Estima cuanto tiempo (tx) con los recursos disponibles (pr) se requiere para abordar un
#*--- esfuerzo como el que está pendiente de satisfacción por falta de recursos (E2)

print("\tEl esfuerzo total en condiciones de restricción es Etot=E1+E2+E3+E4=%.1f PM" % (E1+E2+E3+E4))
tx=esfuerzo_fijo(E2,pr)

print("\t")
print("\tTiempo agregado a partir de [%.1f,%.1f] a recursos constantes %.2f meses por un total Ex=%.2f PM" % (t1,t2,tx,pr*tx))
print("\tLa duración total del proyecto será ahora")
print("\t\tEtapa sin restricción [0,%.1f]  (%.1f meses)" % (t1,t1))
print("\t\tEtapa con restricción [%.1f,%.1f] (%.1f meses)" % (t1,t2,t2-t1))
print("\t\tEtapa adicional para compensar restricción [%.1f,%.1f] (%.1f meses)" % (t2,t2+tx,tx))
print("\t\tFinalización del proyecto [%.1f,%.1f] (%.1f meses)" % (t2+tx,tf+tx,tf+tx-t2-tx))
print("\t")
print("\tDuración total del proyecto con restriccion de recursos (pr=%.1f)=%.1f meses" % (pr,tf+tx))


#*--- grafica los resultados
#*--- Utiliza segmentos diferentes para las distintas etapas E1,E2,E3,E4 y Ex
#*--- grafica a modo comparativo los esfuerzos mínimo y medio

t_E1=np.linspace(0,t1,100)
t_E1_fit = esfuerzo_instantaneo(t_E1, a_estimada)

t_E2=np.linspace(t1,t2,100)
t_E2_fit=esfuerzo_instantaneo(t_E2, a_estimada)
t_E3_fit=esfuerzo_constante(t_E2,pr)

t_Ex = np.linspace(t2,t2+tx,100)
t_Ex_fit=esfuerzo_constante(t_Ex,pr)

t_E4=np.linspace(t2+tx,tf+tx,100)
t_tail=np.linspace(t2,tf,100)
t_E4_fit = esfuerzo_instantaneo(t_tail, a_estimada)

t_med = np.linspace(0,tf+tx,100)
t_med_fit=esfuerzo_constante(t_med,pmed)

t_min = np.linspace(0,tf+tx,100)
t_min_fit=esfuerzo_constante(t_min,prel)


plt.plot(t_E1, t_E1_fit, label='E1', color='blue')
plt.plot(t_E2, t_E2_fit, label='E2 (restricción)', linestyle=":",color='blue')
plt.plot(t_E2, t_E3_fit, label='E3 (disponible)',color='red')
plt.plot(t_Ex, t_Ex_fit, label='Ex (adicional)',color='green')
plt.plot(t_E4, t_E4_fit, label='E4', color='blue')


plt.plot(t_med, t_med_fit, label='media', linestyle="--",color='black')
plt.plot(t_min, t_min_fit, label='min', linestyle=":",color='black')

plt.xlabel('Tiempo (meses)')
plt.ylabel('Esfuerzo instantáneo (personas)')
plt.legend()
plt.show()
