import pygame
from pygame import Vector2
import os
import random
from var import *

    
class Node:
    def __init__(self, vec:Vector2):
        self.pos = vec
        self.pre = None
        self.next = None

class myData:
    def __init__(self):
        self.head = None
        self.tail = None
        self.body = set()
    
    def put(self, vec:Vector2):
        if vec == None:
            return
        n = Node(vec)
        if self.tail == None:
            self.tail = n
        else:
            self.head.pre = n
            n.next = self.head
            self.body.add((self.head.pos.x, self.head.pos.y))
        self.head = n

    def get(self):
        if self.head == None:
            return
        cur = self.tail
        self.body.discard((cur.pos.x, cur.pos.y))
        self.tail = cur.pre
        self.tail.next = None
        cur.pre = None
        return cur.pos

    def __contains__(self, head_vec:tuple):
        return True if head_vec in self.body else False
    
    def __iter__(self):
        return iter(self.body)
    
    def __len__(self):
        return len(self.body)


class sandWorm:
    def __init__(self, length, x, y, opponent:bool=False):
        self.len = length
        self.body = myData()
        for i in range(length):
            self.body.put(Vector2(x+i, y))
        self.head = self.body.head
        self.dir = Vector2(1, 0)
        self.last_update_time = pygame.time.get_ticks()
        self.__init_rate = 150
        self.rate = 150

        self.sandworm_type = "opponent" if opponent else "sandworm"
        self.head_left = pygame.image.load(os.path.join('img', self.sandworm_type +'_head_1.png')).convert()
        self.head_left = pygame.transform.scale(self.head_left, (CELL_SIZE, CELL_SIZE))
        self.head_up = pygame.image.load(os.path.join('img', self.sandworm_type +'_head_2.png')).convert()
        self.head_up = pygame.transform.scale(self.head_up, (CELL_SIZE, CELL_SIZE))
        self.head_right = pygame.image.load(os.path.join('img', self.sandworm_type +'_head_3.png')).convert()
        self.head_right = pygame.transform.flip(self.head_right, False, True)
        self.head_right = pygame.transform.scale(self.head_right, (CELL_SIZE, CELL_SIZE))
        self.head_down = pygame.image.load(os.path.join('img', self.sandworm_type +'_head_4.png')).convert()
        self.head_down = pygame.transform.scale(self.head_down, (CELL_SIZE, CELL_SIZE))
        self.head_left.set_colorkey(WHITE)
        self.head_up.set_colorkey(WHITE)
        self.head_right.set_colorkey(WHITE)
        self.head_down.set_colorkey(WHITE)

        self.tail_left = pygame.image.load(os.path.join('img', self.sandworm_type +'_tail_1.png')).convert()
        self.tail_left = pygame.transform.scale(self.tail_left, (CELL_SIZE, CELL_SIZE))
        self.tail_up = pygame.image.load(os.path.join('img', self.sandworm_type +'_tail_2.png')).convert()
        self.tail_up = pygame.transform.scale(self.tail_up, (CELL_SIZE, CELL_SIZE))
        self.tail_right = pygame.image.load(os.path.join('img', self.sandworm_type +'_tail_3.png')).convert()
        self.tail_right = pygame.transform.flip(self.tail_right, False, True)
        self.tail_right = pygame.transform.scale(self.tail_right, (CELL_SIZE, CELL_SIZE))
        self.tail_down = pygame.image.load(os.path.join('img', self.sandworm_type +'_tail_4.png')).convert()
        self.tail_down = pygame.transform.scale(self.tail_down, (CELL_SIZE, CELL_SIZE))
        self.tail_left.set_colorkey(WHITE)
        self.tail_up.set_colorkey(WHITE)
        self.tail_right.set_colorkey(WHITE)
        self.tail_down.set_colorkey(WHITE)

        self.body_tl = pygame.image.load(os.path.join('img', self.sandworm_type +'_curve_1.png')).convert()
        self.body_tl = pygame.transform.scale(self.body_tl, (CELL_SIZE, CELL_SIZE))
        self.body_br = pygame.image.load(os.path.join('img', self.sandworm_type +'_curve_2.png')).convert()
        self.body_br = pygame.transform.scale(self.body_br, (CELL_SIZE, CELL_SIZE))
        self.body_bl = pygame.image.load(os.path.join('img', self.sandworm_type +'_curve_3.png')).convert()
        self.body_bl = pygame.transform.scale(self.body_bl, (CELL_SIZE, CELL_SIZE))
        self.body_tr = pygame.image.load(os.path.join('img', self.sandworm_type +'_curve_4.png')).convert()
        self.body_tr = pygame.transform.scale(self.body_tr, (CELL_SIZE, CELL_SIZE))
        self.body_tl.set_colorkey(WHITE)
        self.body_br.set_colorkey(WHITE)
        self.body_bl.set_colorkey(WHITE)
        self.body_tr.set_colorkey(WHITE)

        self.body_hori = pygame.image.load(os.path.join('img', self.sandworm_type +'_body_1.png')).convert()
        self.body_hori = pygame.transform.scale(self.body_hori, (CELL_SIZE, CELL_SIZE))
        self.body_vert_d = pygame.image.load(os.path.join('img', self.sandworm_type +'_body_4.png')).convert()
        self.body_vert_d = pygame.transform.scale(self.body_vert_d, (CELL_SIZE, CELL_SIZE))
        self.body_vert_u = pygame.image.load(os.path.join('img', self.sandworm_type +'_body_2.png')).convert()
        self.body_vert_u = pygame.transform.scale(self.body_vert_u, (CELL_SIZE, CELL_SIZE))
        self.body_hori.set_colorkey(WHITE)
        self.body_vert_d.set_colorkey(WHITE)
        self.body_vert_u.set_colorkey(WHITE)


    def draw(self, surf):
        if self.body.tail != None:
            tail_rect = (self.body.tail.pos.x*CELL_SIZE, self.body.tail.pos.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            surf.blit(self.update_tail_graphic(self.body.tail.pos, self.body.tail.pre.pos), tail_rect)
        cur = self.head.next
        while cur != self.body.tail:
            body_rect = (cur.pos.x*CELL_SIZE, cur.pos.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            surf.blit(self.update_body_graphic(cur.pos, cur.pre.pos, cur.next.pos), body_rect)
            cur = cur.next
        if self.head != None:
            head_rect = (self.head.pos.x*CELL_SIZE, self.head.pos.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            surf.blit(self.update_head_graphic(), head_rect)

    
    def update_head_graphic(self):
        if self.dir == Vector2(1, 0):
            return self.head_right
        elif self.dir == Vector2(-1, 0):
            return self.head_left
        elif self.dir == Vector2(0, 1):
            return self.head_down
        elif self.dir == Vector2(0, -1):
            return self.head_up
        # else:
        #     print(f'Error: Invalid Direction{self.dir}')
        #     return self.head_right
        
    def update_tail_graphic(self, tail_pos, pre_pos):
        if tail_pos.x == pre_pos.x:
            if tail_pos.y < pre_pos.y:
                return self.tail_down
            else:
                return self.tail_up
        else:
            if tail_pos.x < pre_pos.x:
                return self.tail_right
            else:
                return self.tail_left
            
    def update_body_graphic(self, pos, pre_pos, next_pos):
        rel_pre = next_pos - pos
        rel_next = pre_pos - pos
        body = self.body_hori
        if rel_pre.x == rel_next.x and rel_pre == Vector2(0, 1):
            body = self.body_vert_u
        elif rel_pre.x == rel_next.x and rel_pre == Vector2(0, -1):
            body = self.body_vert_d
        elif rel_pre.y == rel_next.y:
            body = self.body_hori
        else:
            if rel_pre.x == -1 and rel_next.y == -1 or rel_pre.y == -1 and rel_next.x == -1:
                body = self.body_br
            elif rel_pre.x == -1 and rel_next.y == 1 or rel_pre.y == 1 and rel_next.x == -1:
                body = self.body_tl
            elif rel_pre.x == 1 and rel_next.y == -1 or rel_pre.y == -1 and rel_next.x == 1:
                body = self.body_bl
            elif rel_pre.x == 1 and rel_next.y == 1 or rel_pre.y == 1 and rel_next.x == 1:
                body = self.body_tr
        return body
        

    def update(self):
        if self.body.tail == None or self.head == None:
            return
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.rate:
            self.body.get()
            new_head_pos = self.head.pos+self.dir
            self.body.put(new_head_pos)
            self.head = self.body.head
            self.last_update_time = now

    def time_stop_update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.rate:
            self.increase()
            self.last_update_time = now

    def increase(self, length=1):
        for _ in range(length):
            new_head_pos = self.head.pos+self.dir
            self.body.put(new_head_pos)
            self.head = self.body.head
            self.len += 1

    def decrease(self, length=1):
        for _ in range(length):
            if self.len < 1: break
            self.body.get()
            self.len -= 1

    def resetRate(self):
        self.rate = self.__init_rate

    def accelerate(self):
        self.rate = self.__init_rate >> 1

class opponentSandworm:
    def __init__(self):
        self.size = random.randint(3, 15)
        self.sandWorm = sandWorm(self.size, -self.size, random.randint(0, CELL_NUM - 1), True)

    def random_dir(self, a, b):      
        self.sandWorm.dir = Vector2(random.choice(a), random.choice(b))
        while self.sandWorm.dir == Vector2(0, 0) or self.sandWorm.dir == Vector2(1, 1) or self.sandWorm.dir == Vector2(-1, -1) or self.sandWorm.dir == Vector2(1, -1) or self.sandWorm.dir == Vector2(-1, 1):
            self.sandWorm.dir = Vector2(random.choice(a), random.choice(b))

    def is_head_surrounded(self):
        directions = [
            Vector2(1, 0),
            Vector2(-1, 0),
            Vector2(0, 1),
            Vector2(0, -1)
        ]
        
        for d in directions:
            next_pos = self.sandWorm.head.pos + d
            if (0 <= next_pos.x < CELL_NUM and 
                0 <= next_pos.y < CELL_NUM and 
                (next_pos.x, next_pos.y) not in self.sandWorm.body):
                return False
        return True

    def update(self):
        directions = [
        Vector2(1, 0), 
        Vector2(-1, 0),
        Vector2(0, 1),
        Vector2(0, -1)
        ]
        opposite_dir = -self.sandWorm.dir
        valid_directions = [d for d in directions if d != opposite_dir]

        if random.random() < 0.1:
            safe_directions = []
            for d in valid_directions:
                next_pos = self.sandWorm.head.pos + d
                if (0 <= next_pos.x < CELL_NUM) and (0 <= next_pos.y < CELL_NUM):
                    if (next_pos.x, next_pos.y) not in self.sandWorm.body:
                        safe_directions.append(d)

            if safe_directions:
                self.sandWorm.dir = random.choice(safe_directions)
            else:
                reverse_pos = self.sandWorm.head.pos + opposite_dir
                if (0 <= reverse_pos.x < CELL_NUM) and (0 <= reverse_pos.y < CELL_NUM) and (reverse_pos.x, reverse_pos.y) not in self.sandWorm.body:
                    self.sandWorm.dir = opposite_dir

        
        next_head_pos = self.sandWorm.head.pos + self.sandWorm.dir
        if (0 <= next_head_pos.x < CELL_NUM) and (0 <= next_head_pos.y < CELL_NUM):
            if (next_head_pos.x, next_head_pos.y) not in self.sandWorm.body:
                self.sandWorm.update()
            else:
                if self.is_head_surrounded():
                    return 'head'
                
                
        else:
            if (self.sandWorm.head.pos.x == 0 and self.sandWorm.dir.x == -1
                or self.sandWorm.head.pos.x == CELL_NUM-1 and self.sandWorm.dir.x == 1):
                self.random_dir([0], [1, -1])
            elif (self.sandWorm.head.pos.y == 0 and self.sandWorm.dir.y == -1
                or self.sandWorm.head.pos.y == CELL_NUM-1 and self.sandWorm.dir.y == 1):
                self.random_dir([1, -1], [0])
            elif self.sandWorm.head.pos == Vector2(0, 0) and self.sandWorm.dir == Vector2(-1, 0):
                self.sandWorm.dir = Vector2(0, 1)
            elif self.sandWorm.head.pos == Vector2(0, 0) and self.sandWorm.dir == Vector2(0, -1):
                self.sandWorm.dir = Vector2(1, 0)
            elif self.sandWorm.head.pos == Vector2(CELL_NUM-1, 0) and self.sandWorm.dir == Vector2(1, 0):
                self.sandWorm.dir = Vector2(0, 1)
            elif self.sandWorm.head.pos == Vector2(CELL_NUM-1, 0) and self.sandWorm.dir == Vector2(0, -1):
                self.sandWorm.dir = Vector2(-1, 0)
            elif self.sandWorm.head.pos == Vector2(0, CELL_NUM-1) and self.sandWorm.dir == Vector2(-1, 0):
                self.sandWorm.dir = Vector2(0, -1)
            elif self.sandWorm.head.pos == Vector2(0, CELL_NUM-1) and self.sandWorm.dir == Vector2(0, 1):
                self.sandWorm.dir = Vector2(1, 0)
            elif self.sandWorm.head.pos == Vector2(CELL_NUM-1, CELL_NUM-1) and self.sandWorm.dir == Vector2(1, 0):
                self.sandWorm.dir = Vector2(0, -1)
            elif self.sandWorm.head.pos == Vector2(CELL_NUM-1, CELL_NUM-1) and self.sandWorm.dir == Vector2(0, 1):
                self.sandWorm.dir = Vector2(-1, 0)


    def draw(self, surf):
        self.sandWorm.draw(surf)

    def check_collision_with_player(self, player_head:Vector2):
        if player_head == self.sandWorm.head.pos:
            return 'head'
        elif (player_head.x, player_head.y) in self.sandWorm.body:
            return 'body'
        return None