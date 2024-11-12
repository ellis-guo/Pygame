import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Game area dimensions (inside border)
GAME_WIDTH, GAME_HEIGHT = 600, 400

# Additional space for text display
TOP_MARGIN = 50  # Space for score at top
SIDE_MARGIN = 20  # Space on sides
BOTTOM_MARGIN = 50  # Space at bottom

# Total window size including margins
WIDTH = GAME_WIDTH + (2 * SIDE_MARGIN)  # Add margins to sides
HEIGHT = GAME_HEIGHT + TOP_MARGIN + BOTTOM_MARGIN  # Add top and bottom margins

# Create window with extra space for text
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

# Define colors (RGB format)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
ORANGE = (255, 165, 0)
BLUE = (31, 64, 237)

# Game constants
SNAKE_SIZE = 20
BORDER_THICKNESS = 10
FPS = 10  # Base game speed

class SnakeGame:
    # A class that make our game more easier to navigate and maintain
    # and make it easier to reuse and add new features or modify existing ones.
    def __init__(self):
        self.snake_color = BLUE
        self.bg_color = BLACK
        self.mute = False
        self.font = pygame.font.SysFont('arial', 28)
        self.small_font = pygame.font.SysFont('arial', 20)
        self.clock = pygame.time.Clock()
        self.load_assets()
        
        # Add some color to food
        self.food_color = [255, 0, 0]
        self.color_direction = 1
        self.food_size = SNAKE_SIZE
        self.size_direction = 1
    
    def draw_snake(self, snake_body):
        # Beautified the graphics of the snake
        SNAKE_HEAD_COLOR = (31, 64, 238)
        SNAKE_TAIL_COLOR = (0, 128, 128)
        
        for index, pos in enumerate(snake_body):
            color_ratio = index / len(snake_body)
            #  Make the color of the snake's head and tail changes with its length
            segment_color = (
                int(SNAKE_HEAD_COLOR[0] * (1 - color_ratio) + SNAKE_TAIL_COLOR[0] * color_ratio),
                int(SNAKE_HEAD_COLOR[1] * (1 - color_ratio) + SNAKE_TAIL_COLOR[1] * color_ratio),
                int(SNAKE_HEAD_COLOR[2] * (1 - color_ratio) + SNAKE_TAIL_COLOR[2] * color_ratio)
            )
            segment_rect = pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE)
            pygame.draw.rect(window, segment_color, segment_rect, border_radius=8)

        
    def load_assets(self):
        """Load dynamic background and music with error handling"""
        try:
            if os.path.exists("background_music.mp3"):
                pygame.mixer.music.load("background_music.mp3")
                pygame.mixer.music.play(-1)
            else:
                print("Warning: background_music.mp3 not found")
                
            if os.path.exists("background_image.jpg"):
                self.background_image = pygame.image.load("background_image.jpg")
                self.background_image = pygame.transform.scale(
                    self.background_image, 
                    (GAME_WIDTH - 2*BORDER_THICKNESS, 
                     GAME_HEIGHT - 2*BORDER_THICKNESS)
                )
            else:
                print("Warning: background_image.jpg not found")
                self.background_image = None
        except pygame.error as e:
            print(f"Error loading assets: {e}")
            self.background_image = None

    def show_message(self, text, color, pos):
        """Display a message on the screen."""
        message = self.font.render(text, True, color)
        message_rect = message.get_rect(center=pos)
        window.blit(message, message_rect)

    def draw_border(self):
        """Draw border around the game area."""
        # Game area starts after TOP_MARGIN
        game_rect = pygame.Rect(
            SIDE_MARGIN, 
            TOP_MARGIN, 
            GAME_WIDTH, 
            GAME_HEIGHT
        )
        pygame.draw.rect(window, WHITE, game_rect, BORDER_THICKNESS)

    def generate_food_position(self, snake_body):
        """Generate new food position ensuring it doesn't overlap with snake"""
        while True:
            food_pos = [
                random.randrange(SIDE_MARGIN + BORDER_THICKNESS, 
                               SIDE_MARGIN + GAME_WIDTH - BORDER_THICKNESS - SNAKE_SIZE, 
                               SNAKE_SIZE),
                random.randrange(TOP_MARGIN + BORDER_THICKNESS, 
                               TOP_MARGIN + GAME_HEIGHT - BORDER_THICKNESS - SNAKE_SIZE, 
                               SNAKE_SIZE)
            ]
            # Ensures food does not spawn on the snake body
            if food_pos not in snake_body:
                return food_pos

    def handle_input(self, event, direction):
        """Handle keyboard input"""
        if event.type == pygame.KEYDOWN:
            key_direction = {
                pygame.K_UP: ('UP', 'DOWN'),
                pygame.K_DOWN: ('DOWN', 'UP'),
                pygame.K_LEFT: ('LEFT', 'RIGHT'),
                pygame.K_RIGHT: ('RIGHT', 'LEFT')
            }
            
            if event.key in key_direction:
                new_dir, opposite = key_direction[event.key]
                if direction != opposite:
                    return new_dir
            elif event.key == pygame.K_m:
                self.toggle_mute()
                
        return direction

    def toggle_mute(self):
        """Toggle music mute state"""
        self.mute = not self.mute
        pygame.mixer.music.set_volume(0 if self.mute else 1)

    def check_collision(self, snake_pos):
        """Check if snake has collided with walls or itself"""
        # Wall collision - adjusted for new game area position
        if (snake_pos[0] < SIDE_MARGIN + BORDER_THICKNESS or 
            snake_pos[0] >= SIDE_MARGIN + GAME_WIDTH - BORDER_THICKNESS or
            snake_pos[1] < TOP_MARGIN + BORDER_THICKNESS or 
            snake_pos[1] >= TOP_MARGIN + GAME_HEIGHT - BORDER_THICKNESS):
            return True
            
        # Self collision
        if snake_pos in self.snake_body[1:]:
            return True
            
        return False

    def draw_game_info(self, score, speed):
        """Draw game information outside the border"""
        # Draw score at top
        score_text = self.font.render(f'Score: {score}', True, WHITE)
        window.blit(score_text, (SIDE_MARGIN, 10))
        
        # Draw speed at top right
        speed_text = self.small_font.render(f'Speed: {speed}', True, WHITE)
        window.blit(speed_text, (WIDTH - SIDE_MARGIN - speed_text.get_width(), 15))
        
        # Draw controls at bottom
        controls_text = self.small_font.render('P: Pause  M: Mute  Arrow Keys: Move', True, WHITE)
        window.blit(controls_text, (SIDE_MARGIN, HEIGHT - 30))

    def game_loop(self):
        """Main game loop"""
        self.snake_pos = [SIDE_MARGIN + GAME_WIDTH//4, TOP_MARGIN + GAME_HEIGHT//2]
        self.snake_body = [self.snake_pos[:]]
        direction = 'RIGHT'
        food_pos = self.generate_food_position(self.snake_body)
        score = 0
        speed = FPS

        while True:
            self.update_food_properties()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                direction = self.handle_input(event, direction)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    if self.pause_menu() == 'restart':
                        return 'restart'

            # Update snake position
            move = {
                'UP': (0, -SNAKE_SIZE),
                'DOWN': (0, SNAKE_SIZE),
                'LEFT': (-SNAKE_SIZE, 0),
                'RIGHT': (SNAKE_SIZE, 0)
            }
            dx, dy = move[direction]
            self.snake_pos = [self.snake_pos[0] + dx, self.snake_pos[1] + dy]

            # Check collisions
            if self.check_collision(self.snake_pos):
                return 'game_over'

            # Update snake body
            self.snake_body.insert(0, list(self.snake_pos))
            
            # Check food collision
            if (abs(self.snake_pos[0] - food_pos[0]) < SNAKE_SIZE and 
                abs(self.snake_pos[1] - food_pos[1]) < SNAKE_SIZE):
                score += 1
                speed = min(FPS + score // 5, 25)  # Increase speed with score
                food_pos = self.generate_food_position(self.snake_body)
            else:
                self.snake_body.pop()

            # Draw everything
            window.fill(BLACK)  # Clear entire window
            if self.background_image:
                window.blit(self.background_image, 
                            (SIDE_MARGIN + BORDER_THICKNESS, 
                            TOP_MARGIN + BORDER_THICKNESS))
            
            # Draw game area background
            pygame.draw.rect(window, GRAY, 
                           (SIDE_MARGIN + BORDER_THICKNESS, 
                            TOP_MARGIN + BORDER_THICKNESS,
                            GAME_WIDTH - 2*BORDER_THICKNESS,
                            GAME_HEIGHT - 2*BORDER_THICKNESS))
            
            if self.background_image:
                window.blit(self.background_image, 
                          (SIDE_MARGIN + BORDER_THICKNESS, 
                           TOP_MARGIN + BORDER_THICKNESS))
                
            self.draw_border()
            self.draw_game_info(score, speed)

            # Draw snake
            self.draw_snake(self.snake_body)


            # Draw food
            pygame.draw.rect(window, tuple(self.food_color), 
                         pygame.Rect(food_pos[0], food_pos[1], self.food_size, self.food_size))

            pygame.display.update()
            self.clock.tick(speed)

    def pause_menu(self):
        """
        You can pause to attend to urgent matters and then come back to your journey anytime!
        """
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        window.blit(overlay, (0, 0))
        
        options = [
            ('Paused', -60),
            ('Press C to Continue', 0),
            ('Press R to Restart', 40),
            ('Press Q to Quit', 80)
        ]
        
        for text, y_offset in options:
            self.show_message(text, WHITE, (WIDTH // 2, HEIGHT // 2 + y_offset))
        
        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        return 'continue'
                    if event.key == pygame.K_r:
                        return 'restart'
                    if event.key == pygame.K_q:
                        return 'quit'
    
    def update_food_properties(self):
        # Make the food randomly shifts in both color and size
        if not (0 <= self.food_color[1] + 5 * self.color_direction <= 255):
            self.color_direction *= -1
        self.food_color[1] += 5 * self.color_direction
        self.food_color[1] = max(0, min(255, self.food_color[1]))

        if not (SNAKE_SIZE - 5 <= self.food_size + self.size_direction <= SNAKE_SIZE + 5):
            self.size_direction *= -1
        self.food_size += self.size_direction
        self.food_size = max(SNAKE_SIZE - 5, min(SNAKE_SIZE + 5, self.food_size))

    def game_over_screen(self):
        """Display game over screen"""
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        window.blit(overlay, (0, 0))
        
        self.show_message('Game Over!', RED, (WIDTH // 2, HEIGHT // 2 - 40))
        self.show_message('Press Y to Play Again or N to Quit', WHITE, (WIDTH // 2, HEIGHT // 2 + 20))
        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    if event.key == pygame.K_n:
                        return False

    def start_screen(self):
        """Display start screen"""
        window.fill(self.bg_color)
        self.show_message('Snake Game', GREEN, (WIDTH // 2, HEIGHT // 3))
        self.show_message('Press Y to Start or N to Quit', WHITE, (WIDTH // 2, HEIGHT // 2))
        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    if event.key == pygame.K_n:
                        return False

def main():
    game = SnakeGame()
    
    while True:
        if not game.start_screen():
            break
            
        while True:
            result = game.game_loop()
            if result == 'quit':
                pygame.quit()
                return
            elif result == 'restart':
                break
            elif result == 'game_over':
                if not game.game_over_screen():
                    pygame.quit()
                    return
                break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
