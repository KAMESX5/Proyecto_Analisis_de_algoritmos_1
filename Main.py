import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interfaz.server import start_server  # Importar servidor

if __name__ == "__main__":
    print("Iniciando el servidor...")
    start_server()
