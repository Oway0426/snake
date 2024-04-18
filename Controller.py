from typing import List
import pygame as pg
from Config import *
from Model import *
import random


def key_input(pressed_keys: List):
    """
    從 pygame 的鍵盤輸入判斷哪些按鍵被按下
    回傳方向
    """
    for key in pressed_keys:
        if key == pg.K_UP:
            movement = UP
            break
        if key == pg.K_DOWN:
            movement = DOWN
            break
        if key == pg.K_LEFT:
            movement = LEFT
            break
        if key == pg.K_RIGHT:
            movement = RIGHT
            break
        if key == pg.K_a:
            return "new"
    else:
        return None
    return movement


# 以下為大作業


def generate_wall(walls: List[Wall], player: Player, direction: int) -> None:
    """
    生成一個 `Wall` 的物件並加到 `walls` 裡面，不能與現有牆壁或玩家重疊
    新牆壁一定要與現有牆壁有接觸 (第一階段)，更好的話請讓牆壁朝著同個方向生長 (第二階段)
    無回傳值

    Keyword arguments:
    walls -- 牆壁物件的 list
    player -- 玩家物件
    direction -- 蛇的移動方向
    """
    w, h = pg.display.get_surface().get_size()
    while True:
        if len(walls) == 0:
            (w1, h1) = (random.randint(0, w - 25), random.randint(0, h - 25))
            
            walls.append(Wall(pos=(w1,h1)))
            break
        elif direction == 0:
            min1 = h
            y = []
            for wall in walls:
                if wall.pos_y == min1:
                    y.append([wall.pos_x,wall.pos_y-25])
                elif wall.pos_y < min1:
                    min1 = wall.pos_y
                    y.clear()
                    y = [[wall.pos_x,wall.pos_y-25]]
                else:
                    continue
            if y[0][1] < 0:
                direction = 1
                continue
            else:
                if len(y) == 1:
                    if abs(y[0][0] - player.head_x) < 25 or abs(y[0][1]-player.head_y) < 25:
                        return direction
                    else:
                        walls.append(Wall(pos=(y[0])))
                        return direction
                else:
                    if abs(y[0][0] - player.head_x) < 25 or abs(y[0][1]-player.head_y) < 25:
                        return direction
                    else:

                        random_wall = random.randint(0,len(y)-1)
                        walls.append(Wall(pos=(y[random_wall])))
                        return direction
        elif direction == 1:
            y = []
            max1 = 0
            for wall in walls:
                if wall.pos_x == max1:
                    y.append([wall.pos_x+25,wall.pos_y])
                elif wall.pos_x > max1:
                    max1 = wall.pos_x
                    y.clear()
                    y = [[wall.pos_x+25,wall.pos_y]]
                else:
                    continue
            if y[0][0]>w:
                direction = 2
                continue
            else:
                if len(y) == 1:
                    if abs(y[0][0] - player.head_x) < 25 or abs(y[0][1]-player.head_y) < 25:
                        return direction
                    else:
                        walls.append(Wall(pos=(y[0])))
                        return direction
                else:
                    if abs(y[0][0] - player.head_x) < 25 or abs(y[0][1]-player.head_y) < 25:
                        return direction
                    else:
                        random_wall = random.randint(0,len(y)-1)
                        walls.append(Wall(pos=(y[random_wall])))
                        return direction
        elif direction == 2:
            y = []
            max1 = 0
            for wall in walls:
                if wall.pos_y == max1:
                    y.append([wall.pos_x,wall.pos_y+25])
                elif wall.pos_y > max1:
                    max1 = wall.pos_y
                    y.clear()
                    y = [[wall.pos_x,wall.pos_y+25]]
                else:
                    continue
            if y[0][1] > h-25:
                direction = 3
                continue
            else:
                if len(y) == 1:
                    walls.append(Wall(pos=(y[0])))
                    return direction
                else:
                    random_wall = random.randint(0,len(y)-1)
                    walls.append(Wall(pos=(y[random_wall])))
                    return direction
        elif direction == 3:
            y = []
            min1 = w
            for wall in walls:
                if wall.pos_x == min1:
                    y.append([wall.pos_x-25,wall.pos_y])
                elif wall.pos_y < min1:
                    min1 = wall.pos_x
                    y.clear()
                    y = [[wall.pos_x-25,wall.pos_y]]
                else:
                    continue
            if y[0][0] < 0:
                direction = 0
                continue
            else:
                if len(y) == 1:
                    if abs(y[0][0] - player.head_x) < 25 or abs(y[0][1]-player.head_y) < 25:
                        return direction
                    else:
                        walls.append(Wall(pos=(y[0])))
                        return direction
                else:
                    if abs(y[0][0] - player.head_x) < 25 or abs(y[0][1]-player.head_y) < 25:
                        return direction
                    else:
                        random_wall = random.randint(0,len(y)-1)
                        walls.append(Wall(pos=(y[random_wall])))
                        return direction
        else:
            continue

                


    


def generate_food(foods: List[Food], walls: List[Wall], player: Player) -> None:
    """
    在隨機位置生成一個 `Food` 的物件並加到 `foods` 裡面，不能與現有牆壁或玩家重疊
    無回傳值

    Keyword arguments:
    foods -- 食物物件的 list
    walls -- 牆壁物件的 list
    player -- 玩家物件
    """
    w, h = pg.display.get_surface().get_size()
    while True:
        flag = True
        (w1, h1) = (random.randint(0, w - 25), random.randint(0, h - 25))
        for wall in walls:
            i = wall.pos_x
            j = wall.pos_y
            dist = abs(w1 - i)
            dist1 = abs(h1 - j)
            if dist < 25 or dist1 < 25:
                flag = False
                break
            else:
                continue
        for k, q,temp_size,temp_size in player.snake_list:
            d = abs(w1 - k)
            d1 = abs(h1 - q)
            if d < 25 or d1 < 25:
                flag = False
                break
            else:
                continue
        if flag:
            foods.append(Food(pos=(w1, h1)))
            break
                


def generate_poison(walls: List[Wall], foods: List[Food], player: Player) -> None:
    """
    在隨機位置生成一個 `Poison` 的物件並回傳，不能與現有其他物件或玩家重疊

    Keyword arguments:
    walls -- 牆壁物件的 list
    foods -- 食物物件的 list
    player -- 玩家物件
    """
    w, h = pg.display.get_surface().get_size()
    while True:
        flag = True
        (w1, h1) = (random.randint(0, w - 25), random.randint(0, h - 25))
        for wall in walls:
            i = wall.pos_x
            j = wall.pos_y
            dist = abs(w1 - i)
            dist1 = abs(h1 - j)
            if dist < 25 or dist1 < 25:
                flag = False
                break
            else:
                continue
        for kk,qr,temp_size,temp_size in player.snake_list:
            d = abs(w1 - kk)
            d1 = abs(h1 - qr)
            if d < 25 or d1 < 25:
                flag = False
                break
            else:
                continue
        for food in foods:
            dis_x = food.pos_x
            dis_y = food.pos_y
            d2 = abs(w1 - dis_x)
            d3 = abs(h1 -dis_y)
            if d2 < 25 or d3 < 25:
                flag = False
                break
            else:
                continue
        if flag:
            return Poison(pos=(w1,h1)) 
    


def calculate_time_interval(player: Player) -> int:
    """
    根據蛇的長度，計算並回傳每一秒有幾幀
    蛇的長度每增加 4 幀數就 +1，從小到大，最大為 `TIME_INTERVAL_MAX`，最小為 `TIME_INTERVAL_MIN`
    """
    return TIME_INTERVAL_MIN
