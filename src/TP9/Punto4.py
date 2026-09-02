"""
Punto4.py

Script para estimar el esfuerzo (E) y el tiempo calendario (td) de un
proyecto de software a partir de su tamaño (S), utilizando un modelo
tipo COCOMO:

    E  = 8 * S^0.95        (esfuerzo, en personas-mes, en función del tamaño S)
    td = 2.4 * E^0.33      (tiempo calendario, en meses, en función del esfuerzo E)

El script grafica en pantalla:
    1) E en función de S, para S en un intervalo [s_min, s_max]
    2) td en función de E, para E en un intervalo [e_min, e_max]

Los límites de ambos intervalos se reciben como argumentos de línea de
comandos (no están fijos en el código).

Requisitos:
    pip install numpy matplotlib

Uso:
    python Punto4.py --s-min 0 --s-max 10000 --e-min 1 --e-max 500
"""

import argparse
import sys

import matplotlib
import numpy as np


def _configurar_backend_interactivo() -> None:
    """
    Intenta seleccionar un backend interactivo de matplotlib para poder
    mostrar los gráficos en pantalla con plt.show().

    Se prueban varios backends comunes en orden de preferencia, cubriendo
    los más habituales en Linux, macOS y Windows.  Para cada candidato se
    verifica que su módulo pueda importarse realmente (matplotlib.use() por
    sí solo no garantiza que el backend funcione, ya que la importación
    real se difiere hasta el primer uso de pyplot).

    Si ningún backend interactivo está disponible, el script termina con un
    mensaje que indica cómo instalar uno.
    """
    from matplotlib.backends.registry import BackendRegistry

    registry = BackendRegistry()

    # Orden de preferencia: Qt → Tk → GTK → macOS nativo
    candidatos = ("QtAgg", "Qt5Agg", "TkAgg", "GTK3Agg", "GTK4Agg", "macosx")

    for backend in candidatos:
        try:
            # Verificar que el módulo del backend realmente puede importarse
            registry.load_backend_module(backend)
            matplotlib.use(backend)
            return
        except (ImportError, ModuleNotFoundError):
            continue

    sys.exit(
        "No se encontró un backend gráfico interactivo.\n"
        "Instalá alguno de los siguientes para poder ver los gráficos:\n"
        "  Linux:   sudo apt-get install python3-tk\n"
        "  macOS:   brew install python-tk\n"
        "  Cualquier SO: pip install PyQt5"
    )


_configurar_backend_interactivo()

import matplotlib.pyplot as plt  # noqa: E402  (import tras configurar el backend)


def calcular_esfuerzo(tamano: np.ndarray) -> np.ndarray:
    """
    Calcula el esfuerzo estimado (E) de un proyecto a partir de su tamaño (S).

    Fórmula: E = 8 * S^0.95

    Args:
        tamano (np.ndarray): Arreglo de tamaños del proyecto (S), en la
            unidad definida por el modelo (p. ej. KLOC o puntos de función).

    Returns:
        np.ndarray: Esfuerzo estimado (E), en personas-mes.
    """
    return 8 * np.power(tamano, 0.95)


def calcular_tiempo_calendario(esfuerzo: np.ndarray) -> np.ndarray:
    """
    Calcula el tiempo calendario estimado (td) a partir del esfuerzo (E).

    Fórmula: td = 2.4 * E^0.33

    Args:
        esfuerzo (np.ndarray): Arreglo de valores de esfuerzo (E), en
            personas-mes.

    Returns:
        np.ndarray: Tiempo calendario estimado (td), en meses.
    """
    return 2.4 * np.power(esfuerzo, 0.33)


def graficar_esfuerzo_vs_tamano(tamanos: np.ndarray, esfuerzos: np.ndarray) -> None:
    """
    Genera el gráfico de esfuerzo (E) en función del tamaño (S).

    Args:
        tamanos (np.ndarray): Valores de tamaño (S) usados en el eje X.
        esfuerzos (np.ndarray): Valores de esfuerzo (E) usados en el eje Y.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(tamanos, esfuerzos, color="tab:blue", linewidth=2)
    plt.title("Esfuerzo (E) en función del tamaño del proyecto (S)")
    plt.xlabel("Tamaño del proyecto (S)")
    plt.ylabel("Esfuerzo (E) [personas-mes]")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


def graficar_tiempo_vs_esfuerzo(esfuerzos: np.ndarray, tiempos: np.ndarray) -> None:
    """
    Genera el gráfico de tiempo calendario (td) en función del esfuerzo (E).

    Args:
        esfuerzos (np.ndarray): Valores de esfuerzo (E) usados en el eje X.
        tiempos (np.ndarray): Valores de tiempo calendario (td) usados en el eje Y.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(esfuerzos, tiempos, color="tab:green", linewidth=2)
    plt.title("Tiempo calendario (td) en función del esfuerzo (E)")
    plt.xlabel("Esfuerzo (E) [personas-mes]")
    plt.ylabel("Tiempo calendario (td) [meses]")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


def parsear_argumentos() -> argparse.Namespace:
    """
    Define y parsea los argumentos de línea de comandos del script.

    Argumentos soportados:
        --s-min   Límite inferior del intervalo de tamaños S (default: 0)
        --s-max   Límite superior del intervalo de tamaños S (default: 10000)
        --e-min   Límite inferior del intervalo de esfuerzos E (default: 1)
        --e-max   Límite superior del intervalo de esfuerzos E (default: 500)
        --puntos  Cantidad de puntos usados para graficar cada curva (default: 1000)

    Returns:
        argparse.Namespace: Objeto con los valores de los argumentos parseados.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Calcula y grafica el esfuerzo (E) en función del tamaño (S) "
            "y el tiempo calendario (td) en función del esfuerzo (E)."
        )
    )
    parser.add_argument(
        "--s-min", type=float, default=0,
        help="Límite inferior del intervalo de tamaños S (default: 0)."
    )
    parser.add_argument(
        "--s-max", type=float, default=10000,
        help="Límite superior del intervalo de tamaños S (default: 10000)."
    )
    parser.add_argument(
        "--e-min", type=float, default=1,
        help="Límite inferior del intervalo de esfuerzos E (default: 1)."
    )
    parser.add_argument(
        "--e-max", type=float, default=500,
        help="Límite superior del intervalo de esfuerzos E (default: 500)."
    )
    parser.add_argument(
        "--puntos", type=int, default=1000,
        help="Cantidad de puntos usados para graficar cada curva (default: 1000)."
    )
    return parser.parse_args()


def main() -> None:
    """
    Función principal: obtiene los intervalos desde los argumentos de línea
    de comandos, calcula E y td, y muestra ambos gráficos en pantalla.
    """
    args = parsear_argumentos()

    # Intervalo de tamaños [s_min, s_max] para calcular el esfuerzo E
    tamanos = np.linspace(args.s_min, args.s_max, num=args.puntos)
    esfuerzos_para_tamanos = calcular_esfuerzo(tamanos)

    # Intervalo de esfuerzos [e_min, e_max] para calcular el tiempo calendario td
    esfuerzos = np.linspace(args.e_min, args.e_max, num=args.puntos)
    tiempos = calcular_tiempo_calendario(esfuerzos)

    # Mostrar los gráficos solicitados en pantalla
    graficar_esfuerzo_vs_tamano(tamanos, esfuerzos_para_tamanos)
    graficar_tiempo_vs_esfuerzo(esfuerzos, tiempos)


if __name__ == "__main__":
    main()