import os
import sys
import math

import pygame
import requests


def get_image(x, y, theme):
    server_address = 'https://static-maps.yandex.ru/v1?'
    api_key = '1c61eb4c-5ad0-4d78-9b19-b45653666b96'
    ll_spn = f'll={x},{y}&z={z}&theme={theme}'
    map_request = f"{server_address}{ll_spn}&apikey={api_key}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


LAT_STEP = 0.025  # Шаги при движении карты по широте и долготе
LON_STEP = 0.01926
x, y = map(float, input('Введите координаты объекта: ').split(','))
z = int(input('Введите масштаб карты: '))
zxc = 1
map_file = get_image(x, y, 'dark')
pygame.init()
screen = pygame.display.set_mode((600, 450))
FPS = 60
clock = pygame.time.Clock()
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
run = True
while run:
    for event in pygame.event.get():
        if pygame.event.wait().type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
            if z <= 20:
                z += 1
            map_file = get_image(x, y, theme)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
            if z >= 1:
                z -= 1
            map_file = get_image(x, y, theme)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                get_image(x, y - LON_STEP * math.pow(2, 15 - z), theme)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            if event.key == pygame.K_UP:
                get_image(x, y + LON_STEP * math.pow(2, 15 - z), theme)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            if event.key == pygame.K_LEFT:
                get_image(x - LAT_STEP * math.pow(2, 15 - z), y, theme)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            if event.key == pygame.K_RIGHT:
                get_image(x + LAT_STEP * math.pow(2, 15 - z), y, theme)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if zxc % 2 != 0:
                    theme = 'light'
                elif zxc % 2 == 0:
                    theme = 'dark'
                zxc += 1
                map_file = get_image(x, y, theme)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
