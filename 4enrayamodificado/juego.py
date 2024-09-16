import pygame
import random

# Inicializando pygame
pygame.init()

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
pygame.display.set_caption('Quantik')

# Estructura de datos del tablero
tablero = [[None for _ in range(TAMANO_CUADRICULA)] for _ in range(TAMANO_CUADRICULA)]

# Piezas para cada jugador
piezas = {
    HUMANO: {'circulo': 2, 'cuadrado': 2, 'rectangulo': 2, 'cono': 2},
    IA: {'circulo': 2, 'cuadrado': 2, 'rectangulo': 2, 'cono': 2}
}

# Pieza seleccionada del jugador humano
pieza_seleccionada = None

# Dibujar la cuadrícula
def dibujar_cuadricula():
    for x in range(1, TAMANO_CUADRICULA):
        pygame.draw.line(pantalla, NEGRO, (x * TAMANO_CELDA, 0), (x * TAMANO_CELDA, TAMANO_TABLERO), 2)
        pygame.draw.line(pantalla, NEGRO, (0, x * TAMANO_CELDA), (TAMANO_TABLERO, x * TAMANO_CELDA), 2)

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

# Movimiento de la IA (movimiento basico valido aleatorio)
def movimiento_ia():
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

# Comprobar si hay un movimiento ganador (4 figuras distintas en una fila, columna o cuadrante)
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

    running = True
    turno = HUMANO  # Jugador humano tiene el primer turno

    while running:
        pantalla.fill(BLANCO)
        dibujar_cuadricula()
        dibujar_piezas()

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
                                    print("Gana humano!")
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
            movimiento_ia()
            if comprobar_ganador():
                print("Gana la IA!")
                running = False
            turno = HUMANO

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()