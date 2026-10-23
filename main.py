import pygame
from pygame import Vector2
import random
import os
from items import ItemManager
from sandWorm import sandWorm, opponentSandworm
from var import *


# Initialization
pygame.init()
screen = pygame.display.set_mode((CELL_SIZE*CELL_NUM, CELL_SIZE*CELL_NUM))
pygame.display.set_caption('sand_worm')
bgd_img = pygame.image.load(os.path.join('img', 'bg1_0.jpg')).convert()
bgd_img_trasformed = pygame.transform.scale(bgd_img, (CELL_NUM*CELL_SIZE, CELL_NUM*CELL_SIZE))
st_bgd_img = pygame.image.load(os.path.join('img', 'bg2_0.jpg')).convert()
st_bgd_img_trasformed = pygame.transform.scale(st_bgd_img, (CELL_NUM*CELL_SIZE, CELL_NUM*CELL_SIZE))
menu_bg = pygame.image.load(os.path.join('img', 'menu_background.png')).convert()
play_button_image = pygame.image.load(os.path.join('img', 'play_button.png')).convert_alpha()
play_button_rect = play_button_image.get_rect(midbottom=(CELL_NUM*CELL_SIZE//2, CELL_NUM * CELL_SIZE - 2.7*CELL_SIZE))
end = pygame.image.load(os.path.join('img', 'end.png')).convert_alpha()
end_transform = pygame.transform.scale(end, (CELL_NUM*CELL_SIZE+200, CELL_NUM*CELL_SIZE))

# Clock Setting
clock = pygame.time.Clock()

font_name = pygame.font.match_font('comicsans', 50)

# Function
def text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(font_name, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surf.blit(text_surf, text_rect)

def check_collide_wall():
    if not 0 <= player.head.pos.x <= CELL_NUM-1:
        return False
    elif not 0 <= player.head.pos.y <= CELL_NUM-1:
        return False
    else:
        return True

def check_collide_body():
    if (player.head.pos.x, player.head.pos.y) in player.body:
        return False
    else:
        return True
    
def time_stop():
    global score, player, items, is_paused, key_sample_time, score_update_time, state, last_state_time, opponent_sandworms, last_opponent_spawn_time
    running = True
    x = random.randint(2, CELL_NUM-1)
    y = random.randint(2, CELL_NUM-1)
    player = sandWorm(3, x, y)
    items.items_all_random(player.body)
    player.dir = random.choice([Vector2(1, 0), Vector2(0, 1), Vector2(0, -1)])
    screen.blit(st_bgd_img_trasformed, (0, 0))
    items.draw(screen)
    player.draw(screen)
    text(screen, 'Score: '+str(score), 25, CELL_SIZE+30, 10)
    pygame.display.update()
    pygame.time.delay(300)
    for i in state:
        state[i] = False
    for i in last_state_time:
        last_state_time[i] = 0
    score_update_time = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_paused = True
                if pygame.time.get_ticks() - key_sample_time > 100:
                    if state['reverse']:
                        if event.key == pygame.K_a and player.dir != Vector2(-1, 0):
                            player.dir = Vector2(1, 0)
                        elif event.key == pygame.K_d and player.dir != Vector2(1, 0):
                            player.dir = Vector2(-1, 0)
                        elif event.key == pygame.K_w and player.dir != Vector2(0, -1):
                            player.dir = Vector2(0, 1)
                        elif event.key == pygame.K_s and player.dir != Vector2(0, 1):
                            player.dir = Vector2(0, -1)
                    else:
                        if event.key == pygame.K_a and player.dir != Vector2(1, 0):
                            player.dir = Vector2(-1, 0)
                        elif event.key == pygame.K_d and player.dir != Vector2(-1, 0):
                            player.dir = Vector2(1, 0)
                        elif event.key == pygame.K_w and player.dir != Vector2(0, 1):
                            player.dir = Vector2(0, -1)
                        elif event.key == pygame.K_s and player.dir != Vector2(0, -1):
                            player.dir = Vector2(0, 1)
                    key_sample_time = pygame.time.get_ticks()

        if is_paused:
            screen.fill((30, 30, 30))
            text(screen, 'Paused - Press ESC to Resume', 50, CELL_SIZE*CELL_NUM//2, CELL_SIZE*CELL_NUM//2, WHITE)
            pygame.display.update()
            while is_paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_paused = False
                        pygame.quit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        is_paused = False
                clock.tick(10)
            score_update_time += pygame.time.get_ticks()-pause_time
            time_stop_mode_last_time += pygame.time.get_ticks()-pause_time
            key_sample_time += pygame.time.get_ticks()-pause_time
            last_state_time = {i:pygame.time.get_ticks()-pause_time+last_state_time[i] for i in last_state_time}
                        
        if not 0 <= player.head.pos.x <= CELL_NUM-1:
            return True
        elif not 0 <= player.head.pos.y <= CELL_NUM-1:
            return True
        if (player.head.pos.x, player.head.pos.y) in player.body:
            return True
        if player.len <= 2:
            return True
        if pygame.time.get_ticks() - start_time > 10000:
            items.update_last_time_after_stop(start_time, pygame.time.get_ticks())
            last_opponent_spawn_time += pygame.time.get_ticks()-start_time
            return False

        now = pygame.time.get_ticks()
        hit = items.collideWith(player.head.pos)
        if hit == 'corpse':
            player.increase()
        elif hit == 'harvestor':
            player.increase(5)
        elif hit == 'thumper':
            state['accelerate'] = True
            last_state_time['accelerate'] = now
            player.accelerate()
        elif hit == 'muaddib':
            state['invincible'] = True
            last_state_time['invincible'] = now
        elif not state['invincible']:
            if hit == 'water':
                state['poison'] = True
                last_state_time['poison'] = now
                last = now
                player.decrease()
            elif hit == 'baron':
                return True
            elif hit == 'mother':
                state['reverse'] = True
                last_state_time['reverse'] = now

        if state['poison'] and now - last_state_time['poison'] <= 30000:
            if now - last > 1000:
                player.decrease()
                last = now
        else:
            last = 0
            state['poison'] = False
        if state['accelerate'] and now - last_state_time['accelerate'] > 20000:
            state['accelerate'] = False
            player.resetRate()
        if state['reverse'] and now - last_state_time['reverse'] > 20000:
            state['reverse'] = False
        if state['invincible'] and now - last_state_time['invincible'] > 15000:
            state['invincible'] = False
        
        if now - score_update_time > 1000:
            score += 1*player.len
            score_update_time = now

        for sandworm in opponent_sandworms:
            hit = sandworm.check_collision_with_player(player.head.pos)
            if hit == None:
                continue
            if hit == 'head':
                player.increase(sandworm.size)
                opponent_sandworms.remove(sandworm)
            elif hit == 'body' and not state['invincible']:
                return True

        player.update()
        for sandworm in opponent_sandworms:
            if sandworm.update():
                opponent_sandworms.remove(sandworm)
        screen.blit(st_bgd_img_trasformed, (0, 0))
        items.draw(screen)
        player.draw(screen)
        for sandworm in opponent_sandworms:
            sandworm.draw(screen)
        text(screen, 'Score: '+str(score), 25, CELL_SIZE+30, 10)
        pygame.display.update()


    

def draw_start_menu():
    clock.tick(10)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return False
                
        screen.blit(menu_bg, (0,0))
        screen.blit(play_button_image, play_button_rect)
        text(screen, 'Highest Score: '+str(highscore), 25, CELL_SIZE*CELL_NUM//2, CELL_SIZE*CELL_NUM//2+150, WHITE)
        pygame.display.update()


running = True
show_start_menu = True
highscore = 0


while running:
    if show_start_menu:
        f = open('highest_score.txt', 'r')
        highscore = int(f.read())
        f.close()
        if draw_start_menu():
            break
        opponent_sandworms = []
        player = sandWorm(3, 1, CELL_NUM>>1)
        items = ItemManager()
        score = 0
        last_state_time = {"accelerate":0, "invincible":0, "poison":0, "reverse":0}
        state = {"accelerate":False, "invincible":False, "poison":False, "reverse":False}
        is_paused = False
        is_died = False
        time_stop_mode_timer = 60000
        last_opponent_spawn_time = pygame.time.get_ticks()
        time_stop_mode_last_time = pygame.time.get_ticks()
        key_sample_time = pygame.time.get_ticks()
        score_update_time = pygame.time.get_ticks()
        show_start_menu = False
    
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_paused = True
            if pygame.time.get_ticks() - key_sample_time > 100:
                if state['reverse']:
                    if event.key == pygame.K_a and player.dir != Vector2(-1, 0):
                        player.dir = Vector2(1, 0)
                    elif event.key == pygame.K_d and player.dir != Vector2(1, 0):
                        player.dir = Vector2(-1, 0)
                    elif event.key == pygame.K_w and player.dir != Vector2(0, -1):
                        player.dir = Vector2(0, 1)
                    elif event.key == pygame.K_s and player.dir != Vector2(0, 1):
                        player.dir = Vector2(0, -1)
                else:
                    if event.key == pygame.K_a and player.dir != Vector2(1, 0):
                        player.dir = Vector2(-1, 0)
                    elif event.key == pygame.K_d and player.dir != Vector2(-1, 0):
                        player.dir = Vector2(1, 0)
                    elif event.key == pygame.K_w and player.dir != Vector2(0, 1):
                        player.dir = Vector2(0, -1)
                    elif event.key == pygame.K_s and player.dir != Vector2(0, -1):
                        player.dir = Vector2(0, 1)
                key_sample_time = pygame.time.get_ticks()
            

    if is_paused:
        screen.fill((30, 30, 30))
        text(screen, 'Paused - Press ESC to Resume', 50, CELL_SIZE*CELL_NUM//2, CELL_SIZE*CELL_NUM//2, WHITE)
        pygame.display.update()
        pause_time = pygame.time.get_ticks()
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    is_paused = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    is_paused = False
            clock.tick(10)
        items.update_last_time_after_stop(pause_time, pygame.time.get_ticks())
        score_update_time += pygame.time.get_ticks()-pause_time
        time_stop_mode_last_time += pygame.time.get_ticks()-pause_time
        key_sample_time += pygame.time.get_ticks()-pause_time
        last_state_time = {i:pygame.time.get_ticks()-pause_time for i in last_state_time}
        last_opponent_spawn_time += pygame.time.get_ticks()-pause_time
            
            

    if not 0 <= player.head.pos.x <= CELL_NUM-1:
        is_died = True
    elif not 0 <= player.head.pos.y <= CELL_NUM-1:
        is_died = True
    if (player.head.pos.x, player.head.pos.y) in player.body:
        is_died = True
    if player.len <= 2:
        is_died = True

    now = pygame.time.get_ticks()
    if now - time_stop_mode_last_time > time_stop_mode_timer:
        if time_stop():
            is_died = True
        score += 100
        time_stop_mode_last_time = pygame.time.get_ticks()
        now = pygame.time.get_ticks()

    if now - last_opponent_spawn_time > 30000 and len(opponent_sandworms) < 2 and random.random() < 0.5:
        opponent_sandworms.append(opponentSandworm())
        last_opponent_spawn_time = now
    

    hit = items.collideWith(player.head.pos)
    if hit == 'corpse':
        player.increase()
        score += 1
    elif hit == 'harvestor':
        player.increase(5)
        score += 5
    elif hit == 'thumper':
        state['accelerate'] = True
        last_state_time['accelerate'] = now
        player.accelerate()
    elif hit == 'muaddib':
        state['invincible'] = True
        last_state_time['invincible'] = now
    elif not state['invincible']:
        if hit == 'water':
            state['poison'] = True
            last_state_time['poison'] = now
            last = now
            player.decrease()
        elif hit == 'baron':
            is_died = True
        elif hit == 'mother':
            state['reverse'] = True
            last_state_time['reverse'] = now

    if state['poison'] and now - last_state_time['poison'] <= 30000:
        if now - last > 1000:
            player.decrease()
            last = now
    else:
        last = 0
        state['poison'] = False
    if state['accelerate'] and now - last_state_time['accelerate'] > 20000:
        state['accelerate'] = False
        player.resetRate()
    if state['reverse'] and now - last_state_time['reverse'] > 20000:
        state['reverse'] = False
    if state['invincible'] and now - last_state_time['invincible'] > 15000:
        state['invincible'] = False
    
    if now - score_update_time > 1000:
        score += 1*player.len
        score_update_time = now
    
    for sandworm in opponent_sandworms:
        hit = sandworm.check_collision_with_player(player.head.pos)
        if hit == None:
            continue
        if hit == 'head':
            player.increase(sandworm.size)
            opponent_sandworms.remove(sandworm)
        elif hit == 'body' and not state['invincible']:
            is_died = True
            
    if is_died:
        screen.blit(end_transform, (-75, 0))
        text(screen, 'Score: '+str(score), 50, CELL_SIZE*CELL_NUM//2, CELL_SIZE*CELL_NUM//2+150, WHITE)
        pygame.display.update()
        pygame.time.delay(2000)
        f = open('highest_score.txt', 'r+')
        if score > highscore:
            f.seek(0)
            f.write(str(score))
        f.close()
        show_start_menu = True
        is_died = False
    else:
        player.update()
        items.update(player.body)
        for sandworm in opponent_sandworms:
            if sandworm.update():
                opponent_sandworms.remove(sandworm)
        screen.blit(bgd_img_trasformed, (0, 0))
        items.draw(screen)
        player.draw(screen)
        for sandworm in opponent_sandworms:
            sandworm.draw(screen)
        text(screen, 'Score: '+str(score), 25, CELL_SIZE+30, CELL_SIZE, BLACK)
        pygame.display.update()

pygame.quit()