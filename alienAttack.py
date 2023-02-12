#this is JakeTheHolt
import time
import maze
import re
import random
import timer

tiles        = maze.tiles
player_start = maze.player_start
enemy_start  = maze.enemy_start
maze         = maze.maze

TILE_SIZE = 64
WIDTH = TILE_SIZE * 8
HEIGHT = TILE_SIZE * 8
LEVEL = 1
MAX_LEVEL = 1
DIRECTION = [1,0]
TIMER = 0
PLAYER_HEALTH = 1
ENEMY_HEALTH = 1
ENEMY_SPEED = 60 #60 is 1 tile every second!
PLAYER_PROJECTILE_SPEED = 1.0 # Smaller is faster
ENEMY_PROJECTILE_SPEED = 3.0

unlock = 0

player = Actor("player", anchor=(0, 0), pos=(player_start[LEVEL][0], player_start[LEVEL][1]))
enemy  = Actor("enemy",  anchor=(0, 0), pos=(enemy_start[LEVEL][0], enemy_start[LEVEL][1]))
enemy_projectile = Actor("enemy_projectile", anchor=(32, 32), pos=(2 * TILE_SIZE, 1 * TILE_SIZE))
player_projectile = Actor("player_projectile", anchor=(32, 32), pos=(2 * TILE_SIZE, 1 * TILE_SIZE))

enemy_hit_timer  = timer.timer(enemy,  60)  # Create a timer which is only active when the enemy is visible
timers = [enemy_hit_timer]

VISIBLE = [player, enemy]

enemy.yv = -1
music.play('background')
music.set_volume(0.8)

ENEMY_HEALTH = 5

