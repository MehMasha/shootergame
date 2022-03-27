from pygame import *
from random import randint
 

#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
    
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
    
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self): ###
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

lost = 0 
score = 0
 
class Enemy(GameSprite):
    def update(self):
        global lost
        global score 
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -100
            self.rect.x = randint(0, 600)
            if self.speed == 5:
                score -= 1
            elif self.speed == 4:
                score -= 5
            elif self.speed == 3:
                score -= 10
            elif self.speed == 2: 
                score -= 15
            else: 
                score -= 20
            # score -= 5
            self.speed = randint(1, 5)
            lost += 1


class Bullet(GameSprite): ################
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()




#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

menu = transform.scale(image.load('images.jpg'), (win_width, win_height))


screamer = transform.scale(image.load('ast.png'), (win_width, win_height)) 
scream = mixer.Sound('fire.ogg') 
 
#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0, 600), -100, 80, 50, randint(1, 5)) 
    monsters.add(monster)



asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(0, 600), -100, 80, 50, randint(1, 5))
    asteroids.add(asteroid)




fire_sound = mixer.Sound('fire.ogg') 
bullets = sprite.Group() 


bullets_count = 0 ###########


lifes = 1000

font.init() 
font2 = font.SysFont('Arial', 40)
font1 = font.SysFont('Arial', 20)
menutext = font2.render('Нажмите R для продолжения игры', True, (255, 0, 0))
losetext = font2.render('Вы проиграли!', True, (255, 0, 0)) #######
wintext = font2.render('Вы выиграли!', True, (255, 0, 0)) #######
menutext2 = font2.render('', True, (255, 0, 0)) #######



finish = False
pause = 1
#Основной цикл игры:
run = True 
while run:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN: 
            if e.key == K_p:
                finish = True
                pause = 1
            if e.key == K_r:
                finish = False
            if e.key == K_l: 
                score = 0
                lost = 0
                for m in monsters:
                    m.rect.y = -100
            if e.key == K_SPACE and bullets_count < 10: ########
                fire_sound.play()
                ship.fire()
                bullets_count += 1 ######
                waittime = 0 #######


    
    if not finish:
        window.blit(background,(0,0))
        ship.update()
        ship.reset()

        monsters.update()
        monsters.draw(window)


        bullets.update()
        bullets.draw(window)

        asteroids.update()
        asteroids.draw(window)

        
        lifestext = font2.render(str(lifes), 1, (255, 0, 0))
        window.blit(lifestext, (500, 10))


        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 0, 0))
        window.blit(text_lose, (10, 10))
        text_score = font1.render('Счет: ' + str(score), 1, (255, 0, 0)) 
        window.blit(text_score, (10, 30)) 
    
        if ship.rect.y < 0: 
            window.blit(screamer, (0,0))
            scream.play()
        



        if bullets_count == 10 and waittime < 120: ########
            text = font2.render('Перезарядка', True, (255, 0, 0))
            window.blit(text, (200, 200))
            waittime += 1
        elif bullets_count == 10 and waittime >= 120:
            waittime = 0
            bullets_count = 0
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            monster = Enemy('ufo.png', randint(0, 600), -100, 80, 50, randint(1, 5))
            monsters.add(monster)
            score += 10




        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            if sprite.spritecollide(ship, monsters, True):
                monster = Enemy('ufo.png', randint(0, 600), -100, 80, 50, randint(1, 5))
                monsters.add(monster)
            if sprite.spritecollide(ship, asteroids, True):
                asteroid = Enemy('asteroid.png', randint(0, 600), -100, 80, 50, randint(1, 5))
                asteroids.add(asteroid)
            lifes -= 1
        
        if lifes <= 0 or lost > 5:
            finish = True
            menutext2 = losetext
            pause = 0






        if score > 100:
            finish = True
            menutext2 = wintext
            pause = 0

    else: 
        if pause:
            window.blit(menu, (0,0))
            window.blit(menutext, (200, 200))
        else:
            window.blit(menu, (0,0))
            window.blit(menutext2, (100, 100))
            score = 0
            lost = 0
            bullets_count = 0
            ship.rect.x = 300
            ship.rect.y = 400
            for m in monsters:
                m.rect.x = randint(0, 600)
                m.rect.y = -100
            for b in bullets:
                b.kill()
            finish = False
            display.update()

            time.delay(3000)
    
    display.update()
    
    time.delay(20)