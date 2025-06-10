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

ASSETS_PATH = 'assets'

try:
    FONT_PATH = os.path.join(ASSETS_PATH, 'Minecraftia-Regular.ttf')
    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError
    title_font = pygame.font.Font(FONT_PATH, 40)
    option_font = pygame.font.Font(FONT_PATH, 13)
    feedback_font = pygame.font.Font(FONT_PATH, 32)
    explanation_font = pygame.font.Font(FONT_PATH, 18)
    menu_font = pygame.font.Font(FONT_PATH, 40)
    description_font = pygame.font.Font(FONT_PATH, 20)
    story_font = pygame.font.Font(FONT_PATH, 16)
    conclusion_font = pygame.font.Font(FONT_PATH, 13)

except FileNotFoundError:
    print(f"Erro: Fonte 'Minecraftia-Regular.ttf' não encontrada na pasta '{ASSETS_PATH}'!")
    print("Usando fontes padrão do Pygame.")
    title_font = pygame.font.Font(None, 65)
    option_font = pygame.font.Font(None, 24)
    feedback_font = pygame.font.Font(None, 48)
    explanation_font = pygame.font.Font(None, 28)
    menu_font = pygame.font.Font(None, 65)
    description_font = pygame.font.Font(None, 32)
    story_font = pygame.font.Font(None, 30)
    conclusion_font = pygame.font.Font(None, 30)


def scale_image_proportional_height(image, target_height):
    original_width, original_height = image.get_size()
    if original_height == 0: return image
    aspect_ratio = original_width / original_height
    target_width = int(target_height * aspect_ratio)
    return pygame.transform.scale(image, (target_width, target_height))

