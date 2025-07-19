import pygame
import sys
import os

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con PyInstaller y desarrollo."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Inicialización de PyGame
pygame.init()

# Configuración de la ventana (ajustable a pantalla completa si se desea)
WIDTH, HEIGHT = 1200, 750  # Puedes ajustar esto según tu pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Acertijo del Cerro de las Tres Esmeraldas")
clock = pygame.time.Clock()

# Colores
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHTBLUE = (173, 216, 230)
DARKBLUE = (0, 0, 139)
GREY = (128, 128, 128)

# Estado inicial del juego (variables a migrar de main.js)
bars = [
    [1, 0, 1, 1],
    [1, 1, 0, 0],
    [0, 1, 0, 0]
]
bars_is_right = [True, True, True]
bar_x_translation = [
    [WIDTH * 0.75 - (WIDTH * 0.5 * 0.2) / 2, 0],
    [WIDTH * 0.75 - (WIDTH * 0.5 * 0.2) / 2, 0],
    [WIDTH * 0.75 - (WIDTH * 0.5 * 0.2) / 2, 0],
]
current_focus = 0
left_loser = False
right_loser = False
game_finished = False

# Variables de sensores y alarmas
left_sensor = 0
right_sensor = 0
left_alarm = False
right_alarm = False

# Variables de transición para los supresores (0=gris, 1=verde)
stone_transition_left = 0.0
stone_transition_right = 0.0
STONE_TRANSITION_SPEED = 0.15  # Entre 0 y 1 por frame, para ~0.3s

# Placeholder para funciones de renderizado y lógica
def draw_background():
    global left_loser, right_loser, game_finished
    # Dibujar imagen de fondo
    if background_img:
        bg_scaled = pygame.transform.smoothscale(background_img, (WIDTH, HEIGHT))
        screen.blit(bg_scaled, (0, 0))
    # Gradiente de color encima, con transparencia
    grad_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    if left_loser:
        for x in range(WIDTH):
            color = [
                int(RED[0] + (PURPLE[0] - RED[0]) * (x / (WIDTH * 0.3))),
                int(RED[1] + (PURPLE[1] - RED[1]) * (x / (WIDTH * 0.3))),
                int(RED[2] + (PURPLE[2] - RED[2]) * (x / (WIDTH * 0.3))),
                120
            ] if x < WIDTH * 0.3 else [*PURPLE, 120]
            pygame.draw.line(grad_surface, color, (x, 0), (x, HEIGHT))
        screen.blit(grad_surface, (0, 0))
    elif right_loser:
        for x in range(WIDTH):
            color = [
                int(PURPLE[0] + (RED[0] - PURPLE[0]) * (x / (WIDTH * 1.5))),
                int(PURPLE[1] + (RED[1] - PURPLE[1]) * (x / (WIDTH * 1.5))),
                int(PURPLE[2] + (RED[2] - PURPLE[2]) * (x / (WIDTH * 1.5))),
                120
            ] if x < WIDTH * 1.5 else [*RED, 120]
            pygame.draw.line(grad_surface, color, (x, 0), (x, HEIGHT))
        screen.blit(grad_surface, (0, 0))
    elif game_finished and not left_loser and not right_loser:
        for x in range(WIDTH):
            color = [
                int(GREEN[0] + (PURPLE[0] - GREEN[0]) * (x / (WIDTH * 0.3))),
                int(GREEN[1] + (PURPLE[1] - GREEN[1]) * (x / (WIDTH * 0.3))),
                int(GREEN[2] + (PURPLE[2] - GREEN[2]) * (x / (WIDTH * 0.3))),
                120
            ] if x < WIDTH * 0.3 else [*PURPLE, 120]
            pygame.draw.line(grad_surface, color, (x, 0), (x, HEIGHT))
        screen.blit(grad_surface, (0, 0))
    else:
        grad_surface.fill((*PURPLE, 220))
        screen.blit(grad_surface, (0, 0))

# Utilidad para dibujar rectángulos redondeados
# PyGame no tiene roundrect nativo, así que usamos draw.rect por ahora

def draw_rect(x, y, width, height, colour):
    rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    pygame.draw.rect(screen, colour, rect, border_radius=5)

