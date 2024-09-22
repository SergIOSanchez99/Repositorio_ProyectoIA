import pygame
import random

# Inicializar pygame
pygame.init()

# Constantes
TAMAÑO_TABLERO = 600  # Tamaño fijo del tablero 600x600
ANCHO_PANTALLA = TAMAÑO_TABLERO
ALTO_PANTALLA = TAMAÑO_TABLERO + 100  # Espacio extra para las piezas debajo
TAMAÑO_CELDA = TAMAÑO_TABLERO // 4  # Celda basada en el tamaño del tablero
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Formas
FORMAS = ['esfera', 'cubo', 'cilindro', 'cono']

# Jugadores
HUMANO = 1
IA = 2

# Configurar la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('GEOMETRIC-4')

# Estructura del tablero
tablero = [[None for _ in range(4)] for _ in range(4)]

# Piezas para cada jugador (8 en total por jugador)
piezas = {
    HUMANO: {'esfera': 2, 'cubo': 2, 'cilindro': 2, 'cono': 2},
    IA: {'esfera': 1, 'cubo': 1, 'cilindro': 1, 'cono': 1}  # IA solo empieza con una pieza
}

# Pieza seleccionada por el jugador humano
pieza_seleccionada = None

# Dibujar la cuadrícula
def dibujar_cuadricula():
    for x in range(1, 4):
        pygame.draw.line(pantalla, NEGRO, (x * TAMAÑO_CELDA, 0), (x * TAMAÑO_CELDA, TAMAÑO_TABLERO), 2)
        pygame.draw.line(pantalla, NEGRO, (0, x * TAMAÑO_CELDA), (TAMAÑO_TABLERO, x * TAMAÑO_CELDA), 2)

