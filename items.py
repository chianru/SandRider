import pygame
from pygame import Vector2
import random
from var import *
from sandWorm import myData
import os


class Item:
    def __init__(self, type:str, pos:tuple, img):
        self.type = type
        self.pos = Vector2(pos[0], pos[1])
        self.last_update_time = pygame.time.get_ticks()
        self.life_time = items_data[self.type]['life_time']
        self.disappear = False if self.life_time == None else True
        self.image = pygame.image.load(os.path.join('img', img)).convert()
        self.image_transformed = pygame.transform.scale(self.image, (CELL_SIZE+10, CELL_SIZE+10))
        self.image_transformed.set_colorkey(tuple(items_data[self.type]['set_color_key']))
        self.alpha = 128
        self.spawn_time = pygame.time.get_ticks()
    
    def draw(self, surf):
        elapsed_time = pygame.time.get_ticks() - self.spawn_time
        if elapsed_time < 300:
            self.alpha = int(128 + (127 * (elapsed_time / 300)))
        else:
            self.alpha = 255
        self.image_transformed.set_alpha(self.alpha)
        img_rect = (self.pos.x*CELL_SIZE, self.pos.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        surf.blit(self.image_transformed, img_rect)

    def check_updated(self, now):
        if not self.disappear:
            return False
        if now - self.last_update_time > self.life_time:
            self.last_update_time = now
            return True
        else:
            return False
        


class ItemManager:
    def __init__(self):
        now = pygame.time.get_ticks()
        self.items = {}
        self.items_spawn_time = {item:now for item in items_data}
        self.items_num = {item:0 for item in items_data}
        self.spawn_last_reduction_time = now
        self.spawn_reduction_timer = 30000
        self.spawn_reduction_amount = 5000
    
    def add(self, type:str, sandWorm_body:myData):
        if len(self.items) + len(sandWorm_body)+1 == CELL_NUM**2:
            return
        pos = self.random_cell()
        while pos in sandWorm_body or pos in self.items:
            pos = self.random_cell()
        self.items[pos] = Item(type, pos, items_data[type]['image'])
        self.items_num[type] += 1

    def kill(self, pos:Vector2):
        killed = self.items.pop((pos.x, pos.y))
        if self.items_num[killed.type] > 0:
            self.items_num[killed.type] -= 1
    
    def random_cell(self):
        x = random.randint(1, CELL_NUM)
        y = random.randint(1, CELL_NUM)
        return (x, y)
    
    def draw(self, surf):
        for item in self.items.values():
            item.draw(surf)
    
    def update(self, sandWorm_body:myData):
        if pygame.time.get_ticks() - self.spawn_last_reduction_time > self.spawn_reduction_timer:
            items_data['water']['spawn_time'] = max(10000, items_data['water']['spawn_time']-self.spawn_reduction_amount)
            items_data['baron']['spawn_time'] = max(10000, items_data['baron']['spawn_time']-self.spawn_reduction_amount)
            items_data['mother']['spawn_time'] = max(10000, items_data['mother']['spawn_time']-self.spawn_reduction_amount)
            self.spawn_last_reduction_time = pygame.time.get_ticks()

        for item in self.items.values():
            now = pygame.time.get_ticks()
            type = item.type
            if item.check_updated(now):
                self.kill(item.pos)
                # self.items_spawn_time[type] = now
                return
        for type in items_data:
            now = pygame.time.get_ticks()
            if now - self.items_spawn_time[type] > items_data[type]["spawn_time"]:
                if items_data[type]["max_num"] == None or self.items_num[type] < items_data[type]["max_num"]:
                    if type == 'muaddib': 
                        if random.random() <= items_data['muaddib']['generate_probi']:
                            self.add('muaddib', sandWorm_body)
                            self.items_spawn_time['muaddib'] = now
                        else:
                            self.items_spawn_time['muaddib'] = now
                    else:       
                        self.add(type, sandWorm_body)
                        self.items_spawn_time[type] = now
    
    def collideWith(self, head:Vector2):
        coor_head = (head.x, head.y)
        if coor_head in self.items and self.items[coor_head].alpha == 255:
            item = self.items[coor_head]
            self.kill(item.pos)
            return item.type

    def items_all_random(self, sandWorm_body:myData):
        help_items = self.items.copy()
        self.items.clear()
        for item in help_items.values():
            pos = self.random_cell()
            while pos in sandWorm_body or pos in self.items or pos in help_items:
                pos = self.random_cell()
            self.items[pos] = Item(item.type, pos, items_data[item.type]['image'])
        help_items = None

    def update_last_time_after_stop(self, pause, now):
        for item in self.items.values():
            item.last_update_time += now-pause
        for item in self.items_spawn_time:
            self.items_spawn_time[item] += now-pause
        self.spawn_last_reduction_time += now-pause