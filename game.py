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
WIN = 6
game_state = 0
selected_option = 0
settings_selected_option = 0
immortality_start_time = 0
is_immortal = False
menu_options = ["Start Game", "Controls and rules", "Settings", "Quit"]

# Settings
music_enabled = True
volume = 5
difficulty = 1
bg_color_index = 0 
bg_colors = ["Night", "Day"]
difficulty_names = ["Easy", "Normal", "Hard"]
set_seed = ["Set", "Random"]

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
is_game_music_on = False
init_window(screen_x,screen_y,"Circle Apocalypse")
set_target_fps(fps)

pyray.init_audio_device()
player = load_texture("img/player.png")
bgnight = load_texture("img/bg_citynight.png")
bgday = load_texture("img/bg_cityday.png")
saw = load_texture("img/saw.png")
music = pyray.load_music_stream("sounds/game_music.mp3")
pyray.play_music_stream(music)
pyray.pause_music_stream(music)

direction = None

enemies = [
    (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r),
    (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r),
    (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r),
    (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r),
    (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r)
]

# Initial enemy directions
enemy_directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in enemies]
last_direction_change = time.time()

# Functions to draw different screens
def draw_menu():
    # Draw the main menu
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

def get_target_count_from_difficulty():
    # Get number of targets based on difficulty
    if difficulty == 0:  # Easy
        return 10
    elif difficulty == 1:  # Normal
        return 15
    else:  # Hard
        return 20

def get_enemy_count_from_difficulty():
    # Get number of enemies based on difficulty
    if difficulty == 0:  # Easy
        return 3
    elif difficulty == 1:  # Normal
        return 5
    else:  # Hard
        return 7

def draw_game():
    pyray.update_music_stream(music)
    pyray.set_music_volume(music, volume)
    # Draw the actual game
    clear_background(DARKGRAY)
    global x, y, r, target_x, target_y, target_r, score, game_state, enemy_directions, last_direction_change, enemies, immortality_start_time, is_immortal
    
    # Draw background based on setting
    if bg_color_index == 0:
        draw_texture(bgnight, 0, 0, WHITE)
    else:
        draw_texture(bgday, 0, 0, WHITE)
    # Draw saws
    draw_texture(saw, 100, 100, WHITE)
    # Draw player
    draw_circle(x, y, r, BLUE)
    draw_texture(player, x - 16, y - 16, WHITE)
    
    # Draw score
    draw_text(f"score = {score}",0,20,32,WHITE)

    # Creating target circle and player circle
    draw_circle(x,y,r,BLUE)
    draw_circle(target_x+16,target_y+16,target_r,YELLOW)

    # Change direction every 5 seconds
    if time.time() - last_direction_change > 5:
        enemy_directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in enemies]
        last_direction_change = time.time()

    # Drawing enemies and updating their positions
    for i in range(len(enemies)):
        enemy_x, enemy_y, enemy_r = enemies[i]
        dx, dy = enemy_directions[i]
        draw_circle(enemy_x, enemy_y, enemy_r, RED)
        enemy_x += dx * 1
        enemy_y += dy * 1
    
    # Wrapping player around the screen
        if x > screen_x:
            x = 0
        elif x < 0:
            x = screen_x
        if y > screen_y:
            y = 0
        elif y < 0:
            y = screen_y
    
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

    # Checking collision of circles to collect target to earn score
    if check_collision_circles((x,y),r,(target_x + 16,target_y + 16),target_r):
        target_x = random.randint(30, screen_x-30)
        target_y = random.randint(30, screen_y-30)
        target_x += random.randint(-20, 20)
        target_y += random.randint(-20, 20)
        target_x = max(target_r, min(screen_x - target_r, target_x))
        target_y = max(target_r, min(screen_y - target_r, target_y))
        r += 5
        score += 1
    
    # Check for win condition
    if score >= get_target_count_from_difficulty():
        print("YOU WIN!")
        game_state = WIN

    # 3 seconds immortality check
    if is_immortal and time.time() - immortality_start_time > 3:
        is_immortal = False

    # Checking collision of circles to end game if player hits enemy
    if not is_immortal:
        for enemy_x, enemy_y, enemy_r in enemies:
            if check_collision_circles((x, y), r, (enemy_x, enemy_y), enemy_r):
                print("YOU DIED")
                game_state = GAME_OVER
                #pyray.close_window()
                #exit()

    if is_immortal:
        remaining_time = 3 - (time.time() - immortality_start_time)
        if remaining_time > 0:
            # Flash the player or show timer
            if int(time.time()):  # Flashing effect
                draw_circle(x, y, r + 7, YELLOW) # Yellow outline when immortal
                draw_circle(x, y, r, BLUE)  # Draw player again to cover outline
    # Simple game message
    draw_text("Game is running! Press P for menu", 0, 0, 20, WHITE)
    