def draw():
    global LEVEL
    screen.clear()
    for row in range(len(maze[LEVEL])):
        for column in range(len(maze[LEVEL][row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[LEVEL][row][column]]
            if tile!='path':
                screen.blit('path', (x, y)) # This draws a path under everything not a path!
            screen.blit(tile, (x, y)) # Draw the tile as the maze intended
    for character in VISIBLE: # Draw all visible characters
        character.draw()
def update(): # Update function is called 60 times a second
    global VISIBLE
    global TIMER
    global ENEMY_HEALTH
    global ENEMY_SPEED
    global PLAYER_HEALTH
    global ENEMY_PROJECTILE_SPEED
    TIMER = TIMER + 1

    advance_timers() # Function to advance all active timers

    if player_projectile in VISIBLE: # If player_projectile is visible, then move it by one space in the direction last perfored
        if player_projectile.x >= WIDTH or player_projectile.y >= HEIGHT or player_projectile.x <= -TILE_SIZE/2.0 or player_projectile.y <= -TILE_SIZE/2.0:
            VISIBLE.remove(player_projectile)
        if enemy in VISIBLE and player_projectile.colliderect(enemy) and not enemy_hit_timer.is_active(): # Did the player_projectile collide with the enemy?
            ENEMY_HEALTH -= 1
            enemy_hit_timer.start() # start the timer for the enemy
            if (ENEMY_HEALTH == 0):
                enemy.image = 'enemy_hurt5'
                sounds.winner_chicken_dinner.play()
                #game_exit("YOU WIN!")
            if (ENEMY_HEALTH == 4):
                enemy.image = 'enemy_hurt'
            if (ENEMY_HEALTH == 3):
                enemy.image = 'enemy_hurt1'
            if (ENEMY_HEALTH == 2):
                enemy.image = 'enemy_hurt2'
            if (ENEMY_HEALTH == 1):
                enemy.image = 'enemy_hurt3'

    if enemy_projectile in VISIBLE: # If player_projectile is visible, then move it by one space in the direction last perfored
        if enemy_projectile.x >= WIDTH or enemy_projectile.y >= HEIGHT or enemy_projectile.x <= -TILE_SIZE/2.0 or enemy_projectile.y <= -TILE_SIZE/2.0:
            VISIBLE.remove(enemy_projectile)
        if player in VISIBLE and enemy_projectile.colliderect(player):
            sounds.death.play()
            music.set_volume(0)
            game_exit("YOU DIED!")
    if TIMER%ENEMY_SPEED == 0:
        move_enemy()

    if enemy in VISIBLE:
        if (enemy_hit_timer.is_expired() and (ENEMY_HEALTH == 0)): # Only after the timer has expired, and health is 0, remove the enemy
            game_exit("YOU WIN!")


    if TIMER%ENEMY_SPEED == 59:
        throw_enemy_projectile()
        sounds.lazer.play()
    if (ENEMY_HEALTH == 0):
        if enemy_projectile in VISIBLE:
            VISIBLE.remove(enemy_projectile)
        #if enemy in VISIBLE:
        #     VISIBLE.remove(enemy)

def on_key_down(key):
    # player movement
    global LEVEL
    global MAX_LEVEL
    global DIRECTION
    global VISIBLE
    row = int(player.y / TILE_SIZE)
    column = int(player.x / TILE_SIZE)

    if key == keys.UP:
        row = row - 1
        player.image = 'playerup'
        DIRECTION = [0,-1]
    if key == keys.DOWN:
        row = row + 1
        player.image = 'playerdown'
        DIRECTION = [0,1]
    if key == keys.LEFT:
        column = column - 1
        player.image = 'playerleft'
        DIRECTION = [-1,0]
    if key == keys.RIGHT:
        column = column + 1
        player.image = 'playerright'
        DIRECTION = [1,0]

    tile = tiles[maze[LEVEL][row][column]]
    if tile != 'space':
        x = column * TILE_SIZE
        y = row * TILE_SIZE
        animate(player, duration=0.1, pos=(x, y))
    global unlock

    if key == keys.SPACE:
        throw_player_projectile()
    #    sounds.shot.play()

    if enemy in VISIBLE:
        if (enemy_hit_timer.is_expired() and (ENEMY_HEALTH == 0)): # Only after the timer has expired, and health is 0, remove the enemy
            VISIBLE.remove(enemy)

def advance_timers():
    for t in timers:
        #print ("name:" + t.actor.image + " count:", t.count, " visible:", t.actor in VISIBLE," active:", t.is_active())
        if (t.actor in VISIBLE) and t.is_active():
            t.advance()

# enemy movement
def move_enemy():
    if enemy not in VISIBLE or enemy_hit_timer.is_active():
        return # Return from function if enemy is no longer visible
    y = enemy.y
    x = enemy.x
    if LEVEL==4: # Move towards player for boss level
        if random.randint(0, 1): # randomly choose number (0 or 1), if 1, move enemy in x direction closer to player, if 0, move enemy in y direction closer to player
            if player.x < enemy.x:
                x -= TILE_SIZE
            else:
                x += TILE_SIZE
        else:
            if player.y < enemy.y:
                y -= TILE_SIZE
            else:
                y += TILE_SIZE
    else:
        x += (enemy.yv * TILE_SIZE)

    column = int(x/ TILE_SIZE)
    row    = int(y / TILE_SIZE)
    tile = tiles[maze[LEVEL][row][column]]
    if tile!='space':
        animate(enemy, duration=0.1, pos=(x, y))
    else:
        enemy.yv = enemy.yv * -1

def throw_player_projectile():
    if player_projectile in VISIBLE:
        return
    VISIBLE.append(player_projectile)
    player_projectile.x = player.x + (TILE_SIZE/2.0)
    player_projectile.y = player.y + (TILE_SIZE/2.0)
    player_projectile.angle = 180
    x = player_projectile.x
    y = -TILE_SIZE
    duration = ((player.y+TILE_SIZE) / HEIGHT) * PLAYER_PROJECTILE_SPEED
    animate(player_projectile, duration=(duration), pos=(x, y))

def throw_enemy_projectile():
    if enemy_projectile in VISIBLE:
        return
    VISIBLE.append(enemy_projectile)
    enemy_projectile.x = enemy.x + (TILE_SIZE/2.0)
    enemy_projectile.y = enemy.y + (TILE_SIZE/2.0)
    enemy_projectile.angle = 0
    x = enemy_projectile.x
    y = HEIGHT
    duration = ((HEIGHT-player.y) / HEIGHT) * ENEMY_PROJECTILE_SPEED
    animate(enemy_projectile, duration=(duration), pos=(x, y))
# Advance all of the timers, but only if their actors are visible and they are active
def advance_timers():
    for t in timers:
        #print ("name:" + t.actor.image + " count:", t.count, " visible:", t.actor in VISIBLE," active:", t.is_active())
        if (t.actor in VISIBLE) and t.is_active():
            t.advance()

def game_exit(message):
    print (message)
    time.sleep(2)
    exit()
