import pygame
import random
import math

# Pygame Initialization
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Utility-Based Pac-Man")

# Clock for Controlling Frame Rate
clock = pygame.time.Clock()
FPS = 10
#10 değeri, oyun döngüsünün saniyede 10 kez çalışacağını ifade eder.

class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = RIGHT
        self.score = 0
        self.lives = 3
#Bu fonksiyon, bir oyun nesnesinin (örneğin, bir hayalet ya da Pac-Man) oyun alanında hareketini kontrol etmek için yazılmıştır.
# Kod, nesnenin yeni bir pozisyona geçmeden önce çarpışma kontrolleri yapmasını ve sınırları aşmasını engellemeyi amaçlar.
    def move(self):
        # Bir hücrenin piksel cinsinden boyutudur. Hareket her seferinde bir hücre kadar olur.
        new_x = self.x + self.direction[0] * CELL_SIZE
        new_y = self.y + self.direction[1] * CELL_SIZE

        # Check for wall collisions within the labyrinth boundaries
        #Yeni koordinatlar labirent matrisindeki hücrelere dönüştürülür.
        # Bu, hangi hücreye girileceğini belirlemek içindir.
        new_x_index = new_x // CELL_SIZE
        new_y_index = new_y // CELL_SIZE

        # Ensure new coordinates are within labyrinth bounds
        if 0 <= new_x_index < len(game.labyrinth[0]) and 0 <= new_y_index < len(game.labyrinth):

            if game.labyrinth[new_y_index][new_x_index] != 1:
                #Yeni pozisyon bir duvar değilse (!= 1), hareket gerçekleştirilir.
                self.x = new_x % WIDTH
                self.y = new_y % HEIGHT
            else:
                # Wall collision: Change direction to avoid getting stuck
                self.set_random_direction()
        else:
            # Out of bounds: Change direction
            self.set_random_direction()

    def set_direction(self, direction):
        self.direction = direction

    def get_position(self):
        return self.x, self.y

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = color

    def move(self):
        new_x = self.x + self.direction[0] * CELL_SIZE
        new_y = self.y + self.direction[1] * CELL_SIZE

        # Labirent sınırlarını kontrol et
        new_x_index = new_x // CELL_SIZE
        new_y_index = new_y // CELL_SIZE

        # Eğer yeni pozisyon labirent sınırları dışındaysa, hareket etmeye devam etme
        if 0 <= new_x_index < len(game.labyrinth[0]) and 0 <= new_y_index < len(game.labyrinth):
            # Eğer yeni pozisyon duvar değilse, hayalet hareket edebilir
            if game.labyrinth[new_y_index][new_x_index] != 1:
                self.x = new_x % WIDTH
                self.y = new_y % HEIGHT
            else:
                self.set_random_direction()  # Duvara çarptığında yön değiştir
        else:
            self.set_random_direction()  # Sınır dışına çıktığında yön değiştir

    def set_random_direction(self):
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def get_position(self):
        return self.x, self.y

class Game:
    def __init__(self):
        self.labyrinth = self.create_labyrinth()
        self.pacman = PacMan(14 * CELL_SIZE, 17 * CELL_SIZE)  # Pac-Man starts in the middle of the maze
        self.foods = self.generate_food()
        self.ghosts = self.generate_ghosts(4)  # 4 ghosts

    def create_labyrinth(self):
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

        labyrinth = []
        for row in maze:
            labyrinth.append([1 if cell == "#" else 0 for cell in row])
        return labyrinth

    def generate_food(self):
        foods = []
        for y, row in enumerate(self.labyrinth):
            for x, cell in enumerate(row):
                if cell == 0:  # Place food at all empty cells
                    foods.append(Food(x * CELL_SIZE, y * CELL_SIZE))
        return foods

    def generate_ghosts(self, count):
        ghosts = []
        colors = [RED, GREEN, CYAN, MAGENTA]
        empty_cells = [(x, y) for y, row in enumerate(self.labyrinth) for x, cell in enumerate(row) if cell == 0]
        for i in range(count):
            x, y = random.choice(empty_cells)
            ghosts.append(Ghost(x * CELL_SIZE, y * CELL_SIZE, colors[i % len(colors)]))
        return ghosts

    def draw(self):
        screen.fill(BLUE)  # Set background color to blue

        # Draw Labyrinth
        for y in range(len(self.labyrinth)):
            for x in range(len(self.labyrinth[0])):
                if self.labyrinth[y][x] == 1:
                    pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw Pac-Man
        pygame.draw.circle(screen, YELLOW, (self.pacman.x + CELL_SIZE // 2, self.pacman.y + CELL_SIZE // 2), CELL_SIZE // 2)

        # Draw Food
        for food in self.foods:
            pygame.draw.circle(screen, WHITE, (food.x + CELL_SIZE // 2, food.y + CELL_SIZE // 2), 4)  # Food as white dots

        # Draw Ghosts
        for ghost in self.ghosts:
            pygame.draw.rect(screen, ghost.color, (ghost.x, ghost.y, CELL_SIZE, CELL_SIZE))

        # Display Score and Lives
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.pacman.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.pacman.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

    def update(self):
        self.choose_next_move()
        self.pacman.move()

        # Check Food Collision
        pacman_pos = self.pacman.get_position()
        for food in self.foods[:]:
            if pacman_pos == food.get_position():
                self.foods.remove(food)
                self.pacman.score += 10

        # Move Ghosts
        for ghost in self.ghosts:
            ghost.move()

        # Check Ghost Collision
        for ghost in self.ghosts:
            if pacman_pos == ghost.get_position():
                self.pacman.lives -= 1
                if self.pacman.lives <= 0:
                    print(f"Game Over! Your Score: {self.pacman.score}")
                    pygame.quit()
                    exit()

    def is_game_over(self):
        return len(self.foods) == 0

    def utility_function(self, direction):
        new_x = (self.pacman.x + direction[0] * CELL_SIZE) % WIDTH
        new_y = (self.pacman.y + direction[1] * CELL_SIZE) % HEIGHT
#Bu satır, yeni pozisyonda bir duvar olup olmadığını kontrol eder.
        if self.labyrinth[new_y // CELL_SIZE][new_x // CELL_SIZE] == 1:
            return -float('inf')  # Penalize hitting a wall

        distance_to_food = [
            math.sqrt((new_x - food.x) ** 2 + (new_y - food.y) ** 2) for food in self.foods
        ]
        return -min(distance_to_food) if distance_to_food else 0  # Minimize distance to closest food

    def choose_next_move(self):
        best_utility = -float('inf')
        best_direction = self.pacman.direction

        for direction in [UP, DOWN, LEFT, RIGHT]:
            utility = self.utility_function(direction)
            if utility > best_utility:
                best_utility = utility
                best_direction = direction

        self.pacman.set_direction(best_direction)

def main():
    global game
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game.is_game_over():
            game.update()

        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()


