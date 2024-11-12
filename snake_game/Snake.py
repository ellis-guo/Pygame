import pygame # to create and control the game
import sys # to handle quitting
import random # for generating random food positions

# Initialize the Pygame library to set up the game environment
pygame.init()

# Set up the dimensions of the game window
WIDTH, HEIGHT = 600, 400 # set up screen dimensions to 600 by 400 pixels
window = pygame.display.set_mode((WIDTH, HEIGHT)) # define a window using these dimensions 
pygame.display.set_caption('Snake')  # give it the title “Snake”

# Define RGB color values for various elements
WHITE = (255, 255, 255)  # Color for text and messages
GREEN = (0, 255, 0)      # Color for the snake
RED = (255, 0, 0)        # Color for the food
BLACK = (0, 0, 0)        # Color for the background

# Set colors for the snake and background
snake_color = GREEN
bg_color = BLACK

# Define the size of the snake and food elements
SNAKE_SIZE = 20

# Initialize the game clock to control the frame rate
clock = pygame.time.Clock()

# Define the font style and size for text display
font = pygame.font.SysFont('arial', 28)

def show_message(text, color, pos):
    """Display a text message on the screen at a specified position.
    
    Parameters:
        text (str): The message text to display.
        color (tuple): RGB color of the text.
        pos (tuple): (x, y) position to place the text on the screen.
    """
    message = font.render(text, True, color)
    window.blit(message, pos)
    pygame.display.update()

def game_over():
    """Handle game-over logic:
    Clears the screen, shows a “Game Over” message, and waits for the 
    player to choose to restart or quit.
    
    Returns:
        bool: True if the player wants to play again, False to quit.
    """
    # Fill the screen with the background color
    window.fill(bg_color)
    
    # Render the "Game Over!" message and center it near the top of the screen
    game_over_text = font.render('Game Over!', True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    window.blit(game_over_text, game_over_rect)

    # Render the "Press Y to Play Again or N to Quit" message below the game-over message
    restart_text = font.render('Press Y to Play Again or N to Quit', True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    window.blit(restart_text, restart_rect)

    pygame.display.update()

    # Wait for player input to determine if they want to restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

def start_screen():
    """Display the initial start screen with options to begin or quit the game.
    
    Returns:
        bool: True if the player wants to start, False to quit.
    """
    # Fill the screen with the background color
    window.fill(bg_color)
    # Display start message
    show_message('Press Y to Start or N to Quit', WHITE, (100, HEIGHT // 2 - 20))

    # Wait for player input to either start or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

def game_loop():
    """Main game loop that controls the gameplay, snake movement, and interactions.
    
    Returns:
        bool: False when the game ends (collision or quit).
    """
    # Initialize snake position, body segments, direction, and speed
    snake_pos = [100, 50]  # Initial position of the snake's head
    snake_body = [[100, 50]]  # a list that keeps track of all the segments of the snake
    direction = 'RIGHT'  # The snake starts by moving to the right
    change_to = direction
    speed = 8  # Snake's movement speed (affects game difficulty)

    # Generate an initial random position for the food
    food_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
    food_generate = True  # Boolean to track if food needs regenerateing, True to indicate that food is present

    # Initialize score
    score = 0

    # Main loop for gameplay
    while True:
        # Process player input for snake direction
        for event in pygame.event.get(): # loop through events, checks if any key has been pressed or if the game should quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: # if an arrow key is pressed, update change_to to the new desired direction
                # additional checking to prevent the snake from reversing directly
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        # Update snake direction based on user input
        direction = change_to

        # Move the snake's head in the current direction
        if direction == 'UP': # decrease the Y-coordinate of snake_pos to move the head upward
            snake_pos[1] -= SNAKE_SIZE
        if direction == 'DOWN':
            snake_pos[1] += SNAKE_SIZE
        if direction == 'LEFT':
            snake_pos[0] -= SNAKE_SIZE
        if direction == 'RIGHT':
            snake_pos[0] += SNAKE_SIZE

        # Add a new segment at the head position
        snake_body.insert(0, list(snake_pos)) # updated snake_pos is then added to the beginning of snake_body, creating a new head position
        # Check if snake has collided with food
        if pygame.Rect(snake_pos[0], snake_pos[1], SNAKE_SIZE, SNAKE_SIZE).colliderect(
            pygame.Rect(food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE)):
            food_generate = False  # Mark that food needs to regenerate
            score += 1  # Increase score when food is eaten
        else:
            # If food not eaten, remove the last segment to maintain the current length
            snake_body.pop()

        # Food reappear at a new location if it was eaten
        if not food_generate:
            food_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                        random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
        food_generate = True

        # Fill the background color for each frame
        window.fill(bg_color)

        # Draw the snake on the screen 
        for pos in snake_body:
            pygame.draw.rect(window, snake_color, pygame.Rect(
                pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))

        # Draw the food on the screen
        pygame.draw.rect(window, RED, pygame.Rect(
            food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE))

        # Display the current score at the top-left corner
        score_text = font.render(f'Score: {score}', True, WHITE)
        window.blit(score_text, (10, 10))

        # Check if the snake has collided with the wall or itself
        if snake_pos[0] < 0 or snake_pos[0] >= WIDTH:
            return False
        if snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
            return False  # End game if out of bounds
        for block in snake_body[1:]:
            if snake_pos == block:
                return False  # End game if snake collides with itself

        # Update the game display with all changes
        pygame.display.update()

        # Control the game speed (frames per second)
        clock.tick(speed)

# Main loop for the game execution flow
while True:
    if not start_screen():
        break  # Exit if player chooses to quit

    if not game_loop():
        if not game_over():
            break  # Exit if player chooses to quit after game over

pygame.quit()  # Quit Pygame when the game loop ends