def draw_instructions():
    # Draw instructions screen
    clear_background(DARKGREEN)
    
    draw_text("HOW TO PLAY", 250, 100, 36, WHITE)
    
    instructions = [
        "Collect yellow targets",
        "Each target gives you a score and makes you bigger",
        "Collect all the targets required to win",
        "Don't let saws touch you or you will die!",
        "Good luck!",
        "",
        "Use WASD or ARROW KEYS to move your player",
        "Use P to return to menu",
        "Use M to mute/unmute music",
        "",
        "Press SPACE to return to menu"
    ]
    
    for i, instruction in enumerate(instructions):
        draw_text(instruction, 100, 200 + i * 40, 24, WHITE)

def draw_settings():
    # Draw game over screen
    clear_background(BLACK)
    
    draw_text("SETTINGS", 250, 100, 36, WHITE)

    settings_options = [
    f"Enable music: {'ON' if music_enabled else 'OFF'}",
    f"Volume: {volume}/10",
    f"Difficulty: {difficulty_names[difficulty]}",
    f"Change background: {bg_colors[bg_color_index]}",
    f"Seed type: {set_seed[0]}"
    "",
    "Back to Menu"
    ]

    # Instructions at bottom
    draw_text("Use UP/DOWN arrows to navigate, LEFT/RIGHT arrows OR ENTER to select", 100, 500, 18, LIGHTGRAY)

    for i, setting in enumerate(settings_options):
        if i == 4:  # Skip empty line
            continue
            
        color = YELLOW if i == settings_selected_option else WHITE
        y_pos = 150 + i * 50
        
        if i == settings_selected_option and i != 5:  # Not "Back to Menu"
            draw_text(">", 50, y_pos, 24, YELLOW)

            
        draw_text(setting, 100, y_pos, 24, color)

def draw_win():
    # Draw winning screen screen
    clear_background(DARKGREEN)    
    draw_text("YOU WIN!", 300, 200, 48, WHITE)
    draw_text(f"Final Score: {score}", 300, 300, 32, YELLOW)
    draw_text("Press SPACE to return to menu", 200, 400, 24, LIGHTGRAY)

def draw_game_over():
    # Draw game over screen
    clear_background(RED)
    
    draw_text("GAME OVER", 250, 200, 48, WHITE)
    draw_text(f"Final Score: {score}", 300, 300, 32, YELLOW)
    draw_text("Press SPACE to return to menu", 200, 400, 24, LIGHTGRAY)

