import pygame
import sys
import os

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guardião Digital: O Combate aos Crimes Virtuais")

fullscreen = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (211, 47, 47)
GREEN = (56, 142, 60)
BUTTON_TEXT_COLOR = (40, 40, 40)

title_font = pygame.font.Font(None, 65)
option_font = pygame.font.Font(None, 28)
feedback_font = pygame.font.Font(None, 48)
explanation_font = pygame.font.Font(None, 28)
menu_font = pygame.font.Font(None, 65)

ASSETS_PATH = 'assets'

def scale_image_proportional_height(image, target_height):
    original_width, original_height = image.get_size()
    if original_height == 0: return image
    aspect_ratio = original_width / original_height
    target_width = int(target_height * aspect_ratio)
    return pygame.transform.scale(image, (target_width, target_height))

try:
    combate_path = os.path.join(ASSETS_PATH, 'combate.png')
    combate_bg = pygame.image.load(combate_path).convert()
    combate_bg = pygame.transform.scale(combate_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    menu_path = os.path.join(ASSETS_PATH, 'menu.png')
    menu_image = pygame.image.load(menu_path).convert()
    menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    vitoria_path = os.path.join(ASSETS_PATH, 'vitoria.png')
    vitoria_image = pygame.image.load(vitoria_path).convert()
    vitoria_image = pygame.transform.scale(vitoria_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    derrota_path = os.path.join(ASSETS_PATH, 'derrota.png')
    derrota_image = pygame.image.load(derrota_path).convert()
    derrota_image = pygame.transform.scale(derrota_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    PLAYER_TARGET_HEIGHT = SCREEN_HEIGHT * 0.25
    ENEMY_TARGET_HEIGHT = SCREEN_HEIGHT * 0.35

    player_image = scale_image_proportional_height(pygame.image.load(os.path.join(ASSETS_PATH, 'personagem.png')).convert_alpha(), PLAYER_TARGET_HEIGHT)
    phishing_image = scale_image_proportional_height(pygame.image.load(os.path.join(ASSETS_PATH, 'phishing.png')).convert_alpha(), ENEMY_TARGET_HEIGHT)
    malware_image = scale_image_proportional_height(pygame.image.load(os.path.join(ASSETS_PATH, 'malware.png')).convert_alpha(), ENEMY_TARGET_HEIGHT)
    senha_image = scale_image_proportional_height(pygame.image.load(os.path.join(ASSETS_PATH, 'senha.png')).convert_alpha(), ENEMY_TARGET_HEIGHT)

    enemy_images = [phishing_image, malware_image, senha_image]

except pygame.error as e:
    print(f"Erro ao carregar imagem: {e}")
    pygame.quit()
    sys.exit()

crimes = [
    {
        "enemy_name": "Ameaça de Phishing",
        "options": [
            "Clicar no link para verificar a promoção.",
            "Responder ao e-mail com seus dados pessoais.",
            "Verificar o remetente e ignorar links suspeitos.",
            "Baixar o anexo para ver o que é."
        ],
        "correct_option_index": 2,
        "explanation": "Phishing tenta enganá-lo para roubar dados."
    },
    {
        "enemy_name": "Ataque de Malware",
        "options": [
            "Baixar software de sites não oficiais.",
            "Manter antivírus atualizado e escanear arquivos.",
            "Desativar o firewall para acelerar a internet.",
            "Ignorar as atualizações do sistema operacional."
        ],
        "correct_option_index": 1,
        "explanation": "A melhor defesa é a prevenção: use antivírus."
    },
    {
        "enemy_name": "Invasão por Senha Fraca",
        "options": [
            "Usar '123456' ou 'senha' em tudo.",
            "Criar senhas longas com letras, números e símbolos.",
            "Anotar a senha em um papel ao lado do PC.",
            "Usar a mesma senha para todos os serviços."
        ],
        "correct_option_index": 1,
        "explanation": "Senhas fortes e únicas são essenciais."
    }
]

player_health = 3
max_player_health = 3
current_crime_index = 0
game_state = "menu"
feedback_message = ""
feedback_timer = 0
feedback_explanation = ""

def draw_text(text, font, color, surface, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def draw_menu_screen():
    screen.blit(menu_image, (0, 0))
    draw_text("Pressione F11 para Tela Cheia", explanation_font, WHITE, screen, 10, 10)

def draw_game_state():
    screen.blit(combate_bg, (0, 0))

    enemy_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.38)
    player_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.60)

    current_enemy_image = enemy_images[current_crime_index]
    enemy_rect = current_enemy_image.get_rect(center=enemy_pos)
    screen.blit(current_enemy_image, enemy_rect)

    player_rect = player_image.get_rect(center=player_pos)
    screen.blit(player_image, player_rect)

    crime = crimes[current_crime_index]
    draw_text(crime["enemy_name"], title_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.12, center=True)

    draw_health_bar()

    button_rects = [
        pygame.Rect(80, 560, 515, 60),
        pygame.Rect(685, 560, 515, 60),
        pygame.Rect(80, 635, 515, 60),
        pygame.Rect(685, 635, 515, 60)
    ]

    for i, option in enumerate(crime["options"]):
        current_button_rect = button_rects[i]
        draw_text(option, option_font, BUTTON_TEXT_COLOR, screen, current_button_rect.centerx, current_button_rect.centery, center=True)

    global feedback_timer
    if feedback_timer > 0:
        feedback_y = SCREEN_HEIGHT * 0.25
        draw_text(feedback_message, feedback_font, GREEN if feedback_message == "Correto!" else RED, screen, SCREEN_WIDTH/2, feedback_y, center=True)
        if feedback_explanation:
            explanation_y = SCREEN_HEIGHT * 0.75
            draw_text(feedback_explanation, explanation_font, WHITE, screen, SCREEN_WIDTH/2, explanation_y, center=True)
        feedback_timer -= 1

    return button_rects

def draw_health_bar():
    text_x = 80
    text_y = 30
    bar_x = 160
    bar_y = 20
    segment_width = 45
    segment_height = 20

    draw_text("Pontos de vida:", option_font, WHITE, screen, text_x, text_y, center=True)
    pygame.draw.rect(screen, RED, (bar_x, bar_y, max_player_health * segment_width, segment_height))
    if player_health > 0:
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, player_health * segment_width, segment_height))

