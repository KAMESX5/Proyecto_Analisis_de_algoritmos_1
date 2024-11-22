import timeit

# Generador de palabras aleatorias
import random
import string
from Punto1 import terminal_fuerzaBruta,terminal_dinamica,terminal_voraz

def generar_palabra_aleatoria(longitud):
    """Genera una palabra aleatoria de la longitud especificada."""
    letras = string.ascii_lowercase  # Caracteres a usar: letras minúsculas
    return ''.join(random.choice(letras) for _ in range(longitud))


def medir_tiempos_subasta(A, B, ofertas):
    # Tiempo para la solución de fuerza bruta
    tiempo_fuerza_bruta = timeit.timeit(
        stmt=lambda: subastasFuerzaBruta(A, B, ofertas),
        number=3
    )

    # Tiempo para la solución dinámica
    tiempo_dinamico = timeit.timeit(
        stmt=lambda: subastas_dinamico(A, B, ofertas),
        number=3
    )

    # Tiempo para la solución voraz
    tiempo_voraz = timeit.timeit(
        stmt=lambda: subastas_voraz(ofertas, A, B),
        number=3
    )

    # Mostrar los resultados de tiempo para cada función
    print(f"Para A = {A}, B = {B}, con {len(ofertas)} ofertas:")
    print(f"  Fuerza Bruta: {tiempo_fuerza_bruta:.6f} segundos")
    print(f"  Programación Dinámica: {tiempo_dinamico:.6f} segundos")
    print(f"  Algoritmo Voraz: {tiempo_voraz:.6f} segundos\n")

if __name__ == "__main__":
    # Ejecutar pruebas para diferentes tamaños de palabra
    for longitud in [5, 10, 15, 20]:  
        medir_funciones(longitud)



