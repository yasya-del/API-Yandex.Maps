import os
import sys

import pygame
import requests


def get_image(s1, s2):
    server_address = 'https://static-maps.yandex.ru/v1?'
    api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
    ll_spn = f'll={x},{y}&spn={s1},{s2}'
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

x, y = map(float, input('Введите координаты объекта: ').split(','))
s1, s2 = map(float, input('Введите масштаб карты: ').split(','))
map_file = get_image(s1, s2)
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
            if s1 <= 20.75:
                s1 += 0.25
            if s2 <= 20.75:
                s2 += 0.25
            print(s1, s2)
            map_file = get_image(s1, s2)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
            print(1)
            if s1 >= 0.252:
                s1 -= 0.25
            if s2 >= 0.252:
                s2 -= 0.25
            print(s1, s2)
            map_file = get_image(s1, s2)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)