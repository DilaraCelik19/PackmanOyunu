import pygame
import random

# Pygame başlat
pygame.init()

# Yeni labirent
maze = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "######.##          ##.######",
    "######.## ###--### ##.######",
    "######.## #      # ##.######",
    "       ## #      # ##       ",
    "######.## #      # ##.######",
    "######.## ######## ##.######",
    "######.##          ##.######",
    "######.## ######## ##.######",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#o..##................##..o#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

# Labirent hücre boyutu
cell_size = 20  # Daha büyük bir labirent olduğu için boyut küçültüldü
maze_width = len(maze[0]) * cell_size
maze_height = len(maze) * cell_size

# Ekran boyutları
screen_width = maze_width
screen_height = maze_height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pac-Man")

# Tüm geçerli (boş) pozisyonları belirle
#bir 2D labirent (maze) matrisindeki tüm geçerli (boş) pozisyonları belirlemek için kullanılır.
# Bu pozisyonlar, duvar olmayan hücrelerdir
valid_positions = [
    #row_index: Her satırın indeksini temsil eder.
    #row: O satırdaki tüm hücreleri temsil eder.
    (col_index * cell_size, row_index * cell_size)
    for row_index, row in enumerate(maze)
    for col_index, cell in enumerate(row)
    if cell != "#"  # Geçerli hücreler (boş alanlar)
    #Bu koşul, yalnızca hücre duvar değilse
    # (yani "#" sembolü içermiyorsa) o hücreyi geçerli pozisyon olarak kabul eder:
]

# Pac-Man başlangıç konumu rastgele
pacman_x, pacman_y = random.choice(valid_positions)
speed = 5

# Hayalet verileri (rastgele başlangıç)
ghosts = [
    {"x": random.choice(valid_positions)[0], "y": random.choice(valid_positions)[1], "color": (255, 0, 0), "dir": "RIGHT"},  # Kırmızı hayalet
    {"x": random.choice(valid_positions)[0], "y": random.choice(valid_positions)[1], "color": (0, 255, 0), "dir": "DOWN"},  # Yeşil hayalet
    {"x": random.choice(valid_positions)[0], "y": random.choice(valid_positions)[1], "color": (0, 0, 255), "dir": "LEFT"},  # Mavi hayalet
    {"x": random.choice(valid_positions)[0], "y": random.choice(valid_positions)[1], "color": (255, 165, 0), "dir": "UP"},  # Turuncu hayalet
]
ghost_speed = 2

