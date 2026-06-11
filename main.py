import pygame
import sys
import copy

TAMANO_CELDA = 70
FILAS = 8
COLUMNAS = 8
ANCHO_TABLERO = TAMANO_CELDA * COLUMNAS
ALTO_TABLERO = TAMANO_CELDA * FILAS
ANCHO_PANEL = 250
ANCHO = ANCHO_TABLERO + ANCHO_PANEL
ALTO = ALTO_TABLERO
FPS = 60
TIEMPO_INICIAL = 600

# Colores
COLOR_CLARO = (238, 238, 210)
COLOR_OSCURO = (118, 150, 86)
COLOR_PANEL = (45, 45, 45)
COLOR_TEXTO = (245, 245, 245)
COLOR_SELECCION = (246, 246, 105, 180)
COLOR_MOVIMIENTO = (60, 180, 255, 150)
COLOR_ULTIMO_MOV = (255, 255, 0, 80)
COLOR_JAQUE = (255, 0, 0, 150)

UNICODE_PIEZAS = {
    "p": "♙", "t": "♖", "c": "♘", "a": "♗", "q": "♕", "k": "♔",
    "P": "♟", "T": "♜", "C": "♞", "A": "♝", "Q": "♛", "K": "♚",
}

RUTAS_IMAGENES = {
    "p": "imagenes/P.png", "t": "imagenes/T.png", "c": "imagenes/C.png",
    "a": "imagenes/A.png", "q": "imagenes/Q.png", "k": "imagenes/K.png",
    "P": "imagenes/P(2).png", "T": "imagenes/T(2).png", "C": "imagenes/C(2).png",
    "A": "imagenes/A(2).png", "Q": "imagenes/Q(2).png", "K": "imagenes/K(2).png",
}

def color_pieza(pieza):
    if pieza is None: return None
    return "blanco" if pieza.islower() else "negro"

def dentro_tablero(f, c):
    return 0 <= f < 8 and 0 <= c < 8

def camino_libre(tablero, fo, co, fd, cd):
    pf = 0 if fd == fo else (1 if fd > fo else -1)
    pc = 0 if cd == co else (1 if cd > co else -1)
    f, c = fo + pf, co + pc
    while (f, c) != (fd, cd):
        if tablero[f][c] is not None: return False
        f += pf
        c += pc
    return True

def mov_basico(tablero, fo, co, fd, cd):
    if not dentro_tablero(fd, cd): return False
    pieza = tablero[fo][co]
    if pieza is None: return False
    destino = tablero[fd][cd]
    if fo == fd and co == cd: return False
    if destino and color_pieza(pieza) == color_pieza(destino): return False

    dx, dy = cd - co, fd - fo

    if pieza == "p": # Blanco
        if dx == 0 and dy == -1 and not destino: return True
        if fo == 6 and dx == 0 and dy == -2 and not tablero[5][co] and not destino: return True
        if abs(dx) == 1 and dy == -1 and destino and destino.isupper(): return True
        return False
    if pieza == "P": # Negro
        if dx == 0 and dy == 1 and not destino: return True
        if fo == 1 and dx == 0 and dy == 2 and not tablero[2][co] and not destino: return True
        if abs(dx) == 1 and dy == 1 and destino and destino.islower(): return True
        return False
    if pieza.lower() == "c":
        return (abs(dx), abs(dy)) in [(1, 2), (2, 1)]
    if pieza.lower() == "t":
        return (fo == fd or co == cd) and camino_libre(tablero, fo, co, fd, cd)
    if pieza.lower() == "a":
        return abs(dx) == abs(dy) and camino_libre(tablero, fo, co, fd, cd)
    if pieza.lower() == "q":
        return (fo == fd or co == cd or abs(dx) == abs(dy)) and camino_libre(tablero, fo, co, fd, cd)
    if pieza.lower() == "k":
        return abs(dx) <= 1 and abs(dy) <= 1
    return False

