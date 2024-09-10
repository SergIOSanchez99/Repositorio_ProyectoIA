import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Juego de Dados: Usuario vs Máquina')

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Fuente
fuente = pygame.font.Font(None, 36)

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

def turno_jugador():
    dados = []
    for i in range(3):
        pygame.time.wait(1000)  # Espera de 1 segundo entre lanzamientos
        dado = tirar_dado()
        dados.append(dado)
        pantalla.fill(NEGRO)
        dibujar_dados(dados)
        mostrar_texto(f'Lanzamiento {i + 1}', 50, 50)
        pygame.display.flip()
    return dados

def main():
    reloj = pygame.time.Clock()
    corriendo = True
    turno = True  # True para Usuario, False para Máquina

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pantalla.fill(NEGRO)
        
        if turno:
            mostrar_texto('Turno del Usuario', 50, 50)
            pygame.display.flip()
            dados_usuario = turno_jugador()
            # Procesar si el usuario quiere relanzar (esto se puede manejar con más interacción en una interfaz completa)
            mostrar_texto(f'Dados del Usuario: {dados_usuario}', 50, 150)
            pygame.display.flip()
            pygame.time.wait(2000)
        else:
            mostrar_texto('Turno de la Máquina', 50, 50)
            pygame.display.flip()
            dados_maquina = turno_jugador()
            mostrar_texto(f'Dados de la Máquina: {dados_maquina}', 50, 150)
            pygame.display.flip()
            pygame.time.wait(2000)

        turno = not turno  # Cambiar de turno

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()
