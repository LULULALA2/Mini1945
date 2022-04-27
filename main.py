import pygame
from time import sleep
from random import *


# 규칙
# gameover: 적 3개 지나치면 or 적과 충돌
# score: 적 격추 (10점씩)
# ❤💔

# 색상 세팅(RGB코드)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 게임화면 생성 및 설정
screen_width = 480
screen_height = 640

background = pygame.image.load("images/background.jpg")

pygame.mixer.init()
bgm = pygame.mixer.music.load('sound/bgm.mp3')
pygame.mixer.music.play(-1)
bgm_v = pygame.mixer.music.get_volume()
pygame.mixer.music.set_volume(bgm_v - 0.8)

s_shot = pygame.mixer.Sound("sound/shot.wav")
s_kill = pygame.mixer.Sound('sound/kill.wav')
s_stageup = pygame.mixer.Sound("sound/stageup.wav")
s_gameover = pygame.mixer.Sound("sound/gameover.wav")
s_stageup, s_gameover.set_volume(0.3)
s_shot, s_kill.set_volume(0.2)


def mainMessage(text):
    global gameDisplay
    textfont = pygame.font.Font(None, 80)
    text = textfont.render(text, True, RED)
    textpos = text.get_rect()
    textpos.center = (screen_width / 2, screen_height / 2)
    gameDisplay.blit(text, textpos)

def ending():
    pygame.display.update()
    sleep(4)
    gameStart()

def life_DOWN(count):
    global gameDisplay
    font = pygame.font.SysFont(None, 35)
    text = font.render('Life : ' + str(count), True, RED)
    gameDisplay.blit(text, (350, 10))

def score(count):
    global gameDisplay
    font = pygame.font.Font(None, 35)
    text = font.render('Score : ' + str(count), True, RED)
    gameDisplay.blit(text, (10, 10))

def stage(count):
    global gameDisplay
    font = pygame.font.Font(None, 35)
    text = font.render('Stage : ' + str(count), True, WHITE)
    gameDisplay.blit(text, (180, 10))

def stageUP(count):
    global gameDisplay
    textfont = pygame.font.Font(None, 60)
    text = textfont.render('Stage ' + str(count), True, WHITE)
    textpos = text.get_rect()
    textpos.center = (screen_width / 2, screen_height / 2)
    gameDisplay.blit(text, textpos)
    pygame.display.update()
    s_stageup.play()
    sleep(1)

def gameOver(msg):
    global gameDisplay
    mainMessage(msg)
    pygame.display.update()
    s_gameover.play()
    sleep(1)
    gameDisplay.fill(BLACK)
    mainMessage('Game Over')
    ending()

# 게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gameDisplay
    gameDisplay.blit(obj, (x, y))


