from pygame import*

width = 700
height = 500

window = display.set_mode((width, height))
display.set_caption('Лабиринт')

background = transform.scale(image.load('background.jpg'),(width,height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def walk(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < height - 80:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < width - 80:
            self.rect.x += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def walk(self):
        if self.rect.x <= width - 250:
            self.direction = 'right'
        if self.rect.x >= width -80:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class wall(sprite.Sprite):
    def __init__(self, color1, color2, color3, wall_x, wall_y, width, height):
        super(). __init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill((color1, color2, color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

player = Player('homa.jpg', 5, height - 80, 5)
monster = Enemy('mam.jpg', width - 80, 280, 5)
gold = GameSprite('treasure.png', width - 120, height - 80, 0)

w1 = wall(187, 70, 202, 100, 20, 450, 10)
w2 = wall(187, 70, 202, 100, 480, 350, 10)
w3 = wall(187, 70, 202, 100, 20, 10, 380)
w4 = wall(187, 70, 202, 200, 150, 10, 330)
w5 = wall(187, 70, 202, 300, 20, 10, 330)
w6 = wall(187, 70, 202, 400, 20, 10, 330)

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')



game = True 
finish = False
FPS = 60
clock = time.Clock()

font.init()
font = font.Font(None, 35)
win = font.render('ай маладес вазьми орбузег у Миши', True, (0,0,0))
lose = font.render('ну трындыц', True, (0,0,0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background,(0,0))
        player.reset()
        monster.reset()
        gold.reset()
        player.walk()
        monster.walk()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
    
    if sprite.collide_rect(player, gold):
        finish = True
        window.blit(win, (100,200))
        money.play()

    if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, w6):
        finish =  True
        window.blit(lose, (200,200))
        kick.play()

    display.update()
    clock.tick(FPS)