def buscar_rey(tablero, turno):
    r = "k" if turno == "blanco" else "K"
    for f in range(8):
        for c in range(8):
            if tablero[f][c] == r: return f, c
    return None

def en_jaque(tablero, turno):
    pos = buscar_rey(tablero, turno)
    if not pos: return True
    fr, cr = pos
    enemigo = "negro" if turno == "blanco" else "blanco"
    for f in range(8):
        for c in range(8):
            p = tablero[f][c]
            if p and color_pieza(p) == enemigo:
                if mov_basico(tablero, f, c, fr, cr): return True
    return False

def mov_legal(tablero, fo, co, fd, cd, turno, movidos):
    pieza = tablero[fo][co]
    if not pieza or color_pieza(pieza) != turno: return False

    # Especial: Enroque
    if pieza.lower() == "k" and abs(cd - co) == 2 and fo == fd:
        if en_jaque(tablero, turno): return False
        direccion = 1 if cd > co else -1
        torre_col = 7 if cd > co else 0
        torre = "t" if turno == "blanco" else "T"
        if tablero[fo][torre_col] != torre: return False
        if (fo, co) in movidos or (fo, torre_col) in movidos: return False
        if not camino_libre(tablero, fo, co, fo, torre_col): return False
        for c_paso in [co + direccion, co + 2 * direccion]:
            temp = copy.deepcopy(tablero)
            temp[fo][c_paso] = pieza
            temp[fo][co] = None
            if en_jaque(temp, turno): return False
        return True

    if not mov_basico(tablero, fo, co, fd, cd): return False
    
    temp = copy.deepcopy(tablero)
    temp[fd][cd] = temp[fo][co]
    temp[fo][co] = None
    return not en_jaque(temp, turno)

def obtener_movs_legales(tablero, f, c, turno, movidos):
    res = []
    for fd in range(8):
        for cd in range(8):
            if mov_legal(tablero, f, c, fd, cd, turno, movidos):
                res.append((fd, cd))
    return res