# 게임 시작!
def gameStart():
    global gameDisplay, player, enemy, bullet, shotzone, clock

    stage_lv = 1

    # 플레이어 정보 (크기, 위치, 속도 등)
    player_life = 3

    player_size = player.get_rect().size
    player_width = player_size[0]
    player_x_pos = (screen_width / 2) - (player_width / 2)
    player_y_pos = screen_height - player_width - 40
    player_to_x_left = 0
    player_to_x_right = 0

    player_speed = 3
    to_x = 0

    enemy_size = enemy.get_rect().size
    enemy_width = enemy_size[0]
    enemy_height = enemy_size[1]
    enemy_x_pos = randint(0, (screen_width - enemy_width))
    enemy_y_pos = 0

    enemy_speed = 3

    shotzone_size = shotzone.get_rect().size
    shotzone_width = shotzone_size[0]
    shotzone_height = shotzone_size[1]

    bullet_size = bullet.get_rect().size
    bullet_width = bullet_size[0]
    bullet_height = bullet_size[1]

    isShot = False
    shotcount = 0
    bullets = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 키를 누르고 있을 때 (좌우 + space)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_to_x_left -= player_speed
                elif event.key == pygame.K_RIGHT:
                    player_to_x_right += player_speed

                elif event.key == pygame.K_SPACE:  # 공격키

                    bullet_x_pos = (player_x_pos + player_width / 2) - (bullet_width / 2)
                    bullet_y_pos = player_y_pos

                    bullets.append([bullet_x_pos, bullet_y_pos])

                    s_shot.play()

            # 키를 뗄 때 (멈춤)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player_to_x_left = 0
                elif event.key == pygame.K_RIGHT:
                    player_to_x_right = 0

        gameDisplay.blit(background, (0, 0))


        # 플레이어 위치, 화면 안에서 움직이게 하기
        player_x_pos += player_to_x_left + player_to_x_right

        if player_x_pos < 0:
            player_x_pos = 0

        elif player_x_pos > screen_width - player_width:
            player_x_pos = screen_width - player_width

        # 적이 아래로 계속 내려옴
        enemy_y_pos += enemy_speed

        if enemy_y_pos > screen_height:
            player_life -= 1
            s_kill.play()
            enemy_y_pos = 0
            enemy_x_pos = randint(0, (screen_width - enemy_width))

        ## GameOver event 1) life = 0
        if player_life == 0:
            gameOver("No life")

        # 충돌 처리 (플레이어가 이동한 좌표에 영역설정)
        player_rect = player.get_rect()
        player_rect.left = player_x_pos
        player_rect.top = player_y_pos

        enemy_rect = enemy.get_rect()
        enemy_rect.left = enemy_x_pos
        enemy_rect.top = enemy_y_pos

        shotzone_x_pos = enemy_x_pos + (enemy_width * 1 / 4)
        shotzone_y_pos = enemy_y_pos + (enemy_height * 1 / 4)
        shotzone_rect = shotzone.get_rect()
        shotzone_rect.left = shotzone_x_pos
        shotzone_rect.top = shotzone_y_pos

        ## GameOver event 2) 적과 충돌했는지 체크
        # (충돌시 life와 관계없이 바로 게임오버)

        if player_rect.colliderect(enemy_rect):
            drawObject(player, player_x_pos, player_y_pos)
            gameOver("Crashed!!")

        # 화면에 이미지 그리기
        drawObject(player, player_x_pos, player_y_pos)
        drawObject(enemy, enemy_x_pos, enemy_y_pos)

        life_DOWN(player_life)
        score(shotcount)
        stage(stage_lv)


        # 총을 쐈을 때,
            # 총알이 계속 위로 나감
        if len(bullets) != 0: # 계속 나가는 총알들 반복
            for i, bullet_xy in enumerate(bullets):
                bullet_xy[1] -= 10 # 총알좌표리스트에서 인덱스[1]은 y좌표 (y좌표 -10)
                bullets[i][1] = bullet_xy[1] # 리스트에서 계속 꺼내오는 총알 전부 10씩 위로 이동

                bullet_rect = bullet.get_rect()
                bullet_rect.left = bullet_x_pos
                bullet_rect.top = bullet_y_pos
                # 총알을 맞추면 적 격추
                if bullet_rect.colliderect(shotzone_rect):
                    drawObject(shotzone, shotzone_x_pos, shotzone_y_pos)
                    s_kill.play()
                    bullets.remove(bullet_xy)
                    isShot = True
                    shotcount += 10

                    # 적 비행기를 일정 횟수 처치하면 스테이지 +1, 적 비행기속도 1.5배
                    # stage 2
                    if shotcount == 70:
                        enemy_speed *= 1.5
                        stage_lv += 1
                        stageUP(stage_lv)
                        stage(stage_lv)

                    # stage 3
                    if shotcount == 150:
                        enemy_speed *= 1.5
                        stage_lv += 1
                        stageUP(stage_lv)
                        stage(stage_lv)

                # 총알이 화면밖을 벗어나면
                if bullet_xy[1] <= (0 - bullet_height):
                    try:
                        bullets.remove(bullet_xy)  # 밖으로 나간 총알 제거
                    except:
                        pass

        # bullets(총알좌표리스트)에 있는 총알들을 다 화면에 그려줘야함
        if len(bullets) != 0:
            for bullet_x_pos, bullet_y_pos in bullets:
                drawObject(bullet, bullet_x_pos, bullet_y_pos)

        # 적이 총알에 맞으면
        if isShot:
            enemy_x_pos = randint(0, (screen_width - enemy_width))
            enemy_y_pos = 0
            isShot = False

        drawObject(enemy, enemy_x_pos, enemy_y_pos)

        pygame.display.update()  # 게임화면을 계속 업뎃해줌
        clock.tick(60)  # FPS = 60

    # 게임 종료
    pygame.quit()


# 게임 초기화 함수
def initGame():
    global gameDisplay, player, enemy, bullet, clock, shotzone  # 게임이 진행될 게임 화면, 게임의 초당 프레임(FPS), 비행기 변수 선언, 적 선언

    pygame.init()
    gameDisplay = pygame.display.set_mode((screen_width, screen_height))  # 게임화면의 가로세로크기를 설정
    pygame.display.set_caption('Mini 1945')

    player = pygame.image.load('images/player.png')
    enemy = pygame.image.load('images/enemy.png')
    bullet = pygame.image.load('images/bullet.png')
    shotzone = pygame.image.load('images/shotzone.png')

    clock = pygame.time.Clock()  # 초당 프레임수를 설정할 수 있는 Clock 객체 생성


initGame()
gameStart()