try:
    combate_bg = pygame.image.load(os.path.join(ASSETS_PATH, 'combate.png')).convert()
    combate_bg = pygame.transform.scale(combate_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    menu_image = pygame.image.load(os.path.join(ASSETS_PATH, 'menu.png')).convert()
    menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    vitoria_image = pygame.image.load(os.path.join(ASSETS_PATH, 'vitoria.png')).convert()
    vitoria_image = pygame.transform.scale(vitoria_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    derrota_image = pygame.image.load(os.path.join(ASSETS_PATH, 'derrota.png')).convert()
    derrota_image = pygame.transform.scale(derrota_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    introducao_bg = pygame.image.load(os.path.join(ASSETS_PATH, 'introducao.png')).convert()
    introducao_bg = pygame.transform.scale(introducao_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    historia_bg = pygame.image.load(os.path.join(ASSETS_PATH, 'historia.png')).convert()
    historia_bg = pygame.transform.scale(historia_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    conclusao_bg = pygame.image.load(os.path.join(ASSETS_PATH, 'conclusao.png')).convert()
    conclusao_bg = pygame.transform.scale(conclusao_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    PLAYER_TARGET_HEIGHT = SCREEN_HEIGHT * 0.30
    PLAYER_PORTRAIT_HEIGHT = SCREEN_HEIGHT * 0.65
    
    ENEMY_DOSSIER_HEIGHT = SCREEN_HEIGHT * 0.20
    ENEMY_COMBAT_HEIGHT = SCREEN_HEIGHT * 0.35

    player_image_combat = scale_image_proportional_height(pygame.image.load(os.path.join(ASSETS_PATH, 'personagem.png')).convert_alpha(), PLAYER_TARGET_HEIGHT)
    player_image_portrait = scale_image_proportional_height(pygame.image.load(os.path.join(ASSETS_PATH, 'personagem.png')).convert_alpha(), PLAYER_PORTRAIT_HEIGHT)

    
    enemy_filenames = [
        'phishing.png', 'malware.png', 'senha.png', 'ransomware.png', 'spyware.png',
        'adware.png', 'golpe.png', 'cyberstalking.png', 'pirataria.png', 'deepfake.png'
    ]
    
    dossier_enemy_images = []
    combat_enemy_images = []

    for filename in enemy_filenames:
        path = os.path.join(ASSETS_PATH, filename)
        original_image = pygame.image.load(path).convert_alpha()
        dossier_enemy_images.append(scale_image_proportional_height(original_image, ENEMY_DOSSIER_HEIGHT))
        combat_enemy_images.append(scale_image_proportional_height(original_image, ENEMY_COMBAT_HEIGHT))

except pygame.error as e:
    print(f"Erro ao carregar imagem: {e}")
    pygame.quit()
    sys.exit()

crimes = [
    {
        "enemy_name": "Ameaça de Phishing",
        "description": "Este inimigo envia e-mails e mensagens falsas, fingindo ser de empresas ou pessoas confiáveis, para tentar ROUBAR suas senhas e dados pessoais.",
        "options": ["Clicar no link para resgatar seu prêmio.", "Responder pedindo para confirmarem a identidade.", "Verificar o remetente e ignorar links suspeitos.", "Encaminhar o e-mail para um amigo ver."],
        "correct_option_index": 2,
        "explanation": "Interagir com o e-mail, mesmo que para questionar, confirma que seu endereço é ativo para os golpistas.",
        "correct_explanation": "Excelente! Desconfiar sempre é a melhor defesa. Verificar quem enviou e não clicar em nada suspeito mantém suas informações seguras."
    },
    {
        "enemy_name": "Ataque de Malware",
        "description": "Malware é um programa malicioso que se instala no seu dispositivo para danificá-lo ou roubar informações. Ele pode vir de downloads, anexos ou sites perigosos.",
        "options": ["Manter antivírus e sistema operacional atualizados.", "Instalar um 'limpador de PC' de um anúncio.", "Ignorar avisos de segurança do navegador.", "Conectar um pendrive achado na rua."],
        "correct_option_index": 0,
        "explanation": "Muitos malwares se disfarçam de programas úteis ou são espalhados por dispositivos físicos infectados.",
        "correct_explanation": "Perfeito! Manter tudo atualizado corrige falhas de segurança que os malwares usam para atacar."
    },
    {
        "enemy_name": "Invasão por Senha Fraca",
        "description": "Esta ameaça explora senhas fáceis de adivinhar (como '123456' ou 'senha') ou que você usa em vários lugares, facilitando a invasão de suas contas.",
        "options": ["Usar o nome do seu pet como senha.", "Usar a mesma senha forte em todos os sites.", "Salvar senhas no bloco de notas do PC.", "Criar senhas longas, fortes e únicas para cada serviço."],
        "correct_option_index": 3,
        "explanation": "Mesmo uma senha forte se torna inútil se for vazada e você a reutiliza em vários lugares.",
        "correct_explanation": "Isso mesmo! Senhas fortes e diferentes para cada site, junto com MFA, criam uma barreira muito mais difícil de ser quebrada."
    },
    {
        "enemy_name": "Sequestro por Ransomware",
        "description": "Este inimigo 'sequestra' seus arquivos, criptografando-os para que você não possa mais acessá-los. Depois, ele exige um pagamento de resgate para liberá-los.",
        "options": ["Formatar o PC e restaurar de um backup seguro.", "Pagar o resgate para garantir os arquivos de volta.", "Procurar um descriptografador em sites suspeitos.", "Negociar um valor menor com o criminoso."],
        "correct_option_index": 0,
        "explanation": "Pagar o resgate não garante a devolução dos arquivos e financia o crime. Descriptografadores falsos podem conter mais vírus.",
        "correct_explanation": "Ação inteligente! Ter um backup (cópia de segurança) dos seus arquivos importantes é a forma mais eficaz de se recuperar de um ataque de ransomware."
    },
    {
        "enemy_name": "Espionagem por Spyware",
        "description": "Este inimigo secreto observa suas atividades, coletando dados de navegação e senhas sem que você perceba.",
        "options": ["Aceitar todos os cookies de um site sem ler.", "Achar que o modo anônimo te deixa invisível.", "Usar software anti-spyware e ler as permissões dos apps.", "Instalar um app que pede acesso aos seus contatos."],
        "correct_option_index": 2,
        "explanation": "Muitos apps pedem permissões que não precisam para funcionar, coletando seus dados para vender a terceiros.",
        "correct_explanation": "Correto! Ferramentas de segurança e atenção ao que você instala são essenciais para manter os espiões longe."
    },
    {
        "enemy_name": "Inundação de Adware",
        "description": "Mais irritante do que perigoso, este inimigo inunda sua tela com anúncios e pop-ups indesejados, muitas vezes deixando seu dispositivo mais lento.",
        "options": ["Clicar em 'Fechar' em todos os pop-ups.", "Instalar um programa que promete acelerar seu PC.", "Ignorar e se acostumar com os anúncios.", "Usar um bloqueador de anúncios e verificar o que instala."],
        "correct_option_index": 3,
        "explanation": "Muitos programas que prometem melhorias de sistema, na verdade, instalam ainda mais adware e outros malwares.",
        "correct_explanation": "Exato! Um bom bloqueador de anúncios e cuidado com as instalações de programas mantêm seu navegador limpo."
    },
    {
        "enemy_name": "Golpe do Estelionato Eletrônico",
        "description": "Este vigarista usa de engenharia social para aplicar golpes, como o famoso golpe do 'parente pedindo dinheiro' ou falsas promoções.",
        "options": ["Fazer PIX para um amigo que pediu ajuda no WhatsApp.", "Fazer compras online usando um cartão virtual.", "Clicar em um link de emprego recebido por SMS.", "Confiar em um e-mail do 'banco' pedindo sua senha."],
        "correct_option_index": 1,
        "explanation": "Sempre confirme pedidos de dinheiro por uma ligação ou outro meio. Golpistas podem clonar contas de redes sociais.",
        "correct_explanation": "Perfeito! Cartões virtuais criam uma camada extra de segurança para suas compras online."
    },
    {
        "enemy_name": "Perseguição (Cyberstalking)",
        "description": "Este inimigo representa uma ameaça direta à sua paz e segurança, usando a internet para perseguir, ameaçar e assediar de forma obsessiva.",
        "options": ["Postar sua localização atual nas redes sociais.", "Bloquear o agressor e denunciar o perfil à plataforma.", "Manter o perfil aberto para mostrar que não tem medo.", "Discutir com o agressor nos comentários."],
        "correct_option_index": 1,
        "explanation": "Expor sua localização ou confrontar o agressor publicamente pode escalar o perigo.",
        "correct_explanation": "Ação correta e segura. Bloquear, denunciar e guardar as provas para as autoridades é o caminho certo a seguir."
    },
    {
        "enemy_name": "Pirataria de Software",
        "description": "Este ladrão digital copia e distribui ilegalmente softwares, jogos e mídias, violando direitos autorais e muitas vezes incluindo malwares nos arquivos.",
        "options": ["Comprar uma licença oficial do software.", "Usar um ativador para 'desbloquear' o programa.", "Baixar um filme de um site de torrents.", "Pedir a um amigo para copiar um jogo pago."],
        "correct_option_index": 0,
        "explanation": "Programas 'crackeadores' ou ativadores são uma porta de entrada comum para vírus e ransomware.",
        "correct_explanation": "Exatamente! Apoiar os desenvolvedores e garantir um software seguro e livre de vírus é sempre a melhor opção."
    },
    {
        "enemy_name": "Ameaça Deepfake",
        "description": "Usando inteligência artificial, este inimigo cria vídeos e áudios falsos, mas extremamente realistas, para espalhar desinformação ou aplicar golpes.",
        "options": ["Acreditar em um áudio de um familiar pedindo dinheiro.", "Confiar em um vídeo de uma celebridade endossando algo.", "Analisar inconsistências e buscar fontes confiáveis.", "Achar que é fácil identificar um vídeo falso."],
        "correct_option_index": 2,
        "explanation": "A tecnologia Deepfake está cada vez mais convincente, tornando difícil a identificação apenas 'no olho'.",
        "correct_explanation": "Perfeito! O pensamento crítico é a principal ferramenta contra deepfakes. Sempre duvide e verifique as fontes."
    }
]

game_story = """Em um mundo cada vez mais conectado, uma onda de crimes digitais ameaça a segurança de todos. Vírus, golpistas e ladrões de dados se espalham pela rede, causando o caos.
Mas um herói anônimo, conhecido apenas como o Guardião Digital, ergue-se para proteger os inocentes. Armado com seu conhecimento e seu fiel notebook, ele é a última linha de defesa.
Sua missão: Enfrentar e derrotar as 10 ameaças digitais para restaurar a paz e a segurança no ciberespaço."""


player_health = 3
max_player_health = 3
current_crime_index = 0
game_state = "menu"
feedback_active = False
last_answer_was_correct = False

def draw_text(text, font, color, surface, x, y, center=False, max_width=None):
    if max_width:
        paragraphs = text.split('\n')
        y_offset = 0
        for paragraph in paragraphs:
            words = paragraph.split(' ')
            lines = []
            current_line = ""
            for word in words:
                if font.size(current_line + " " + word)[0] <= max_width:
                    current_line += " " + word
                else:
                    lines.append(current_line.strip())
                    current_line = word
            lines.append(current_line.strip())
            
            for line in lines:
                text_surface = font.render(line, True, color)
                text_rect = text_surface.get_rect()
                if center:
                    text_rect.center = (x, y + y_offset)
                else:
                    text_rect.topleft = (x, y + y_offset)
                surface.blit(text_surface, text_rect)
                y_offset += font.get_height()
            y_offset += font.get_height()
    else:
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

def draw_story_screen():
    screen.blit(historia_bg, (0, 0))
    portrait_rect = player_image_portrait.get_rect(center=(SCREEN_WIDTH * 0.18, SCREEN_HEIGHT / 2))
    screen.blit(player_image_portrait, portrait_rect)
    draw_text(game_story, story_font, BLACK, screen, SCREEN_WIDTH * 0.68, SCREEN_HEIGHT * 0.35, center=True, max_width=SCREEN_WIDTH * 0.45)
    draw_text("Clique ou Pressione Enter para continuar...", explanation_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20, center=True)


def draw_introduction_screen():
    screen.blit(introducao_bg, (0, 0))
    crime = crimes[current_crime_index]
    draw_text(crime["enemy_name"], title_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.40, center=True)
    enemy_image = dossier_enemy_images[current_crime_index]
    enemy_rect = enemy_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.55))
    screen.blit(enemy_image, enemy_rect)
    draw_text(crime["description"], description_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.72, center=True, max_width=SCREEN_WIDTH * 0.6)
    draw_text("Clique para continuar...", explanation_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, center=True)

def draw_game_state():
    screen.blit(combate_bg, (0, 0))
    enemy_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.30)
    player_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.55)
    current_enemy_image = combat_enemy_images[current_crime_index]
    enemy_rect = current_enemy_image.get_rect(center=enemy_pos)
    screen.blit(current_enemy_image, enemy_rect)
    player_rect = player_image_combat.get_rect(center=player_pos)
    screen.blit(player_image_combat, player_rect)
    crime = crimes[current_crime_index]
    draw_text(crime["enemy_name"], title_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.12, center=True)
    draw_health_bar()
    button_rects = [pygame.Rect(80, 560, 515, 60), pygame.Rect(685, 560, 515, 60), pygame.Rect(80, 635, 515, 60), pygame.Rect(685, 635, 515, 60)]
    for i, option in enumerate(crime["options"]):
        current_button_rect = button_rects[i]
        draw_text(option, option_font, BUTTON_TEXT_COLOR, screen, current_button_rect.centerx, current_button_rect.centery, center=True)
    if feedback_active:
        draw_feedback_overlay(last_answer_was_correct)
    return button_rects

def draw_feedback_overlay(was_correct):
    crime = crimes[current_crime_index]
    overlay_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    if was_correct:
        overlay_surf.fill((0, 100, 0, 180))
        message = "Ação Correta!"
        explanation = crime["correct_explanation"]
    else:
        overlay_surf.fill((100, 0, 0, 180))
        message = "Ação Incorreta!"
        explanation = crime["explanation"]

    screen.blit(overlay_surf, (0, 0))
    
    draw_text(message, title_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.3, center=True)
    draw_text(explanation, description_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.5, center=True, max_width=SCREEN_WIDTH - 300)
    draw_text("Clique para continuar...", explanation_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40, center=True)

def draw_health_bar():
    text_x = 80
    text_y = 30
    bar_x = 140
    bar_y = 20
    segment_width = 45
    segment_height = 20
    draw_text("Integridade:", option_font, WHITE, screen, text_x, text_y, center=True)
    pygame.draw.rect(screen, RED, (bar_x, bar_y, max_player_health * segment_width, segment_height))
    if player_health > 0:
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, player_health * segment_width, segment_height))

