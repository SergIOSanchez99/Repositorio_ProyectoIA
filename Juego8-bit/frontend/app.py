
from flask import Flask, render_template, jsonify, request
from juego import Juego

app = Flask(__name__)

# Instancia del juego
juego = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configuracion', methods=['POST'])
def configuracion():
    global juego
    data = request.json
    jugador_inicial = data['jugador_inicial']
    dificultad = data['dificultad']
    juego = Juego(jugador_inicial, dificultad)
    return jsonify({'mensaje': 'Configuración guardada correctamente'})

@app.route('/movimiento', methods=['POST'])
def movimiento():
    data = request.json
    fila = data['fila']
    columna = data['columna']
    pieza = data['pieza']
    resultado = juego.hacer_movimiento(fila, columna, pieza)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
