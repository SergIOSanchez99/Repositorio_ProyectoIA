import pygame
import random

# Constantes
TAMANO_TABLERO = 600  # Tamaño de tablero fijo
ANCHO_PANTALLA = TAMANO_TABLERO
ALTO_PANTALLA = TAMANO_TABLERO + 100  # Espacio extra para las piezas debajo
TAMANO_CUADRICULA = 4
TAMANO_CELDA = TAMANO_TABLERO // TAMANO_CUADRICULA  
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Figuras
FIGURAS = ['circulo', 'cuadrado', 'rectangulo', 'cono']

# Jugadores
HUMANO = 1
IA = 2

# Configuración de pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Geometric-4')

# Estructura de datos del tablero
tablero = [[None for _ in range(TAMANO_CUADRICULA)] for _ in range(TAMANO_CUADRICULA)]

# Piezas para cada jugador
piezas = {
    HUMANO: {'circulo': 2, 'cuadrado': 2, 'rectangulo': 2, 'cono': 2},
    IA: {'circulo': 2, 'cuadrado': 2, 'rectangulo': 2, 'cono': 2}
}

# Pieza seleccionada del jugador humano
pieza_seleccionada = None

def menu_principal():
    font = pygame.font.SysFont(None, 48)
    title_font = pygame.font.SysFont(None, 64)  # Use a larger font for the title

    texto_humano = font.render("Humano empieza", True, NEGRO)
    texto_ia = font.render("IA empieza", True, NEGRO)
    title_text = title_font.render("Geometric-4", True, NEGRO)  # Render the title text

    rect_humano = texto_humano.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 50))
    rect_ia = texto_ia.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 50))
    title_rect = title_text.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 150))  # Position the title above the options

    while True:
        pantalla.fill(BLANCO)
        
        pantalla.blit(title_text, title_rect)  # Blit the title text to the screen
        pygame.draw.rect(pantalla, ROJO, rect_humano.inflate(20, 10))
        pygame.draw.rect(pantalla, AZUL, rect_ia.inflate(20, 10))

        pantalla.blit(texto_humano, rect_humano)
        pantalla.blit(texto_ia, rect_ia)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if rect_humano.collidepoint(x, y):
                    return HUMANO

                if rect_ia.collidepoint(x, y):
                    return IA
                
def menu_dificultad():
    global dificultad_seleccionada

    font = pygame.font.SysFont(None, 48)
    title_font = pygame.font.SysFont(None, 64)

    texto_facil = font.render("Fácil", True, NEGRO)
    texto_medio = font.render("Medio", True, NEGRO)
    texto_dificil = font.render("Difícil", True, NEGRO)
    title_text = title_font.render("Seleccionar Dificultad", True, NEGRO)

    rect_facil = texto_facil.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 50))
    rect_medio = texto_medio.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
    rect_dificil = texto_dificil.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 50))
    title_rect = title_text.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 150))

    while True:
        pantalla.fill(BLANCO)
        pantalla.blit(title_text, title_rect)
        pygame.draw.rect(pantalla, AZUL, rect_facil.inflate(20, 10))
        pygame.draw.rect(pantalla, AZUL, rect_medio.inflate(20, 10))
        pygame.draw.rect(pantalla, AZUL, rect_dificil.inflate(20, 10))

        pantalla.blit(texto_facil, rect_facil)
        pantalla.blit(texto_medio, rect_medio)
        pantalla.blit(texto_dificil, rect_dificil)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if rect_facil.collidepoint(x, y):
                    dificultad_seleccionada = 'facil'
                    return
                elif rect_medio.collidepoint(x, y):
                    dificultad_seleccionada = 'medio'
                    return
                elif rect_dificil.collidepoint(x, y):
                    dificultad_seleccionada = 'dificil'
                    return
        
        

# Dibujar la cuadrícula
def dibujar_cuadricula():
    for x in range(1, TAMANO_CUADRICULA):
        pygame.draw.line(pantalla, NEGRO, (x * TAMANO_CELDA, 0), (x * TAMANO_CELDA, TAMANO_TABLERO), 2)
        pygame.draw.line(pantalla, NEGRO, (0, x * TAMANO_CELDA), (TAMANO_TABLERO, x * TAMANO_CELDA), 2)

