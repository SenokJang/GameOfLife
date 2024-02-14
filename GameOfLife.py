from os import system
system("pip3 install pygame")
system("pip3 install numpy")


import tkinter as tk

root = tk.Tk()
root.withdraw()  # 창을 나타나지 않도록 설정

# 화면의 너비와 높이 가져오기
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# print("화면 너비:", screen_width)
# print("화면 높이:", screen_height)



import pygame
import numpy as np

# 화면 설정
pygame.init()

width, height = screen_width, screen_height  # 초기값 설정
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")

# 색깔 설정
bg = 25, 25, 25
white = 255, 255, 255

# 셀 크기와 격자 설정
nxC, nyC = int(screen_width/20), int(screen_height/20)
dimCW = width / nxC
dimCH = height / nyC

# 초기 상태 설정
gameState = np.zeros((nxC, nyC))

# 마우스 클릭 이벤트 처리 함수
def handle_mouse_click(pos):
    cell_x, cell_y = int(pos[0] / dimCW), int(pos[1] / dimCH)
    gameState[cell_x, cell_y] = 1 if gameState[cell_x, cell_y] == 0 else 0

# 콘웨이의 생명 게임 알고리즘 적용 함수
def apply_game_of_life():
    global gameState
    newGameState = np.copy(gameState)

    for x in range(nxC):
        for y in range(nyC):
            # 주변 이웃 확인
            n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                      gameState[(x)     % nxC, (y - 1) % nyC] + \
                      gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                      gameState[(x - 1) % nxC, (y)     % nyC] + \
                      gameState[(x + 1) % nxC, (y)     % nyC] + \
                      gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                      gameState[(x)     % nxC, (y + 1) % nyC] + \
                      gameState[(x + 1) % nxC, (y + 1) % nyC]

            # 규칙 적용
            if gameState[x, y] == 0 and n_neigh == 3:
                newGameState[x, y] = 1
            elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                newGameState[x, y] = 0

    gameState = np.copy(newGameState)


# 세포의 속도
speed = 10


# 게임 시작 여부
gameStarted = False

# 게임 루프
running = True
while running:
    screen.fill(bg)
    pygame.time.wait(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not gameStarted:  # Left mouse button
                handle_mouse_click(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter key
                gameStarted = not gameStarted

    # 게임이 시작되지 않았다면 마우스로 생성된 셀을 계속해서 그리기
    if not gameStarted:
        for x in range(nxC):
            for y in range(nyC):
                poly = [(x * dimCW, y * dimCH),
                        ((x + 1) * dimCW, y * dimCH),
                        ((x + 1) * dimCW, (y + 1) * dimCH),
                        (x * dimCW, (y + 1) * dimCH)]

                if gameState[x, y] == 1:
                    pygame.draw.polygon(screen, white, poly, 0)
                else:
                    pygame.draw.polygon(screen, bg, poly, 1)
    # 게임이 시작된 후에는 콘웨이의 생명 게임 알고리즘 적용
    else:
        apply_game_of_life()
        # 그리기
        for x in range(nxC):
            for y in range(nyC):
                poly = [(x * dimCW, y * dimCH),
                        ((x + 1) * dimCW, y * dimCH),
                        ((x + 1) * dimCW, (y + 1) * dimCH),
                        (x * dimCW, (y + 1) * dimCH)]

                if gameState[x, y] == 1:
                    pygame.draw.polygon(screen, white, poly, 0)
                else:
                    pygame.draw.polygon(screen, bg, poly, 1)

    # 화면 업데이트
    pygame.display.flip()

pygame.quit()
