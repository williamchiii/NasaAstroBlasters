import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Shooting Game')  # Set a caption for the window
image = pygame.image.load('background.png')
icon = pygame.image.load('playerImage.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Load and scale images
playerImg = pygame.image.load('playerImage.png')
player_image = pygame.transform.scale(playerImg, (100, 100))
enemyImg = pygame.image.load('Asteroid.png')  # Load enemy image once
image = pygame.transform.scale(image, (1280, 720))  # Scale background image

# Bullet class to handle shooting
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))  # Bullet dimensions (width, height)
        self.image.fill((255, 0, 0))  # Bullet color (red)
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)  # Start bullet at the top-middle of the player
        self.speed = -10  # Speed of the bullet (moving up)

    def update(self):
        # Move the bullet upward
        self.rect.y += self.speed
        # Remove the bullet if it goes off-screen
        if self.rect.bottom < 0:
            self.kill()

# Group to store bullets
bullet_group = pygame.sprite.Group()

# Enemy management
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(enemyImg, (100, 100))  # Scale enemy image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4

    def update(self):
        # Move enemy down the screen
        self.rect.y += self.speed
        # Reset enemy position if it moves off the bottom
        if self.rect.top > 720:
            self.rect.x = random.randint(0, 1180)  # Reset to random x position
            self.rect.y = random.randint(-150, -100)  # Reset to random y position above the screen

# Create enemy group and add enemies
enemy_group = pygame.sprite.Group()
num_of_enemies = 6
for _ in range(num_of_enemies):
    enemy_x = random.randint(0, 1180)  # Random x position
    enemy_y = random.randint(-150, -100)  # Random y position above the screen
    enemy = Enemy(enemy_x, enemy_y)
    enemy_group.add(enemy)

# Player management
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(playerImg, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (370, 380)  # Starting position
        self.speed = 10

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 1280:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 720:
            self.rect.y += self.speed

# Create a player instance and player group
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

# Initialize score, lives, and font
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# Quit button properties
quit_button_color = (255, 0, 0)
quit_button_hover_color = (200, 0, 0)
quit_button_rect = pygame.Rect(1180, 10, 90, 40)  # Position of the quit button (top-right corner)

# Function to display score and lives
def display_score_lives():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

# Function to display Quit button
def display_quit_button():
    mouse_pos = pygame.mouse.get_pos()
    if quit_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, quit_button_hover_color, quit_button_rect)
    else:
        pygame.draw.rect(screen, quit_button_color, quit_button_rect)
    quit_text = font.render("Quit", True, (255, 255, 255))
    screen.blit(quit_text, (quit_button_rect.x + 20, quit_button_rect.y + 5))

# Function to display Game Over screen with Restart and Quit options
def game_over_screen():
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(game_over_text, (540, 300))
    screen.blit(restart_text, (430, 400))

# Reset game state function
def reset_game():
    global score, lives, enemy_group
    score = 0
    lives = 3
    enemy_group.empty()
    for _ in range(num_of_enemies):
        enemy_x = random.randint(0, 1180)  # Random x position
        enemy_y = random.randint(-150, -100)  # Random y position above the screen
        enemy = Enemy(enemy_x, enemy_y)
        enemy_group.add(enemy)

# Game loop
running = True
game_over = False
last_shot_time = 0  # Time of the last shot
shooting_cooldown = 1000  # 1000 milliseconds = 1 second

while running:
    clock.tick(60)  # Limit to 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button_rect.collidepoint(event.pos):
                running = False  # Quit the game when the button is clicked

    if not game_over:
        # Get the keys pressed
        keys = pygame.key.get_pressed()

        # Update player position
        player.update(keys)

        # Shoot bullets with spacebar
        current_time = pygame.time.get_ticks()

        if keys[pygame.K_SPACE] and (current_time - last_shot_time) >= shooting_cooldown:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullet_group.add(bullet)
            last_shot_time = current_time  # Update the last shot time

        # Update bullet and enemy positions
        bullet_group.update()
        enemy_group.update()

        # Check for bullet-enemy collisions
        collisions = pygame.sprite.groupcollide(bullet_group, enemy_group, True, False)
        for bullet, enemies in collisions.items():
            for enemy in enemies:
                # Increase score by 1 for each hit
                score += 1
                # Reset enemy position after hit
                enemy.rect.x = random.randint(0, 1180)  # Reset to random x position
                enemy.rect.y = random.randint(-150, -100)  # Reset to random y position above the screen

        # Check for player-enemy collisions
        if pygame.sprite.spritecollideany(player, enemy_group):
            lives -= 1
            if lives == 0:
                game_over = True  # Trigger game over
            else:
                # Reset enemy positions when hit
                for enemy in enemy_group:
                    enemy.rect.x = random.randint(0, 1180)
                    enemy.rect.y = random.randint(-150, -100)

        # Draw background, player, bullets, enemies, and display score/lives
        screen.blit(image, (0, 0))
        player_group.draw(screen)
        bullet_group.draw(screen)
        enemy_group.draw(screen)
        display_score_lives()

        # Display the quit button
        display_quit_button()

    else:
        # Display Game Over screen
        game_over_screen()

        # Handle restart or quit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Restart the game
            reset_game()
            game_over = False
        if keys[pygame.K_q]:  # Quit the game
            running = False

    # Update the display
    pygame.display.flip()

pygame.quit()