def draw_end_screen():
    if game_state == "victory":
        screen.blit(vitoria_image, (0, 0))
    elif game_state == "game_over":
        screen.blit(derrota_image, (0, 0))

def draw_conclusion_screen():
    screen.blit(conclusao_bg, (0, 0))
    title_text = "Missão Cumprida, Guardião Digital!"
    draw_text(title_text, title_font, GREEN, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.2, center=True)
    conclusion_text = """Você derrotou todas as ameaças e tornou a internet mais segura! Lembre-se sempre das lições que aprendeu:
    - Use senhas fortes e ative a autenticação de múltiplos fatores (MFA).
    - Desconfie de e-mails, mensagens e links suspeitos.
    - Mantenha seus aplicativos e sistema operacional sempre atualizados.
    - Converse com amigos e familiares sobre os riscos da internet.
    A segurança digital é uma responsabilidade de todos!"""

    draw_text(conclusion_text, conclusion_font, BLACK, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.3, center=True, max_width=SCREEN_WIDTH * 0.8)
    draw_text("Clique para comemorar sua vitória...", explanation_font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, center=True)

def main():

    global game_state, player_health, current_crime_index, feedback_active, last_answer_was_correct, screen, fullscreen
    
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
                    if fullscreen: screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else: screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

            if game_state == "menu":
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or (event.type == pygame.MOUSEBUTTONDOWN):
                    game_state = "story"
            
            elif game_state == "story":
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or (event.type == pygame.MOUSEBUTTONDOWN):
                    game_state = "introduction"

            elif game_state == "introduction":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "playing"

            elif game_state == "playing":
                if feedback_active:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        feedback_active = False
                        if last_answer_was_correct:
                            current_crime_index += 1
                            if current_crime_index >= len(crimes):
                                game_state = "conclusion"
                            else:
                                game_state = "introduction"
                        else:
                            if player_health <= 0:
                                game_state = "game_over"
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        crime = crimes[current_crime_index]
                        for i, button_rect in enumerate(button_rects):
                            if button_rect.collidepoint(event.pos):
                                if i == crime["correct_option_index"]:
                                    last_answer_was_correct = True
                                else:
                                    last_answer_was_correct = False
                                    player_health -= 1
                                feedback_active = True
            
            elif game_state == "conclusion":
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    game_state = "victory"

            elif game_state in ["victory", "game_over"]:
                 if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    game_state = "menu" 
                    player_health = max_player_health
                    current_crime_index = 0
                    feedback_active = False

        if game_state == "menu":
            draw_menu_screen()
        elif game_state == "story":
            draw_story_screen()
        elif game_state == "introduction":
            draw_introduction_screen()
        elif game_state == "playing":
            button_rects = draw_game_state()
        elif game_state == "conclusion":
            draw_conclusion_screen()
        elif game_state in ["victory", "game_over"]:
            draw_end_screen()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()