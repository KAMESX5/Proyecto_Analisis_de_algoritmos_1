from flask import Flask, render_template, request
from proyecto.Punto1 import terminal_fuerzaBruta,terminal_dinamica,terminal_voraz
from proyecto.Punto2 import subastasFuerzaBruta,subastas_dinamico,subastas_voraz
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resolver', methods=['POST'])
def resolver():
    try:
        A = int(request.form['acciones'])
        B = int(request.form['precio_minimo'])
        metodo = request.form['metodo']
        ofertas_raw = request.form['ofertas']
        ofertas = [tuple(map(int, oferta.split(','))) for oferta in ofertas_raw.split('\n')]
        print(ofertas)
        if metodo == 'fuerza_bruta':
            ganancia, solucion = subastasFuerzaBruta(ofertas, A, B)
        elif metodo == 'dinamico':
            ganancia, solucion = subastas_dinamico(ofertas, A, B)
        elif metodo == 'voraz':
            ganancia, solucion = subastas_voraz(ofertas, A, B)
        else:
            return "Método no válido.", 400

        return render_template('Subasta.html', ganancia=ganancia, solucion=solucion)
    except Exception as e:
        return f"Error: {e}", 400

def start_server():
    app.run(debug=True)

    
