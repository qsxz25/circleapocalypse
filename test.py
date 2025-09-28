from pyray import *
import time
import pyray
import random
from random import seed

# Variables
seed(1000)
MENU = 0
GAME = 1
GAME_OVER = 2
INSTRUCTIONS = 3
SETTINGS = 4
PAUSE = 5
game_state = 0
selected_option = 0
settings_selected_option = 0
menu_options = ["Start Game", "Controls and rules", "Settings", "Quit"]

# Settings variables
music_enabled = True
volume_level = 5  # 0-10 scale
difficulty = 1  # 0=Easy, 1=Normal, 2=Hard
bg_color_index = 0  # 0=Dark, 1=Light
bg_colors = ["Dark", "Light"]
difficulty_names = ["Easy", "Normal", "Hard"]

screen_x = 800
screen_y = 800
target_x = random.randint(30, screen_x-30)
target_y = random.randint(30, screen_y-30)
target_r = 15
r = 40
x = 200
y = 200
enemy_x = random.randint(30, screen_x-30)
enemy_y = random.randint(30, screen_y-30)
enemy_r = 75
speed = 4
fps = 60
score = 0
init_window(screen_x,screen_y,"Circle Apocalypse")
set_target_fps(fps)

# Audio disabled for now - no external files needed
audio_enabled = False
try:
    pyray.init_audio_device()
    audio_enabled = True
    print("Audio initialized successfully")
except:
    print("Audio initialization failed - continuing without audio")

direction = None

enemies = [
    (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r),
    (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r),
    (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r),
    (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r),
    (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r)
]

enemy_directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in enemies]
last_direction_change = time.time()

# Functions to draw different screens

def draw_menu():
    """Draw the main menu"""
    clear_background(DARKBLUE)
    
    # Title
    draw_text("CIRCLE APOCALYPSE", 200, 100, 48, GOLD)
    
    # Menu options
    for i, option in enumerate(menu_options):
        color = YELLOW if i == selected_option else WHITE
        y_pos = 250 + i * 60
        draw_text(option, 300, y_pos, 32, color)
        
        # Draw arrow for selected option
        if i == selected_option:
            draw_text(">", 250, y_pos, 32, YELLOW)
    
    # Instructions at bottom
    draw_text("Use UP/DOWN arrows to navigate, ENTER to select", 150, 500, 20, LIGHTGRAY)

def get_speed_from_difficulty():
    """Get player speed based on difficulty"""
    if difficulty == 0:  # Easy
        return 6
    elif difficulty == 1:  # Normal
        return 4
    else:  # Hard
        return 2

def get_enemy_count_from_difficulty():
    """Get number of enemies based on difficulty"""
    if difficulty == 0:  # Easy
        return 3
    elif difficulty == 1:  # Normal
        return 5
    else:  # Hard
        return 7

def draw_background():
    """Draw background based on setting"""
    if bg_color_index == 0:  # Dark theme
        clear_background(DARKGRAY)
        # Draw some simple background elements
        for i in range(0, screen_x, 100):
            for j in range(0, screen_y, 100):
                draw_circle(i + 50, j + 50, 5, Color(40, 40, 40, 100))
    else:  # Light theme
        clear_background(LIGHTGRAY)
        # Draw some simple background elements
        for i in range(0, screen_x, 100):
            for j in range(0, screen_y, 100):
                draw_circle(i + 50, j + 50, 5, Color(200, 200, 200, 100))

