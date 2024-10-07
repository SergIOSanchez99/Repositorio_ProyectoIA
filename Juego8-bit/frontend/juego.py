
class Juego:
    def __init__(self, jugador_inicial, dificultad):
        self.tablero = [[None for _ in range(4)] for _ in range(4)]  # Tablero 4x4
        self.turno = jugador_inicial
        self.dificultad = dificultad
        self.ganador = None

    def hacer_movimiento(self, fila, columna, pieza):
        if self.tablero[fila][columna] is None:
            self.tablero[fila][columna] = pieza
            if self.comprobar_ganador():
                self.ganador = self.turno
            self.turno = 'IA' if self.turno == 'HUMANO' else 'HUMANO'
        return {'tablero': self.tablero, 'turno': self.turno, 'ganador': self.ganador}

    def comprobar_ganador(self):
        for fila in range(4):
            if self.tablero[fila].count(None) == 0:
                return True
        for columna in range(4):
            if all(self.tablero[fila][columna] is not None for fila in range(4)):
                return True
        return False
