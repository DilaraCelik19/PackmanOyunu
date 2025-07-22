import pygame
import subprocess  # subprocess kullanarak user.py'yi çalıştıracağız
from anamenu import display_menu  # Menü fonksiyonu

# Pygame başlat
pygame.init()

# Ekran boyutları
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Ana menüyü görüntüle ve kullanıcının seçtiği modu al
mode = display_menu(screen, screen_width, screen_height)
print(f"Seçilen Mod: {mode}")  # Debug çıktısı

# Kullanıcı seçimine göre mod başlat
if mode == "user":
    print("User mode başlatılıyor...")  # Debug çıktısı
    subprocess.run(["python", "user.py"])  # user.py dosyasını çalıştır
elif mode == "ai":
    print("Ai mode başlatılıyor...")  # Debug çıktısı
    subprocess.run(["python", "ai.py"])  # ai.py dosyasını çalıştır
