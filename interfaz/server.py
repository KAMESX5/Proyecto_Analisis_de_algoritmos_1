from flask import Flask, render_template, request
from proyecto.Punto1 import Terminal
from proyecto.Punto2 import subastasFuerzaBruta,subastas_dinamico,subastas_voraz
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resolver_subasta', methods=['POST'])
def resolver_subasta():
    try:
        A = int(request.form['acciones'])
        B = int(request.form['precio_minimo'])
        metodo = request.form['metodo']
        ofertas_raw = request.form['ofertas']
        ofertas = [tuple(map(int, oferta.split(','))) for oferta in ofertas_raw.split('\n')]
        if metodo == 'fuerza_bruta':
            ganancia, solucion = subastasFuerzaBruta(A, B, ofertas)
        elif metodo == 'dinamico':
            ganancia, solucion = subastas_dinamico(A, B, ofertas)
        elif metodo == 'voraz':
            ganancia, solucion = subastas_voraz(A, B, ofertas)
        else:
            return "Método no válido.", 400
        print("retorne")
        return render_template('solucion.html', ganancia=ganancia, solucion=solucion)
    except Exception as e:
        return f"Error: {e}", 400

@app.route('/resolver_terminal', methods=['POST'])
def resolver_terminal():
    try:
        cadena1 = request.form['cadena1']
        cadena2 = request.form['cadena2']
        metodo = request.form['metodo']
        terminal_inteligente = Terminal()
        if metodo == 'fuerza_bruta':
            ganancia, solucion = terminal_inteligente.terminal_fuerzaBruta(cadena1,cadena2)
        elif metodo == 'dinamico':
            ganancia, solucion = terminal_inteligente.terminal_dinamica(cadena1,cadena2)
        elif metodo == 'voraz':
            ganancia, solucion = terminal_inteligente.terminal_voraz(cadena1,cadena2)
        else:
            return "Método no válido.", 400

        return render_template('solucion.html', ganancia=ganancia, solucion=solucion)
    except Exception as e:
        return f"Error: {e}", 400



def start_server():
    app.run(debug=True)

    