def draw_game():
    """Draw the actual game"""
    global x, y, r, target_x, target_y, target_r, score, game_state, enemy_directions, last_direction_change, enemies, speed
    
    # Draw background
    draw_background()
    
    # Update speed based on difficulty
    speed = get_speed_from_difficulty()
    
    # Draw score and info
    text_color = BLACK if bg_color_index == 1 else WHITE
    draw_text(f"Score: {score}", 10, 10, 32, text_color)
    draw_text(f"Difficulty: {difficulty_names[difficulty]}", 10, 50, 24, text_color)

    # Draw player (blue circle)
    draw_circle(x, y, r, BLUE)
    
    # Draw target (yellow circle)
    draw_circle(target_x, target_y, target_r, YELLOW)

    # Change enemy direction every 5 seconds
    if time.time() - last_direction_change > 5:
        enemy_directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in enemies]
        last_direction_change = time.time()

    # Drawing enemies and updating their positions
    for i in range(len(enemies)):
        enemy_x, enemy_y, enemy_r = enemies[i]
        dx, dy = enemy_directions[i]
        
        # Draw enemy as red circle with rotating effect
        draw_circle(enemy_x, enemy_y, enemy_r, RED)
        draw_circle_lines(enemy_x, enemy_y, enemy_r, RED)
        
        # Move enemies
        enemy_speed = 2 if difficulty <= 1 else 3
        enemy_x += dx * enemy_speed
        enemy_y += dy * enemy_speed
    
        # Wrapping enemies around the screen
        if enemy_x > screen_x: 
            enemy_x = 0
        elif enemy_x < 0:
            enemy_x = screen_x
        if enemy_y > screen_y:
            enemy_y = 0
        elif enemy_y < 0:
            enemy_y = screen_y
        enemies[i] = (enemy_x, enemy_y, enemy_r)

    # Wrapping player around the screen
    if x > screen_x:
        x = 0
    elif x < 0:
        x = screen_x
    if y > screen_y:
        y = 0
    elif y < 0:
        y = screen_y

    # Checking collision to collect target
    if check_collision_circles((x,y), r, (target_x, target_y), target_r):
        target_x = random.randint(30, screen_x-30)
        target_y = random.randint(30, screen_y-30)
        growth = 3 if difficulty == 2 else 5  # Smaller growth on hard mode
        r += growth
        score += 1
    
    # Checking collision with enemies
    for enemy_x, enemy_y, enemy_r in enemies:
        if check_collision_circles((x, y), r, (enemy_x, enemy_y), enemy_r):
            print("YOU DIED")
            game_state = GAME_OVER
    
    # Game instructions
    draw_text("Press P for menu", 10, screen_y - 30, 20, text_color)

def draw_instructions():
    """Draw instructions screen"""
    clear_background(DARKGREEN)
    
    draw_text("HOW TO PLAY", 250, 100, 36, WHITE)
    
    instructions = [
        "Collect yellow targets to grow and score points",
        "Avoid the red enemy circles - they will kill you!",
        "Your size increases each time you collect a target",
        "Enemies move randomly and change direction every 5 seconds",
        "",
        "CONTROLS:",
        "WASD or ARROW KEYS - Move your blue circle",
        "P - Return to menu (during game)",
        "L - Toggle music on/off (during game)",
        "",
        "Adjust difficulty in Settings for different challenges!",
        "",
        "Press SPACE to return to menu"
    ]
    
    for i, instruction in enumerate(instructions):
        draw_text(instruction, 50, 150 + i * 30, 20, WHITE)

def draw_settings():
    """Draw interactive settings screen"""
    clear_background(BLACK)
    
    draw_text("SETTINGS", 300, 50, 36, WHITE)
    
    settings_options = [
        f"Music: {'ON' if music_enabled else 'OFF'}",
        f"Volume: {volume_level}/10 {'■' * volume_level}{'□' * (10 - volume_level)}",
        f"Difficulty: {difficulty_names[difficulty]}",
        f"Theme: {bg_colors[bg_color_index]}",
        "",
        "Back to Menu"
    ]

    for i, setting in enumerate(settings_options):
        if i == 4:  # Skip empty line
            continue
            
        color = YELLOW if i == settings_selected_option else WHITE
        y_pos = 150 + i * 50
        
        if i == settings_selected_option and i != 5:  # Not "Back to Menu"
            draw_text(">", 50, y_pos, 24, YELLOW)
            draw_text("<", 700, y_pos, 24, YELLOW)
        elif i == settings_selected_option:
            draw_text(">", 50, y_pos, 24, YELLOW)
            
        draw_text(setting, 100, y_pos, 24, color)
    
    # Instructions
    draw_text("Use UP/DOWN to navigate", 250, 450, 20, LIGHTGRAY)
    draw_text("Use LEFT/RIGHT to change values", 230, 480, 20, LIGHTGRAY)
    draw_text("Press ENTER to go back to menu", 240, 510, 20, LIGHTGRAY)
 
def draw_game_over():
    """Draw game over screen"""
    clear_background(RED)
    
    draw_text("GAME OVER", 250, 200, 48, WHITE)
    draw_text(f"Final Score: {score}", 300, 300, 32, YELLOW)
    draw_text(f"Difficulty: {difficulty_names[difficulty]}", 320, 340, 24, YELLOW)
    draw_text("Press SPACE to return to menu", 200, 400, 24, LIGHTGRAY)

