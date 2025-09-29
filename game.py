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
WIN = 5
game_state = 0
selected_option = 0
settings_selected_option = 0
immortality_start_time = 0
is_immortal = False
menu_options = ["Start Game", "Controls and rules", "Settings", "Quit"]

# Settings
music_enabled = False
volume = 0.5
difficulty = 1
bg_color_index = 0
set_seed_index = 0
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
enemysource_rec = Rectangle(0,0,35,35)
enemydesc_rec = Rectangle(enemy_x-enemy_r,enemy_y-enemy_r,2*enemy_r,2*enemy_r)
playersource_rec = Rectangle(0,0,32,32)
playerdesc_rec = Rectangle(x-16,y-16,2*r,2*r)
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
menu_music = pyray.load_music_stream("sounds/main_menu_music.mp3")
music = pyray.load_music_stream("sounds/game_music.mp3")
music_distant = pyray.load_music_stream("sounds/game_music_distant.mp3")
death_sound_effect = pyray.load_sound("sounds/death.wav")
coin_sound_effect = pyray.load_sound("sounds/coin.wav")
select_sound_effect = pyray.load_sound("sounds/select.wav")
pyray.play_music_stream(music)
pyray.pause_music_stream(music)
pyray.play_music_stream(menu_music)
pyray.play_music_stream(music_distant)
pyray.pause_music_stream(music_distant)
pyray.pause_music_stream(menu_music)

pyray.set_sound_volume(select_sound_effect, volume/10)

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

def reset_music_function():
    if music_enabled == False:
        return
    elif music_enabled == True:
        pyray.stop_music_stream(menu_music)
        pyray.stop_music_stream(music)
        pyray.stop_music_stream(music_distant)
        pyray.play_music_stream(menu_music)
        pyray.play_music_stream(music)
        pyray.play_music_stream(music_distant)

def draw_menu():
    pyray.update_music_stream(menu_music)
    pyray.set_music_volume(menu_music, volume)
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

def get_seed_index():
    # Get seed based on players chose
    if set_seed_index == 0:
        seed("20080905")
    elif set_seed_index == 1:
        seed(random.randint(0, 100000))

def draw_game():
    pyray.update_music_stream(music)
    pyray.update_music_stream(music_distant)
    pyray.set_music_volume(music, volume/2)
    pyray.set_music_volume(music_distant, 0)
    # Draw the actual game
    clear_background(DARKGRAY)
    global x, y, r, target_x, target_y, target_r, score, game_state, enemy_directions, last_direction_change, enemies, immortality_start_time, is_immortal, enemy_rec

    # Draw background based on setting
    if bg_color_index == 0:
        draw_texture(bgnight, 0, 0, WHITE)
    else:
        draw_texture(bgday, 0, 0, WHITE)
    # Draw player
    draw_circle(x, y, r, BLANK)
    draw_texture(player, x - 16, y - 16, WHITE)

    # Creating target circle
    playerdesc_rec.x = x-r
    playerdesc_rec.y = y-r
    draw_texture_pro(player,playersource_rec,playerdesc_rec,(0,0),0,WHITE)
    draw_circle(target_x+16,target_y+16,target_r,YELLOW)

    # Change direction every 5 seconds
    if time.time() - last_direction_change > 5:
        enemy_directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in enemies]
        last_direction_change = time.time()

    # Drawing enemies and updating their positions
    for i in range(len(enemies)):
        enemy_x, enemy_y, enemy_r = enemies[i]
        dx, dy = enemy_directions[i]
        draw_circle(enemy_x, enemy_y, enemy_r, BLANK)
        enemydesc_rec.x = enemy_x - enemy_r
        enemydesc_rec.y = enemy_y - enemy_r
        draw_texture_pro(saw,enemysource_rec,enemydesc_rec,(0,0),0, WHITE)
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
        playerdesc_rec.width = 2*r
        playerdesc_rec.height = 2*r
        score += 1
        pyray.play_sound(coin_sound_effect)
        pyray.set_sound_volume(coin_sound_effect, volume/5)
    
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
            enemy_rec = Rectangle(enemy_x, enemy_y, 2*enemy_r,2*enemy_r)
            if check_collision_circles((x, y), r, (enemy_x, enemy_y), enemy_r):
                print("YOU DIED")
                game_state = GAME_OVER
                pyray.play_sound(death_sound_effect)
                pyray.set_sound_volume(death_sound_effect, volume/3)
                #pyray.close_window()
                #exit()

    if is_immortal:
        remaining_time = 3 - (time.time() - immortality_start_time)
        if remaining_time > 0:
            draw_circle(x, y, r + 7, YELLOW) # Yellow outline when immortal
            draw_texture_pro(player,playersource_rec,playerdesc_rec,(0,0),0,WHITE) # Draw player again to cover outline
    # Draw score
    target_count = get_target_count_from_difficulty()
    for _ in range(target_count):
        draw_text(f"score = {score}/{target_count}",0,20,32,WHITE)
        
    # Simple game message
    draw_text("Game is running! Press P for menu", 0, 0, 20, WHITE)
    
