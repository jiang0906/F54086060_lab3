import pygame
import math
import os
from settings import PATH_LEFT, PATH_RIGHT

pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))

# 為了區分兩路，特別設另一個名稱來方便後面可互相取代
PATH_ALT = PATH_LEFT

class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        self.path = PATH_ALT
        self.path_index = 0
        self.path_alt = 0
        self.move_count = 0
        self.stride = 1
        self.x, self.y = self.path[0]

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        pygame.draw.rect(win, (0, 255, 0), [self.x - self.width // 2, self.y - self.height // 2 - 10, 20, 5])
        pygame.draw.rect(win, (255, 0, 0), [self.x - self.width // 2 + 20, self.y - self.height // 2 - 10, 20, 5])

    def move(self):
        ax, ay = self.path[self.path_index]  # x, y position of point A
        bx, by = self.path[self.path_index + 1]
        distance_a_b = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
        max_count = int(distance_a_b / self.stride)

        if self.move_count < max_count:
            unit_vector_x = (bx - ax) / distance_a_b
            unit_vector_y = (by - ay) / distance_a_b
            delta_x = unit_vector_x * self.stride
            delta_y = unit_vector_y * self.stride

            # 更新每一步的座標以及下一步的準備
            self.x += delta_x
            self.y += delta_y
            self.move_count += 1

        # 一旦大於max_count後，就是準備下一步的動作
        if self.move_count >= max_count:
            self.path_index += 1
            self.move_count = 0

        # 用奇數偶數餘數不同來區別觸發不同的路徑
        global PATH_ALT
        if self.path_alt % 2 == 1:
            PATH_ALT = PATH_RIGHT
        else:
            PATH_ALT = PATH_LEFT
        self.path_alt += 1


class EnemyGroup:
    def __init__(self):
        self.gen_count = 0
        self.gen_period = 120   # (unit: frame)
        self.reserved_members = []
        self.expedition = [Enemy()]

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        # 前者為達成週期為120幀之條件，後者為產生的敵人庫存要進if消掉
        if self.gen_count % self.gen_period == 0 and len(self.reserved_members) != 0:
            self.expedition.append(self.reserved_members.pop())
        self.gen_count += 1

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        # 生產出主程式那邊輸入的3個敵人後，則進入campaign
        for i in range(num):
            self.reserved_members.append(Enemy())

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)