class AjedrezJuego:
    def __init__(self):
        self.tablero = [
            ["T", "C", "A", "Q", "K", "A", "C", "T"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            [None]*8, [None]*8, [None]*8, [None]*8,
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["t", "c", "a", "q", "k", "a", "c", "t"]
        ]
        self.turno = "blanco"
        self.seleccion = None
        self.movs_posibles = []
        self.movidos = set()
        self.ultimo_mov = None
        self.tiempo_blancas = TIEMPO_INICIAL
        self.tiempo_negras = TIEMPO_INICIAL
        self.ultimo_tick = pygame.time.get_ticks()
        self.mensaje = "¡Que comience el juego!"
        self.fin = False
        self.capturadas_b = []
        self.capturadas_n = []

    def actualizar_tiempo(self):
        if self.fin: return
        ahora = pygame.time.get_ticks()
        dt = (ahora - self.ultimo_tick) / 1000
        self.ultimo_tick = ahora
        if self.turno == "blanco":
            self.tiempo_blancas -= dt
            if self.tiempo_blancas <= 0:
                self.tiempo_blancas = 0
                self.fin = True
                self.mensaje = "Tiempo agotado. Ganan Negras."
        else:
            self.tiempo_negras -= dt
            if self.tiempo_negras <= 0:
                self.tiempo_negras = 0
                self.fin = True
                self.mensaje = "Tiempo agotado. Ganan Blancas."

    def mover(self, fo, co, fd, cd):
        pieza = self.tablero[fo][co]
        captura = self.tablero[fd][cd]
        
        if pieza.lower() == "k" and abs(cd - co) == 2:
            t_col_o = 7 if cd > co else 0
            t_col_d = cd - 1 if cd > co else cd + 1
            self.tablero[fd][t_col_d] = self.tablero[fd][t_col_o]
            self.tablero[fd][t_col_o] = None
            self.movidos.add((fd, t_col_d))

        self.tablero[fd][cd] = pieza
        self.tablero[fo][co] = None
        self.movidos.add((fd, cd))
        self.ultimo_mov = ((fo, co), (fd, cd))

        if captura:
            if color_pieza(captura) == "blanco": self.capturadas_b.append(UNICODE_PIEZAS[captura])
            else: self.capturadas_n.append(UNICODE_PIEZAS[captura])

        if pieza == "p" and fd == 0: self.tablero[fd][cd] = "q"
        if pieza == "P" and fd == 7: self.tablero[fd][cd] = "Q"

        self.turno = "negro" if self.turno == "blanco" else "blanco"
        self.verificar_estado()

    def verificar_estado(self):
        hay_movs = False
        for f in range(8):
            for c in range(8):
                if self.tablero[f][c] and color_pieza(self.tablero[f][c]) == self.turno:
                    if obtener_movs_legales(self.tablero, f, c, self.turno, self.movidos):
                        hay_movs = True; break
            if hay_movs: break
        
        jaque = en_jaque(self.tablero, self.turno)
        if not hay_movs:
            self.fin = True
            if jaque: self.mensaje = f"JAQUE MATE. Gana {('Negras' if self.turno == 'blanco' else 'Blancas')}."
            else: self.mensaje = "TABLAS por Ahogado."
        elif jaque:
            self.mensaje = f"¡JAQUE al rey {self.turno}!"
        else:
            self.mensaje = f"Turno de {self.turno.capitalize()}"

def formatear_tiempo(seg):
    m = int(seg // 60)
    s = int(seg % 60)
    return f"{m:02}:{s:02}"

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ajedrez Parcial - 10 Min")
    reloj = pygame.time.Clock()
    
    f_ui = pygame.font.SysFont("segoe ui", 20)
    f_timer = pygame.font.SysFont("consolas", 36, bold=True)
    f_msg = pygame.font.SysFont("segoe ui", 18, italic=True)
    f_piezas = pygame.font.SysFont("dejavusans", 54)

    imgs = {}
    for p, r in RUTAS_IMAGENES.items():
        try:
            img = pygame.image.load(r).convert_alpha()
            imgs[p] = pygame.transform.scale(img, (TAMANO_CELDA, TAMANO_CELDA))
        except: imgs[p] = None

    juego = AjedrezJuego()

    while True:
        juego.actualizar_tiempo()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r: juego = AjedrezJuego()
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not juego.fin:
                x, y = pygame.mouse.get_pos()
                if x < ANCHO_TABLERO:
                    c, f = x // TAMANO_CELDA, y // TAMANO_CELDA
                    if juego.seleccion:
                        fo, co = juego.seleccion
                        if (f, c) in juego.movs_posibles:
                            juego.mover(fo, co, f, c)
                            juego.seleccion = None
                            juego.movs_posibles = []
                        elif juego.tablero[f][c] and color_pieza(juego.tablero[f][c]) == juego.turno:
                            juego.seleccion = (f, c)
                            juego.movs_posibles = obtener_movs_legales(juego.tablero, f, c, juego.turno, juego.movidos)
                        else:
                            juego.seleccion = None
                            juego.movs_posibles = []
                    else:
                        if juego.tablero[f][c] and color_pieza(juego.tablero[f][c]) == juego.turno:
                            juego.seleccion = (f, c)
                            juego.movs_posibles = obtener_movs_legales(juego.tablero, f, c, juego.turno, juego.movidos)

        pantalla.fill(COLOR_PANEL)
        
        for f in range(8):
            for c in range(8):
                color = COLOR_CLARO if (f + c) % 2 == 0 else COLOR_OSCURO
                pygame.draw.rect(pantalla, color, (c*TAMANO_CELDA, f*TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
                
                # Ultimo movimiento
                if juego.ultimo_mov:
                    (fo, co), (fd, cd) = juego.ultimo_mov
                    if (f, c) in [(fo, co), (fd, cd)]:
                        s = pygame.Surface((TAMANO_CELDA, TAMANO_CELDA), pygame.SRCALPHA)
                        s.fill(COLOR_ULTIMO_MOV)
                        pantalla.blit(s, (c*TAMANO_CELDA, f*TAMANO_CELDA))

        if juego.seleccion:
            f, c = juego.seleccion
            s = pygame.Surface((TAMANO_CELDA, TAMANO_CELDA), pygame.SRCALPHA)
            s.fill(COLOR_SELECCION)
            pantalla.blit(s, (c*TAMANO_CELDA, f*TAMANO_CELDA))
            for mf, mc in juego.movs_posibles:
                s = pygame.Surface((TAMANO_CELDA, TAMANO_CELDA), pygame.SRCALPHA)
                if juego.tablero[mf][mc]: s.fill((255, 0, 0, 100))
                else: pygame.draw.circle(s, COLOR_MOVIMIENTO, (TAMANO_CELDA//2, TAMANO_CELDA//2), 12)
                pantalla.blit(s, (mc*TAMANO_CELDA, mf*TAMANO_CELDA))

        if en_jaque(juego.tablero, juego.turno):
            fr, cr = buscar_rey(juego.tablero, juego.turno)
            s = pygame.Surface((TAMANO_CELDA, TAMANO_CELDA), pygame.SRCALPHA)
            s.fill(COLOR_JAQUE)
            pantalla.blit(s, (cr*TAMANO_CELDA, fr*TAMANO_CELDA))

        for f in range(8):
            for c in range(8):
                p = juego.tablero[f][c]
                if p:
                    if imgs.get(p): pantalla.blit(imgs[p], (c*TAMANO_CELDA, f*TAMANO_CELDA))
                    else:
                        txt = f_piezas.render(UNICODE_PIEZAS[p], True, (0,0,0))
                        pantalla.blit(txt, (c*TAMANO_CELDA + 5, f*TAMANO_CELDA - 5))

        px = ANCHO_TABLERO + 20
        pygame.draw.rect(pantalla, (30,30,30), (ANCHO_TABLERO + 10, 20, ANCHO_PANEL - 20, 80), border_radius=10)
        t_n = f_timer.render(formatear_tiempo(juego.tiempo_negras), True, (255, 50, 50) if juego.turno == "negro" else (150, 150, 150))
        pantalla.blit(t_n, (px + 40, 35))
        pantalla.blit(f_ui.render("NEGRAS", True, (200, 200, 200)), (px + 65, 75))

        pygame.draw.rect(pantalla, (30,30,30), (ANCHO_TABLERO + 10, ALTO - 100, ANCHO_PANEL - 20, 80), border_radius=10)
        t_b = f_timer.render(formatear_tiempo(juego.tiempo_blancas), True, (50, 255, 50) if juego.turno == "blanco" else (150, 150, 150))
        pantalla.blit(t_b, (px + 40, ALTO - 90))
        pantalla.blit(f_ui.render("BLANCAS", True, (200, 200, 200)), (px + 65, ALTO - 50))

        pygame.draw.line(pantalla, (100,100,100), (ANCHO_TABLERO + 20, 150), (ANCHO - 20, 150))
        msg_y = 170
        for linea in juego.mensaje.split(". "):
            m_surf = f_msg.render(linea, True, COLOR_TEXTO)
            pantalla.blit(m_surf, (px, msg_y))
            msg_y += 25

        pantalla.blit(f_ui.render("Capturadas:", True, (150, 150, 150)), (px, 260))
        pantalla.blit(f_ui.render("".join(juego.capturadas_n[-12:]), True, (200, 200, 200)), (px, 290))
        pantalla.blit(f_ui.render("".join(juego.capturadas_b[-12:]), True, (200, 200, 200)), (px, 320))

        pantalla.blit(f_ui.render("R para reiniciar", True, (100, 100, 100)), (px + 30, 400))

        pygame.display.flip()
        reloj.tick(FPS)

if __name__ == "__main__":
    main()
