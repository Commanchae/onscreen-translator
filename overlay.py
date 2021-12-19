#https://www.reddit.com/r/Python/comments/ha5aws/a_transparent_overlay_in_pygame/   

import win32api
import win32con
import win32gui
import pygame
import time
import cv2
from main import OnscreenTranslator
from PIL import ImageGrab, Image, ImageOps

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 12)
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), 1)
pygame.display.set_caption("Moving Vehicles")
transparency_color = (255, 192, 203)  # Transparency color
screen.set_colorkey((0,0,0))

# Variables
ost = OnscreenTranslator()
    # Test Rect
exit_rectangle = pygame.Rect(10,10,100,200)
translate_rectangle = pygame.Rect(10,500, 100,200)
# Set window configs.
hwnd = pygame.display.get_wm_info()["window"]
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparency_color), 0, win32con.LWA_COLORKEY)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def getTupleDifferences(tuple1,tuple2):
    return (tuple1[0]-tuple2[0], tuple1[1]- tuple2[1])

running = True
rectangle_list = [exit_rectangle, translate_rectangle]
text_list = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if exit_rectangle.collidepoint((pos)):
                running = False
            if translate_rectangle.collidepoint((pos)):
                print("WORKING")
                image = ImageGrab.grab()
                image = ImageOps.grayscale(image)
                data = ost.getTesseractDataFromImage(image)
                for i in range(len(data["level"])):
                    if data["text"][i] != "":
                        text_list.append((myfont.render(data["text"][i], False, (255,0,0)), (data["left"][i], data["top"][i])))



    screen.fill(transparency_color)  # Transparent background
    
    for rectangle in rectangle_list:
        pygame.draw.rect(screen, (0,0,0,125), rectangle) 
    for item in text_list:
        screen.blit(item[0], (item[1][0], item[1][1]) )
    pygame.display.update()

im.show()