# Dibujar las piezas en el tablero
def dibujar_piezas():
    for fila in range(4):
        for col in range(4):
            if tablero[fila][col]:
                jugador, forma = tablero[fila][col]
                color = ROJO if jugador == HUMANO else AZUL
                if forma == 'esfera':
                    pygame.draw.circle(pantalla, color, (col * TAMAÑO_CELDA + TAMAÑO_CELDA // 2, fila * TAMAÑO_CELDA + TAMAÑO_CELDA // 2), TAMAÑO_CELDA // 4)
                elif forma == 'cubo':
                    pygame.draw.rect(pantalla, color, (col * TAMAÑO_CELDA + TAMAÑO_CELDA // 4, fila * TAMAÑO_CELDA + TAMAÑO_CELDA // 4, TAMAÑO_CELDA // 2, TAMAÑO_CELDA // 2))
                elif forma == 'cilindro':
                    pygame.draw.rect(pantalla, color, (col * TAMAÑO_CELDA + TAMAÑO_CELDA // 3, fila * TAMAÑO_CELDA + TAMAÑO_CELDA // 4, TAMAÑO_CELDA // 4, TAMAÑO_CELDA // 2))
                elif forma == 'cono':
                    pygame.draw.polygon(pantalla, color, [(col * TAMAÑO_CELDA + TAMAÑO_CELDA // 2, fila * TAMAÑO_CELDA + TAMAÑO_CELDA // 4),
                                                       (col * TAMAÑO_CELDA + TAMAÑO_CELDA // 4, fila * TAMAÑO_CELDA + TAMAÑO_CELDA // 2),
                                                       (col * TAMAÑO_CELDA + 3 * TAMAÑO_CELDA // 4, fila * TAMAÑO_CELDA + TAMAÑO_CELDA // 2)])

# Dibujar las piezas disponibles para el jugador humano
def dibujar_piezas_disponibles():
    x_offset = 10
    y_offset = TAMAÑO_TABLERO + 20  # Posicionadas justo debajo del tablero

    areas_clicables = {}  # Almacenar áreas clicables para las piezas restantes

    for forma in FORMAS:
        if piezas[HUMANO][forma] > 0:  # Solo dibujar si hay piezas disponibles
            if forma == 'esfera':
                pygame.draw.circle(pantalla, ROJO, (x_offset + 30, y_offset), 20)
                areas_clicables['esfera'] = pygame.Rect(x_offset, y_offset - 20, 60, 40)
            elif forma == 'cubo':
                pygame.draw.rect(pantalla, ROJO, (x_offset + 10, y_offset - 20, 40, 40))
                areas_clicables['cubo'] = pygame.Rect(x_offset + 10, y_offset - 20, 40, 40)
            elif forma == 'cilindro':
                pygame.draw.rect(pantalla, ROJO, (x_offset + 20, y_offset - 20, 20, 40))
                areas_clicables['cilindro'] = pygame.Rect(x_offset + 20, y_offset - 20, 20, 40)
            elif forma == 'cono':
                pygame.draw.polygon(pantalla, ROJO, [(x_offset + 30, y_offset - 30),
                                                     (x_offset + 10, y_offset + 20),
                                                     (x_offset + 50, y_offset + 20)])
                areas_clicables['cono'] = pygame.Rect(x_offset + 10, y_offset - 30, 40, 50)
            
            x_offset += 70

    return areas_clicables

# Verificar si una jugada es válida
def jugada_valida(fila, col, forma, jugador):
    oponente = IA if jugador == HUMANO else HUMANO  # Determinar el oponente
    
    # Revisar fila y columna
    for i in range(4):
        if tablero[fila][i] and tablero[fila][i][0] == oponente and tablero[fila][i][1] == forma:
            return False
        if tablero[i][col] and tablero[i][col][0] == oponente and tablero[i][col][1] == forma:
            return False

    # Revisar la región 2x2
    fila_region, col_region = fila // 2 * 2, col // 2 * 2
    for i in range(fila_region, fila_region + 2):
        for j in range(col_region, col_region + 2):
            if tablero[i][j] and tablero[i][j][0] == oponente and tablero[i][j][1] == forma:
                return False

    return True

# Colocar una pieza en el tablero
def colocar_pieza(fila, col, forma, jugador):
    tablero[fila][col] = (jugador, forma)
    piezas[jugador][forma] -= 1


# Movimiento de la IA (mejor decisión posible)
def movimiento_ia():
    # Buscar un movimiento ganador para la IA
    for fila in range(4):
        for col in range(4):
            if not tablero[fila][col]:  # Espacio vacío
                for forma in FORMAS:
                    if piezas[IA][forma] > 0 and jugada_valida(fila, col, forma, IA):
                        # Simular colocar la pieza para revisar si ganaría
                        tablero[fila][col] = (IA, forma)
                        if revisar_victoria(IA):
                            return  # Hacer el movimiento ganador
                        # Deshacer la jugada simulada
                        tablero[fila][col] = None

    # Bloquear al humano si está cerca de ganar
    for fila in range(4):
        for col in range(4):
            if not tablero[fila][col]:  # Espacio vacío
                for forma in FORMAS:
                    if piezas[IA][forma] > 0 and jugada_valida(fila, col, forma, HUMANO):
                        # Simular la jugada para ver si el humano ganaría
                        tablero[fila][col] = (HUMANO, forma)
                        if revisar_victoria(HUMANO):
                            # Bloquear el movimiento colocando la pieza de la IA
                            tablero[fila][col] = (IA, forma)
                            piezas[IA][forma] -= 1
                            return
                        # Deshacer la jugada simulada
                        tablero[fila][col] = None

    # Si no hay movimientos críticos, realizar un movimiento válido al azar
    movimientos_validos = []
    for fila in range(4):
        for col in range(4):
            if not tablero[fila][col]:  # Espacio vacío
                for forma in FORMAS:
                    if piezas[IA][forma] > 0 and jugada_valida(fila, col, forma, IA):
                        movimientos_validos.append((fila, col, forma))

    if movimientos_validos:
        movimiento = random.choice(movimientos_validos)
        colocar_pieza(*movimiento, IA)


# Revisar si hay una victoria
def revisar_victoria(jugador):
    # Revisar filas y columnas
    for i in range(4):
        if len(set([tablero[i][j][1] for j in range(4) if tablero[i][j] and tablero[i][j][0] == jugador])) == 4:
            return True
        if len(set([tablero[j][i][1] for j in range(4) if tablero[j][i] and tablero[j][i][0] == jugador])) == 4:
            return True

    # Revisar regiones 2x2
    for fila in range(0, 4, 2):
        for col in range(0, 4, 2):
            formas = set()
            for i in range(fila, fila + 2):
                for j in range(col, col + 2):
                    if tablero[i][j] and tablero[i][j][0] == jugador:
                        formas.add(tablero[i][j][1])
            if len(formas) == 4:
                return True

    return False

# Pantalla de inicio para seleccionar el turno
def pantalla_inicio():
    pantalla.fill(BLANCO)
    fuente = pygame.font.SysFont(None, 36)
    texto_humano = fuente.render("Humano Comienza", True, NEGRO)
    texto_ia = fuente.render("IA Comienza", True, NEGRO)
    pantalla.blit(texto_humano, (ANCHO_PANTALLA // 4 - texto_humano.get_width() // 2, ALTO_PANTALLA // 2))
    pantalla.blit(texto_ia, (3 * ANCHO_PANTALLA // 4 - texto_ia.get_width() // 2, ALTO_PANTALLA // 2))
    boton_humano = pygame.Rect(ANCHO_PANTALLA // 4 - 100, ALTO_PANTALLA // 2 - 20, 200, 50)
    boton_ia = pygame.Rect(3 * ANCHO_PANTALLA // 4 - 100, ALTO_PANTALLA // 2 - 20, 200, 50)
    pygame.draw.rect(pantalla, NEGRO, boton_humano, 2)
    pygame.draw.rect(pantalla, NEGRO, boton_ia, 2)
    return boton_humano, boton_ia

# Mostrar mensaje de victoria en pantalla
def mostrar_ganador(jugador):
    pantalla.fill(BLANCO)
    fuente = pygame.font.SysFont(None, 72)
    mensaje = "¡Humano Gana!" if jugador == HUMANO else "¡IA Gana!"
    texto = fuente.render(mensaje, True, ROJO if jugador == HUMANO else AZUL)
    pantalla.blit(texto, (ANCHO_PANTALLA // 2 - texto.get_width() // 2, ALTO_PANTALLA // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Pausa de 3 segundos antes de salir

# Bucle principal del juego
def main():
    global pieza_seleccionada  # Asegurarse de que sea global

    corriendo = True
    turno = None  # No hay turno asignado hasta que el jugador elija

    while corriendo:
        if turno is None:
            boton_humano, boton_ia = pantalla_inicio()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if boton_humano.collidepoint(x, y):
                        turno = HUMANO
                    elif boton_ia.collidepoint(x, y):
                        turno = IA
                        movimiento_ia()  # La IA realiza su primer movimiento

        else:
            pantalla.fill(BLANCO)
            dibujar_cuadricula()
            dibujar_piezas()

            # Dibujar piezas disponibles para el humano
            if turno == HUMANO and pieza_seleccionada is None:
                dibujar_piezas_disponibles()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

                if turno == HUMANO:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if pieza_seleccionada is None:
                            # Verificar si el jugador seleccionó una pieza disponible
                            areas_clicables = dibujar_piezas_disponibles()
                            for forma, rect in areas_clicables.items():
                                if rect.collidepoint(x, y):
                                    pieza_seleccionada = forma
                                    break
                        else:
                            # Colocar la pieza seleccionada
                            fila, col = y // TAMAÑO_CELDA, x // TAMAÑO_CELDA
                            if fila < 4 and col < 4 and not tablero[fila][col] and jugada_valida(fila, col, pieza_seleccionada, HUMANO):
                                colocar_pieza(fila, col, pieza_seleccionada, HUMANO)
                                if revisar_victoria(HUMANO):
                                    mostrar_ganador(HUMANO)
                                    corriendo = False
                                pieza_seleccionada = None
                                turno = IA

            if turno == IA:
                movimiento_ia()
                if revisar_victoria(IA):
                    mostrar_ganador(IA)
                    corriendo = False
                turno = HUMANO

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
