import pygame, sys
from pygame.locals import *

def tablero(pantalla, tamaño_celda):

    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)

    filas = 8
    columnas = 8

    for fila in range(filas):
        for col in range(columnas):

            if(fila + col) % 2 == 0:
                color = BLANCO
            else:
                color = NEGRO

            rect  = ( col * tamaño_celda, fila * tamaño_celda, tamaño_celda, tamaño_celda)
            pygame.draw.rect(pantalla, color, rect )
            


def main():

    pygame.init()

    ANCHO = 600
    ALTO = 600

    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Mi primer juego")

    clock = pygame.time.Clock()

    BLANCO = (255, 255, 255)

    tamaño = 60

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
    pieza_seleccionada = None

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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                x_mouse, y_mouse = pygame.mouse.get_pos()

                col = x_mouse // tamaño
                fila = y_mouse // tamaño

                if pieza_seleccionada == None:

                    if tablero_logico[fila][col] != None:
                        pieza_seleccionada = (fila, col)

                else:

                    fila_origen, col_origen = pieza_seleccionada

                    pieza = tablero_logico[fila_origen][col_origen]

                    movimiento_valido = False

                    if pieza == "p":

                     if fila == fila_origen - 1 and col == col_origen:
                        movimiento_valido = True

                    else:

                        movimiento_valido = True


                    if movimiento_valido:

                        tablero_logico[fila][col] = pieza

                        tablero_logico[fila_origen][col_origen] = None

                    pieza_seleccionada = None

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