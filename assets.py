import pygame
import os

def load_images(base_path):
    #ТУТ ПАСТРОИМ КАРТИНКИ
    try:
        images = {
            "main_background": pygame.image.load(os.path.join(base_path, "Back_City.png")),
            "couch": pygame.image.load(os.path.join(base_path, "Enemy_Couch.png")),
            #"player": pygame.image.load(os.path.join(base_path, "Player.png")),
            "coffee": pygame.image.load(os.path.join(base_path, "B_coffee.png")),
            "clock": pygame.image.load(os.path.join(base_path, "B_Clock.png")),
            #"office": pygame.image.load(os.path.join(base_path, "Player.png")),
            
        }
        return images
    except pygame.error as e:
        print(f"Ошибка загрузки изображения: {e}")
        return {}