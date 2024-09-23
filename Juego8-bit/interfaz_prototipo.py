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

# Mostrar la introducción con botones
def mostrar_intro():
    pantalla.fill(BLANCO)
    fuente = pygame.font.Font(None, 74)
    texto_juego = fuente.render('GEOMETRIC-4', True, NEGRO)
    pantalla.blit(texto_juego, (ANCHO_PANTALLA // 2 - texto_juego.get_width() // 2, ALTO_PANTALLA // 2 - 50))

    fuente = pygame.font.Font(None, 36)
    texto_instrucciones = fuente.render('¿Quién empieza?', True, NEGRO)
    pantalla.blit(texto_instrucciones, (ANCHO_PANTALLA // 2 - texto_instrucciones.get_width() // 2, ALTO_PANTALLA // 2 + 20))

    # Botones
    boton_humano = pygame.Rect(ANCHO_PANTALLA // 2 - 100, ALTO_PANTALLA // 2 + 70, 200, 50)
    boton_ia = pygame.Rect(ANCHO_PANTALLA // 2 - 100, ALTO_PANTALLA // 2 + 130, 200, 50)

    pygame.draw.rect(pantalla, ROJO, boton_humano)
    pygame.draw.rect(pantalla, AZUL, boton_ia)

    texto_humano = fuente.render('Humano', True, BLANCO)
    texto_ia = fuente.render('IA', True, BLANCO)
    pantalla.blit(texto_humano, (ANCHO_PANTALLA // 2 - texto_humano.get_width() // 2, ALTO_PANTALLA // 2 + 80))
    pantalla.blit(texto_ia, (ANCHO_PANTALLA // 2 - texto_ia.get_width() // 2, ALTO_PANTALLA // 2 + 140))

    pygame.display.flip()

    # Esperar entrada del usuario
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clic izquierdo
                    if boton_humano.collidepoint(evento.pos):
                        return HUMANO  # El humano empieza
                    elif boton_ia.collidepoint(evento.pos):
                        return IA  # La IA empieza

# Mostrar el resultado
def mostrar_resultado(gano_humano):
    pantalla.fill(BLANCO)
    fuente = pygame.font.Font(None, 74)
    if gano_humano:
        texto_ganador = fuente.render('¡Ganaste!', True, ROJO)
    else:
        texto_ganador = fuente.render('¡La IA ganó!', True, AZUL)
    pantalla.blit(texto_ganador, (ANCHO_PANTALLA // 2 - texto_ganador.get_width() // 2, ALTO_PANTALLA // 2 - 50))

    pygame.display.flip()
    pygame.time.wait(2000)  # Esperar 2 segundos antes de cerrar

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

# Movimiento de la IA (algoritmo goloso)
def movimiento_ia():
    formas_disponibles = [forma for forma in FORMAS if piezas[IA][forma] > 0]
    if not formas_disponibles:
        return  # No hay piezas disponibles

    mejor_jugada = None
    mejor_puntaje = -1

    # Evaluar todas las jugadas posibles
    for forma in formas_disponibles:
        for fila in range(4):
            for col in range(4):
                if not tablero[fila][col] and jugada_valida(fila, col, forma, IA):
                    colocar_pieza(fila, col, forma, IA)
                    if revisar_victoria(IA):
                        return  # Hacer el movimiento ganador
                    puntaje = evaluar_jugada(fila, col, forma)
                    if puntaje > mejor_puntaje:
                        mejor_puntaje = puntaje
                        mejor_jugada = (fila, col, forma)
                    tablero[fila][col] = None  # Deshacer la jugada simulada

    # Si se encuentra la mejor jugada, colócala
    if mejor_jugada:
        fila, col, forma = mejor_jugada
        colocar_pieza(fila, col, forma, IA)

# Evaluar el puntaje de una jugada
def evaluar_jugada(fila, col, forma):
    # Puedes personalizar la lógica de evaluación aquí
    return random.randint(1, 10)  # Ejemplo simple

# Revisar condiciones de victoria
def revisar_victoria(jugador):
    # Verificar filas y columnas
    for i in range(4):
        if len(set(tablero[i][j][1] for j in range(4) if tablero[i][j] and tablero[i][j][0] == jugador)) == 4:
            return True
        if len(set(tablero[j][i][1] for j in range(4) if tablero[j][i] and tablero[j][i][0] == jugador)) == 4:
            return True

    # Verificar cuadrantes 2x2
    for fila_region in range(0, 4, 2):
        for col_region in range(0, 4, 2):
            formas_en_cuadrante = set()
            for i in range(fila_region, fila_region + 2):
                for j in range(col_region, col_region + 2):
                    if tablero[i][j] and tablero[i][j][0] == jugador:
                        formas_en_cuadrante.add(tablero[i][j][1])
            if len(formas_en_cuadrante) == 4:
                return True

    return False

# Bucle principal del juego
def main():
    global pieza_seleccionada
    reloj = pygame.time.Clock()
    ejecutando = True

    # Mostrar la introducción y decidir quién empieza
    quien_empieza = mostrar_intro()

    while ejecutando:
        pantalla.fill(BLANCO)
        dibujar_cuadricula()
        dibujar_piezas()
        areas_clicables = dibujar_piezas_disponibles()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Clic izquierdo
                x, y = evento.pos
                if y < TAMAÑO_TABLERO:  # Clic dentro del tablero
                    fila, col = y // TAMAÑO_CELDA, x // TAMAÑO_CELDA
                    if pieza_seleccionada and not tablero[fila][col] and jugada_valida(fila, col, pieza_seleccionada, HUMANO):
                        colocar_pieza(fila, col, pieza_seleccionada, HUMANO)
                        if revisar_victoria(HUMANO):
                            mostrar_resultado(True)
                            ejecutando = False  # Detener el juego o implementar reinicio
                        else:
                            movimiento_ia()  # Movimiento de la IA
                            if revisar_victoria(IA):
                                mostrar_resultado(False)
                                ejecutando = False  # Detener el juego o implementar reinicio
                        pieza_seleccionada = None  # Reiniciar la selección de la pieza
                else:  # Clic en las piezas disponibles
                    for forma, area in areas_clicables.items():
                        if area.collidepoint(x, y):
                            pieza_seleccionada = forma
                            break

            # Si la IA comienza, hacer su movimiento al principio del ciclo
            if quien_empieza == IA and pieza_seleccionada is None:
                movimiento_ia()  # Movimiento de la IA
                if revisar_victoria(IA):
                    mostrar_resultado(False)
                    ejecutando = False  # Detener el juego

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()
