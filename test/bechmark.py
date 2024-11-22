import timeit

# Generador de palabras aleatorias
import random
import string
from Punto1 import terminal_fuerzaBruta,terminal_dinamica,terminal_voraz
from Punto2 import subastasFuerzaBruta,subastas_dinamico,subastas_voraz

def generar_palabra_aleatoria(longitud):
    """Genera una palabra aleatoria de la longitud especificada."""
    letras = string.ascii_lowercase  # Caracteres a usar: letras minúsculas
    return ''.join(random.choice(letras) for _ in range(longitud))

def generar_datos_subasta(num_ofertas, max_acciones=1000, max_precio=500, max_minimo=300, max_maximo=600):
    """
    Genera valores aleatorios para A, B y una lista de ofertas.
    
    Args:
        num_ofertas (int): Número de ofertas a generar.
        max_acciones (int): Máximo valor para A (cantidad de acciones disponibles).
        max_precio (int): Máximo precio para B y el precio de cada oferta.
        max_minimo (int): Máximo valor para el mínimo de acciones de cada oferta.
        max_maximo (int): Máximo valor para el máximo de acciones de cada oferta.
        
    Returns:
        A (int): Cantidad de acciones disponibles.
        B (int): Precio mínimo aceptable por acción.
        ofertas (list): Lista de ofertas en el formato (precio, mínimo, máximo).
    """
    A = random.randint(1, max_acciones)        # Cantidad total de acciones disponibles
    B = random.randint(1, max_precio)          # Precio mínimo aceptable por acción
    
    ofertas = []
    for _ in range(num_ofertas):
        precio = random.randint(1, max_precio)  # Precio de la oferta
        minimo = random.randint(1, max_minimo)  # Mínimo de acciones que la oferta puede aceptar
        maximo = random.randint(minimo, max_maximo)  # Máximo de acciones que la oferta puede aceptar
        ofertas.append((precio, minimo, maximo))
    
    return A, B, ofertas

## Configura las funciones a medir
def medir_funciones(longitud_palabra):
    cadena1 = generar_palabra_aleatoria(longitud_palabra)
    cadena2 = generar_palabra_aleatoria(longitud_palabra)
    
    # Configura los tiempos para cada función, utilizando lambdas para acceder a las variables locales
    tiempo_fuerza_bruta = timeit.timeit(
        stmt=lambda: terminal_fuerzaBruta(cadena1, cadena2),
        number=5
    )
    
    tiempo_dinamica = timeit.timeit(
        stmt=lambda: terminal_dinamica(cadena1, cadena2),
        number=5
    )
    
    tiempo_voraz = timeit.timeit(
        stmt=lambda: terminal_voraz(cadena1, cadena2),
        number=5
    )
    
    # Muestra los resultados
    print(f"Para palabras de longitud {longitud_palabra}:")
    print(f"  Fuerza Bruta: {tiempo_fuerza_bruta:.6f} segundos")
    print(f"  Programación Dinámica: {tiempo_dinamica:.6f} segundos")
    print(f"  Algoritmo Voraz: {tiempo_voraz:.6f} segundos\n")

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

# Ejecutar pruebas para diferentes tamaños de palabra
for longitud in [5, 10, 15, 20]:  
    medir_funciones(longitud)


for longitud in [2, 6, 12, 16]:
    A, B, ofertas = generar_datos_subasta(num_ofertas=longitud,max_precio=150*longitud)
    #print(f"A (acciones disponibles): {A}")
    #print(f"B (precio mínimo): {B}")
    #print("Ofertas generadas (precio, mínimo, máximo):")
    #for oferta in ofertas:
    #    print(oferta)   
    medir_tiempos_subasta( A, B, ofertas)