def reset_game():
    seed(1000) # Ensure special seed is set for new game
    # Reset game variables for a new game
    global x, y, r, score, target_x, target_y, enemies, enemy_directions, last_direction_change, direction, immortality_start_time, is_immortal

    
    x = 400  # Center of screen
    y = 400  # Center of screen
    r = 40
    score = 0
    direction = None
    target_x = random.randint(30, screen_x-30)
    target_y = random.randint(30, screen_y-30)
    
    # Reset enemies to completely new positions
    target_count = get_target_count_from_difficulty()
    for _ in range(target_count):
        draw_text(f"Score to win: {target_count}", 150, 250, 32, BLACK)
        
        
    # Reset enemies to completely new positions
    enemy_count = get_enemy_count_from_difficulty()
    enemies = []
    for _ in range(enemy_count):
        new_enemy = (random.randint(30, screen_x-30), random.randint(30, screen_y-30), enemy_r)
        enemies.append(new_enemy)
    
    # Reset enemy directions
    enemy_directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in enemies]
    last_direction_change = time.time()

    #Immortality check
    immortality_start_time = time.time()
    is_immortal = True

def handle_menu_input():
    # Handle input in menu state
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
        elif selected_option == 2:  # Controls
            game_state = SETTINGS
        elif selected_option == 3:  # Quit
            pyray.close_window()
            exit()
    
    return True

def handle_game_input():
    # Handle input during gameplay
    global x, y, r, game_state, direction, is_game_music_on
    
    # Player movement logic
    if is_key_pressed(KEY_W) and direction != "DOWN":
        direction = "UP"
    if is_key_pressed(KEY_A) and direction != "RIGHT":
        direction = "LEFT"
    if is_key_pressed(KEY_S) and direction != "UP":
        direction = "DOWN"
    if is_key_pressed(KEY_D) and direction != "LEFT":
        direction = "RIGHT"
    if is_key_pressed(KEY_UP) and direction != "DOWN":
        direction = "UP"
    if is_key_pressed(KEY_LEFT) and direction != "RIGHT":
        direction = "LEFT"
    if is_key_pressed(KEY_DOWN) and direction != "UP":
        direction = "DOWN"
    if is_key_pressed(KEY_RIGHT) and direction != "LEFT":
        direction = "RIGHT"
    match direction:
        case "UP":
            y -= speed
        case "LEFT":
            x -= speed
        case "DOWN":
            y += speed
        case "RIGHT":
            x += speed
  
    if pyray.is_key_pressed(pyray.KEY_M):
        if is_game_music_on == True:
            pyray.pause_music_stream(music)
            is_game_music_on = False
        else:
            pyray.resume_music_stream(music)
            is_game_music_on = True

    # Return to menu
    if is_key_pressed(KEY_P):
        game_state = MENU
    
    return True

def handle_settings_input():
    # Handle input in settings screen
    global settings_selected_option, music_enabled, volume, difficulty, bg_color_index, game_state
    
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
            if music_enabled:
                pyray.resume_music_stream(music)
            else:
                pyray.pause_music_stream(music)
        elif settings_selected_option == 1:  # Volume
            volume = max(0, volume - 1)
        elif settings_selected_option == 2:  # Difficulty
            difficulty = (difficulty - 1) % 3
        elif settings_selected_option == 3:  # Background
            bg_color_index = (bg_color_index - 1) % 2
    
    if is_key_pressed(KEY_RIGHT):
        if settings_selected_option == 0:  # Music
            music_enabled = not music_enabled
            if music_enabled:
                pyray.resume_music_stream(music)
            else:
                pyray.pause_music_stream(music)
        elif settings_selected_option == 1:  # Volume
            volume = min(10, volume + 1)
        elif settings_selected_option == 2:  # Difficulty
            difficulty = (difficulty + 1) % 3
        elif settings_selected_option == 3:  # Background
            bg_color_index = (bg_color_index + 1) % 2
    
    if is_key_pressed(KEY_ENTER):
        if settings_selected_option == 5:  # Back to Menu
            game_state = MENU
    
    return True

# Main game loop
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
    
    elif game_state == WIN:
        draw_win()
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
pyray.unload_texture(bgday)
pyray.unload_texture(bgnight)
pyray.unload_texture(saw)
pyray.unload_music_stream(music)
pyray.close_audio_device()
pyray.close_window()