def reset_game():
    """Reset game variables for a new game"""
    seed(1000)
    global x, y, r, score, target_x, target_y, enemies, enemy_directions, last_direction_change, direction
    
    print(f"Starting new game on {difficulty_names[difficulty]} difficulty")
    
    x = 400
    y = 400
    r = 40
    score = 0
    direction = None
    target_x = random.randint(30, screen_x-30)
    target_y = random.randint(30, screen_y-30)
    
    # Reset enemies based on difficulty
    enemy_count = get_enemy_count_from_difficulty()
    enemies = []
    for _ in range(enemy_count):
        new_enemy = (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r)
        enemies.append(new_enemy)
    
    enemy_directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in enemies]
    last_direction_change = time.time()

def handle_menu_input():
    """Handle input in menu state"""
    global selected_option, game_state
    
    if is_key_pressed(KEY_UP):
        selected_option = (selected_option - 1) % len(menu_options)
    
    if is_key_pressed(KEY_DOWN):
        selected_option = (selected_option + 1) % len(menu_options)
    
    if is_key_pressed(KEY_ENTER):
        if selected_option == 0:  # Start Game
            game_state = GAME
            reset_game()
        elif selected_option == 1:  # Instructions
            game_state = INSTRUCTIONS 
        elif selected_option == 2:  # Settings
            game_state = SETTINGS
        elif selected_option == 3:  # Quit
            return False
    
    return True

def handle_settings_input():
    """Handle input in settings screen"""
    global settings_selected_option, music_enabled, volume_level, difficulty, bg_color_index, game_state
    
    if is_key_pressed(KEY_UP):
        settings_selected_option = (settings_selected_option - 1) % 6
        if settings_selected_option == 4:  # Skip empty line
            settings_selected_option = 3
    
    if is_key_pressed(KEY_DOWN):
        settings_selected_option = (settings_selected_option + 1) % 6
        if settings_selected_option == 4:  # Skip empty line
            settings_selected_option = 5
    
    if is_key_pressed(KEY_LEFT):
        if settings_selected_option == 0:  # Music
            music_enabled = not music_enabled
        elif settings_selected_option == 1:  # Volume
            volume_level = max(0, volume_level - 1)
        elif settings_selected_option == 2:  # Difficulty
            difficulty = (difficulty - 1) % 3
        elif settings_selected_option == 3:  # Theme
            bg_color_index = (bg_color_index - 1) % 2
    
    if is_key_pressed(KEY_RIGHT):
        if settings_selected_option == 0:  # Music
            music_enabled = not music_enabled
        elif settings_selected_option == 1:  # Volume
            volume_level = min(10, volume_level + 1)
        elif settings_selected_option == 2:  # Difficulty
            difficulty = (difficulty + 1) % 3
        elif settings_selected_option == 3:  # Theme
            bg_color_index = (bg_color_index + 1) % 2
    
    if is_key_pressed(KEY_ENTER):
        if settings_selected_option == 5:  # Back to Menu
            game_state = MENU
    
    return True

def handle_game_input():
    """Handle input during gameplay"""
    global x, y, r, game_state, direction
    
    # Player movement logic
    if is_key_down(KEY_W) or is_key_down(KEY_UP):
        direction = "UP"
    elif is_key_down(KEY_A) or is_key_down(KEY_LEFT):
        direction = "LEFT"
    elif is_key_down(KEY_S) or is_key_down(KEY_DOWN):
        direction = "DOWN"
    elif is_key_down(KEY_D) or is_key_down(KEY_RIGHT):
        direction = "RIGHT"
    else:
        direction = None
        
    # Move player based on direction
    if direction == "UP":
        y -= speed
    elif direction == "LEFT":
        x -= speed
    elif direction == "DOWN":
        y += speed
    elif direction == "RIGHT":
        x += speed

    # Return to menu
    if is_key_pressed(KEY_P):
        game_state = MENU
    
    return True

# Main game loop
print("Starting Circle Apocalypse...")
running = True

while running and not window_should_close():
    begin_drawing()
    
    if game_state == MENU:
        draw_menu()
        running = handle_menu_input()
    
    elif game_state == GAME:
        draw_game()
        running = handle_game_input()
    
    elif game_state == GAME_OVER:
        draw_game_over()
        if is_key_pressed(KEY_SPACE):
            game_state = MENU
    
    elif game_state == INSTRUCTIONS:
        draw_instructions()
        if is_key_pressed(KEY_SPACE):
            game_state = MENU

    elif game_state == SETTINGS:
        draw_settings()
        running = handle_settings_input()
    
    end_drawing()

print("Closing game...")
if audio_enabled:
    pyray.close_audio_device()
pyray.close_window()