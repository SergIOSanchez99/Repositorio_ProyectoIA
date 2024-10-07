
document.addEventListener('DOMContentLoaded', () => {
    const configuracionElement = document.getElementById('configuracion');
    const tableroElement = document.getElementById('tablero');
    const comenzarBtn = document.getElementById('comenzar');
    let figuraSeleccionada = null;

    // Manejo de la configuración inicial
    comenzarBtn.addEventListener('click', () => {
        const jugadorInicial = document.getElementById('jugador_inicial').value;
        const dificultad = document.getElementById('dificultad').value;

        fetch('/configuracion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                jugador_inicial: jugadorInicial,
                dificultad: dificultad
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.mensaje);
            configuracionElement.style.display = 'none';
            tableroElement.style.display = 'block';
            dibujarTablero([ [null, null, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null] ]);
        });
    });

    // Manejo de selección de figuras
    document.querySelectorAll('.figura').forEach(button => {
        button.addEventListener('click', () => {
            figuraSeleccionada = button.dataset.figura;
        });
    });

    function dibujarTablero(tablero) {
        const gridContainer = document.getElementById('grid-container');
        gridContainer.innerHTML = '';
        for (let fila = 0; fila < 4; fila++) {
            const rowElement = document.createElement('div');
            rowElement.classList.add('fila');
            for (let columna = 0; columna < 4; columna++) {
                const celda = document.createElement('div');
                celda.classList.add('celda');
                celda.dataset.fila = fila;
                celda.dataset.columna = columna;
                if (tablero[fila][columna]) {
                    dibujarFigura(celda, tablero[fila][columna]);
                }
                rowElement.appendChild(celda);
            }
            gridContainer.appendChild(rowElement);
        }
    }

    function dibujarFigura(celda, figura) {
        switch (figura) {
            case 'Círculo':
                celda.innerHTML = '&#9711;';
                break;
            case 'Cuadrado':
                celda.innerHTML = '&#9632;';
                break;
            case 'Rectángulo':
                celda.innerHTML = '&#9644;';
                break;
            case 'Triángulo':
                celda.innerHTML = '&#9651;';
                break;
        }
    }

    // Manejo de clic en el tablero
    document.getElementById('grid-container').addEventListener('click', (e) => {
        const fila = e.target.dataset.fila;
        const columna = e.target.dataset.columna;
        if (fila !== undefined && columna !== undefined && figuraSeleccionada) {
            hacerMovimiento(fila, columna, figuraSeleccionada);
        }
    });

    function hacerMovimiento(fila, columna, figura) {
        fetch('/movimiento', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                fila: parseInt(fila),
                columna: parseInt(columna),
                pieza: figura
            })
        })
        .then(response => response.json())
        .then(data => {
            dibujarTablero(data.tablero);
            if (data.ganador) {
                alert(data.ganador + ' ha ganado!');
            }
        });
    }
});
