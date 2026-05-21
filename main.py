import pygame, sys
from pygame.locals import *
from tablero import *

def main():
    pygame.init()

    ANCHO = 800
    ALTO = 800
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Mi primer juego")

    clock = pygame.time.Clock()

    BLANCO = (255, 255, 255)

    tamaño = 100 

    tablero_logico = [
        ["t","c","a","q","k","a","c","t"],
        ["p","p","p","p","p","p","p","p"],
        [None]*8,
        [None]*8,
        [None]*8,
        [None]*8,
        ["p","p","p","p","p","p","p","p"],
        ["t","c","a","q","k","a","c","t"],
    ]

    imagenes = {
        "p": pygame.transform.scale(pygame.image.load("imagenes/P.png"), (tamaño, tamaño)),
        "t": pygame.transform.scale(pygame.image.load("imagenes/T.png"), (tamaño, tamaño)),
        "c": pygame.transform.scale(pygame.image.load("imagenes/C.png"), (tamaño, tamaño)),
        "a": pygame.transform.scale(pygame.image.load("imagenes/A.png"), (tamaño, tamaño)),
        "q": pygame.transform.scale(pygame.image.load("imagenes/Q.png"), (tamaño, tamaño)),
        "k": pygame.transform.scale(pygame.image.load("imagenes/K.png"), (tamaño, tamaño)),
    }

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLANCO)

        tablero(screen, tamaño)

        for fila in range(8):
            for col in range(8):
                pieza = tablero_logico[fila][col]

                if pieza:
                    img = imagenes[pieza]
                    x = col * tamaño
                    y = fila * tamaño

                    screen.blit(img, (x, y))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()