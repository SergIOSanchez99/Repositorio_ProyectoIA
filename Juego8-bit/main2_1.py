import random

# Inicializar el tablero vacío (4x4)
tablero = [['' for _ in range(4)] for _ in range(4)]

# Piezas disponibles para el jugador y la máquina (duplicadas)
piezas_usuario = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D']
piezas_maquina = ['a', 'a', 'b', 'b', 'c', 'c', 'd', 'd']

# Función para mostrar el tablero
def mostrar_tablero(tablero):
    for fila in tablero:
        print(' '.join([celda if celda else '.' for celda in fila]))

# Función para verificar si la colocación es válida
def es_movimiento_valido(tablero, fila, columna, pieza):
    # Verifica si el lugar está vacío
    if tablero[fila][columna] != '':
        return False
    
    # Verificar cuadrante
    inicio_fila, inicio_columna = 2 * (fila // 2), 2 * (columna // 2)
    for i in range(2):
        for j in range(2):
            if tablero[inicio_fila + i][inicio_columna + j].lower() == pieza.lower():
                return False
    
    return True

# Función para verificar si hay un ganador en un cuadrante
def verificar_ganador_cuadrante(tablero, inicio_fila, inicio_columna):
    piezas = set()
    for i in range(2):
        for j in range(2):
            pieza = tablero[inicio_fila + i][inicio_columna + j]
            if pieza == '':
                return False
            piezas.add(pieza.lower())
    return len(piezas) == 4

# Función para verificar si hay un ganador general
def verificar_ganador(tablero):
    # Verificar filas y columnas
    for i in range(4):
        if len(set(tablero[i])) == 4 and '' not in tablero[i]:
            return True
        if len(set([tablero[j][i] for j in range(4)])) == 4 and '' not in [tablero[j][i] for j in range(4)]:
            return True

    # Verificar cada cuadrante
    for inicio_fila in range(0, 4, 2):
        for inicio_columna in range(0, 4, 2):
            if verificar_ganador_cuadrante(tablero, inicio_fila, inicio_columna):
                return True
    
    return False

# Función para turno del jugador
def turno_jugador():
    while True:
        mostrar_tablero(tablero)
        fila = int(input("Ingresa la fila (0-3): "))
        columna = int(input("Ingresa la columna (0-3): "))
        pieza = input("Elige una pieza (A, B, C, D): ").upper()
        
        if pieza in piezas_usuario and es_movimiento_valido(tablero, fila, columna, pieza):
            tablero[fila][columna] = pieza
            piezas_usuario.remove(pieza)
            break
        else:
            print("Movimiento no válido, intenta nuevamente.")

# Función para turno de la máquina
def turno_maquina():
    print("Turno de la máquina...")
    while True:
        fila = random.randint(0, 3)
        columna = random.randint(0, 3)
        pieza = random.choice(piezas_maquina)
        
        if es_movimiento_valido(tablero, fila, columna, pieza):
            tablero[fila][columna] = pieza
            piezas_maquina.remove(pieza)
            break

# Juego principal
def jugar():
    while True:
        turno_jugador()
        if verificar_ganador(tablero):
            print("¡Felicidades! ¡Has ganado!")
            mostrar_tablero(tablero)
            break
        
        turno_maquina()
        if verificar_ganador(tablero):
            print("La máquina ha ganado.")
            mostrar_tablero(tablero)
            break
        
        if not piezas_usuario and not piezas_maquina:
            print("Empate. No quedan más movimientos.")
            mostrar_tablero(tablero)
            break

jugar()
