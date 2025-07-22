import pygame


def display_menu(screen, screen_width, screen_height):
    menu_screen = True
    while menu_screen:
        screen.fill((0, 0, 0))  # Ekranı siyah ile dolduruyoruz
        font = pygame.font.Font(None, 74)  # Yazı fontunu ayarlıyoruz

        # Bilgilendirme yazısı
        info_text = font.render("User mod için 1'i seçin", True, (255, 255, 255))  # User mode bilgilendirmesi
        info_text2 = font.render("AI mod için 2'yi seçin", True, (255, 255, 255))  # AI mode bilgilendirmesi

        # Seçenekler yazıları
        user_text = font.render("1. User Mode", True, (255, 255, 255))  # User Mode yazısı
        ai_text = font.render("2. AI Mode", True, (255, 255, 255))  # AI Mode yazısı

        # Yazıları ekrana yerleştir
        screen.blit(info_text, (screen_width // 4, screen_height // 5))  # User mode bilgilendirmesi
        screen.blit(info_text2, (screen_width // 4, screen_height // 3))  # AI mode bilgilendirmesi
        screen.blit(user_text, (screen_width // 4, screen_height // 2))  # User mode seçeneği
        screen.blit(ai_text, (screen_width // 4, screen_height // 1.5))  # AI mode seçeneği

        pygame.display.flip()  # Ekranı güncelle

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # 1 tuşuna basıldığında
                    return "user"
                if event.key == pygame.K_2:  # 2 tuşuna basıldığında
                    return "ai"