# Constantes para las pistas y barras
track_width = int(WIDTH * 0.5)
track_height = int(HEIGHT * 0.025)
track_x_pos = int(WIDTH * 0.5)
track_y_pos = [
    int(HEIGHT * 0.5 - (HEIGHT * 0.3)),
    int(HEIGHT * 0.5),
    int(HEIGHT * 0.5 + (HEIGHT * 0.3))
]
bar_width = int(track_width * 0.2)
bar_height = int(track_height * 1.75)
crystal_radius = int((1/8) * bar_width)
quarter_bar = int((1/4) * bar_width)
receptor_width = int(0.05 * bar_width)
receptor_height = int(0.75 * HEIGHT)


def draw_tracks():
    for i in range(len(track_y_pos)):
        draw_rect(track_x_pos, track_y_pos[i], track_width, track_height, WHITE)
        draw_rect(track_x_pos, track_y_pos[i], track_width, int(track_height * 0.1), BLACK)
    # Receptores
    for i in range(len(bar_x_translation)):
        for j in range(len(bars[i])):
            receptor_pos_x = int((track_x_pos + (track_width // 2)) - bar_width + ((quarter_bar * (j+1)) - crystal_radius))
            draw_rect(receptor_pos_x, track_y_pos[1], receptor_width, receptor_height, WHITE)
        for j in range(len(bars[i])):
            receptor_pos_x = int((track_x_pos - (track_width // 2)) + ((quarter_bar * (j+1)) - crystal_radius))
            draw_rect(receptor_pos_x, track_y_pos[1], receptor_width, receptor_height, WHITE)
    # Indicadores con lógica de paridad
    indicator_colour = RED
    for i in range(len(bar_x_translation)):
        for j in range(len(bars[i])):
            # Right indicators
            crystal_pos_x = int((track_x_pos + (track_width // 2) - bar_width) + ((quarter_bar * (j+1)) - crystal_radius))
            right_crystals = 0
            for row in range(len(bars)):
                is_right = bars_is_right[row]
                if bars[row][j] == 1 and is_right:
                    right_crystals += 1
            color = indicator_colour if right_crystals % 2 == 0 and right_crystals != 0 else GREY
            pygame.draw.circle(screen, color, (crystal_pos_x, track_y_pos[1] + (receptor_height // 2) + 20), int(crystal_radius * 0.4))
        for j in range(len(bars[i])):
            # Left indicators
            crystal_pos_x = int((track_x_pos - (track_width // 2)) + ((quarter_bar * (j+1)) - crystal_radius))
            left_crystals = 0
            for row in range(len(bars)):
                is_right = bars_is_right[row]
                if bars[row][j] == 1 and not is_right:
                    left_crystals += 1
            color = indicator_colour if left_crystals % 2 == 0 and left_crystals != 0 else GREY
            pygame.draw.circle(screen, color, (crystal_pos_x, track_y_pos[1] + (receptor_height // 2) + 20), int(crystal_radius * 0.4))

def draw_bar():
    for i in range(len(bar_x_translation)):
        if current_focus == i:
            draw_rect(int(bar_x_translation[i][0]), track_y_pos[i], bar_width + 10, bar_height + 10, LIGHTBLUE)
        draw_rect(int(bar_x_translation[i][0]), track_y_pos[i], bar_width, bar_height, DARKBLUE)
        # Cristales (ahora ranitas)
        for j in range(len(bars[i])):
            if bars[i][j] != 0:
                crystal_pos_x = int((bar_x_translation[i][0] - (bar_width // 2)) + ((quarter_bar * (j+1)) - crystal_radius))
                if frog_img:
                    frog_size = int(crystal_radius * 1.6)
                    frog_scaled = pygame.transform.smoothscale(frog_img, (frog_size, frog_size))
                    frog_rect = frog_scaled.get_rect(center=(crystal_pos_x, track_y_pos[i]))
                    screen.blit(frog_scaled, frog_rect)
                else:
                    pygame.draw.circle(screen, YELLOW, (crystal_pos_x, track_y_pos[i]), int(crystal_radius * 0.8))

# Alarmas
alarm_radius = int((WIDTH/2) * 0.05)
alarm_margin = 0.15
left_alarm_x = int(WIDTH * alarm_margin)
left_alarm_y = int(WIDTH * 0.4)
right_alarm_x = int(WIDTH * (1 - alarm_margin))
right_alarm_y = int(WIDTH * 0.4)

def draw_alarm():
    # Left alarm
    pygame.draw.circle(screen, (169,169,169), (left_alarm_x, left_alarm_y + 5), alarm_radius + 5)
    pygame.draw.circle(screen, (128,128,128), (left_alarm_x, left_alarm_y + 5), alarm_radius)
    if left_alarm:
        pygame.draw.circle(screen, RED, (left_alarm_x, left_alarm_y + 5), int(alarm_radius * 0.7))
    # Right alarm
    pygame.draw.circle(screen, (169,169,169), (right_alarm_x, right_alarm_y + 5), alarm_radius + 5)
    pygame.draw.circle(screen, (128,128,128), (right_alarm_x, right_alarm_y + 5), alarm_radius)
    if right_alarm:
        pygame.draw.circle(screen, RED, (right_alarm_x, right_alarm_y + 5), int(alarm_radius * 0.7))

def update_sensors():
    global left_sensor, right_sensor
    left_sensor = 0
    right_sensor = 0
    for column in range(len(bars[0])):
        left_crystals = 0
        right_crystals = 0
        for row in range(len(bars)):
            is_right = bars_is_right[row]
            if bars[row][column] == 1:
                if is_right:
                    right_crystals += 1
                else:
                    left_crystals += 1
        if left_crystals % 2 == 0 and left_crystals != 0:
            left_sensor += 1
        elif right_crystals % 2 == 0 and right_crystals != 0:
            right_sensor += 1

# Lógica de movimiento de barras y controles
move_speed = 8.65  # Velocidad de animación de barra

# Cargar sonidos
try:
    bar_move_sound = pygame.mixer.Sound(resource_path("src/bar_move.wav"))
    win_sound = pygame.mixer.Sound(resource_path("src/win.wav"))
    lose_sound = pygame.mixer.Sound(resource_path("src/lose.wav"))
except Exception as e:
    bar_move_sound = win_sound = lose_sound = None
    print("No se pudieron cargar los sonidos:", e)

# Cargar imagen de rana
try:
    frog_img = pygame.image.load(resource_path("src/ranas.png")).convert_alpha()
except Exception as e:
    frog_img = None
    print("No se pudo cargar la imagen de la rana:", e)

# Cargar imágenes de piedras para los supresores
try:
    stone_grey_img = pygame.image.load(resource_path("src/grey_stone.png")).convert_alpha()
    stone_green_img = pygame.image.load(resource_path("src/green_stone.png")).convert_alpha() 
except Exception as e:
    stone_grey_img = stone_green_img = None
    print("No se pudieron cargar las imágenes de piedra:", e)

# Cargar imagen de fondo
try:
    background_img = pygame.image.load(resource_path("src/background_.png")).convert()
except Exception as e:
    background_img = None
    print("No se pudo cargar la imagen de fondo:", e)

# Fuente para mensajes
def get_font(size=48):
    try:
        return pygame.font.Font("Poppins-Regular.ttf", size)
    except:
        return pygame.font.SysFont("arial", size)

def draw_centered_text(text, color, y, size=48):
    font = get_font(size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(surface, rect)

# Lógica de victoria/derrota
def check_game_state():
    global left_loser, right_loser, game_finished
    if all(bar_x_translation[i][1] == 0 for i in range(3)):  # Todas las barras quietas
        if left_sensor == 1 and not left_alarm:
            left_loser = True
            game_finished = True
            if lose_sound:
                lose_sound.play()
        elif right_sensor == 1 and not right_alarm:
            right_loser = True
            game_finished = True
            if lose_sound:
                lose_sound.play()
        # Victoria: todas las barras a la izquierda
        elif all(not bars_is_right[i] for i in range(3)) and not game_finished:
            game_finished = True
            if win_sound:
                win_sound.play()

# Modificar move_bar para reproducir sonido
def move_bar(index):
    global bars_is_right, bar_x_translation
    if bar_move_sound:
        bar_move_sound.play()
    # Cambia la dirección de la barra
    bars_is_right[index] = not bars_is_right[index]
    # Determina la posición objetivo
    if bars_is_right[index]:
        target_x = track_x_pos + (track_width // 2) - (bar_width // 2)
    else:
        target_x = track_x_pos - (track_width // 2) + (bar_width // 2)
    # Calcula la velocidad de movimiento
    current_x = bar_x_translation[index][0]
    direction = 1 if target_x > current_x else -1
    bar_x_translation[index][1] = direction * move_speed
    bar_x_translation[index] = bar_x_translation[index][:2]  # Elimina target_x anterior si existe
    bar_x_translation[index].append(target_x)

# Mostrar mensajes de estado en pantalla
def draw_status():
    if left_loser:
        draw_centered_text("¡Perdiste!", RED, HEIGHT // 9)
    elif right_loser:
        draw_centered_text("¡Perdiste!", RED, HEIGHT //9)
    elif game_finished:
        draw_centered_text("¡Ganaste!", GREEN, HEIGHT // 9)
    else:
        draw_centered_text("Para jugar usa el mouse", WHITE, 40, 32)

def update_bar_positions():
    for i in range(len(bar_x_translation)):
        if len(bar_x_translation[i]) > 2:
            target_x = bar_x_translation[i][2]
            current_x = bar_x_translation[i][0]
            velocity = bar_x_translation[i][1]
            if (velocity > 0 and current_x + velocity >= target_x) or (velocity < 0 and current_x + velocity <= target_x):
                bar_x_translation[i][0] = target_x
                bar_x_translation[i][1] = 0
                bar_x_translation[i] = bar_x_translation[i][:2]
            else:
                bar_x_translation[i][0] += velocity

# Actualizar controles de teclado en main()
space_held = False
mouse_supresor = None  # Puede ser 'left', 'right' o None

# Coordenadas de los botones supresores
left_button_rect = pygame.Rect(left_alarm_x - alarm_radius, left_alarm_y - alarm_radius, alarm_radius * 2, alarm_radius * 2)
right_button_rect = pygame.Rect(right_alarm_x - alarm_radius, right_alarm_y - alarm_radius, alarm_radius * 2, alarm_radius * 2)

# --- Botón de reinicio ---
reset_button_rect = pygame.Rect(20, 20, 120, 40)

def reset_game():
    global bars, bars_is_right, bar_x_translation, current_focus
    global left_loser, right_loser, game_finished
    global left_sensor, right_sensor, left_alarm, right_alarm
    global space_held, mouse_supresor
    bars = [
        [1, 0, 1, 1],
        [1, 1, 0, 0],
        [0, 1, 0, 0]
    ]
    bars_is_right = [True, True, True]
    bar_x_translation = [
        [WIDTH * 0.75 - (WIDTH * 0.5 * 0.2) / 2, 0],
        [WIDTH * 0.75 - (WIDTH * 0.5 * 0.2) / 2, 0],
        [WIDTH * 0.75 - (WIDTH * 0.5 * 0.2) / 2, 0],
    ]
    current_focus = 0
    left_loser = False
    right_loser = False
    game_finished = False
    left_sensor = 0
    right_sensor = 0
    left_alarm = False
    right_alarm = False
    space_held = False
    mouse_supresor = None
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.rewind()

# --- Botones de volumen ---
volume_button_rect = pygame.Rect(WIDTH - 60, 20, 40, 40)
volume_up_rect = pygame.Rect(WIDTH - 110, 20, 40, 40)
volume_down_rect = pygame.Rect(WIDTH - 160, 20, 40, 40)
volume_muted = False
volume_level = 0.2  # 20% por defecto

def set_volume(level):
    global volume_level
    volume_level = max(0.0, min(1.0, round(level, 2)))
    if not volume_muted:
        pygame.mixer.music.set_volume(volume_level)

def toggle_volume():
    global volume_muted
    volume_muted = not volume_muted
    if volume_muted:
        pygame.mixer.music.set_volume(0)
        if bar_move_sound: bar_move_sound.set_volume(0)
        if win_sound: win_sound.set_volume(0)
        if lose_sound: lose_sound.set_volume(0)
    else:
        pygame.mixer.music.set_volume(volume_level)
        if bar_move_sound: bar_move_sound.set_volume(1)
        if win_sound: win_sound.set_volume(1)
        if lose_sound: lose_sound.set_volume(1)

def draw_volume_controls():
    # Botón mute
    pygame.draw.rect(screen, (220,220,220), volume_button_rect, border_radius=8)
    pygame.draw.rect(screen, (100,100,100), volume_button_rect, 2, border_radius=8)
    icon_img = sound_off_img if volume_muted else sound_on_img
    if icon_img:
        icon_scaled = pygame.transform.smoothscale(icon_img, (32, 32))
        icon_rect = icon_scaled.get_rect(center=volume_button_rect.center)
        screen.blit(icon_scaled, icon_rect)
    # Botón +
    pygame.draw.rect(screen, (220,220,220), volume_up_rect, border_radius=8)
    pygame.draw.rect(screen, (100,100,100), volume_up_rect, 2, border_radius=8)
    font = get_font(28)
    plus = font.render("+", True, (0,0,0))
    plus_rect = plus.get_rect(center=volume_up_rect.center)
    screen.blit(plus, plus_rect)
    # Botón -
    pygame.draw.rect(screen, (220,220,220), volume_down_rect, border_radius=8)
    pygame.draw.rect(screen, (100,100,100), volume_down_rect, 2, border_radius=8)
    minus = font.render("-", True, (0,0,0))
    minus_rect = minus.get_rect(center=volume_down_rect.center)
    screen.blit(minus, minus_rect)
    # Nivel de volumen
    vol_text = get_font(20).render(f"{int(volume_level*100)}%", True, (0,0,0))
    vol_rect = vol_text.get_rect(center=(WIDTH-85, 70))
    screen.blit(vol_text, vol_rect)

# --- Mejorar centrado de texto en botón de reinicio ---
def draw_reset_button():
    pygame.draw.rect(screen, (220,220,220), reset_button_rect, border_radius=8)
    pygame.draw.rect(screen, (100,100,100), reset_button_rect, 2, border_radius=8)
    font = get_font(28)
    text = font.render("Reiniciar", True, (0,0,0))
    text_rect = text.get_rect(center=reset_button_rect.center)
    screen.blit(text, text_rect)

def draw_supresor_buttons():
    global stone_transition_left, stone_transition_right
    # Actualizar transición izquierda
    target_left = 1.0 if left_alarm else 0.0
    if abs(stone_transition_left - target_left) > 0.01:
        stone_transition_left += (target_left - stone_transition_left) * STONE_TRANSITION_SPEED
    else:
        stone_transition_left = target_left
    # Actualizar transición derecha
    target_right = 1.0 if right_alarm else 0.0
    if abs(stone_transition_right - target_right) > 0.01:
        stone_transition_right += (target_right - stone_transition_right) * STONE_TRANSITION_SPEED
    else:
        stone_transition_right = target_right
    # Izquierdo
    center = (left_alarm_x, left_alarm_y)
    if stone_grey_img and stone_green_img:
        # Mezcla alpha
        stone_grey = pygame.transform.smoothscale(stone_grey_img, (int(alarm_radius*2), int(alarm_radius*2))).copy()
        stone_green = pygame.transform.smoothscale(stone_green_img, (int(alarm_radius*2), int(alarm_radius*2))).copy()
        stone_grey.set_alpha(int(255 * (1-stone_transition_left)))
        stone_green.set_alpha(int(255 * stone_transition_left))
        rect = stone_grey.get_rect(center=center)
        screen.blit(stone_grey, rect)
        screen.blit(stone_green, rect)
    # Derecho
    center = (right_alarm_x, right_alarm_y)
    if stone_grey_img and stone_green_img:
        stone_grey = pygame.transform.smoothscale(stone_grey_img, (int(alarm_radius*2), int(alarm_radius*2))).copy()
        stone_green = pygame.transform.smoothscale(stone_green_img, (int(alarm_radius*2), int(alarm_radius*2))).copy()
        stone_grey.set_alpha(int(255 * (1-stone_transition_right)))
        stone_green.set_alpha(int(255 * stone_transition_right))
        rect = stone_grey.get_rect(center=center)
        screen.blit(stone_grey, rect)
        screen.blit(stone_green, rect)

# Cargar imágenes de íconos de volumen
try:
    sound_on_img = pygame.image.load(resource_path("src/sound_on.png")).convert_alpha()
    sound_off_img = pygame.image.load(resource_path("src/sound_off.png")).convert_alpha()
except Exception as e:
    sound_on_img = sound_off_img = None
    print("No se pudieron cargar los íconos de volumen:", e)

# Cargar sonido de jungla de fondo
try:
    pygame.mixer.music.load(resource_path("src/sonido.mp3"))
    pygame.mixer.music.set_volume(volume_level)
    pygame.mixer.music.play(-1)  # Loop infinito
except Exception as e:
    print("No se pudo cargar el sonido de jungla:", e)


def main():
    global left_alarm, right_alarm, current_focus, space_held, mouse_supresor, volume_level
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # --- Estos botones deben funcionar SIEMPRE ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if reset_button_rect.collidepoint(mx, my):
                    reset_game()
                    continue
                if volume_button_rect.collidepoint(mx, my):
                    toggle_volume()
                    continue
                if volume_up_rect.collidepoint(mx, my):
                    if not volume_muted and volume_level < 1.0:
                        set_volume(volume_level + 0.05)
                    continue
                if volume_down_rect.collidepoint(mx, my):
                    if not volume_muted and volume_level > 0.0:
                        set_volume(volume_level - 0.05)
                    continue
            # --- El resto solo si el juego no ha terminado ---
            if not game_finished:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        current_focus = (current_focus - 1) % 3
                    if event.key == pygame.K_DOWN:
                        current_focus = (current_focus + 1) % 3
                    if event.key == pygame.K_RETURN:
                        move_bar(current_focus)
                    if event.key == pygame.K_SPACE:
                        space_held = True
                    if event.key == pygame.K_r:
                        reset_game()
                    if event.key == pygame.K_m:
                        toggle_volume()
                    if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        if not volume_muted and volume_level < 1.0:
                            set_volume(volume_level + 0.05)
                    if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        if not volume_muted and volume_level > 0.0:
                            set_volume(volume_level - 0.05)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        space_held = False
                        left_alarm = False
                        right_alarm = False
                        mouse_supresor = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    # Clic en botón izquierdo
                    if left_button_rect.collidepoint(mx, my):
                        focused_bar_x = bar_x_translation[current_focus][0]
                        if focused_bar_x < (WIDTH // 2):
                            left_alarm = True
                            right_alarm = False
                            mouse_supresor = 'left'
                    # Clic en botón derecho
                    elif right_button_rect.collidepoint(mx, my):
                        focused_bar_x = bar_x_translation[current_focus][0]
                        if focused_bar_x > (WIDTH // 2):
                            right_alarm = True
                            left_alarm = False
                            mouse_supresor = 'right'
                    else:
                        # Clic en barra
                        for i in range(3):
                            bar_rect = pygame.Rect(
                                int(bar_x_translation[i][0] - bar_width // 2),
                                int(track_y_pos[i] - bar_height // 2),
                                bar_width, bar_height
                            )
                            if bar_rect.collidepoint(mx, my):
                                if current_focus == i:
                                    move_bar(i)
                                else:
                                    current_focus = i
            # No desactivamos el supresor en MOUSEBUTTONUP ni al cambiar el enfoque
        # Lógica de supresor con espacio (dinámico)
        if space_held and not game_finished:
            focused_bar_x = bar_x_translation[current_focus][0]
            if focused_bar_x < (WIDTH // 2):
                left_alarm = True
                right_alarm = False
            elif focused_bar_x > (WIDTH // 2):
                right_alarm = True
                left_alarm = False
            else:
                left_alarm = False
                right_alarm = False
            mouse_supresor = None  # Si se activa por espacio, desactiva el de mouse
        update_bar_positions()
        update_sensors()
        check_game_state()
        draw_background()
        draw_tracks()
        draw_bar()
        draw_supresor_buttons()
        draw_reset_button()
        draw_volume_controls()
        draw_status()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 