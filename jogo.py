import pygame
import sys
import os # Usado para verificar se os arquivos existem

# --- Inicialização do Pygame ---
pygame.init()

# --- Configurações da Tela ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guardião Digital: O Combate aos Crimes Virtuais")

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (211, 47, 47)
GREEN = (56, 142, 60)
BLUE = (25, 118, 210)
DARK_BLUE = (21, 101, 192)
LIGHT_GREY = (200, 200, 200)
BACKGROUND_COLOR = (20, 25, 40)

# --- Fontes ---
title_font = pygame.font.Font(None, 48)
option_font = pygame.font.Font(None, 28)
feedback_font = pygame.font.Font(None, 36)
explanation_font = pygame.font.Font(None, 24)
menu_font = pygame.font.Font(None, 50)

# <<< NOVO: Carregando as imagens ---
try:
    # Carrega a imagem do menu e ajusta para o tamanho da tela
    menu_image = pygame.image.load('menu.png').convert()
    menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Carrega o personagem e os inimigos com canal alfa (para transparência)
    player_image = pygame.image.load('personagem.png').convert_alpha()
    phishing_image = pygame.image.load('phishing.png').convert_alpha()
    malware_image = pygame.image.load('malware.png').convert_alpha()
    senha_image = pygame.image.load('senha.png').convert_alpha()

    # Organiza as imagens dos inimigos em uma lista na ordem das fases
    enemy_images = [phishing_image, malware_image, senha_image]

except pygame.error as e:
    print(f"Erro ao carregar imagem: {e}")
    print("\nCertifique-se que os arquivos 'menu.png', 'personagem.png', 'phishing.png', 'malware.png' e 'senha.png' estão na mesma pasta do script.")
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
game_state = "menu"  # menu, playing, game_over, victory

# Para feedback visual (certo/errado)
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
    screen.blit(menu_image, (0, 0)) # Desenha a imagem de fundo do menu
    draw_text("Clique em qualquer lugar para começar", menu_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80, center=True)

def draw_game_state():
    """Desenha todos os elementos do jogo na tela."""
    screen.fill(BACKGROUND_COLOR)

    crime = crimes[current_crime_index]
    draw_text(crime["enemy_name"], title_font, RED, screen, SCREEN_WIDTH / 2, 40, center=True)

    # <<< ALTERADO: Desenha a imagem do inimigo
    current_enemy_image = enemy_images[current_crime_index]
    enemy_rect = current_enemy_image.get_rect(center=(SCREEN_WIDTH / 2, 160))
    screen.blit(current_enemy_image, enemy_rect)

    # <<< ALTERADO: Desenha a imagem do jogador
    player_rect = player_image.get_rect(center=(SCREEN_WIDTH / 2, 500))
    screen.blit(player_image, player_rect)

    draw_health_bar()

    button_rects = []
    button_height = 60
    button_width = SCREEN_WIDTH - 100
    start_y = 280 # Ajustado Y para dar espaço para as imagens
    for i, option in enumerate(crime["options"]):
        button_rect = pygame.Rect(50, start_y + i * (button_height + 15), button_width, button_height)
        button_rects.append(button_rect)
        pygame.draw.rect(screen, BLUE, button_rect, border_radius=10)
        pygame.draw.rect(screen, DARK_BLUE, button_rect, width=3, border_radius=10)
        draw_text(f"{i+1}. {option}", option_font, WHITE, screen, button_rect.centerx, button_rect.centery, center=True)

    global feedback_timer
    if feedback_timer > 0:
        draw_text(feedback_message, feedback_font, feedback_color, screen, SCREEN_WIDTH/2, 250, center=True) # Ajustado Y
        if feedback_explanation:
            draw_text(feedback_explanation, explanation_font, LIGHT_GREY, screen, SCREEN_WIDTH/2, SCREEN_HEIGHT - 20, center=True)
        feedback_timer -= 1

    return button_rects


def draw_health_bar():
    draw_text("Sua Integridade:", option_font, WHITE, screen, 100, 560, center=True)
    pygame.draw.rect(screen, RED, (180, 550, max_player_health * 50, 20))
    if player_health > 0:
        pygame.draw.rect(screen, GREEN, (180, 550, player_health * 50, 20))

def draw_end_screen(message, color):
    screen.fill(BACKGROUND_COLOR)
    draw_text(message, title_font, color, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50, center=True)
    draw_text("Clique para jogar novamente", option_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20, center=True)


# --- Loop Principal do Jogo ---
def main():
    global game_state, player_health, current_crime_index, feedback_message, feedback_color, feedback_timer, feedback_explanation
    
    clock = pygame.time.Clock()
    running = True
    button_rects = []

    while running:
        # --- Processamento de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "menu":
                    game_state = "playing"
                elif game_state == "playing":
                    if feedback_timer <= 0:
                        crime = crimes[current_crime_index]
                        for i, button_rect in enumerate(button_rects):
                            if button_rect.collidepoint(event.pos):
                                if i == crime["correct_option_index"]:
                                    feedback_message = "Correto!"
                                    feedback_color = GREEN
                                    feedback_explanation = ""
                                    feedback_timer = 90
                                    current_crime_index += 1
                                    if current_crime_index >= len(crimes):
                                        game_state = "victory"
                                else:
                                    player_health -= 1
                                    feedback_message = "Errado!"
                                    feedback_color = RED
                                    feedback_explanation = crime["explanation"]
                                    feedback_timer = 180
                                    if player_health <= 0:
                                        game_state = "game_over"
                else: # Em game_over ou victory, um clique reseta o jogo
                    game_state = "menu"
                    player_health = max_player_health
                    current_crime_index = 0
                    feedback_timer = 0

        # --- Lógica de Atualização e Desenho ---
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