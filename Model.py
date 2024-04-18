from typing import List
from Config import *
import pygame as pg
pg.init()

end_sound = pg.mixer.Sound("KO.wav")
end_sound.set_volume(0.2)
class Food:
    """
    食物物件，初始化方法為 `Food((左上角 x, 左上角 y))`
    `self.pos_x` 及 `self.pos_y` 為食物的座標
    """

    def __init__(self, pos):
        self.surf = pg.surface.Surface(size=(SNAKE_SIZE, SNAKE_SIZE))
        self.surf.fill(FOOD_COLOR)
        self.rect = self.surf.get_rect(topleft=pos)

    @property
    def pos_x(self):
        return self.rect.topleft[0]

    @property
    def pos_y(self):
        return self.rect.topleft[1]


class Poison:
    """
    毒藥物件，初始化方法為 `Poison((左上角 x, 左上角 y))`
    `self.pos_x` 及 `self.pos_y` 為毒藥的座標
    """

    def __init__(self, pos):
        self.surf = pg.surface.Surface(size=(SNAKE_SIZE, SNAKE_SIZE))
        self.surf.fill(POISON_COLOR)
        self.rect = self.surf.get_rect(topleft=pos)

    @property
    def pos_x(self):
        return self.rect.topleft[0]

    @property
    def pos_y(self):
        return self.rect.topleft[1]


class Wall:
    """
    牆壁物件，初始化方法為 `Wall((左上角 x, 左上角 y))`
    `self.pos_x` 及 `self.pos_y` 為牆壁的座標
    """

    def __init__(self, pos):
        self.surf = pg.surface.Surface(size=(SNAKE_SIZE, SNAKE_SIZE))
        self.surf.fill(WALL_COLOR)
        self.rect = self.surf.get_rect(topleft=pos)

    @property
    def pos_x(self):
        return self.rect.topleft[0]

    @property
    def pos_y(self):
        return self.rect.topleft[1]


class Player:
    """
    玩家物件
    `self.snake_list` 紀錄每一段蛇的資訊 `(左上 x, 左上 y, 寬, 高)`
    `self.head_x` 及 `self.head_y` 為蛇頭的座標
    `self.length` 為蛇的長度
    """

    def __init__(self):
        self.snake_list = [[200, 100, SNAKE_SIZE, SNAKE_SIZE]]

    @property
    def head_x(self):
        return self.snake_list[0][0]

    @property
    def head_y(self):
        return self.snake_list[0][1]

    @property
    def length(self):
        return len(self.snake_list)

    # 以下為大作業

    def new_block(self, new_pos) -> None:
        """
        將新一節蛇身的資訊加到 `snake_list` 最後面，無回傳值

        Keyword arguments:
        new_pos -- 新一節蛇身的座標 (左上 x, 左上 y)
        """
        self.snake_list.append((new_pos[0],new_pos[1] ,SNAKE_SIZE,SNAKE_SIZE))

    def draw_snake(self, screen) -> None:
        """
        畫出蛇，顏色要黃藍相間，無回傳值
        顏色可以用 `SNAKE_COLOR_YELLOW` 及 `SNAKE_COLOR_BLUE`
        可以用 `pg.draw.rect(screen 物件, 顏色, (座標 x, 座標 y, 寬, 高))`

        Keyword arguments:
        screen -- pygame 螢幕物件
        """
        c = 0
        for block in self.snake_list:
            if c%2==0:
                pg.draw.rect(screen,SNAKE_COLOR_YELLOW,block)
                c+=1
            else:
                pg.draw.rect(screen,SNAKE_COLOR_BLUE,block)
                c+=1

        

    def check_border(self) -> bool:
        """
        判斷蛇的頭有沒有超出螢幕範圍
        有超出就回傳 `True`
        沒有超出回傳 `False`

        Return:
        bool -- 蛇的頭有沒有超出螢幕範圍
        """
        w,h = pg.display.get_surface().get_size()
        if self.head_x < 0 or self.head_x + 24 > w:
            end_sound.play()
            return True
        elif self.head_y < 0 or self.head_y + 24 > h:
            end_sound.play()
            return True
        else:
            return False

    def move(self, direction) -> None:
        """
        根據 `direction` 移動蛇的座標，無回傳值，`direction` 為哪個按鍵被按到
        -1: 其他
        0: 上
        1: 右
        2: 下
        3: 左
        方向的代號也可以直接使用 `UP`, `RIGHT`, `DOWN`, `LEFT`，在 `Config.py` 裡面定義好了

        Keyword arguments:
        direction -- 蛇的移動方向
        """
        if direction == 0:
            self.snake_list.insert(0,(self.head_x,self.head_y-25,SNAKE_SIZE,SNAKE_SIZE))
            self.snake_list.pop(-1)
        elif direction == 1:
            self.snake_list.insert(0,(self.head_x+25,self.head_y,SNAKE_SIZE,SNAKE_SIZE))
            self.snake_list.pop(-1)
        elif direction == 2:
            self.snake_list.insert(0,(self.head_x,self.head_y+25,SNAKE_SIZE,SNAKE_SIZE))
            self.snake_list.pop(-1)
        elif direction == 3:
            self.snake_list.insert(0,(self.head_x-25,self.head_y,SNAKE_SIZE,SNAKE_SIZE))
            self.snake_list.pop(-1)
        else:
            pass
            
       
        
       
    def detect_player_collision(self) -> bool:
        """
        判斷蛇的頭是否碰到蛇的其他段
        有碰到就回傳 `True`
        沒有碰到回傳 `False`

        Return:
        bool -- 是否碰到蛇 (自己) 的其他段
        """
        c=0
        flag = False
        for i,j,temp_size,temp_size in self.snake_list:
            if c == 0:
                c+=1
                continue
            else:
                d1 = abs( i - self.head_x)
                d2 = abs(j - self.head_y)
                if d1<25 and d2<25:
                    flag = True
                    break
                else:
                    continue
        if flag == True:
            end_sound.play()
            return True
        else:
            return False
                    

    def detect_wall_collision(self, walls: List[Wall]) -> bool:
        """
        判斷蛇的頭是否碰到牆壁
        有碰到就回傳 `True`
        沒有碰到回傳 `False`

        Keyword arguments:
        walls -- 牆壁物件的 list

        Return:
        bool -- 是否碰到牆壁
        """
        flag = False
        for wall in walls:
            disx = abs(wall.pos_x - self.head_x)
            disy = abs(wall.pos_y - self.head_y)
            if disx < 25 and disy < 25:
                end_sound.play()
                return True
            else:
                continue
        if flag == False:
            return False
        

    def detect_food_collision(self, foods: List[Food]) -> bool:
        """
        判斷蛇的頭是否碰到食物
        有碰到就回傳 `True`
        沒有碰到回傳 `False`

        Keyword arguments:
        foods -- 食物物件的 list

        Return:
        bool -- 是否碰到食物
        """
        for food in foods:
            i = food.pos_x
            j = food.pos_y
        d1 = abs( i - self.head_x)
        d2 = abs(j - self.head_y)
        if d1<25 and d2<25:
            return True
        else:
            return False

    def detect_poison_collision(self, poison: Poison) -> bool:
        """
        判斷蛇的頭是否碰到毒藥
        有碰到就回傳 `True`
        沒有碰到回傳 `False`

        Keyword arguments:
        poison -- 毒藥物件

        Return:
        bool -- 是否碰到毒藥
        """
        i = poison.pos_x
        j = poison.pos_y
        d1 = abs( i - self.head_x)
        d2 = abs(j - self.head_y)
        if d1<25 and d2<25:
            return True
        else:
            return False