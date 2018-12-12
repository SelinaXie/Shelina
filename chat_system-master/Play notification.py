import pygame
def Notification():
    pygame.mix.init()
    sound=pygame.mixer.Sound('qq.wav')
    sound.play()