def draw_instructions():
    pyray.update_music_stream(menu_music)
    pyray.set_music_volume(menu_music, volume)
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
    pyray.update_music_stream(menu_music)
    pyray.set_music_volume(menu_music, volume)
    # Draw game over screen
    clear_background(BLACK)
    
    draw_text("SETTINGS", 250, 100, 36, WHITE)

    settings_options = [
    f"Enable music: {'ON' if music_enabled else 'OFF'}",
    f"Volume: {round(volume,1)}",
    f"Difficulty: {difficulty_names[difficulty]}",
    f"Change background: {bg_colors[bg_color_index]}",
    f"Seed type: {set_seed[set_seed_index]}",
    "",
    "Back to Menu"
    ]

    # Instructions at bottom
    draw_text("Use UP/DOWN arrows to navigate, LEFT/RIGHT arrows OR ENTER to select", 100, 500, 18, LIGHTGRAY)

    for i, setting in enumerate(settings_options):
        if i == 5:  # Skip empty line
            continue
            
        color = YELLOW if i == settings_selected_option else WHITE
        y_pos = 150 + i * 50
        
        if i == settings_selected_option and i != 6:  # Not "Back to Menu"
            draw_text(">", 50, y_pos, 24, YELLOW)
            
        draw_text(setting, 100, y_pos, 24, color)

def draw_win():
    pyray.update_music_stream(music)
    pyray.update_music_stream(music_distant)
    pyray.set_music_volume(music, 0)
    pyray.set_music_volume(music_distant, volume)
    # Draw winning screen screen
    clear_background(DARKGREEN)    
    draw_text("YOU WIN!", 300, 200, 48, WHITE)
    draw_text(f"Final Score: {score}", 300, 300, 32, YELLOW)
    draw_text("Press SPACE to return to menu", 200, 400, 24, LIGHTGRAY)

def draw_game_over():
    pyray.update_music_stream(music)
    pyray.update_music_stream(music_distant)
    pyray.set_music_volume(music, 0)
    pyray.set_music_volume(music_distant, volume)
    # Draw game over screen
    clear_background(RED)
    
    draw_text("GAME OVER", 250, 200, 48, WHITE)
    draw_text(f"Final Score: {score}", 300, 300, 32, YELLOW)
    draw_text("Press SPACE to return to menu", 200, 400, 24, LIGHTGRAY)