# Yem verileri
#pellets adında bir liste oluşturuluyor.
# Bu liste, for döngüsü ve koşullarla bir list comprehension kullanılarak oluşturulmuş.
pellets = [
    #X koordinatı. Sütun indeksine bağlı olarak hesaplanır ve hücrenin merkezine yerleştirilir.
    #Y koordinatı. Satır indeksine bağlı olarak hesaplanır ve hücrenin merkezine yerleştirilir.
    (col_index * cell_size + cell_size // 2, row_index * cell_size + cell_size // 2)
    for row_index, row in enumerate(maze)
    for col_index, cell in enumerate(row)
    if cell == "." or cell == "o"
]

# Pac-Man'in can sayısı ve skor
lives = 3
score = 0  # Başlangıç skoru

# Çarpışma sayacı
collision_count = 0

# Zamanlayıcı
clock = pygame.time.Clock()

# Çarpışma kontrol fonksiyonu
def can_move(new_x, new_y):
    col = new_x // cell_size
    row = new_y // cell_size
    #Bu kontrol, row ve col değerlerinin labirent sınırları içinde olup olmadığını kontrol eder:
    if 0 <= row < len(maze) and 0 <= col < len(maze[0]):  # Labirent sınırları içinde mi?
        if maze[row][col] != "#":  # Duvar değilse hareket edebilir
            return True
    return False  # Geçersiz hareket

# Hayaletlerin düzgün hareket etmesini sağlayan fonksiyon
#Hayaletin şu anda hareket ettiği yön (ghost["dir"]) kontrol edilir.
#Örneğin, eğer "UP" yönünde hareket ediyorsa, hayaletin yukarıya doğru ilerleyip ilerleyemeyeceği kontrol edilir.
#Eğer hedef pozisyon (new_x veya new_y) geçerliyse (can_move fonksiyonundan True dönerse), hayalet bu yöne hareket eder.
#Eğer hareket edemiyorsa, rastgele bir başka yön seçilir (random.choice).
def move_ghost(ghost):
    if ghost["dir"] == "UP":
        new_y = ghost["y"] - ghost_speed
        if can_move(ghost["x"], new_y):
            ghost["y"] = new_y
        else:
            ghost["dir"] = random.choice(["DOWN", "LEFT", "RIGHT"])
    elif ghost["dir"] == "DOWN":
        new_y = ghost["y"] + ghost_speed
        if can_move(ghost["x"], new_y):
            ghost["y"] = new_y
        else:
            ghost["dir"] = random.choice(["UP", "LEFT", "RIGHT"])
    elif ghost["dir"] == "LEFT":
        new_x = ghost["x"] - ghost_speed
        if can_move(new_x, ghost["y"]):
            ghost["x"] = new_x
        else:
            ghost["dir"] = random.choice(["UP", "DOWN", "RIGHT"])
    elif ghost["dir"] == "RIGHT":
        new_x = ghost["x"] + ghost_speed
        if can_move(new_x, ghost["y"]):
            ghost["x"] = new_x
        else:
            ghost["dir"] = random.choice(["UP", "DOWN", "LEFT"])

# Hayaletlerin sadece siyah yol boyunca hareket etmesini sağlama
def can_move_on_path(new_x, new_y):
    col = new_x // cell_size
    row = new_y // cell_size
    if 0 <= row < len(maze) and 0 <= col < len(maze[0]):
        # Labirentten dışarı çıkmaması ve mavi alana geçmemesi için
        if maze[row][col] != "#" and maze[row][col] != ".":
            return True
    return False

collision_timer = 0  # Çarpışma sonrası bekleme süresi

def check_collision():
    global lives, collision_count, collision_timer
    if collision_timer > 0:
        collision_timer -= 1
        return False  # Bekleme süresince çarpışmayı algılama
#Hayaletler ve Pac-Man arasındaki mesafe kontrol edilir.
#Eğer mesafe çarpışma sınırı (cell_size // 2) içindeyse, çarpışma algılanır.
    for ghost in ghosts:
        if abs(ghost["x"] - pacman_x) < cell_size // 2 and abs(ghost["y"] - pacman_y) < cell_size // 2:
            collision_count += 1
            if collision_count <= 3:
                lives -= 1
            collision_timer = 60  # 1 saniyelik bekleme (fps'e bağlı)
            return True
    return False


# Yem toplama kontrolü
def check_pellet_collision():
    global pellets, score
    for pellet in pellets:
        #pellets listesi içinde her yem (pellet) Pac-Man'in konumuna göre kontrol edilir.
        #Eğer Pac-Man'in merkezi ile yem arasındaki yatay ve dikey mesafe, bir hücrenin yarısından küçükse (cell_size // 2),
        # Pac-Man o yemi yemiş kabul edilir.
        if abs(pacman_x + cell_size // 2 - pellet[0]) < cell_size // 2 and abs(pacman_y + cell_size // 2 - pellet[1]) < cell_size // 2:
        #Çarpışma algılandığında, ilgili yem pellets listesinden kaldırılır (pellets.remove(pellet)).
        #Bu, yemin haritadan kaybolmasını sağlar.
            pellets.remove(pellet)
        #Yem yendiğinde, score değeri 10 artırılır.
            score += 10
            return True
    return False

# Ana oyun döngüsü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hayaletlerin hareket etmesi
    for ghost in ghosts:
        move_ghost(ghost)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        new_y = pacman_y - speed
        if can_move(pacman_x, new_y):
            pacman_y = new_y
    if keys[pygame.K_DOWN]:
        new_y = pacman_y + speed
        if can_move(pacman_x, new_y + cell_size - 1):
            pacman_y = new_y
    if keys[pygame.K_LEFT]:
        new_x = pacman_x - speed
        if can_move(new_x, pacman_y):
            pacman_x = new_x
    if keys[pygame.K_RIGHT]:
        new_x = pacman_x + speed
        if can_move(new_x + cell_size - 1, pacman_y):
            pacman_x = new_x

    # Çarpışma kontrolü
    if check_collision():
        if collision_count == 3:
            print(f"Oyun Bitti! Toplam Skor: {score}")
            running = False

    check_pellet_collision()
    screen.fill((0, 0, 0))

    # Labirenti çiz
    for row_index, row in enumerate(maze):
        for col_index, cell in enumerate(row):
            if cell == "#":
                #Eğer hücre duvarı temsil ediyorsa ("#"), bu hücre ekrana bir mavi kare olarak çizilir.
                pygame.draw.rect(
                    screen,
                    (0, 0, 255),
                    pygame.Rect(
                        col_index * cell_size,
                        row_index * cell_size,
                        cell_size,
                        cell_size
                    )
                )
#Pac-Man karakterini bir sarı daire olarak çizer.

#screen -> Çizimin yapılacağı yüzey.
    pygame.draw.circle(
        screen,
        (255, 255, 0),
        (pacman_x + cell_size // 2, pacman_y + cell_size // 2),
        cell_size // 3
    )

    for ghost in ghosts:
        pygame.draw.circle(
            screen,
            ghost["color"],
            (ghost["x"] + cell_size // 2, ghost["y"] + cell_size // 2),
            cell_size // 3
        )
#for pellet in pellets:
#pellets isimli listeyi dolaşır. Bu liste, her bir yem için merkez koordinatlarını (x, y) içerir.
    for pellet in pellets:
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            pellet,
            cell_size // 6
        )
#Metin, oyuncunun kalan canlarını ve skorunu ekrana yazdırmak için hazırlanır.


    font = pygame.font.Font(None, 36)
    text = font.render(f'Canlar: {lives}  Skor: {score}', True, (255, 255, 255))
    screen.blit(text, (10, 10))
#Pygame ekranını günceller.
    pygame.display.flip()
    #Oyunun sabit bir hızda çalışmasını sağlar. Daha yüksek FPS daha akıcı bir oyun deneyimi sunar.
    clock.tick(60)

pygame.quit()



