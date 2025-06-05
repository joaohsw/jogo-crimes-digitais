import pygame
import sys
import os

# --- Inicialização do Pygame ---
pygame.init()

# --- Configurações da Tela ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guardião Digital: O Combate aos Crimes Virtuais")

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (211, 47, 47)
GREEN = (56, 142, 60)
# Cor do texto do botão, um cinza escuro para contraste
BUTTON_TEXT_COLOR = (40, 40, 40)

# --- Fontes (tamanhos ajustados) ---
title_font = pygame.font.Font(None, 70)
option_font = pygame.font.Font(None, 32)        # <<< ALTERADO: Fonte das opções diminuída
feedback_font = pygame.font.Font(None, 52)
explanation_font = pygame.font.Font(None, 32)
menu_font = pygame.font.Font(None, 70)

# --- Função para escalar imagens proporcionalmente à altura ---
def scale_image_proportional_height(image, target_height):
    original_width, original_height = image.get_size()
    if original_height == 0: return image
    aspect_ratio = original_width / original_height
    target_width = int(target_height * aspect_ratio)
    return pygame.transform.scale(image, (target_width, target_height))

# --- Carregando e escalando as imagens ---
try:
    combate_bg = pygame.image.load('combate.png').convert()
    combate_bg = pygame.transform.scale(combate_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    menu_image = pygame.image.load('menu.png').convert()
    menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    PLAYER_TARGET_HEIGHT = SCREEN_HEIGHT * 0.25
    ENEMY_TARGET_HEIGHT = SCREEN_HEIGHT * 0.40

    player_image = scale_image_proportional_height(pygame.image.load('personagem.png').convert_alpha(), PLAYER_TARGET_HEIGHT)
    phishing_image = scale_image_proportional_height(pygame.image.load('phishing.png').convert_alpha(), ENEMY_TARGET_HEIGHT)
    malware_image = scale_image_proportional_height(pygame.image.load('malware.png').convert_alpha(), ENEMY_TARGET_HEIGHT)
    senha_image = scale_image_proportional_height(pygame.image.load('senha.png').convert_alpha(), ENEMY_TARGET_HEIGHT)

    enemy_images = [phishing_image, malware_image, senha_image]

except pygame.error as e:
    print(f"Erro ao carregar ou escalar imagem: {e}")
    pygame.quit()
    sys.exit()

# --- Dados do Jogo (Fases/Crimes) ---
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
        "explanation": "Phishing tenta enganá-lo para roubar dados. Sempre desconfie de remetentes desconhecidos."
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
        "explanation": "A melhor defesa contra malware é a prevenção: use um bom antivírus e só baixe de fontes confiáveis."
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
        "explanation": "Senhas fortes e únicas para cada serviço são essenciais. Use um gerenciador de senhas."
    }
]

# --- Variáveis do Jogo ---
player_health = 3
max_player_health = 3
current_crime_index = 0
game_state = "menu"

feedback_message = ""
feedback_color = WHITE
feedback_explanation = ""
feedback_timer = 0

# --- Funções Auxiliares ---
def draw_text(text, font, color, surface, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# --- Funções de Desenho dos Estados ---

def draw_menu_screen():
    screen.blit(menu_image, (0, 0))
    draw_text("Clique em qualquer lugar para começar", menu_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85, center=True)

def draw_game_state():
    screen.blit(combate_bg, (0, 0))

    enemy_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.38) # Posição do inimigo
    player_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.60) # Posição do jogador

    current_enemy_image = enemy_images[current_crime_index]
    enemy_rect = current_enemy_image.get_rect(center=enemy_pos)
    screen.blit(current_enemy_image, enemy_rect)

    player_rect = player_image.get_rect(center=player_pos)
    screen.blit(player_image, player_rect)

    crime = crimes[current_crime_index]
    draw_text(crime["enemy_name"], title_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.08, center=True)

    draw_health_bar()

    button_rects = []
    
    # Coordenadas do centro de cada área de botão, ajustadas para o novo layout
    button_centers = [
        (SCREEN_WIDTH * 0.28, SCREEN_HEIGHT * 0.84),  # Botão superior esquerdo
        (SCREEN_WIDTH * 0.72, SCREEN_HEIGHT * 0.84),  # Botão superior direito
        (SCREEN_WIDTH * 0.28, SCREEN_HEIGHT * 0.925), # Botão inferior esquerdo
        (SCREEN_WIDTH * 0.72, SCREEN_HEIGHT * 0.925)  # Botão inferior direito
    ]
    
    button_clickable_size = (SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.07)

    for i, option in enumerate(crime["options"]):
        center_pos = button_centers[i]
        
        # <<< ALTERADO: Remove o número identificador
        draw_text(option, option_font, BUTTON_TEXT_COLOR, screen, center_pos[0], center_pos[1], center=True)

        clickable_rect = pygame.Rect((0,0), button_clickable_size)
        clickable_rect.center = center_pos
        button_rects.append(clickable_rect)
        
        # Descomente a linha abaixo para visualizar as áreas clicáveis
        # pygame.draw.rect(screen, (255,0,0), clickable_rect, 2)

    global feedback_timer
    if feedback_timer > 0:
        feedback_y = SCREEN_HEIGHT * 0.25 # Posição do feedback de acerto/erro
        draw_text(feedback_message, feedback_font, GREEN if feedback_message == "Correto!" else RED, screen, SCREEN_WIDTH/2, feedback_y, center=True)
        if feedback_explanation:
            explanation_y = SCREEN_HEIGHT * 0.75 # Posição da explicação do erro
            draw_text(feedback_explanation, explanation_font, WHITE, screen, SCREEN_WIDTH/2, explanation_y, center=True)
        feedback_timer -= 1

    return button_rects


def draw_health_bar():
    # Posição da barra de vida na parte superior esquerda
    text_x = 100
    text_y = 50
    bar_x = 200
    bar_y = 45
    segment_width = 50
    segment_height = 20

    draw_text("Integridade:", option_font, WHITE, screen, text_x, text_y, center=True)
    pygame.draw.rect(screen, RED, (bar_x, bar_y, max_player_health * segment_width, segment_height))
    if player_health > 0:
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, player_health * segment_width, segment_height))

def draw_end_screen(message, color):
    screen.blit(combate_bg, (0,0))
    msg_y = SCREEN_HEIGHT / 2 - 40
    restart_y = SCREEN_HEIGHT / 2 + 40
    draw_text(message, title_font, color, screen, SCREEN_WIDTH / 2, msg_y, center=True)
    draw_text("Clique para jogar novamente", option_font, WHITE, screen, SCREEN_WIDTH / 2, restart_y, center=True)

# --- Loop Principal do Jogo ---
def main():
    global game_state, player_health, current_crime_index, feedback_message, feedback_color, feedback_timer, feedback_explanation
    
    clock = pygame.time.Clock()
    running = True
    button_rects = [] 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "menu":
                    game_state = "playing"
                elif game_state == "playing":
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
                else: 
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
            draw_end_screen("VITÓRIA! Você protegeu o sistema!", GREEN)
        elif game_state == "game_over":
            draw_end_screen("GAME OVER! O sistema foi comprometido.", RED)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()