def draw_end_screen():
    if game_state == "victory":
        screen.blit(vitoria_image, (0, 0))
    elif game_state == "game_over":
        screen.blit(derrota_image, (0, 0))

def main():
    global game_state, player_health, current_crime_index, feedback_message, feedback_timer, feedback_explanation
    global screen, fullscreen
    
    clock = pygame.time.Clock()
    running = True
    button_rects = [] 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

            if game_state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = "playing"
            
            elif game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if feedback_timer <= 0:
                        crime = crimes[current_crime_index]
                        if button_rects:
                            for i, button_rect in enumerate(button_rects):
                                if button_rect.collidepoint(event.pos):
                                    if i == crime["correct_option_index"]:
                                        feedback_message = "Correto!"
                                        feedback_explanation = ""
                                        feedback_timer = 90
                                        current_crime_index += 1
                                        if current_crime_index >= len(crimes):
                                            game_state = "victory"
                                    else:
                                        player_health -= 1
                                        feedback_message = "Errado!"
                                        feedback_explanation = crime["explanation"]
                                        feedback_timer = 180
                                        if player_health <= 0:
                                            game_state = "game_over"
            
            elif game_state in ["victory", "game_over"]:
                 if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    game_state = "menu" 
                    player_health = max_player_health
                    current_crime_index = 0
                    feedback_timer = 0
                    feedback_message = ""
                    feedback_explanation = ""

        if game_state == "menu":
            draw_menu_screen()
        elif game_state == "playing":
            button_rects = draw_game_state() 
        elif game_state == "victory":
            draw_end_screen()
        elif game_state == "game_over":
            draw_end_screen()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()