import matplotlib
matplotlib.use('Agg')  # Obliga a usar el backend que no requiere interfaz gráfica
import matplotlib.pyplot as plt

def calcular_iteraciones_collatz(n):
    """Calcula la cantidad de iteraciones para que n llegue a 1."""
    iteraciones = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        iteraciones += 1
    return iteraciones

def main():
    limite_superior = 10000
    numeros_inicio = list(range(1, limite_superior + 1))
    conteo_iteraciones = []

    # Proceso de cálculo para el rango 1 - 10,000
    for i in numeros_inicio:
        pasos = calcular_iteraciones_collatz(i)
        conteo_iteraciones.append(pasos)

    # Configuración del gráfico
    plt.figure(figsize=(12, 6))
    
    # Eje X: Número de inicio (n)
    # Eje Y: Número de iteraciones para converger
    plt.scatter(numeros_inicio, conteo_iteraciones, s=1, alpha=0.5, color='royalblue')
    
    plt.title(f"Conjetura de Collatz: Iteraciones para converger (1 a {limite_superior})")
    plt.xlabel("Número de inicio (n)")
    plt.ylabel("Número de iteraciones")
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Guardar o mostrar
    print("Generando gráfico...")
    plt.savefig("collatz_grafico.png")
    plt.close()

if __name__ == "__main__":
    main()