def dibujar_celdas_no_validas(pieza_seleccionada):
    for i in range(TAMANO_CUADRICULA):
        for j in range(TAMANO_CUADRICULA):
            if not es_movimiento_valido(i, j, pieza_seleccionada, HUMANO):
                # Dibujar un "X" o colorear la celda
                pygame.draw.line(pantalla, ROJO, (j * TAMANO_CELDA, i * TAMANO_CELDA), ((j + 1) * TAMANO_CELDA, (i + 1) * TAMANO_CELDA))
                pygame.draw.line(pantalla, ROJO, ((j + 1) * TAMANO_CELDA, i * TAMANO_CELDA), (j * TAMANO_CELDA, (i + 1) * TAMANO_CELDA))

# Dibujar las piezas en el tablero
def dibujar_piezas():
    for fila in range(TAMANO_CUADRICULA):
        for columna in range(TAMANO_CUADRICULA):
            if tablero[fila][columna]:
                jugador, figura = tablero[fila][columna]
                color = ROJO if jugador == HUMANO else AZUL
                if figura == 'circulo':
                    pygame.draw.circle(pantalla, color, (columna * TAMANO_CELDA + TAMANO_CELDA // 2, fila * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 4)
                elif figura == 'cuadrado':
                    pygame.draw.rect(pantalla, color, (columna * TAMANO_CELDA + TAMANO_CELDA // 4, fila * TAMANO_CELDA + TAMANO_CELDA // 4, TAMANO_CELDA // 2, TAMANO_CELDA // 2))
                elif figura == 'rectangulo':
                    pygame.draw.rect(pantalla, color, (columna * TAMANO_CELDA + TAMANO_CELDA // 3, fila * TAMANO_CELDA + TAMANO_CELDA // 4, TAMANO_CELDA // 4, TAMANO_CELDA // 2))
                elif figura == 'cono':
                    pygame.draw.polygon(pantalla, color, [(columna * TAMANO_CELDA + TAMANO_CELDA // 2, fila * TAMANO_CELDA + TAMANO_CELDA // 4),
                                                       (columna * TAMANO_CELDA + TAMANO_CELDA // 4, fila * TAMANO_CELDA + TAMANO_CELDA // 2),
                                                       (columna * TAMANO_CELDA + 3 * TAMANO_CELDA // 4, fila * TAMANO_CELDA + TAMANO_CELDA // 2)])

# Dibujar las piezas disponibles para el jugador
def dibujar_piezas_disponibles():
    x_offset = 10
    y_offset = TAMANO_TABLERO + 20  # Posicion debajo del tablero

    areas_seleccionables = {}  # Guardar areas clickeables para las piezas restantes

    for figura in FIGURAS:
        if piezas[HUMANO][figura] > 0:  # Solo dibujar si quedan piezas disponibles
            if figura == 'circulo':
                pygame.draw.circle(pantalla, ROJO, (x_offset + 30, y_offset), 20)
                areas_seleccionables['circulo'] = pygame.Rect(x_offset, y_offset - 20, 60, 40)
            elif figura == 'cuadrado':
                pygame.draw.rect(pantalla, ROJO, (x_offset + 10, y_offset - 20, 40, 40))
                areas_seleccionables['cuadrado'] = pygame.Rect(x_offset + 10, y_offset - 20, 40, 40)
            elif figura == 'rectangulo':
                pygame.draw.rect(pantalla, ROJO, (x_offset + 20, y_offset - 20, 20, 40))
                areas_seleccionables['rectangulo'] = pygame.Rect(x_offset + 20, y_offset - 20, 20, 40)
            elif figura == 'cono':
                pygame.draw.polygon(pantalla, ROJO, [(x_offset + 30, y_offset - 30),
                                                  (x_offset + 10, y_offset + 20),
                                                  (x_offset + 50, y_offset + 20)])
                areas_seleccionables['cono'] = pygame.Rect(x_offset + 10, y_offset - 30, 40, 50)
            
            x_offset += 70

    return areas_seleccionables

def dibujar_boton_cancelar():
    font = pygame.font.SysFont(None, 36)
    texto_cancelar = font.render("Cancelar", True, NEGRO)
    rect_cancelar = texto_cancelar.get_rect(center=(ANCHO_PANTALLA - 100, ALTO_PANTALLA - 50))
    pygame.draw.rect(pantalla, ROJO, rect_cancelar.inflate(20, 10)) #Dibujar boton rojo
    pantalla.blit(texto_cancelar, rect_cancelar)
    return rect_cancelar # Retornar el rectangulo para verificar clicks

# Verificar si hay una pieza colocada por el oponente en la fila, columna, o cuadrante
def es_movimiento_valido(fila, columna, figura, jugador):
    oponente = IA if jugador == HUMANO else HUMANO  # Determinar el oponente
    
    # Verificar fila y columna
    for i in range(TAMANO_CUADRICULA):
        if tablero[fila][i] and tablero[fila][i][0] == oponente and tablero[fila][i][1] == figura:
            return False
        if tablero[i][columna] and tablero[i][columna][0] == oponente and tablero[i][columna][1] == figura:
            return False

    # Verificar cuadrante
    region_fila, region_columna = fila // 2 * 2, columna // 2 * 2
    for i in range(region_fila, region_fila + 2):
        for j in range(region_columna, region_columna + 2):
            if tablero[i][j] and tablero[i][j][0] == oponente and tablero[i][j][1] == figura:
                return False

    return True

# Colocar una pieza en el tablero
def colocar_pieza(fila, columna, figura, jugador):
    tablero[fila][columna] = (jugador, figura)
    piezas[jugador][figura] -= 1

def evaluar_tablero(jugador):
    """
    Evaluar el tablero para el jugador especificado.
    """
    puntaje = 0
    oponente = HUMANO if jugador == IA else IA

    # Criterio 1: Control de espacios
    for fila in range(TAMANO_CUADRICULA):
        for columna in range(TAMANO_CUADRICULA):
            if tablero[fila][columna] is not None:
                pieza_jugador, _ = tablero[fila][columna]
                if pieza_jugador == jugador:
                    puntaje += 10
                else:
                    puntaje -= 10

    # Criterio 2: Potencial victoria o bloqueo
    for fila in range(TAMANO_CUADRICULA):
        puntaje += evaluar_linea(fila, 0, 0, 1, jugador)  # Fila
    for columna in range(TAMANO_CUADRICULA):
        puntaje += evaluar_linea(0, columna, 1, 0, jugador)  # Columna
    
    # Evaluar cuadrantes
    for i in range(0, TAMANO_CUADRICULA, 2):
        for j in range(0, TAMANO_CUADRICULA, 2):
            puntaje += evaluar_cuadrante(i, j, jugador)

    return puntaje

def evaluar_cuadrante(fila_inicio, columna_inicio, jugador):
    """
    Evalúa un cuadrante 2x2 para el jugador especificado.
    """
    figuras_jugador = set()
    figuras_oponente = set()
    for i in range(2):
        for j in range(2):
            if tablero[fila_inicio + i][columna_inicio + j] is not None:
                pieza_jugador, figura = tablero[fila_inicio + i][columna_inicio + j]
                if pieza_jugador == jugador:
                    figuras_jugador.add(figura)
                else:
                    figuras_oponente.add(figura)
    
    if len(figuras_jugador) == 3 and len(figuras_oponente) == 0:
        return 50  # Potencial victoria
    elif len(figuras_oponente) == 3 and len(figuras_jugador) == 0:
        return 40  # Bloqueo de victoria del oponente
    elif len(figuras_jugador) == 3:
        return 30  # Tres figuras distintas
    return 0  # Aseguramos que siempre se devuelva un valor numérico
    
    
def evaluar_linea(fila, columna, delta_fila, delta_columna, jugador):
    """
    Evalúa una línea (fila o columna) para el jugador especificado.
    """
    figuras_jugador = set()
    figuras_oponente = set()
    for _ in range(TAMANO_CUADRICULA):
        if tablero[fila][columna] is not None:
            pieza_jugador, figura = tablero[fila][columna]
            if pieza_jugador == jugador:
                figuras_jugador.add(figura)
            else:
                figuras_oponente.add(figura)
        fila += delta_fila
        columna += delta_columna
    
    if len(figuras_jugador) == 3 and len(figuras_oponente) == 0:
        return 50  # Potencial victoria
    elif len(figuras_oponente) == 3 and len(figuras_jugador) == 0:
        return 40  # Bloqueo de victoria del oponente
    elif len(figuras_jugador) == 3:
        return 30  # Tres figuras distintas
    return 0


def encontrar_mejor_movimiento():
    """
    La IA evalúa los movimientos posibles y elige el mejor basándose en un algoritmo voraz.
    Ahora considera la elección de la pieza como parte de la estrategia.
    """
    mejor_puntaje = float('-inf')
    mejor_movimiento = None

    for fila in range(TAMANO_CUADRICULA):
        for columna in range(TAMANO_CUADRICULA):
            if tablero[fila][columna] is None:  # Espacio vacío
                figuras_faltantes = figuras_faltantes_en_linea(fila, columna)
                for figura in FIGURAS:  # Cambiado de figuras_faltantes a FIGURAS
                    if piezas[IA][figura] > 0 and es_movimiento_valido(fila, columna, figura, IA):
                        # Simular el movimiento
                        tablero[fila][columna] = (IA, figura)
                        puntaje = evaluar_tablero(IA)
                        
                        # Bonus por usar una pieza estratégica
                        if figura in figuras_faltantes:
                            puntaje += 20
                        
                        tablero[fila][columna] = None  # Deshacer el movimiento

                        if puntaje > mejor_puntaje:
                            mejor_puntaje = puntaje
                            mejor_movimiento = (fila, columna, figura)

    return mejor_movimiento

def figuras_faltantes_en_linea(fila, columna):
    """
    Determina qué figuras faltan en la fila, columna y cuadrante de la posición dada.
    """
    figuras_faltantes = set(FIGURAS)
    
    # Verificar fila
    for c in range(TAMANO_CUADRICULA):
        if tablero[fila][c] is not None:
            figuras_faltantes.discard(tablero[fila][c][1])
    
    # Verificar columna
    for f in range(TAMANO_CUADRICULA):
        if tablero[f][columna] is not None:
            figuras_faltantes.discard(tablero[f][columna][1])
    
    # Verificar cuadrante
    cuadrante_fila = (fila // 2) * 2
    cuadrante_columna = (columna // 2) * 2
    for f in range(cuadrante_fila, cuadrante_fila + 2):
        for c in range(cuadrante_columna, cuadrante_columna + 2):
            if tablero[f][c] is not None:
                figuras_faltantes.discard(tablero[f][c][1])
    
    return figuras_faltantes


def encontrar_mejor_movimiento():
    """
    La IA evalúa los movimientos posibles y elige el mejor basándose en un algoritmo voraz.
    """
    mejor_puntaje = float('-inf')
    mejor_movimiento = None

    for fila in range(TAMANO_CUADRICULA):
        for columna in range(TAMANO_CUADRICULA):
            if tablero[fila][columna] is None:  # Espacio vacío
                for figura in FIGURAS:
                    if piezas[IA][figura] > 0 and es_movimiento_valido(fila, columna, figura, IA):
                        # Simular el movimiento
                        tablero[fila][columna] = (IA, figura)
                        puntaje = evaluar_tablero(IA)
                        tablero[fila][columna] = None  # Deshacer el movimiento

                        if puntaje > mejor_puntaje:
                            mejor_puntaje = puntaje
                            mejor_movimiento = (fila, columna, figura)

    return mejor_movimiento

def movimiento_ia(dificultad):
    if dificultad == 'facil':
        # Dificultad fácil (movimiento aleatorio)
        movimientos_validos = []
        for row in range(TAMANO_CUADRICULA):
            for col in range(TAMANO_CUADRICULA):
                if not tablero[row][col]:  # espacio vacio
                    for shape in FIGURAS:
                        if piezas[IA][shape] > 0 and es_movimiento_valido(row, col, shape, IA):
                            movimientos_validos.append((row, col, shape))
        if movimientos_validos:
            movimiento = random.choice(movimientos_validos)
            colocar_pieza(*movimiento, IA)

    elif dificultad == 'medio':
        mejor_movimiento = encontrar_mejor_movimiento()
        if mejor_movimiento:
            fila, columna, figura = mejor_movimiento 
            colocar_pieza(fila, columna, figura, IA)
            print(f"La IA ha colocado un {figura} en la fila {fila}, columna {columna}")


def comprobar_ganador():
    # Check rows
    for fila in range(TAMANO_CUADRICULA):
        figuras_en_fila = set()
        for columna in range(TAMANO_CUADRICULA):
            if tablero[fila][columna]:
                _, figura = tablero[fila][columna]
                figuras_en_fila.add(figura)
        if len(figuras_en_fila) == 4:  # Check if we have 4 different shapes
            return True

    # Check columns
    for columna in range(TAMANO_CUADRICULA):
        figuras_en_columna = set()
        for fila in range(TAMANO_CUADRICULA):
            if tablero[fila][columna]:
                _, figura = tablero[fila][columna]
                figuras_en_columna.add(figura)
        if len(figuras_en_columna) == 4:  # Check if we have 4 different shapes
            return True

    # Check 2x2 regions
    for fila_region in range(0, TAMANO_CUADRICULA, 2):
        for columna_region in range(0, TAMANO_CUADRICULA, 2):
            figuras_en_region = set()
            for i in range(2):
                for j in range(2):
                    if tablero[fila_region + i][columna_region + j]:
                        _, figura = tablero[fila_region + i][columna_region + j]
                        figuras_en_region.add(figura)
            if len(figuras_en_region) == 4:  # Check if we have 4 different shapes
                return True

    return False

# Bucle principal del juego
def main():
    global pieza_seleccionada 

    pygame.init()

    turno = menu_principal()
    menu_dificultad()  # Jugador humano tiene el primer turno

    running = True

    while running:
        pantalla.fill(BLANCO)
        dibujar_cuadricula()
        dibujar_piezas()
        if pieza_seleccionada is not None:
            dibujar_celdas_no_validas(pieza_seleccionada)

        # Dibujar piezas disponibles para el jugador humano
        if turno == HUMANO and pieza_seleccionada is None:
            dibujar_piezas_disponibles()

        boton_cancelar_rect = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if turno == HUMANO:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()  # Obtener la posicion de click del mouse
                    
                    # Dibujar el boton cancelar si se selecciona una pieza
                    if pieza_seleccionada is not None:
                        boton_cancelar_rect = dibujar_boton_cancelar()

                    # Verificar si el jugador clickeo en el boton cancelar
                    if boton_cancelar_rect and boton_cancelar_rect.collidepoint(x, y):
                        pieza_seleccionada = None
                        print("Selección de pieza cancelada!")
                        break

                    if pieza_seleccionada is None:
                        # Verificar si el jugador clickeo en una pieza disponible
                        areas_seleccionables = dibujar_piezas_disponibles()  # Obtener las areas clickeables dinamicamente
                        for figura, rect in areas_seleccionables.items():
                            if rect.collidepoint(x, y):
                                pieza_seleccionada = figura
                                break
                    else:
                        # Despues de seleccionar la pieza, verificar donde se coloca
                        fila, columna = y // TAMANO_CELDA, x // TAMANO_CELDA  # Convertir click de mouse a cuadricula del tablero
                        
                        if 0 <= fila < 4 and 0 <= columna < 4:
                            if not tablero[fila][columna] and es_movimiento_valido(fila, columna, pieza_seleccionada, HUMANO):
                                colocar_pieza(fila, columna, pieza_seleccionada, HUMANO)
                                if comprobar_ganador():
                                    font = pygame.font.SysFont(None, 36)
                                    texto_ganador = font.render("Gana humano!", True, NEGRO)
                                    texto_rect = texto_ganador.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA - 25))
                                    pantalla.blit(texto_ganador, texto_rect)
                                    dibujar_piezas()
                                    pygame.display.flip()
                                    pygame.time.wait(2000)  # Wait for 2 seconds before quitting
                                    running = False
                                    break
                                pieza_seleccionada = None  # Reiniciar seleccion
                                turno = IA  # Turno de la IA
                        else:
                            print("El click está fuera del tablero!")

        # Dibujar el boton cancelar solo si se selecciona una pieza
        if pieza_seleccionada is not None:
            boton_cancelar_rect = dibujar_boton_cancelar()

        if turno == IA and running:
            movimiento_ia(dificultad_seleccionada)
            if comprobar_ganador():
                font = pygame.font.SysFont(None, 36)
                texto_ganador = font.render("Gana la IA!", True, NEGRO)
                texto_rect = texto_ganador.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA - 25))
                pantalla.blit(texto_ganador, texto_rect)
                dibujar_piezas()
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds before quitting
                running = False
            turno = HUMANO

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()