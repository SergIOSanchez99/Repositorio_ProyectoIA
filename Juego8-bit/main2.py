import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Juego de Dados: TRIKAZ')

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Fuente
fuente = pygame.font.Font(None, 36)

# Tamaño de los botones
BOTON_ANCHO, BOTON_ALTO = 150, 50

def tirar_dado():
    return random.randint(1, 6)

def dibujar_dados(dados):
    for i, dado in enumerate(dados):
        pygame.draw.rect(pantalla, BLANCO, (100 + i * 150, 200, 100, 100))
        texto = fuente.render(f'{dado}', True, NEGRO)
        pantalla.blit(texto, (130 + i * 150, 240))

def mostrar_texto(texto, x, y):
    texto_surf = fuente.render(texto, True, NEGRO)
    pantalla.blit(texto_surf, (x, y))

def dibujar_boton(texto, x, y):
    pygame.draw.rect(pantalla, ROJO, (x, y, BOTON_ANCHO, BOTON_ALTO))
    texto_surf = fuente.render(texto, True, BLANCO)
    pantalla.blit(texto_surf, (x + 10, y + 10))

def boton_presionado(pos, x, y, ancho, alto):
    return x <= pos[0] <= x + ancho and y <= pos[1] <= y + alto

def turno_jugador():
    dados = [tirar_dado() for _ in range(3)]
    return dados

def main():
    reloj = pygame.time.Clock()
    corriendo = True
    turno = True  # True para Usuario, False para Máquina
    dados_usuario = []
    dados_maquina = []
    puntaje_usuario = 0
    puntaje_maquina = 0
    lanzar = False
    
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if turno and boton_presionado(evento.pos, 325, 500, BOTON_ANCHO, BOTON_ALTO):
                    dados_usuario = turno_jugador()
                    puntaje_usuario = sum(dados_usuario)
                    lanzar = True
        
        pantalla.fill(NEGRO)
        
        if turno:
            mostrar_texto('Turno del Usuario', 50, 50)
            dibujar_boton('Lanzar Dados', 325, 500)
            if lanzar:
                dibujar_dados(dados_usuario)
                mostrar_texto(f'Dados del Usuario: {dados_usuario}', 50, 150)
                mostrar_texto(f'Puntaje: {puntaje_usuario}', 50, 200)
                lanzar = False
        else:
            mostrar_texto('Turno de la Máquina', 50, 50)
            dados_maquina = turno_jugador()
            puntaje_maquina = sum(dados_maquina)
            dibujar_dados(dados_maquina)
            mostrar_texto(f'Dados de la Máquina: {dados_maquina}', 50, 150)
            mostrar_texto(f'Puntaje: {puntaje_maquina}', 50, 200)
        
        pygame.display.flip()
        reloj.tick(60)

        if turno:
            pygame.time.wait(2000)  # Esperar 2 segundos después del turno del usuario
        turno = not turno  # Cambiar de turno

if __name__ == "__main__":
    main()
