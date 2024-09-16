import random

# Inicializar el tablero vacío (4x4)
tablero = [['' for _ in range(4)] for _ in range(4)]

# Piezas disponibles para el jugador y la máquina (duplicadas)
# A, a = círculo
# B, b = rombo
# C, c = cuadrado
# D, d = triángulo

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

    # Identificar si la pieza pertenece al jugador o la máquina
    es_usuario = pieza.isupper()

    # Verificar fila y columna
    for i in range(4):
        # Si hay una pieza del mismo tipo del oponente en la fila o columna, no puede colocar la pieza
        if es_usuario:
            # Si encuentra la versión minúscula de la pieza en la fila o columna
            if tablero[fila][i] == pieza.lower() or tablero[i][columna] == pieza.lower():
                return False
        else:
            # Si encuentra la versión mayúscula de la pieza en la fila o columna
            if tablero[fila][i] == pieza.upper() or tablero[i][columna] == pieza.upper():
                return False

    # Verificar cuadrante (2x2)
    inicio_fila, inicio_columna = 2 * (fila // 2), 2 * (columna // 2)
    for i in range(2):
        for j in range(2):
            celda = tablero[inicio_fila + i][inicio_columna + j]
            if es_usuario:
                # Si encuentra la versión minúscula de la pieza en el cuadrante
                if celda == pieza.lower():
                    return False
            else:
                # Si encuentra la versión mayúscula de la pieza en el cuadrante
                if celda == pieza.upper():
                    return False

    # Si pasa todas las verificaciones, el movimiento es válido
    return True


# Función para verificar si hay un ganador en un cuadrante
def verificar_ganador_cuadrante(tablero, inicio_fila, inicio_columna):
    piezas = set()
    for i in range(2):
        for j in range(2):
            pieza = tablero[inicio_fila + i][inicio_columna + j]
            if pieza == '':  # Si hay casillas vacías, no hay ganador en este cuadrante
                return False
            piezas.add(pieza.lower())
    return len(piezas) == 4  # Ganador si hay 4 piezas distintas

# Función para verificar si hay un ganador general
def verificar_ganador(tablero):
    # Verificar filas y columnas
    for i in range(4):
        # Verificar fila
        if len(set([celda.lower() for celda in tablero[i] if celda])) == 4 and '' not in tablero[i]:
            return True
        # Verificar columna
        columna = [tablero[j][i] for j in range(4)]
        if len(set([celda.lower() for celda in columna if celda])) == 4 and '' not in columna:
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
        try:
            fila = int(input("Ingresa la fila (0-3): "))
            columna = int(input("Ingresa la columna (0-3): "))
            pieza = input("Elige una pieza (A, B, C, D): ").upper()
        except ValueError:
            print("Entrada inválida, por favor ingresa valores correctos.")
            continue
        
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

# Función para verificar si hay empate
def verificar_empate():
    for fila in tablero:
        if '' in fila:  # Si hay al menos una celda vacía, no hay empate
            return False
    return True

# Juego principal
def jugar():
    while True:
        turno_jugador()
        if verificar_ganador(tablero):
            print("¡Felicidades! ¡Has ganado!")
            mostrar_tablero(tablero)
            print("Gracias por jugar.")
            break
        
        turno_maquina()
        if verificar_ganador(tablero):
            print("La máquina ha ganado.")
            mostrar_tablero(tablero)
            print("Gracias por jugar.")
            break
        
        if verificar_empate():
            print("Empate. No quedan más movimientos.")
            mostrar_tablero(tablero)
            print("Gracias por jugar.")
            break

# Iniciar el juego
jugar()
