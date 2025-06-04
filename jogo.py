import pygame
import sys
import textwrap

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guardião Digital: O Combate aos Crimes Virtuais")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (211, 47, 47)
GREEN = (56, 142, 60)
BLUE = (25, 118, 210)
DARK_BLUE = (21, 101, 192)
LIGHT_GREY = (200, 200, 200)
BACKGROUND_COLOR = (20, 25, 40) 
PLAYER_COLOR = (0, 200, 255) 
ENEMY_COLOR = (255, 80, 80) 

title_font = pygame.font.Font(None, 48)
option_font = pygame.font.Font(None, 28)
feedback_font = pygame.font.Font(None, 36)
explanation_font = pygame.font.Font(None, 24)

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
        "explanation": "Phishing tenta enganá-lo para roubar dados. Sempre desconfie de remetentes desconhecidos e nunca clique em links ou anexos suspeitos."
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
        "explanation": "A melhor defesa contra malware é a prevenção: use um bom antivírus, mantenha tudo atualizado e só baixe de fontes confiáveis."
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
        "explanation": "Senhas fortes e únicas para cada serviço são essenciais. Use um gerenciador de senhas para ajudar a lembrar delas."
    }
]


player_health = 3
max_player_health = 3
current_crime_index = 0
game_state = "playing"  

feedback_message = ""
feedback_color = WHITE
feedback_explanation = ""
feedback_timer = 0


def draw_text(text, font, color, surface, x, y, center=False, max_width=None):
    """Função para desenhar texto, com quebra de linha opcional."""
    if max_width:
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            if font.size(current_line + " " + word)[0] <= max_width:
                current_line += " " + word
            else:
                lines.append(current_line.strip())
                current_line = word
        lines.append(current_line.strip())
        
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect()
            if center:
                text_rect.center = (x, y + i * font.get_height())
            else:
                text_rect.topleft = (x, y + i * font.get_height())
            surface.blit(text_surface, text_rect)
    else:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)


def draw_game_state():
    """Desenha todos os elementos do jogo na tela."""
    screen.fill(BACKGROUND_COLOR)

    crime = crimes[current_crime_index]
    draw_text(crime["enemy_name"], title_font, ENEMY_COLOR, screen, SCREEN_WIDTH / 2, 80, center=True)
    
    pygame.draw.rect(screen, ENEMY_COLOR, (SCREEN_WIDTH / 2 - 50, 120, 100, 100))
    
    pygame.draw.rect(screen, PLAYER_COLOR, (SCREEN_WIDTH / 2 - 40, 480, 80, 80))

    draw_health_bar()

    button_rects = []
    button_height = 60
    button_width = SCREEN_WIDTH - 100
    start_y = 250
    for i, option in enumerate(crime["options"]):
        button_rect = pygame.Rect(50, start_y + i * (button_height + 15), button_width, button_height)
        button_rects.append(button_rect)
        
        pygame.draw.rect(screen, BLUE, button_rect, border_radius=10)
        pygame.draw.rect(screen, DARK_BLUE, button_rect, width=3, border_radius=10)
        
        draw_text(f"{i+1}. {option}", option_font, WHITE, screen, button_rect.centerx, button_rect.centery, center=True, max_width=button_width - 20)
        
    global feedback_timer
    if feedback_timer > 0:
        draw_text(feedback_message, feedback_font, feedback_color, screen, SCREEN_WIDTH/2, 220, center=True)
        if feedback_explanation:
            draw_text(feedback_explanation, explanation_font, LIGHT_GREY, screen, SCREEN_WIDTH/2, SCREEN_HEIGHT - 30, center=True, max_width=SCREEN_WIDTH - 100)
        feedback_timer -= 1
    
    return button_rects


def draw_health_bar():
    """Desenha a barra de vida do jogador."""
    draw_text("Sua Integridade:", option_font, WHITE, screen, 100, 500, center=True)
    pygame.draw.rect(screen, RED, (180, 490, max_player_health * 50, 20))
    if player_health > 0:
        pygame.draw.rect(screen, GREEN, (180, 490, player_health * 50, 20))

def draw_end_screen(message):
    """Desenha a tela de Game Over ou Vitória."""
    screen.fill(BACKGROUND_COLOR)
    color = GREEN if game_state == "victory" else RED
    draw_text(message, title_font, color, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50, center=True)
    draw_text("Clique para jogar novamente", option_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20, center=True)


def main():
    global game_state, player_health, current_crime_index, feedback_message, feedback_color, feedback_timer, feedback_explanation

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "playing":
                    if feedback_timer <= 0:
                        crime = crimes[current_crime_index]
                        for i, button_rect in enumerate(button_rects):
                            if button_rect.collidepoint(event.pos):
                                if i == crime["correct_option_index"]:
                                    feedback_message = "Correto!"
                                    feedback_color = GREEN
                                    feedback_explanation = ""
                                    feedback_timer = 90  # Frames (1.5s a 60fps)
                                    
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
                else: 
                    game_state = "playing"
                    player_health = max_player_health
                    current_crime_index = 0
                    feedback_timer = 0
        
        if game_state == "playing":
            button_rects = draw_game_state()
        elif game_state == "victory":
            draw_end_screen("VITÓRIA! Você protegeu o sistema!")
        elif game_state == "game_over":
            draw_end_screen("GAME OVER! O sistema foi comprometido.")

        pygame.display.flip()
        
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()