def reset_game():
    global x, y, r, score, target_x, target_y, enemies, enemy_directions, last_direction_change, direction, immortality_start_time, is_immortal, playerdesc_rec

    x = 400  # Center of screen
    y = 400  # Center of screen
    r = 40
    playerdesc_rec = Rectangle(x-16,y-16,2*r,2*r)
    score = 0
    direction = None
    target_x = random.randint(30, screen_x-30)
    target_y = random.randint(30, screen_y-30)
    
    seed = get_seed_index()
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
        play_sound(select_sound_effect)
        selected_option = (selected_option - 1) % len(menu_options)
    
    if is_key_pressed(KEY_DOWN):
        play_sound(select_sound_effect)
        selected_option = (selected_option + 1) % len(menu_options)
    
    if is_key_pressed(KEY_ENTER):
        play_sound(select_sound_effect)
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
    global x, y, r, game_state, direction, is_game_music_on, music_enabled
    
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
 
    # Mute/Unmute music on M key
    if pyray.is_key_pressed(pyray.KEY_M):
        if is_game_music_on == True:
            pyray.stop_music_stream(menu_music)
            pyray.stop_music_stream(music)
            pyray.stop_music_stream(music_distant)
            is_game_music_on = False
            music_enabled = False
        else:
            pyray.play_music_stream(menu_music)
            pyray.play_music_stream(music)
            pyray.play_music_stream(music_distant)
            is_game_music_on = True
            music_enabled = True

    # Return to menu
    if is_key_pressed(KEY_P):
        game_state = MENU
        reset_music_function()
        
    return True

def handle_settings_input():
    # Handle input in settings screen
    global settings_selected_option, music_enabled, volume, difficulty, bg_color_index, game_state, set_seed_index
    
    if is_key_pressed(KEY_UP):
        play_sound(select_sound_effect)
        settings_selected_option = (settings_selected_option - 1) % 7
        if settings_selected_option == 5:  # Skip empty line
            settings_selected_option = 4
    
    if is_key_pressed(KEY_DOWN):
        play_sound(select_sound_effect)
        settings_selected_option = (settings_selected_option + 1) % 7
        if settings_selected_option == 5:  # Skip empty line
            settings_selected_option = 6
    
    if is_key_pressed(KEY_LEFT):
        play_sound(select_sound_effect)
        if settings_selected_option == 0:  # Music
            music_enabled = not music_enabled
            if music_enabled:
                pyray.play_music_stream(menu_music)
                pyray.play_music_stream(music)
                pyray.play_music_stream(music_distant)
            else:
                pyray.stop_music_stream(menu_music)
                pyray.stop_music_stream(music)
                pyray.stop_music_stream(music_distant)
        elif settings_selected_option == 1:  # Volume
            volume = max(0.0, volume - 0.1)            
        elif settings_selected_option == 2:  # Difficulty
            difficulty = (difficulty - 1) % 3
        elif settings_selected_option == 3:  # Background
            bg_color_index = (bg_color_index - 1) % 2
        elif settings_selected_option == 4:
            set_seed_index = (set_seed_index- 1) % 2

    if is_key_pressed(KEY_RIGHT):
        play_sound(select_sound_effect)
        if settings_selected_option == 0:  # Music
            music_enabled = not music_enabled
            if music_enabled:
                pyray.play_music_stream(menu_music)
                pyray.play_music_stream(music)
                pyray.play_music_stream(music_distant)
            else:
                pyray.stop_music_stream(menu_music)
                pyray.stop_music_stream(music)
                pyray.stop_music_stream(music_distant)
        elif settings_selected_option == 1:  # Volume
            volume = min(1.0, volume + 0.1)
        elif settings_selected_option == 2:  # Difficulty
            difficulty = (difficulty + 1) % 3
        elif settings_selected_option == 3:  # Background
            bg_color_index = (bg_color_index + 1) % 2
        elif settings_selected_option == 4:
            set_seed_index = (set_seed_index + 1) % 2
    
    if is_key_pressed(KEY_ENTER):
        play_sound(select_sound_effect)
        if settings_selected_option == 6:  # Back to Menu
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
            reset_music_function()
    
    elif game_state == WIN:
        draw_win()
        if is_key_pressed(KEY_SPACE):
            game_state = MENU
            reset_music_function()
    
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
pyray.unload_music_stream(music_distant)
pyray.unload_music_stream(menu_music)
pyray.unload_sound(death_sound_effect)
pyray.unload_sound(coin_sound_effect)
pyray.unload_sound(select_sound_effect)
pyray.close_audio_device()
pyray.close_window()